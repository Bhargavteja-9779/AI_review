#!/usr/bin/env python3
"""Merge database screening (screening/db_screening.csv) with the earlier web-search pass
(evidence/screening.csv via screening/web_vs_db.csv) into the final evidence set.

Rules
  * Records found by both routes: concordant decisions kept; the six discordant records take the
    consensus decision in RESOLVED (re-read title/abstract by both passes).
  * Web-only records keep their web-pass decision; database-only records keep their database decision.
  * Two web entries that resolve to one database record (R01144) are one study (duplicate removed).
  * Charting: web-included studies keep evidence/charting_included.csv; newly included studies are
    charted manually in screening/db_charting_manual.tsv (layer and primary method from title + abstract).
Outputs: evidence/master_included.csv, evidence/master_context.csv, evidence/master_counts.json,
         screening/prisma2020.json
"""
import csv, json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESOLVED = {"arXiv:2602.14457": "INCLUDED", "arXiv:2502.05209": "INCLUDED", "arXiv:2609.11028": "INCLUDED",
            "arXiv:2607.07184": "INCLUDED", "arXiv:2509.16203": "CONTEXT", "arXiv:2605.28825": "INCLUDED"}
WEB_DUPLICATE = {"iclr2026:strategicdishonesty"}  # same study as arXiv:2509.18058 (both -> R01144)
LAYERS = {"L1": "L1 Context signal", "L2": "L2 Awareness", "L3": "L3 Behavioural divergence",
          "L4": "L4 Validity consequence and response"}
METHODS = {"B": "Behavioural contrast (black-box)", "E": "Benchmark / environment construction",
           "R": "Reasoning-trace / transcript monitoring", "W": "White-box (probes, steering, features)",
           "T": "Training- or weight-based (elicitation, organisms)", "A": "Developer or third-party audit"}


def rd(p):
    return list(csv.DictReader((ROOT / p).open()))


