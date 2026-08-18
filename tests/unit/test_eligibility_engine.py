from backend.app.eligibility.engine import (
    evaluate_requirement,
    get_results_for_level,
)


def make_requirement(
    requirement_type,
    minimum_count="",
    subject_name="",
):
    """
    Create a minimal O/L requirement row
    for eligibility-engine unit testing.
    """

    return {
        "requirement_id": "TEST001",
        "programme_id": "TEST_PROGRAMME",
        "requirement_group_id": "TEST_GROUP",
        "group_operator": "AND",
        "education_level": "O_LEVEL",
        "requirement_type": requirement_type,
        "subject_name": subject_name,
        "minimum_grade": "",
        "minimum_count": minimum_count,
        "qualification_id": "",
        "description": "",
        "mandatory": "true",
        "source_id": "TEST_SOURCE",
    }


def strong_ol_profile():
    """
    Example O/L profile satisfying the
    intended IIT Foundation requirements.
    """

    return {
        "O_LEVEL": {
            "Mathematics": "A",
            "English": "B",
            "Science": "C",
            "ICT": "A",
            "Sinhala": "S",
            "History": "S",
        }
    }


def test_nested_ol_results_are_selected():

    profile = strong_ol_profile()

    results = get_results_for_level(
        profile,
        "O_LEVEL",
    )

    assert results["Mathematics"] == "A"
    assert results["English"] == "B"


def test_flat_legacy_results_are_not_treated_as_ol():

    profile = {
        "Mathematics": "A",
        "English": "A",
    }

    results = get_results_for_level(
        profile,
        "O_LEVEL",
    )

    assert results == {}


def test_ol_six_passes_requirement():

    requirement = make_requirement(
        "O_LEVEL_PASS_COUNT",
        minimum_count="6",
    )

    result = evaluate_requirement(
        requirement,
        strong_ol_profile(),
    )

    assert result["passed"] is True


def test_ol_three_credit_requirement():

    requirement = make_requirement(
        "O_LEVEL_CREDIT_COUNT",
        minimum_count="3",
    )

    result = evaluate_requirement(
        requirement,
        strong_ol_profile(),
    )

    assert result["passed"] is True


def test_ol_mathematics_credit_requirement():

    requirement = make_requirement(
        "O_LEVEL_SUBJECT_CREDIT",
        subject_name="Mathematics",
    )

    result = evaluate_requirement(
        requirement,
        strong_ol_profile(),
    )

    assert result["passed"] is True


def test_ol_english_credit_requirement():

    requirement = make_requirement(
        "O_LEVEL_SUBJECT_CREDIT",
        subject_name="English",
    )

    result = evaluate_requirement(
        requirement,
        strong_ol_profile(),
    )

    assert result["passed"] is True


def test_ol_subject_credit_fails_for_s_grade():

    requirement = make_requirement(
        "O_LEVEL_SUBJECT_CREDIT",
        subject_name="English",
    )

    profile = strong_ol_profile()

    profile["O_LEVEL"]["English"] = "S"

    result = evaluate_requirement(
        requirement,
        profile,
    )

    assert result["passed"] is False


def test_ol_pass_count_fails_below_six():

    requirement = make_requirement(
        "O_LEVEL_PASS_COUNT",
        minimum_count="6",
    )

    profile = {
        "O_LEVEL": {
            "Mathematics": "A",
            "English": "B",
            "Science": "C",
            "ICT": "S",
            "History": "S",
            "Sinhala": "F",
        }
    }

    result = evaluate_requirement(
        requirement,
        profile,
    )

    assert result["passed"] is False