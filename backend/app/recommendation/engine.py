import csv
from pathlib import Path

from backend.app.eligibility.engine import (
    evaluate_programme,
)

from backend.app.progression.engine import (
    get_progression_pathways,
)


# ------------------------------------
# Data locations
# ------------------------------------

PROGRAMMES_PATH = Path(
    "data/reference/programmes.csv"
)

CAREERS_PATH = Path(
    "data/reference/careers.csv"
)

PROGRAMME_CAREERS_PATH = Path(
    "data/relationships/programme_careers.csv"
)

ENTRY_REQUIREMENTS_PATH = Path(
    "data/relationships/programme_entry_requirements.csv"
)


# ------------------------------------
# Load active programmes
# ------------------------------------

def load_active_programmes():

    programmes = []

    with PROGRAMMES_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            status = (
                row.get(
                    "programme_status",
                    "",
                )
                .strip()
                .lower()
            )

            if status == "active":
                programmes.append(row)

    return programmes


# ------------------------------------
# Load active careers
# ------------------------------------

def load_active_careers():

    careers = []

    with CAREERS_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            status = (
                row.get(
                    "active_status",
                    "",
                )
                .strip()
                .lower()
            )

            if status == "active":
                careers.append(row)

    return careers


# ------------------------------------
# Load programme-career relationships
# ------------------------------------

def load_programme_career_relationships():

    relationships = []

    with PROGRAMME_CAREERS_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            relationships.append(row)

    return relationships


# ------------------------------------
# Load programme entry requirements
# ------------------------------------

def load_programme_entry_requirements():

    requirements = []

    with ENTRY_REQUIREMENTS_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            requirements.append(row)

    return requirements


# ------------------------------------
# Detect education levels supplied
# by the learner
# ------------------------------------

def detect_student_education_levels(
    student_profile,
):
    """
    Determine which education levels are
    represented in the learner profile.

    Supported formats:

    Legacy flat A/L profile:

        {
            "Combined Mathematics": "B",
            "Physics": "C",
            "Chemistry": "C",
        }

    Multi-level profile:

        {
            "O_LEVEL": {...},
            "A_LEVEL": {...},
        }

    A flat legacy profile remains A_LEVEL
    for backward compatibility.
    """

    if not isinstance(
        student_profile,
        dict,
    ):
        return set()

    recognised_levels = {
        "O_LEVEL",
        "A_LEVEL",
    }

    supplied_levels = set()

    # ------------------------------------
    # Detect nested education-level data
    # ------------------------------------

    for level in recognised_levels:

        level_results = student_profile.get(
            level
        )

        if (
            isinstance(
                level_results,
                dict,
            )
            and level_results
        ):
            supplied_levels.add(
                level
            )

    # ------------------------------------
    # Legacy flat profile
    #
    # Existing WiseLanka behaviour treats
    # flat subject dictionaries as A/L.
    # ------------------------------------

    nested_format = any(
        key in recognised_levels
        for key in student_profile
    )

    if (
        student_profile
        and not nested_format
    ):
        supplied_levels.add(
            "A_LEVEL"
        )

    return supplied_levels


# ------------------------------------
# Get education levels required by
# a programme
# ------------------------------------

def get_programme_education_levels(
    programme_id,
    requirements=None,
):
    """
    Return the education levels used by a
    programme's entry requirements.

    Example:

        PRG0001 -> {"A_LEVEL"}
        PRG0004 -> {"O_LEVEL"}
    """

    if requirements is None:

        requirements = (
            load_programme_entry_requirements()
        )

    levels = set()

    for requirement in requirements:

        if (
            requirement.get(
                "programme_id",
                "",
            )
            != programme_id
        ):
            continue

        education_level = (
            requirement.get(
                "education_level",
                "",
            )
            .strip()
            .upper()
        )

        if education_level:
            levels.add(
                education_level
            )

    return levels


# ------------------------------------
# Check whether a programme is
# relevant to the supplied profile
# ------------------------------------

def programme_matches_student_level(
    programme_id,
    student_levels,
    requirements=None,
):
    """
    A programme should only be evaluated when
    the learner supplied at least one education
    level used by that programme's entry
    requirements.

    This prevents:

    - O/L learners receiving A/L degree
      programmes as immediate recommendations.

    - A/L learners receiving O/L-entry
      foundation programmes as though those
      were their primary current-level options.
    """

    programme_levels = (
        get_programme_education_levels(
            programme_id,
            requirements,
        )
    )

    # If a programme currently has no
    # structured entry requirements,
    # exclude it from eligibility-based
    # recommendation until evidence exists.
    if not programme_levels:
        return False

    return bool(
        programme_levels
        & student_levels
    )


# ------------------------------------
# Get careers related to a programme
# ------------------------------------

