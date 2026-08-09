from collections import defaultdict

from backend.app.data_loader import load_csv


GRADE_RANK = {
    "F": 0,
    "S": 1,
    "C": 2,
    "B": 3,
    "A": 4,
}


def grade_meets_minimum(student_grade, minimum_grade):
    """
    Check whether a student's grade meets
    or exceeds the required minimum grade.
    """

    student_grade = student_grade.strip().upper()
    minimum_grade = minimum_grade.strip().upper()

    if student_grade not in GRADE_RANK:
        return False

    if minimum_grade not in GRADE_RANK:
        return False

    return (
        GRADE_RANK[student_grade]
        >= GRADE_RANK[minimum_grade]
    )


def evaluate_requirement(
    requirement,
    student_results,
):
    """
    Evaluate one entry requirement.
    """

    requirement_type = requirement[
        "requirement_type"
    ]

    # ------------------------------------
    # Requirement:
    # Pass a minimum number of A/L subjects
    # ------------------------------------

    if requirement_type == "A_LEVEL_PASS":

        minimum_count = int(
            requirement["minimum_count"]
        )

        passed_subjects = sum(
            1
            for grade in student_results.values()
            if grade.strip().upper()
            in {"A", "B", "C", "S"}
        )

        passed = (
            passed_subjects >= minimum_count
        )

        return {
            "requirement_id":
                requirement["requirement_id"],

            "passed":
                passed,

            "message":
                (
                    f"{passed_subjects} A/L subjects "
                    f"passed; {minimum_count} required"
                ),
        }

    # ------------------------------------
    # Requirement:
    # Specific subject minimum grade
    # ------------------------------------

    if requirement_type == "SUBJECT_GRADE":

        subject = requirement["subject_name"]

        minimum_grade = requirement[
            "minimum_grade"
        ]

        student_grade = student_results.get(
            subject
        )

        if student_grade is None:

            return {
                "requirement_id":
                    requirement[
                        "requirement_id"
                    ],

                "passed":
                    False,

                "message":
                    f"{subject} was not provided",
            }

        passed = grade_meets_minimum(
            student_grade,
            minimum_grade,
        )

        return {
            "requirement_id":
                requirement["requirement_id"],

            "passed":
                passed,

            "message":
                (
                    f"{subject}: {student_grade} "
                    f"(minimum {minimum_grade})"
                ),
        }

    # ------------------------------------
    # Unknown rule type
    # ------------------------------------

    return {
        "requirement_id":
            requirement["requirement_id"],

        "passed":
            False,

        "message":
            (
                "Unsupported requirement type: "
                f"{requirement_type}"
            ),
    }


def evaluate_programme(
    programme_id,
    student_results,
):
    """
    Evaluate whether a learner satisfies
    the entry requirements of a programme.
    """

    requirements = load_csv(
        "relationships/"
        "programme_entry_requirements.csv"
    )

    programme_requirements = [
        requirement
        for requirement in requirements
        if requirement["programme_id"]
        == programme_id
    ]

    if not programme_requirements:

        return {
            "programme_id":
                programme_id,

            "eligible":
                False,

            "groups":
                [],

            "message":
                (
                    "No entry requirements "
                    "were found for this programme."
                ),
        }

    # ------------------------------------
    # Group requirements
    # ------------------------------------

    grouped_requirements = defaultdict(list)

    for requirement in programme_requirements:

        group_id = requirement[
            "requirement_group_id"
        ]

        grouped_requirements[
            group_id
        ].append(requirement)

    group_results = []

    # ------------------------------------
    # Evaluate each logical group
    # ------------------------------------

    for (
        group_id,
        requirements_in_group,
    ) in grouped_requirements.items():

        operator = (
            requirements_in_group[0][
                "group_operator"
            ]
            .strip()
            .upper()
        )

        evaluated_requirements = [
            evaluate_requirement(
                requirement,
                student_results,
            )
            for requirement
            in requirements_in_group
        ]

        if operator == "OR":

            group_passed = any(
                item["passed"]
                for item
                in evaluated_requirements
            )

        elif operator == "AND":

            group_passed = all(
                item["passed"]
                for item
                in evaluated_requirements
            )

        else:

            group_passed = False

        group_results.append(
            {
                "group_id":
                    group_id,

                "operator":
                    operator,

                "passed":
                    group_passed,

                "requirements":
                    evaluated_requirements,
            }
        )

    # ------------------------------------
    # Programme eligibility
    # ------------------------------------

    eligible = (
        len(group_results) > 0
        and all(
            group["passed"]
            for group in group_results
        )
    )

    return {
        "programme_id":
            programme_id,

        "eligible":
            eligible,

        "groups":
            group_results,
    }