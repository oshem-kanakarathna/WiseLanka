from backend.app.skills.engine import (
    get_career_skills,
    get_programme_skills,
    get_skill_alignment,
)


def test_get_programme_skills():
    skills = get_programme_skills(
        "PRG0007"
    )

    skill_names = {
        skill["skill_name"]
        for skill in skills
    }

    assert len(skills) == 9

    assert "Programming" in skill_names
    assert "Machine Learning" in skill_names
    assert "Artificial Intelligence" in skill_names
    assert "Deep Learning" in skill_names


def test_get_career_skills():
    skills = get_career_skills(
        "CAR0004"
    )

    skill_names = {
        skill["skill_name"]
        for skill in skills
    }

    assert len(skills) == 7

    assert "Programming" in skill_names
    assert "Machine Learning" in skill_names
    assert "Deep Learning" in skill_names


def test_full_skill_alignment():
    result = get_skill_alignment(
        "PRG0007",
        "CAR0004",
    )

    assert result["status"] == "AVAILABLE"

    assert (
        result["alignment_percentage"]
        == 100.0
    )

    assert (
        result["shared_skill_count"]
        == 7
    )

    assert (
        result["additional_skill_count"]
        == 0
    )


def test_partial_skill_alignment():
    result = get_skill_alignment(
        "PRG0006",
        "CAR0003",
    )

    assert result["status"] == "AVAILABLE"

    assert (
        result["alignment_percentage"]
        == 50.0
    )

    assert (
        result["shared_skill_count"]
        == 3
    )

    assert (
        result["additional_skill_count"]
        == 3
    )

    additional_names = {
        skill["skill_name"]
        for skill
        in result[
            "additional_career_skills"
        ]
    }

    assert (
        "Mathematics for Computing"
        in additional_names
    )

    assert (
        "Artificial Intelligence"
        in additional_names
    )

    assert (
        "Deep Learning"
        in additional_names
    )


def test_unknown_programme():
    result = get_skill_alignment(
        "PRG9999",
        "CAR0004",
    )

    assert result["status"] == "NOT_FOUND"

    assert (
    result["alignment_percentage"]
    is None
)

    assert result["shared_skills"] == []

    assert (
        result["additional_career_skills"]
        == []
    )


def test_unknown_career():
    result = get_skill_alignment(
        "PRG0007",
        "CAR9999",
    )

    assert result["status"] == "NOT_FOUND"

    assert (
    result["alignment_percentage"]
    is None
)

    assert result["shared_skills"] == []

    assert (
        result["additional_career_skills"]
        == []
    )


def test_additional_skills_are_not_personal_skill_gaps():
    result = get_skill_alignment(
        "PRG0006",
        "CAR0003",
    )

    explanation = result[
        "explanation"
    ].lower()

    assert "personal skill" in explanation

def test_insufficient_programme_skill_data():
    result = get_skill_alignment(
        "PRG0001",
        "CAR0003",
    )

    assert (
        result["status"]
        == "INSUFFICIENT_DATA"
    )

    assert (
        result["alignment_percentage"]
        is None
    )

    assert (
        result["programme_skill_count"]
        == 0
    )

    assert (
        result["shared_skills"]
        == []
    )

    assert (
        result[
            "additional_career_skills"
        ]
        == []
    )

    assert (
        "sufficient"
        in result[
            "explanation"
        ].lower()
    )