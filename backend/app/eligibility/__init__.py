from collections import defaultdict

from backend.app.data_loader import load_csv


GRADE_ORDER = {
    "A": 4,
    "B": 3,
    "C": 2,
    "S": 1,
    "F": 0,
}


def grade_meets_minimum(student_grade, minimum_grade):
    student_value = GRADE_ORDER.get(student_grade.upper(), -1)
    minimum_value = GRADE_ORDER.get(minimum_grade.upper(), -1)

    return student_value >= minimum_value


def evaluate_requirement(requirement, student_results):
    requirement_type = requirement["requirement_type"]

    if requirement_type == "A_LEVEL_PASS":
        minimum_count = int(requirement["minimum_count"])

        passed_subjects = sum(
            1
            for grade in student_results.values()
            if GRADE_ORDER.get(grade.upper(), 0) >= GRADE_ORDER["S"]
        )

        passed = passed_subjects >= minimum_count

        return {
            "requirement_id": requirement["requirement_id"],
            "passed": passed,
            "message": (
                f"Passed {passed_subjects} A/L subjects "
                f"(minimum required: {minimum_count})"
            ),
        }

    if requirement_type == "SUBJECT_GRADE":
        subject = requirement["subject_name"]
        minimum_grade = requirement["minimum_grade"]

        student_grade = student_results.get(subject)

        if student_grade is None:
            return {
                "requirement_id": requirement["requirement_id"],
                "passed": False,
                "message": f"{subject}: subject not provided",
            }

        passed = grade_meets_minimum(student_grade, minimum_grade)

        return {
            "requirement_id": requirement["requirement_id"],
            "passed": passed,
            "message": (
                f"{subject}: student grade {student_grade}, "
                f"minimum required {minimum_grade}"
            ),
        }

    return {
        "requirement_id": requirement["requirement_id"],
        "passed": False,
        "message": f"Unsupported requirement type: {requirement_type}",
    }


def evaluate_programme(programme_id, student_results):
    requirements = load_csv(
        "relationships/programme_entry_requirements.csv"
    )

    programme_requirements = [
        requirement
        for requirement in requirements
        if requirement["programme_id"] == programme_id
    ]

    grouped_requirements = defaultdict(list)

    for requirement in programme_requirements:
        grouped_requirements[
            requirement["requirement_group_id"]
        ].append(requirement)

    group_results = []

    for group_id, group_items in grouped_requirements.items():
        operator = group_items[0]["group_operator"]

        item_results = [
            evaluate_requirement(item, student_results)
            for item in group_items
        ]

        if operator == "OR":
            group_passed = any(
                result["passed"]
                for result in item_results
            )
        else:
            group_passed = all(
                result["passed"]
                for result in item_results
            )

        group_results.append(
            {
                "group_id": group_id,
                "operator": operator,
                "passed": group_passed,
                "requirements": item_results,
            }
        )

    eligible = all(
        group["passed"]
        for group in group_results
    )

    return {
        "programme_id": programme_id,
        "eligible": eligible,
        "groups": group_results,
    }