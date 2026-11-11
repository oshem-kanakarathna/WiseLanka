import json
import sqlite3

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.app.api.main import app
from backend.app.research import responses


def payload(**updates):
    result = {
        "instrument_version": responses.INSTRUMENT_VERSION,
        "age_18_plus": True,
        "consent_confirmed": True,
        "device": "Mobile phone",
        "tasks": ["Task 1 — A/L learner profile", "Task 4 — Qualification progression"],
        "route": "Yes",
        "answers": {"Q5": "4", "Q6": "5", "Q24": "Synthetic explanation"},
    }
    result.update(updates)
    return result


def test_pydantic_rejects_missing_adult_confirmation():
    request = payload()
    del request["age_18_plus"]
    with pytest.raises(ValidationError):
        responses.ResearchResponse.model_validate(request)


def test_consent_confirmation_required():
    with pytest.raises(ValidationError):
        responses.ResearchResponse.model_validate(payload(consent_confirmed=False))


@pytest.mark.parametrize("answers", [
    {"Q5": "6"}, {"Q20": "Made up option"}, {"Q30": "unknown"},
    {"Q6": "3"},  # Q6 requires Task 1, which is absent below.
])
def test_invalid_or_inapplicable_question_answers_rejected(answers):
    tasks = ["Task 4 — Qualification progression"]
    with pytest.raises(ValidationError):
        responses.ResearchResponse.model_validate(payload(tasks=tasks, answers=answers))


def test_written_feedback_length_is_limited():
    with pytest.raises(ValidationError):
        responses.ResearchResponse.model_validate(payload(answers={"Q25": "x" * 2001}))


def test_hidden_conditional_answer_rejected():
    with pytest.raises(ValidationError):
        responses.ResearchResponse.model_validate(payload(
            tasks=["Task 2 — Career pathways"], answers={"Q6": "4"}
        ))


def test_sqlite_response_and_observation_linkage_and_duplicate_guard(tmp_path):
    db = tmp_path / "responses.sqlite3"
    responses.initialize_database(db)
    valid = responses.ResearchResponse.model_validate(payload())
    response_id = responses.insert_response(db, valid)
    observation_id = responses.insert_observation(
        db, response_id, "Task 1 — A/L learner profile", "UNASSISTED", 42
    )
    with sqlite3.connect(db) as connection:
        row = connection.execute(
            "SELECT instrument_version,adult_confirmed,consent_confirmed,device_category,tasks_attempted_json,answers_json FROM research_responses WHERE response_id=?",
            (response_id,),
        ).fetchone()
        obs = connection.execute(
            "SELECT response_id,task_id FROM research_task_observations WHERE observation_id=?",
            (observation_id,),
        ).fetchone()
        assert row[0:4] == (responses.INSTRUMENT_VERSION, 1, 1, "Mobile phone")
        assert json.loads(row[4]) == valid.tasks
        assert json.loads(row[5]) == valid.answers
        assert obs == (response_id, "Task 1 — A/L learner profile")
        with pytest.raises(sqlite3.IntegrityError):
            responses.insert_observation(db, response_id, "Task 1 — A/L learner profile", "ASSISTED")


def test_collection_disabled_rejects_before_database_access(monkeypatch, tmp_path):
    db = tmp_path / "should-not-exist.sqlite3"
    monkeypatch.delenv("RESEARCH_COLLECTION_ENABLED", raising=False)
    monkeypatch.setattr(responses, "default_database_path", lambda: db)
    with TestClient(app) as client:
        result = client.post("/research/responses", json=payload())
    assert result.status_code == 503
    assert not db.exists()


def test_explicit_false_and_invalid_switch_values_fail_closed(monkeypatch):
    for value in ("false", "yes", "1", ""):
        monkeypatch.setenv("RESEARCH_COLLECTION_ENABLED", value)
        assert responses.collection_enabled() is False


def test_enabled_route_writes_invitation_bound_synthetic_response_only(monkeypatch, tmp_path):
    db = tmp_path / "responses.sqlite3"
    monkeypatch.setenv("RESEARCH_COLLECTION_ENABLED", "true")
    monkeypatch.setattr(responses, "default_database_path", lambda: db)
    responses.initialize_database(db)
    invitation = responses.create_invitation(db, consent_verified=True)
    request = payload()
    request.pop("consent_confirmed")  # Consent is confirmed from the researcher-created session.
    request.update({"invitation_token": invitation["invitation_token"], "idempotency_key": "d36de873-30cf-4482-89af-b3f005867013"})
    with TestClient(app) as client:
        result = client.post("/research/responses", json=request)
    assert result.status_code == 201
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 1


def test_phase_two_database_schema_migrates_without_losing_existing_response(tmp_path):
    db = tmp_path / "phase-two.sqlite3"
    with sqlite3.connect(db) as connection:
        connection.executescript("""
            CREATE TABLE research_responses (
              response_id TEXT PRIMARY KEY,instrument_version TEXT NOT NULL,adult_confirmed INTEGER NOT NULL,
              consent_confirmed INTEGER NOT NULL,device_category TEXT NOT NULL,tasks_attempted_json TEXT NOT NULL,
              route_answer TEXT NOT NULL,answers_json TEXT NOT NULL,consent_reference TEXT,submitted_at_utc TEXT NOT NULL
            );
            CREATE TABLE research_task_observations (
              observation_id TEXT PRIMARY KEY,response_id TEXT NOT NULL,task_id TEXT NOT NULL,
              completion_state TEXT NOT NULL,duration_seconds INTEGER,created_at_utc TEXT NOT NULL,
              UNIQUE(response_id,task_id)
            );
            INSERT INTO research_responses VALUES
              ('synthetic-existing-id','evaluation-prototype-v2-2026-10-31',1,1,'Tablet','[]','Yes','{}',NULL,'2026-10-01T00:00:00+00:00');
        """)
    responses.initialize_database(db)
    with sqlite3.connect(db) as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(research_responses)")}
        row = connection.execute("SELECT response_id,session_id,idempotency_key FROM research_responses").fetchone()
    assert {"session_id", "idempotency_key", "payload_sha256"} <= columns
    assert row == ("synthetic-existing-id", None, None)
