
# WiseLanka

**An Explainable, Rule-Based Education and Career Pathway Intelligence System for Sri Lankan Learners**

WiseLanka is a final-year academic software project designed to help Sri Lankan learners explore educational programmes, academic eligibility, career relationships, and possible qualification progression pathways.

The system uses curated educational data and explicit rules to generate explainable guidance. Its current recommendation implementation is rule-based, not a trained machine-learning model.

## Features

- Academic programme eligibility assessment
- Programme recommendations based on academic qualifications
- Learner personalisation using interests, career goals, and preferences
- Academic qualification progression pathways
- Alternative education pathways
- Programme-to-career relationships
- Skills alignment information
- Scholarship eligibility guidance
- Human-readable explanations for assessment results

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Data validation | Pydantic |
| Application server | Uvicorn |
| Structured data | CSV files |
| Backend testing | pytest, HTTPX |
| Frontend testing | Playwright, unittest |
| Version control | Git and GitHub |

## Project Structure

```text
WiseLanka/
├── backend/
│   └── app/
│       ├── api/
│       ├── eligibility/
│       ├── recommendation/
│       ├── personalisation/
│       ├── progression/
│       ├── alternative_pathways/
│       ├── scholarships/
│       └── skills/
├── frontend/
│   ├── pages/
│   ├── components/
│   └── browser_tests/
├── data/
│   ├── master/
│   └── relationships/
├── knowledge_base/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── requirements.txt
└── requirements-dev.txt
```

Other project directories include assets, configuration, diagrams, reports, notebooks, and model-related folders. The presence of model-related folders does not imply a trained ML model is currently used.

## Installation

### Requirements

- Python 3.9 or a compatible version
- pip
- A modern web browser

Run the following commands from the repository root.

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install application and testing dependencies

```bash
python -m pip install -r requirements-dev.txt
```

### 4. Install the Playwright Chromium browser

```bash
python -m playwright install chromium
```

## Running WiseLanka

The frontend and backend run as separate local services.

### Start the FastAPI backend

From the repository root:

```bash
python -m uvicorn backend.app.api.main:app --host 127.0.0.1 --port 8000
```

### Start the frontend

Open a second Terminal in the repository root:

```bash
python -m http.server 5500 --bind 127.0.0.1
```

### Open the website

Visit:

http://127.0.0.1:5500/

The landing page is the default entry point. **Find my pathway** and the
**Pathways** navigation link open the pathway overview, where users can choose
the learner profile, personalised recommendations, or guided assistant.
The educational journey cards open the corresponding learner profile directly.
All learner-facing pages share the landing page's navigation, Montserrat
typography, and monochrome theme.

The current frontend uses the shared styles in `frontend/styles/` and the
page scripts in `frontend/components/`. Earlier landing and experience themes
have been removed. The active profile, eligibility, recommendation, scholarship
and guided-assistant scripts provide the current pages' backend connections.

The backend health endpoint is available at:

http://127.0.0.1:8000/

The API's interactive documentation is available at:

http://127.0.0.1:8000/docs

## Running Automated Tests

### Backend unit and integration tests

```bash
python -m pytest tests/ -v
```

### Frontend automated tests

```bash
python -m unittest discover -s frontend/browser_tests -p "test_*.py" -v
```

### Live browser-to-backend integration test

Start the frontend and backend servers before running:

```bash
python frontend/browser_tests/live_integration_check.py
```

This test submits a fictional learner profile to the real API and compares returned recommendations and progression information with the rendered browser interface.

## Verified Test Results

The following results were observed during development:

| Test | Result |
|---|---|
| Backend unit and integration suite | 92 passed |
| Frontend automated suite | 9 passed |
| Live browser integration | Passed |
| Fresh-environment backend startup | Passed |
| Fresh-environment recommendation API test | Passed |

These results describe the tested implementation and scenarios; they do not establish exhaustive correctness across every possible learner profile.

## Methodology and Explainability

WiseLanka's currently implemented recommendation functionality evaluates learner profiles against documented, structured academic requirements.

The system can report:

- Whether recorded academic requirements were satisfied
- Which requirements passed or failed
- Academic matching information
- Career and interest assessment information where supporting evidence exists
- Related academic progression pathways and conditions

Missing information should not automatically be interpreted as a negative assessment.

## Important Limitations

WiseLanka is an educational guidance system, not an official university admissions service.

- Recommendations depend on the accuracy and coverage of curated data.
- Programme requirements and scholarship conditions may change.
- Academic matching scores are not probabilities of admission.
- Academic progression pathways are not guaranteed admissions.
- Missing relationships or evidence do not necessarily indicate unsuitability.
- Learners should independently confirm requirements with the relevant institutions.

## Academic Project

WiseLanka is being developed as a University of Westminster final-year software project, with an emphasis on explainable recommendation logic, modular architecture, automated testing, and reproducibility.
