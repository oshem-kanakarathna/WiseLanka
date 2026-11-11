# WiseLanka evaluation instrument and relevance-version crosswalk

**Review status: proposal for author/supervisor review, not an approved protocol.** Inspected 6 November 2026. No instrument was edited. There are zero genuine participant responses, and no independent relevance ratings.

## 1. Four-task baseline mapped to later materials

The local two-page `WiseLanka Prototype Evaluation Task Sheet.pdf` is the original four-task sheet identified in the project materials. Its tasks are A/L profile, career pathways, O/L pathway and Foundation qualification progression. Its order and labels match the four task choices in `frontend/pages/research-evaluation.html`. The questionnaire's conditional items are internally aligned to this four-task sequence. The six moderator cards are a later expanded/reordered set. This corrects the earlier methodology-audit inference that the four questionnaire labels were themselves mismatched; the evidence reviewed here places the mismatch between the four-task baseline and later moderator sets.

The crosswalk below treats the four-task sheet as the provisional baseline, not as proof that the ethics panel approved this exact file/version. The original sheet itself has no observer scoring rubric, time limit or explicit completion data schema.

| Original task no. | Moderator card / later scenario | Learner scenario and expected participant action | Observation measure available | Questionnaire mapping | Analysis measure | Status |
|---:|---|---|---|---|---|---|
| 1 | Six-card T2 (partial match: AL_IT); five-task U2 (partial match); comparison task S1 is related but is a different protocol | Baseline A/L profile (Combined Mathematics B, Physics C, Chemistry C); generate pathways; inspect recommendation, eligibility and entry explanations. Later AL_IT adds a stated IT goal and explicit unresolved UGC/selection checks. | Original sheet: no defined observation fields. Later cards propose success/help/time/errors; only use if B4 and procedure are authorised. | Task selector Task 1; Q6. General Q10–Q13, Q18–Q19, Q20–Q23 can apply. | Descriptive task success/assistance/time only if approved; Q6 rating; separate uncertainty/comprehension item counts. | Core baseline; later AL_IT specificity is optional expansion unless the baseline source values are confirmed identical. |
| 2 | Six-card T5 (partial match but expands to skills/scholarship/chatbot); no exact five-task counterpart; comparison S1/S2 not the career task | From Task 1 recommendation, locate careers, relevance labels and available demand/remote-work information; consider understandability and usefulness. | Original sheet: no defined observation fields. Later rubric's career/skill success is broader than this task. | Task selector Task 2; Q14–Q15. Q19 and Q25–Q29 may capture general perceptions/comments. | Descriptive completion if authorised; Q14/Q15 item distributions and comments. Participant perception is not independent relevance. | Core baseline. Chatbot/skills/scholarships are not implied by the original Task 2. |
| 3 | Six-card T1 (partial match: OL6/foundation); no direct same-number mapping in later five-task sequence (U1); comparison tasks are unrelated | Baseline O/L profile (Mathematics A, English A, Science A, ICT A, Sinhala A, History A); generate pathways; inspect Foundation route and represented eligibility/source. | Original sheet: no defined observer fields. Later OL6 card adds explicit MET/no-guarantee endpoint; verify frozen values match before reuse. | Task selector Task 3; Q7. General Q10–Q13, Q18–Q19, Q20–Q23 can apply. | Descriptive task outcome if authorised; Q7 and separate comprehension counts. | Core baseline. Reuse of six-card T1 requires input and source equivalence check; card order differs. |
| 4 | Six-card T4 (not equivalent: NVQ6/UoVT Mechatronics); five-task U4 (same broad vocational theme, not same route); comparison S1/S2 not equivalent | Continue from Task 3 Foundation recommendation; locate progression information; distinguish direct from conditional steps and inspect additional conditions/next steps. | Original sheet: no observer rubric. Later T4 asks qualification/provider checks for a different vocational route. | Task selector Task 4; Q16–Q17 and Q24. Q20–Q23 general items also apply. | Descriptive completion if approved; Q16/Q17 ratings, Q24 text and relevant comprehension answers separately. | Core baseline. NVQ conditional progression is an expansion, not a replacement for Foundation progression. |

### Six-card expansion mapping

