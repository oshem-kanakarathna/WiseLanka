"""Local researcher-operated session and observation commands.

No HTTP admin endpoint is exposed. Commands fail closed unless the operator has
explicitly enabled collection for an approved local environment.
"""
from __future__ import annotations

import argparse
import sqlite3
from urllib.parse import urlsplit

from backend.app.research import responses


def _local_questionnaire_url(value: str, token: str) -> str:
    parts = urlsplit(value)
    if parts.scheme not in {"http", "https"} or parts.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Questionnaire URL must use a local host; public invitation URLs are not supported")
    if parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("Questionnaire URL must not contain query parameters or a fragment")
    return value.rstrip("#") + "#invite=" + token


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local WiseLanka researcher session operations")
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create-invitation", help="Create a session before the four evaluation tasks")
    create.add_argument("--consent-verified", action="store_true", required=True,
                        help="Attest that the separately obtained written consent procedure was completed")
    create.add_argument("--expires-minutes", type=int, default=180)
    create.add_argument("--questionnaire-url", default="http://127.0.0.1:5500/pages/research-evaluation.html")
    observe = subparsers.add_parser("record-observation", help="Record a task outcome against its pre-task session ID")
    observe.add_argument("--session-id", required=True)
    observe.add_argument("--task-id", required=True, choices=sorted(responses.TASKS))
    observe.add_argument("--state", required=True,
                         choices=["UNASSISTED", "ASSISTED", "NOT_COMPLETED", "SKIPPED", "TECHNICAL_FAILURE"])
    observe.add_argument("--duration-seconds", type=int)
    args = parser.parse_args(argv)

    if not responses.collection_enabled():
        parser.error("Research operations are disabled; collection remains fail-closed")
    path = responses.default_database_path()
    responses.initialize_database(path)
    if args.command == "create-invitation":
        try:
            _local_questionnaire_url(args.questionnaire_url, "validation-token")
            invitation = responses.create_invitation(path, consent_verified=args.consent_verified,
                                                     expires_in_minutes=args.expires_minutes)
            url = _local_questionnaire_url(args.questionnaire_url, invitation["invitation_token"])
        except ValueError as error:
            parser.error(str(error))
        # The raw token is intentionally emitted once to the local operator's terminal only.
        print("Study session created before tasks.")
        print(f"Session ID for observation notes: {invitation['session_id']}")
        print(f"Invitation expires (UTC): {invitation['expires_at_utc']}")
        print(f"One-time local questionnaire URL: {url}")
    else:
        if args.duration_seconds is not None and args.duration_seconds < 0:
            parser.error("Duration cannot be negative")
        try:
            responses.insert_session_observation(path, args.session_id, args.task_id,
                                                 args.state, args.duration_seconds)
        except (ValueError, sqlite3.Error) as error:
            parser.error(str(error))
        print("Task observation recorded against the study-session ID.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
