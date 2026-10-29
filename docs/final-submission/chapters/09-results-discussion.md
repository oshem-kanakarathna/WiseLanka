# 9. Results and critical discussion

## 9.1 What the evidence supports

The executed checks support a bounded claim: the current artifact consistently processes the tested profile, policy, relevance and interaction scenarios, with reproducible local inference and explicit uncertainty. Five live journeys demonstrate integration beyond mocked responses. Fresh installation and separate asset provisioning strengthen confidence that the prototype is not dependent solely on an old developer environment.

The UGC correction is a stronger research observation than a raw increase in test count. It shows that formal rule execution can be reliable while the knowledge representation remains incomplete. The repair changed academic conclusions conservatively instead of using semantic confidence to conceal the omission. This supports the design decision to separate source validation, rule execution and relevance.

## 9.2 What the evidence does not support

Passing tests does not establish that the rule set covers all admission cases, that every source is current, that rank order reflects learner preferences, or that the interface is usable by its intended population. The 14 reference cases are not a random sample of Sri Lankan learners. The nine ranking cases have no independent labels. No human research finding exists. The dissertation must therefore avoid claims that the prototype reduces career indecision, improves outcomes or increases satisfaction.

Similarity values are numerical proximity in a representation space, not calibrated probabilities. The appearance of a high-scoring programme may be consistent with its title and still fail a mandatory condition. Conversely, a programme marked NOT_ASSESSED may be a viable route once evidence is supplied. Honest uncertainty is an output feature, but excessive unknowns can reduce usefulness; the usability study should investigate whether learners understand and can act on these distinctions.

## 9.3 Trade-offs and alternative interpretations

Local embeddings provide genuine pretrained inference without requiring invented training data, but their utility remains unproven against TF–IDF and deterministic exploration. With 11 programmes and short descriptors, lexical matching or a curated list may be adequate for many cases. A semantic component adds dependencies and model assets, so its continued value should depend on measured relevance rather than the presence of an AI label.

The seven-to-one IT/Business imbalance may influence apparent matching success. A weak Business result could arise from catalogue coverage rather than encoder failure. Evaluation must use equivalent candidate sets and disclose academic-group sizes. It should not attribute differences caused by the WP5 policy changes to a model improvement over historical WP3 outputs.

The guided assistant limits hallucination opportunities by reusing domain outputs and refusing unsupported questions. This improves controllability at the cost of conversational flexibility. It does not independently verify its source data, and a structured wrong rule could still yield a confidently formatted wrong response. Similarly, multilingual labels reduce some interface barriers but leave English source content and semantic preferences as constraints. Testing should establish actual comprehension instead of counting translated keys as universal access.

CSV storage makes this snapshot easy to inspect and version, while manual maintenance introduces stale-data and curation risks. A database alone would not solve those risks. Independent review, route-specific evidence and a documented update process are higher-priority improvements than infrastructure migration for this artifact.

## 9.4 Objective alignment

Objectives III–V have substantial prototype implementation and technical evidence. Objective I has a source-grounded narrative draft but needs broader/full-text author review. Objective II has historical and design context, with limited contemporary empirical learner-needs evidence. Objective VI has implemented features and partial automated validation. Objective VII remains partial because usability feedback has not been collected. Objective VIII is addressed by explicit limitations and justified future work, subject to final academic review. The detailed matrix preserves these differences rather than assigning all objectives an undifferentiated “complete”.

The exact questions in section 1.3 now guide the following evidence-bounded responses. Full component/method mapping is in RESEARCH_QUESTION_TRACEABILITY.md.

| Question | What the current record supports | What is not established |
|---|---|---|
| MRQ | A local prototype integrates policy-aware assessments, relevance and interaction mechanisms | That intended learners receive effective personalised, explainable and accessible support in practice |
| SRQ-I | Typed profiles, sourced rule groups and pathway relationships are integrated and exercised | Independent educational suitability and comprehensive policy coverage |
| SRQ-II | Source/status explanations and comprehension instruments exist | Improved understanding or trust; no adult study/comparison or dedicated trust measure |
| SRQ-III | Conditional routes and self-report gap comparisons execute | Better educational/career planning or objective learner competence |
| SRQ-IV | Language controls, reflow and optional speech/text states are technically demonstrated | Accessibility improvement, fluent translation quality, native speech and comprehensive manual accessibility |
| SRQ-V | Functional/scenario/runtime results are recorded | Independently measured relevance, usability or comparative ranking-quality improvement |

“Improve” in an approved question is an investigation target, not a result. With no suitable human/comparison evidence, the appropriate response is not yet established. No question is rewritten to match the available tests.

## 9.5 Threats to validity and implications

Implementation-authored scenarios risk confirming the same assumptions encoded in the rules. Reviewer blinding, held-out scenarios and domain adjudication can reduce that risk. Model pretraining may carry language/domain biases that are not revealed by a few English examples. A small convenience usability sample, if later approved, will support exploratory design findings rather than national generalisation.

Automated accessibility evidence is limited to selected rules/states; translation accuracy and assistive-technology interaction need human review. One-machine performance lacks concurrency and device diversity. Historical sources may differ from the next admissions intake. These threats constrain the conclusion but do not negate the demonstrable artifact: they specify the conditions under which its evidence can be used responsibly.