| Later card | Content | Relationship to original four tasks | Recommendation |
|---|---|---|---|
| T1 | O/L Foundation, official source, represented MET/no-guarantee | Partially maps to original Task 3, but appears first and uses OL6 scenario. Confirm exact grade/source equivalence. | Do not renumber the core; adapt only after values and ethics version are checked. |
| T2 | A/L IT; subject evidence vs unresolved UGC selection; relevance vs eligibility | Partially maps to original Task 1; adds IT interest and a specific uncertainty/comprehension criterion. | Candidate extension; preserve Task 1 label if formally selected. |
| T3 | Business or failed Engineering; distinguish NOT_MET vs NOT_ASSESSED | No direct counterpart in the four-task sheet. | Optional additional scenario requiring instrument/ethics review. |
| T4 | NVQ6 to UoVT Mechatronics conditional route | Not the original Foundation qualification progression in Task 4. | Optional alternative pathway task; do not substitute silently. |
| T5 | Careers, skills, scholarships, chatbot; distinguish self-report/competence and current scholarship status | Overlaps original Task 2 career exploration but adds FR5/FR7/FR8 domains. | Keep extra components out of baseline unless authorised. |
| T6 | English/Sinhala/Tamil switching, keyboard, guided support, optional voice | No original task counterpart; tests Objective VI in human use. | Separate accessibility/language/voice study or explicit approved extension. |

### Other task version

`docs/evidence/research-sprint2/evaluation-readiness/USABILITY_TASKS.md` is a later **five-task** proposal (U1 O/L, U2 A/L IT, U3 Engineering gap, U4 NVQ6, U5 skills/chatbot), proposed English/typing, 25–35 minutes. It explicitly excludes a comparison condition and says no sessions were executed. It is not the same as either the four-task sheet or six-card sequence. `MODERATOR_RUBRIC.md` uses U1–U5 and C1–C5; the six-card `TASKS_AND_EXPLANATION_RUBRIC.md` instead uses T1–T6 and E1–E5. Do not mix U and T identifiers, score anchors or task denominators.

## 2. Questionnaire mapping and conditional logic

Source: `frontend/pages/research-evaluation.html`, current questionnaire v2 context, dated 2026-10-31. It asks which of four named tasks were attempted, then contains Q5–Q29. The current conditional mapping is:

| Question ID | Type / construct in source | Applicability | Crosswalk finding |
|---|---|---|---|
| Q5 | Likert, navigation | General | No task condition. |
| Q6 | Likert, entering A/L results | Task 1 | Correctly aligns with four-task baseline Task 1. |
| Q7 | Likert, entering O/L results | Task 3 | Correctly aligns with four-task baseline Task 3. |
| Q8–Q9 | Likert, readability/device and recommendation presentation | General | Perception only; no automated accessibility claim. |
| Q10–Q13 | Likert, recommendation rationale, assessment distinctions, missing information, entry explanations | General | Clarity/perceived understanding ratings; not proof of correct comprehension. |
| Q14–Q15 | Likert, career pathway discovery and programme relationship | Task 2 | Correctly aligns with four-task baseline Task 2. |
| Q16–Q17 | Likert, next qualification steps/direct vs conditional progression | Task 4 | Correctly aligns in topic; source wording says “for the O/L learner,” matching Foundation path. |
| Q18–Q19 | Likert, no admission guarantee and usefulness as starting point | General | Q19 is perceived usefulness, not trust or actual educational benefit. |
| Q20–Q23 | Fixed-choice, MET nuance, missing evidence, conditional progression, official verification | General | Comprehension probes; any answer key/scoring must be frozen and independently checked. They are not a validated instrument. |
| Q24 | Optional text, additional progression requirement | Task 4 | Conditional as expected; applicable denominator is Task 4 respondents, with skipped/blank distinct from no requirement. |
| Q25–Q29 | Optional open responses, usefulness, difficulty, accessibility, improvement, other comments | General | Qualitative text. B5 ethics conflict must be resolved before treating omissions as permitted. |

Context includes age eligibility, device category, attempted tasks and pathway. Task selection is participant-reported attempt, not completion. The questionnaire is custom and not SUS. The preview/collection backend is not evidence that a human study is authorised.

## 3. Observation and explanation rubrics

