# Reproducing Research Sprint 2A

## Frozen baseline

Run date30October2026. GitHEAD `a19b68fa5b872fa9639eb653c3b528e803071a78`; actual API version0.6.0 (`backend/app/api/main.py:81`). Existing uncommitted academic preparation and both backups were present before evaluation. BASELINE.json records that status and351 pre-existing source/data/test/academic/evidence file hashes, excluding Python bytecode. No application/data edits were required. raw/dataset-records.json stores all20 CSV tables, not merely selected test rows.

| Curated dataset | Records |
|---|---:|
| data/master/institution_types.csv | 12 |
| data/master/programme_types.csv | 16 |
| data/master/qualification_frameworks.csv | 3 |
| data/master/qualification_types.csv | 18 |
| data/master/study_modes.csv | 6 |
| data/metadata/evidence_sources.csv | 21 |
| data/metadata/recognition_records.csv | 18 |
| data/reference/careers.csv | 5 |
| data/reference/institutions.csv | 11 |
| data/reference/programmes.csv | 11 |
| data/reference/qualifications.csv | 12 |
| data/reference/scholarships.csv | 1 |
| data/reference/skills.csv | 13 |
| data/relationships/career_skills.csv | 28 |
| data/relationships/programme_careers.csv | 15 |
| data/relationships/programme_entry_requirements.csv | 33 |
| data/relationships/programme_skills.csv | 22 |
| data/relationships/qualification_progression.csv | 5 |
| data/relationships/scholarship_applicability.csv | 2 |
| data/relationships/scholarship_eligibility_requirements.csv | 7 |

The entry-rule IDs areREQ0001–17 andREQ0019–34 (33 rows; nonconsecutive IDs are intentional, not an implied extra record). Programme IDsPRG0001–11, qualificationIDsQLF0001–12, progressionIDsPROG0001–5 and evidenceIDsSRC0001–21 are explicitly inventoried in the snapshot. Eligibility/progression API requests use real catalogue IDs and synthetic evidence only.

## Environment and commands actually executed

Python3.9.6, macOS15.5 arm64; interpreter `/private/tmp/wiselanka-repro-venv/bin/python`. FastAPI0.128.8, Pydantic2.13.5, Starlette0.49.3, HTTPX0.28.1. raw/pip-freeze.txt gives actual installed versions; no environment/dependency update was performed. Source PDF parsing uses existing QA-only pypdf5.9.0, not a new application dependency. Semantic model assets are not needed by this eligibility/progression harness.

From the repository root, the evaluation command was:

```sh
/private/tmp/wiselanka-repro-venv/bin/python docs/evidence/research-sprint2/educational-correctness/run_evaluation.py
```

Actual stdout/stderr are raw/harness-stdout.txt and raw/harness-stderr.txt; Python exit0. **Exit0 means completed measurement, not every expected outcome passed**:45 scenarios produced42 agreements/3 disagreements. RUN_MANIFEST.json records UTC times, versions and the locked oracle hash. FastAPI TestClient exercised actual in-process handlers and startup integrity checking; this was not a browser workflow, external admissions service or mocked eligibility response.

COMMAND_RESULTS.json preserves the exact focused-regression/integrity/pip commands and their zero exits. The five selected existing test files yielded40 passed. They are a regression check, not independent reference labels or the complete205-test suite. No earlierWP1–WP5 evidence runner was invoked, because those runners write to accepted evidence locations.

## Source capture and documentary provenance

`python3 docs/evidence/research-sprint2/educational-correctness/fetch_sources.py` attempted21 official URLs. Initial sandbox DNS failure exit2 is retained separately. The network-authorised retry returned21 HTTP200 responses. FETCH_RESULTS.json records requested/final URLs, actual UTC times, content types, bytes and SHA256s. SRC0004/SRC0021 snapshot the same15MB handbook; inspect its2025/26 edition and recorded PDF page locations. Access does not establish currency for another intake.

Three supplemental direct GETs are in SUPPLEMENTARY_FETCH_RESULTS.json: IIT admission page, UCSC programme page and UoVT prospectus. Their retrieval occurred **after** the first scenario execution and informed additional source/limitation analysis, not a silently rewritten oracle. Browser PDF-size limits/UCSC403 were overcome by direct downloads. The67-page UoVT PDF is image-only; pypdf yields no substantive text. Selected embedded JPEG pages were visually inspected, not automatically OCR-verified or all67 pages read. Relevant views include PDF16/29/30 (printed13/25/26); other inspected context pages are2/3/4/17/28/32/34/48/49/50/51. Exact internal prospectus publication year remains unverified despite its2026/27 URL.

`extract_sources.py` reproduces HTML/plain-PDF text using the standard HTML parser and QA pypdf. Image-only pages require visual inspection; an empty text extraction is not evidence that the source lacks conditions. For those inspected pages, the original JPEG stream was obtained from the page `/Resources` → `/XObject` image with `/DCTDecode` (possibly a list) using `get_object().get_data()`, then viewed locally. Images and PDFs remain in the ignored sources/ directory. Files were not uploaded or published. Stored catalogue dates were not refreshed to manufacture a source-verification history.

Source snapshots/full extracts are **local-only and ignored by Git**, including copyrighted handbook/prospectus content. Keep them for the approved local research archive. Re-fetching can return changed pages; check hashes and preserve both versions rather than overwriting the accepted copy. SOURCE_RECORD_AUDIT.csv describes the scoped claim verification; SOURCE_VERIFICATION_MATRIX.csv describes programme/pathway accuracy and limits.

## Re-run without overwriting this evidence

Copy the entire evaluation directory, including its local sources, to a **sibling** directory such as `docs/evidence/research-sprint2/educational-correctness-replay-01/`. Run that copy's run_evaluation.py from the repository root using a compatible environment. Its root/path derivation assumes this same directory depth. Do not rerun in the accepted evidence folder: the harness intentionally writes local outputs. Re-run source fetching only in the replay directory, with network permission where required.

Before starting, compare the20 dataset hashes and protected code hashes. The harness verifies the frozen SCENARIO_DEFINITIONS.csv hash from ORACLE_LOCK.json; it does not derive expectations from the engine or CSV predicates. The reference table is the experiment input. Reproduce the unchanged scenario values, do not regenerate expected outcomes from observed responses, and preserve disagreements. A different application snapshot requires a separately named experiment and an explicit comparison.

The harness first writes automatic result fields; raw/expected-vs-actual-before-review.csv preserves those original rows. EXPECTED_VS_ACTUAL.csv then records the evaluator's reviewed explanation/source findings. Automatic EC29 warning remains visible and is explicitly resolved as legitimate OR-branch reporting. Reproduction of the numeric decisions is automatic; reproduction of explanation/source adjudication requires reading the documented evidence. No independent human review is claimed.

## Evidence interpretation

Direct external-source facts, evaluator uncertainty conventions, missing-rule design checks and nonrepresentable reference facts are separately labelled. Twenty cases have direct published-condition reference outcomes,18 fully API-representable; only14 of those18 are academic decisions, with4 conditional-route text checks. The same evaluator knew the implementation, so documentary grounding is not independent expert adjudication. Missing data, self-reported awards, unknown selection and conditional route listings cannot establish actual admission.

No participant feedback, source endorsement, educational effectiveness, ranking-quality improvement or national accuracy is measured. This sprint adds evidence files only and stops before any fix, dissertation change, commit or push.
