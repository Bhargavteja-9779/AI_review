## 3 Review methodology

### 3.1 Design and protocol deviations

A protocol (v0.1) was written before any formal searching. It specified a scoping review reported according to PRISMA-ScR (Tricco et al. 2018), using the scoping-review framework of Arksey and O'Malley (2005) as refined by Levac et al. (2010). A scoping design was chosen because terminology in the field is inconsistent, study designs are heterogeneous, and the objective is to map concepts, methods and gaps rather than to pool effects. The protocol was not registered.

The planned information sources were bibliographic APIs: OpenAlex, arXiv, Semantic Scholar and DBLP, with Crossref and DOI resolution for verification. All of them were blocked by the network policy of the computing environment in which the review was conducted, and publisher full-text pages could not be retrieved. Scopus and Web of Science require institutional licences and were not available. We therefore made two documented deviations (protocol v0.2):

1. **Information source.** Records were identified through a general web-search tool that returns result links with machine-generated summaries. Queries were logged verbatim (Supplementary File S1), but the tool provides neither hit counts nor exportable record sets.
2. **Design label.** Because database coverage cannot be demonstrated and full texts could not be read, we do not claim compliance with PRISMA-ScR. We describe the study as a *structured critical review with a scoping-style evidence map*. We follow the PRISMA-ScR items that remain applicable (rationale, objectives, eligibility, sources, selection, charting, synthesis and limitations) and report deviations wherever they arise.

The ready-to-run database search scripts written for the original protocol are released with the review. An update using bibliographic databases is planned (Section 7).

### 3.2 Eligibility criteria

Table 2 summarises the eligibility criteria. In brief, sources were eligible if they (I1) were primary empirical studies, methodological or benchmark papers, or developer or third-party evaluation reports; (I2) measured, induced, detected or mitigated behaviour that depends on evaluation context, or strategic or induced underperformance, in LLMs or LLM-based agents; and (I3) reported enough method detail for the charting fields.

**Table 2** Eligibility criteria and screening codes

| Code | Criterion | Applied at |
|---|---|---|
| I1 | Primary study, method/benchmark paper, or developer/third-party evaluation report | Title, abstract, metadata |
| I2 | Phenomenon: evaluation-context-dependent behaviour, strategic or induced underperformance, or a method to detect, elicit or mitigate it in LLMs or LLM agents | Title, abstract, metadata |
| I3 | Method details sufficient to chart framework layer and method family | Abstract and retrieved summaries |
| Period | 1 January 2019 to 9 October 2026 | Metadata |
| E1 | Different construct (e.g. environmental situational awareness), or a method unrelated to evaluation validity | Title, abstract |
| E3 | Non-archival community forum post or informal blog without an organisational or archival report | Venue |
| E6 | Title or identifier could not be confirmed from retrieved records | Metadata |
| R0 | Duplicate identifier | Identifier |
| CONTEXT | Eligible publication outside the phenomenon boundary (methodology, background theory, adjacent evaluation-validity literature such as contamination, jailbreak scoring or benchmark design); cited for context, not charted | Title, abstract |

Training-data contamination was deliberately placed outside the phenomenon boundary. It is a data-side rather than a model-side threat, and it has been reviewed recently (e.g. Chen S et al. 2025). Contamination studies were retained as context.

### 3.3 Information sources and search

Twenty-five record-identifying search batches and one metadata-verification batch were executed on 9 October 2026, comprising 133 queries in total (six pilot queries for the novelty check and 127 in batches B1–B26). The batches covered seven concept areas:

- evaluation and situational awareness;
- sandbagging and capability elicitation;
- alignment faking, scheming and sabotage evaluations;
- reward hacking and evaluator gaming;
- reasoning-trace monitoring and faithfulness;
- white-box detection (probes, steering, feature-based methods);
- system cards, third-party evaluations and governance.

Searches combined construct terms ("evaluation awareness", "test awareness", "sandbagging", "strategic underperformance", "alignment faking", "evaluation faking", "observer effect", "capability elicitation", "scheming") with system terms (language model, LLM, agent). Known-item searches checked the metadata of sources cited by included studies, which amounts to informal backward citation chasing. Every query, its batch and the records it yielded are listed in Supplementary File S1 (`evidence/search_log.md`, `evidence/candidates.tsv`).

### 3.4 Selection

Records were merged and deduplicated on identifier (arXiv ID, DOI or a stable grey-literature key) by a script (`evidence/screen.py`). They were then screened against Table 2 using deterministic rules applied to the title, the venue and the recorded scope of each record. The decision rules are written in the script and are reproduced in Supplementary File S2, together with one primary decision code per record.

Screening was performed by a single reviewer working with an AI system (see the AI-use statement). No dual independent screening took place. As safeguards, the rules were fixed before the final pass, every decision is logged, and borderline records were placed in the CONTEXT category rather than silently excluded.

### 3.5 Data charting

For each included source, the following were charted: identifier, title, first author or organisation, year, venue, source type (peer-reviewed, preprint, grey literature), framework layer and method family (Section 3.6). For a purposive anchor set of 37 primary studies that define the field's main empirical claims, we additionally charted, from abstracts and retrieved summaries:

- the construct name used;
- the setting;
- the models evaluated, as reported;
- the main reported result;
- the design features reported, namely a control or counterfactual condition, more than one model family, and ground truth by construction.

Unreported fields are marked N/R. All charting is at abstract or summary level because full texts were inaccessible. Quantitative values in this review are therefore reported exactly as stated in the source abstracts or summaries and are labelled "as reported".

### 3.6 Framework derivation and assignment rules

An initial framework was formulated in the protocol, separating the evaluation-context signal, model awareness, behavioural divergence and the validity consequence. It was then revised inductively during charting; for example, reasoning-trace monitoring was split from white-box methods after charting showed that the two have distinct validity problems. Each source was assigned to one primary layer according to its main object of study:

- **L1** studies manipulate or characterise properties of the evaluation;
- **L2** studies measure whether models recognise evaluation;
- **L3** studies measure behaviour conditional on that recognition, or strategic underperformance or misreporting;
- **L4** studies propose or test responses (detection, elicitation, suppression, environment redesign, training interventions) or report validity consequences in developer or third-party evaluations.

Method families were assigned by documented keyword rules applied to the title and recorded scope, with 30 manual overrides for multi-method studies whose titles do not reveal their primary method (`evidence/chart.py`). Single-layer assignment necessarily simplifies multi-method studies; Section 7 discusses the consequences.

### 3.7 Critical appraisal and synthesis

Formal risk-of-bias assessment is not required for scoping-style reviews, and it was not feasible without full texts. We did not compute quality scores. Instead, the anchor-set charting records which design features each study reports, and Section 4 discusses evidential weight qualitatively. Before any cross-study statement, findings were classified as directly comparable (same construct, measure and model), conditionally comparable (same construct but different measure or model) or non-comparable. No effect sizes were pooled and no leaderboards were constructed. Apparent disagreements were typed as a genuine contradiction, context-dependent, a metric artefact, a methodological artefact, or insufficient evidence (Table 6).
