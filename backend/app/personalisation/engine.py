
"""Evidence-based learner personalisation for WiseLanka.

Academic eligibility and personal suitability are deliberately
separate. Missing career relationship evidence is not treated
as evidence that a programme is unsuitable.
"""

from typing import Any, Dict, List

from backend.app.recommendation.engine import recommend_programmes
from backend.app.data_loader import load_csv
from backend.app.eligibility.engine import assess_academic_gaps
from backend.app.skills.engine import assess_learner_skills
from backend.app.personalisation.models import LearnerProfile
from backend.app.progression.engine import get_progression_pathways


RELEVANCE_SCORES = {
    "high": 100.0,
    "medium": 65.0,
    "low": 30.0,
}


def _normalise(value: Any) -> str:
    return str(value or "").strip().casefold()


def _normalise_interests(interests: Any) -> List[str]:
    if not isinstance(interests, list):
        return []

    return [
        str(interest).strip()
        for interest in interests
        if isinstance(interest, str) and interest.strip()
    ]


def _assess_career_goal(
    programme: Dict[str, Any],
    career_goal_id: str,
) -> Dict[str, Any]:
    """Match a career ID against documented programme-career links."""

    if not career_goal_id:
        return {
            "status": "NOT_PROVIDED",
            "score": None,
            "explanation": "No career goal was supplied.",
        }

    for career in programme.get("career_pathways", []):
        if _normalise(career.get("career_id")) != _normalise(
            career_goal_id
        ):
            continue

        relevance = _normalise(career.get("relevance_level"))
        score = RELEVANCE_SCORES.get(relevance)

        if score is None:
            return {
                "status": "NOT_ASSESSED",
                "score": None,
                "explanation": (
                    "A career relationship exists, but its relevance "
                    "has not been assessed."
                ),
            }

        return {
            "status": "ASSESSED",
            "score": score,
            "career_id": career.get("career_id"),
            "career_name": career.get("career_name"),
            "relevance_level": career.get("relevance_level"),
            "explanation": (
                f"The curated knowledge base records "
                f"{career.get('relevance_level')} relevance between "
                f"this programme and {career.get('career_name')}."
            ),
        }

    return {
        "status": "NOT_ASSESSED",
        "score": None,
        "explanation": (
            "No verified programme-career relationship is currently "
            "recorded for this career goal. This does not mean "
            "the programme is unsuitable."
        ),
    }


def _assess_interests(
    programme: Dict[str, Any],
    interests: List[str],
) -> Dict[str, Any]:
    """Provide transparent descriptive interest matching."""

    if not interests:
        return {
            "status": "NOT_PROVIDED",
            "matched_interests": [],
            "explanation": "No interests were supplied.",
        }

    searchable_fields = [
        programme.get("programme_name", ""),
        programme.get("field_of_study", ""),
    ]

    searchable_fields.extend(
        career.get("career_category", "")
        for career in programme.get("career_pathways", [])
    )

    searchable_text = " ".join(
        _normalise(value) for value in searchable_fields
    )

    matched = [
        interest
        for interest in interests
        if _normalise(interest) in searchable_text
    ]

    return {
        "status": "DESCRIPTIVE_MATCH",
        "matched_interests": matched,
        "explanation": (
            "Interest matching checks terms in programme fields "
            "and documented career categories. It is a simple "
            "descriptive match, not a semantic AI assessment."
        ),
    }


def _assess_preferences(
    programme: Dict[str, Any],
    preferences: Dict[str, Any],
) -> Dict[str, Any]:
    """Compare preferences only when programme data is available."""

    supported_fields = ("study_mode", "district")
    comparisons = []

    for field in supported_fields:
        preferred = preferences.get(field)

        if not preferred:
            continue

        actual = programme.get(field)

        if not actual:
            comparisons.append({
                "field": field,
                "status": "UNKNOWN",
                "preferred": preferred,
                "actual": None,
            })
            continue

        comparisons.append({
            "field": field,
            "status": (
                "MATCH"
                if _normalise(preferred) == _normalise(actual)
                else "NO_MATCH"
            ),
            "preferred": preferred,
            "actual": actual,
        })

    return {
        "comparisons": comparisons,
        "explanation": (
            "Preferences are compared against available programme "
            "metadata. Unknown values are not treated as mismatches."
        ),
    }


def personalise_recommendations(
    learner_profile: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate personalised assessments without altering eligibility."""

    if not isinstance(learner_profile, dict):
        raise ValueError("learner_profile must be an object.")

    learner_profile = LearnerProfile.model_validate(learner_profile).model_dump()

    education = learner_profile.get("education")

    if not isinstance(education, dict) or (not education and not learner_profile["existing_qualifications"]):
        raise ValueError(
            "learner_profile.education must contain qualification results."
        )

    interests = _normalise_interests(
        learner_profile.get("interests", [])
    )
    career_goal_id = str(
        learner_profile.get("career_goal_id") or ""
    ).strip()

    preferences = learner_profile.get("preferences") or {}
    if not isinstance(preferences, dict):
        raise ValueError("preferences must be an object.")

    existing_recommendations = recommend_programmes(education)
    skills = assess_learner_skills(career_goal_id, learner_profile["self_reported_skills"])
    assessed_programmes = existing_recommendations or [
        row for row in load_csv("reference/programmes.csv") if row.get("programme_status") == "Active"
    ]
    academic_insights = [
        {**assess_academic_gaps(item["programme_id"], education, learner_profile["education_complete"], learner_profile["existing_qualifications"]),
         "programme_name": item["programme_name"]}
        for item in assessed_programmes
    ]
    gaps_by_id = {item["programme_id"]: item for item in academic_insights}
    personalised = []

    for programme in existing_recommendations:
        career_assessment = _assess_career_goal(
            programme, career_goal_id
        )
        interest_assessment = _assess_interests(
            programme, interests
        )
        preference_assessment = _assess_preferences(
            programme, preferences
        )

        personalised.append({
            **programme,
            "academic_match_score": programme["match_score"],
            "career_goal_assessment": career_assessment,
            "interest_assessment": interest_assessment,
            "preference_assessment": preference_assessment,
            "personal_suitability_score": career_assessment["score"],
            "personal_suitability_status": career_assessment["status"],
            "academic_gap_insights": gaps_by_id[programme["programme_id"]],
        })

    # Keep academic eligibility as the primary ordering.
    # Career suitability is a secondary ranking signal only.
    personalised.sort(
        key=lambda item: (
            item["academic_match_score"],
            (
                item["personal_suitability_score"]
                if item["personal_suitability_score"] is not None
                else -1
            ),
        ),
        reverse=True,
    )

    return {
        "count": len(personalised),
        "recommendations": personalised,
        "assessment_method": "RULE_BASED_PERSONALISATION_V1",
        "learner_category": learner_profile["learner_category"],
        "existing_qualifications": learner_profile["existing_qualifications"],
        "held_qualification_progression": [
            get_progression_pathways(item["qualification_id"])
            for item in learner_profile["existing_qualifications"] if item["qualification_id"]
        ],
        "qualification_note": "Awards are self-reported context only. Their authenticity, equivalence and admission eligibility have not been verified.",
        "academic_insights": academic_insights,
        "learner_skill_insights": skills,
        "disclaimer": (
            "Academic eligibility is based on curated requirements. "
            "Career suitability uses documented programme-career "
            "relationships. Missing evidence is not a negative "
            "assessment. Results are guidance, not admission decisions."
        ),
    }