| Instrument | Version/content | Measures | Alignment and disposition |
|---|---|---|---|
| Original four-task PDF | Existing two-page sheet; the four steps above, followed by questionnaire | Instructions and what to inspect; no explicit observer record, success criteria, timing, assistance, errors, scoring or exclusions found in the reviewed text | Retain as provisional task baseline pending confirmation against ethics attachments. Do not retroactively claim it measured task success or time. |
| `TASKS_AND_EXPLANATION_RUBRIC.md` | Six cards T1–T6 plus E1–E5, 0–2 comprehension rubric | Outcomes for O/L, A/L, unmet Engineering, vocational NVQ, skills/scholarship, multilingual/accessibility | Proposed and broader than baseline. Its success note uses “1” for both unassisted and assisted in separate outcomes; if retained, preserve separate categorical completion state and assistance flag rather than treating a single score as unambiguous. E3–E5 are expansion topics. |
| `docs/evidence/research-sprint2/evaluation-readiness/MODERATOR_RUBRIC.md` | Five U tasks and C1–C5, 0–2 custom comprehension probes | NOT_ASSESSED, relevance vs eligibility, Engineering gap, conditional vocational route, unreported skills | Another proposed instrument version. U1–U5 do not correspond one-to-one with original tasks. Keep its states (unassisted/assisted/not completed/skipped/technical failure/withdrawn) distinct if approved. |
| `templates/TASK_OBSERVATIONS_BLANK.csv` and moderator observation forms | Prepared blank templates | Task outcome, timing/assistance/error notes (field set depends on file version) | Preparation only. Ethics B4 marks observation N/A; do not fill with human observations before written resolution. |

Comprehension ratings are researcher-coded responses, not directly validated knowledge tests. If use is approved, define response anchors per exact four-task outcomes, keep raw deidentified answer and initial score, and identify who scored it. If only the implementer scores, disclose the conflict and avoid implying independent scoring.

## 4. Relevance-evaluation pack comparison

| Pack/version | Scenario set and candidate pool | Scale / blinding | Judges and disagreement | Metrics / completeness | Assessment |
|---|---|---|---|---|---|
| Older project pack: `docs/final-submission/research-evaluation/independent-ranking/` | 9 development-exposed scenarios; 51 unique scenario–programme pairs; A/B are randomized permutations of the same 51 pairs. Manifest seeds 20261103/20261104. | 0 unrelated, 1 weak, 2 moderate, 3 strong; `UNJUDGEABLE`. Method/rank/score withheld; cards expose more scenario context and programme identity. | Two independent adult judges proposed. Initial ratings preserved; per-judge results and disagreement; no ordinal averaging. | nDCG@3 for groups n≥3, @2 for n=2, singleton excluded; missing/UNJUDGEABLE and zero ideal gain unavailable. Manifest says 0 judgements, labels unavailable, nDCG not computed. | Internally reproducible but superseded as prospective choice by the larger revised pack. Scenarios all developer-exposed; not held out. |
| Sprint 2B generic blank export: `docs/evidence/research-sprint2/ai-ranking/BLANK_RELEVANCE_REVIEW.csv` and `ai-ranking/blinded-review/` | 21 scenarios, 127 unique pairs in current files: 9 development-exposed + 12 evaluator-authored, catalogue-aware follow-ups. A/B cards describe the same pair pool in different order. | Current instructions use 0–3 plus `UNJUDGEABLE`, with method/order blinding; `BLANK_RELEVANCE_REVIEW.csv` is a single generic 127-row export and does not carry the same pack-specific/reviewer identity fields. | Two qualified independent adult judges proposed; no responses. | Newer analysis rules use status-grouped metrics and exclude D01/D08; no labels or metrics. | Do not issue this generic export in parallel with the pack-specific readiness forms. Retain as a legacy artifact. |
| Revised readiness pack: `docs/evidence/research-sprint2/evaluation-readiness/relevance-review/A|B/` | 21 scenarios and 127 unique scenario–programme pairs; same pool in separate A/B permutations; 11 programmes, imbalanced occurrence. Max 117 pairs / 19 interpretable scenarios after predeclared D01/D08 exclusion, before other exclusions. | 0 unrelated, 1 broad/indirect, 2 clear/partial, 3 strong/direct; `UNJUDGEABLE`; skipped is blank. Cards use interest and frozen programme text, omit method/rank/score and full learner profile; public programme names remain visible. | Two independent adults with relevant familiarity and no implementation/tuning role proposed. Preserve separate grades, skip/UNJUDGEABLE and 4×4 disagreements; no ordinal average. | Status-grouped nDCG@3 for n≥3; nDCG@2 for n=2; singleton omitted; require complete numeric group and nonzero IDCG; same complete-case groups across methods; exclude D01/D08. Ready as blank materials only; no judgements. | **Recommended sole candidate** for future review, subject to ethics/supervisor approval and hash/version freeze. It adds independent labels, not independent scenario construction. |

The revised pack's identities combine pack, case and candidate; never join on a case/candidate code alone across A/B. It is method/order-blinded, not institution-anonymous. Proposed reviewer burden is 127 cards each (estimated 45–75 minutes in blocks; not piloted). Candidate descriptions are frozen short catalogue text, so reviewers assess text-fit, not complete curriculum suitability or provider accuracy.

