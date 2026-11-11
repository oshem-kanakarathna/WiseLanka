from backend.app.scholarships.engine import evaluate_scholarship


def test_eligible_applicant():
    profile = {
        "citizenship": "Sri Lanka",
        "age_on_reference_date": 19,
        "a_level_exam_year": 2024,
        "a_level_pass_count": 3,
        "o_level_english_grade": "B",
        "a_level_english_grade": "S",
        "state_university_internal_student": False,
        "field": "STEM",
    }

    result = evaluate_scholarship("SCH0001", profile)

    assert result["eligibility_status"] == "ELIGIBLE_TO_APPLY"
    assert result["field_evaluation"]["status"] == "PASSED"

    assert all(
        requirement["status"] == "PASSED"
        for requirement in result["requirements"]
    )


def test_applicant_who_fails_requirements():
    profile = {
        "citizenship": "Sri Lanka",
        "age_on_reference_date": 17,
        "a_level_exam_year": 2024,
        "a_level_pass_count": 2,
        "o_level_english_grade": "S",
        "a_level_english_grade": "S",
        "state_university_internal_student": True,
        "field": "STEM",
    }

    result = evaluate_scholarship("SCH0001", profile)

    assert result["eligibility_status"] == "REQUIREMENTS_NOT_MET"

    failed_ids = {
        requirement["requirement_id"]
        for requirement in result["requirements"]
        if requirement["status"] == "FAILED"
    }

    assert "SREQ0002" in failed_ids
    assert "SREQ0004" in failed_ids
    assert "SREQ0005" in failed_ids
    assert "SREQ0007" in failed_ids


def test_missing_information_is_potentially_eligible():
    profile = {
        "citizenship": "Sri Lanka",
        "age_on_reference_date": 19,
        "a_level_exam_year": 2024,
        "a_level_pass_count": 3,
        "field": "STEM",
    }

    result = evaluate_scholarship("SCH0001", profile)

    assert result["eligibility_status"] == "POTENTIALLY_ELIGIBLE"

    unknown_ids = {
        requirement["requirement_id"]
        for requirement in result["requirements"]
        if requirement["status"] == "UNKNOWN"
    }

    assert "SREQ0005" in unknown_ids
    assert "SREQ0006" in unknown_ids
    assert "SREQ0007" in unknown_ids


def test_ineligible_field():
    profile = {
        "citizenship": "Sri Lanka",
        "age_on_reference_date": 19,
        "a_level_exam_year": 2024,
        "a_level_pass_count": 3,
        "o_level_english_grade": "A",
        "a_level_english_grade": "B",
        "state_university_internal_student": False,
        "field": "Arts",
    }

    result = evaluate_scholarship("SCH0001", profile)

    assert result["field_evaluation"]["status"] == "FAILED"
    assert result["eligibility_status"] == "REQUIREMENTS_NOT_MET"


def test_unknown_scholarship():
    result = evaluate_scholarship(
        "SCH9999",
        {
            "citizenship": "Sri Lanka",
        },
    )

    assert result["status"] == "NOT_FOUND"
    assert result["scholarship_id"] == "SCH9999"


def test_result_contains_scholarship_information():
    profile = {
        "citizenship": "Sri Lanka",
        "age_on_reference_date": 19,
        "a_level_exam_year": 2024,
        "a_level_pass_count": 3,
        "o_level_english_grade": "B",
        "a_level_english_grade": "S",
        "state_university_internal_student": False,
        "field": "Agriculture",
    }

    result = evaluate_scholarship("SCH0001", profile)

    assert result["scholarship_id"] == "SCH0001"
    assert result["scholarship_name"]
    assert result["provider_name"]
    assert result["application_url"]
    assert result["last_verified_date"]
    assert result["disclaimer"]

    assert result["field_evaluation"]["status"] == "PASSED"