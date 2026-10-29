# Educational correctness protocol and review

Review date: 2026-10-29. Scenarios are fictional reference cases authored by the implementer, not real admissions outcomes or independent domain validation. `rule-evidence.csv` inventories all 33 active requirement rows and their stored source links; a stored date is not evidence that every source was independently rechecked in WP5.

## Source checks actually performed

- UGC Admissions Handbook 2025/26: https://www.ugc.ac.lk/downloads/admissions/Handbook_2025_26/student_handbook_english.pdf — actual PDF downloaded and parsed. SHA256 `8b9cc7b24ed2a10ed19c22a1e12d0a9336c0db15f1623ea2aca35334e005c93d`. PDF page 16 (printed 9), section 1.2: approved A/L passes in one sitting, attempt limits and Common General Paper condition; page 17 (printed 10): selection thresholds depend on annual/course/district context. PDF 75 (printed 68) engineering, 77–78 (printed 70–71) Computer Science, 81 (printed 74) AI course information. `ugc-page-index.json` records extraction matches. The PDF was inspected with QA-only pypdf 5.9.0; no full copyrighted handbook is added to Git.
- Moratuwa IT: https://www.uom.lk/itfac/education/undergraduate/it — subject conditions plus district Z-score selection condition. Source review exposed incomplete overall eligibility modelling.
- IIT foundation: https://www.iit.ac.lk/foundation/it/ — documented O/L entry and 40% in each of four foundation modules for relevant progression, subject to provider decisions. No blanket admission guarantee follows.
- OUSL Business: https://ou.ac.lk/programme/bachelor-of-management-studies-honours-2/ — age, qualification alternatives and selection information reviewed; remaining provider evidence stays NOT_ASSESSED.
- Peradeniya Engineering: https://eng.pdn.ac.lk/academic/undergraduate-programme/ — subject and selection context considered with UGC handbook.
- Jaffna University College: https://ucj.ac.lk/hndmnt/ — specified vocational route and qualification information reviewed.
- UoVT Mechatronics: https://uovt.ac.lk/en/academics/courses/btech-mechatronics-technology — qualification route/conditions reviewed; no general equivalence or exemption inferred.

These checks concern published sources, not provider endorsement. Earlier WP2 records retain their original provenance. Not every legacy programme description, recognition record, career-skill relationship or scholarship was freshly independently validated. Scholarship presence is historical awareness; it is not an assertion that applications are open. No new scholarship is invented. Policy year and changing provider pages limit currency; refresh applicable intake requirements before real guidance.

## Confirmed defect and conservative repair

Subject passes alone previously allowed overall MET for PRG0001–3 while omitting general UGC evidence. Added SRC0021 and provider-review REQ0032–34; refreshed PRG0009 REQ0025. Same-sitting/attempt/Common General Paper and district selection evidence is not collected, so a subject match now yields NOT_ASSESSED overall. A known failed required subject still produces NOT_MET. No new admission score calculator or assumptions about age/district were introduced. Provider-review groups are excluded from numeric subject-match scoring; the score is never an admission probability.

A second repair distinguishes an omitted subject in a learner-declared complete examination from an incomplete record. Only a declared complete record establishes that the subject is absent; otherwise the result is NOT_ASSESSED. The declaration is not independently authenticated.

## Reproducible evaluation protocol

1. Freeze dataset SHA256s/model revision, source intake/date and scenario version before running.
2. For each rule, record rule ID, exact source location, applicable learner route and qualification conditions, AND/OR semantics, evidence absent and expected three-state outcome. Use scenarios.json and rule-evidence.csv together.
3. Check synthetic values against the source; obtain independent subject/provider review before claiming domain accuracy. Keep reviewer identity/role and disagreements under approved data handling.
4. Test boundaries, explicit failed grades, absent grades, missing complete-result declarations, unknown awards and conditional progression. Do not substitute unknown evidence with a rejection or eligible result.
5. Compare API results with reference outcomes; separately record source validity versus code execution. The 14 reference cases measure consistency with specified rules, not national admissions accuracy.
6. Check contradictions across rule groups, route alternatives, titles/framework metadata and source years. CSV integrity detects IDs/relationships, not whether an official statement is substantively correct. Refresh stale/contradictory source rows through review; do not silently infer equivalence.
7. Recheck links and provider decisions before actual learner use. Record inaccessible/ambiguous evidence as unresolved and retain NOT_ASSESSED.
