import csv
import json
import sqlite3

import pytest

from backend.app.research import reporting, responses


def make_response(**updates):
    payload = {
        "instrument_version": responses.INSTRUMENT_VERSION,
        "age_18_plus": True,
        "consent_confirmed": True,
        "device": "Mobile phone",
        "tasks": ["Task 1 — A/L learner profile"],
        "route": "Yes",
        "answers": {"Q5": "4", "Q6": "N/A", "Q20": reporting.COMPREHENSION_KEYS["Q20"],
                    "Q21": "Not sure.", "Q25": "Synthetic, anonymous-test comment"},
    }
    payload.update(updates)
    return responses.ResearchResponse.model_validate(payload)


def make_db(path, entries=()):
    responses.initialize_database(path)
    for response in entries:
        responses.insert_response(path, response)
    return path


def test_empty_database_reports_zero_counts_and_empty_items(tmp_path):
    db = make_db(tmp_path / "empty.sqlite3")
    summary = reporting.calculate_summary(db)
    assert summary["submitted_responses"] == 0
    assert summary["item_counts"]["Q5"]["missing"] == 0
    assert summary["item_counts"]["Q6"]["not_applicable"] == 0
    assert summary["item_counts"]["Q5"]["rating_mean"] is None
    assert summary["comprehension"]["Q20"] == {"correct": 0, "incorrect": 0, "unanswered": 0}


def test_counts_ratings_missing_na_and_conditional_applicability(tmp_path):
    first = make_response()
    second = make_response(
        tasks=["Task 2 — Career pathways"],
        answers={"Q5": "2", "Q14": "5", "Q20": "Not sure."},
    )
    db = make_db(tmp_path / "summary.sqlite3", [first, second])
    summary = reporting.calculate_summary(db)
    assert summary["submitted_responses"] == 2
    assert summary["context_item_counts"]["device"]["responses"] == 2
    assert summary["context_item_counts"]["tasks"]["answer_counts"]["Task 1"] == 1
    assert summary["context_item_counts"]["route"]["answer_counts"]["Yes"] == 2
    assert summary["item_counts"]["Q5"]["rating_distribution_1_to_5"] == {"1": 0, "2": 1, "3": 0, "4": 1, "5": 0}
    assert summary["item_counts"]["Q5"]["rating_mean"] == 3
    assert summary["item_counts"]["Q5"]["rating_median"] == 3
    assert summary["item_counts"]["Q6"]["not_observed_not_applicable_answer"] == 1
    assert summary["item_counts"]["Q6"]["not_applicable"] == 1
    assert summary["item_counts"]["Q14"]["applicable"] == 1
    assert summary["item_counts"]["Q14"]["missing"] == 0
    assert summary["item_counts"]["Q16"]["not_applicable"] == 2
    assert summary["comprehension"]["Q20"] == {"correct": 1, "incorrect": 1, "unanswered": 0}
    assert summary["comprehension"]["Q21"]["unanswered"] == 1


def test_observation_summaries_use_existing_response_linkage(tmp_path):
    db = make_db(tmp_path / "observations.sqlite3", [make_response()])
    with sqlite3.connect(db) as connection:
        response_id = connection.execute("SELECT response_id FROM research_responses").fetchone()[0]
    responses.insert_observation(db, response_id, "Task 1 — A/L learner profile", "UNASSISTED", 40)
    responses.insert_observation(db, response_id, "Task 4 — Qualification progression", "SKIPPED")
    summary = reporting.calculate_summary(db)
    task1 = summary["observations_by_task"]["Task 1 — A/L learner profile"]
    assert task1["observations"] == 1
    assert task1["completion_states"] == {"UNASSISTED": 1}
    assert task1["duration_median_seconds"] == 40
    assert summary["observations_by_task"]["Task 2 — Career pathways"]["observations"] == 0


@pytest.mark.parametrize("value", ["=1+1", "+cmd", "-1+2", "@SUM(A1:A2)", "  =HYPERLINK(\"x\")", "\t=1"])
def test_csv_formula_injection_cells_are_neutralized(value):
    assert reporting.safe_csv_cell(value).startswith("'")


def test_report_is_aggregate_html_and_feedback_export_has_no_response_ids(tmp_path):
    db = make_db(tmp_path / "responses.sqlite3", [make_response(answers={
        "Q5": "5", "Q25": "=HYPERLINK(\"https://example.invalid\")"})])
    output = tmp_path / "private-report"
    files = reporting.generate_report(db, output)
    html = files["html"].read_text(encoding="utf-8")
    assert "Synthetic" not in html
    assert "response_id" not in html
    with files["qualitative_csv"].open(encoding="utf-8", newline="") as stream:
        data = list(csv.DictReader(stream))
    assert data[0]["feedback_text_no_response_id"].startswith("'=")
    assert "response_id" not in data[0]
    assert files["summary"].exists()


def test_synthetic_demo_labels_html_json_and_all_csv_exports(tmp_path):
    db = make_db(tmp_path / "responses.sqlite3", [make_response()])
    files = reporting.generate_report(db, tmp_path / "synthetic-report", synthetic_demo=True)
    label = reporting.SYNTHETIC_LABEL
    assert label in files["html"].read_text(encoding="utf-8")
    assert json.loads(files["summary"].read_text(encoding="utf-8"))["data_classification"] == label
    for key in ("items_csv", "comprehension_csv", "observations_csv", "qualitative_csv"):
        with files[key].open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        assert rows and all(row["data_classification"] == label for row in rows)


def test_report_rejects_output_inside_repository(tmp_path):
    db = make_db(tmp_path / "responses.sqlite3")
    with pytest.raises(reporting.ReportingError, match="outside the project"):
        reporting.generate_report(db, reporting.PROJECT_ROOT / "frontend" / "pages" / "report-test")


def test_database_opened_read_only_and_missing_or_invalid_schema_rejected(tmp_path):
    db = make_db(tmp_path / "responses.sqlite3", [make_response()])
    with pytest.raises(sqlite3.OperationalError):
        with reporting._readonly_connection(db) as connection:
            connection.execute("DELETE FROM research_responses")
    empty_file = tmp_path / "not-research.sqlite3"
    sqlite3.connect(empty_file).close()
    with pytest.raises(reporting.ReportingError, match="expected research schema"):
        reporting.calculate_summary(empty_file)
