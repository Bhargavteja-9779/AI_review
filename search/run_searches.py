#!/usr/bin/env python3
"""Execute and log the formal searches defined in queries.json.

Default is a dry run that prints the exact query sent to each source.
With --execute it calls each API, saves the raw responses under search/raw/,
appends one row per executed search to search/logs/search_log.csv, and writes
normalized records to search/records_raw.csv for dedup.py.

Standard library only; outbound HTTPS honours HTTPS_PROXY / SSL_CERT_FILE.
"""
import argparse
import csv
import datetime as dt
import json
import pathlib
import time
import urllib.parse
import urllib.request
import urllib.error
import os
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw"
LOG = HERE / "logs" / "search_log.csv"
RECORDS = HERE / "records_raw.csv"
UA = "AI-review-scoping/0.2 (academic literature review; VIT Vellore)"

LOG_FIELDS = ["run_id", "database", "platform", "search_date_utc", "query", "request_url",
              "fields_searched", "date_range", "filters", "language", "document_types",
              "records_returned", "records_reported_by_source", "export_file", "notes"]
REC_FIELDS = ["source", "source_id", "doi", "arxiv_id", "title", "authors", "year", "venue", "type", "abstract"]


def q(term):
    return f'"{term}"' if " " in term or "-" in term else term


def or_block(terms):
    return "(" + " OR ".join(q(t) for t in terms) + ")"


def boolean_query(cfg):
    a, bs, bb, c = (or_block(cfg[k]) for k in ("A", "B_specific", "B_broad", "C"))
    return f"{a} AND ({bs} OR ({bb} AND {c}))"


def get(url, accept="application/json", headers=None, tries=8):
    h = {"User-Agent": UA, "Accept": accept, **(headers or {})}
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and k < tries - 1:
                time.sleep(min(60, 3 * 2 ** k)); continue
            raise


# ---------- OpenAlex ----------
def openalex(cfg, execute, run_id):
    query = boolean_query(cfg)
    flt = f"title_and_abstract.search:{query},from_publication_date:{cfg['date_from']}"
    base = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"filter": flt, "per-page": 200})
    if not execute:
        return query, base, []
    recs, cursor, pages, total = [], "*", [], None
    while cursor:
        data = json.loads(get(base + "&cursor=" + urllib.parse.quote(cursor)))
        total = data["meta"]["count"]
        pages.append(data)
        for w in data["results"]:
            ids = w.get("ids", {})
            arx = ""
            for loc in w.get("locations") or []:
                lid = (loc.get("landing_page_url") or "")
                if "arxiv.org/abs/" in lid:
                    arx = lid.rsplit("/", 1)[-1]
            recs.append({"source": "OpenAlex", "source_id": w["id"],
                         "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower(),
                         "arxiv_id": arx, "title": w.get("title") or "",
                         "authors": "; ".join(a["author"]["display_name"] for a in w.get("authorships", [])),
                         "year": w.get("publication_year") or "",
                         "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
                         "type": w.get("type") or ""})
        cursor = data["meta"].get("next_cursor")
        if not data["results"]:
            break
        time.sleep(0.2)
    out = RAW / f"{run_id}_openalex.json"
    out.write_text(json.dumps(pages))
    return query, base, recs, total, out.name


