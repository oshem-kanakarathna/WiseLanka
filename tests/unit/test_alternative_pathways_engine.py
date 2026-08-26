from backend.app.alternative_pathways.engine import (
    find_alternative_pathways,
)


GOOD_O_LEVEL_PROFILE = {
    "O_LEVEL": {
        "Mathematics": "A",
        "English": "A",
        "Science": "A",
        "ICT": "A",
        "Sinhala": "A",
        "History": "A",
    }
}


WEAK_O_LEVEL_PROFILE = {
    "O_LEVEL": {
        "Mathematics": "S",
        "English": "S",
        "Science": "S",
        "ICT": "S",
        "Sinhala": "S",
        "History": "S",
    }
}


def test_computer_science_alternative_pathway_available():
    result = find_alternative_pathways(
        "PRG0006",
        GOOD_O_LEVEL_PROFILE,
    )

    assert result["target_programme_id"] == "PRG0006"
    assert result["target_qualification_id"] == "QLF0006"
    assert result["count"] >= 1
    assert result["eligible_alternative_count"] >= 1

    pathway = result["alternative_pathways"][0]

    assert pathway["alternative_programme_id"] == "PRG0004"
    assert pathway["alternative_qualification_id"] == "QLF0004"

    assert pathway["current_eligibility"]["eligible"] is True

    assert pathway["pathway_status"] == "AVAILABLE_NOW"

    assert (
        pathway["progression_type"]
        == "Direct Academic Progression"
    )

    assert pathway["target_programme_id"] == "PRG0006"


def test_ai_data_science_preserves_conditional_progression():
    result = find_alternative_pathways(
        "PRG0007",
        GOOD_O_LEVEL_PROFILE,
    )

    assert result["target_programme_id"] == "PRG0007"
    assert result["eligible_alternative_count"] >= 1

    pathway = result["alternative_pathways"][0]

    assert pathway["alternative_programme_id"] == "PRG0004"
    assert pathway["pathway_status"] == "AVAILABLE_NOW"

    assert (
        pathway["progression_type"]
        == "Conditional Academic Progression"
    )

    assert "50 percent" in pathway["progression_conditions"]

    assert pathway["guaranteed"] is False


def test_existing_pathway_can_be_currently_unavailable():
    result = find_alternative_pathways(
        "PRG0006",
        WEAK_O_LEVEL_PROFILE,
    )

    assert result["count"] >= 1
    assert result["eligible_alternative_count"] == 0

    pathway = result["alternative_pathways"][0]

    assert pathway["alternative_programme_id"] == "PRG0004"

    assert pathway["current_eligibility"]["eligible"] is False

    assert (
        pathway["pathway_status"]
        == "REQUIREMENTS_NOT_MET"
    )

    failed = pathway["current_eligibility"][
        "failed_requirements"
    ]

    assert len(failed) > 0

    assert any(
        "Mathematics" in requirement
        for requirement in failed
    )

    assert any(
        "English" in requirement
        for requirement in failed
    )


def test_unknown_target_programme_returns_empty_result():
    result = find_alternative_pathways(
        "PRG9999",
        GOOD_O_LEVEL_PROFILE,
    )

    assert result["target_programme_id"] == "PRG9999"
    assert result["target_programme_name"] is None
    assert result["target_qualification_id"] is None

    assert result["count"] == 0
    assert result["eligible_alternative_count"] == 0

    assert result["alternative_pathways"] == []

    assert "message" in result


def test_programme_without_incoming_progression_returns_no_alternatives():
    result = find_alternative_pathways(
        "PRG0004",
        GOOD_O_LEVEL_PROFILE,
    )

    assert result["target_programme_id"] == "PRG0004"

    assert result["count"] == 0
    assert result["eligible_alternative_count"] == 0

    assert result["alternative_pathways"] == []