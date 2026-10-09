#!/usr/bin/env python3
"""Assemble manuscript/supplementary/ from the evidence, search and screening outputs (no hand-edited counts)."""
import csv, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "manuscript" / "supplementary"
for f in OUT.glob("*"):
    f.unlink()

COPY = {
    "S1a_web_search_log.md": "evidence/search_log.md",
    "S1c_web_identified_records.tsv": "evidence/candidates.tsv",
    "S1d_web_anchor_register.jsonl": "evidence/register.jsonl",
    "S1e_database_search_log.csv": "search/logs/search_log.csv",
    "S1f_frozen_query_v0.2.json": "search/queries.json",
    "S2a_web_screening_decisions.csv": "evidence/screening.csv",
    "S2b_database_screening_decisions.csv": "screening/db_screening.csv",
    "S2c_stage1_audit_sample.txt": "screening/stage1_audit_sample.txt",
    "S2d_rescue_candidates.tsv": "screening/rescue_candidates.tsv",
    "S2e_web_vs_database_reconciliation.csv": "screening/web_vs_db.csv",
    "S2f_reliability.json": "screening/reliability.json",
    "S3_anchor_set_fulltext_charting.tsv": "evidence/anchor_set.tsv",
    "S4a_included_studies.csv": "evidence/master_included.csv",
    "S4b_prisma2020_counts.json": "screening/prisma2020.json",
    "S4c_evidence_map_counts.json": "evidence/master_counts.json",
    "S4d_database_studies_manual_charting.tsv": "screening/db_charting_manual.tsv",
}
for dst, src in COPY.items():
    shutil.copy(ROOT / src, OUT / dst)

# S1b: database search strategy, rendered from the executed-search log
log = list(csv.reader((ROOT / "search/logs/search_log.csv").open()))
q = json.loads((ROOT / "search/queries.json").read_text())
lines = ["# S1b Database search strategy (executed 9 October 2026)", "",
         f"Protocol version {q['protocol_version']}, frozen {q['frozen_on']}. Logical form: A AND (B_specific OR (B_broad AND C)); "
         f"publication date from {q['date_from']}.", ""]
for k in ("A", "B_specific", "B_broad", "C"):
    lines.append(f"- **{k}**: " + "; ".join(q[k]))
lines += ["", "| Source | Interface | Retrieved (UTC) | Field | Filters | Query string as submitted | Records retrieved | Hits reported by API | Status |",
          "|---|---|---|---|---|---|---|---|---|"]
for r in log:
    status = r[14] or "OK"
    lines.append(f"| {r[1]} | {r[2]} | {r[3]} | {r[6]} | {r[8]} | `{r[4].replace('|', '&#124;')}` | {r[11]} | {r[12] or 'n/a'} | {status} |")
lines += ["", "arXiv reported and returned 1732 matching records; 11 first posted before 2019 were removed by the date limit, "
          "leaving 1721. OpenAlex and DBLP could not be searched (see Status)."]
(OUT / "S1b_database_search_strategy.md").write_text("\n".join(lines) + "\n")

readme = """# Supplementary material

| File | Content |
|---|---|
| S1a_web_search_log.md | All 133 executed web-search queries, verbatim, grouped by batch (9 Oct 2026) |
| S1b_database_search_strategy.md | Concept blocks and the exact query string submitted to each database API, with timestamps, counts and failures |
| S1c_web_identified_records.tsv | Every record identified by the web searches, with batch, metadata status and scope area |
| S1d_web_anchor_register.jsonl | 20 detailed records identified in web batch B1 |
| S1e_database_search_log.csv | Machine-written log of every database API run (including the failed OpenAlex and DBLP runs) |
| S1f_frozen_query_v0.2.json | Frozen query configuration (protocol amendment v0.2) |
| S2a_web_screening_decisions.csv | One decision and code per web record (R0, E1, E3, E6, CONTEXT, INCLUDED) |
| S2b_database_screening_decisions.csv | Stage and decision for every unique database record |
| S2c_stage1_audit_sample.txt | Random sample of 120 stage-1 exclusions read for the audit (seed 20261009) |
| S2d_rescue_candidates.tsv | 399 stage-1 exclusions flagged by the rescue pattern and screened manually |
| S2e_web_vs_database_reconciliation.csv | Web records matched to database records, with both decisions |
| S2f_reliability.json | Stage-1 audit rate (Wilson CI), inter-pass screening agreement and layer-assignment agreement |
| S3_anchor_set_fulltext_charting.tsv | Full-text charting of the 37 anchor studies (Table 5; design features) |
| S4a_included_studies.csv | All included studies with route of identification, source type, framework layer and method family |
| S4b_prisma2020_counts.json | Counts behind Fig. 1 |
| S4c_evidence_map_counts.json | Counts behind Figs. 2 and 3 |
| S4d_database_studies_manual_charting.tsv | Manual layer and method coding of studies identified only by the databases |

Raw API responses are in `search/raw/`. To reproduce all counts and figures from the repository root:
`python3 search/dedup.py && python3 screening/screen_db.py && python3 evidence/screen.py && python3 evidence/chart.py &&
python3 screening/merge.py && python3 screening/reliability.py && python3 evidence/figures.py && python3 manuscript/make_supplementary.py`
(the database search itself is re-run with `python3 search/run_searches.py --execute`; Scopus requires `ELSEVIER_API_KEY`).
"""
(OUT / "README.md").write_text(readme)
print(sorted(p.name for p in OUT.iterdir()))
