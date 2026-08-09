from fastapi import FastAPI
from pydantic import BaseModel

from backend.app.eligibility.engine import evaluate_programme
from backend.app.eligibility.explainer import build_explanation


app = FastAPI(
    title="WiseLanka API",
    version="0.1.0",
)


class EligibilityRequest(BaseModel):
    programme_id: str
    student_results: dict[str, str]


@app.get("/")
def root():
    return {
        "message": "WiseLanka API is running"
    }


@app.post("/eligibility")
def check_eligibility(request: EligibilityRequest):

    result = evaluate_programme(
        request.programme_id,
        request.student_results,
    )

    explanation = build_explanation(result)

    return explanation