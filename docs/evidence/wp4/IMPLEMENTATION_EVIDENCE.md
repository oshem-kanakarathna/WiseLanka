# WP4 — guided support, trilingual core interface and optional voice input

Date: 2026-10-29. Accepted WP3 was selectively checkpointed as `3cfc2b1`.
WP4 is uncommitted. No push, WP5/WP6 work, paid API, database or new dependency.

## Delivered architecture

A reusable `guided-assistant.js` component is integrated into the existing learner
profile page. `GET /assistant/options` supplies active programme IDs/titles.
`POST /assistant/guidance` accepts a bounded intent, optional programme ID, optional
question (300 characters), `en/si/ta` language and optional typed current profile.
The profile is sent only when the user selects the explicit checkbox. There is no
conversation history, profile persistence or audio endpoint.

The deterministic assistant reuses eligibility, progression, alternatives, skills,
career relationship and scholarship engines and the current CSV catalogue. It
never calls a generative model or edits rules, profiles or semantic relevance.
Source facts and detailed engine explanations are rendered as original-language
content with appropriate official links. Unknown evidence and provider decisions
are preserved; programme/admission/competence guarantees are not generated.

Supported intents:

| Intent | Behaviour |
|---|---|
| programme | Recorded programme title, subject, type, context and official link |
| eligibility | Canonical MET/NOT_MET/NOT_ASSESSED groups, gaps, next steps and sources |
| progression | Recorded qualification progression, conditions and source links |
| alternatives | Existing alternative-pathway assessment; no guaranteed admission |
| skills_topic | Self-reported versus development/unreported skills; no competence test |
| careers | Curated programme-career links with an explicit per-relationship citation limitation |
| scholarships | Recorded opportunity/status/dates, official link and unresolved personal eligibility |
| help | Guided list of supported topics |

Natural-language coverage is deliberately narrow. The optional text/transcript
recogniser accepts exact supported topic labels in the three interface languages
and a small set of English aliases. It does not claim general language
understanding. Arbitrary, ambiguous or instruction-injection questions return
UNSUPPORTED with no invented answer. Users can always choose a topic instead.
Unknown programme IDs request a valid selection. Missing profiles request input;
missing relationships are unassessed, not negative conclusions. Scholarship
availability is separate from eligibility; the recorded opportunity remains Closed.
Current-profile exam data does not establish citizenship/age/reference-year rules.

## Translation design and actual coverage

`data/localisation/ui.json` is the central catalogue, shared by backend summaries
and frontend translation. It contains **135 keys in each of English, Sinhala and
Tamil**, with automated nonblank/key-parity checks. No duplicated page versions or
new frontend framework were introduced.

The visible language selector covers the core learner-profile journey: primary
navigation, hero, major input labels/options, subject-row labels, common validation
messages, assessment statuses, recommendation/relevance headings, assistant
controls/messages and voice notices/states. Canonical IDs and input values do not
change when displayed text changes. Existing results are translated in place;
rendered content and learner inputs survive switching. HTML language and Unicode
font fallbacks are updated. Source titles/details and English-only semantic inputs
are explicitly identified, not silently translated.

Translations are implementation-authored draft strings, **not linguistically or
academically validated translations**. Fluent Sinhala/Tamil review remains pending,
including terminology and comprehension. Key presence does not establish accuracy.
Not every help paragraph or technical engine string is translated. Separate legacy
eligibility/recommendation/scholarship pages remain English; trilingual coverage is
the integrated core profile/results/assistant journey. Source facts remain English
unless an original source provides otherwise. MiniLM remains English-only.

The translator retains original text nodes and uses central keys/exact English
label matching plus templates for dynamic subject/award controls. Missing catalogue
or missing keys disables switching and retains English with an explicit error.
This is intentionally small, but label changes require catalogue/test maintenance.
No language or profile state is persisted by this component.

## Voice implementation and privacy

Optional browser `SpeechRecognition`/`webkitSpeechRecognition` is used only after
explicit opt-in and a microphone-button click. It is single-utterance input to the
assistant question field. A transcript is editable and never auto-submitted.
Stop, error, denial, no-speech, unavailable language, audio-capture and network
states are handled. Language change/consent withdrawal stop active listening.
Results after listening stops or consent is withdrawn are ignored. No MediaRecorder,
audio storage, audio upload endpoint or synthesis service was added.

The UI warns that browser recognition may send audio to a browser-provider service;
no offline/local-only recognition claim is made. Text and topic-selection paths
remain functional when recognition is unavailable. Requested `en-LK`, `si-LK`,
`ta-LK` language codes are not proof of installed/provider language support.

Sources consulted for API design/limitations:
- https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition
- https://webaudio.github.io/web-speech-api/

