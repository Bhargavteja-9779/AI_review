# Scoping Review: Evaluation Awareness, Sandbagging and Observer Effects in LLM Evaluation

**Status (2026-10-09): Stage 1 of 30 complete — design and protocol. NO formal literature search has been executed yet.** No manuscript text exists, by design: the master prompt forbids drafting before the evidence base is established.

Working title: *When Models Know They Are Being Tested: A Scoping Review of Evaluation Awareness, Sandbagging, and Observer Effects as Threats to the Validity of Large Language Model Evaluation*

Primary target: *Artificial Intelligence Review* (Springer). Contingency (resubmission only): *ACM Computing Surveys*. All journal metrics are provisional and **[NOT VERIFIED]** against JCR.

| File | Contents |
|---|---|
| `docs/00_capability_audit.md` | What this environment can and cannot access, plus the recovery route |
| `docs/01_journal_dossier.md` | Journal facts, decision matrix, verification status |
| `docs/02_topic_and_novelty.md` | Candidate topics, pilot novelty scan, previous-review matrix, falsification criteria |
| `docs/03_protocol.md` | Scope, design, RQs, eligibility, search, screening, charting, synthesis |
| `search/queries.json`, `search/run_searches.py` | Formal queries; executor that logs every search (dry run by default) |
| `search/dedup.py` | Deterministic deduplication + count ledger |
| `extraction/` | Charting and screening templates |
| `logs/operations_log.md` | Every operation performed, with result |

## Blocker

This container's egress policy blocks OpenAlex, arXiv, Semantic Scholar, DBLP, Crossref, doi.org and publisher sites. To continue:

1. Allow those hosts in the environment's Network access settings (list in `docs/00_capability_audit.md`).
2. In a fresh session on this branch, run:

```
python3 search/run_searches.py            # dry run: shows exact queries
python3 search/run_searches.py --execute  # executes + logs
python3 search/dedup.py
```

Before executing, replace `REPLACE_WITH_AUTHOR_EMAIL` in `run_searches.py` with a contact address (OpenAlex/arXiv etiquette).
