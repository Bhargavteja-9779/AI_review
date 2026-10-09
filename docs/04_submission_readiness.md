# 04 — Hostile-editor assessment, compliance audit and readiness

Date: 9 October 2026.

**Overall status: READY FOR AUTHOR REVIEW — *not* READY FOR SUBMISSION.**

No one can guarantee acceptance. The three most likely desk-rejection reasons are listed in Section 1, and Section 4 lists what the authors must do before submitting.

## 1. Hostile-editor and reviewer simulation

| Criterion | Status | Evidence | Required action |
|---|---|---|---|
| A Scope fit (AIR) | PASS | AIR publishes critical surveys of AI techniques; this is an LLM-evaluation methodology review | — |
| B Novelty | CONDITIONAL | No prior review centred on model-originated validity threats was found. Closest: Uluırmak & Kurban 2026 (EvalSafetyGap); deception surveys. Novelty was checked only via web search | Re-run the novelty check in Scopus/WoS/Google Scholar before submission |
| C Reproducible methodology | **FAIL (major)** | Queries logged, but no bibliographic-database search; no hit counts; web-search coverage unknowable | Run `evidence/run_searches.py --execute` (OpenAlex/arXiv/S2/DBLP) and the Scopus API with network access; reconcile with current records |
| D Evidence supports conclusions | CONDITIONAL | Conclusions are hedged and tied to anchor studies, but all values come from abstracts/summaries; some only from secondary summaries | Read full texts of the 37 anchor studies; verify every number in Tables 4–6 |
| E Synthesis rather than listing | PASS | Organised by RQ, framework layers, typed contradictions | — |
| F Framework genuinely useful | PASS (conditional on D) | Explicit layers and assignment rules; explains 4 of 5 contradictions | Expert validation of layer assignments recommended |
| G Comparison validity | PASS | Comparability classes; no pooling or leaderboards | — |
| H Contradictions explained | PASS | Table 6 | — |
| I References genuine and accurate | CONDITIONAL | 159 references, all cited, every citation resolved by script; metadata only as confirmed in search results; some initials missing; no DOI resolution performed | Resolve all identifiers; complete author lists and initials; check versions and venues |
| J Writing | PASS | Clear, hedged, consistent terminology | Native-speaker/author polish |
| K Ethics and declarations | CONDITIONAL | Springer AI policy followed (AI disclosed, not an author); funding/COI/contributions drafted | Authors must confirm every declaration (Section 4) |
| L Author-instruction compliance | CONDITIONAL | Abstract 223 words (limit 150–250 ✓); 4–6 keywords ✓; author-year references; declarations section ✓. Length limits and reference style not verified against the live AIR page | Check the current AIR submission guidelines and apply the Springer LaTeX/Word template |
| M Three most plausible desk-rejection reasons | — | (1) Non-database, abstract-level methodology; (2) evidence base dominated by preprints (66%); (3) extensive AI involvement in conducting the review | Address (1) by the database/full-text update; (2) cannot be changed but is disclosed; (3) is disclosed and requires genuine author verification |

## 2. Final compliance audit

| Area | Check | Status |
|---|---|---|
| Integrity | No fabricated sources, counts or values; quantitative values labelled "as reported" | PASS (as far as checked) |
| Integrity | Novelty claim worded without "first"/"only" | PASS |
| Methods | Queries recorded verbatim (133) | PASS |
| Methods | Database access accurately described (none) | PASS |
| Methods | Counts reconcile: 422 → 4 dup → 418 → 52 excluded + 141 context + 225 charted | PASS (asserted in `screen.py`) |
| Methods | Abstract, Fig. 1, Section 4.1 and supplementary counts agree | PASS (all generated from the same JSON) |
| Methods | Protocol deviations documented | PASS (Section 3.1) |
| References | Citation ↔ reference cross-check | PASS (`manuscript/check_citations.py`) |
| References | DOI resolution / retraction check | NOT TESTED (network blocked) |
| Figures | Numbered by order of appearance; captions; cited in text | PASS |
| Figures | Palette CVD-validated | PASS (contrast WARN relieved by labels and counts in text) |
| Files | DOCX and PDF built; PDF reopened and inspected (42 pages) | PASS |
| Files | Plagiarism/similarity scan | NOT TESTED (no tool available; not claimed) |
| Journal | Current AIR length limit, reference style, template | NOT VERIFIED (official page unreachable) |
| Journal | APC (AIR is fully open access since 2024; amount unverified) | NOT VERIFIED |

## 3. Readiness by dimension

| Dimension | Status | Unresolved risk | Next action |
|---|---|---|---|
| Scientific novelty | Good (provisional) | An overlooked database-indexed review | Database novelty check |
| Journal scope fit | Good | — | — |
| Methodological rigour | Weak | Reviewers may reject a web-search/abstract-level method | Database search + full-text charting + second screener |
| Evidence quality | Moderate | Preprint-heavy; secondary-summary values | Full-text verification |
| Synthesis depth | Good | — | — |
| Framework contribution | Good | Single-layer simplification | Sensitivity check of assignments |
| Reference integrity | Moderate | Incomplete initials; no DOI resolution | Resolve all identifiers |
| Ethical compliance | Conditional | Declarations unconfirmed | Authors confirm |
| Formatting compliance | Conditional | Template not applied | Apply the Springer template |
| File completeness | Good | — | — |

## 4. Author actions before submission (blocking)

1. Confirm or correct the declarations: funding, competing interests, author contributions (CRediT), and data/code availability. If the data are to be deposited, make the GitHub repository public or deposit to Zenodo/OSF and insert the URL or DOI.
2. Confirm the AI-use statement accurately describes how the authors used and verified the AI output, and personally verify the manuscript.
3. With network access, run `python3 evidence/run_searches.py --execute`, then `evidence/dedup.py`. Screen any new records, and update the counts by re-running `screen.py`, `chart.py` and `figures.py`.
4. Obtain full texts of at least the 37 anchor studies and verify every number in Tables 4–6 and Section 4.
5. Resolve every reference against arXiv, the publisher or a DOI; complete initials; update preprints that have since been published.
6. Have a second person independently screen a random 20% sample plus all CONTEXT/INCLUDED borderline records, and report agreement.
7. Check the current AIR author instructions, apply the Springer Nature template, and run a similarity check.
8. Do not submit to more than one journal at a time; ACM Computing Surveys is the contingency only after a decision from AIR.
