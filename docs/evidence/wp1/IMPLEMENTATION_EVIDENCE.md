# Work Package 1 implementation evidence

Date: 2026-10-29. WP1 corrections verified and closed. Baseline HEAD: `e79e883`; changes are uncommitted.
Approved requirements: recovered proposal excerpts supplied by the project owner.
The original proposal, interim report, supervisor feedback, rubric and ethics
approval have not been revalidated through this implementation.

## Requirements and completion

| Requirement | WP1 result | Evidence |
|---|---|---|
| A: complete O/L input | Additional subject rows support nine and more subjects, including custom names. Mathematics/English and the initial four optional rows remain. | `frontend/components/learner-profile.js`, `test_learner_gaps.py`, nine-subject API/live cases |
| A: compatibility and validity | Six-subject and flat/nested A/L requests remain supported. Blank/invalid grades and duplicate normalised subject names are rejected. Nine subjects are not a global prerequisite. | `personalisation/models.py`, `test_learner_gap_api.py`; existing suites |
| A: incomplete results | Users explicitly choose “Not reported”; unset grade rows block submission. A confirmation records completeness. Conflicting complete/unreported choices block submission. Insufficient counts with incomplete input remain unassessed. | Profile UI/browser tests and live incomplete scenario |
| B: structured profile | Three learner categories; structured awards (title, optional catalogue ID, framework, level); optional skill self-reports. No accounts, identifiers or persistence added. | `personalisation/models.py`; qualification-only API/browser/live cases |
| C: academic gaps | Existing eligibility engine supplies pass/fail calculations. An additive evidence-aware assessment provides MET/NOT_MET/NOT_ASSESSED at requirement, AND/OR group and programme levels, with sources and next steps. | `eligibility/engine.py`; `test_academic_gap_insights.py` |
| C: personal skills | Career requirements compared with explicit reports and development interests. Unreported skills remain NOT_ASSESSED. No competence or proficiency verification is claimed. | `skills/engine.py`; API/browser/live cases |
| D: interface | Existing cards and responsive workspace retained. Labels, focus after adding rows, visible keyboard focus, live status/error focus, empty/failure states and retry for unavailable choices included. | Profile HTML/CSS/JS; mobile and keyboard browser checks; screenshots |

FR1–FR3 are extended; FR5–FR6 gain learner-specific insights. Existing FR4
alternatives and progression are preserved, not expanded. Objectives III and V
are supported through structured input and demonstrable insights; Objective VII
through synthetic automated evaluation. Objective IV receives better structured
inputs and explanations, but its AI-assisted component remains outstanding.

## Contracts and design decisions

`POST /personalised-recommendations` retains its envelope and original fields.
New optional request fields are `learner_category`, `existing_qualifications`,
`self_reported_skills`, and `education_complete`. `education` is still required;
use `{}` for a qualification-only profile. At least examination results or one
award is required. Categories describe context; they do not affect eligibility.

An award contains `title`, `qualification_id`, `framework`, `level`; only its title
is required. Awards are self-reported context. They never substitute for exam
results or establish an NVQ/SLQF equivalence. Custom awards use an empty catalogue ID because the catalogue has limited coverage.
When an ID is supplied it must reference an active catalogue record, and nonblank
metadata must match that record. Omitted framework/level metadata is filled from
the record, and returned text is canonicalised. This checks catalogue consistency,
not award authenticity or admission equivalence. No certificate identifiers are used.

Each optional skill contains `skill_id` and `status` (`REPORTED` or
`DEVELOPMENT_OPPORTUNITY`). Duplicate or unknown/inactive skill IDs are rejected.
Canonical skill/qualification choices come from new read-only
`GET /profile-options`, using existing CSV files. If choices cannot load, the UI
permits manual award/examination entry and offers retry; it does not invent skills.

New response fields include `academic_insights`, `learner_skill_insights`, reported
awards/category and an award-assessment note. Each recommendation also contains
`academic_gap_insights`. With no examination-based recommendations, the limited
active catalogue is shown as unassessed academic guidance, not recommendations.

Academic insight aggregation: AND requires all MET; a known NOT_MET makes the
conjunction NOT_MET. OR requires one MET; with none MET and some unknown it is
NOT_ASSESSED. Missing rules, source records, unsupported rule types and missing
subject/level input remain NOT_ASSESSED. Incomplete insufficient counts remain
NOT_ASSESSED; a supplied grade below the threshold can establish NOT_MET. No
thresholds were copied into the insights layer.

Legacy eligibility booleans/categories/scores remain unchanged for compatibility.
Consumers must use the new insight status to distinguish uncertain evidence;
the updated UI suppresses the legacy negative label and score when academic
insights are NOT_ASSESSED. Omitted completeness flags retain legacy interpretation
of submitted count results. The UI starts its completeness confirmation unchecked.

