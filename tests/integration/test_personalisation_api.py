
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

    assert data["count"] == 8
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
        if programme["programme_id"] not in {"PRG0001", "PRG0002", "PRG0003"}:
            continue
        assert programme["eligible"] is False
        assert programme["category"] == "NOT_ASSESSED"
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
    assert response.json()["count"] == 8


def test_vocational_profile_includes_exact_documented_nvq_entry_route():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(
            education={},
            learner_category="VOCATIONAL_LEARNER",
            existing_qualifications=[{
                "qualification_id": "QLF0012",
                "title": "Electrician (NVQ Level 4 Certificate)",
            }],
        ),
    )

    assert response.status_code == 200
    data = response.json()
    route = next(item for item in data["recommendations"] if item["programme_id"] == "PRG0010")
    assert route["academic_gap_insights"]["status"] == "NOT_ASSESSED"
    assert route["eligible"] is False
    groups = {group["group_id"]: group for group in route["academic_gap_insights"]["groups"]}
    assert groups["GRP015"]["operator"] == "OR"
    assert groups["GRP015"]["status"] == "MET"
    assert groups["GRP016"]["operator"] == "AND"
    assert groups["GRP016"]["status"] == "NOT_ASSESSED"
    assert "not admission decisions" in data["disclaimer"]


def test_vocational_profile_includes_exact_hnd_qualification_progression_route():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(
            education={},
            learner_category="VOCATIONAL_LEARNER",
            existing_qualifications=[{
                "qualification_id": "QLF0010",
                "title": "Higher National Diploma in Mechatronics Technology",
            }],
        ),
    )

    assert response.status_code == 200
    data = response.json()
    route = next(item for item in data["recommendations"] if item["programme_id"] == "PRG0011")
    assert route["academic_gap_insights"]["status"] == "NOT_ASSESSED"
    assert route["eligible"] is False


def test_unrelated_reported_qualification_does_not_shortlist_nvqq_route():
    response = client.post(
        "/personalised-recommendations",
        json=make_profile(
            education={},
            learner_category="VOCATIONAL_LEARNER",
            existing_qualifications=[{
                "title": "Synthetic unrelated qualification",
            }],
        ),
    )

    assert response.status_code == 200
    ids = {item["programme_id"] for item in response.json()["recommendations"]}
    assert "PRG0010" not in ids
    assert "PRG0011" not in ids
