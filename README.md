# WiseLanka — Frontend Developer Handoff

WiseLanka is a Sri Lankan education and career pathway prototype. This handoff snapshot contains the FastAPI backend, plain HTML/CSS/JavaScript frontend, curated CSV catalogue and automated tests. The frontend can be redesigned independently while preserving the existing API contracts and policy-aware eligibility engine.

## Requirements

- Python 3.9 or newer
- pip
- A current desktop browser

## Fresh local setup

Run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

The application uses local CSV data in `data/`; no database is required for normal recommendations. Gemini exploration and research response collection are disabled by default. Do not place credentials, private research records, or local databases in the repository.

## Run locally

Terminal 1, from the repository root:

```bash
python -m uvicorn backend.app.api.main:app --host 127.0.0.1 --port 8000
```

Terminal 2, from the repository root:

```bash
python -m http.server 5500 --bind 127.0.0.1
```

Open <http://127.0.0.1:5500/frontend/pages/learner-profile.html>. Other prototype pages are available under `frontend/pages/`. API health and OpenAPI documentation are at <http://127.0.0.1:8000/> and <http://127.0.0.1:8000/docs>.

## Tests

Backend regression suite:

```bash
python -m pytest tests/ -q
```

Frontend browser suite (Playwright synchronous tests):

```bash
python -m unittest discover -s frontend/browser_tests -p "test_*.py" -v
```

Install Playwright Chromium once:

```bash
python -m playwright install chromium
```

The research-preview browser tests select the installed Google Chrome channel, so Google Chrome must also be installed for those tests. The `frontend/browser_tests/live_*.py` scripts require the local backend and static frontend servers to be running. They use fictional/synthetic profiles; do not use them to submit participant data.

## Optional semantic ranking

The checked-in model lock contains model identity and hashes, not model weights. The application has a deterministic/TF–IDF fallback when local ONNX inference is unavailable. To provision the pinned model explicitly, activate the virtual environment and run:

```bash
python -m pip install -r requirements-ai.txt
python scripts/setup_semantic_model.py
```

This optional setup downloads model artifacts from the pinned upstream revision. Model setup is not required to run the application or tests that do not require ONNX inference. Do not commit downloaded model files; `.models/` is ignored.

## Optional Gemini exploration

The Gemini feature is optional and disabled unless explicitly configured. No API key is included in this repository. Keep any developer key in a local, untracked environment variable; never place it in frontend code, a committed file, logs, screenshots or issue reports. The frontend redesign should remain usable with the feature disabled and preserve local eligibility assessments.

## Research preview and collection safeguards

`frontend/pages/research-evaluation.html` is a research questionnaire interface. The collection feature is disabled by default. This repository snapshot contains no participant database or participant responses. The response API and schema are included because the main FastAPI application imports them. Researcher invitation-management and local reporting tools are excluded from this developer handoff. Collection remains disabled by default. Do not activate collection or conduct participant research unless the university's applicable ethics and data-handling conditions have been confirmed. The ordinary application can run without a research database.

## Frontend integration contract

Keep the static frontend architecture unless a redesign decision is agreed. Backend routes and Pydantic request/response models are defined in `backend/app/api/main.py` and domain modules under `backend/app/`. The CSV catalogue under `data/` supplies programme, qualification, requirement, career, skill, scholarship and evidence relationships. Academic eligibility is determined by the local rule engine; ranking relevance must not be presented as admission probability or allowed to override eligibility.