Skills use `SELF_REPORTED`, `DEVELOPMENT_OPPORTUNITY`, or `NOT_ASSESSED` for insight
status and retain `REPORTED`/`DEVELOPMENT_OPPORTUNITY`/`UNREPORTED` report categories.
They deliberately do not say a career competence requirement is MET. Expected
career levels are displayed without claiming the learner meets them. Reports
outside the selected career are retained with relevance unassessed. Missing career
evidence does not generate a negative judgement. Programme–career alignment is
unchanged and is not used as learner competence evidence.

Alternatives considered: imposing nine subjects globally would break valid partial
and six-subject assessments; deriving personal competence from a programme would
be unsupported; deriving qualification equivalence from framework numbers would
be unsafe. A new database, account system or separate service was unnecessary.
The existing modular architecture and CSV data are retained with no dependency
changes. The recommender remains rule-based, not trained AI.

## Modified and added files

| File (relative to repository) | Purpose |
|---|---|
| `backend/app/personalisation/models.py` | Added typed profile, award and skill contracts and validation |
| `backend/app/api/main.py` | Uses shared profile model; adds read-only CSV options endpoint |
| `backend/app/eligibility/engine.py` | Adds evidence-aware tri-state gap view using existing rule evaluations |
| `backend/app/skills/engine.py` | Adds self-report/career comparison, separate from programme alignment |
| `backend/app/personalisation/engine.py` | Shared validation and additive academic/skills insight responses |
| `frontend/pages/learner-profile.html` | Learner context, awards, skills, completeness and insight containers |
| `frontend/components/learner-profile.js` | Dynamic subjects, validation, CSV choices, payloads and insight rendering |
| `frontend/components/learner-profile.css` | Scoped form/focus/reflow styling |
| `tests/integration/test_learner_gap_api.py` | New synthetic API/compatibility scenarios |
| `tests/unit/test_academic_gap_insights.py` | Missing evidence, unsupported rules and AND/OR uncertainty tests |
| `frontend/browser_tests/test_learner_gaps.py` | Thirteen synthetic browser interaction checks with mocked API responses |
| `frontend/browser_tests/live_integration_check.py` | Optional API-base override; original live assertions retained |
| `frontend/browser_tests/live_learner_gap_check.py` | Real-API WP1 scenarios and screenshot capture |
| `docs/evidence/wp1/*` | This summary, actual test logs and synthetic UI screenshots |

The pre-existing staged README, Git history, CSV files and both untracked
JavaScript backups were preserved. No commits or pushes were made.

## Verification and actual outcomes

Final backend run: **132 passed** (original 92 plus 40 new cases).
Final browser suite: **22 passed** (original 9 plus 13 new tests).
Original live check: **passed**, one recommendation and three progression items.
WP1 live check: **passed**, five successful real-API form submissions, one rejected contradictory
catalogue request and mobile reflow, with no JavaScript page errors. See the logs alongside this document.

| Synthetic scenario | Actual result |
|---|---|
| Six O/L subjects, two credits, confirmed complete | Existing foundation assessment NOT_MET; missing credit count explained |
| Six O/L subjects, three qualifying credits | MET without requiring nine subjects |
| Nine subjects, third credit in ninth subject | MET and existing engine `eligible=true` |
| Existing flat/nested A/L profiles | Three eligible results retained |
| Missing/invalid grades, blank or normalised duplicate subjects | API 422; missing/duplicate UI submissions blocked |
| Award alongside exam failure | Award does not override the unmet exam requirement |
| Qualification-only vocational profile | Award retained; academic status NOT_ASSESSED, no inferred admission route |
| Reported Programming and OOP development interest | Separate SELF_REPORTED/development states; other career skills unassessed |
| No reported skills | All recorded career skills NOT_ASSESSED, never inferred absent |
| Unknown career | No invented career requirements; reports preserved |
| Incomplete low counts/missing subject | NOT_ASSESSED rather than a false negative in new insights/UI |
| Supplied low English grade despite incomplete profile | NOT_MET for that actual academic requirement |
| Missing source evidence/no programme rules/unsupported rules | NOT_ASSESSED |
| Satisfied OR option with other options absent | Group MET; alternatives are not falsely treated as mandatory |
| Delayed catalogue response or retry with an existing award row | Choices populate without losing manual metadata; selected awards can be edited into custom reports |
| Unknown/inactive or contradictory catalogue reference | API 422; omitted metadata on a valid reference is filled consistently |
| Keyboard removal of qualification/subject rows | Focus moves to a neighbouring row or Add button |
| Endpoint uncertainty with missing sources or incomplete results | Canonical insight remains NOT_ASSESSED alongside unchanged legacy fields |
| New context fields with existing A/L profile | Every legacy recommendation field equals baseline output |
| 390px viewport and keyboard-added row | No horizontal overflow; focus moves to the added subject |
| Options service failure | Retry message and manual award entry remain available |

