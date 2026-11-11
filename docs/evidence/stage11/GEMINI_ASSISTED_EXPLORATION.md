# Stage 11 — Optional Gemini pathway exploration

**Status:** Implemented as an isolated, default-disabled prototype endpoint. No Gemini API request was made during implementation or testing. The route is not connected to the frontend, has not been activated for users, and must not be used for participant research.

## Design and integration

- New `backend/app/gemini_exploration/` package contains request/response validation, source-grounded catalogue construction, Google REST transport and a separate FastAPI route at `POST /gemini/pathway-exploration`.
- `backend/app/api/main.py` only imports and registers this router. Existing recommendation, eligibility and progression endpoints are unchanged.
- `GEMINI_EXPLORATION_ENABLED` must equal `true` to enable the route; absent, blank or other values keep it off. `GEMINI_API_KEY` and an explicit `GEMINI_MODEL` are required only after the feature flag is enabled. No `.env` loading or default model selection is added.
- The REST `generateContent` request uses `generationConfig.responseFormat.text` with `mimeType: APPLICATION_JSON` and a JSON Schema `schema`. It no longer sends deprecated `responseSchema`. `GEMINI_MODEL` remains configurable; Google's current model list includes stable `gemini-3.5-flash-lite`.
- The request accepts the existing typed learner profile, a fixed exploration-domain choice and up to three programme IDs for comparison. Profile validation and academic assessments remain local. The provider prompt receives only the selected domain, compared catalogue IDs and source-backed catalogue records. It does not receive grades, qualification profile, category, free-text interests/career intention, names, contact details, direct identifiers or questionnaire answers.
- The provider can select only catalogue programme identifiers in the structured response. Progression IDs are checked against the CSV graph and must target the selected programme's qualification. Unknown IDs, duplicate candidates, unrelated progression edges and malformed structured output fail closed.
- User-facing programme, requirement, source and progression facts are rendered from the local validated CSV records, not generated prose. An item can be `VERIFIED` only when the programme's official source and all represented requirement evidence meet the source checks. Programmes without represented entry requirements are `PARTIALLY_VERIFIED`, their entry requirements are `NOT_ASSESSED`, and the local academic engine separately returns `MET`, `NOT_MET` or `NOT_ASSESSED` from the supplied profile.
- Results are ordered by locally computed academic status (`MET`, `NOT_ASSESSED`, `NOT_MET`) and only then by Gemini's selection order. Gemini receives no academic outcomes and cannot edit existing recommendations or eligibility. Similarity/exploration is not admission probability or an admission decision.
- Outside-catalogue strings are returned only in a separate `UNVERIFIED` collection with an explicit warning. They are not turned into programme records, links, requirements or authoritative recommendations.

## Limits, operation and privacy

- The active programme and progression catalogue is small; model selection can therefore appear useful without demonstrating external relevance. There are no independent relevance labels and no educational-effectiveness findings.
- Gemini is an external service. When explicitly enabled, a domain choice and curated catalogue evidence (including programme names, documented requirements and source URLs) are transmitted to Google. API key use may incur charges and Google data-handling terms depend on the account/service tier. Before any activation, the student must check current terms, billing, retention/training settings, institutional policy, privacy notices and supervisor/ethics requirements. Official documentation: [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output) and [Gemini API billing](https://ai.google.dev/gemini-api/docs/billing).
- The standard-library REST client sends the key in `x-goog-api-key`, not a URL; limits the call to eight seconds, response body to 64 KiB and generated output to 700 tokens. No prompt, key, provider response or learner profile is logged by this module. Provider errors are returned as generic messages.
- The current API route accepts a learner profile because the canonical eligibility engine needs it, but the Gemini prompt builder deliberately does not serialize or transmit that profile. Synthetic tests verify a sentinel in free-text profile fields is absent from the mocked provider prompt.
- A future frontend must label this as optional exploratory support, show evidence and uncertainty, preserve existing recommendation results and make clear that out-of-catalogue ideas are unverified. No frontend changes were made in this stage.
- This implementation does not establish production security, availability, provider-source freshness, model reliability, accessibility, user trust or recommendation quality. Do not enable it for a live study or general users without the decisions below.

## Test evidence

`tests/integration/test_gemini_pathway_exploration.py` uses synthetic profiles and mocked provider responses only. Its cases cover the disabled default, no provider call while disabled, profile-data exclusion from the prompt, local eligibility preservation and ordering, official source links, missing requirements, unverified ideas, unsupported programme IDs, unrelated progression IDs, invalid JSON, provider failure, unknown comparison IDs, questionnaire-field rejection, the exact outgoing `responseFormat` request, response-envelope parsing, header-only key placement and sanitised transport errors.

Stage 11C ran `/private/tmp/wiselanka-minilm-runtime-venv/bin/python -m pytest tests/integration/test_gemini_pathway_exploration.py -q`: **11 passed**. Full backend regression ran `/private/tmp/wiselanka-minilm-runtime-venv/bin/python -m pytest tests -q`: **280 passed, 0 failed, 0 skipped**. `git diff --check` passed. All provider tests use mocks; they establish local contract and fail-closed behavior, not live Gemini availability, actual model behavior, provider data handling or relevance quality.

## Decisions required before activation

1. Supervisor/student confirmation that an external generative-AI service is appropriate for the project and does not require ethics amendment or participant information changes.
2. Institutional privacy/data-protection review of the catalogue content, domain inputs, Google service terms and account tier; decide whether external transmission is acceptable.
3. Confirm billing/usage limits and select/pin an available Gemini model explicitly. No model is hard-coded because provider model availability changes.
4. Agree how `VERIFIED`, `PARTIALLY_VERIFIED` and `UNVERIFIED` should be presented in a future UI and review the source-check policy.
5. Add an approved, documented deployment secret process, rate limiting/abuse control and monitoring before any non-local exposure.
6. Complete independent relevance and usability evaluation before making claims about benefit or effectiveness.
