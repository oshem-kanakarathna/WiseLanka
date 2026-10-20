
import pytest

from backend.app.personalisation.engine import (
    personalise_recommendations,
)


STRONG_AL_RESULTS = {
    "Combined Mathematics": "B",
    "Physics": "C",
    "Chemistry": "C",
}


def get_programme(response, programme_id):
    return next(
        programme
        for programme in response["recommendations"]
        if programme["programme_id"] == programme_id
    )


def test_personalisation_preserves_academic_eligibility():
    response = personalise_recommendations({
        "education": STRONG_AL_RESULTS,
        "career_goal_id": "CAR0001",
    })

    programme = get_programme(response, "PRG0001")

    assert programme["eligible"] is True
    assert programme["category"] == "ELIGIBLE"
    assert programme["match_score"] == 100.0
    assert programme["academic_match_score"] == 100.0


def test_software_engineering_career_alignment():
    response = personalise_recommendations({
        "education": STRONG_AL_RESULTS,
        "career_goal_id": "CAR0001",
    })

    it_programme = get_programme(response, "PRG0001")
    ai_programme = get_programme(response, "PRG0003")

    assert it_programme["personal_suitability_score"] == 100.0
    assert ai_programme["personal_suitability_score"] == 65.0

    assert (
        it_programme["career_goal_assessment"]["relevance_level"]
        == "High"
    )


def test_interests_match_programme_description():
    response = personalise_recommendations({
        "education": STRONG_AL_RESULTS,
        "interests": ["Artificial Intelligence"],
    })

    ai_programme = get_programme(response, "PRG0003")

    assert (
        "Artificial Intelligence"
        in ai_programme["interest_assessment"]["matched_interests"]
    )


def test_study_preference_is_recorded():
    response = personalise_recommendations({
        "education": STRONG_AL_RESULTS,
        "preferences": {
            "district": "Colombo",
        },
    })

    programme = get_programme(response, "PRG0001")

    comparisons = programme["preference_assessment"]["comparisons"]

    assert len(comparisons) == 1
    assert comparisons[0]["field"] == "district"
    assert comparisons[0]["preferred"] == "Colombo"
    assert comparisons[0]["status"] in {
        "MATCH",
        "NO_MATCH",
        "UNKNOWN",
    }


def test_missing_career_relationship_is_not_negative_score():
    response = personalise_recommendations({
        "education": STRONG_AL_RESULTS,
        "career_goal_id": "CAR9999",
    })

    for programme in response["recommendations"]:
        assert programme["personal_suitability_score"] is None
        assert (
            programme["personal_suitability_status"]
            == "NOT_ASSESSED"
        )


def test_missing_education_is_rejected():
    with pytest.raises(ValueError):
        personalise_recommendations({
            "career_goal_id": "CAR0001",
        })


def test_personalisation_returns_explanations():
    response = personalise_recommendations({
        "education": STRONG_AL_RESULTS,
        "career_goal_id": "CAR0001",
        "interests": ["Software Development"],
    })

    for programme in response["recommendations"]:
        assert programme["career_goal_assessment"]["explanation"]
        assert programme["interest_assessment"]["explanation"]
        assert programme["preference_assessment"]["explanation"]


def test_original_recommendation_fields_are_preserved():
    response = personalise_recommendations({
        "education": STRONG_AL_RESULTS,
        "career_goal_id": "CAR0001",
    })

    for programme in response["recommendations"]:
        assert "programme_id" in programme
        assert "career_pathways" in programme
        assert "progression" in programme
        assert "failed_requirements" in programme
