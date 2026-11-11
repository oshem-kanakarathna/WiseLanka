import sqlite3
import uuid

import pytest
from fastapi.testclient import TestClient

from backend.app.api.main import app
from backend.app.research import responses
from backend.app.research.reporting import calculate_summary


def public_payload(invitation_token, **updates):
    payload = {
        "invitation_token": invitation_token,
        "idempotency_key": str(uuid.uuid4()),
        "instrument_version": responses.INSTRUMENT_VERSION,
        "age_18_plus": True,
        "device": "Mobile phone",
        "tasks": ["Task 1 — A/L learner profile", "Task 4 — Qualification progression"],
        "route": "Yes",
        "answers": {"Q5": "4", "Q6": "5", "Q20": "The checked academic requirements appear satisfied, but additional admission conditions may still apply."},
    }
    payload.update(updates)
    return payload


def setup_db(tmp_path, monkeypatch, *, enabled=True):
    db = tmp_path / "private-research.sqlite3"
    responses.initialize_database(db)
    monkeypatch.setattr(responses, "default_database_path", lambda: db)
    monkeypatch.setenv("RESEARCH_COLLECTION_ENABLED", "true" if enabled else "false")
    return db


def issue(db):
    return responses.create_invitation(db, consent_verified=True, expires_in_minutes=60)


def test_invitation_hashing_session_observation_and_idempotent_submission(tmp_path, monkeypatch):
    db = setup_db(tmp_path, monkeypatch)
    invitation = issue(db)
    with sqlite3.connect(db) as connection:
        token_hash, session_id = connection.execute("SELECT token_sha256,session_id FROM research_invitations").fetchone()
        assert token_hash != invitation["invitation_token"]
        assert len(session_id) == 36
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 0
    responses.insert_session_observation(db, invitation["session_id"],
        "Task 1 — A/L learner profile", "UNASSISTED", 52)
    payload = public_payload(invitation["invitation_token"])
    with TestClient(app) as client:
        first = client.post("/research/responses", json=payload)
        retry = client.post("/research/responses", json=payload)
        changed = dict(payload, answers={"Q5": "3"})
        reused = client.post("/research/responses", json=changed)
    assert first.status_code == 201 and first.json() == {"status": "received", "duplicate_retry": False}
    assert retry.status_code == 200 and retry.json() == {"status": "received", "duplicate_retry": True}
    assert reused.status_code == 409
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 1
        assert connection.execute("SELECT session_id,consent_confirmed,adult_confirmed FROM research_responses").fetchone() == (invitation["session_id"], 1, 1)
    summary = calculate_summary(db)
    assert summary["observations_by_task"]["Task 1 — A/L learner profile"]["observations"] == 1


def test_invalid_and_expired_invitations_are_rejected(tmp_path, monkeypatch):
    db = setup_db(tmp_path, monkeypatch)
    invitation = issue(db)
    with sqlite3.connect(db) as connection:
        connection.execute("UPDATE research_invitations SET expires_at_utc='2000-01-01T00:00:00+00:00'")
    with TestClient(app) as client:
        invalid = client.post("/research/responses", json=public_payload("x" * 48))
        expired = client.post("/research/responses", json=public_payload(invitation["invitation_token"]))
    assert invalid.status_code == 404
    assert expired.status_code == 410
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 0


def test_consent_verification_must_be_present_and_cannot_be_self_asserted(tmp_path, monkeypatch):
    db = setup_db(tmp_path, monkeypatch)
    with pytest.raises(responses.ConsentVerificationRequired):
        responses.create_invitation(db, consent_verified=False)
    invitation = issue(db)
    with sqlite3.connect(db) as connection:
        connection.execute("UPDATE research_sessions SET consent_verified=0")
    payload = public_payload(invitation["invitation_token"], consent_confirmed=True)
    with TestClient(app) as client:
        result = client.post("/research/responses", json=payload)
    assert result.status_code == 422
    payload.pop("consent_confirmed")
    with TestClient(app) as client:
        result = client.post("/research/responses", json=payload)
    assert result.status_code == 403
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 0


@pytest.mark.parametrize("update", [
    {"age_18_plus": False},
    {"instrument_version": "unknown"},
    {"answers": {"Q30": "bad"}},
    {"tasks": ["Task 4 — Qualification progression"], "answers": {"Q6": "4"}},
    {"device": "Unknown"},
    {"route": "Unknown"},
])
def test_invalid_questionnaire_payloads_do_not_write(tmp_path, monkeypatch, update):
    db = setup_db(tmp_path, monkeypatch)
    invitation = issue(db)
    with TestClient(app) as client:
        result = client.post("/research/responses", json=public_payload(invitation["invitation_token"], **update))
    assert result.status_code == 422
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 0


def test_text_and_body_size_limits(tmp_path, monkeypatch):
    db = setup_db(tmp_path, monkeypatch)
    invitation = issue(db)
    with TestClient(app) as client:
        long_text = client.post("/research/responses", json=public_payload(
            invitation["invitation_token"], answers={"Q25": "x" * 2001}))
        large_body = client.post("/research/responses", content=b" " * (32 * 1024 + 1),
                                 headers={"content-type": "application/json"})
    assert long_text.status_code == 422
    assert large_body.status_code == 413
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 0


def test_disabled_switch_rejects_without_write_or_token_consumption(tmp_path, monkeypatch):
    db = setup_db(tmp_path, monkeypatch, enabled=True)
    invitation = issue(db)
    monkeypatch.setenv("RESEARCH_COLLECTION_ENABLED", "false")
    with TestClient(app) as client:
        result = client.post("/research/responses", json=public_payload(invitation["invitation_token"]))
    assert result.status_code == 503
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT count(*) FROM research_responses").fetchone()[0] == 0
        assert connection.execute("SELECT used_at_utc FROM research_invitations").fetchone()[0] is None
