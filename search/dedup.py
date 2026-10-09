#!/usr/bin/env python3
"""Deduplicate search/records_raw.csv (never modified) into search/records_unique.csv.

Rules, applied in order:
  1. identical DOI
  2. identical arXiv id (version stripped)
  3. identical normalized title + year
  4. normalized-title similarity >= 0.93 -> flagged for manual inspection only
     (conference vs. journal versions etc.), NOT auto-merged.
Writes duplicates.csv (with the rule that matched), manual_check.csv and count_ledger.json.
"""
import csv
import difflib
import json
import pathlib
import re
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent


def norm_title(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def main():
    rows = list(csv.DictReader((HERE / "records_raw.csv").open()))
    keep, dups, seen = [], [], {}
    for r in rows:
        keys = []
        if r["doi"]:
            keys.append(("doi", r["doi"].strip().lower()))
        if r["arxiv_id"]:
            keys.append(("arxiv", re.sub(r"v\d+$", "", r["arxiv_id"].strip())))
        nt = norm_title(r["title"])
        if nt:
            keys.append(("title_year", f"{nt}|{r['year']}"))
        hit = next(((k, seen[k]) for k in keys if k in seen), None)
        if hit:
            master = keep[hit[1]]
            master["sources"] = ";".join(sorted(set(master["sources"].split(";")) | {r["source"]}))
            for f in ("doi", "arxiv_id", "venue"):
                if not master[f] and r[f]:
                    master[f] = r[f]
            dups.append({**r, "rule": hit[0][0], "kept_id": master["record_id"]})
        else:
            r = {**r, "record_id": f"R{len(keep)+1:05d}", "sources": r["source"]}
            keep.append(r)
            idx = len(keep) - 1
        for k in keys:
            seen.setdefault(k, hit[1] if hit else idx)

    titles = [norm_title(r["title"]) for r in keep]
    # blocked fuzzy comparison: only compare titles sharing their first two significant tokens
    blocks = {}
    for i, t in enumerate(titles):
        toks = [w for w in t.split() if len(w) > 3][:2]
        if t and toks:
            blocks.setdefault(" ".join(toks), []).append(i)
    manual = []
    for idx in blocks.values():
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                sm = difflib.SequenceMatcher(None, titles[i], titles[j])
                if sm.quick_ratio() >= 0.93 and sm.ratio() >= 0.93:
                    manual.append({"a": keep[i]["record_id"], "b": keep[j]["record_id"],
                                   "title_a": keep[i]["title"], "title_b": keep[j]["title"]})

    def dump(name, data):
        if not data:
            (HERE / name).write_text("")
            return
        with (HERE / name).open("w", newline="") as f:
            w = csv.DictWriter(f, list(data[0].keys()))
            w.writeheader()
            w.writerows(data)

    dump("records_unique.csv", keep)
    dump("duplicates.csv", dups)
    dump("manual_check.csv", manual)
    by_source = {}
    for r in rows:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    ledger = {"records_by_source": by_source, "total_before_dedup": len(rows),
              "duplicates_removed": len(dups), "unique_after_dedup": len(keep),
              "pairs_flagged_for_manual_check": len(manual)}
    assert ledger["total_before_dedup"] == ledger["duplicates_removed"] + ledger["unique_after_dedup"]
    (HERE / "count_ledger.json").write_text(json.dumps(ledger, indent=2))
    print(json.dumps(ledger, indent=2))


if __name__ == "__main__":
    main()
