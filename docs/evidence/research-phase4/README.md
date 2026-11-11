# Phase 4 — synthetic end-to-end verification record

## Scope

This evidence records software verification using temporary databases and synthetic questionnaire records only. No participant was recruited and no genuine response was collected. `RESEARCH_COLLECTION_ENABLED` remains false by default and is set true only inside the isolated E2E subprocess, where `RESEARCH_DATABASE_PATH` points to a temporary database outside the repository.

## Implemented flow

1. Local researcher CLI creates the study session and expiring one-time invitation before the tasks, after the researcher attests that separately obtained written consent is complete.
2. The researcher uses the session UUID for task observations before questionnaire submission.
3. The participant receives a local-only URL with the token in a URL fragment; the page removes it from browser history and keeps it in memory for POST.
4. FastAPI validates age, instrument, fields, applicability, session consent status, token, expiry, body length and idempotency.
5. SQLite atomically inserts the response and consumes the invitation. Identical retries return the same acknowledgement; altered or second submissions are rejected.
6. The reporting module reads response and session-linked observation tables in read-only mode.

## Evidence and tests

The relevant automated coverage is in:

- `tests/integration/test_research_storage.py`
- `tests/integration/test_research_collection_workflow.py`
- `tests/integration/test_research_admin.py`
- `tests/integration/test_research_reporting.py`
- `frontend/browser_tests/test_research_evaluation_preview.py`
- `frontend/browser_tests/test_research_evaluation_submission.py`
- `frontend/browser_tests/test_research_evaluation_live_e2e.py`

The live E2E exercises the page through local HTTP, Chrome and a separately started FastAPI process, then checks the persisted synthetic response, the shared session ID, prior task observation, and reporting calculations. It checks page width at 390px and 1280px. The mocked browser tests exercise network failure/retry with the same idempotency key. All browser test data is synthetic.

Test counts and run commands are recorded in the completion response for the current work phase; they must be refreshed after any later changes.

## Limitations before participant use

The consent flag is an operator attestation, not a connection to an approved consent register. CORS is a browser policy, not access control. This local workflow does not provide authentication, TLS, encryption at rest, managed backups, retention/deletion automation, a withdrawal portal, or researcher identity auditing. The one-time invite is bearer access. The page is not configured for public hosting. These are activation blockers, not claims that the university has authorized collection.
