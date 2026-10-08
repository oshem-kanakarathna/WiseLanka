from typing import Any, Dict, List, Optional

from backend.app.data_loader import load_csv


GRADE_ORDER = {
    "F": 0,
    "S": 1,
    "C": 2,
    "B": 3,
    "A": 4,
}


def _normalise(value: Any) -> str:
    """Convert a value into a clean lowercase string for comparison."""
    if value is None:
        return ""

    return str(value).strip().lower()


def _to_number(value: Any) -> Optional[float]:
    """Convert a value to a number when possible."""
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_boolean(value: Any) -> Optional[bool]:
    """Convert common boolean representations to True or False."""
    if isinstance(value, bool):
        return value

    normalised = _normalise(value)

    if normalised in {"true", "yes", "1"}:
        return True

    if normalised in {"false", "no", "0"}:
        return False

    return None


def _grade_at_least(
    actual_grade: Any,
    required_grade: Any,
) -> Optional[bool]:
    """Check whether an examination grade meets a minimum grade."""

    actual = str(actual_grade).strip().upper()
    required = str(required_grade).strip().upper()

    if actual not in GRADE_ORDER or required not in GRADE_ORDER:
        return None

    return GRADE_ORDER[actual] >= GRADE_ORDER[required]


def _evaluate_requirement(
    requirement: Dict[str, str],
    learner_profile: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate one scholarship eligibility requirement."""

    field_name = requirement.get("field_name", "").strip()
    operator = requirement.get("operator", "").strip().upper()
    required_value = requirement.get("required_value", "").strip()
    minimum_value = requirement.get("minimum_value", "").strip()

    actual_value = learner_profile.get(field_name)

    result = {
        "requirement_id": requirement.get("requirement_id"),
        "requirement_type": requirement.get("requirement_type"),
        "field_name": field_name,
        "description": requirement.get("description"),
        "mandatory": _normalise(requirement.get("mandatory")) == "true",
        "source_id": requirement.get("source_id"),
        "actual_value": actual_value,
        "status": "UNKNOWN",
    }

    # Missing learner information is UNKNOWN, not FAILED.
    if actual_value is None or actual_value == "":
        return result

    if operator == "EQUALS":
        required_boolean = _to_boolean(required_value)
        actual_boolean = _to_boolean(actual_value)

        if required_boolean is not None and actual_boolean is not None:
            passed = actual_boolean == required_boolean
        else:
            passed = (
                _normalise(actual_value)
                == _normalise(required_value)
            )

    elif operator == "GREATER_THAN":
        actual_number = _to_number(actual_value)
        required_number = _to_number(required_value)

        if actual_number is None or required_number is None:
            return result

        passed = actual_number > required_number

    elif operator == "GREATER_THAN_OR_EQUAL":
        actual_number = _to_number(actual_value)

        comparison_value = (
            minimum_value
            if minimum_value != ""
            else required_value
        )

        required_number = _to_number(comparison_value)

        if actual_number is None or required_number is None:
            return result

        passed = actual_number >= required_number

    elif operator == "GRADE_AT_LEAST":
        grade_result = _grade_at_least(
            actual_value,
            required_value,
        )

        if grade_result is None:
            return result

        passed = grade_result

    else:
        # Unknown operators remain UNKNOWN rather than being
        # incorrectly treated as failures.
        return result

    result["status"] = "PASSED" if passed else "FAILED"

    return result


def _get_applicable_fields(
    scholarship_id: str,
    applicability_rows: List[Dict[str, str]],
) -> List[str]:
    """Return fields of study associated with a scholarship."""

    fields = []

    for row in applicability_rows:
        if row.get("scholarship_id") != scholarship_id:
            continue

        if (
            row.get("target_type", "").strip().upper()
            != "FIELD"
        ):
            continue

        if (
            row.get("relationship_type", "").strip().upper()
            != "ELIGIBLE_FIELD"
        ):
            continue

        value = row.get("target_value", "").strip()

        if value:
            fields.append(value)

    return fields


def evaluate_scholarship(
    scholarship_id: str,
    learner_profile: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Evaluate a learner profile against a scholarship's recorded rules.

    This determines whether the learner appears eligible to apply.
    It does not predict or guarantee that the scholarship will be awarded.
    """

    # load_csv() already starts from the project's data directory,
    # so paths here must be relative to data/.
    scholarships = load_csv(
        "reference/scholarships.csv"
    )

    requirements = load_csv(
        "relationships/scholarship_eligibility_requirements.csv"
    )

    applicability = load_csv(
        "relationships/scholarship_applicability.csv"
    )

    scholarship = next(
        (
            row
            for row in scholarships
            if row.get("scholarship_id") == scholarship_id
        ),
        None,
    )

    if scholarship is None:
        return {
            "scholarship_id": scholarship_id,
            "status": "NOT_FOUND",
            "message": (
                "Scholarship was not found in the "
                "WiseLanka knowledge base."
            ),
        }

    scholarship_requirements = [
        row
        for row in requirements
        if row.get("scholarship_id") == scholarship_id
    ]

    applicable_fields = _get_applicable_fields(
        scholarship_id,
        applicability,
    )

    evaluations = [
        _evaluate_requirement(
            requirement,
            learner_profile,
        )
        for requirement in scholarship_requirements
    ]

    # Evaluate whether the learner's intended field is
    # represented in the scholarship applicability data.
    field_evaluation = None
    learner_field = learner_profile.get("field")

    if applicable_fields:
        if learner_field is None or learner_field == "":
            field_evaluation = {
                "field": learner_field,
                "status": "UNKNOWN",
                "applicable_fields": applicable_fields,
            }

        else:
            field_matches = any(
                _normalise(learner_field)
                == _normalise(field)
                for field in applicable_fields
            )

            field_evaluation = {
                "field": learner_field,
                "status": (
                    "PASSED"
                    if field_matches
                    else "FAILED"
                ),
                "applicable_fields": applicable_fields,
            }

    failed_requirements = [
        item
        for item in evaluations
        if (
            item["mandatory"]
            and item["status"] == "FAILED"
        )
    ]

    unknown_requirements = [
        item
        for item in evaluations
        if (
            item["mandatory"]
            and item["status"] == "UNKNOWN"
        )
    ]

    # Determine the overall application eligibility status.
    if (
        field_evaluation
        and field_evaluation["status"] == "FAILED"
    ):
        overall_status = "REQUIREMENTS_NOT_MET"

    elif failed_requirements:
        overall_status = "REQUIREMENTS_NOT_MET"

    elif (
        unknown_requirements
        or (
            field_evaluation
            and field_evaluation["status"] == "UNKNOWN"
        )
    ):
        overall_status = "POTENTIALLY_ELIGIBLE"

    else:
        overall_status = "ELIGIBLE_TO_APPLY"

    return {
        "scholarship_id": scholarship_id,
        "scholarship_name": scholarship.get(
            "scholarship_name"
        ),
        "provider_name": scholarship.get(
            "provider_name"
        ),
        "scholarship_type": scholarship.get(
            "scholarship_type"
        ),
        "coverage_description": scholarship.get(
            "coverage_description"
        ),
        "application_url": scholarship.get(
            "application_url"
        ),
        "opening_date": scholarship.get(
            "opening_date"
        ),
        "closing_date": scholarship.get(
            "closing_date"
        ),
        "scholarship_status": scholarship.get(
            "status"
        ),
        "last_verified_date": scholarship.get(
            "last_verified_date"
        ),
        "eligibility_status": overall_status,
        "requirements": evaluations,
        "field_evaluation": field_evaluation,
        "disclaimer": (
            "This result indicates apparent eligibility to apply "
            "based on the rules recorded in the WiseLanka knowledge "
            "base. It does not guarantee nomination, selection, "
            "admission, or a scholarship award."
        ),
    }