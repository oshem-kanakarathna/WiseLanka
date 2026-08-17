from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.eligibility.engine import (
    evaluate_programme,
)

from backend.app.eligibility.explainer import (
    build_explanation,
)

from backend.app.recommendation.engine import (
    recommend_programmes,
)


# ----------------------------------------
# Create WiseLanka API
# ----------------------------------------

app = FastAPI(
    title="WiseLanka API",
    description=(
        "AI-powered education pathway "
        "intelligence backend for Sri Lanka."
    ),
    version="0.1.0",
)


# ----------------------------------------
# CORS
# Allows our frontend on port 5500
# to communicate with FastAPI on port 8000
# ----------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ----------------------------------------
# Request models
# ----------------------------------------

class EligibilityRequest(BaseModel):

    programme_id: str

    student_results: dict[str, str]


class RecommendationRequest(BaseModel):

    student_results: dict[str, str]


# ----------------------------------------
# API health check
# ----------------------------------------

@app.get("/")
def root():

    return {
        "application": "WiseLanka",
        "status": "running",
        "message": "WiseLanka API is running",
    }


# ----------------------------------------
# Eligibility endpoint
# ----------------------------------------

@app.post("/eligibility")
def check_eligibility(
    request: EligibilityRequest,
):

    technical_result = evaluate_programme(
        request.programme_id,
        request.student_results,
    )

    explanation = build_explanation(
        technical_result
    )

    return explanation


# ----------------------------------------
# Recommendation endpoint
# ----------------------------------------

@app.post("/recommendations")
def get_recommendations(
    request: RecommendationRequest,
):

    recommendations = recommend_programmes(
        request.student_results
    )

    return {
        "count": len(recommendations),
        "recommendations": recommendations,
    }