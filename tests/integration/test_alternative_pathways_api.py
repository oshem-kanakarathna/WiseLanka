"""
Integration tests for the WiseLanka
Alternative Pathway Intelligence API.

These tests verify that the FastAPI endpoint
correctly connects the HTTP layer with the
alternative pathway engine.
"""

from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


# --------------------------------------------------
# Test 1
# Eligible O/L learner should receive an available
# foundation pathway towards Computer Science.
# --------------------------------------------------

def test_alternative_pathway_api_available_now():

    response = client.post(
        "/alternative-pathways/PRG0006",
        json={
            "student_results": {
                "O_LEVEL": {
                    "Mathematics": "A",
                    "English": "A",
                    "Science": "A",
                    "ICT": "A",
                    "Sinhala": "A",
                    "History": "A",
                }
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["target_programme_id"] == "PRG0006"
    assert data["target_qualification_id"] == "QLF0006"

    assert data["count"] == 1
    assert data["eligible_alternative_count"] == 1

    pathway = data["alternative_pathways"][0]

    assert pathway["alternative_programme_id"] == "PRG0004"

    assert (
        pathway["alternative_qualification_id"]
        == "QLF0004"
    )

    assert pathway["pathway_status"] == "AVAILABLE_NOW"

    assert pathway["current_eligibility"]["eligible"] is True

    assert (
        pathway["progression_type"]
        == "Direct Academic Progression"
    )

    assert pathway["target_programme_id"] == "PRG0006"


# --------------------------------------------------
# Test 2
# Learner who does not satisfy the foundation
# requirements should still receive the route,
# but it must be marked REQUIREMENTS_NOT_MET.
# --------------------------------------------------

def test_alternative_pathway_api_requirements_not_met():

    response = client.post(
        "/alternative-pathways/PRG0006",
        json={
            "student_results": {
                "O_LEVEL": {
                    "Mathematics": "S",
                    "English": "S",
                    "Science": "S",
                    "ICT": "S",
                    "Sinhala": "S",
                    "History": "S",
                }
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["target_programme_id"] == "PRG0006"

    assert data["count"] == 1
    assert data["eligible_alternative_count"] == 0

    pathway = data["alternative_pathways"][0]

    assert pathway["alternative_programme_id"] == "PRG0004"

    assert (
        pathway["pathway_status"]
        == "REQUIREMENTS_NOT_MET"
    )

    assert pathway["current_eligibility"]["eligible"] is False

    assert len(
        pathway["current_eligibility"]["failed_requirements"]
    ) > 0


# --------------------------------------------------
# Test 3
# Unknown target programme should return a valid
# empty result rather than crash the API.
# --------------------------------------------------

def test_alternative_pathway_api_unknown_programme():

    response = client.post(
        "/alternative-pathways/PRG9999",
        json={
            "student_results": {
                "O_LEVEL": {
                    "Mathematics": "A",
                    "English": "A",
                    "Science": "A",
                }
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["target_programme_id"] == "PRG9999"

    assert data["count"] == 0
    assert data["eligible_alternative_count"] == 0

    assert data["alternative_pathways"] == []


# --------------------------------------------------
# Test 4
# Missing request body should be rejected by
# FastAPI/Pydantic validation.
# --------------------------------------------------

def test_alternative_pathway_api_missing_body():

    response = client.post(
        "/alternative-pathways/PRG0006"
    )

    assert response.status_code == 422


# --------------------------------------------------
# Test 5
# Malformed student_results should be rejected
# rather than reaching the pathway engine.
# --------------------------------------------------

def test_alternative_pathway_api_invalid_profile():

    response = client.post(
        "/alternative-pathways/PRG0006",
        json={
            "student_results": [
                "Mathematics",
                "English",
            ]
        },
    )

    assert response.status_code == 422