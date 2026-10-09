## 3 Review methodology

### 3.1 Design, protocol and amendments

A protocol (v0.1) was written before any formal searching. It specified a scoping review reported according to PRISMA-ScR (Tricco et al. 2018), using the framework of Arksey and O'Malley (2005) as refined by Levac et al. (2010). A scoping design was chosen because terminology in the field is inconsistent, study designs are heterogeneous, and the objective is to map concepts, methods and gaps rather than to pool effects. The protocol was not registered. The selection process is reported with a PRISMA 2020 flow diagram that separates database searches from other identification methods (Page et al. 2021).

Identification took place in two phases on 9 October 2026. In the first phase, the bibliographic APIs named in the protocol were unreachable from the computing environment, so records were identified through 25 logged web-search batches (identification via other methods). In the second phase, after network access was opened, the protocol's database searches were executed. Protocol amendment v0.2, made before the database searches were run and recorded with a timestamp in the released query file, (a) added Scopus as an information source, (b) added the model-originated threat terms "strategic deception", "strategic dishonesty" and "deceptive alignment", and (c) added "reward hacking" and "specification gaming" in combination with an evaluation term, to match the scope that the first phase had shown to be necessary. The search strategy was then frozen. Two planned sources could not be searched: OpenAlex returned HTTP 429 (daily quota exhausted) and DBLP returned an anti-automation page instead of results. Both failures are logged (Supplementary File S1b).

### 3.2 Eligibility criteria

Table 2 summarises the eligibility criteria. In brief, sources were eligible if they (I1) were primary empirical studies, methodological or benchmark papers, or developer or third-party evaluation reports; (I2) measured, induced, detected or mitigated behaviour that depends on evaluation context, or strategic or induced underperformance, in LLMs or LLM-based agents; and (I3) reported enough method detail for the charting fields.

**Table 2** Eligibility criteria and screening codes

| Code | Criterion | Applied at |
|---|---|---|
| I1 | Primary study, method/benchmark paper, or developer/third-party evaluation report | Title, abstract, metadata |
| I2 | Phenomenon: evaluation-context-dependent behaviour, strategic or induced underperformance, or a method to detect, elicit or mitigate it in LLMs or LLM agents | Title, abstract, metadata |
| I3 | Method details sufficient to chart framework layer and method family | Title and abstract (full text for the anchor set) |
| Period | 1 January 2019 to 9 October 2026 | Metadata |
| E1 | Different construct (e.g. environmental situational awareness), or a method unrelated to evaluation validity | Title, abstract |
| E3 | Non-archival community forum post or informal blog without an organisational or archival report | Venue |
| E6 | Title or identifier could not be confirmed from retrieved records | Metadata |
| S1 | No phenomenon term of the frozen query in title or abstract (rule-assisted pre-screen, audited) | Title, abstract |
| R0 | Duplicate identifier or version of the same work | Identifier, title |
| CONTEXT | Eligible publication outside the phenomenon boundary (methodology, background theory, adjacent evaluation-validity literature such as contamination, jailbreak scoring or benchmark design); cited for context, not charted | Title, abstract |

Training-data contamination was deliberately placed outside the phenomenon boundary. It is a data-side rather than a model-side threat, and it has been reviewed recently (e.g. Chen S et al. 2025). Contamination studies were retained as context.

### 3.3 Information sources and search

**Databases.** Three sources were searched on 9 October 2026 through their APIs: Scopus (Elsevier Search API, field TITLE-ABS-KEY), arXiv (export API, abstract field, restricted to cs.CL, cs.AI, cs.LG and cs.CR) and Semantic Scholar (Academic Graph bulk search over titles and abstracts). Together they cover the peer-reviewed venues indexed by Scopus, the preprint server on which most of this literature first appears, and the conference proceedings (NeurIPS, ICML, ICLR, ACL) indexed by Semantic Scholar. The query combined three concept blocks: system terms (A: language model(s), LLM(s), foundation model, frontier model, AI agent, AI system); phenomenon terms specific enough to stand alone (B1: evaluation awareness, eval awareness, test awareness, sandbagging, strategic underperformance, alignment faking, evaluation faking, observer effect, evaluation gaming, under-elicitation, password-locked, hidden capabilities, strategic deception, strategic dishonesty, deceptive alignment); and broader phenomenon terms that were admitted only with an evaluation term (B2: situational awareness, scheming, capability elicitation, reward hacking, specification gaming; C: evaluation, benchmark, test, assessment, audit). The logical form was A AND (B1 OR (B2 AND C)), limited to publications from 1 January 2019. The exact strings submitted to each API, the retrieval timestamps and the record counts are given in Supplementary File S1b, and the raw API responses are released.

**Other methods.** The first-phase web searches comprised 133 queries in 25 record-identifying batches and one metadata-verification batch. They covered seven concept areas: evaluation and situational awareness; sandbagging and capability elicitation; alignment faking, scheming and sabotage evaluations; reward hacking and evaluator gaming; reasoning-trace monitoring and faithfulness; white-box detection; and system cards, third-party evaluations and governance. Known-item searches checked the metadata of sources cited by included studies (backward citation chasing). Developer system cards and third-party evaluation reports, which bibliographic databases do not index, were identified only by this route. Every query and the records it yielded are listed in Supplementary File S1a.

### 3.4 Selection

