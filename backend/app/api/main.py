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

from backend.app.alternative_pathways.engine import (
    find_alternative_pathways,
)

from backend.app.skills.engine import (
    get_skill_alignment,
)


# ----------------------------------------
# Type definitions
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
    version="0.4.0",
)


# ----------------------------------------
# CORS
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
    """

    student_results: StudentResults


class AlternativePathwayRequest(BaseModel):
    """
    Request model for finding alternative
    pathways towards a target programme.
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
        "version": "0.4.0",
        "message": "WiseLanka API is running",
        "supported_profile_formats": [
            "legacy_flat_a_level",
            "level_aware_nested",
        ],
        "features": [
            "programme_eligibility",
            "programme_recommendations",
            "career_pathway_intelligence",
            "qualification_progression",
            "alternative_pathway_intelligence",
            "skills_intelligence",
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
        "count": len(recommendations),
        "recommendations": recommendations,
    }


# ----------------------------------------
# Qualification progression endpoint
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


# ----------------------------------------
# Alternative pathway endpoint
# ----------------------------------------

@app.post(
    "/alternative-pathways/{target_programme_id}"
)
def get_alternative_pathways(
    target_programme_id: str,
    request: AlternativePathwayRequest,
):

    pathways = find_alternative_pathways(
        target_programme_id,
        request.student_results,
    )

    return pathways


# ----------------------------------------
# Skills intelligence endpoint
#
# Example:
#
# GET /skills/alignment/PRG0007/CAR0004
#
# Compares skills represented by a
# programme with skills recorded for a
# selected career.
#
# This is programme-career alignment.
# It does not claim that an individual
# learner personally has or lacks skills.
# ----------------------------------------

@app.get(
    "/skills/alignment/{programme_id}/{career_id}"
)
def get_programme_career_skill_alignment(
    programme_id: str,
    career_id: str,
):

    alignment = get_skill_alignment(
        programme_id,
        career_id,
    )

    return alignment