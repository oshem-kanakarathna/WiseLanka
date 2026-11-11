# Stage 7 — backend and academic decision QA

**Run date:** 6 November 2026
**Application:** 0.6.0; source tree based on recorded evaluation snapshot `a19b68fa5b872fa9639eb653c3b528e803071a78` plus existing working-tree changes.
**Scope:** backend, curated CSV catalogue, eligibility/progression, recommendation ranking and API edge probes. No participant data, database records or research collection were used. The original 45-case evidence remains unchanged.

## A. Current test and data-integrity results

| Check | Actual result | Command/environment |
|---|---|---|
| Full backend suite | **264 passed, 5 skipped** | `/private/tmp/wiselanka-repro-venv/bin/python -m pytest tests/ -q`; Python 3.9.6, FastAPI 0.128.8, Pydantic 2.13.4, Starlette 0.49.3, HTTPX 0.28.1. |
| Focused catalogue, scenario, relevance suites | **41 passed, 5 skipped** | `pytest tests/integration/test_wp2_scenarios.py tests/unit/test_data_integrity.py tests/unit/test_relevance_engine.py tests/integration/test_hybrid_relevance.py -q`. |
| CSV catalogue integrity | **Passed** | `python -m backend.app.data_integrity`; 20 tables loaded, 11 programmes, 12 qualifications, 33 entry-rule records, 5 progression edges and all referenced identifiers/relationships passed the validator. |
| Frozen source-grounded scenarios | **43 agreements / 2 disagreements of 45; harness exit 0** | Replayed unchanged `SCENARIO_DEFINITIONS.csv` and `ORACLE_LOCK.json` through FastAPI `TestClient`, writing to a fresh OS temporary directory, not over the accepted evidence. All 45 requests returned HTTP 200. |
| Ranking invariants | Covered by passing tests for TF–IDF, fallback, deterministic tie order and academic partition preservation | The actual MiniLM inference tests were **skipped** in this environment because NumPy, ONNX Runtime and/or the tokenizer dependencies are unavailable. Fallback behavior was tested. |

The five skips were: three real MiniLM/encoder checks due missing optional local-model dependencies, the checksum-failure test because `onnxruntime` is absent, and the non-finite-vector test because NumPy is absent. Thus this run verifies policy-preserving deterministic/fallback behavior, but does not newly execute the actual ONNX model. Historical MiniLM evidence exists in WP3/WP5; it is not substituted for this current run.

The repository `.venv` has no pytest. The existing `/private/tmp/wiselanka-repro-venv` was used; no dependency or environment files were changed.

## B. Historical 43/45 comparison: current replay

The Sprint 2A original baseline remains **42/45** and is preserved at `docs/evidence/research-sprint2/educational-correctness/EXPECTED_VS_ACTUAL.csv`. The separate Sprint 2A.1 corrected replay recorded **43/45**, with EC39 and EC40 remaining. A new isolated replay of the same 45 synthetic cases on the present working tree again produced **43 agreements and 2 disagreements**. It did not change either expected outcome or the accepted evidence files. Temporary raw output was written under `/var/folders/7q/tr1whnfn4fg9dq6_vbx32jx80000gn/T/wiselanka-stage7-final-45-epxsimf2/` for this session.

| Case | Frozen expected result | Actual result | Evidence and rule context | QA classification |
|---|---|---|---|---|
| EC39 — `PRG0008`, OUSL Bachelor of Management Studies Honours | `NOT_MET`, based on synthetic reference context `age_at_registration = 17` against the reviewed OUSL page's minimum age 18 | `NOT_ASSESSED` | The API profile has subject results and examination completeness but no age-at-registration field. The official source is `SRC0016` / [OUSL programme page](https://ou.ac.lk/programme/bachelor-of-management-studies-honours-2/). `PROVIDER_REVIEW` is deliberately returned as unknown when provider-only evidence is unavailable (`backend/app/eligibility/engine.py`, requirement evaluation and `assess_academic_gaps`). | **Input-contract limitation, not a false eligibility result.** No age or date-of-birth field was added. |
| EC40 — `PRG0009`, University of Peradeniya Engineering | `NOT_MET`, based on synthetic reference context `CGP_all_allowed_attempts = [29,29,29]` against the inspected UGC 2025/26 handbook's 30% Common General Paper registration minimum | `NOT_ASSESSED` | The API does not accept Common General Paper marks, sitting/attempt history or selection cut-off evidence. The verified source snapshot is `SRC0021` / [UGC 2025/26 admissions handbook](https://www.ugc.ac.lk/downloads/admissions/Handbook_2025_26/student_handbook_english.pdf#page=16); the rule is represented as provider review in `data/relationships/programme_entry_requirements.csv` (`REQ0025`). | **Input-contract limitation, not a false eligibility result.** The correct conservative output is unknown on the supplied request. Do not add exam-history collection without a justified approved scope. |

Both reference outcomes contain information deliberately not sent to the application. These cases do not show incorrect rule execution on the submitted request. They show that the current request cannot reproduce a richer external reference decision. Do not relabel the expected results to match the system or call 43/45 an eligibility accuracy score. The denominator mixes academic, uncertainty, missing-rule and progression cases and the oracle was authored by an evaluator who had inspected the system.

EC29 retains a structural warning because a known failed A/L branch coexists with unresolved alternative-qualification routes. The final overall state remains `NOT_ASSESSED`, which is consistent with unresolved OR alternatives; this is not a third disagreement. The replay also confirms EC08 remains corrected to `NOT_ASSESSED` when completeness is omitted.

## C. Defect found and correction

### Corrected: IIT Computing Foundation rule-level source attribution

