"""Private SQLite foundation for a future approved research study.

This module is deliberately separate from the educational CSV knowledge base.
The default database path is outside the repository and is not opened at import
or application startup. No research data is collected by importing this module.
"""
from __future__ import annotations

import json
import os
import hashlib
import secrets
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator, model_validator

INSTRUMENT_VERSION = "evaluation-prototype-v2-2026-10-31"
DEVICES = {
    "Laptop or desktop computer", "Mobile phone", "Tablet", "Other device", "Prefer not to say"
}
TASKS = {
    "Task 1 — A/L learner profile", "Task 2 — Career pathways",
    "Task 3 — O/L learner profile", "Task 4 — Qualification progression"
}
ROUTES = {
    "Yes", "No", "Partially / A different pathway appeared",
    "Not sure / Did not complete these tasks"
}
LIKERT_IDS = {"Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13",
              "Q14", "Q15", "Q16", "Q17", "Q18", "Q19"}
SINGLE_IDS = {"Q20", "Q21", "Q22", "Q23"}
TEXT_IDS = {"Q24", "Q25", "Q26", "Q27", "Q28", "Q29"}
QUESTION_IDS = LIKERT_IDS | SINGLE_IDS | TEXT_IDS
QUESTION_OPTIONS = {
    "Q20": {"The learner is guaranteed admission.",
            "The checked academic requirements appear satisfied, but additional admission conditions may still apply.",
            "The institution has already accepted the learner.", "Not sure."},
    "Q21": {"The learner definitely does not meet the requirement.",
            "The requirement is automatically satisfied.",
            "More information is needed before making a definite decision.", "Not sure."},
    "Q22": {"Progression is guaranteed after completing the current programme.",
            "Progression may be possible if additional stated conditions are satisfied.",
            "The learner is not allowed to progress.", "Not sure / No conditional route appeared."},
    "Q23": {"Assume WiseLanka’s recommendation guarantees admission.",
            "Verify the current requirements and selection conditions through official institutional sources.",
            "Ignore any conditions that WiseLanka could not assess.", "Not sure."},
}
CONDITIONAL = {"Q6": "Task 1", "Q7": "Task 3", "Q14": "Task 2", "Q15": "Task 2",
               "Q16": "Task 4", "Q17": "Task 4", "Q24": "Task 4"}
Answer = Union[StrictStr, List[StrictStr]]


def collection_enabled() -> bool:
    """Only the exact string 'true' enables collection; absent/invalid values fail closed."""
    return os.environ.get("RESEARCH_COLLECTION_ENABLED", "false").strip().lower() == "true"


class QuestionnaireFields(BaseModel):
    """Questionnaire fields shared by the API request and stored response."""
    model_config = ConfigDict(extra="forbid", strict=True)

    instrument_version: Literal["evaluation-prototype-v2-2026-10-31"]
    age_18_plus: StrictBool
    device: StrictStr
    tasks: List[StrictStr] = Field(max_length=4)
    route: StrictStr
    answers: Dict[str, Answer] = Field(default_factory=dict, max_length=25)

    @field_validator("age_18_plus")
    @classmethod
    def require_adult(cls, value):
        if value is not True:
            raise ValueError("Research responses are restricted to adults aged 18 or over")
        return value

    @field_validator("device")
    @classmethod
    def valid_device(cls, value):
        if value not in DEVICES:
            raise ValueError("Unknown device category")
        return value

    @field_validator("tasks")
    @classmethod
    def valid_tasks(cls, value):
        if len(value) != len(set(value)) or not set(value) <= TASKS:
            raise ValueError("Tasks must be unique known questionnaire options")
        return value

    @field_validator("route")
    @classmethod
    def valid_route(cls, value):
        if value not in ROUTES:
            raise ValueError("Unknown route answer")
        return value

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, value):
        unknown = set(value) - QUESTION_IDS
        if unknown:
            raise ValueError("Unknown questionnaire question ID")
        for question_id, answer in value.items():
            if question_id in LIKERT_IDS:
                if answer not in {"1", "2", "3", "4", "5", "N/A"}:
                    raise ValueError("Rating must be 1–5 or N/A")
            elif question_id in SINGLE_IDS:
                if answer not in QUESTION_OPTIONS[question_id]:
                    raise ValueError("Unknown answer option")
            elif question_id in TEXT_IDS:
                if not isinstance(answer, str) or len(answer) > 2000:
                    raise ValueError("Written answers must be at most 2000 characters")
            if isinstance(answer, list):
                raise ValueError("Only task selection may contain multiple values")
        return value

    @model_validator(mode="after")
    def validate_applicability(self):
        selected = {task.split(" — ", 1)[0] for task in self.tasks}
        for question_id, task in CONDITIONAL.items():
            if question_id in self.answers and task not in selected:
                raise ValueError("Answer supplied for a question not applicable to selected tasks")
        return self


