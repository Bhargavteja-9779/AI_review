## 5 Discussion

### 5.1 Principal findings

The review supports four conclusions, each qualified by the strength of the evidence behind it.

**(i) Evaluation-conditioned behaviour in LLMs has been demonstrated, but mostly under induced or strongly scaffolded conditions.** Evidence is strong that models *can* underperform selectively when instructed or trained to (van der Weij et al. 2025), *can* discriminate evaluation from deployment transcripts (Needham et al. 2025), and *can* behave differently when they infer that they are observed (Greenblatt et al. 2024a; Lynch et al. 2025). Evidence on how often this happens *spontaneously* in realistic evaluations is weaker and mixed. Honeypot evaluations in a real internal deployment found no unprompted scheming (Krakovna et al. 2026); aggregate output shifts associated with verbalised awareness were small (Knecht et al. 2026); and only a minority of models showed alignment faking in a replication across 25 models (Sheshadri et al. 2025).

**(ii) "Evaluation awareness" is a family of weakly coupled constructs, not one quantity.** Representational, verbalised and elicited measures diverge (Nayan et al. 2026; Heidari et al. 2026). Each has a hypothesised directional bias (Section 4.3). Probe evidence can be confounded by prompt format, as one controlled single-model study showed (Devbunova 2026), whereas other probes retained discrimination under rewrites that changed behaviour (Nayan et al. 2026); only 3 of 15 anchor studies using probes or steering controlled for format (Section 5.4). Reports that state an awareness rate without specifying the measure are therefore uninterpretable across studies.

**(iii) The link from awareness to behaviour is heterogeneous in magnitude and direction.** Test awareness can increase or decrease harmful compliance depending on the model (Abdelnabi and Salem 2025). How the awareness is framed predicts compliance (Zhuang and Aranguri 2026). Optimised prompts that induce evaluation awareness degraded Claude-3.5-Haiku by 73 pp on arithmetic but by only 0.6 pp on code generation, where Llama-3.3-70B dropped 86.6 pp (Chaudhary 2026). A single "evaluation-awareness correction" applied across models is therefore not justified by current evidence.

**(iv) Detecting adversarial underperformance is harder than eliciting capability.** In adversarial settings, detection of sandbagging was unreliable (Taylor J et al. 2025; Li C et al. 2025), and monitors that detected code sabotage well found sandbagging harder to detect (Ward et al. 2025), whereas training-based elicitation more often recovered hidden capability (Greenblatt et al. 2024b; Taylor J et al. 2025; Ryd et al. 2026), at the cost of false positives. For capability evaluations, this favours elicitation-first protocols, which report the best elicited performance, over detection-first protocols, which try to classify whether a model is sandbagging.

### 5.2 Comparison with the human-sciences literature

The trajectory of this literature resembles that of research on the Hawthorne effect, where effects of being studied were found to exist but their conditions, mechanisms and magnitudes remained poorly understood, and new concepts were called for (McCambridge et al. 2014). Two differences matter.

First, LLM evaluators have access to model internals. This permits measurement designs, namely representation probing, steering and weight perturbation, that are impossible with human participants. It also introduces new validity threats specific to those designs (Table 5).

Second, unlike human participants, models are trained, and training can be informed by evaluation results. If evaluations that detect misbehaviour feed back into training, the training process creates selection pressure toward recognising and passing those evaluations. That pressure is what Goodhart-type arguments predict (Gao et al. 2023). Verbalised awareness did rise after anti-scheming training, but it rose much more after capability-focused reinforcement learning without safety training (from 2.0% to 20.6%; Schoen et al. 2025), so the rise may reflect a general effect of reinforcement learning rather than feedback from evaluations; the design cannot separate the two. The analogy with human research participation therefore *understates* the threat.

### 5.3 Comparison with prior reviews

