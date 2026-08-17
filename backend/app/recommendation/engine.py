import csv
from pathlib import Path

from backend.app.eligibility.engine import (
    evaluate_programme,
)


# ------------------------------------
# Data location
# ------------------------------------

PROGRAMMES_PATH = Path(
    "data/reference/programmes.csv"
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
# Evaluate student against
# every active programme
# ------------------------------------

def evaluate_all_programmes(
    student_profile,
):

    programmes = load_active_programmes()

    results = []

    for programme in programmes:

        programme_id = programme[
            "programme_id"
        ]

        evaluation = evaluate_programme(
            programme_id,
            student_profile,
        )

        # Add programme metadata needed
        # by the recommendation layer.
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
            # Example:
            # Combined Mathematics: S
            # (minimum C)
            #
            # Missing subjects such as:
            # "Physics was not provided"
            # do not receive partial credit.
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
        #
        # Only show the alternatives that
        # actually satisfied the group.
        #
        # Other unused alternatives should
        # not be reported as learner failures.
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
        #
        # No alternative satisfied the group,
        # so the failed alternatives are
        # useful for explaining what is
        # missing.
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