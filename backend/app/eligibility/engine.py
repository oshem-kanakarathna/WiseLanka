from collections import defaultdict

from backend.app.data_loader import load_csv


# --------------------------------------------------
# Grade ranking
#
# Higher number = stronger grade
# --------------------------------------------------

GRADE_RANK = {
    "F": 0,
    "S": 1,
    "C": 2,
    "B": 3,
    "A": 4,
}


def grade_meets_minimum(
    student_grade,
    minimum_grade,
):
    """
    Check whether a student's grade meets
    or exceeds the required minimum grade.
    """

    if student_grade is None:
        return False

    if minimum_grade is None:
        return False

    student_grade = (
        str(student_grade)
        .strip()
        .upper()
    )

    minimum_grade = (
        str(minimum_grade)
        .strip()
        .upper()
    )

    if student_grade not in GRADE_RANK:
        return False

    if minimum_grade not in GRADE_RANK:
        return False

    return (
        GRADE_RANK[student_grade]
        >= GRADE_RANK[minimum_grade]
    )


def get_results_for_level(
    student_results,
    education_level,
):
    """
    Return student results for a specific
    education level.

    Supports BOTH:

    Old flat format:
    {
        "Combined Mathematics": "B",
        "Physics": "C"
    }

    and new level-aware format:
    {
        "A_LEVEL": {
            "Combined Mathematics": "B",
            "Physics": "C"
        },
        "O_LEVEL": {
            "English": "B",
            "Mathematics": "A"
        }
    }

    Flat legacy input is treated as A_LEVEL
    so existing A/L recommendation behaviour
    remains backward compatible.
    """

    education_level = (
        str(education_level or "A_LEVEL")
        .strip()
        .upper()
    )

    if not isinstance(
        student_results,
        dict,
    ):
        return {}

    # Detect new nested profile format.
    nested_format = any(
        isinstance(value, dict)
        for value in student_results.values()
    )

    if nested_format:

        level_results = student_results.get(
            education_level,
            {},
        )

        if isinstance(
            level_results,
            dict,
        ):
            return level_results

        return {}

    # Backward compatibility:
    # old flat format represents A/L results.
    if education_level == "A_LEVEL":
        return student_results

    return {}


