#!/usr/bin/env python3
"""Database screening pipeline (Section 3.4). Reproduces, from search/records_unique.csv and the recorded manual
decisions, every file in screening/ that feeds screening/merge.py.

  1. Version merge: exact-title version pairs flagged in search/manual_check.csv (second record dropped).
  2. Stage 1: records whose title+abstract match none of the phenomenon terms (STRICT) are rule-excluded.
     Audit: AUDIT_N random stage-1 exclusions (seed 20261009) -> stage1_audit_sample.txt (read manually).
  3. Rescue pass: RESCUE pattern applied to all stage-1 exclusions -> rescue_candidates.tsv, screened manually
     (rescue_decisions.txt).
  4. Stage 2: STRICT matches screened manually on title/abstract (decisions.txt, "<n><I|C|E>").
  5. Cross-check with the web-search pass (evidence/screening.csv) -> web_vs_db.csv, interpass_agreement.json.
"""
import csv, json, pathlib, random, re, unicodedata
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
STRICT = (r"evaluation[- ]aware|eval[- ]aware|test[- ]aware|aware (that|when|of being) (it is |they are )?(being )?(evaluated|tested)|"
          r"know(s)? (when|that) (they are|it is) being (evaluated|tested)|sandbag|strategic(ally)? underperform|password[- ]lock|"
          r"hidden capabilit|capability elicitation|under-?elicit|alignment[- ]faking|evaluation[- ]faking|fak(e|ing) alignment|"
          r"deceptive(ly)? align|\bscheming\b|\bscheme(s)? against|strategic(ally)? (deception|deceptive|dishonest|deceiv|lie|lying)|"
          r"situational awareness|reward hack|specification gaming|reward tamper|observer effect|hawthorne|evaluation gaming|"
          r"gaming (the )?evaluat|benchmark gaming|covert(ly)? (action|sabotage)|sabotage evaluation|exploration hacking")
RESCUE = (r"defeat device|deceiv|decept|dishonest|\blie(s)?\b|lying|elicit|underperform|\bmonitor(s|ing)? (for|of)? ?(misbehav|misalign|"
          r"reasoning|chain|cot|agent)|probe(s)? (for|detect)|unfaithful|faithful(ness)? of (chain|cot|reason)|backdoor|sleeper|obfuscat|"
          r"covert|sabotag|self[- ]aware|introspect|self[- ]recogni|evaluation validity|construct validity|ecological validity|"
          r"(know|recogni[sz]e|detect)s? (when|that) (it|they) (is|are) being|being watched|unmonitored|oversight evasion|"
          r"evade (oversight|monitor)")
AUDIT_N, SEED = 120, 20261009
CODE = {"I": "INCLUDED", "C": "CONTEXT", "E": "EXCLUDED"}


def nt(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def text(r):
    return (r["title"] + " " + r.get("abstract", "")).lower()


def write(name, rows, fields, delim=","):
    with (HERE / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fields, delimiter=delim, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def main():
    uniq = {r["record_id"]: r for r in csv.DictReader((ROOT / "search/records_unique.csv").open())}
    drop = {p["b"] for p in csv.DictReader((ROOT / "search/manual_check.csv").open())}
    (HERE / "version_merge.json").write_text(json.dumps({"version_duplicates_merged": len(drop)}))
    rows = [r for k, r in uniq.items() if k not in drop]

    stage2 = sorted((r for r in rows if re.search(STRICT, text(r))), key=lambda r: (r["year"], r["title"]))
    s2ids = {r["record_id"] for r in stage2}
    stage1 = [r for r in rows if r["record_id"] not in s2ids]
    with (HERE / "stage2_candidates.tsv").open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["n", "record_id", "year", "title", "venue", "abstract_head"])
        for i, r in enumerate(stage2, 1):
            w.writerow([i, r["record_id"], r["year"], r["title"], r["venue"][:40], " ".join(r.get("abstract", "").split()[:45])])
    write("stage1_excluded.csv", stage1, ["record_id", "year", "title", "sources"])

    resc = sorted((r for r in stage1 if re.search(RESCUE, text(r))), key=lambda r: r["title"])
    with (HERE / "rescue_candidates.tsv").open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["m", "record_id", "year", "title", "abstract_head"])
        for i, r in enumerate(resc, 1):
            w.writerow([i, r["record_id"], r["year"], r["title"], " ".join(r.get("abstract", "").split()[:28])])

    dec2 = {int(m.group(1)): m.group(2) for m in re.finditer(r"(\d+)([ICE])", (HERE / "decisions.txt").read_text())}
    assert sorted(dec2) == list(range(1, len(stage2) + 1)), "decisions.txt must cover every stage-2 candidate"
    rtxt = (HERE / "rescue_decisions.txt").read_text()
    decr = {int(m.group(1)): m.group(2) for m in re.finditer(r"(\d+)([IC])\b", rtxt)}
    dec = {r["record_id"]: dec2[i] for i, r in enumerate(stage2, 1)}
    dec.update({r["record_id"]: decr.get(i, "E") for i, r in enumerate(resc, 1)})
    rids = {r["record_id"] for r in resc}

    out = []
    for k, r in uniq.items():
        stage = "version-merge" if k in drop else ("stage2" if k in s2ids else ("rescue" if k in rids else "stage1-rule"))
        d = "DUPLICATE" if k in drop else CODE[dec.get(k, "E")]
        out.append({**r, "stage": stage, "decision": d})
    write("db_screening.csv", out, ["record_id", "sources", "doi", "arxiv_id", "title", "year", "venue", "stage", "decision"])

    # cross-check with the web-search pass
    keys = {}
    for r in out:
        if r["decision"] == "DUPLICATE":
            continue
        if r["arxiv_id"]: keys["ax:" + re.sub(r"v\d+$", "", r["arxiv_id"].lower())] = r
        if r["doi"]: keys["doi:" + r["doi"].lower()] = r
        keys["t:" + nt(r["title"])] = r
    web = [w for w in csv.DictReader((ROOT / "evidence/screening.csv").open()) if w["decision"] != "DUPLICATE"]
    for w in web:
        i = w["id"]; k = []
        if i.lower().startswith("arxiv:"): k.append("ax:" + i[6:].lower())
        if i.lower().startswith("doi:"): k.append("doi:" + i[4:].lower())
        k.append("t:" + nt(w["title"]))
        hit = next((keys[x] for x in k if x in keys), None)
        w["db_match"] = hit["record_id"] if hit else ""; w["db_decision"] = hit["decision"] if hit else ""
    write("web_vs_db.csv", web, list(web[0].keys()))
    pairs = [(w["decision"], w["db_decision"]) for w in web if w["db_match"]]
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / n / n
    (HERE / "interpass_agreement.json").write_text(json.dumps({
        "overlap_n": n, "agreement": round(po, 3), "cohen_kappa": round((po - pe) / (1 - pe), 3),
        "note": "agreement between web-metadata screening pass (first) and database title/abstract screening pass (second) "
                "on records identified by both; discordant n=%d resolved by consensus re-reading" % sum(a != b for a, b in pairs)}, indent=1))

    random.seed(SEED)
    sample = random.sample(stage1, AUDIT_N)
    print("unique", len(uniq), "| version dups", len(drop), "| stage2", len(stage2), "| stage1 excl", len(stage1),
          "| rescue", len(resc), "| audit sample", len(sample))
    print(Counter((r["stage"], r["decision"]) for r in out))
    print("interpass", n, round(po, 3), round((po - pe) / (1 - pe), 3))


if __name__ == "__main__":
    main()
