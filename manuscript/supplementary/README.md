# Supplementary material

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
