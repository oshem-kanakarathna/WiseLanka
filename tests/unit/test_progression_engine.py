from backend.app.progression.engine import (
    get_progression_pathways,
)


def test_foundation_has_three_progression_pathways():

    result = get_progression_pathways(
        "QLF0004"
    )

    assert result["qualification_id"] == "QLF0004"
    assert result["count"] == 3
    assert len(result["pathways"]) == 3


def test_foundation_progression_destinations():

    result = get_progression_pathways(
        "QLF0004"
    )

    destination_ids = {
        pathway["to_qualification_id"]
        for pathway in result["pathways"]
    }

    assert destination_ids == {
        "QLF0005",
        "QLF0006",
        "QLF0007",
    }


def test_software_engineering_progression():

    result = get_progression_pathways(
        "QLF0004"
    )

    pathway = next(
        item
        for item in result["pathways"]
        if item["to_qualification_id"]
        == "QLF0005"
    )

    assert (
        pathway["qualification_name"]
        == "BEng (Hons) Software Engineering"
    )

    assert (
        pathway["progression_type"]
        == "Direct Academic Progression"
    )

    assert pathway["guaranteed"] is False

    assert len(pathway["programmes"]) == 1

    programme = pathway["programmes"][0]

    assert programme["programme_id"] == "PRG0005"

    assert (
        programme["provider_name"]
        == "Informatics Institute of Technology"
    )

    assert (
        programme["awarding_body_name"]
        == "University of Westminster"
    )


def test_computer_science_progression():

    result = get_progression_pathways(
        "QLF0004"
    )

    pathway = next(
        item
        for item in result["pathways"]
        if item["to_qualification_id"]
        == "QLF0006"
    )

    programme = pathway["programmes"][0]

    assert programme["programme_id"] == "PRG0006"

    assert (
        programme["awarding_body_name"]
        == "University of Westminster"
    )


def test_ai_data_science_progression_is_conditional():

    result = get_progression_pathways(
        "QLF0004"
    )

    pathway = next(
        item
        for item in result["pathways"]
        if item["to_qualification_id"]
        == "QLF0007"
    )

    assert (
        pathway["progression_type"]
        == "Conditional Academic Progression"
    )

    assert pathway["guaranteed"] is False

    assert "50 percent" in pathway["conditions"]

    programme = pathway["programmes"][0]

    assert programme["programme_id"] == "PRG0007"

    assert (
        programme["awarding_body_name"]
        == "Robert Gordon University"
    )


def test_unknown_qualification_returns_empty_result():

    result = get_progression_pathways(
        "QLF9999"
    )

    assert result["qualification_id"] == "QLF9999"
    assert result["qualification_name"] is None
    assert result["count"] == 0
    assert result["pathways"] == []


def test_degree_with_no_further_progression_returns_empty_pathways():

    result = get_progression_pathways(
        "QLF0005"
    )

    assert result["qualification_id"] == "QLF0005"

    assert (
        result["qualification_name"]
        == "BEng (Hons) Software Engineering"
    )

    assert result["count"] == 0
    assert result["pathways"] == []