# ---------- arXiv ----------
def arxiv(cfg, execute, run_id):
    def field_or(terms):
        return "(" + " OR ".join(f'abs:{q(t)}' for t in terms) + ")"
    cats = "(" + " OR ".join(f"cat:{c}" for c in cfg["arxiv_categories"]) + ")"
    query = f"{field_or(cfg['A'])} AND ({field_or(cfg['B_specific'])} OR ({field_or(cfg['B_broad'])} AND {field_or(cfg['C'])})) AND {cats}"
    base = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": query, "sortBy": "submittedDate", "sortOrder": "descending"})
    if not execute:
        return query, base, []
    ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/",
          "x": "http://arxiv.org/schemas/atom"}
    recs, start, total, chunks = [], 0, None, []
    while total is None or start < total:
        xml = get(base + f"&start={start}&max_results=200", "application/atom+xml")
        chunks.append(xml.decode())
        root = ET.fromstring(xml)
        total = int(root.find("o:totalResults", ns).text)
        entries = root.findall("a:entry", ns)
        if not entries:
            break
        for e in entries:
            aid = e.find("a:id", ns).text.rsplit("/", 1)[-1]
            year = e.find("a:published", ns).text[:4]
            if year < cfg["date_from"][:4]:
                continue
            doi = e.find("x:doi", ns)
            recs.append({"source": "arXiv", "source_id": aid, "doi": (doi.text.lower() if doi is not None else ""),
                         "arxiv_id": aid.split("v")[0], "title": " ".join(e.find("a:title", ns).text.split()),
                         "authors": "; ".join(a.find("a:name", ns).text for a in e.findall("a:author", ns)),
                         "year": year, "venue": "arXiv", "type": "preprint",
                         "abstract": " ".join((e.find("a:summary", ns).text or "").split())})
        start += len(entries)
        time.sleep(3.1)  # arXiv API etiquette
    out = RAW / f"{run_id}_arxiv.xml"
    out.write_text("\n<!-- page break -->\n".join(chunks))
    return query, base, recs, total, out.name


# ---------- Semantic Scholar ----------
def s2(cfg, execute, run_id):
    def ob(terms):
        return "(" + " | ".join(f'"{t}"' for t in terms) + ")"
    query = f"{ob(cfg['A'])} + ({ob(cfg['B_specific'])} | ({ob(cfg['B_broad'])} + {ob(cfg['C'])}))"
    base = "https://api.semanticscholar.org/graph/v1/paper/search/bulk?" + urllib.parse.urlencode(
        {"query": query, "year": cfg["date_from"][:4] + "-",
         "fields": "title,authors,year,venue,externalIds,publicationTypes,abstract"})
    if not execute:
        return query, base, []
    recs, token, pages, total = [], None, [], None
    while True:
        data = json.loads(get(base + (f"&token={token}" if token else "")))
        pages.append(data)
        total = data.get("total")
        for p in data.get("data", []):
            ext = p.get("externalIds") or {}
            recs.append({"source": "SemanticScholar", "source_id": p["paperId"],
                         "doi": (ext.get("DOI") or "").lower(), "arxiv_id": ext.get("ArXiv") or "",
                         "title": p.get("title") or "",
                         "authors": "; ".join(a.get("name", "") for a in p.get("authors") or []),
                         "year": p.get("year") or "", "venue": p.get("venue") or "",
                         "type": ",".join(p.get("publicationTypes") or []), "abstract": p.get("abstract") or ""})
        token = data.get("token")
        if not token:
            break
        time.sleep(1.1)
    out = RAW / f"{run_id}_s2.json"
    out.write_text(json.dumps(pages))
    return query, base, recs, total, out.name


# ---------- DBLP (no boolean OR: one query per specific term) ----------
def dblp(cfg, execute, run_id):
    queries = [f"{t}" for t in cfg["B_specific"]]
    base = "https://dblp.org/search/publ/api?format=json&h=1000&q="
    if not execute:
        return " || ".join(queries), base + "<term>", []
    recs, raw = [], {}
    for t in queries:
        data = json.loads(get(base + urllib.parse.quote(t)))
        raw[t] = data
        for h in (data["result"]["hits"].get("hit") or []):
            i = h["info"]
            au = i.get("authors", {}).get("author", [])
            au = au if isinstance(au, list) else [au]
            ee = i.get("ee", "")
            ee = ee if isinstance(ee, str) else (ee[0] if ee else "")
            recs.append({"source": "DBLP", "source_id": i.get("key", ""), "doi": (i.get("doi") or "").lower(),
                         "arxiv_id": ee.rsplit("/", 1)[-1] if "arxiv.org/abs/" in ee else "",
                         "title": i.get("title", ""), "authors": "; ".join(a.get("text", "") for a in au),
                         "year": i.get("year", ""), "venue": i.get("venue", "") if isinstance(i.get("venue"), str) else "",
                         "type": i.get("type", "")})
        time.sleep(1.0)
    recs = [r for r in recs if str(r["year"]) >= cfg["date_from"][:4]]
    out = RAW / f"{run_id}_dblp.json"
    out.write_text(json.dumps(raw))
    return " || ".join(queries), base + "<term>", recs, len(recs), out.name


