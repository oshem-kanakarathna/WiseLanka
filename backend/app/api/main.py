
from typing import Any, Dict, Union

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from backend.app.personalisation.models import LearnerProfile, ExistingQualification
from backend.app.data_loader import load_csv, KnowledgeDataError
from backend.app.data_integrity import validate_catalogue
from backend.app.assistant.engine import GuidanceRequest, answer as guidance_answer, options as guidance_options
from backend.app.research.api import router as research_router
from backend.app.gemini_exploration.api import router as gemini_exploration_router

from backend.app.eligibility.engine import (
    evaluate_programme, assess_academic_gaps,
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

@asynccontextmanager
async def lifespan(app):
    validate_catalogue()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="WiseLanka API",
    description=(
        "Education and career pathway intelligence "
        "backend for Sri Lankan learners."
    ),
    version="0.6.0",
)
app.include_router(research_router)
app.include_router(gemini_exploration_router)


@app.exception_handler(FileNotFoundError)
@app.exception_handler(KnowledgeDataError)
async def knowledge_data_error(request, error):
    return JSONResponse(status_code=503, content={
        "detail": "Educational knowledge data is unavailable or invalid. No eligibility decision was made."
    })


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

class ExamResultsRequest(BaseModel):
    student_results: StudentResults

    @field_validator("student_results")
    @classmethod
    def validate_results(cls, value):
        return LearnerProfile.validate_results(value)


class EligibilityRequest(ExamResultsRequest):
    programme_id: str
    existing_qualifications: list[ExistingQualification] = Field(default_factory=list)
    education_complete: Dict[str, bool] = Field(default_factory=dict)


class RecommendationRequest(ExamResultsRequest):
    pass


class AlternativePathwayRequest(ExamResultsRequest):
    pass


class ScholarshipEligibilityRequest(BaseModel):
    learner_profile: ScholarshipProfile


# ----------------------------------------
# Personalisation request models
# ----------------------------------------

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
        [item.model_dump() for item in request.existing_qualifications],
    )
    insight = assess_academic_gaps(
        request.programme_id, request.student_results, request.education_complete,
        [item.model_dump() for item in request.existing_qualifications],
    )
    explanation = build_explanation(technical_result, insight)

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

@app.get("/profile-options")
def get_profile_options():
    """Read-only choices from the existing CSV knowledge base."""
    return {
        "skills": [
            {"skill_id": row["skill_id"], "skill_name": row["skill_name"]}
            for row in load_csv("reference/skills.csv") if row.get("active_status") == "Active"
        ],
        "qualifications": [
            {key: row[key] for key in ("qualification_id", "qualification_name", "framework_name", "framework_level")}
            for row in load_csv("reference/qualifications.csv") if row.get("active_status") == "Active"
        ],
    }


@app.post("/personalised-recommendations")
def get_personalised_recommendations(
    request: PersonalisedRecommendationRequest,
):
    """
    Return academic recommendations enriched with
    transparent personal suitability assessments.

    Academic eligibility is never overridden by
    interests or career preferences.

    Canonical evidence-aware academic status is in
    recommendations[].academic_gap_insights.status and academic_insights[].status:
    MET, NOT_MET or NOT_ASSESSED. NOT_ASSESSED is neither eligibility nor rejection.
    Legacy eligible/category/match_score fields remain unchanged for compatibility
    and must not override this status when input or source evidence is missing.
    Reported qualifications and skills do not verify admission equivalence or competence.
    """

    try:
        result = personalise_recommendations(
            request.learner_profile.model_dump()
        )

    except KnowledgeDataError:
        raise
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


@app.get("/assistant/options")
def assistant_options():
    return guidance_options()


@app.post("/assistant/guidance")
def assistant_guidance(request: GuidanceRequest):
    try:
        return guidance_answer(request)
    except KnowledgeDataError:
        raise
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