def main():
    uniq = {r["record_id"]: r for r in rd("search/records_unique.csv")}
    db = {r["record_id"]: r for r in rd("screening/db_screening.csv")}
    web = rd("screening/web_vs_db.csv")
    charted_web = {r["id"]: r for r in rd("evidence/charting_included.csv")}
    manual = {r["record_id"]: r for r in csv.DictReader((ROOT / "screening/db_charting_manual.tsv").open(), delimiter="\t")}

    final, route = {}, {}  # key -> decision ; key -> identified via
    for w in web:
        if w["id"] in WEB_DUPLICATE:
            continue
        dec = w["decision"]
        if w["db_match"]:
            dbd = db[w["db_match"]]["decision"]
            dec = RESOLVED.get(w["id"], dec) if dec != dbd else dec
            assert dec == dbd or w["id"] in RESOLVED, w["id"]
        final[w["id"]] = dec
        route[w["id"]] = ("both:" + w["db_match"]) if w["db_match"] else "other-methods"
    matched = {w["db_match"] for w in web if w["db_match"]}
    for k, r in db.items():
        if k not in matched and r["decision"] != "DUPLICATE":
            final[k] = r["decision"]
            route[k] = "databases"

    included, context = [], []
    for k, dec in final.items():
        if dec == "INCLUDED":
            if k in charted_web:
                row = dict(charted_web[k])
            else:
                rid = k if k in uniq else route[k].split(":", 1)[1]
                u, m = uniq[rid], manual[rid]
                v = u["venue"] or "preprint"
                stype = "Preprint" if any(s in v.lower() for s in ("arxiv", "medrxiv", "preprint")) else "Peer-reviewed"
                row = {"id": f"arXiv:{u['arxiv_id']}" if u["arxiv_id"] else (f"doi:{u['doi']}" if u["doi"] else rid),
                       "title": u["title"], "first_author_or_org": (u["authors"].split(";")[0] or "NR").strip(),
                       "year": u["year"], "venue_or_type": v, "source_type": stype,
                       "framework_layer": LAYERS[m["layer"]], "method_family": METHODS[m["method"]],
                       "scope_area": m["note"], "read_level": "title/abstract (database record)"}
            row["identified_via"] = route[k].split(":")[0]
            row["db_record_id"] = k if route[k] == "databases" else (route[k].split(":", 1)[1] if ":" in route[k] else "")
            included.append(row)
        elif dec == "CONTEXT":
            context.append({"key": k, "identified_via": route[k].split(":")[0]})

    def dump(name, rows):
        with (ROOT / name).open("w", newline="") as f:
            w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    dump("evidence/master_included.csv", included)
    dump("evidence/master_context.csv", context)

    counts = {
        "n": len(included),
        "by_identified_via": Counter(o["identified_via"] for o in included),
        "by_layer": Counter(o["framework_layer"] for o in included),
        "by_method": Counter(o["method_family"] for o in included),
        "by_type": Counter(o["source_type"] for o in included),
        "by_year": Counter(o["year"] for o in included),
        "by_year_type": {y: Counter(o["source_type"] for o in included if o["year"] == y)
                         for y in sorted({o["year"] for o in included})},
        "layer_x_method": {l: Counter(o["method_family"] for o in included if o["framework_layer"] == l)
                           for l in sorted({o["framework_layer"] for o in included})},
        "context_n": len(context),
    }
    (ROOT / "evidence/master_counts.json").write_text(json.dumps(counts, indent=2, default=dict))

    # PRISMA 2020 flow (databases column and other-methods column)
    ledger = json.load((ROOT / "search/count_ledger.json").open())
    # records found by both routes count once, in the databases column
    dbcol = Counter()
    for k, r in db.items():
        if r["decision"] == "DUPLICATE":
            continue
        webk = [w["id"] for w in web if w["db_match"] == k and w["id"] not in WEB_DUPLICATE]
        dbcol[final[webk[0]] if webk else final[k]] += 1
    stage = Counter((r["stage"], r["decision"]) for r in db.values())
    oth = Counter(final[w["id"]] for w in web if not w["db_match"])
    othcode = Counter(w["code"] for w in web if not w["db_match"] and w["decision"] == "EXCLUDED")
    prisma = {
        "databases": {
            "identified_by_source": ledger["records_by_source"], "identified_total": ledger["total_before_dedup"],
            "duplicates_removed_automatic": ledger["duplicates_removed"],
            "version_duplicates_removed_manual": stage[("version-merge", "DUPLICATE")],
            "records_screened": sum(dbcol.values()),
            "excluded_stage1_rule": stage[("stage1-rule", "EXCLUDED")],
            "excluded_rescue_screen": stage[("rescue", "EXCLUDED")],
            "excluded_stage2_title_abstract": stage[("stage2", "EXCLUDED")],
            "final_excluded": dbcol["EXCLUDED"], "final_context": dbcol["CONTEXT"], "final_included": dbcol["INCLUDED"],
        },
        "other_methods": {
            "identified_web_batches": 422, "duplicates_within_web": 4, "web_records": len(web),
            "already_retrieved_by_databases": sum(1 for w in web if w["db_match"]),
            "records_assessed": sum(oth.values()), "excluded_by_code": othcode,
            "final_context": oth["CONTEXT"], "final_included": oth["INCLUDED"],
        },
        "total_included": len(included), "total_context": len(context),
    }
    assert prisma["databases"]["final_included"] + prisma["other_methods"]["final_included"] == len(included)
    assert prisma["databases"]["identified_total"] - ledger["duplicates_removed"] - prisma["databases"]["version_duplicates_removed_manual"] == prisma["databases"]["records_screened"]
    (ROOT / "screening/prisma2020.json").write_text(json.dumps(prisma, indent=2, default=dict))
    print(json.dumps(prisma, indent=2, default=dict)); print(json.dumps(counts, indent=1, default=dict)[:1500])


if __name__ == "__main__":
    main()
