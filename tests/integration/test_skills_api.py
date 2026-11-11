from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


def test_skills_alignment_full_match():
    response = client.get(
        "/skills/alignment/PRG0007/CAR0004"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "AVAILABLE"
    assert data["programme_id"] == "PRG0007"
    assert data["career_id"] == "CAR0004"
    assert data["alignment_percentage"] == 100.0
    assert data["shared_skill_count"] == 7
    assert data["additional_skill_count"] == 0


def test_skills_alignment_partial_match():
    response = client.get(
        "/skills/alignment/PRG0006/CAR0003"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "AVAILABLE"
    assert data["alignment_percentage"] == 50.0
    assert data["shared_skill_count"] == 3
    assert data["additional_skill_count"] == 3

    additional_names = {
        skill["skill_name"]
        for skill in data[
            "additional_career_skills"
        ]
    }

    assert "Mathematics for Computing" in additional_names
    assert "Artificial Intelligence" in additional_names
    assert "Deep Learning" in additional_names


def test_skills_alignment_unknown_programme():
    response = client.get(
        "/skills/alignment/PRG9999/CAR0004"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "NOT_FOUND"
    assert data["alignment_percentage"] is None
    assert data["shared_skills"] == []


def test_skills_alignment_unknown_career():
    response = client.get(
        "/skills/alignment/PRG0007/CAR9999"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "NOT_FOUND"
    assert data["alignment_percentage"] is None
    assert data["shared_skills"] == []


def test_skills_alignment_explanation_is_safe():
    response = client.get(
        "/skills/alignment/PRG0006/CAR0003"
    )

    assert response.status_code == 200

    data = response.json()

    assert "personal skill" in (
        data["explanation"].lower()
    )