**Deduplication.** Database records were deduplicated automatically on DOI, version-stripped arXiv identifier and normalised title plus year (`search/dedup.py`). Title pairs with a similarity of at least 0.93 were flagged, and 30 flagged pairs that were versions of the same work (for example, a preprint and its proceedings version) were merged after manual inspection. Web records were matched to database records on the same keys, and records found by both routes are counted once, in the databases column of the flow diagram.

**Stage 1 (rule-assisted pre-screen).** Semantic Scholar's bulk search stems query terms (for example, "scheming" also retrieves "scheme"), which inflated the number of irrelevant records. Records whose title and abstract contained none of the phenomenon terms of the frozen query, written as a fixed regular expression (Supplementary File S2), were therefore excluded at stage 1. To check this rule, a random sample of 120 stage-1 exclusions (seed 20261009) was read in full at title and abstract level. It contained one relevant record (0.8%; Wilson 95% CI 0.2–4.6%). A rescue pass then applied a broader pattern to all stage-1 exclusions, and the 399 records it matched were screened manually.

**Stage 2 (title and abstract).** All records that passed stage 1 or were flagged by the rescue pass were screened manually against Table 2. Each record received one decision code. Records in the first-phase web set were screened on titles, venues and retrieved summaries using the same criteria.

**Reconciliation and reliability.** Ninety web records were also retrieved by the databases and had therefore been screened twice, once in each phase, without access to the earlier decision. The two passes agreed on 84 of the 90 records (93.3%; Cohen's κ = 0.747; Cohen 1960). The six discordant records were re-read and resolved by consensus; five became included studies and one a contextual reference. Screening was performed by a single reviewer working with an AI system (see the AI-use statement); there was no dual independent screening. The safeguards were the frozen rules, the audited stage-1 sample with a rescue pass, the inter-pass reliability check and a complete decision log (Supplementary File S2; `screening/`).

### 3.5 Data charting

For each included study, the following were charted: identifier, title, first author or organisation, year, venue, source type (peer-reviewed, preprint, grey literature), framework layer and method family (Section 3.6). Studies identified only through the databases were charted manually from title and abstract (`screening/db_charting_manual.tsv`).

For a purposive anchor set of 37 primary studies that carry the field's main empirical claims, the full texts were retrieved (latest arXiv version as of 9 October 2026) and read. For each one we charted:

- the construct name used;
- the setting;
- the models evaluated;
- the main result;
- the design features reported, namely a control or counterfactual condition, more than one model family, and ground truth by construction.

Every quantitative statement about an anchor study in Sections 4 and 5 was checked against the full text. Statements about other studies rest on their abstracts and are worded accordingly.

### 3.6 Framework derivation and assignment rules

An initial framework was formulated in the protocol, separating the evaluation-context signal, model awareness, behavioural divergence and the validity consequence. It was then revised inductively during charting; for example, reasoning-trace monitoring was split from white-box methods after charting showed that the two have distinct validity problems. Each source was assigned to one primary layer according to its main object of study:

- **L1** studies manipulate or characterise properties of the evaluation;
- **L2** studies measure whether models recognise evaluation;
- **L3** studies measure behaviour conditional on that recognition, or strategic underperformance or misreporting;
- **L4** studies propose or test responses (detection, elicitation, suppression, environment redesign, training interventions) or report validity consequences in developer or third-party evaluations.

For studies identified in the first phase, method families were assigned by documented keyword rules applied to the title and recorded scope, with 30 manual overrides for multi-method studies whose titles do not reveal their primary method (`evidence/chart.py`). Studies identified only in the database phase were assigned a layer and a method family manually from their abstracts. To check the rule-based layer assignment, the 37 anchor studies were also coded manually from their full texts: the two assignments agreed for 34 of 37 studies (91.9%; κ = 0.881; `screening/reliability.py`). Single-layer assignment necessarily simplifies multi-method studies; Section 7 discusses the consequences.

### 3.7 Critical appraisal and synthesis

Formal risk-of-bias assessment is not required for scoping reviews, and no validated tool exists for the designs in this field. We did not compute quality scores. Instead, the full-text charting of the anchor set records which design features each study reports, and Section 4 discusses evidential weight qualitatively. Before any cross-study statement, findings were classified as directly comparable (same construct, measure and model), conditionally comparable (same construct but different measure or model) or non-comparable. No effect sizes were pooled and no leaderboards were constructed. Apparent disagreements were typed as a genuine contradiction, context-dependent, a metric artefact, a methodological artefact, or insufficient evidence (Table 7).

### 3.8 Reporting audit of the anchor set

To test whether the reporting practices recommended in Section 5.4 are already followed, the full texts of the 37 anchor studies were coded against the twelve checklist items (Table 8) using a frozen codebook (Supplementary File S5). Each item has an applicability rule; for example, the probe items apply only to studies that use activation probes or steering. Each study received one of four codes per item: reported, partly reported, not reported, or not applicable, with a verbatim quotation or a location for every positive code. Four coders, working with AI assistance, coded disjoint subsets. An independent coder, blind to the primary codes, re-coded a random sample of ten studies (seed 20261009). Agreement over the 120 double-coded cells was 93.3% (Cohen's κ = 0.90); agreement on applicability alone was κ = 0.98, and agreement on the code when both coders judged the item applicable was κ = 0.84 (85 cells). The primary codes are analysed. Adherence to an item is the share of applicable studies that report it, counting partial reporting as one half. Because the checklist was derived partly from these studies, the audit describes reporting practice; it is not a validation of the checklist.