Environment: Python 3.9.6. Final backend suite used the existing reproduction
virtual environment `/private/tmp/wiselanka-repro-venv` with pytest 8.4.2,
FastAPI 0.128.8, Pydantic 2.13.5 and HTTPX 0.28.1. Browser tests and live API used
project `.venv`, Playwright 1.60.0 and Pydantic 2.13.5. An earlier backend pass also
ran under system Python/Pydantic 2.13.4; the final recorded pass uses the pinned
version. No fresh installation was performed for WP1.

Initial verification issues were resolved: project `.venv` lacks pytest; system
Python lacks Playwright. An initial Python 3.10-style union annotation failed on
3.9 and was corrected. Sandbox Chromium launches failed and were rerun with
approved escalation. Existing port 8000 served stale API code and port 8001 was
occupied; a separate updated API on 8011 was used without stopping user servers.
The temporary API was stopped after verification. Restart the usual backend to
load the new endpoint and response fields before reviewing the UI on port 8000.
These failed setup attempts are not counted as passing tests.

Reproduction commands:

```sh
python -m pytest tests/ -q
python -m unittest discover -s frontend/browser_tests -p 'test_*.py' -v
python frontend/browser_tests/live_integration_check.py
python frontend/browser_tests/live_learner_gap_check.py
```

Use an environment with requirements-dev.txt installed and Chromium available.
Live scripts require frontend on 5500 and an updated API (default 8000).
Set `WISELANKA_API_BASE=http://127.0.0.1:8011` when using an alternative test port.
The frontend supports the same local override through `window.WISELANKA_API_BASE`
set before its script loads. Browser tests require permission to launch Chromium.

## Demonstrable interface evidence

- [Nine-subject result and requirement sources](nine-subject-results.png)
- [Mobile skill insight states](mobile-skill-insights.png)
- [Qualification-only vocational profile](qualification-only.png)
- [Backend test output](backend-tests.txt)
- [Browser test output](frontend-tests.txt)
- [Original live check](live-integration.txt)
- [WP1 live scenarios](live-wp1.txt)
- [Timestamped commands, exit codes and source/evidence SHA-256 hashes](verification-manifest.json)

Screenshots were captured from synthetic real-API sessions. They demonstrate
rendered states, not participant evaluation or accessibility conformance.

## Limitations and DSR use

The qualification catalogue and career-skill knowledge remain computing-focused.
Vocational profile representation is supported; vocational admission/pathway
coverage is not added in WP1. Self-reports do not establish proficiency, award
authenticity or equivalence. Career-skill mappings currently lack per-relationship
source citations; the UI and API disclose this. Academic source URLs are drawn
from stored provenance and were not independently reverified online here.

Grade vocabulary remains the existing engine's A/B/C/S/F. Subject aliases and
retake/sitting reconciliation are not implemented. This is a single supplied
results set per level; missing individual subjects are conservatively unassessed.
Exact repeated keys in raw JSON are collapsed by JSON parsing; normalised distinct
keys are checked for duplicates and the UI prevents duplicate entries before
serialisation. Legacy consumers still need to adopt the new uncertainty fields.

Checks cover Chromium, one mobile viewport and selected keyboard interactions;
there is no full screen-reader, cross-browser or WCAG conformance evaluation.
No new usability participants, feedback, recommendation-quality study or AI
comparison were conducted. Existing tests and these checks do not establish
population-wide effectiveness or educational benefit.

For Design Science Research, retain the requirement mapping, design alternatives,
synthetic inputs and logs as artefact-development/demonstration evidence. Use the
scenario set as a starting point for independently checked expected outcomes,
explanation-fidelity review and approved adult-only usability/accessibility
research. Do not reuse automated pass counts as evidence of user satisfaction.
WP2 and AI/chatbot/multilingual/voice work have not been started.


## Acceptance-audit correction closure

The catalogue loading race is corrected by refreshing selects in existing award
rows when choices arrive, without dispatching change events or overwriting manual
metadata. Retry uses the same path. Existing skill choices are retained on refresh.
A shared removal helper moves keyboard focus to the next/previous row, or the Add
button when no rows remain. Catalogue consistency is enforced in the shared typed
award model, so API and direct personalisation callers use the same validation.

The API endpoint description now identifies academic_gap_insights.status and
academic_insights[].status as the canonical evidence-aware status. Two new endpoint
regressions explicitly exercise the legacy false/unknown and true/unknown cases.
Legacy eligible/category/match_score values are preserved for compatibility; they
must not supersede an unknown evidence-aware assessment.

The qualification-only screenshot now captures the reported-award element itself.
Final logs were generated by successful subprocess executions with exit codes,
commands, timestamps and source/evidence hashes saved in verification-manifest.json.
All audit correction conditions are closed within WP1's stated prototype scope.
Remaining research, coverage and accessibility limitations above are unchanged.
No participant evaluation, educational-effectiveness result or official-source
reverification is claimed. Original staged changes and both backup files remain
untouched. No Git commit/push or WP2 implementation formed part of this closure.
