# 03 — Scoping Review Protocol (v0.1, frozen pending pilot test of the formal queries)

Protocol date: 2026-10-09. Not registered. (OSF registration is feasible for scoping reviews; PROSPERO does not accept them. **Registration has not occurred and must not be claimed.**)

## 1. Review design

**Selected:** scoping review, reported per PRISMA-ScR (Tricco et al., 2018; citation to be verified).

**Justification:**
- The terminology is inconsistent (evaluation awareness / situational awareness / test awareness / observer effect / evaluation faking / sandbagging / under-elicitation).
- The field reports lacking a shared conceptual basis.
- The evidence is mainly recent preprints, with heterogeneous designs.
- The objective is to map concepts, measurement methods and gaps, not to pool effect sizes.

**Rejected alternatives:**
- *Systematic review with meta-analysis*: outcomes and metrics are not commensurable.
- *Bibliometric review*: citation patterns are not the research question.
- *Pure critical review*: weaker reproducibility than the field now allows.

## 2. Scope

| Element | Definition |
|---|---|
| Core technology | Large language models and LLM-based agents (incl. multimodal foundation models when the LLM is the evaluated component) |
| Phenomenon | Model behaviour or internal state that depends on whether the model is (or infers it is) being evaluated, tested, trained or monitored; and deliberate or induced underperformance on evaluations |
| Evaluation boundary | Capability, safety, alignment and dangerous-capability evaluations |
| Period | 2019-01-01 to search date |
| Sources | Peer-reviewed papers, conference papers, preprints (arXiv, OpenReview, SSRN), and technical reports/system cards from model developers and evaluation organizations (charted separately as grey literature) |
| Language | English (a limitation; stated) |
| Explicitly excluded | Training-data contamination and benchmark leakage (data-side, not model-strategic); human-participant Hawthorne effects; reward hacking/specification gaming with no evaluation-context conditionality; general deception studies with no link to evaluation validity |

## 3. Research questions

| RQ | Question | Evidence fields | Planned output |
|---|---|---|---|
| RQ1 | How are evaluation awareness, sandbagging, alignment/evaluation faking and related constructs defined and operationalized? | Construct name, definition text, operationalization, induced vs. emergent | Concept map (Fig. 2); terminology table |
| RQ2 | What methods detect or measure these phenomena, and what validity evidence supports each? | Method family, access level (black/grey/white-box), ground-truth source, validation reported, failure cases | Measurement taxonomy (Table 5) + validity-evidence matrix |
| RQ3 | Under which model, task and context conditions are the phenomena observed, and where do findings conflict? | Models, scale, families, environment cues, effect direction/size as reported, comparability class | Evidence map + contradiction table (Table 7) |
| RQ4 | Which countermeasures have been proposed (realism engineering, steering/suppression, perturbation-based detection, fine-tuning elicitation, probes), and how rigorously are they evaluated? | Countermeasure, threat addressed, evaluation design, robustness to adaptive models | Countermeasure matrix |
| RQ5 | Which gaps most threaten the validity of current evaluation practice, and which studies would resolve them? | Derived from RQ1–4 | Gap matrix + prioritized agenda + reporting checklist |

A question counts as answered when every included study is charted on its fields and the output artefact is complete. If RQ4 has fewer than 5 studies it is merged into RQ5 (a documented deviation).

## 4. Eligibility

**Include:**
- (I1) a primary empirical study, a methodological/benchmark paper, or a developer/third-party evaluation report; that
- (I2) measures, induces, detects or mitigates evaluation-context-dependent behaviour or strategic/induced underperformance in LLMs or LLM agents; and
- (I3) reports enough method detail to chart RQ2 fields.

**Exclude:**
- (E1) out-of-scope phenomenon (§2);
- (E2) no LLM;
- (E3) position/opinion piece with no method or data (kept as background only);
- (E4) duplicate or superseded version (keep the most complete; link versions);
- (E5) non-English;
- (E6) full text unavailable (listed separately, not silently dropped).

## 5. Information sources and search

