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
| 16 | 2026-10-09 | Network opened (new container). Database searches executed: Scopus (API key via environment variable only, never stored), arXiv, Semantic Scholar; OpenAlex (HTTP 429 quota) and DBLP (anti-bot page) failed and were logged | 5649 records (244 / 1721 / 3684) | search/run_searches.py, search/raw/, search/logs/search_log.csv |
| 17 | 2026-10-09 | Deduplication (blocked fuzzy matching) and version merge | 1796 duplicates; 3853 unique; 30 version pairs merged | search/dedup.py, search/records_unique.csv |
| 18 | 2026-10-09 | Two-stage screening with audited stage-1 rule (1/120 false negatives) and rescue pass (399 records) | 166 included, 157 context, 3500 excluded (after reconciliation) | screening/screen_db.py, screening/db_screening.csv |
| 19 | 2026-10-09 | Reconciliation with the web pass (90 overlapping records) | Agreement 93.3%, kappa 0.747; 6 discordant resolved | screening/web_vs_db.csv, screening/interpass_agreement.json |
| 20 | 2026-10-09 | Merge and PRISMA 2020 two-column flow; manual charting of 91 newly included studies; duplicate web entry removed | 315 included studies | screening/merge.py, screening/prisma2020.json, evidence/master_included.csv |
| 21 | 2026-10-09 | Full texts of the 37 anchor studies downloaded from arXiv and every manuscript claim about them checked (five parallel checks) | 158 claims: 142 supported, 16 corrected; all 37 anchor rows re-charted | evidence/anchor_set.tsv |
| 22 | 2026-10-09 | Reference verification: arXiv API (authors, titles, dates), OpenReview (venues), Crossref (DOIs), conference pages (workshop papers) | 181 references; 4 venue misattributions to main conferences corrected to workshops; published versions cited | manuscript/references.py |
| 23 | 2026-10-09 | Formal decomposition of evaluation error and estimand table added; PDF pipeline switched to MathML + Chromium | Equations render | manuscript/sections/03_results.md, manuscript/build.py |
