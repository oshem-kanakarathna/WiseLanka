# WiseLanka research workflow — Phase 4

## Default state and scope

`RESEARCH_COLLECTION_ENABLED` defaults to `false`. When false or invalid, `POST /research/responses` returns 503 before reading the request body, opening SQLite, or consuming an invitation. The HTML remains a local-only preview when opened without an invitation token; it makes no submission request. No HTTP researcher/admin route exists.

SQLite uses the private per-user application data location unless `RESEARCH_DATABASE_PATH` is explicitly set to an absolute path outside the repository. The directory/file receive owner-only permissions where supported. An explicit path must still be chosen from a private, non-served location. The database is not encrypted. Do not set the switch true or use the local admin tool for real participants until the approved study procedure, ethics conditions, secure hosting and data-handling requirements have been confirmed.

## Local researcher session lifecycle

The researcher runs the local CLI **before the practical tasks**, after the separate written consent process has been completed:

```sh
RESEARCH_COLLECTION_ENABLED=true PYTHONPATH=. python -m backend.app.research.admin create-invitation --consent-verified --expires-minutes 180
```

The operator attestation `--consent-verified` is not an institutional verification service. The command records only a Boolean and timestamp; signatures and consent forms remain in the separately approved process. It creates a random UUID study-session ID and a 256-bit random invitation token, stores only the token's SHA-256 hash, and prints the raw token once as a local URL fragment. The URL is restricted to `localhost`, `127.0.0.1` or `::1`; fragments are not sent in HTTP requests, and the page removes the fragment from browser history after reading it. The expiry is bounded to 5 minutes–24 hours, with a default of 3 hours.

The printed session ID is the researcher’s observation key. Record task observations as the tasks occur:

```sh
RESEARCH_COLLECTION_ENABLED=true PYTHONPATH=. python -m backend.app.research.admin record-observation --session-id SESSION_UUID --task-id 'Task 1 — A/L learner profile' --state UNASSISTED --duration-seconds 75
```

The participant then completes the four tasks and questionnaire from that invitation. The API derives consent from the researcher-created session; the browser cannot assert consent itself. The participant supplies only the adult confirmation and questionnaire fields—no name, email, date of birth, academic results, IP address or account.

## Submission and storage controls

The public endpoint accepts the instrument version, strict 18+ confirmation, device/tasks/route, known answer IDs, an invitation token and a UUID idempotency key. Conditional questions are checked against selected task IDs. Per-answer text is limited to 2,000 characters and the JSON request to 32 KiB. Consent fields in a client body are rejected. Stored answers include only allowlisted values.

The invitation token is hashed at rest, expires, and can be used for one successful submission. An identical retry with the same key and payload returns an idempotent acknowledgement; a changed payload or different key cannot create another response. `BEGIN IMMEDIATE` makes the response insert and invitation consumption atomic. A success response is sent only after SQLite commits. The API does not return participant/session identifiers.

The database contains `research_sessions`, `research_invitations`, `research_responses`, legacy response-linked observations, and `research_session_observations`. The session ID is generated before tasks and is present on the response and pre-task observation rows. No consent signature is stored. The report reader includes both legacy response-linked and new session-linked task observations.

CORS is restricted to the existing local WiseLanka frontend origins (ports 5500/5501). Request bodies and invitation tokens are not logged by application code; the token travels in the URL fragment and POST body, not query strings. Use HTTPS, authenticated/restricted server access and university-approved encrypted storage before any non-local deployment. CORS is not authentication.

## Questionnaire and server contract

Instrument version: `evaluation-prototype-v2-2026-10-31`. Item IDs Q5–Q29 match `frontend/pages/research-evaluation.html`. Q6, Q7, Q14, Q15, Q16, Q17 and Q24 are applicable only when Tasks 1, 3, 2, 2, 4, 4 and 4 were selected respectively. Device and route must be selected for an invited submission; ratings, comprehension answers and written feedback remain optional. Empty text fields are omitted from the request.

With a valid invitation, the page posts JSON to the local FastAPI `/research/responses` endpoint. It has pending, error, retry and server-confirmed success states. It keeps the raw token, answer state and idempotency key in page memory only. Network retry reuses the same key. Without an invitation, the original preview behavior remains: no network call, storage, download, or submission.

Set another backend origin by assigning `window.WISELANKA_API_BASE_URL` before the questionnaire script runs. Production origins are not configured here; no public deployment is part of this phase.

## Synthetic verification

Backend workflow tests use only temporary SQLite databases and synthetic profiles:

```sh
PYTHONPATH=. python -m pytest -q tests/integration/test_research_collection_workflow.py tests/integration/test_research_admin.py
```

Browser-to-FastAPI E2E test (requires the project's FastAPI/uvicorn/Playwright dependencies, installed Google Chrome, and local ports 5500 or 5501):

```sh
PYTHONPATH=. python -m unittest discover -s frontend/browser_tests -p 'test_research_evaluation_live_e2e.py' -v
```

The E2E test explicitly sets the collection switch only in its test subprocess, creates a temporary database/session, submits a clearly synthetic answer set in Chrome at mobile and desktop widths, validates session linkage and report summaries, and terminates its API process. It reuses an already-running frontend only if it serves the questionnaire on an approved localhost port. This is software verification, not participant research. Do not treat its synthetic record as a finding.

## Conditions still required before real collection

- Confirm supervisor/university authorization for this exact session/invitation/API procedure and final questionnaire.
- Confirm how separate signed consent is verified, recorded and kept separate, including retention and withdrawal arrangements.
- Confirm participant information wording, recruitment and debrief/withdrawal procedures against approved ethics conditions.
- Choose a private approved storage/hosting location, HTTPS, encrypted storage/backups, named researcher access, retention/deletion schedule, incident handling and secure export process.
- Verify accessibility, translations and voice support with appropriate manual checks; current automation does not establish those results.
- Ensure the session/invitation CLI is run only by the authorized researcher and raw one-time invitation links are delivered privately.

The collection switch remains false by default. No live data, public dashboard, consent document or participant identity is stored by this implementation.