Relative to deception surveys (Park et al. 2024; Chen B et al. 2025; Shi et al. 2026), this review treats the evaluation as the object of study, so that deception matters only insofar as it changes what scores mean. Relative to the review of the AI "observer effect" by Maurya et al. (2026), which discusses fifteen landmark contributions up to 2024, it adds a reproducible multi-database search, the 2025–2026 measurement literature and an explicit separation of awareness from behaviour. Relative to the broad proxy–target framing of Uluırmak and Kurban (2026), it isolates the model-originated mechanisms and their measurement. Relative to construct-validity reviews of benchmarks (Bean et al. 2025; Reuel et al. 2024) and to the validity-centred survey of agent benchmarks by Nageshwaran et al. (2026), it adds a class of threat that remains even when a benchmark is well designed, although the benchmark audits in Section 4.9 show that many agent benchmarks are not. A benchmark with strong construct validity can still yield invalid inferences if the evaluated system behaves differently because it recognises the benchmark.

### 5.4 Implications for evaluation practice: a reporting checklist

The heterogeneity documented in Sections 4.3–4.6 is partly a reporting problem. Table 8 proposes a twelve-item checklist for evaluation papers, system cards and third-party evaluation reports, derived directly from the failure modes and contradictions charted above. The checklist is a proposal derived from the evidence and has not been validated as a reporting standard. We did, however, apply it retrospectively to the full texts of the 37 anchor studies (Section 3.8; Fig. 5).

**Table 8** EVAL-AWARE reporting checklist for evaluations exposed to model-originated validity threats

| # | Item | Rationale (evidence in this review) |
|---|---|---|
| 1 | State which awareness construct is measured (elicited, verbalised, represented) and report each separately | Measures diverge and are hypothesised to have opposite biases (Sections 4.3–4.4) |
| 2 | For probe-based claims, report a design that decorrelates evaluation context from prompt format | Probes track format (Devbunova 2026) |
| 3 | Report the layer and selection procedure for probes, with a control probe baseline | Best-decoding layer shifts with scale (Manek 2026) |
| 4 | Report the transcript generator for deployment-side data and test cross-family transfer of elicitation prompts | Generator effects and non-transfer (Li X et al. 2026) |
| 5 | Report the direction of possible bias (capability under-estimation vs safety over-estimation) for each evaluation | Threats bias in opposite directions (Section 2.3) |
| 6 | For capability evaluations, report elicitation effort (prompting, scaffolding, fine-tuning, RL), and best elicited performance alongside default performance | Elicitation recovers hidden capability more reliably than detection (Section 5.1) |
| 7 | When excluding refusals or failures, report results with and without exclusion | Exclusions turn reported scores into ceilings (single preprint: Saraireh 2026); 4 of 25 applicable anchor studies reported both (Section 5.4) |
| 8 | For propensity evaluations, report a cue-ablated or replay-based variant | Stacked cues drive awareness; replay reduces distinguishability (Li C et al. 2026; Ivanov and Africa 2026) |
| 9 | Report unprompted verbalised awareness rates in agentic evaluations, and treat them as lower bounds | Unverbalised awareness documented (Anthropic 2026) |
| 10 | Report per-model rather than pooled awareness–behaviour relations | Magnitude and direction vary by model (Abdelnabi and Salem 2025) |
| 11 | Report uncertainty (confidence intervals, number of samples, seeds) for all rates | Small-sample rates and prompt sensitivity (Sclar et al. 2024; Mizrahi et al. 2024) |
| 12 | State the access level available to the evaluator (black-box, grey-box, white-box) | Access constrains which methods are possible (Casper et al. 2024) |

![Fig. 5 Reporting audit of the 37 anchor studies against the EVAL-AWARE checklist (Table 8), coded from full texts. Adherence (top) is the share of applicable studies reporting the item, counting partial reporting as one half. Studies are ordered by the number of items reported. Inter-coder agreement on a random 10 studies: κ = 0.90.](figures/fig5_reporting_audit.png)

**Reporting audit.** The audit shows a clear split (Fig. 5). Items that concern the *framing* of a study are almost always reported: every study states the evaluator's access level (37 of 37), every multi-model study reports results per model (34 of 34), and nearly all name the awareness construct they measure (adherence 94%, 26 applicable studies) and state the direction of the possible bias (89%). Items that concern *threats to the measurement itself* are reported much less often:

