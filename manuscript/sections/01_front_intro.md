---
title: "When Models Know They Are Being Tested: A Scoping Review of Evaluation Awareness, Sandbagging and Related Model-Originated Threats to the Validity of Large Language Model Evaluation"
---

**P N Bhargav Teja**^1^ and **Divya Meena S**^1,\*^

^1^ School of Computer Science and Engineering, Vellore Institute of Technology, Vellore, Tamil Nadu, India

^\*^ Corresponding author: Divya Meena S, divyameena.s@vit.ac.in

## Abstract

Evaluations of large language models (LLMs) increasingly inform deployment and governance decisions, yet models can recognise evaluation contexts and behave differently in them. This scoping review maps studies of such model-originated threats to evaluation validity: evaluation awareness, sandbagging, alignment and evaluation faking, strategic dishonesty and evaluator gaming. We searched Scopus, arXiv and Semantic Scholar and logged web sources to 9 October 2026. Screening and charting were AI-assisted against written criteria and verified by the authors. Of 5649 database and 418 web records, 315 studies were charted: 167 core studies and 148 adjacent studies; we read the full texts of 37 anchor studies. We propose a four-layer framework (context signal, awareness, behavioural divergence, validity consequence) and formalise it as a decomposition of evaluation error into scorer, context-induced, task and elicitation terms. Context separability is necessary for context-induced bias, awareness is neither necessary nor sufficient for a biased score, and context-induced divergence is not identifiable from evaluation data alone when evaluations are recognisable. Empirically, elicited, verbalised and represented awareness measures diverge; the awareness–behaviour link varies in magnitude and direction across models; and black-box sandbagging detection is unreliable, whereas fine-tuning and activation-level elicitation recover capability from induced sandbaggers. A full-text audit against our twelve-item reporting checklist found that 3 of 15 probe studies controlled for prompt format. The evidence is preprint-dominated, and the validation of detection and elicitation methods rests largely on deliberately induced behaviour. We close with an evidence-graded research agenda.

**Keywords:** Evaluation awareness · Sandbagging · Large language models · AI safety evaluation · Construct validity · Alignment faking

## 1 Introduction

Evaluations are the main instrument through which developers, independent evaluators and regulators decide what a large language model (LLM) can do and how it is likely to behave. Frontier developers condition deployment and safeguard decisions on dangerous-capability and alignment evaluations (Phuong et al. 2024; OpenAI 2025b; Anthropic 2025b), and third-party evaluators increasingly publish pre-deployment assessments (METR 2025a; Souly et al. 2026). Every such decision rests on an inferential step that is rarely stated: that behaviour observed under evaluation is representative of behaviour in deployment.

That step has always been vulnerable to familiar threats such as benchmark contamination, weak construct validity and prompt sensitivity (Raji et al. 2021; Sclar et al. 2024; Bean et al. 2025). This review concerns a different class of threat, one that originates in the evaluated model itself. A model that can recognise that it is being tested may behave differently because it is being tested. Concretely, it may underperform on a capability evaluation (sandbagging), present a more aligned profile on a safety evaluation (alignment or evaluation faking), produce outputs that deceive the scoring pipeline (strategic dishonesty), or exploit the test harness (evaluator gaming). Each of these breaks the link between the reported score and the deployment behaviour the score is meant to predict.

Concern about this possibility is longstanding in the alignment literature (Hubinger et al. 2019; Carlsmith 2023; Ngo et al. 2024), but empirical work on it has grown sharply only since 2024. Models have been shown to underperform selectively when prompted or fine-tuned to do so (van der Weij et al. 2025); frontier models discriminate evaluation transcripts from deployment transcripts well above chance (Needham et al. 2025); linear probes recover an evaluation-versus-deployment distinction from model activations (Nguyen et al. 2025); and developers now report evaluation-awareness measurements in their system cards (Anthropic 2025a; OpenAI 2025a). At the same time, the field acknowledges that it lacks a shared conceptual foundation: studies conflate properties of the evaluation with properties of the model, and detection with behavioural response (Li C et al. 2026).

