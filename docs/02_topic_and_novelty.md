# 02 — Topic Selection and Novelty Dossier (PILOT STAGE)

No topic was supplied. On 2026-10-09 the user asked the agent to choose "something more unique, very impressive". Selection rests on a **pilot novelty scan via WebSearch** (summarized results; not a bibliographic-database search). The formal novelty gate is re-run against the full executed search before drafting.

## Candidates considered

| Candidate | Existing reviews found in pilot | Verdict |
|---|---|---|
| Chain-of-thought faithfulness measurement | "The Mirage of Explainability: A Survey on CoT Faithfulness in LLMs" (PKU-PILLAR, ~Jan 2026); "A Comprehensive Survey on Trustworthiness in Reasoning with LLMs" (arXiv 2509.03871); FaithCoT-Bench (ICLR 2026) | Rejected — recently surveyed |
| Statistical rigor in LLM evaluation | No dedicated review found; arXiv 2506.18082 contains a partial practice survey | Possible, but weaker AI-technical fit for AIR |
| LLM benchmark contamination / LLM-as-judge | Several surveys published 2024–2025 (from background knowledge; not re-verified) | Rejected — crowded |
| **Evaluation awareness, sandbagging and observer effects as threats to the validity of LLM evaluations** | **None found.** Adjacent: Park et al. 2024 (*Patterns*, AI-deception survey); "From Hallucination to Scheming" (arXiv 2604.04788, deception taxonomy + benchmark mapping); Frontier Model Forum "Frontier Capability Assessments" technical report (2025) | **Selected** |

## Working title

*When Models Know They Are Being Tested: A Scoping Review of Evaluation Awareness, Sandbagging, and Observer Effects as Threats to the Validity of Large Language Model Evaluation*

## Why now (pilot evidence; all items are arXiv preprints or lab reports unless noted, and **unverified until full text is read**)

- A body of 2025–2026 primary work exists. Examples: the AI Sandbagging paper (ICLR 2025); "Evaluation Awareness Scales Predictably" (arXiv 2509.13333); "Decomposing and Measuring Evaluation Awareness" (2605.23055); "Evaluation Awareness Is Not One Capability" (2606.23583, 37 models); "Evaluation Awareness in LMs: Representation, Verbalization, and Control" (2608.21766); EvalDetectBench (2609.01611); "…Shifts from Format to Context with Model Scale" (2609.22119); "Strategic Dishonesty Can Undermine AI Safety Evaluations" (ICLR 2026); "Evaluation Faking" (2505.17815); prompted-sandbagging detection preprints (2604.25249, 2604.26206); "Elicitation Floors" (SSRN).
- The field itself reports **no shared conceptual foundation**. 2605.23055 describes work conflating properties of the evaluation with properties of the model, and detection with behavioural response. That calls for a scoping design.
- There is an **apparent contradiction** to explain. One paper reports predictable (power-law) scaling of evaluation awareness (2509.13333); another argues it is a set of weakly coupled aspects, not one capability (2606.23583).
- The practical stakes are clear. Frontier-lab and third-party system cards now report evaluation-awareness and sandbagging tests, yet their methods are heterogeneous.

## Preliminary previous-review comparison (to be completed from full texts)

| Review | Year / status | Focus | Covers eval awareness as a validity threat? | Measurement-method taxonomy? | Gap left for this review |
|---|---|---|---|---|---|
| Park et al., "AI deception: A survey of examples, risks, and potential solutions" | 2024, *Patterns* (peer-reviewed; metadata NOT VERIFIED) | Deception broadly | Predates most of the literature | No | Not evaluation-centred; pre-2025 |
| "From Hallucination to Scheming" (arXiv 2604.04788) | 2026, preprint | Deception taxonomy + benchmark mapping | Partially (as one behaviour) | Benchmarks, not measurement validity | No validity framework for evaluations themselves |
| Frontier Model Forum, "Frontier Capability Assessments" | 2025, industry technical report | Assessment practice | Elicitation and validity, in general terms | No systematic evidence map | Not a systematic or scoping review |
| CoT-faithfulness surveys | 2025–2026 | Faithfulness of reasoning traces | Only indirectly (verbalized awareness relies on CoT) | Faithfulness metrics | Different construct |

## Proposed contribution (conditional on the executed search)

1. The first *systematically searched* evidence map of model-side threats to evaluation validity. ("First" is claimed only if the formal search finds no prior review.)
2. A conceptual framework separating (a) the **evaluation-context signal** (properties of the environment), (b) **awareness** (representation / verbalization), (c) **behavioural divergence** (sandbagging, alignment/evaluation faking, refusal shifts), and (d) the **validity consequence** for the reported score.
3. A taxonomy of measurement methods (behavioural contrast, verbalized-CoT classification, white-box probes and steering, model organisms such as password-locking, weight/noise perturbation, fine-tuning elicitation), with the validity evidence each carries.
4. A structured analysis of contradictions (e.g. the scaling claims).
5. An evidence-graded research agenda and a reporting checklist for evaluation papers and system cards.

## Falsification criteria (what would kill or narrow the novelty claim)

- A published survey or systematic review whose primary focus is evaluation awareness or sandbagging → narrow to measurement validity of detection methods, or to the system-card/grey-literature evidence.
- Fewer than ~25 eligible primary studies after full-text screening → convert to a structured critical review, and say so.
- More than ~250 eligible studies → restrict to studies with an explicit evaluation-vs-deployment manipulation.