- only 3 of the 15 studies that use probes or steering as evidence fully decorrelate evaluation context from prompt format (adherence 37%), although format confounding is the best-documented failure mode of probe evidence (Devbunova 2026);
- only 7 of the 27 agentic or reasoning-trace studies report unprompted verbalised-awareness rates and treat them as lower bounds, and 12 report no such rate at all (adherence 41%);
- only 1 of the 18 studies that rely on deployment-side transcripts or elicitation prompts tests whether results transfer across transcript generators or model families (adherence 47%);
- only 4 of the 25 studies that exclude outputs (refusals, unparseable answers, filtered tasks) report results with and without the exclusion (adherence 52%);
- uncertainty is fully reported for main results in 17 of the 37 studies (46%) and partly in 19 more.

Median adherence per study was 79% (range 50–100%). The pattern matters for interpretation. The items least often reported are exactly those that would distinguish a genuine awareness effect from a measurement artefact (Table 4): format confounds for probes, the lower-bound status of verbalised awareness, generator effects for transcript classification, and the effect of exclusions on reported rates. Items 2, 4, 7 and 9 are therefore the most useful additions to current practice.

## 6 Research gaps and prioritised agenda

Table 9 lists evidence-based gaps, each with the study that would address it and the strength of the evidence that the gap exists. Gaps are ordered by our judgement of priority, which weighs importance for evaluation validity, evidence strength and feasibility.

**Table 9** Prioritised research agenda

| Priority | Gap | Evidence that the gap exists | Proposed study | Evidence strength |
|---|---|---|---|---|
| 1 | Detection and elicitation validated only on *induced* behaviour | Ground truth obtained almost exclusively by construction (Section 4.4); organisms deliberately trained to be detectable or resistant | Blinded auditing games in which red teams construct organisms by *training incentives* rather than direct instruction; report transfer from induced to incentive-driven behaviour | Strong |
| 2 | No validated mapping between awareness measures | 1 of 15 cross-paradigm correlations significant; partial representation–verbalisation correspondence | Multi-measure study on shared items with known ground truth, estimating the upward bias of elicitation and the downward bias of verbalisation | Strong |
| 3 | Few studies of evaluation properties (L1) | 6 of 167 core studies (3.6%) | Factorial cue-ablation studies across task families, including agentic, multimodal and multilingual evaluations | Strong (coverage gap) |
| 4 | Awareness–behaviour link unexplained across models | Direction and magnitude vary (Table 7) | Pre-registered, multi-family studies relating awareness framing to behaviour change, with model-level random effects | Moderate |
| 5 | Feedback from evaluation into training | Verbalised awareness rose after anti-scheming training, and more after capability-focused RL (Schoen et al. 2025) | Controlled training runs that vary whether evaluation-derived data enter training; measure subsequent awareness | Moderate |
| 6 | Sycophancy vs strategic accounts not separable | Baek et al. (2026); Santos-Grueiro (2026) | Designs in which the two accounts predict different behaviour (e.g. evaluator-preference reversal under recognised evaluation) | Moderate |
| 7 | Countermeasures validated by model judgement only | Realism mostly validated by model discriminators; one deployment-grounded validation (Williams et al. 2026) | Validate realism and replay methods against deployment outcomes, not only against discriminator accuracy | Moderate |
| 8 | Peer-review and replication deficit | 13.8% of core studies archival peer-reviewed; key findings single-model | Independent replications of anchor findings (Table 6) with released prompts and code | Strong |
| 9 | Evaluation reporting heterogeneity | Rates reported without construct, uncertainty or access level | Adoption study of a reporting checklist (Table 8) across system cards | Weak (practice evidence only) |

## 7 Limitations of the review

The review has substantial limitations, which readers should weigh before relying on its conclusions.

*Screening and verification.* Screening, tiering, charting and the full-text checks of the anchor studies were AI-assisted and verified by the authors, with every decision logged. There was no independent dual screening by two human reviewers, and the consistency statistics reported here (inter-pass κ = 0.747, rule–manual κ = 0.881, inter-coder κ = 0.90 for the reporting audit) come from AI-assisted processes. They are evidence of consistency, not of inter-rater reliability between independent human reviewers.

