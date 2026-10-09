# Operations Log

| # | Date (UTC) | Operation | Result | Artefact |
|---|---|---|---|---|
| 1 | 2026-10-09 | Repo inspection | Empty repo; no topic or files supplied | — |
| 2 | 2026-10-09 | Capability audit (curl, WebFetch, WebSearch) | Bibliographic APIs and publisher sites blocked by egress policy; WebSearch works (summaries only) | docs/00_capability_audit.md |
| 3 | 2026-10-09 | Asked user for topic + network decision | User: agent picks a "unique" topic; user will widen network access | — |
| 4 | 2026-10-09 | Re-test after user answer | Still blocked (new container needed) | — |
| 5 | 2026-10-09 | Pilot novelty scan — WebSearch (NOT a database search; result counts not recorded because the tool returns summaries) | Queries: (a) "survey OR systematic review chain-of-thought faithfulness measurement metrics LLM reasoning 2025"; (b) "systematic review statistical rigor uncertainty reporting significance testing in LLM evaluation papers"; (c) "survey evaluation awareness sandbagging LLM capability elicitation underperformance review"; (d) "\"evaluation awareness\" language models survey OR review OR taxonomy 2026"; (e) "survey capability elicitation under-elicitation dangerous capability evaluations validity threats frontier models review paper"; (f) "survey \"alignment faking\" OR \"scheming\" OR \"strategic deception\" large language models evaluations review 2025 2026" | docs/02_topic_and_novelty.md |
| 6 | 2026-10-09 | Journal scouting — WebSearch | AIR and ACM CSUR facts gathered from summaries; JCR not accessible | docs/01_journal_dossier.md |
| 7 | 2026-10-09 | Protocol v0.1 written | Scoping review (PRISMA-ScR); 5 RQs | docs/03_protocol.md |
| 8 | 2026-10-09 | Search + dedup scripts written; dry run OK; dedup tested on a 5-row synthetic fixture (outside repo) | No real search executed | search/ |
| 9 | 2026-10-09 | User supplied authors and a Scopus key; requested full completion with no placeholders | Network still blocked (Scopus key could not be used; not stored in repo); the account's only environment is the restricted default | — |
| 10 | 2026-10-09 | Evidence collection: 25 WebSearch batches + 1 verification batch (133 queries total) | 422 records identified | evidence/search_log.md, candidates.tsv, register.jsonl |
| 11 | 2026-10-09 | Dedup + rule-based screening | 4 duplicates; 418 screened; 19 E6, 12 E1, 21 E3 excluded; 141 context; 225 charted | evidence/screen.py, screening.csv, prisma_counts.json |
| 12 | 2026-10-09 | Charting and framework assignment; 37-study anchor set | Layer and method counts | evidence/chart.py, charting_included.csv, anchor_set.tsv |
| 13 | 2026-10-09 | Figures (palette CVD-validated) | 4 figures | evidence/figures.py, manuscript/figures |
| 14 | 2026-10-09 | Manuscript drafted; 159 references; citation cross-check passes | DOCX + PDF (42 pp), inspected | manuscript/ |
| 15 | 2026-10-09 | Cover letter, hostile-editor assessment, compliance audit | READY FOR AUTHOR REVIEW (not submission) | manuscript/cover_letter.*, docs/04_submission_readiness.md |