def evaluate_requirement(
    requirement,
    student_results,
):
    """
    Evaluate one programme entry requirement.

    Supported requirement types:

    - A_LEVEL_PASS
    - SUBJECT_GRADE
    - SUBJECT_SET_COUNT
    - O_LEVEL_PASS_COUNT
    - O_LEVEL_CREDIT_COUNT
    - O_LEVEL_SUBJECT_CREDIT

    The requirement's education_level determines
    which section of the learner profile is used.
    """

    requirement_type = (
        requirement["requirement_type"]
        .strip()
        .upper()
    )

    education_level = (
        requirement.get(
            "education_level",
            "A_LEVEL",
        )
        .strip()
        .upper()
    )

    level_results = get_results_for_level(
        student_results,
        education_level,
    )

    # --------------------------------------------------
    # Requirement type:
    # A_LEVEL_PASS
    #
    # Example:
    # At least 3 A/L subjects must be passed.
    # --------------------------------------------------

    if requirement_type == "A_LEVEL_PASS":

        minimum_count = int(
            requirement["minimum_count"]
        )

        passed_subjects = 0

        for grade in level_results.values():

            if grade_meets_minimum(
                grade,
                "S",
            ):
                passed_subjects += 1

        passed = (
            passed_subjects
            >= minimum_count
        )

        return {
            "requirement_id":
                requirement["requirement_id"],

            "passed":
                passed,

            "message":
                (
                    f"{passed_subjects} A/L subjects passed; "
                    f"{minimum_count} required"
                ),
        }

    # --------------------------------------------------
    # Requirement type:
    # SUBJECT_GRADE
    #
    # Generic subject-grade evaluator.
    # Works for A/L or O/L depending on
    # education_level in the requirement row.
    # --------------------------------------------------

    if requirement_type == "SUBJECT_GRADE":

        subject = (
            requirement["subject_name"]
            .strip()
        )

        minimum_grade = (
            requirement["minimum_grade"]
            .strip()
            .upper()
        )

        student_grade = level_results.get(
            subject
        )

        if student_grade is None:

            return {
                "requirement_id":
                    requirement["requirement_id"],

                "passed":
                    False,

                "message":
                    (
                        f"{education_level} "
                        f"{subject} was not provided"
                    ),
            }

        student_grade = (
            str(student_grade)
            .strip()
            .upper()
        )

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
                    f"{education_level} {subject}: "
                    f"{student_grade} "
                    f"(minimum {minimum_grade})"
                ),
        }

    # --------------------------------------------------
    # Requirement type:
    # SUBJECT_SET_COUNT
    #
    # Example:
    # At least 2 subjects from an approved set
    # must have grade C or above.
    # --------------------------------------------------

    if requirement_type == "SUBJECT_SET_COUNT":

        approved_subjects = [
            subject.strip()
            for subject
            in requirement[
                "subject_name"
            ].split("|")
            if subject.strip()
        ]

        minimum_grade = (
            requirement["minimum_grade"]
            .strip()
            .upper()
        )

        minimum_count = int(
            requirement["minimum_count"]
        )

        matched_subjects = []

        for subject in approved_subjects:

            student_grade = level_results.get(
                subject
            )

            if student_grade is None:
                continue

            student_grade = (
                str(student_grade)
                .strip()
                .upper()
            )

            if grade_meets_minimum(
                student_grade,
                minimum_grade,
            ):
                matched_subjects.append(
                    {
                        "subject":
                            subject,

                        "grade":
                            student_grade,
                    }
                )

        passed = (
            len(matched_subjects)
            >= minimum_count
        )

        matched_text = ", ".join(
            (
                f"{item['subject']}: "
                f"{item['grade']}"
            )
            for item
            in matched_subjects
        )

        if not matched_text:
            matched_text = "None"

        return {
            "requirement_id":
                requirement["requirement_id"],

            "passed":
                passed,

            "message":
                (
                    f"{len(matched_subjects)} approved "
                    f"{education_level} subjects met grade "
                    f"{minimum_grade} or above; "
                    f"{minimum_count} required. "
                    f"Matched: {matched_text}"
                ),
        }

    # --------------------------------------------------
    # Requirement type:
    # O_LEVEL_PASS_COUNT
    #
    # Example:
    # At least 6 O/L subjects must be passed.
    #
    # S or above is treated as a pass.
    # --------------------------------------------------

    if requirement_type == "O_LEVEL_PASS_COUNT":

        minimum_count = int(
            requirement["minimum_count"]
        )

        passed_subjects = 0

        for grade in level_results.values():

            if grade_meets_minimum(
                grade,
                "S",
            ):
                passed_subjects += 1

        passed = (
            passed_subjects
            >= minimum_count
        )

        return {
            "requirement_id":
                requirement["requirement_id"],

            "passed":
                passed,

            "message":
                (
                    f"{passed_subjects} O/L subjects passed; "
                    f"{minimum_count} required"
                ),
        }

    # --------------------------------------------------
    # Requirement type:
    # O_LEVEL_CREDIT_COUNT
    #
    # Example:
    # At least 3 O/L subjects must have
    # credit passes.
    #
    # C or above is treated as a credit.
    # --------------------------------------------------

    if requirement_type == "O_LEVEL_CREDIT_COUNT":

        minimum_count = int(
            requirement["minimum_count"]
        )

        credit_subjects = []

        for (
            subject,
            grade,
        ) in level_results.items():

            if grade_meets_minimum(
                grade,
                "C",
            ):

                credit_subjects.append(
                    {
                        "subject":
                            subject,

                        "grade":
                            str(grade)
                            .strip()
                            .upper(),
                    }
                )

        passed = (
            len(credit_subjects)
            >= minimum_count
        )

        credit_text = ", ".join(
            (
                f"{item['subject']}: "
                f"{item['grade']}"
            )
            for item
            in credit_subjects
        )

        if not credit_text:
            credit_text = "None"

        return {
            "requirement_id":
                requirement["requirement_id"],

            "passed":
                passed,

            "message":
                (
                    f"{len(credit_subjects)} O/L subjects "
                    f"have credit passes; "
                    f"{minimum_count} required. "
                    f"Credits: {credit_text}"
                ),
        }

    # --------------------------------------------------
    # Requirement type:
    # O_LEVEL_SUBJECT_CREDIT
    #
    # Example:
    # Mathematics must have a credit pass
    # of C or above.
    # --------------------------------------------------

    if requirement_type == "O_LEVEL_SUBJECT_CREDIT":

        subject = (
            requirement["subject_name"]
            .strip()
        )

        student_grade = level_results.get(
            subject
        )

        if student_grade is None:

            return {
                "requirement_id":
                    requirement["requirement_id"],

                "passed":
                    False,

                "message":
                    (
                        f"O_LEVEL {subject} "
                        "was not provided"
                    ),
            }

        student_grade = (
            str(student_grade)
            .strip()
            .upper()
        )

        passed = grade_meets_minimum(
            student_grade,
            "C",
        )

        return {
            "requirement_id":
                requirement["requirement_id"],

            "passed":
                passed,

            "message":
                (
                    f"O_LEVEL {subject}: "
                    f"{student_grade} "
                    "(credit pass C or above required)"
                ),
        }

    # --------------------------------------------------
    # Unsupported requirement type
    # --------------------------------------------------

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
    all recorded entry requirement groups
    for a programme.

    Rules inside a group use that group's
    AND / OR operator.

    Every requirement group must pass for
    the programme to be eligible.
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

    # --------------------------------------------------
    # No requirements found
    # --------------------------------------------------

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
                    "No entry requirements were "
                    "found for this programme."
                ),
        }

    # --------------------------------------------------
    # Group requirements
    # --------------------------------------------------

    grouped_requirements = defaultdict(
        list
    )

    for requirement in programme_requirements:

        group_id = (
            requirement[
                "requirement_group_id"
            ]
            .strip()
        )

        grouped_requirements[
            group_id
        ].append(requirement)

    group_results = []

    # --------------------------------------------------
    # Evaluate each requirement group
    # --------------------------------------------------

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

        if operator == "AND":

            group_passed = all(
                item["passed"]
                for item
                in evaluated_requirements
            )

        elif operator == "OR":

            group_passed = any(
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

    # --------------------------------------------------
    # Overall programme eligibility
    # --------------------------------------------------

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