Existing reviews do not address this gap directly. Surveys of AI deception catalogue deceptive behaviours broadly but predate most of the evaluation-awareness literature or treat it as one behaviour among many (Park et al. 2024; Shi et al. 2026; Chen B et al. 2025). A 2026 review of the AI "observer effect" is closest in theme, but synthesises fifteen landmark contributions published up to 2024 and predates the measurement literature on evaluation awareness (Maurya et al. 2026). Broad reviews of safety-evaluation methods and of reward hacking name sandbagging or evaluator gaming as challenges without synthesising how they are measured (Grey and Segerie 2025; Wang X et al. 2026; Morampudi et al. 2026). A recent hybrid survey frames benchmark validity and alignment failure as a common proxy–target divergence problem across eight evidence streams (Uluırmak and Kurban 2026), but it does not centre on model-originated threats or on how they are measured. Reviews of benchmark validity and safety datasets address the evaluator side of the problem rather than the model side (Röttger et al. 2025; Bean et al. 2025). Recent reviews in *Artificial Intelligence Review* address adjacent problems: the validity of LLM-agent benchmarks as measurement instruments (Nageshwaran et al. 2026; Kehkashan et al. 2026), risks from deception and persuasion by LLMs (Jones and Bergen 2026), LLM-as-a-judge evaluation (Nadăş 2026) and epistemic norms for safety and alignment research (Navaie 2026). Judged from their abstracts, none treats the evaluated model's own recognition of evaluation as a threat to the validity of scores. Section 2.4 and Table 1 give the detailed comparison.

This review asks five questions:

- **RQ1.** How are evaluation awareness, sandbagging, alignment or evaluation faking and related constructs defined and operationalised?
- **RQ2.** Which methods are used to detect or measure these phenomena, and what evidence supports their validity?
- **RQ3.** Under which model, task and context conditions are the phenomena observed, and where do findings conflict?
- **RQ4.** Which countermeasures have been proposed, and how rigorously have they been evaluated?
- **RQ5.** Which gaps most threaten the validity of current evaluation practice, and which studies would close them?

The review makes four contributions:

1. A reproducible, tiered evidence map: 167 core studies of model-originated threats to LLM evaluation validity and 148 adjacent studies, identified through three bibliographic databases and logged web searches, with all screening decisions logged and all counts generated by released scripts.
2. A four-layer framework (context signal, awareness, behavioural divergence, validity consequence) with explicit assignment rules, and a formal decomposition of evaluation error that states what each study design can and cannot identify. The framework separates constructs that the literature frequently conflates.
3. A structured comparison of measurement methods and their validity evidence, and a typed analysis of seven apparent contradictions in the literature.
4. A twelve-item reporting checklist for evaluation papers and system cards, applied retrospectively to the full texts of the anchor studies with independent double coding, and an evidence-graded research agenda.

The remainder of the paper is organised as follows. Section 2 introduces terminology and prior reviews. Section 3 describes the review method, including the protocol amendments and the two-phase identification. Section 4 reports results by research question. Section 5 discusses implications. Section 6 sets out the research agenda, Section 7 the limitations of the review, and Section 8 concludes.

## 2 Background and terminology

### 2.1 Measurement validity and observer effects

The concern addressed here is an instance of a general measurement problem. In psychometrics, validity is a property of the inferences drawn from scores rather than of the scores themselves (Messick 1995). Measurement modelling makes the same point for computational systems: unobservable constructs must be operationalised, and mismatches between a construct and its operationalisation produce systematic error (Jacobs and Wallach 2021). Benchmarks presented as general measures of progress have been criticised on exactly these grounds (Raji et al. 2021). A recent review of 445 LLM benchmarks found widespread weaknesses in how measured phenomena, tasks and metrics support the claims made from them (Bean et al. 2025).

In the human sciences, the analogous model-side threat is the observer or Hawthorne effect: participants change their behaviour because they are studied. A systematic review of that literature concluded that research-participation effects exist but that little can be securely known about their conditions, mechanisms or magnitude, and that new concepts were needed (McCambridge et al. 2014). The parallel with the current LLM literature is close, and we return to it in Section 5. A related principle, often summarised as Goodhart's law, holds that a measure placed under optimisation pressure ceases to measure what it measured before. Overoptimisation of a learned reward model illustrates it quantitatively (Gao et al. 2023).

### 2.2 Constructs

Five constructs recur in the literature. We define them operationally here, and Section 4.3 examines how the primary studies actually use them.

