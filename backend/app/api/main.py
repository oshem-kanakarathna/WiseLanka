
from typing import Any, Dict, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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

from backend.app.scholarships.engine import (
    evaluate_scholarship,
)

from backend.app.personalisation.engine import (
    personalise_recommendations,
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

ScholarshipProfile = Dict[str, Any]


# ----------------------------------------
# Create WiseLanka API
# ----------------------------------------

app = FastAPI(
    title="WiseLanka API",
    description=(
        "Education and career pathway intelligence "
        "backend for Sri Lankan learners."
    ),
    version="0.6.0",
)


# ----------------------------------------
# CORS configuration
# ----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------
# Existing request models
# ----------------------------------------

class EligibilityRequest(BaseModel):
    programme_id: str
    student_results: StudentResults


class RecommendationRequest(BaseModel):
    student_results: StudentResults


class AlternativePathwayRequest(BaseModel):
    student_results: StudentResults


class ScholarshipEligibilityRequest(BaseModel):
    learner_profile: ScholarshipProfile


# ----------------------------------------
# Personalisation request models
# ----------------------------------------

class LearnerProfile(BaseModel):
    """
    Structured learner profile.

    Education accepts both existing formats:

    1. Flat A/L results:
       {"Physics": "B", "Chemistry": "C"}

    2. Nested education levels:
       {"A_LEVEL": {"Physics": "B"}}
    """

    education: StudentResults

    interests: list[str] = Field(
        default_factory=list
    )

    career_goal_id: str = ""

    preferences: Dict[str, Any] = Field(
        default_factory=dict
    )


class PersonalisedRecommendationRequest(BaseModel):
    learner_profile: LearnerProfile


# ----------------------------------------
# API health check
# ----------------------------------------

@app.get("/")
def root():

    return {
        "application": "WiseLanka",
        "status": "running",
        "version": "0.6.0",
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
            "scholarship_intelligence",
            "learner_personalisation",
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
# Existing recommendation endpoint
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
# NEW: Personalised recommendation endpoint
# ----------------------------------------

@app.post("/personalised-recommendations")
def get_personalised_recommendations(
    request: PersonalisedRecommendationRequest,
):
    """
    Return academic recommendations enriched with
    transparent personal suitability assessments.

    Academic eligibility is never overridden by
    interests or career preferences.
    """

    try:
        result = personalise_recommendations(
            request.learner_profile.model_dump()
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    return result


# ----------------------------------------
# Qualification progression endpoint
# ----------------------------------------

@app.get("/progression/{qualification_id}")
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
        request.student_results
    )

    return pathways


# ----------------------------------------
# Skills intelligence endpoint
#
# Example:
# GET /skills/alignment/PRG0007/CAR0004
#
# Compares skills represented by a programme
# with skills recorded for a selected career.
#
# This does NOT mean the learner personally
# has or lacks those skills.
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


# ----------------------------------------
# Scholarship intelligence endpoint
#
# Example:
# POST /scholarships/SCH0001/eligibility
#
# Evaluates a learner profile against
# evidence-backed scholarship rules.
#
# Possible assessment outcomes:
# ELIGIBLE_TO_APPLY
# POTENTIALLY_ELIGIBLE
# REQUIREMENTS_NOT_MET
#
# Eligibility to apply does not guarantee
# nomination, selection, admission,
# or a scholarship award.
#
# Scholarship application availability
# must be checked separately.
# ----------------------------------------

@app.post(
    "/scholarships/{scholarship_id}/eligibility"
)
def check_scholarship_eligibility(
    scholarship_id: str,
    request: ScholarshipEligibilityRequest,
):

    result = evaluate_scholarship(
        scholarship_id,
        request.learner_profile,
    )

    return result
