# Evaluation plan v0.2 — proposed for supervisor and ethics review

**Not approved for recruitment or data collection.** This plan strengthens the existing WP5/WP6 instruments; it does not assert an amendment has been approved. The signed university ethics decision and conditions must be inspected first. Preserve the exact approved questions; qualify answers rather than redefining “improve” to mean “implemented”.

## Small, manageable study

Proposed target: **8 consenting adults**, exploratory convenience/purposive recruitment, with a practical range of6–10 only if approved. Aim to include adult A/L/recent school-leaver, vocational and early-career perspectives where feasible, recording actual category coverage without inventing balance. Ask adult eligibility by confirmation, not date of birth or ID; exclude anyone under18. Participation must not affect grades/employment or involve pressure through dependent relationships. Recruitment channel, inclusion details, incentive (if any) and sample size require supervisor/ethics agreement. There is no statistical power or representativeness claim for this target.

Use fictional profiles exclusively. Proposed session35–40minutes: information/consent5; neutral familiarisation3; two comparison tasks12; pathways/skills and accessibility tasks10; questionnaire/debrief5–10. Timing and exclusions are proposals, not measured findings. A separately approved pilot with1–2 adults can check burden; disclose and exclude pilot data from the main descriptive comparison if procedures change. Do not pilot with people before the approval gate.

## Supporting questions and measures

| Question/construct | Tasks and measures | What it can establish |
|---|---|---|
| I integration/suitability | Existing synthetic cases/source validation; user finds appropriate route and source | Technical integration plus bounded task usefulness; independent source/relevance review still required |
| II understanding, trust, transparency | E1–E2 explanation probes; after-condition clarity/transparency/reliance items in MEASURES_ADDENDUM_v2.md | Correct interpretation versus reported confidence; no validated trust scale or causal improvement from agreement alone |
| III planning/routes/gaps | Existing T3–T5, E3–E5; ask participant to state a conditional next step and distinguish unreported from absent skill | Understanding of fictional routes/gaps and perceived planning usefulness, not improved real career outcomes |
| IV accessibility | T6; text fallback; language/device/manual checklist with fluent/native reviewers | Observed barriers and task access in actual tested contexts; no universal accessibility benefit |
| V relevance and usability | Independent ranking judgements; candidate usefulness item; success/help/time/errors and custom questionnaire | Descriptive relevance/usefulness/usability, separate from educational effectiveness |

Keep independent expert-style relevance judging separate from the learner usability sample. Do not treat a useful-looking programme as formal eligibility or an unreported skill as lack of competence.

## Optional comparison: ordinary official-source lookup versus WiseLanka

ConditionA: participant starts from a neutral link sheet containing the relevant official programme/policy pages; uses those pages without WiseLanka, web search or another AI assistant. This is a **bounded source-based lookup baseline**, not a representative benchmark of all normal counselling/search. ConditionB: participant uses WiseLanka with the same official sources available. Both receive the same fictional profile and neutral questions, equal time allowance, browser/device and moderator rules. Freeze the source versions/availability before sessions. If a source is inaccessible, record outage and exclude the paired comparison or reschedule; do not silently give one condition extra summaries.

Use two distinct tasks to reduce answer memorisation: S1=AL_IT/PRG0001 and S2=AL_Engineering/PRG0009 from WP5 scenarios.json. Both concern subject evidence plus unresolved UGC conditions; independent source reviewer must confirm their answer keys and reasonable workload before release. Domain/content difficulty will still differ. COMPARISON_TASKS_v2.md supplies the neutral questions and source links. Do not compare model speed with human task time.

Predeclare four sequences, then shuffle their allocation with seed20261102 after consent, cycling balanced blocks of4:

- Q1: S1 inA → S2 inB.
- Q2: S2 inB → S1 inA.
- Q3: S1 inB → S2 inA.
- Q4: S2 inA → S1 inB.

At target8, each sequence can be used twice; departures/dropout must be reported. Hide the condition sequence until needed. Keep post-task answer corrections until both tasks end. Use a fixed minimal help prompt, record assistance and cap each task at6minutes. Stop without penalty at the cap; retain completion failure and time-limit/censoring rather than deleting slow cases. No full think-aloud during timed comparisons; brief retrospective comments afterwards reduce differing timing interference. Participants cannot be blinded to the interface; moderator/developer allegiance and learning/carryover remain threats.

If ethics/access/time prevents the comparison, execute only the approved WiseLanka task study, label all results descriptive and state that comparative improvement was not tested. Do not manufacture baseline results or rewrite approved questions.

## Analysis and claim boundaries

Predeclare primary exploratory outcomes as correct distinction of NOT_ASSESSED versus failure/acceptance and unassisted task completion. Record comprehension0–2 using the existing rubric, source/next-step accuracy, task time, errors and help. Report per-condition n/N, each participant's paired differences, medians/ranges and missingness. Do not treat repeated tasks as independent participants or interpret an arbitrary summed questionnaire score as validated trust/SUS.

Compare conditions within participants while showing task/sequence and category coverage. A small counterbalanced study can describe observed differences; it does not by itself justify a causal population-wide improvement claim. Stronger causal inference would require adequately justified sample size, allocation, comparable tasks, stable interventions, controlled confounds and analysis agreed before data collection. Do not use a p-value as a substitute for that design. Report neutral/negative findings and uncertainty.

For usefulness/trust/transparency, show item distributions and reasons, N/A counts and mismatches between confidence and correct uncertainty recognition. Greater confidence alongside incorrect admission certainty is overreliance, not success. Explanation probes and observed task performance are distinct from satisfaction. No inference about real enrolment/employment outcomes is possible.

## Data handling and ethics release

Use study IDs; collect only approved category/language/device context and deidentified answers. No real grades, certificate numbers or unnecessary demographics. Consent/contact linkage, if needed for withdrawal, belongs separately in the approved restricted store. **Never put completed forms, ratings with identifiable reviewer details or participant data into Git or AI prompts.** The repository contains blank forms and synthetic material only.

Researcher/supervisor contacts, ethics reference, approved recruitment text, storage/encryption/access, retention/deletion period, withdrawal cutoff and complaint route remain [PENDING APPROVED DOCUMENTS]. Do not invent these policies. No recording is proposed. Native speech is excluded from the standard participant session until vendor audio processing and optional informed consent are specifically approved; typing or labelled mocks remain sufficient for interaction tasks. Any fluent-review/independent-judge human data also requires the applicable approval determination.

Before collection: inspect decision/conditions, obtain approval for changes, complete information/consent addendum, freeze source/task/model snapshots and allocation, approve scoring/analysis, then recruit eligible adults. No participant finding or trust/relevance score exists yet.

## Method sources

The separation of explanation goals is informed by [Tintarev and Masthoff (2012)](https://link.springer.com/article/10.1007/s11257-011-9117-5). The custom measures and sample are project proposals, not validated instruments or thresholds from that paper. Existing full references remain in ../REFERENCES.md.