### One recommended relevance protocol

1. Seek written ethics/supervisor determination for the separate judge activity, eligibility and recruitment route; do not contact judges beforehand as research participants.
2. Freeze revised readiness pack A/B, instructions, exact dataset/model/comparator outputs, analysis specification and hashes. Keep the researcher key and method outputs inaccessible to judges until ratings lock.
3. Use two independent, adult, non-implementer/non-tuner judges with relevant programme/career familiarity if approved; document broad expertise and conflicts under approved minimal-data handling. If fewer judges participate, report the limitation and do not claim inter-rater evidence.
4. Each judge independently rates all assigned pairs from the fixed cards on 0–3 content fit or `UNJUDGEABLE`; blanks remain skipped. No discussion before lock; preserve original judgements and any later adjudication separately.
5. Validate coverage, duplicate keys, pair IDs, permissible grades and versions before unblinding. Report judge-level rating distributions, exact agreement and the 4×4 disagreement table where both gave numeric ratings; report missing/UNJUDGEABLE separately.
6. Compute only prespecified within-status-group nDCG for fully judged, nonzero-ideal groups, same candidate cases across all methods. Report @3, @2, singleton and excluded counts separately. Keep development-exposed and catalogue-aware follow-up results separate; do not call the latter held-out. No precision/accuracy/superiority claim is supported by labels alone without the corresponding design and uncertainty limits.

## 5. Measure reconciliation

| Measure | Source/instrument state | Reconciliation |
|---|---|---|
| Task success | Later five/six task rubrics; absent from original four-task sheet | Requires a four-task-specific success definition and B4 clearance. Report assisted separately from unassisted. |
| Completion time | Later PIS, v2 comparison plan and addendum | No baseline time limit found; proposed limits differ (six minutes in v2 comparison vs five-minute soft limit in five-task readiness). Do not apply either to baseline until approved. B4 clearance needed. |
| Assistance/errors | Later cards and v2 forms | Define standard neutral help and error taxonomy; B4 clearance needed; do not equate assistance with failure. |
| Explanation comprehension | Current Q20–Q23; newer E1–E5 and C1–C5 | Use one version only. Map approved probes to four-task outcomes; Q20–Q23 are the questionnaire's fixed-choice items. Additional verbal probes change burden/procedure and require approval. |
| Clarity/usefulness ratings | Questionnaire Q5–Q19; separate Q1–Q9 readiness questionnaire; v2 U1–C1 per condition | Do not merge versions. The questionnaire Q19 is perceived usefulness. Addendum T1/T2 are bounded reliance/verification-intention items, not validated trust. |
| Qualitative feedback | Questionnaire Q25–Q29; other packs O1–O5 | Different question sets; use one approved version. B5 conflict about omission must be resolved. Deidentify; no claims before responses. |
| Recommendation relevance | 0–3 independent judge rating packs | Separate construct, evaluator population and protocol. No current labels. It cannot substitute for usability or participant relevance perception. |
| Accessibility/language/voice | Objective VI; six-card T6; manual checklists/mock tests | Automated evidence is not human validation. Any participant language, screen-reader, mobile or native-voice activity is an expansion unless explicit clearance confirms it. |

## 6. Ethics and consent reconciliation

Source: `docs/evidence/research-sprint2/evaluation-readiness/ETHICS_ALIGNMENT.md`, which records inspection of the local ethics form, proposal, separate consent form and submission receipt, while explicitly stating the final clearance decision/conditions and approved information sheet were not found. It is not an approval determination.

