# WP5 system quality and evaluation evidence

Date: 2026-10-29. WP4 checkpoint: `4da06fe`. No WP5 commit or push. Both unrelated JavaScript backups and prior README history preserved. No WP6 work started. User-facing prototype is ready for a conditional feature freeze; research and manual validation are incomplete.

## Actual final verification

| Check | Actual outcome | Evidence |
|---|---|---|
| Backend | 205 passed | backend.log |
| Browser regression | 36 passed | browser.log |
| Live original, WP1, WP2, WP3, WP4 | 5 workflows passed | live-*.log; regression screenshot subdirectories |
| CSV integrity | Passed: 11 programmes, 12 qualifications, 33 requirement rows, 5 progression edges, 21 evidence sources | csv-integrity.log |
| Synthetic source-reference cases | 14/14 passed; assistant requests preserve ranking | scenarios.json; scenario-results.json |
| Ranker comparison | 9 synthetic cases, deterministic / TF-IDF / semantic | comparison.json; ranker-comparison.log |
| Automated accessibility | Zero detected violations in 9 states; 320/390px reflow passed | accessibility-final.json |
| Fresh optional-AI environment | Install and pip consistency passed; model hashes verified | fresh-install.txt; pip-check.log; provisioning-receipt.json |
| Missing model / HTTP recovery | Explicit RULE_BASED_FALLBACK in separate process; real-model server continues SEMANTIC | runtime-network.json |

All 13 final runner checks returned exit code 0, recorded with commands in verification.json. Earlier source-correction failures are retained to show the defect and repair. An initial runtime probe used the wrong expected fallback label; only the probe assertion was corrected, with the rerun passing. No test result was inferred from an old work package.

## Confirmed corrections

1. **High educational-correctness defect:** state-university subject matches omitted unresolved UGC general-entry/selection evidence for PRG0001–3. Official handbook inspection led to SRC0021 and explicit provider-review rules. Subject passes now leave overall NOT_ASSESSED. PRG0009's existing review rule also records the documented general conditions. No guaranteed admission or inferred Z-score.
2. **Medium missing-evidence defect:** absence of a named subject in a declared complete examination now differs from absence in an incomplete record. The former can establish NOT_MET; the latter remains NOT_ASSESSED.
3. **Medium explanation defect:** unassessed provider rules no longer appear as failed academic requirements; recommendation categories follow canonical uncertainty. Provider review does not reduce the separate subject-match score.
4. **Accessibility defects:** prohibited ARIA labels on generic elements and measured contrast failures corrected with region semantics and focused colour changes. Zero findings is limited to automated scanned states.

Existing tests were updated for the corrected policy semantics while preserving grade/score, fallback and integration assertions. Five new policy regression cases were added. Neither semantic relevance nor chatbot guidance changes formal eligibility.

## Performance observations

Frozen MiniLM ONNX CPU model load: 0.288s. Forty warm in-process requests: median 13.5ms, p95 14.9ms. Forty local HTTP requests: median 13.3ms, p95 13.6ms. Process peak RSS: 302.3 MiB (whole process high-water mark, not isolated model size). Single-machine measurements do not establish production throughput or cross-platform performance.

## Academic interpretation

The supplied proposal excerpts are mapped requirement-by-requirement in REQUIREMENTS_TRACEABILITY.md. Bounded profile, recommendation, alternatives, skills, explanation, links and guided support functionality is implemented. Critical literature review is unverified; learner-needs evidence and overall evaluation remain partial. Objective VI remains partly validated because translations and native speech require human/device checks. The original proposal's full research questions/NFRs/rubric and ethics conditions remain uninspected.

Official-source checking uncovered and repaired a real omission; it is not a comprehensive independent educational accuracy study. Reference scenarios verify the specified rules and missing-evidence handling, not actual provider admissions. The small catalogue and unverified provider decisions remain explicit limitations.

No independent relevance labels exist: nDCG@3, accuracy uplift and preference improvement are not computed. Ordering differences and runtime are measured; superiority, educational benefit and satisfaction are unproven. No automatic feedback learning was added.

The draft study package contains participant information, consent wording, tasks, observation/questionnaire templates, analysis and pending manual checks. No participants, SUS scores or feedback exist. Recruitment is blocked until signed ethics conditions and incomplete contact/storage/withdrawal fields are reviewed. Sinhala/Tamil fluent review, native voice/languages, screen readers, complete keyboard/zoom checks and target-device testing remain pending.

## Design Science Research contribution

The designed artifact now has reproducible functional/scenario evaluation, baseline ranking comparisons, source-rule traceability and measured runtime evidence. Source review and accessibility scans supplied concrete observations used in an evaluated refinement cycle. These are technical artifact evaluations, separate from later approved human usability and independent relevance evaluation. Evidence does not replace the literature/problem-investigation or dissertation interpretation stages.

## Evidence index and next decision

- REQUIREMENTS_TRACEABILITY.md — objectives I–VIII and FR1–FR9, implementation versus validation.
- EDUCATIONAL_SOURCE_REVIEW.md; rule-evidence.csv; ugc-page-index.json — actual checked sources and conservative rule semantics.
- AI_EVALUATION_PROTOCOL.md; comparison.json — current functional results and unexecuted independent-judgement protocol.
- ACCESSIBILITY_REVIEW.md; accessibility-*.json — detected findings, fixes, limits and pending manual checks.
- study/ — draft-only ethics-aligned materials and empty data templates.
- REPRODUCIBILITY.md; verification.json; dataset-sha256.json; provisioning-receipt.json; security-review.json — setup, commands, hashes, scope-limited secret review.
- OPEN_ISSUES.md — submission/evaluation blockers and feature-freeze conditions.
- modified-files.txt — all changed/new files excluding the preserved unrelated backups.

Recommendation: **freeze the bounded prototype for controlled evaluation, with documented conditions**. No confirmed blocking regression remains in the executed checks. Before academic closure, obtain the missing approved documents, conduct authorised adult evaluation and complete relevant independent/manual checks. This report stops WP5 implementation; it does not start WP6.