`voice-capability.json` records that both constructor names were exposed in the
headless Chromium environment and localhost was a secure context. **No real
microphone, native transcript accuracy or Sinhala/Tamil recognition was tested.**
Error/consent/listening/transcript handling was tested with explicitly mocked
recognition objects. `voice-mocked-*` screenshots demonstrate mocks, not native
speech success. `voice-controls.png` shows actual browser UI capability controls.

Manual verification still required: record browser/OS/version; try explicit consent,
permission denial, start/stop and an English supported-topic transcript; edit it
before submission; then separately attempt Sinhala/Tamil and record actual support
or language errors. Do not mark successful transcription without observing it.
No participant feedback has been collected in this package.

## Actual final verification

| Check | Actual result |
|---|---|
| Complete backend suite | **200 passed** (177 prior + 23 new) |
| Complete browser suite | **36 passed** (25 prior + 11 new) |
| CSV integrity | Passed |
| Original live integration | Passed |
| WP1 live workflow | Passed |
| WP2 live workflow | Passed |
| WP3 real-model live workflow | Passed |
| New WP4 live workflow | Passed in English, Sinhala and Tamil |

Final commands, timestamps and exit codes are recorded in `verification.json`.
All checks returned exit code zero. Live tests used the AI-enabled API on 8011 and
the existing static frontend on 5500. Regression screenshot destinations were
redirected below WP4; prior evidence was not overwritten. No dependency installation
or Python environment change was needed beyond the accepted WP3 setup.

Backend cases include grounded facts, missing profiles/programmes, academic failure
versus unknown, conditional routes, missing careers, self-report semantics, closed
scholarship guidance, unsupported questions, language contracts and unchanged
profile/ranking. Browser cases include switching with preserved results/input,
localised validation/dynamic labels, missing-key fallback, keyboard submission,
390px reflow, unsupported recognition, opt-in, permission refusal, editable transcript,
no automatic submission, language/network/no-speech failures and error state after
an earlier successful answer. The real WP4 workflow compares complete before/after
recommendation responses and asserts unchanged scores/academic decisions.

During development, a test fixture had an invalid JavaScript object literal and a
backend contract test passed a duplicate Python argument; both tests were corrected.
Final UI review also found that translation updates could replace a new assistant
error with a prior success state. That defect was fixed and regression-tested.
These attempts are not counted as passing verification runs.

## Evidence and traceability

- `assistant-en.png`, `assistant-si.png`, `assistant-ta.png`: real API responses,
  translated headings/controls and visibly original English rule content.
- `language-*.png`: language selector and draft/source-language disclaimer.
- `voice-controls.png`: actual exposed browser controls, not native recognition.
- `voice-mocked-listening.png`, `voice-mocked-denied.png`: mocked event states.
- Test/live logs, voice capability record and verification/source hashes accompany
  this report. `translation-coverage.json` records key parity and verification limits.

| Approved requirement | WP4 contribution / status |
|---|---|
| Objective VI | Core mobile/trilingual/optional voice implementation delivered; linguistic, native speech and full accessibility validation remain PARTIAL |
| FR8 | IMPLEMENTED as a bounded deterministic, knowledge-grounded assistant |
| FR9 | Basic optional voice-input handling IMPLEMENTED; native recognition/language accuracy UNVERIFIED |
| Objectives III/V and FR3–FR7 | Existing structured knowledge, decisions, explanations and official links reused and preserved |
| Objective IV | Frozen semantic ranking preserved; chatbot is not labelled generative AI |
| Objective VII | Functional/scenario evidence expanded; user satisfaction, comprehension and effectiveness remain UNVERIFIED |

## Files, setup and acceptance limitations

Changed: `backend/app/api/main.py`, `frontend/pages/learner-profile.html`,
`frontend/components/learner-profile.css`.
Added: `backend/app/assistant/{__init__,engine}.py`, `data/localisation/ui.json`,
`frontend/components/{i18n,guided-assistant}.js`, backend/browser WP4 tests, live WP4
check, and this evidence directory. The approved CSV rules, semantic model/ranker,
previous evidence, README and two JavaScript backups remain unchanged.

Use the existing application startup commands; there are no WP4 dependencies.
Serve the frontend over localhost HTTP (or HTTPS), not file://, so its translation
JSON can load normally. The model remains optional with WP3's explicit fallback.
All app/assistant processing is local except browser-provider speech processing
where the user elects it. API errors and text alternatives do not require speech.

Technical verification is complete with no failing final check. WP4 is ready for
prototype acceptance **with the explicit fluent-translation and native-speech
validation limitations above**. No WCAG conformance, usability satisfaction or
translation-quality result is claimed. Inherited educational sources were reused,
not independently reverified in WP4. Curated career/skill relationships still lack
individual citations and are disclosed as such.

Immediate WP5 work (not started): expand cross-browser/screen-reader/manual speech
checks; obtain fluent language review; exercise end-to-end learner scenarios and
failure recovery; measure full-browser/network performance; prepare ethics-compliant
adult-only usability and explanation-comprehension evaluation.
