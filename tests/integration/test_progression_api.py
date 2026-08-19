from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


def test_foundation_progression_api():

    response = client.get(
        "/progression/QLF0004"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["qualification_id"]
        == "QLF0004"
    )

    assert data["count"] == 3

    destinations = {
        pathway[
            "to_qualification_id"
        ]
        for pathway
        in data["pathways"]
    }

    assert destinations == {
        "QLF0005",
        "QLF0006",
        "QLF0007",
    }


def test_foundation_progression_api_contains_programmes():

    response = client.get(
        "/progression/QLF0004"
    )

    assert response.status_code == 200

    data = response.json()

    programmes = {}

    for pathway in data["pathways"]:

        for programme in pathway["programmes"]:

            programmes[
                programme["programme_id"]
            ] = programme

    assert "PRG0005" in programmes
    assert "PRG0006" in programmes
    assert "PRG0007" in programmes

    assert (
        programmes["PRG0005"][
            "awarding_body_name"
        ]
        == "University of Westminster"
    )

    assert (
        programmes["PRG0006"][
            "awarding_body_name"
        ]
        == "University of Westminster"
    )

    assert (
        programmes["PRG0007"][
            "awarding_body_name"
        ]
        == "Robert Gordon University"
    )


def test_ai_progression_api_preserves_condition():

    response = client.get(
        "/progression/QLF0004"
    )

    assert response.status_code == 200

    data = response.json()

    pathway = next(
        item
        for item in data["pathways"]
        if item[
            "to_qualification_id"
        ] == "QLF0007"
    )

    assert (
        pathway["progression_type"]
        == "Conditional Academic Progression"
    )

    assert pathway["guaranteed"] is False

    assert (
        "50 percent"
        in pathway["conditions"]
    )


def test_unknown_progression_api_returns_empty_result():

    response = client.get(
        "/progression/QLF9999"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["qualification_id"]
        == "QLF9999"
    )

    assert data["count"] == 0

    assert data["pathways"] == []