class ResearchResponse(QuestionnaireFields):
    """Validated response with consent status assigned from the researcher session."""
    consent_confirmed: StrictBool

    @field_validator("consent_confirmed")
    @classmethod
    def require_consent(cls, value):
        if value is not True:
            raise ValueError("Consent confirmation is required")
        return value

class QuestionnaireSubmission(QuestionnaireFields):
    """Public request: consent is established by the invitation, not self-asserted here."""
    invitation_token: StrictStr
    idempotency_key: StrictStr

    @field_validator("invitation_token")
    @classmethod
    def validate_token_shape(cls, value):
        if not 40 <= len(value) <= 128 or any(ch.isspace() for ch in value):
            raise ValueError("Invalid invitation token")
        return value

    @field_validator("idempotency_key")
    @classmethod
    def validate_idempotency_key(cls, value):
        try:
            parsed = uuid.UUID(value)
        except (ValueError, AttributeError) as exc:
            raise ValueError("Idempotency key must be a UUID") from exc
        if str(parsed) != value.lower():
            raise ValueError("Idempotency key must be a canonical UUID")
        return value.lower()


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS research_responses (
    response_id TEXT PRIMARY KEY,
    instrument_version TEXT NOT NULL,
    adult_confirmed INTEGER NOT NULL CHECK (adult_confirmed = 1),
    consent_confirmed INTEGER NOT NULL CHECK (consent_confirmed = 1),
    device_category TEXT NOT NULL,
    tasks_attempted_json TEXT NOT NULL,
    route_answer TEXT NOT NULL,
    answers_json TEXT NOT NULL,
    consent_reference TEXT,
    submitted_at_utc TEXT NOT NULL,
    session_id TEXT REFERENCES research_sessions(session_id),
    idempotency_key TEXT,
    payload_sha256 TEXT,
    CHECK (length(response_id) = 36)
);
CREATE TABLE IF NOT EXISTS research_task_observations (
    observation_id TEXT PRIMARY KEY,
    response_id TEXT NOT NULL REFERENCES research_responses(response_id) ON DELETE CASCADE,
    task_id TEXT NOT NULL,
    completion_state TEXT NOT NULL,
    duration_seconds INTEGER CHECK (duration_seconds IS NULL OR duration_seconds >= 0),
    created_at_utc TEXT NOT NULL,
    UNIQUE(response_id, task_id)
);
CREATE TABLE IF NOT EXISTS research_sessions (
    session_id TEXT PRIMARY KEY,
    created_at_utc TEXT NOT NULL,
    consent_verified INTEGER NOT NULL CHECK (consent_verified IN (0, 1)),
    consent_verified_at_utc TEXT,
    CHECK (length(session_id) = 36)
);
CREATE TABLE IF NOT EXISTS research_invitations (
    invitation_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE REFERENCES research_sessions(session_id) ON DELETE CASCADE,
    token_sha256 TEXT NOT NULL UNIQUE,
    expires_at_utc TEXT NOT NULL,
    used_at_utc TEXT,
    response_id TEXT REFERENCES research_responses(response_id),
    created_at_utc TEXT NOT NULL,
    CHECK (length(invitation_id) = 36)
);
CREATE TABLE IF NOT EXISTS research_session_observations (
    observation_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES research_sessions(session_id) ON DELETE CASCADE,
    task_id TEXT NOT NULL,
    completion_state TEXT NOT NULL,
    duration_seconds INTEGER CHECK (duration_seconds IS NULL OR duration_seconds >= 0),
    created_at_utc TEXT NOT NULL,
    UNIQUE(session_id, task_id),
    CHECK (length(observation_id) = 36)
);
"""


def default_database_path() -> Path:
    """Private per-user application-data path, never under the source repository."""
    configured = os.environ.get("RESEARCH_DATABASE_PATH")
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_absolute():
            raise ValueError("RESEARCH_DATABASE_PATH must be absolute")
        candidate = candidate.resolve()
        repository = Path(__file__).resolve().parents[3]
        try:
            candidate.relative_to(repository)
        except ValueError:
            return candidate
        raise ValueError("Research database must be outside the repository and public directories")
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    elif __import__("sys").platform == "darwin":
        root = Path.home() / "Library/Application Support"
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    return root / "WiseLanka" / "research-responses.sqlite3"


def initialize_database(path: Path) -> None:
    """Explicitly initialize a database; never called automatically by the app."""
    path = Path(path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.parent.chmod(0o700)
    except OSError:
        pass
    with sqlite3.connect(path) as connection:
        connection.executescript(SCHEMA)
        columns = {row[1] for row in connection.execute("PRAGMA table_info(research_responses)")}
        for name, declaration in (("session_id", "TEXT REFERENCES research_sessions(session_id)"),
                                  ("idempotency_key", "TEXT"), ("payload_sha256", "TEXT")):
            if name not in columns:
                connection.execute(f"ALTER TABLE research_responses ADD COLUMN {name} {declaration}")
        observation_tables = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        if "research_session_observations" not in observation_tables:
            connection.execute("""CREATE TABLE research_session_observations (
                observation_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL REFERENCES research_sessions(session_id) ON DELETE CASCADE,
                task_id TEXT NOT NULL, completion_state TEXT NOT NULL,
                duration_seconds INTEGER CHECK (duration_seconds IS NULL OR duration_seconds >= 0),
                created_at_utc TEXT NOT NULL, UNIQUE(session_id, task_id))""")
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_research_response_session ON research_responses(session_id) WHERE session_id IS NOT NULL")
        connection.execute("DROP INDEX IF EXISTS uq_research_response_idempotency")
        connection.execute("CREATE UNIQUE INDEX uq_research_response_idempotency ON research_responses(session_id,idempotency_key) WHERE idempotency_key IS NOT NULL")
    try:
        path.chmod(0o600)
    except OSError:
        pass


class InvitationError(ValueError):
    """An invitation is absent, expired, consumed, or inconsistent."""


class ConsentVerificationRequired(ValueError):
    """The researcher session does not contain verified separate consent."""


def create_invitation(path: Path, *, consent_verified: bool, expires_in_minutes: int = 180) -> dict[str, str]:
    """Create a pre-task session and one-time invitation; return raw token only once."""
    if consent_verified is not True:
        raise ConsentVerificationRequired("Separate written consent must be verified before issuing an invitation")
    if not isinstance(expires_in_minutes, int) or not 5 <= expires_in_minutes <= 1440:
        raise ValueError("Invitation expiry must be between 5 minutes and 24 hours")
    session_id = str(uuid.uuid4())
    invitation_id = str(uuid.uuid4())
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
    now = datetime.now(timezone.utc)
    created = now.isoformat()
    expires = (now + timedelta(minutes=expires_in_minutes)).isoformat()
    with sqlite3.connect(Path(path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT INTO research_sessions(session_id,created_at_utc,consent_verified,consent_verified_at_utc) VALUES (?,?,1,?)",
            (session_id, created, created),
        )
        connection.execute(
            "INSERT INTO research_invitations(invitation_id,session_id,token_sha256,expires_at_utc,created_at_utc) VALUES (?,?,?,?,?)",
            (invitation_id, session_id, token_hash, expires, created),
        )
    return {"session_id": session_id, "invitation_token": token, "expires_at_utc": expires}


def _insert_validated_response(connection: sqlite3.Connection, response: ResearchResponse,
                               *, session_id: str | None = None, idempotency_key: str | None = None,
                               payload_sha256: str | None = None,
                               consent_reference: str | None = None) -> str:
    response_id = str(uuid.uuid4())
    connection.execute(
        """INSERT INTO research_responses
        (response_id,instrument_version,adult_confirmed,consent_confirmed,device_category,tasks_attempted_json,
         route_answer,answers_json,consent_reference,submitted_at_utc,session_id,idempotency_key,payload_sha256)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (response_id, response.instrument_version, int(response.age_18_plus),
         int(response.consent_confirmed), response.device,
         json.dumps(response.tasks, ensure_ascii=False), response.route,
         json.dumps(response.answers, ensure_ascii=False), consent_reference,
         datetime.now(timezone.utc).isoformat(), session_id, idempotency_key, payload_sha256),
    )
    return response_id