| Source | Access route | Status |
|---|---|---|
| OpenAlex (broad multidisciplinary index; covers arXiv) | REST API | Script ready; **not executed** |
| arXiv (cs.CL, cs.AI, cs.LG, cs.CR) | export API | Script ready; **not executed** |
| Semantic Scholar | Graph API bulk search | Script ready; **not executed** |
| DBLP | search API | Script ready; **not executed** |
| ACL Anthology, OpenReview (ICLR/NeurIPS/ICML) | via OpenAlex/S2 coverage + targeted checks | Planned |
| Scopus, Web of Science | Licensed | **Unavailable — will be stated as a limitation** |
| Grey literature: system cards / evaluation reports (Anthropic, OpenAI, Google DeepMind, Meta, UK AISI, Apollo Research, METR, Frontier Model Forum) | Targeted site searches | Planned; logged separately |
| Citation chaining | Backward + forward from included studies (S2 API) | Planned; logged separately |

### Concept blocks

- **A (system):** "language model*" OR LLM OR LLMs OR "foundation model*" OR "frontier model*" OR "AI agent*" OR "AI system*"
- **B (phenomenon):** "evaluation awareness" OR "eval awareness" OR "test awareness" OR "evaluation-awareness" OR "situational awareness" OR sandbagging OR sandbag OR "strategic underperformance" OR "alignment faking" OR "evaluation faking" OR "observer effect" OR "evaluation gaming" OR "under-elicitation" OR "capability elicitation" OR "password-locked" OR "hidden capabilities" OR scheming
- **C (evaluation context; applied only with the broad B-terms situational awareness / scheming / capability elicitation):** evaluat* OR benchmark* OR test* OR assess* OR audit*

Formal query = A AND (B_specific OR (B_broad AND C)). The source-specific syntax is in `search/queries.json`.

**Pilot:** the WebSearch scan of 2026-10-09 (`logs/operations_log.md`) surfaced the term variants above. After the first executed run, any new recurring term found in included titles is added, and the change is logged as a protocol amendment.

## 6. Selection

Three stages: title → abstract → full text, with one primary exclusion reason at full text.

This is a single-reviewer, AI-assisted process, so **no claim of dual independent screening** is made. Safeguards:
- a piloted rubric on the first 50 records;
- a 20% random re-screen after 7 days, with agreement reported;
- every decision logged in `extraction/screening_log.csv`;
- a human author is asked to validate a random sample and all borderline cases before submission.

## 7. Charting (extraction)

Template: `extraction/charting_template.csv`. N/R = not reported; N/A = not applicable. Every row is tied to the exact version read (arXiv vN / DOI) and to whether it was read as full text or abstract only.

## 8. Critical appraisal

Scoping reviews do not require risk-of-bias appraisal. Because RQ2/RQ3 concern validity, a **descriptive evaluation-rigour profile** is charted (not a score), with 8 binary/ternary items:
1. ground truth for awareness/sandbagging defined;
2. control condition present;
3. more than one model family;
4. variance/uncertainty reported;
5. prompts/environments released;
6. code released;
7. adaptive/adversarial model considered;
8. confound between evaluation cues and task difficulty addressed.

The items are applied per study with a rationale. They are not aggregated into a quality score or used for exclusion.

## 9. Synthesis

- Descriptive counts (year, venue type, model families, access level).
- Framework-based synthesis using the four-layer framework (`02_topic_and_novelty.md`), revised inductively.
- Each finding is classified as directly / conditionally / non-comparable before any cross-study statement.
- Contradictions are typed (genuine / context-dependent / metric artefact / methodological artefact / insufficient evidence).
- No pooled effect sizes and no leaderboard.

## 10. Planned deviations log

None yet.

## Amendment v0.2 (9 October 2026)

Bibliographic APIs stayed blocked in this environment. The user then asked for the full review to be completed with the tools available. Amendments:
1. **Information source:** the session's web-search tool replaced the database APIs; all 133 queries are logged verbatim (`evidence/search_log.md`).
2. **Design label:** "structured critical review with scoping-style evidence map"; PRISMA-ScR compliance is not claimed.
3. **Scope:** broadened from evaluation awareness and sandbagging to *model-originated threats to evaluation validity*. This adds alignment/evaluation faking, strategic dishonesty, evaluator gaming and the detection, elicitation and suppression methods. Data-side contamination stays out of scope.
4. **Exclusion codes:** E6 (unverifiable metadata) and E3 (non-archival forum posts) were added; a CONTEXT category was added for eligible but out-of-boundary publications.
5. **Charting:** at abstract or summary level only (no full texts), with a 37-study anchor set charted in detail.
6. **Appraisal:** no risk-of-bias scores; reported design features are charted instead.