- **Situational awareness**: a model's knowledge of itself and its circumstances, including whether it is in training, testing or deployment (Berglund et al. 2023; Laine et al. 2024). It is broader than evaluation awareness.
- **Evaluation awareness**: recognition by a model that its current context is an evaluation (Needham et al. 2025; Nguyen et al. 2025). Three senses need to be kept apart: a *capacity* to discriminate evaluation from deployment, an episode-level *state* (the model's credence, $A$ in Section 4.2), and a *report* of that state, verbalised or elicited. Some authors restrict the term to recognition alone; others include the resulting behaviour.
- **Sandbagging**: strategic underperformance on an evaluation relative to the model's actual capability (van der Weij et al. 2025); we adopt this definition. The GPT-5 system card defines it as a model's ability and propensity to respond to safety or capability evaluations in a way that significantly diverges from performance under real conditions (OpenAI 2025a), and OpenAI's Preparedness Framework lists sandbagging as a research category (OpenAI 2025b).
- **Alignment faking and evaluation faking**: behaving in line with the training or evaluation objective when the model infers that it is observed, while behaving differently when it infers that it is not (Greenblatt et al. 2024a; Fan et al. 2025).
- **Evaluator gaming**: obtaining a high score by exploiting the scoring process rather than performing the intended task, including test-case exploitation, reward hacking and outputs that mislead automated graders (Zhong et al. 2026a; Panfilov et al. 2026).

### 2.3 Elicitation and the direction of error

A capability evaluation underestimates a model when elicitation is incomplete, whether because the model hides a capability or because the evaluators did not try hard enough. Post-training enhancements such as scaffolding, tool use and prompting can raise benchmark performance by amounts that would otherwise require more than five times as much training compute, and sometimes more than twenty times (Davidson et al. 2023). Dangerous-capability evaluations therefore treat insufficient elicitation as a central threat (Phuong et al. 2024; Benton et al. 2024). Sandbagging is the adversarial limit of this problem. It is distinct from ordinary under-elicitation because the source of error is the model's own policy. Conversely, alignment faking produces an *over*-estimate of safety. The two threats bias evaluation results in opposite directions on different evaluation types, and a review that treats them together must keep the direction of error explicit.

### 2.4 Prior reviews

Table 1 compares this review with the closest existing syntheses. None takes model-originated evaluation-validity threats as its primary object, and none synthesises the 2025–2026 primary literature on evaluation awareness measurement, which accounts for most of the evidence charted here (Section 4.1).

**Table 1** Comparison with the closest prior reviews and syntheses (coverage judged from abstracts, and from the full text for Maurya et al. 2026)

| Review | Type, status | Primary focus | Evaluation awareness as a validity threat | Measurement-method synthesis | What this review adds |
|---|---|---|---|---|---|
| Park et al. (2024) | Survey, *Patterns* | AI deception: examples, risks, solutions | Not a focus; predates most studies | No | Evaluation-centred scope; 2024–2026 evidence |
| Shi et al. (2026) | Taxonomy and benchmark analysis (50 benchmarks), ICLR 2026 workshop | Unified deception taxonomy mapped to benchmarks | One behaviour among many | Benchmarks, not measurement validity | Validity framework for the evaluation itself |
| Chen B et al. (2025) | Survey, preprint | Deception defined via signalling theory; deception cycle | Partial | No | Measurement-method comparison and contradictions |
| Uluırmak and Kurban (2026) | Hybrid survey (373 studies), preprint | Proxy–target divergence across eight evidence streams | Touched (strategic behaviour, alignment faking) | Broad; not awareness-specific | Model-side mechanisms; awareness measurement; reporting checklist |
| Maurya et al. (2026) | Review of 15 selected contributions (2016–2024), *IJSRCSEIT* | "Observer effect": behaviour when unmonitored | Central, but conceptual; studies to 2024 only | No; narrative synthesis of landmark studies selected from Google Scholar, arXiv and developer repositories | Logged multi-database search; 2025–2026 measurement literature; comparability classes and reporting checklist |
| Grey and Segerie (2025) | Systematic literature review, preprint | Taxonomy of AI safety evaluations (capabilities, propensities, control) | Named as a challenge (sandbagging) | Broad taxonomy of evaluation techniques | Threat-specific synthesis of how sandbagging and awareness are measured and detected |
| Wang X et al. (2026); Morampudi et al. (2026) | Surveys, preprint; *Discover Artificial Intelligence* | Reward hacking in RLHF/RLVR and in agentic systems | Not a focus | Detection and mitigation of reward hacking | Reward hacking treated as one evaluator-gaming pathway within a validity framework |
| Nageshwaran et al. (2026) | Systematic mapping review (PRISMA-ScR; 259 studies), *Artificial Intelligence Review* | Validity of LLM-agent benchmarks: capability, scoring and environment | Not a focus (evaluator-side validity) | Benchmark design and scoring | Model-originated threats; complements its evaluator-side analysis |
| Jones and Bergen (2026) | Review, *Artificial Intelligence Review* | Risks from manipulation, persuasion and deception by LLMs | Not a focus | No | Deception and awareness as threats to evaluation validity; measurement-method synthesis |
| Frontier Model Forum (2025) | Industry technical report | Practice of frontier capability assessment | Elicitation and validity in general | No systematic evidence map | Documented evidence map |
| Röttger et al. (2025) | Systematic review (144 datasets), AAAI | Open safety-evaluation datasets | No | Dataset landscape | Model-originated threats |
| Bean et al. (2025) | Systematic review (445 benchmarks), NeurIPS | Construct validity of LLM benchmarks | No | Benchmark design | Model-side threats complementary to construct validity |