def get_programme_careers(
    programme_id,
):

    careers = load_active_careers()

    relationships = (
        load_programme_career_relationships()
    )

    career_lookup = {
        career["career_id"]: career
        for career in careers
    }

    career_pathways = []

    for relationship in relationships:

        if (
            relationship.get(
                "programme_id"
            )
            != programme_id
        ):
            continue

        career_id = relationship.get(
            "career_id",
            "",
        )

        career = career_lookup.get(
            career_id
        )

        if career is None:
            continue

        career_pathways.append(
            {
                "career_id":
                    career_id,

                "career_name":
                    career.get(
                        "career_name",
                        "",
                    ),

                "career_category":
                    career.get(
                        "career_category",
                        "",
                    ),

                "industry":
                    career.get(
                        "industry",
                        "",
                    ),

                "description":
                    career.get(
                        "description",
                        "",
                    ),

                "minimum_qualification_level":
                    career.get(
                        "minimum_qualification_level",
                        "",
                    ),

                "sri_lanka_demand":
                    career.get(
                        "sri_lanka_demand",
                        "",
                    ),

                "international_potential":
                    career.get(
                        "international_potential",
                        "",
                    ),

                "remote_work_potential":
                    career.get(
                        "remote_work_potential",
                        "",
                    ),

                "self_employment_potential":
                    career.get(
                        "self_employment_potential",
                        "",
                    ),

                "relevance_level":
                    relationship.get(
                        "relevance_level",
                        "",
                    ),

                "relationship_notes":
                    relationship.get(
                        "notes",
                        "",
                    ),
            }
        )

    # ------------------------------------
    # Put highly relevant careers first
    # ------------------------------------

    relevance_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    career_pathways.sort(
        key=lambda item:
            relevance_order.get(
                item["relevance_level"],
                99,
            )
    )

    return career_pathways


# ------------------------------------
# Evaluate student against relevant
# active programmes
# ------------------------------------

def evaluate_all_programmes(
    student_profile,
):

    programmes = load_active_programmes()

    requirements = (
        load_programme_entry_requirements()
    )

    student_levels = (
        detect_student_education_levels(
            student_profile
        )
    )

    results = []

    for programme in programmes:

        programme_id = programme[
            "programme_id"
        ]

        # ------------------------------------
        # Education-level filtering
        # ------------------------------------

        if not programme_matches_student_level(
            programme_id,
            student_levels,
            requirements,
        ):
            continue

        evaluation = evaluate_programme(
            programme_id,
            student_profile,
        )

        # ------------------------------------
        # Add programme metadata needed
        # by the recommendation layer
        # ------------------------------------

        evaluation["programme_name"] = (
            programme["programme_name"]
        )

        evaluation["field_of_study"] = (
            programme.get(
                "field_of_study",
                "",
            )
        )

        evaluation["application_url"] = (
            programme.get(
                "application_url",
                "",
            )
        )

        evaluation["programme_type"] = (
            programme.get(
                "programme_type",
                "",
            )
        )

        evaluation["duration_months"] = (
            programme.get(
                "duration_months",
                "",
            )
        )

        evaluation["study_mode"] = (
            programme.get(
                "study_mode",
                "",
            )
        )

        evaluation["delivery_mode"] = (
            programme.get(
                "delivery_mode",
                "",
            )
        )

        evaluation["campus"] = (
            programme.get(
                "campus",
                "",
            )
        )

        # ------------------------------------
        # Qualification metadata
        # ------------------------------------

        qualification_id = (
            programme.get(
                "qualification_id",
                "",
            )
            .strip()
        )

        evaluation["qualification_id"] = (
            qualification_id
        )

        # ------------------------------------
        # Academic progression intelligence
        #
        # Progression is qualification-based.
        #
        # Example:
        #
        # PRG0004
        #     ↓
        # QLF0004
        #     ↓
        # QLF0005 / QLF0006 / QLF0007
        # ------------------------------------

        if qualification_id:

            evaluation["progression"] = (
                get_progression_pathways(
                    qualification_id
                )
            )

        else:

            evaluation["progression"] = {
                "qualification_id":
                    None,

                "qualification_name":
                    None,

                "count":
                    0,

                "pathways":
                    [],
            }

        # ------------------------------------
        # Record programme entry level
        # ------------------------------------

        evaluation[
            "entry_education_levels"
        ] = sorted(
            get_programme_education_levels(
                programme_id,
                requirements,
            )
        )

        # ------------------------------------
        # Add career pathways
        # ------------------------------------

        evaluation["career_pathways"] = (
            get_programme_careers(
                programme_id
            )
        )

        results.append(
            evaluation
        )

    return results


# ------------------------------------
# Calculate programme match score
# ------------------------------------