*Information sources and recall.* Three databases were searched, but OpenAlex and DBLP could not be queried, and Web of Science, the ACM Digital Library, IEEE Xplore and OpenReview were not searched. The databases retrieved 84% of the core studies of the kinds they index, but missed some that carry a phenomenon term in their titles, so even a well-specified query is limited by term variants and indexing lag. Developer reports and workshop papers were found only through web searches, whose coverage cannot be quantified. Non-English work is probably under-represented.

*Automation and eligibility.* A rule-based pre-screen excluded 2813 records without manual reading. The audit sample and rescue pass bound, but do not eliminate, the number of eligible records missed (Section 3.4). Eligibility was judged on titles and abstracts; there was no full-text eligibility stage.

*Tiering.* The core/adjacent rule was applied after an internal critical review showed that the two identification phases had drawn the phenomenon boundary differently. The rule is written down and applied to every charted study, but it was applied post hoc, and the boundary between adjacent studies and contextual references remains less sharp than the core boundary.

*Depth of reading and the anchor set.* Full texts were read for 37 anchor studies only; other studies were charted from titles and abstracts, and their numbers are marked †. The anchor set was chosen purposively, so statistics computed on it, including the design-feature counts and the reporting audit, describe the anchor set rather than the literature.

*Assignment simplification.* Multi-method and multi-layer studies were assigned a single primary layer and method family.

*Evidence base.* About two-thirds of the core studies are preprints. Several anchor findings come from a small number of research groups and from developer-produced reports whose methods are not fully disclosed.

*Recency.* The field is moving quickly; the search date was 9 October 2026, and later studies are not included.

The most useful next steps are independent dual screening of a stratified sample of decisions, full-text charting beyond the anchor set, and a registered living update of the review with the frozen query, extended to OpenReview and to hyphenated term variants.

## 8 Conclusion

Model-originated threats to evaluation validity have moved from theoretical concern to an active empirical field in less than three years. The evidence charted here shows that LLMs can recognise evaluations, that recognition can change behaviour, and that current detection methods are unreliable against adversarially constructed underperformance. It also shows that "evaluation awareness" is not one quantity, that its relationship to behaviour is model-specific, and that most validity evidence rests on behaviour that was deliberately induced. For practitioners, the immediate implications are to report awareness measures separately and with their biases, to prefer elicitation-first protocols for capability claims, and to treat propensity-based safety results as potentially biased in either direction when awareness is plausible, reporting cue-ablated or replay variants alongside them (Table 8, item 8). For researchers, the priority is to establish whether methods validated on induced behaviour transfer to behaviour that arises from training incentives.

## Declarations

**Funding** The authors did not receive support from any organisation for the submitted work.

**Competing interests** The authors have no relevant financial or non-financial interests to disclose.

**Ethics approval and consent to participate** Not applicable. This study is a review of published and publicly available literature and involved no human participants, human data or animals.

**Consent for publication** Not applicable.

**Data availability** The protocol and its amendments, all search strategies and raw API responses, record logs, screening decisions, tier and charting data, full-text checks, reporting-audit codes and count reconciliations are provided as Supplementary Files S0–S5 and in the repository https://github.com/Bhargavteja-9779/AI_review_PNBT.git, which will be archived with a DOI on publication.

**Code availability** The scripts used for the database searches (`search/run_searches.py`), deduplication (`search/dedup.py`), screening and reconciliation (`screening/screen_db.py`, `screening/merge.py`, `screening/reliability.py`, `evidence/screen.py`), charting (`evidence/chart.py`) and figure generation (`evidence/figures.py`) are provided in the accompanying repository (https://github.com/Bhargavteja-9779/AI_review_PNBT.git), together with the raw API responses.

**Author contributions** P N Bhargav Teja: conceptualisation, methodology, investigation, data curation, formal analysis, visualisation, writing – original draft. Divya Meena S: conceptualisation, supervision, validation, writing – review and editing. Both authors read and approved the final manuscript.

**Use of generative AI** Generative AI tools, including Claude, were used as research assistance during the preparation of this review manuscript to support literature organization, thematic synthesis, academic language refinement, and manuscript structuring. All references, factual claims, and scientific interpretations were subject to human verification against the original sources. The authors take full responsibility for the accuracy, originality, integrity, and final content of the manuscript.
