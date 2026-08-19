from backend.app.recommendation.engine import (
    recommend_programmes,
)


def get_result_by_programme(
    results,
    programme_id,
):
    for result in results:
        if result["programme_id"] == programme_id:
            return result

    raise AssertionError(
        f"Programme {programme_id} not found"
    )


# --------------------------------------------------
# Strong profile
# --------------------------------------------------

def test_strong_profile_is_eligible():

    profile = {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    for programme_id in [
        "PRG0001",
        "PRG0002",
        "PRG0003",
    ]:

        result = get_result_by_programme(
            results,
            programme_id,
        )

        assert result["eligible"] is True

        assert (
            result["category"]
            == "ELIGIBLE"
        )

        assert (
            result["match_score"]
            == 100.0
        )


# --------------------------------------------------
# Near profile
# --------------------------------------------------

def test_near_profile_is_nearly_eligible():

    profile = {
        "Combined Mathematics": "S",
        "Physics": "S",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    for programme_id in [
        "PRG0001",
        "PRG0002",
        "PRG0003",
    ]:

        result = get_result_by_programme(
            results,
            programme_id,
        )

        assert result["eligible"] is False

        assert (
            result["category"]
            == "NEARLY_ELIGIBLE"
        )

        assert (
            result["match_score"]
            == 75.0
        )


# --------------------------------------------------
# Unrelated profile
# --------------------------------------------------

def test_unrelated_profile_not_nearly_eligible():

    profile = {
        "Sinhala": "A",
        "Art": "B",
        "Geography": "C",
    }

    results = recommend_programmes(
        profile
    )

    result_1 = get_result_by_programme(
        results,
        "PRG0001",
    )

    result_2 = get_result_by_programme(
        results,
        "PRG0002",
    )

    result_3 = get_result_by_programme(
        results,
        "PRG0003",
    )

    assert (
        result_1["category"]
        == "NOT_ELIGIBLE"
    )

    assert (
        result_1["match_score"]
        == 50.0
    )

    assert (
        result_2["category"]
        == "NOT_ELIGIBLE"
    )

    assert (
        result_2["match_score"]
        == 0.0
    )

    assert (
        result_3["category"]
        == "NOT_ELIGIBLE"
    )

    assert (
        result_3["match_score"]
        == 0.0
    )


# --------------------------------------------------
# Passed OR groups should not create
# false failed requirements
# --------------------------------------------------

def test_eligible_programme_has_no_false_failed_or_requirements():

    profile = {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    for result in results:

        assert result["eligible"] is True

        assert (
            result["failed_requirements"]
            == []
        )


# --------------------------------------------------
# Near profile should retain useful
# failure explanations
# --------------------------------------------------

def test_near_profile_keeps_useful_failed_requirements():

    profile = {
        "Combined Mathematics": "S",
        "Physics": "S",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    for result in results:

        assert (
            result["category"]
            == "NEARLY_ELIGIBLE"
        )

        assert (
            len(
                result[
                    "failed_requirements"
                ]
            )
            > 0
        )

        # ------------------------------------
# Career pathway integration tests
# ------------------------------------

def test_recommendations_include_career_pathways():

    profile = {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    assert len(results) > 0

    for result in results:

        assert "career_pathways" in result

        careers = result[
            "career_pathways"
        ]

        assert isinstance(
            careers,
            list,
        )

        assert len(careers) > 0


def test_embedded_career_pathways_have_required_fields():

    profile = {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    required_fields = {
        "career_id",
        "career_name",
        "relevance_level",
    }

    for result in results:

        for career in result[
            "career_pathways"
        ]:

            assert required_fields.issubset(
                career.keys()
            )


def test_career_pathways_are_ordered_by_relevance():

    profile = {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    relevance_rank = {
        "High": 3,
        "Medium": 2,
        "Low": 1,
    }

    for result in results:

        careers = result[
            "career_pathways"
        ]

        ranks = [
            relevance_rank[
                career["relevance_level"]
            ]
            for career in careers
        ]

        assert ranks == sorted(
            ranks,
            reverse=True,
        )

        # ----------------------------------------
# Education-level-aware recommendations
# ----------------------------------------


def test_ol_profile_only_returns_ol_entry_programmes():

    profile = {
        "O_LEVEL": {
            "Mathematics": "A",
            "English": "B",
            "Science": "C",
            "ICT": "A",
            "Sinhala": "S",
            "History": "S",
        }
    }

    results = recommend_programmes(
        profile
    )

    programme_ids = {
        result["programme_id"]
        for result in results
    }

    assert programme_ids == {
        "PRG0004"
    }


def test_ol_foundation_profile_is_eligible():

    profile = {
        "O_LEVEL": {
            "Mathematics": "A",
            "English": "B",
            "Science": "C",
            "ICT": "A",
            "Sinhala": "S",
            "History": "S",
        }
    }

    results = recommend_programmes(
        profile
    )

    assert len(results) == 1

    result = results[0]

    assert (
        result["programme_id"]
        == "PRG0004"
    )

    assert result["eligible"] is True

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
        == ["O_LEVEL"]
    )

    assert (
        result["failed_requirements"]
        == []
    )


def test_legacy_al_profile_excludes_ol_foundation():

    profile = {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }

    results = recommend_programmes(
        profile
    )

    programme_ids = {
        result["programme_id"]
        for result in results
    }

    assert "PRG0004" not in programme_ids

    assert programme_ids == {
        "PRG0001",
        "PRG0002",
        "PRG0003",
    }


def test_nested_al_profile_excludes_ol_foundation():

    profile = {
        "A_LEVEL": {
            "Combined Mathematics": "B",
            "Physics": "C",
            "Chemistry": "C",
        }
    }

    results = recommend_programmes(
        profile
    )

    programme_ids = {
        result["programme_id"]
        for result in results
    }

    assert "PRG0004" not in programme_ids

    assert programme_ids == {
        "PRG0001",
        "PRG0002",
        "PRG0003",
    }

def test_ol_foundation_recommendation_contains_progression():

    profile = {
        "O_LEVEL": {
            "Mathematics": "A",
            "English": "B",
            "Science": "C",
            "ICT": "A",
            "Sinhala": "S",
            "History": "S",
        }
    }

    recommendations = recommend_programmes(
        profile
    )

    foundation = next(
        item
        for item in recommendations
        if item["programme_id"]
        == "PRG0004"
    )

    assert (
        foundation["qualification_id"]
        == "QLF0004"
    )

    assert (
        foundation["progression"]["count"]
        == 3
    )

    destinations = {
        pathway["to_qualification_id"]
        for pathway
        in foundation[
            "progression"
        ]["pathways"]
    }

    assert destinations == {
        "QLF0005",
        "QLF0006",
        "QLF0007",
    }


def test_foundation_progression_contains_destination_programmes():

    profile = {
        "O_LEVEL": {
            "Mathematics": "A",
            "English": "B",
            "Science": "C",
            "ICT": "A",
            "Sinhala": "S",
            "History": "S",
        }
    }

    recommendations = recommend_programmes(
        profile
    )

    foundation = next(
        item
        for item in recommendations
        if item["programme_id"]
        == "PRG0004"
    )

    destination_programmes = set()

    for pathway in (
        foundation[
            "progression"
        ]["pathways"]
    ):

        for programme in pathway[
            "programmes"
        ]:

            destination_programmes.add(
                programme["programme_id"]
            )

    assert destination_programmes == {
        "PRG0005",
        "PRG0006",
        "PRG0007",
    }


def test_degree_recommendation_can_have_empty_progression():

    profile = {
        "Combined Mathematics": "B",
        "Physics": "C",
        "Chemistry": "C",
    }

    recommendations = recommend_programmes(
        profile
    )

    programme = next(
        item
        for item in recommendations
        if item["programme_id"]
        == "PRG0001"
    )

    assert programme["qualification_id"]

    assert (
        programme["progression"]["count"]
        == 0
    )

    assert (
        programme["progression"]["pathways"]
        == []
    )