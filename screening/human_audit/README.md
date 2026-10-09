# Human audit of AI-assisted decisions (to be completed by an author)

The review's screening, tiering and layer decisions were made by an AI system. This folder contains a stratified random
sample (seed 20261010) for a human check, as planned in protocol v0.1 (Section 6).

1. `screening_sample.csv`: 100 manually screened database records (30 included, 30 context, 40 excluded, shuffled).
   Hide or ignore the `ai_decision_hidden` column, read title and abstract, and enter INCLUDED / CONTEXT / EXCLUDED
   against Table 2 of the manuscript.
2. `tier_sample.csv`: 60 charted studies (30 core, 30 adjacent, shuffled). Enter core/adjacent using the tier rule in
   Section 3.2 and the layer L1-L4 using Section 3.6, without looking at the hidden columns.
3. Run `python3 screening/human_audit/agreement.py` to compute human-AI agreement and Cohen's kappa, then report the
   results in Section 3.4 and Section 7 of the manuscript (replacing "no second human reviewer").
