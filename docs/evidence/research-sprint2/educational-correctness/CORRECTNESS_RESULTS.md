# Educational correctness evaluation — Research Sprint 2A

Executed30 October2026 against commit `a19b68fa5b872fa9639eb653c3b528e803071a78`, FastAPI application version **0.6.0**. Application/data/earlier academic evidence were not changed. All learners and grades are synthetic; no participant research occurred.

## Baseline and documentary review

The frozen corpus contains **20 CSV datasets,11 programmes,12 qualifications,33 entry-rule rows,5 progression edges and21 registered source records**. Domain counts remain IT7, Business1, Engineering3. BASELINE.json records every dataset count/hash, initial Git status and preservation hashes. raw/dataset-records.json inventories all records, including recognition/source relationships. Existing eligibility/gap/progression tests, WP5 rule-evidence.csv/scenarios.json and the source register were inspected, but not reused as the new expected-output table.

All21 registered URLs returnedHTTP200 in the authorised direct retrieval;20 distinct resources are represented becauseSRC0004/SRC0021 are the same handbook with different anchors. The initial sandbox DNS failures remain in raw/sandbox-fetch-failure.json. **Access is not content verification:** SOURCE_RECORD_AUDIT.csv classifies **16 records VERIFIED in stated scope,4 PARTIALLY VERIFIED and1 OUTDATED**. These counts concern the documented scope, not all claims attached to a page or independent accreditation approval. Three supplementary provider documents were fetched and reviewed to stated limits.

SOURCE_VERIFICATION_MATRIX.csv includes every programme and progression edge, plus specific gaps/conflicts. Selected official requirements were directly checked, including UGC2025/26 general/CS/AI/IT/Engineering sections, IIT foundation, OUSL, Peradeniya, UCJ and UoVT. The UGC PDF is freshly retrieved, not merely a historical cached citation. Its applicability remains **2025/2026**; no claim that it settles another intake or is the latest available edition. Most provider pages lack a publication date. IIT displaysJan2027, OUSL displays a closedJuly2026 call, and UCJ includes course-stage information effective2022/23.

Supplementary source limits: browser UCSC403 was overcome by directHTTP200; the UCSC page supports degree identity/SLQF5 and selective honours progression, not the A/L admission oracle. IIT's general admissions page addresses international applicants and does not resolve local direct-degree minima. The UoVT prospectus is image-only; relevant pages were visually inspected, including PDF16/29 (printed13/25). Its2026/27 URL/landing-page label is not independent proof of an internal publication date. It supports NVQ priority and A/L remaining-vacancy/mode caveats; exact per-programme acceptance is still unresolved. No general qualification equivalence was inferred.

## Oracle design and execution

Expected outcomes were hand-authored from the retrieved official text and locked in ORACLE_LOCK.json **before the first application run**. SCENARIO_DEFINITIONS.csv is unchanged after execution. The evaluator had inspected implementation/tests and is not an independent educational adjudicator. Thus this is a **source-grounded evaluator assessment**, not independent expert validation or actual provider decisions.

Official publications generally do not prescribe software missing-data semantics. The protocol therefore distinguishes direct published-condition cases from a declared conservative uncertainty convention, missing-rule design checks, and reference cases containing facts outside the API contract. It does not relabel all of them “independently verified correctness”.

The unchanged FastAPI app ran through TestClient:40 `/eligibility` requests and5 `/progression/...` requests, allHTTP200. No browser/live-network application workflow or ranking experiment is claimed. Raw requests, extra reference context and complete original responses are preserved in raw/api-responses.jsonl; timings there are harness observations, not a performance benchmark.

