# 04 — Hostile-editor assessment, compliance audit and readiness

Date: 9 October 2026 (after the database phase, full-text checks, reference verification, reporting audit and an internal referee review).

**Overall status: READY FOR AUTHOR REVIEW AND THE HUMAN AUDIT — not yet ready for submission.** No one can guarantee acceptance; the items in Section 4 are what stands between the current manuscript and a defensible submission.

## 1. Internal referee review and response

An internal referee review (simulating an expert AIR reviewer) recommended *major revision* and raised 13 major and 46 minor issues. Response:

| Issue | Status | What was done |
|---|---|---|
| M1 Full-text claim vs released data | Fixed | Read level and arXiv version recorded for all 37 anchors (S3b, S4a); Methods state that the AI system performed the full-text checks with verbatim evidence |
| M2 Protocol deviations | Fixed | Amendments v0.2 (web) and v0.3 (database) and post-hoc revisions written into the protocol (S0); deviations listed in Section 3.1 |
| M3 Eligibility differed by route | Fixed | One written tier rule applied to all 315 charted studies; evidence map reported for the 167 core studies; 148 adjacent studies reported separately |
| M4 AI role / reliability labels | Partly fixed | AI role stated in Methods, Limitations and AI-use statement; κ relabelled as consistency. **Open: a human audit (Section 4, item 1)** |
| M5 PRISMA arithmetic | Fixed | Automation-tool exclusions shown separately; all numbers reconcile (script-generated) |
| M6 Search recall | Fixed | Recall reported (83.8% of indexable core studies; 33/37 anchors) with diagnosed causes of misses; arXiv 1732 vs 1721 explained (date limit) |
| M7 Source-type coding | Fixed | Archival / workshop / preprint / grey, re-coded against verified venues |
| M8 Layer rules and Fig. 4 | Fixed | Mutually exclusive L1/L4 rule; Fig. 4 shows a direct cue-reactive path; rule–manual disagreements named |
| M9 Formal section | Fixed | Assumptions A1–A2, awareness inside the policy, support condition, elicitation term, order dependence; propositions recast as remarks; abstract corrected |
| M10 Overclaims | Fixed | Conclusion, measurement-bias statements, probe confound, Schoen confound, Jang, Ward and Table 7 row corrected |
| M11 Unverified numbers | Fixed | Non-anchor numbers marked † |
| M12 Circular anchor set | Fixed (text) | Selection described honestly; anchor statistics labelled as describing the anchor set |
| M13 PRISMA-ScR items | Fixed | Completed checklist (S6); abstract restructured; consultation stage stated as not undertaken |
| Minor 1–46 | Mostly fixed | Numbers, labels, citation keys, URLs/access dates, OpenReview IDs, definitions. Not done: reading every prior review in full (Table 1 caption states abstract-level judgement) |

## 2. Hostile-editor table (current)

| Criterion | Status | Evidence | Remaining action |
|---|---|---|---|
| Scope fit (AIR) | PASS | Methodological review of LLM evaluation validity | — |
| Novelty | PASS (provisional) | Closest prior review (Maurya et al. 2026) covers 15 studies to 2024; database novelty check done | — |
| Reproducible methodology | PASS with caveat | Three databases, frozen query, raw responses, scripts reproduce every count | Human audit (Section 4) |
| Evidence supports conclusions | PASS with caveat | Anchor claims checked against full texts (16 corrections); non-anchor numbers flagged | Authors spot-check anchor checks |
| Synthesis, framework, formalism | PASS | Formal decomposition, estimand table, worked examples, discriminating tests for every contradiction | — |
| Reporting-practice evidence | PASS | Full-text audit with independent double coding (κ = 0.90, AI coders) | — |
| References | PASS | 182 references verified against arXiv, OpenReview, Crossref and publisher pages | — |
| Declarations | CONDITIONAL | Drafted; AI use disclosed in detail | Authors confirm |
| Three most likely desk-rejection reasons | — | (1) AI-performed screening without a human check; (2) preprint-dominated evidence; (3) length (about 12k words of text) | (1) Section 4 item 1; (2) disclosed, cannot change; (3) check AIR limits, move Tables 4–5 or Section 4.8 to supplementary if needed |

## 3. Compliance audit

| Area | Check | Status |
|---|---|---|
| Integrity | No fabricated sources, counts or values; every count script-generated | PASS |
| Integrity | AI role disclosed accurately (no claim of human screening) | PASS |
| Methods | PRISMA 2020 flow reconciles; PRISMA-ScR checklist complete (S6) | PASS |
| Methods | Protocol and amendments released (S0) | PASS |
| References | Citation ↔ reference cross-check (`manuscript/check_citations.py`) | PASS |
| References | Identifier resolution (arXiv API, Crossref, OpenReview) | PASS |
| Figures | Five figures, numbered by first appearance, inspected | PASS |
| Files | DOCX and PDF built (PDF via MathML, equations render) | PASS |
| Similarity scan | Not available in this environment | NOT TESTED |
| Journal | Current AIR length limit and template | NOT VERIFIED |

## 4. Author actions before submission (blocking)

1. **Human audit (most important).** Complete `screening/human_audit/screening_sample.csv` (100 records) and `tier_sample.csv` (60 studies) without looking at the hidden AI columns, run `python3 screening/human_audit/agreement.py`, and report human–AI κ in Sections 3.4 and 7. If agreement is low, re-screen accordingly.
2. Spot-check at least 5 anchor studies' full-text checks (`evidence/anchor_set.tsv` against the arXiv versions in S3b).
3. Confirm every declaration (funding, competing interests, CRediT roles, AI use). Add a sentence that the authors verified the manuscript only after doing so.
4. Make the repository public and archive it on Zenodo; insert the DOI in the Data availability statement.
5. Check the current AIR author instructions (length, reference style, template) and run a similarity check.
6. Submit to one journal at a time; ACM Computing Surveys is the contingency only after a decision from AIR.
