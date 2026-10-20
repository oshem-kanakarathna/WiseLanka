from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


def test_scholarship_eligibility_api_eligible():
    response = client.post(
        "/scholarships/SCH0001/eligibility",
        json={
            "learner_profile": {
                "citizenship": "Sri Lanka",
                "age_on_reference_date": 19,
                "a_level_exam_year": 2024,
                "a_level_pass_count": 3,
                "o_level_english_grade": "B",
                "a_level_english_grade": "S",
                "state_university_internal_student": False,
                "field": "STEM",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["scholarship_id"] == "SCH0001"
    assert data["eligibility_status"] == "ELIGIBLE_TO_APPLY"
    assert data["field_evaluation"]["status"] == "PASSED"
    assert len(data["requirements"]) == 7


def test_scholarship_eligibility_api_requirements_not_met():
    response = client.post(
        "/scholarships/SCH0001/eligibility",
        json={
            "learner_profile": {
                "citizenship": "Sri Lanka",
                "age_on_reference_date": 17,
                "a_level_exam_year": 2024,
                "a_level_pass_count": 2,
                "o_level_english_grade": "S",
                "a_level_english_grade": "S",
                "state_university_internal_student": True,
                "field": "STEM",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["eligibility_status"]
        == "REQUIREMENTS_NOT_MET"
    )

    failed_requirements = [
        requirement
        for requirement in data["requirements"]
        if requirement["status"] == "FAILED"
    ]

    assert len(failed_requirements) > 0


def test_scholarship_eligibility_api_potentially_eligible():
    response = client.post(
        "/scholarships/SCH0001/eligibility",
        json={
            "learner_profile": {
                "citizenship": "Sri Lanka",
                "age_on_reference_date": 19,
                "a_level_exam_year": 2024,
                "a_level_pass_count": 3,
                "field": "STEM",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["eligibility_status"]
        == "POTENTIALLY_ELIGIBLE"
    )

    unknown_requirements = [
        requirement
        for requirement in data["requirements"]
        if requirement["status"] == "UNKNOWN"
    ]

    assert len(unknown_requirements) > 0


def test_scholarship_eligibility_api_field_not_applicable():
    response = client.post(
        "/scholarships/SCH0001/eligibility",
        json={
            "learner_profile": {
                "citizenship": "Sri Lanka",
                "age_on_reference_date": 19,
                "a_level_exam_year": 2024,
                "a_level_pass_count": 3,
                "o_level_english_grade": "A",
                "a_level_english_grade": "B",
                "state_university_internal_student": False,
                "field": "Arts",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["field_evaluation"]["status"] == "FAILED"
    assert (
        data["eligibility_status"]
        == "REQUIREMENTS_NOT_MET"
    )


def test_scholarship_eligibility_api_unknown_scholarship():
    response = client.post(
        "/scholarships/SCH9999/eligibility",
        json={
            "learner_profile": {
                "citizenship": "Sri Lanka",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "NOT_FOUND"
    assert data["scholarship_id"] == "SCH9999"


def test_root_lists_scholarship_intelligence():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["version"] == "0.6.0"
    assert (
        "scholarship_intelligence"
        in data["features"]
    )