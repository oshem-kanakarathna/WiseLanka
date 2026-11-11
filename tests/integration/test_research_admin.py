import sqlite3

import pytest

from backend.app.research import admin, responses


def test_admin_invitation_uses_local_only_fragment_url():
    url = admin._local_questionnaire_url("http://127.0.0.1:5500/pages/research-evaluation.html", "secret-test-token")
    assert url.endswith("#invite=secret-test-token")
    for value in ("https://example.org/evaluation", "http://localhost/evaluation?x=1",
                  "http://user@localhost/evaluation", "http://localhost/evaluation#other"):
        with pytest.raises(ValueError):
            admin._local_questionnaire_url(value, "token")


def test_admin_cli_fails_closed_without_creating_default_database(monkeypatch, tmp_path):
    db = tmp_path / "must-not-be-created.sqlite3"
    monkeypatch.setattr(responses, "default_database_path", lambda: db)
    monkeypatch.delenv("RESEARCH_COLLECTION_ENABLED", raising=False)
    with pytest.raises(SystemExit):
        admin.main(["create-invitation", "--consent-verified"])
    assert not db.exists()


def test_admin_cli_creates_private_session_and_session_observation(monkeypatch, tmp_path, capsys):
    db = tmp_path / "research.sqlite3"
    monkeypatch.setattr(responses, "default_database_path", lambda: db)
    monkeypatch.setenv("RESEARCH_COLLECTION_ENABLED", "true")
    assert admin.main(["create-invitation", "--consent-verified", "--expires-minutes", "45"]) == 0
    output = capsys.readouterr().out
    assert "One-time local questionnaire URL:" in output
    assert "#invite=" in output
    with sqlite3.connect(db) as connection:
        session_id = connection.execute("SELECT session_id FROM research_sessions").fetchone()[0]
        assert connection.execute("SELECT consent_verified FROM research_sessions").fetchone()[0] == 1
        assert len(connection.execute("SELECT token_sha256 FROM research_invitations").fetchone()[0]) == 64
    assert admin.main(["record-observation", "--session-id", session_id,
        "--task-id", "Task 1 — A/L learner profile", "--state", "ASSISTED", "--duration-seconds", "63"]) == 0
    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT session_id,completion_state,duration_seconds FROM research_session_observations").fetchone() == (session_id,"ASSISTED",63)