def calculate_match_score(
    evaluation,
):
    """
    Calculate how closely the learner matches
    the programme's entry requirements.

    A fully passed requirement group receives
    100%.

    A failed group can receive partial credit
    when the learner has actually supplied a
    relevant subject but narrowly misses the
    required minimum grade.

    Missing relevant subjects do not receive
    partial credit.

    This prevents a learner with unrelated
    subjects from appearing nearly eligible
    simply because they satisfy a generic
    requirement such as three A/L passes.
    """

    groups = evaluation.get(
        "groups",
        [],
    )

    if not groups:
        return 0.0

    group_scores = []

    for group in groups:

        # ------------------------------------
        # Fully passed group
        # ------------------------------------

        if group.get(
            "passed",
            False,
        ):
            group_scores.append(
                100.0
            )
            continue

        requirements = group.get(
            "requirements",
            [],
        )

        if not requirements:
            group_scores.append(
                0.0
            )
            continue

        # ------------------------------------
        # Check whether this failed group
        # represents a genuine near match
        # ------------------------------------

        near_match_found = False

        for requirement in requirements:

            if requirement.get(
                "passed",
                False,
            ):
                continue

            message = (
                requirement.get(
                    "message",
                    "",
                )
                .strip()
                .lower()
            )

            # Genuine near match:
            #
            # A relevant subject was supplied,
            # but the learner missed the
            # minimum grade.
            #
            # Missing subjects receive no
            # partial credit.
            if (
                "minimum" in message
                and "was not provided"
                not in message
            ):
                near_match_found = True
                break

        if near_match_found:

            group_scores.append(
                50.0
            )

        else:

            group_scores.append(
                0.0
            )

    score = (
        sum(group_scores)
        / len(group_scores)
    )

    return round(
        score,
        1,
    )


# ------------------------------------
# Classify programme result
# ------------------------------------

def classify_programme(
    evaluation,
):

    score = calculate_match_score(
        evaluation
    )

    if evaluation["eligible"]:

        category = "ELIGIBLE"

    elif score >= 75:

        category = "NEARLY_ELIGIBLE"

    else:

        category = "NOT_ELIGIBLE"

    passed_requirements = []
    failed_requirements = []

    for group in evaluation.get(
        "groups",
        [],
    ):

        requirements = group.get(
            "requirements",
            [],
        )

        operator = (
            group.get(
                "operator",
                "AND",
            )
            .strip()
            .upper()
        )

        group_passed = group.get(
            "passed",
            False,
        )

        # ------------------------------------
        # Passed OR group
        # ------------------------------------

        if (
            operator == "OR"
            and group_passed
        ):

            for requirement in requirements:

                if requirement.get(
                    "passed",
                    False,
                ):

                    message = requirement.get(
                        "message",
                        "",
                    )

                    if message:
                        passed_requirements.append(
                            message
                        )

            continue

        # ------------------------------------
        # Failed OR group
        # ------------------------------------

        if (
            operator == "OR"
            and not group_passed
        ):

            for requirement in requirements:

                if not requirement.get(
                    "passed",
                    False,
                ):

                    message = requirement.get(
                        "message",
                        "",
                    )

                    if message:
                        failed_requirements.append(
                            message
                        )

            continue

        # ------------------------------------
        # AND groups
        # ------------------------------------

        for requirement in requirements:

            message = requirement.get(
                "message",
                "",
            )

            if requirement.get(
                "passed",
                False,
            ):

                if message:
                    passed_requirements.append(
                        message
                    )

            else:

                if message:
                    failed_requirements.append(
                        message
                    )

    return {
        "programme_id":
            evaluation["programme_id"],

        "programme_name":
            evaluation.get(
                "programme_name",
                evaluation["programme_id"],
            ),

        "field_of_study":
            evaluation.get(
                "field_of_study",
                "",
            ),

        "programme_type":
            evaluation.get(
                "programme_type",
                "",
            ),

        "duration_months":
            evaluation.get(
                "duration_months",
                "",
            ),

        "study_mode":
            evaluation.get(
                "study_mode",
                "",
            ),

        "delivery_mode":
            evaluation.get(
                "delivery_mode",
                "",
            ),

        "campus":
            evaluation.get(
                "campus",
                "",
            ),

        "application_url":
            evaluation.get(
                "application_url",
                "",
            ),

        # ------------------------------------
        # Qualification information
        # ------------------------------------

        "qualification_id":
            evaluation.get(
                "qualification_id",
                "",
            ),

        "entry_education_levels":
            evaluation.get(
                "entry_education_levels",
                [],
            ),

        # ------------------------------------
        # Eligibility result
        # ------------------------------------

        "eligible":
            evaluation["eligible"],

        "category":
            category,

        "match_score":
            score,

        "passed_requirements":
            passed_requirements,

        "failed_requirements":
            failed_requirements,

        # ------------------------------------
        # Career intelligence
        # ------------------------------------

        "career_pathways":
            evaluation.get(
                "career_pathways",
                [],
            ),

        # ------------------------------------
        # Academic progression intelligence
        # ------------------------------------

        "progression":
            evaluation.get(
                "progression",
                {
                    "qualification_id":
                        None,

                    "qualification_name":
                        None,

                    "count":
                        0,

                    "pathways":
                        [],
                },
            ),

        # ------------------------------------
        # Technical eligibility evidence
        # ------------------------------------

        "groups":
            evaluation["groups"],
    }


# ------------------------------------
# Generate programme recommendations
# ------------------------------------

def recommend_programmes(
    student_profile,
):

    evaluations = evaluate_all_programmes(
        student_profile
    )

    recommendations = []

    for evaluation in evaluations:

        recommendation = (
            classify_programme(
                evaluation
            )
        )

        recommendations.append(
            recommendation
        )

    recommendations.sort(
        key=lambda item:
            item["match_score"],
        reverse=True,
    )

    return recommendations