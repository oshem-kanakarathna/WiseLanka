
"""Integration tests for WiseLanka personalisation API."""

from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


STRONG_AL_RESULTS = {
    "A_LEVEL": {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }
}


def make_profile(**overrides):
    profile = {
        "education": STRONG_AL_RESULTS,
        "interests": ["Artificial Intelligence"],
        "career_goal_id": "CAR0001",
        "preferences": {"district": "Colombo"},
    }
    profile.update(overrides)
    return {"learner_profile": profile}


def test_personalised_endpoint_returns_success():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert (
        data["assessment_method"]
        == "RULE_BASED_PERSONALISATION_V1"
    )


def test_personalised_endpoint_preserves_eligibility():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(),
    )

    assert response.status_code == 200

    for programme in response.json()["recommendations"]:
        assert programme["eligible"] is True
        assert programme["category"] == "ELIGIBLE"
        assert programme["academic_match_score"] == 100.0


def test_personalised_endpoint_uses_career_evidence():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(),
    )

    programmes = {
        item["programme_id"]: item
        for item in response.json()["recommendations"]
    }

    assert programmes["PRG0001"]["personal_suitability_score"] == 100.0
    assert programmes["PRG0002"]["personal_suitability_score"] == 100.0
    assert programmes["PRG0003"]["personal_suitability_score"] == 65.0


def test_personalised_endpoint_preserves_explanations():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(),
    )

    assert response.status_code == 200

    for programme in response.json()["recommendations"]:
        assert programme["career_goal_assessment"]["explanation"]
        assert programme["interest_assessment"]["explanation"]
        assert programme["preference_assessment"]["explanation"]


def test_unknown_career_does_not_mean_unsuitable():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(career_goal_id="CAR9999"),
    )

    assert response.status_code == 200

    for programme in response.json()["recommendations"]:
        assert programme["personal_suitability_score"] is None
        assert (
            programme["personal_suitability_status"]
            == "NOT_ASSESSED"
        )


def test_missing_education_returns_validation_error():
    response = client.post(
        "/personalised-recommendations",
        json={
            "learner_profile": {
                "career_goal_id": "CAR0001",
            }
        },
    )

    assert response.status_code == 422


def test_empty_education_returns_validation_error():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(education={}),
    )

    assert response.status_code == 422


def test_invalid_preferences_returns_validation_error():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(preferences=["Colombo"]),
    )

    assert response.status_code == 422


def test_existing_recommendation_endpoint_still_works():
    response = client.post(
        "/recommendations",
        json={
            "student_results": STRONG_AL_RESULTS,
        },
    )

    assert response.status_code == 200
    assert response.json()["count"] == 3
