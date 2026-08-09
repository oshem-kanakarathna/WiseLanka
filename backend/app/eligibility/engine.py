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
    student_grade = student_grade.strip().upper()
    minimum_grade = minimum_grade.strip().upper()

    return (
        student_grade in GRADE_RANK
        and minimum_grade in GRADE_RANK
        and GRADE_RANK[student_grade] >= GRADE_RANK[minimum_grade]
    )


def evaluate_requirement(requirement, student_results):

    requirement_type = requirement["requirement_type"]

    if requirement_type == "A_LEVEL_PASS":

        minimum_count = int(requirement["minimum_count"])

        passed_subjects = sum(
            1
            for grade in student_results.values()
            if grade.strip().upper() in {"A", "B", "C", "S"}
        )

        passed = passed_subjects >= minimum_count

        return {
            "requirement_id": requirement["requirement_id"],
            "passed": passed,
            "message": (
                f"{passed_subjects} A/L subjects passed; "
                f"{minimum_count} required"
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
                "message": f"{subject} was not provided",
            }

        passed = grade_meets_minimum(
            student_grade,
            minimum_grade,
        )

        return {
            "requirement_id": requirement["requirement_id"],
            "passed": passed,
            "message": (
                f"{subject}: {student_grade} "
                f"(minimum {minimum_grade})"
            ),
        }

    return {
        "requirement_id": requirement["requirement_id"],
        "passed": False,
        "message": "Unsupported requirement type",
    }


def evaluate_programme(programme_id, student_results):

    requirements = load_csv(
        "relationships/programme_entry_requirements.csv"
    )

    programme_requirements = [
        row
        for row in requirements
        if row["programme_id"] == programme_id
    ]

    grouped = defaultdict(list)

    for requirement in programme_requirements:
        group_id = requirement["requirement_group_id"]
        grouped[group_id].append(requirement)

    group_results = []

    for group_id, requirements_in_group in grouped.items():

        operator = requirements_in_group[0]["group_operator"].upper()

        evaluated = [
            evaluate_requirement(requirement, student_results)
            for requirement in requirements_in_group
        ]

        if operator == "OR":
            passed = any(item["passed"] for item in evaluated)
        else:
            passed = all(item["passed"] for item in evaluated)

        group_results.append(
            {
                "group_id": group_id,
                "operator": operator,
                "passed": passed,
                "requirements": evaluated,
            }
        )

    eligible = (
        len(group_results) > 0
        and all(group["passed"] for group in group_results)
    )

    return {
        "programme_id": programme_id,
        "eligible": eligible,
        "groups": group_results,
    }