| Stratum | Scenarios | Agree | Disagree | Interpretation |
|---|---:|---:|---:|---|
| Direct official conditions, fully representable |18 |18 |0 |14 academic minimum decisions and4 conditional-route text checks; different tasks, not18 admissions predictions |
| Source-grounded uncertainty convention |22 |21 |1 |21 academic cases and1 conditional vocational route; combines official facts with explicit missing-evidence reasoning |
| Missing direct-entry rules/design-only |3 |3 |0 |IIT three degrees remain NOT_ASSESSED; no independent direct-entry minimum was established |
| Official reference facts absent from API |2 |0 |2 |Age/CGP reference decisions cannot be reproduced from the reduced request; capability limitation |
| **All scenarios** |**45** |**42** |**3** |Heterogeneous case agreement, not national eligibility accuracy |

There are **20 direct official-condition reference cases** in total;18 are fully API-representable and2 contain additional facts. Only the14 academic cases in the fully representable subset directly exercise published minimum-grade/count decisions. The22 uncertainty and3 design-only cases must not be included in a supposedly pure admissions-accuracy denominator.

Two complete O/L profiles met the published foundation minimum;12 complete profiles failed a documented minimum and all12 returnedNOT_MET. No unsupportedMET/admission guarantee was observed in these scenarios. Of24 expectedNOT_ASSESSED cases,23 returned it; the remaining EC08 is described below. The API returned25 NOT_ASSESSED overall because it also lacked the two extra reference facts. This is not evidence that the API ignored supplied age/CGP: those fields do not exist in the tested contract.

## Disagreements and explanation review

- **EC08 — uncertainty semantics:** five supplied O/L passes with no completeness declaration produceNOT_MET rather than the conservative referenceNOT_ASSESSED. The documented legacy count default treats omitted completeness differently from explicit false. EC07 with the same grades and explicit false correctly returnsNOT_ASSESSED. This is an API/legacy exposure: the current frontend always sends the checkbox value and starts unchecked. The failed-count statement is arithmetically correct, but the overall failure summary overstates what an undeclared partial record establishes.
- **EC39 — missing age contract:** the reference learner is17 at registration, so OUSL's age minimum fails. The request contains no age field; application appropriately retains provider uncertainty. This is a representational limitation, not a demonstrated false eligibility grant. Do not introduce sensitive data collection merely to improve agreement.
- **EC40 — missing CGP contract:** reference CGP is29 in every allowed attempt, below the UGC registration minimum. Only subject grades reach the API, so it returnsNOT_ASSESSED. Again, this is an input-capability limit. Prior allowed-attempt achievements matter; a single current29 would not establish failure if an earlier allowed result met30.

Original response summaries and all unique passed/failed/unknown messages were reviewed against the source predicates, alongside the five route conditions. **One misleading missingness summary** was identified (EC08). No wrong numeric minimum or guaranteed-admission statement was identified in this set. All11 foundation cases expose a **rule-citation gap**: their thresholds are corroborated on detailedSRC0010, while the returned four rule-source links point to generalSRC0009, which does not state those numerical predicates. This is a provenance/explanation defect, not11 wrong admission decisions. Counts overlap: EC08 is also one of those11.

An automatic structural warning inEC29 was reviewed and retained: a failed A/L branch can coexist with overallNOT_ASSESSED when alternative awards are unresolved. Its global uncertainty is appropriate; the failed branch is factual. It was not silently recounted as an explanation defect. This is evaluator review, not participant comprehension or fluent-language evaluation.

## Additional checks and research value

**40 existing focused eligibility/gap/progression regressions passed**, and CSV integrity passed; commands/zero exit codes are in COMMAND_RESULTS.json. These40 are current focused regressions, distinct from the historical August40 and not additional independent samples. Full205-backend/36-browser suites were not rerun in this sprint.

The evidence supports bounded evaluation of minimum-condition execution, missing-evidence behaviour, conditional-route presentation and source traceability. It also exposes deliberate coverage limits and a legacy uncertainty risk that successful regression tests alone do not adjudicate. It does not prove complete educational accuracy, actual admission, learner benefit, recognition equivalence, ranking relevance or user satisfaction. ISSUES_FOR_REVIEW.md separates data/provenance, rule/semantics, explanation and insufficient-input issues. No correction was implemented; stop for review before fixes.
