# AI evaluation — functional comparison complete; relevance evaluation pending

Use a frozen model revision, source/code/dataset hashes and identical per-scenario
candidate sets. Compare raw legacy order separately from grouped deterministic,
TF-IDF and frozen semantic order. The academic group order must remain fixed for
all relevance comparisons; otherwise safety-group changes confound AI effects.
The WP5 source correction changes academic groups relative to WP3, so do not compare
historical top-k differences as model improvement.

`comparison.json` and `performance.json` are newly measured WP5 outputs of the WP3
comparison script on the corrected dataset. They contain nine implementer-authored
synthetic cases, not independently labelled learner outcomes. The full-system
scenario-results.json separately covers 14 source-grounded cases. No preference
model is trained, and no feedback is collected.

## Independent judgement protocol — pending ethics/supervisor approval

Freeze development examples and a distinct held-out scenario set before tuning.
Do not tune corpus wording, weights or parameters after inspecting held-out results.
Use eligible consenting adult reviewers with documented relevant expertise; report
actual qualifications and independence rather than assuming it. Separate language
review, domain-rule adjudication and preference-relevance judgements.

Present programme descriptions and source links in a seeded random order, blind to
method and predicted rank. For each scenario/programme, rate interest relevance:
0 irrelevant, 1 weak, 2 moderate, 3 strong; allow UNJUDGEABLE. Relevance is fit to the
stated interests, not eligibility, prestige or an admission probability. Preserve
all initial ratings, disagreement and any adjudication. Do not replace absent
ratings with zero. Include negative judgements and report reviewer coverage.

Evaluate within academic groups using all available candidates, without sampled
negative programmes. Let k=min(3, number of candidates in the evaluated group).
Use gains 2^rating-1 and logarithmic rank discount. Compute nDCG only for completely
judged candidate pools with nonzero ideal gain; otherwise report not computable
and the reason. Report evaluable scenario counts, candidate counts, ties, per-domain
results and paired per-scenario differences. Small samples warrant descriptive
uncertainty and cautious claims, not automatic significance or superiority claims.

For future trained feedback ranking, split by participant (and time where feasible),
keep repeat sessions together, freeze feature preprocessing and training data,
select hyperparameters using development/validation only, and evaluate once on
held-out participants. Never train on test judgements or use future interactions.
Fit TF-IDF only to the declared catalogue snapshot, never rating labels. Query text
is not appended to the fitting corpus.

Current independent judgements: NONE. nDCG@3, precision uplift and satisfaction:
NOT COMPUTED. Ordering differences and runtime are functional observations only.
Satisfaction requires the separate approved usability study; educational benefit
requires a different, substantially stronger study.
