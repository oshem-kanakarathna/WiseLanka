from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


# ========================================
# A/L RECOMMENDATION TESTS
# ========================================


def test_recommendations_strong_profile():
    """
    A strong legacy flat A/L profile should
    return all currently supported A/L-entry
    degree programmes as eligible.
    """

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

    programme_ids = {
        result["programme_id"]
        for result in data["recommendations"]
    }

    assert programme_ids == {
        "PRG0001",
        "PRG0002",
        "PRG0003",
    }

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

        assert (
            result["entry_education_levels"]
            == ["A_LEVEL"]
        )


def test_recommendations_near_profile():
    """
    An A/L profile that passes the general
    subject requirements but misses the
    required C-grade mathematics/physics
    condition should be nearly eligible.
    """

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

        assert (
            result["entry_education_levels"]
            == ["A_LEVEL"]
        )


def test_recommendations_unrelated_profile():
    """
    An unrelated A/L profile should not be
    classified as eligible for the currently
    supported computing degree programmes.
    """

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

    assert data["count"] == 3

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

    for result in data["recommendations"]:

        assert (
            result["entry_education_levels"]
            == ["A_LEVEL"]
        )


# ========================================
# O/L RECOMMENDATION TESTS
# ========================================


def test_recommendations_ol_profile():
    """
    A qualifying O/L learner should receive
    the O/L-entry IIT Computing Foundation
    programme rather than A/L-entry degrees.
    """

    response = client.post(
        "/recommendations",
        json={
            "student_results": {
                "O_LEVEL": {
                    "Mathematics": "A",
                    "English": "B",
                    "Science": "C",
                    "ICT": "A",
                    "Sinhala": "S",
                    "History": "S",
                }
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 1

    recommendation = (
        data["recommendations"][0]
    )

    assert (
        recommendation["programme_id"]
        == "PRG0004"
    )

    assert (
        recommendation["category"]
        == "ELIGIBLE"
    )

    assert (
        recommendation["eligible"]
        is True
    )

    assert (
        recommendation["match_score"]
        == 100.0
    )

    assert (
        recommendation[
            "entry_education_levels"
        ]
        == ["O_LEVEL"]
    )

    assert (
        recommendation[
            "failed_requirements"
        ]
        == []
    )


def test_ol_profile_excludes_al_programmes():
    """
    O/L-only learners must not receive
    A/L-entry degree programmes as immediate
    programme recommendations.
    """

    response = client.post(
        "/recommendations",
        json={
            "student_results": {
                "O_LEVEL": {
                    "Mathematics": "A",
                    "English": "B",
                    "Science": "C",
                    "ICT": "A",
                    "Sinhala": "S",
                    "History": "S",
                }
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    programme_ids = {
        result["programme_id"]
        for result in data["recommendations"]
    }

    assert "PRG0001" not in programme_ids
    assert "PRG0002" not in programme_ids
    assert "PRG0003" not in programme_ids

    assert programme_ids == {
        "PRG0004"
    }


# ========================================
# NESTED A/L FORMAT TEST
# ========================================


def test_recommendations_nested_al_profile():
    """
    The newer nested A/L profile format should
    produce the same immediate A/L programme
    recommendations as the legacy flat format.
    """

    response = client.post(
        "/recommendations",
        json={
            "student_results": {
                "A_LEVEL": {
                    "Combined Mathematics": "B",
                    "Physics": "C",
                    "Chemistry": "C",
                }
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3

    programme_ids = {
        result["programme_id"]
        for result in data["recommendations"]
    }

    assert programme_ids == {
        "PRG0001",
        "PRG0002",
        "PRG0003",
    }

    assert "PRG0004" not in programme_ids

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
            result["entry_education_levels"]
            == ["A_LEVEL"]
        )