The official-source audit found that `SRC0009` (`https://www.iit.ac.lk/foundation/`) does not state the four numerical O/L predicates, whereas the detailed Computing Foundation page `SRC0010` (`https://www.iit.ac.lk/foundation/it/`) was inspected and supports the entry conditions at the recorded scope. Previously `REQ0014`–`REQ0017` exposed the general page as the rule citation. This was a provenance/explanation defect, not evidence that the thresholds themselves were wrong.

Changed only the four `source_id` cells in [programme_entry_requirements.csv](/Users/dan/Documents/UWL/FP/WiseLanka/WiseLanka/data/relationships/programme_entry_requirements.csv:15) from `SRC0009` to `SRC0010`; all operators, descriptions, counts, grades and requirement logic remain unchanged. Added [test_iit_foundation_ol_requirements_link_to_detailed_entry_source](/Users/dan/Documents/UWL/FP/WiseLanka/WiseLanka/tests/integration/test_wp2_scenarios.py:115), which checks the API response exposes the detailed source for all four requirements. The test passed in both focused and full-suite runs. The pre-existing source verification matrix remains historical evidence of the prior gap; it has not been rewritten.

No other confirmed high-priority functional defect was established in this review. No eligibility or progression code was changed.

## D. Eligibility, data and API findings

- **Three-state assessment:** `assess_academic_gaps` in `backend/app/eligibility/engine.py` maps documented rule outcomes and missing evidence into `MET`, `NOT_MET` or `NOT_ASSESSED`. Missing examination completeness does not become a count failure after Sprint 2A.1; false, true, omitted and malformed values have regression coverage. Requirements that depend on missing subjects become `NOT_ASSESSED` unless the relevant exam is explicitly complete. Provider-review predicates remain unknown.
- **Eligibility vs relevance:** `/personalised-recommendations` documents `academic_gap_insights.status` as canonical and warns that legacy `eligible`, category and score fields must not override it (`backend/app/api/main.py:242–258`). `backend/app/relevance/engine.py:118–130` fixes `MET → NOT_ASSESSED → NOT_MET` group order and ranks only within a group; scores are described as text similarity, not admission probability. Tests cover group preservation, input immutability, fallback and deterministic tie-breaking. Actual MiniLM inference was not rerun because dependencies were missing.
- **Knowledge base:** the full integrity validator passed on the 20 CSV tables. It checks IDs, relationship references, duplicates, requirement group operators/counts and approved domains (`backend/app/data_integrity.py:28–100`). The validator cannot establish policy freshness or correctness; saved source verification remains intake-bounded and includes partial/unverified records.
- **Coverage gaps retained as uncertainty:** PRG0005–PRG0007 have no verified direct-entry minima in the inspected sources and remain `NOT_ASSESSED`; the foundation progression route is not treated as direct admission. EC39/EC40 policy fields are not represented. UGC 2025/26 and other undated/provider pages need intake refresh before real-world use.

Synthetic API edge probes produced:

| Input | Actual response |
|---|---|
| Missing learner education and no qualification | Personalised endpoint HTTP 422 with validation detail. |
| Missing required `student_results` | HTTP 422. |
| Grade `Z` | HTTP 422. |
| Duplicate subjects after whitespace/case normalization | HTTP 422. |
| Unknown qualification catalogue ID | HTTP 422. |
| Empty flat recommendation profile | HTTP 200, zero recommendations. |
| Unknown programme at `/eligibility` | HTTP 200, `NOT_ASSESSED`, “Unknown programme”; no positive eligibility claim. |
| Unknown qualification at `/progression/QLF9999` | HTTP 200, zero pathways. |
| Unsupported examination level `T_LEVEL` | HTTP 422. |

Unknown programme/qualification empty-result behavior is already part of the API's graceful contract and tests. The public endpoints do not currently normalize an arbitrary nonblank subject name against a closed subject catalogue. The existing interface supplies controlled options, and no authoritative exhaustive subject-name list was established in this QA; therefore no speculative subject whitelist was introduced. If a future design needs strict subject validation, first establish a verified, extensible subject reference set and compatibility rules.

## E. Files changed in this QA

1. `data/relationships/programme_entry_requirements.csv` — corrected provenance IDs for REQ0014–REQ0017 only.
2. `tests/integration/test_wp2_scenarios.py` — added a focused API regression test for those source links.
3. `docs/final-submission/research-documentation/STAGE7_BACKEND_QA.md` — this report.

Other modified/untracked files were already present in the working tree and were preserved. In particular, the existing dirty `backend/app/api/main.py`, research module, academic documents and two JavaScript backups were not changed by this QA.

## F. Readiness for frontend redesign

**Assessment: suitable to proceed with a frontend redesign against the existing prototype API, with contract-level caution; not production or educational-policy release readiness.** The current backend suite, frozen scenario replay, data-integrity validation and representative API edge probes pass. Academic state and relevance are separated, and the established endpoints return structured uncertainty rather than turning the two unrepresentable reference facts into eligibility decisions.

Before frontend integration is treated as stable, the redesign should consume canonical `academic_gap_insights.status`, preserve `NOT_ASSESSED`, keep similarity separate from admission status, handle HTTP 422/503 and empty arrays, and test against a pinned OpenAPI/API response contract. Configure and verify the optional local model dependencies in the intended development environment if semantic inference is part of the redesign acceptance criteria; the present environment only verified fallback behavior. Continued source refresh and direct-entry coverage remain research/product limitations, not blockers to a visual redesign.

No human evaluation, independent relevance judgements or educational-effectiveness claim is supported by this QA. Research collection remains outside scope and disabled.