def insert_response(path: Path, response: ResearchResponse, consent_reference: Optional[str] = None) -> str:
    """Legacy storage helper for synthetic setup tests; never used by public API."""
    with sqlite3.connect(Path(path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        return _insert_validated_response(connection, response, consent_reference=consent_reference)


def submit_questionnaire(path: Path, submission: QuestionnaireSubmission) -> tuple[str, bool]:
    """Atomically consume an invitation and persist one response; retries are idempotent."""
    token_hash = hashlib.sha256(submission.invitation_token.encode("ascii")).hexdigest()
    response_data = submission.model_dump(exclude={"invitation_token", "idempotency_key"})
    stored_response = ResearchResponse.model_validate({**response_data, "consent_confirmed": True})
    canonical = json.dumps(stored_response.model_dump(), sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    payload_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(Path(path), timeout=10) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")
        invitation = connection.execute(
            """SELECT i.invitation_id,i.session_id,i.expires_at_utc,i.used_at_utc,s.consent_verified
            FROM research_invitations i JOIN research_sessions s ON s.session_id=i.session_id
            WHERE i.token_sha256=?""", (token_hash,),
        ).fetchone()
        if invitation is None:
            raise InvitationError("Invitation is invalid")
        if not invitation["consent_verified"]:
            raise ConsentVerificationRequired("Separate consent is not verified for this session")
        if invitation["used_at_utc"] is not None:
            previous = connection.execute(
                "SELECT response_id,payload_sha256 FROM research_responses WHERE session_id=? AND idempotency_key=?",
                (invitation["session_id"], submission.idempotency_key),
            ).fetchone()
            if previous and previous["payload_sha256"] == payload_hash:
                return previous["response_id"], True
            raise InvitationError("Invitation has already been used")
        if invitation["expires_at_utc"] <= now:
            raise InvitationError("Invitation has expired")

        response_id = _insert_validated_response(
            connection, stored_response, session_id=invitation["session_id"],
            idempotency_key=submission.idempotency_key, payload_sha256=payload_hash,
        )
        updated = connection.execute(
            "UPDATE research_invitations SET used_at_utc=?,response_id=? WHERE invitation_id=? AND used_at_utc IS NULL",
            (now, response_id, invitation["invitation_id"]),
        ).rowcount
        if updated != 1:
            raise InvitationError("Invitation has already been used")
        return response_id, False


def insert_session_observation(path: Path, session_id: str, task_id: str,
                               completion_state: str, duration_seconds: Optional[int] = None) -> str:
    """Record a researcher-observed task against the pre-task session identifier."""
    if task_id not in TASKS:
        raise ValueError("Unknown task ID")
    if completion_state not in {"UNASSISTED", "ASSISTED", "NOT_COMPLETED", "SKIPPED", "TECHNICAL_FAILURE"}:
        raise ValueError("Unknown task completion state")
    if duration_seconds is not None and (not isinstance(duration_seconds, int) or duration_seconds < 0):
        raise ValueError("Duration must be a non-negative integer")
    observation_id = str(uuid.uuid4())
    with sqlite3.connect(Path(path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(
            """INSERT INTO research_session_observations
            (observation_id,session_id,task_id,completion_state,duration_seconds,created_at_utc)
            VALUES (?,?,?,?,?,?)""",
            (observation_id, session_id, task_id, completion_state, duration_seconds,
             datetime.now(timezone.utc).isoformat()),
        )
    return observation_id


def insert_observation(path: Path, response_id: str, task_id: str,
                       completion_state: str, duration_seconds: Optional[int] = None) -> str:
    """Researcher-only future hook; no observation API is exposed in this phase."""
    if task_id not in TASKS:
        raise ValueError("Unknown task ID")
    if completion_state not in {"UNASSISTED", "ASSISTED", "NOT_COMPLETED", "SKIPPED", "TECHNICAL_FAILURE"}:
        raise ValueError("Unknown task completion state")
    if duration_seconds is not None and duration_seconds < 0:
        raise ValueError("Duration cannot be negative")
    observation_id = str(uuid.uuid4())
    with sqlite3.connect(Path(path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(
            """INSERT INTO research_task_observations
            (observation_id,response_id,task_id,completion_state,duration_seconds,created_at_utc)
            VALUES (?,?,?,?,?,?)""",
            (observation_id, response_id, task_id, completion_state, duration_seconds,
             datetime.now(timezone.utc).isoformat()),
        )
    return observation_id
