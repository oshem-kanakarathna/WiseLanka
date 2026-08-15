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

    groups = evaluation.get(
        "groups",
        [],
    )

    if not groups:
        return 0.0

    group_scores = []

    for group in groups:

        requirements = group.get(
            "requirements",
            [],
        )

        if not requirements:
            group_scores.append(0.0)
            continue

        operator = (
            group.get(
                "operator",
                "AND",
            )
            .strip()
            .upper()
        )

        if operator == "OR":

            group_score = (
                100.0
                if any(
                    requirement.get(
                        "passed",
                        False,
                    )
                    for requirement
                    in requirements
                )
                else 0.0
            )

        else:

            passed_count = sum(
                1
                for requirement
                in requirements
                if requirement.get(
                    "passed",
                    False,
                )
            )

            group_score = (
                passed_count
                / len(requirements)
            ) * 100

        group_scores.append(
            group_score
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

    elif score >= 50:

        category = "NEARLY_ELIGIBLE"

    else:

        category = "NOT_ELIGIBLE"

    passed_requirements = []
    failed_requirements = []

    for group in evaluation.get(
        "groups",
        [],
    ):

        for requirement in group.get(
            "requirements",
            [],
        ):

            message = requirement.get(
                "message",
                "",
            )

            if requirement.get(
                "passed"
            ):
                passed_requirements.append(
                    message
                )

            else:
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