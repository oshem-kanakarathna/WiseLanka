"""Public eligibility API: one authoritative implementation."""
from backend.app.eligibility.engine import (
    GRADE_RANK as GRADE_ORDER,
    grade_meets_minimum,
    evaluate_requirement,
    evaluate_programme,
    assess_academic_gaps,
)

__all__ = ["GRADE_ORDER", "grade_meets_minimum", "evaluate_requirement",
           "evaluate_programme", "assess_academic_gaps"]
