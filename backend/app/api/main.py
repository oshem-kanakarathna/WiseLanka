from typing import Dict, Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.eligibility.engine import (
    evaluate_programme,
)

from backend.app.eligibility.explainer import (
    build_explanation,
)

from backend.app.progression.engine import (
    get_progression_pathways,
)

from backend.app.recommendation.engine import (
    recommend_programmes,
)


# ----------------------------------------
# Type definitions
#
# Supports both:
#
# Old flat A/L format:
# {
#     "Combined Mathematics": "A",
#     "Physics": "B",
#     "Chemistry": "C"
# }
#
# New level-aware format:
# {
#     "A_LEVEL": {
#         "Combined Mathematics": "A",
#         "Physics": "B"
#     },
#     "O_LEVEL": {
#         "Mathematics": "A",
#         "English": "B"
#     }
# }
# ----------------------------------------

StudentResults = Dict[
    str,
    Union[
        str,
        Dict[str, str],
    ],
]


# ----------------------------------------
# Create WiseLanka API
# ----------------------------------------

app = FastAPI(
    title="WiseLanka API",
    description=(
        "AI-powered education pathway "
        "intelligence backend for Sri Lanka."
    ),
    version="0.3.0",
)


# ----------------------------------------
# CORS
#
# Allows the development frontend
# running on port 5500 to communicate
# with FastAPI running on port 8000.
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
    """
    Request model for checking one
    programme's eligibility.
    """

    programme_id: str

    student_results: StudentResults


class RecommendationRequest(BaseModel):
    """
    Request model for generating programme
    recommendations.

    student_results accepts both the original
    flat A/L format and the newer level-aware
    nested format.
    """

    student_results: StudentResults


# ----------------------------------------
# API health check
# ----------------------------------------

@app.get("/")
def root():

    return {
        "application": "WiseLanka",
        "status": "running",
        "version": "0.3.0",
        "message": (
            "WiseLanka API is running"
        ),
        "supported_profile_formats": [
            "legacy_flat_a_level",
            "level_aware_nested",
        ],
        "features": [
            "programme_eligibility",
            "programme_recommendations",
            "career_pathway_intelligence",
            "qualification_progression",
        ],
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
        "count":
            len(recommendations),

        "recommendations":
            recommendations,
    }


# ----------------------------------------
# Qualification progression endpoint
#
# Example:
#
# GET /progression/QLF0004
#
# Returns verified immediate academic
# progression pathways from the selected
# qualification.
# ----------------------------------------

@app.get(
    "/progression/{qualification_id}"
)
def get_qualification_progression(
    qualification_id: str,
):

    progression = get_progression_pathways(
        qualification_id
    )

    return progression