#!/usr/bin/env python3
"""Assemble manuscript/supplementary/ from the evidence, search and screening outputs (no hand-edited counts)."""
import csv, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "manuscript" / "supplementary"
for f in OUT.glob("*"):
    f.unlink()

COPY = {
    "S0_protocol_and_amendments.md": "docs/03_protocol.md",
    "S3b_anchor_fulltext_versions.json": "evidence/anchor_versions.json",
    "S4e_tier_coding.csv": "evidence/tier_coding.csv",
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
    "S5a_reporting_audit_codebook.md": "evidence/reporting_audit/codebook.md",
    "S5b_reporting_audit_codes.csv": "evidence/reporting_audit/audit_primary.csv",
    "S5c_reporting_audit_summary.json": "evidence/reporting_audit/audit_summary.json",
}
import zipfile
with zipfile.ZipFile(OUT / "S5d_reporting_audit_coder_files.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted((ROOT / "evidence/reporting_audit").glob("coder_*.json")):
        z.write(f, f.name)
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

checklist = """# S6 PRISMA-ScR checklist (Tricco et al. 2018) with locations in the manuscript

| # | Item | Location |
|---|---|---|
| 1 | Title | Title page (identified as a scoping review) |
| 2 | Structured summary | Abstract (objectives, sources, eligibility, charting, results, limitation, conclusions) |
| 3 | Rationale | Section 1 |
| 4 | Objectives | Section 1 (RQ1–RQ5) |
| 5 | Protocol and registration | Section 3.1; Supplementary File S0 (protocol v0.1, amendments v0.2 and v0.3, post-hoc revisions; not registered) |
| 6 | Eligibility criteria | Section 3.2; Table 2; tier rule |
| 7 | Information sources | Section 3.3; S1b (dates, sources, failed sources) |
| 8 | Search | Section 3.3; S1a (web queries); S1b and S1f (full database strategies) |
| 9 | Selection of sources of evidence | Section 3.4 (deduplication, automation tool, manual screening, who screened, consistency checks) |
| 10 | Data charting process | Section 3.5; S3, S4d, S4e |
| 11 | Data items | Section 3.5 |
| 12 | Critical appraisal of individual sources | Sections 3.7 and 3.8 (design features; reporting audit) |
| 13 | Synthesis of results | Section 3.7 (comparability classes; contradiction typing) |
| 14 | Selection of sources of evidence (results) | Section 4.1; Fig. 1 |
| 15 | Characteristics of sources of evidence | Section 4.1; Figs. 2–3; S4a |
| 16 | Critical appraisal within sources of evidence | Section 5.4; Fig. 5; S5 |
| 17 | Results of individual sources of evidence | Table 6; S3 |
| 18 | Synthesis of results | Sections 4.2–4.9; Tables 3–7 |
| 19 | Summary of evidence | Section 5.1 |
| 20 | Limitations | Section 7 |
| 21 | Conclusions | Section 8 |
| 22 | Funding | Declarations |
"""
(OUT / "S6_PRISMA-ScR_checklist.md").write_text(checklist)

readme = """# Supplementary material

| File | Content |
|---|---|
| S0_protocol_and_amendments.md | Protocol v0.1, amendments v0.2 (web phase) and v0.3 (database phase), and post-hoc revisions reported as deviations |
| S3b_anchor_fulltext_versions.json | arXiv version of each anchor full text read (retrieved 9 Oct 2026) |
| S4e_tier_coding.csv | Core/adjacent tier of every charted study under the written tier rule |
| S6_PRISMA-ScR_checklist.md | Completed PRISMA-ScR checklist with locations |
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
| S5a_reporting_audit_codebook.md | Frozen codebook for the reporting audit (12 items, applicability rules) |
| S5b_reporting_audit_codes.csv | Primary codes (37 studies x 12 items) |
| S5c_reporting_audit_summary.json | Adherence per item and per study; inter-coder agreement |
| S5d_reporting_audit_coder_files.zip | All coder files with the verbatim evidence for every code, including the independent second coding |

Raw API responses are in `search/raw/`. To reproduce all counts and figures from the repository root:
`python3 search/dedup.py && python3 screening/screen_db.py && python3 evidence/screen.py && python3 evidence/chart.py &&
python3 screening/merge.py && python3 screening/reliability.py && python3 evidence/figures.py &&
python3 evidence/reporting_audit/analyse.py && python3 manuscript/make_supplementary.py`
(the database search itself is re-run with `python3 search/run_searches.py --execute`; Scopus requires `ELSEVIER_API_KEY`).
"""
(OUT / "README.md").write_text(readme)
print(sorted(p.name for p in OUT.iterdir()))
