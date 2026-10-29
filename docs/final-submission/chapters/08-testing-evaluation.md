# 8. Testing and evaluation

## 8.1 Evidence snapshot and repeatability

The evaluated code/data checkpoint is `07f4b97` (WP5). Individual logs, command lines, exit codes, model/dependency versions and dataset hashes are saved under docs/evidence/wp5/. `scripts/verify_wp5.py` runs all final checks with local API/static servers and writes a new verification manifest. Re-running changes the local evidence outputs, so preserve the submitted snapshot before further experiments. WP6 documentation work has not added application features or silently rerun these measurements.

## 8.2 Executed technical evaluation

| Layer | Actual result | Interpretation |
|---|---|---|
| Backend automated tests | 205 passed | Specified domain/API/regression behaviour under tested cases |
| Browser automated tests | 36 passed | Tested DOM/forms/interactions, including mocked API/speech cases |
| Live workflows | Original + WP1–WP4: five passed | Browser-to-real-API integration on local servers |
| Synthetic reference scenarios | 14/14 passed | Agreement with implementer-authored expected rule outcomes |
| CSV integrity | Passed | Structural consistency, not substantive policy truth |
| Fresh environment / model | Installed and checksum-verified; pip check passed | Reproduction on the tested Python/macOS platform |
| Automated accessibility | Zero detected violations in nine states | Selected axe rules/states; manual accessibility remains pending |

The reference set includes six/nine-subject O/L, missing/failed grades, state-university A/L evidence, Business/Engineering, reported vocational qualifications, custom awards and confirmed/incomplete examination declarations. The scenario runner additionally checks that asking the assistant leaves ranking unchanged. Other unit/browser tests cover reported/unreported skills, duplicate subjects, model failure, language switching, keyboard controls and mocked recognition errors. These are complementary checks, not counts of independent participants.

## 8.3 Educational correctness review

Source inspection reviewed selected official requirements and progression evidence and discovered the UGC omission discussed in chapter 6. The engine then matched all 14 specified outcomes. However, the same implementer authored both many tests and the rule interpretations. Neither an error-free catalogue nor an independently validated admissions classifier follows. A domain reviewer should adjudicate the source-reference mapping and challenge boundaries, unsupported awards and policy-year mismatches.

An observed MET means the available evidence meets represented requirements. Unknown current intake/provider conditions remain unresolved. Tests do not authenticate grades, verify awards or reproduce selection decisions. These limitations are integral to interpretation, rather than exceptions to be hidden in a footnote.

## 8.4 Ranking and performance evaluation

The nine-case comparison records actual orders/scores and invariant academic groups for deterministic, TF–IDF and frozen semantic methods. No independent relevance ratings were available; `ndcg_at_3` remains null. All cases are synthetic and should not be described as user trials.

On Python 3.9.6/macOS 15.5 arm64, model loading took 0.288 seconds. Forty warm in-process requests had median 13.54 ms and p95 14.95 ms. Whole-process high-water RSS after requests was 302.33 MiB. The separate local-HTTP probe measured median 13.28 ms and p95 13.57 ms over 40 requests. The two probes have different overheads and run conditions, so their small difference is not evidence of network speedup. The source-reference runner's separate timing is not substituted for this comparison measurement.

These measurements use warm, sequential local requests with a tiny catalogue. They exclude full browser rendering, concurrent load, fresh dependency installation and model download; “model load” is not end-to-end cold-machine startup. No statistically supported performance superiority or production capacity is claimed. Missing-model fallback was separately executed and successful normal-model service was confirmed afterwards.

## 8.5 Accessibility and multilingual evaluation

Pinned axe-core 4.10.3 tested WCAG 2A/AA and 2.1AA-tagged checks on learner-profile empty/populated states in three languages and three older English pages: nine states in total. Initial ARIA/contrast findings were corrected. The final scans detected zero violations and 320/390px reflow probes passed. Scan incompletes are retained. This is not a complete WCAG 2.2 conformance audit.

Browser tests verify that language switching preserves entered data and results, translation keys are present and specific keyboard controls work. Strings have not been independently reviewed by fluent Sinhala/Tamil speakers. Speech tests use mocks for permission/error transitions; live headless checks detect capability without testing native audio or transcription. Manual screen-reader, full keyboard, zoom, target-device and native speech/language checks remain pending.

## 8.6 Human study and independent labels — pending

The ethics-review package contains adult-only information/consent drafts, six synthetic task cards, observer records, an eight-item custom questionnaire and objective explanation questions. It is not yet released for recruitment. Signed approval conditions, contacts, recruitment, storage/retention and withdrawal details must be verified first. No sample size or achieved demographic balance is fabricated.

Planned analysis distinguishes unassisted versus assisted task success, elapsed time, errors, comprehension and subjective clarity. The custom questionnaire is not SUS. The current instruments include comprehension probes and perceived clarity items, but no defined comparison condition or dedicated trust measure. They cannot establish that explanations improve understanding/trust, or that access features improve accessibility relative to a baseline. Such claims require an appropriate design and approved instruments, or explicitly bounded descriptive conclusions. An optional standard SUS instrument requires appropriate source/licence/institutional review before use; no SUS result exists. Independent relevance judgements use a separate blinded protocol and must not be treated as satisfaction ratings.

**Results insertion area — NOT COLLECTED:** approved ethics/version; eligible adult sample and recruitment; task completion/time distributions; explanation comprehension; questionnaire response distributions; language/accessibility observations; independent relevance agreement and nDCG where computable. Replace this paragraph only with actual collected and auditable evidence, retaining missingness and adverse findings.
