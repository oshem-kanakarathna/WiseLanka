from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


def test_recommendations_strong_profile():

    response = client.post(
        "/recommendations",
        json={
            "student_results": {
                "Combined Mathematics": "B",
                "Physics": "C",
                "Chemistry": "C",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3

    for result in data["recommendations"]:

        assert (
            result["category"]
            == "ELIGIBLE"
        )

        assert (
            result["match_score"]
            == 100.0
        )

        assert (
            result["failed_requirements"]
            == []
        )


def test_recommendations_near_profile():

    response = client.post(
        "/recommendations",
        json={
            "student_results": {
                "Combined Mathematics": "S",
                "Physics": "S",
                "Chemistry": "C",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3

    for result in data["recommendations"]:

        assert (
            result["category"]
            == "NEARLY_ELIGIBLE"
        )

        assert (
            result["match_score"]
            == 75.0
        )

        assert (
            len(
                result[
                    "failed_requirements"
                ]
            )
            > 0
        )


def test_recommendations_unrelated_profile():

    response = client.post(
        "/recommendations",
        json={
            "student_results": {
                "Sinhala": "A",
                "Art": "B",
                "Geography": "C",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    results = {
        item["programme_id"]: item
        for item
        in data["recommendations"]
    }

    assert (
        results["PRG0001"]["category"]
        == "NOT_ELIGIBLE"
    )

    assert (
        results["PRG0001"]["match_score"]
        == 50.0
    )

    assert (
        results["PRG0002"]["category"]
        == "NOT_ELIGIBLE"
    )

    assert (
        results["PRG0002"]["match_score"]
        == 0.0
    )

    assert (
        results["PRG0003"]["category"]
        == "NOT_ELIGIBLE"
    )

    assert (
        results["PRG0003"]["match_score"]
        == 0.0
    )
    