| Ethics record | Proposed/current documents | Result / decision needed |
|---|---|---|
| Proposal: functional/scenario testing, usability feedback, simple rating and open questions; no under-18 participants or sensitive details | Four-task baseline and fictional inputs are consistent in principle | Confirm exact instruments and procedure covered. Use fictional profile inputs only. |
| Ethics outline: adults 18+, voluntary, low-risk clarity/usefulness/explanation feedback, written consent/withdrawal/confidentiality | Draft PIS and task studies | Broad alignment, but exact release version and signed decision must be checked. |
| B4: observation marked N/A | Later task outcomes, time, assistance and errors | Not demonstrably covered; written confirmation/amendment required before observer records. |
| B5: optional question omission marked NO | Questionnaire and PIS permit skipping | Direct inconsistency. Obtain determination; do not force responses or silently reinterpret. |
| B6: confidentiality N/A; outline references confidential/anonymised data | Coded session ID, linked observations, private storage | Clarify whether data are anonymous or pseudonymous while linkable; approve storage, access, retention, withdrawal and reporting. |
| B7: debrief NO | Later drafts include debrief/withdrawal instructions | Confirm whether to amend/approve debrief wording and process. |
| Form refers to speech-to-text/optional NLP | Current core proposal excludes voice; T6 makes it optional | Confirm exclusion and any audio processing scope. Do not collect/process speech absent explicit approval. |
| No located approval for independent judges or source-lookup comparison | 127-pair judge pack, two-condition comparison proposal | Treat both as scope changes until written supervisor/ethics determination; do not recruit. |
| Recruitment/sample, language, burden, storage/retention/contact fields pending | Drafts propose 6–10, 8, or six-to-eight adults, and conflicting session durations | Do not select a number or promise duration without authority. Complete fields only from verified university instructions. |

Receipt is evidence of submission only. The database collection switch must remain disabled; no route is to be connected or enabled as part of this reconciliation.

## 7. UWL assessment guide check

Official PDF found at `/Users/dan/Documents/UWL/FP/MATERIALS/MSG CP60046E Project AY202526 - FEB-26 - JAN-27.pdf`. Python availability check found none of `pypdf`, `PyPDF2`, `fitz`/PyMuPDF or `pdfplumber`; the earlier `pdftotext` check also found no executable. Per instruction, no software was installed. Therefore **no assessment criterion from the PDF was newly verified in this pass**. Existing rubric transcription elsewhere in project documentation remains to be confirmed against the official guide.

## 8. Minimum correction set before a supervised synthetic dry run

No participant study is authorised by this review. Before a supervised walk-through using only fictional inputs and no database records:

1. Supervisor selects and documents the four-task sheet as the rehearsal sequence, confirms task input/source versions and resolves the six-/five-task variants as excluded from this rehearsal.
2. Prepare a task-to-question map from the four-task table above; check that Task 1/2/3/4 labels are preserved and no task-conditioned question is asked after an unattempted task. Do not edit the questionnaire under this review's scope.
3. Write a four-task observation worksheet only if the purpose is to rehearse observer coding; mark it synthetic/rehearsal only and exclude it from research data. Otherwise do not record task success/time/help/errors.
4. Confirm the dry run is purely an internal software walk-through, not human-participant piloting. Use synthetic profiles; do not create database records, invite/consent volunteers or submit responses.
5. Keep the revised 127-pair judge pack as a separate unfilled candidate. Do not generate scores or run nDCG.

## 9. Source inventory reviewed

- `docs/final-submission/research-documentation/METHODOLOGY_CRITICAL_AUDIT.md`
- `docs/final-submission/research-documentation/RESEARCH_EVIDENCE_STATUS_MATRIX.md`
- `docs/final-submission/research-evaluation/EVALUATION_PLAN_v2.md`
- `docs/final-submission/research-evaluation/COMPARISON_TASKS_v2.md`
- `docs/final-submission/research-evaluation/MEASURES_ADDENDUM_v2.md`
- `docs/final-submission/research-evaluation/PARTICIPANT_INFORMATION_AND_CONSENT.md`
- `/Users/dan/Documents/UWL/FP/WiseLanka Prototype Evaluation Task Sheet.pdf`
- `docs/final-submission/research-evaluation/TASKS_AND_EXPLANATION_RUBRIC.md`
- `docs/evidence/research-sprint2/evaluation-readiness/USABILITY_TASKS.md`, `MODERATOR_RUBRIC.md`, `QUESTIONNAIRE.md`, `TASK_INPUT_CARDS.md`
- `frontend/pages/research-evaluation.html`
- `docs/final-submission/research-evaluation/RELEVANCE_PROTOCOL.md`
- `docs/final-submission/research-evaluation/independent-ranking/PROTOCOL.md`, `preparation-manifest.json`, blank forms/cards
- `docs/evidence/research-sprint2/ai-ranking/EXPERIMENT_PROTOCOL.md`, `blinded-review/REVIEW_PROTOCOL.md`, generic blank export
- `docs/evidence/research-sprint2/evaluation-readiness/RELEVANCE_PACK_AUDIT.md`, `RELEVANCE_REVIEW_INSTRUCTIONS.md`, `ANALYSIS_SPECIFICATION.md`, `ETHICS_ALIGNMENT.md`, revised A/B cards and blank forms

This inventory describes what was read for this proposal; it does not imply that the actual ethics decision was available or that any human evaluation was conducted.