# ---------- Scopus (Elsevier Search API; key from ELSEVIER_API_KEY, never stored) ----------
def scopus(cfg, execute, run_id):
    def ob(terms):
        return "(" + " OR ".join(f'"{t}"' if (" " in t or "-" in t) else t for t in terms) + ")"
    a = ob([t.replace("language models", "language model*").replace("LLMs", "LLM*") for t in cfg["A"]])
    query = (f"TITLE-ABS-KEY({a} AND ({ob(cfg['B_specific'])} OR ({ob(cfg['B_broad'])} AND {ob(cfg['C'])}))) "
             f"AND PUBYEAR > {int(cfg['date_from'][:4]) - 1}")
    base = "https://api.elsevier.com/content/search/scopus?" + urllib.parse.urlencode({"query": query, "count": 25})
    if not execute:
        return query, base, []
    key = os.environ["ELSEVIER_API_KEY"]
    recs, start, total, pages = [], 0, None, []
    while total is None or start < min(total, 5000):
        data = json.loads(get(base + f"&start={start}", headers={"X-ELS-APIKey": key}))["search-results"]
        pages.append(data)
        total = int(data["opensearch:totalResults"])
        entries = [e for e in data.get("entry", []) if "error" not in e]
        if not entries:
            break
        for e in entries:
            recs.append({"source": "Scopus", "source_id": e.get("eid", ""), "doi": (e.get("prism:doi") or "").lower(),
                         "arxiv_id": "", "title": e.get("dc:title", ""), "authors": e.get("dc:creator", ""),
                         "year": (e.get("prism:coverDate") or "")[:4], "venue": e.get("prism:publicationName", ""),
                         "type": e.get("subtypeDescription", "")})
        start += len(entries)
        time.sleep(0.5)
    out = RAW / f"{run_id}_scopus.json"
    out.write_text(json.dumps(pages))
    return query, base, recs, total, out.name


SOURCES = {"OpenAlex": (openalex, "api.openalex.org", "title_and_abstract"),
           "arXiv": (arxiv, "export.arxiv.org API", "abstract (abs:) incl. title"),
           "SemanticScholar": (s2, "api.semanticscholar.org bulk search", "title+abstract (S2 default)"),
           "DBLP": (dblp, "dblp.org search API", "title/metadata"),
           "Scopus": (scopus, "Elsevier Scopus Search API", "TITLE-ABS-KEY")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="actually call the APIs")
    ap.add_argument("--only", nargs="*", choices=list(SOURCES))
    args = ap.parse_args()
    cfg = json.loads((HERE / "queries.json").read_text())
    RAW.mkdir(exist_ok=True)
    LOG.parent.mkdir(exist_ok=True)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    all_recs = []
    new_log = not LOG.exists()
    with LOG.open("a", newline="") as lf:
        w = csv.DictWriter(lf, LOG_FIELDS)
        if new_log and args.execute:
            w.writeheader()
        for name in args.only or SOURCES:
            fn, platform, fields = SOURCES[name]
            if not args.execute:
                query, url, _ = fn(cfg, False, run_id)
                print(f"== {name} ==\nQUERY: {query}\nURL:   {url}\n")
                continue
            try:
                query, url, recs, total, fname = fn(cfg, True, run_id)
                note = ""
            except Exception as e:  # record the failure; never invent a count
                query, url, recs, total, fname, note = "", "", [], "", "", f"FAILED: {e!r}"
                print(f"{name}: {note}")
            w.writerow({"run_id": run_id, "database": name, "platform": platform,
                        "search_date_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                        "query": query, "request_url": url, "fields_searched": fields,
                        "date_range": f"{cfg['date_from']} to search date", "filters": "arXiv: cs.CL/AI/LG/CR" if name == "arXiv" else "none",
                        "language": "no filter (English screened at stage 2)", "document_types": "all",
                        "records_returned": len(recs), "records_reported_by_source": total,
                        "export_file": fname, "notes": note})
            all_recs += recs
            print(f"{name}: {len(recs)} records (source reports {total})")
    if args.execute:
        with RECORDS.open("w", newline="") as f:
            w = csv.DictWriter(f, REC_FIELDS, restval="")
            w.writeheader()
            w.writerows(all_recs)
        print(f"wrote {len(all_recs)} records to {RECORDS}")


if __name__ == "__main__":
    main()
