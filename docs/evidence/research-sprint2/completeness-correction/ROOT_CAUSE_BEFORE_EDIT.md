# Root cause recorded before editing — Sprint 2A.1

EC08 was reproduced against the unchanged `/eligibility` API using the exact frozen SCENARIO_DEFINITIONS.csv request. ProgrammePRG0004 receives five O/L passes (MathC,EnglishC,ScienceC,ICTS,SinhalaS), with `education_complete={}`. Original response: HTTP200, NOT_MET. Omitting the field entirely has the same result. Original request/responses and all boundary probes are in raw/before-reproduction.json; Sprint2A files are hash-protected and are not rewritten.

Trace: `EligibilityRequest` (`backend/app/api/main.py:130–133`) defaults omitted completeness to an empty dictionary. Result normalisation delegates to `LearnerProfile.validate_results`, trimming subject/grade strings and preserving flat A/L versus nested examination sections; it does not establish that the entered subjects exhaust the examination. The personalisation contract also defaults omitted completeness to `{}` (`backend/app/personalisation/models.py`). The endpoint calls the rule evaluator and then `assess_academic_gaps` for authoritative three-state explanations.

At `backend/app/eligibility/engine.py:816`, `complete.get(level, True)` treats a missing examination-specific key as true for failed count predicates. Five supplied passes are fewer than six, so the legacy predicate fails; the canonical layer retains NOT_MET as though the examination were declared complete. Its AND aggregation makes the whole foundation assessment NOT_MET. Named-subject rules already use `complete.get(level) is True` to distinguish confirmed absence from unknown absence. Count rules are inconsistent with that standard. The headline explanation then inherits a stronger failure conclusion than the available evidence supports.

Before-edit probes:

| Completeness input | API behaviour |
|---|---|
| Field omitted / `{}` | NOT_MET for EC08 |
| `{"O_LEVEL":false}` | NOT_ASSESSED |
| `{"O_LEVEL":true}` | NOT_MET, justified by the explicit complete five-pass declaration |
| Top-level null, level-specific null, empty-string value | HTTP422 validation rejection, no academic decision |
| A/L partial two-pass count / one-approved-subject count without flag | NOT_MET; the same defect affects A_LEVEL_PASS and SUBJECT_SET_COUNT |
| Reported NVQ4 award without examination results | NOT_ASSESSED; qualification/provider-review rules bypass examination count handling |

Direct engine calls normalise None/empty completeness to `{}` and share the same risk. An unrelated level key must not establish completeness of the assessed level. Empty/missing result sections already remain NOT_ASSESSED. Positive sufficient counts can be MET without completeness because additional results cannot invalidate those count minima. A supplied below-minimum mandatory subject grade remains demonstrably NOT_MET, even when other results are incomplete. Existing six/nine-subject profiles satisfying the published minima must retain MET; count-failure fixtures must explicitly state completeness if they intend to prove a global count deficit.

Minimum correction selected: require `complete.get(level) is True` before treating a failed count as established. Keep request schema/422 handling, grade thresholds, CSVs, qualification semantics and ranking code unchanged. Update the stale model comment and count-unknown explanation to reflect unknown as well as explicitly incomplete records. Add focused regressions before changing the engine; retain the original failed reproduction/test output. No age/CGP inputs, source-attribution repair or unrelated Sprint2A issue is included.
