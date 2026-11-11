"""Read-only local summaries for the WiseLanka research SQLite store.

This module never enables collection and opens the input database in SQLite
read-only mode. Generated files are deliberately kept outside the repository.
"""
from __future__ import annotations

import argparse
import csv
from contextlib import closing
import html
import json
import os
import sqlite3
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import quote

from backend.app.research.responses import (
    CONDITIONAL,
    INSTRUMENT_VERSION,
    LIKERT_IDS,
    QUESTION_IDS,
    TASKS,
)

COMPREHENSION_KEYS = {
    "Q20": "The checked academic requirements appear satisfied, but additional admission conditions may still apply.",
    "Q21": "More information is needed before making a definite decision.",
    "Q22": "Progression may be possible if additional stated conditions are satisfied.",
    "Q23": "Verify the current requirements and selection conditions through official institutional sources.",
}
TEXT_IDS = {"Q25", "Q26", "Q27", "Q28", "Q29"}
OBSERVATION_STATES = {"UNASSISTED", "ASSISTED", "NOT_COMPLETED", "SKIPPED", "TECHNICAL_FAILURE"}
PROJECT_ROOT = Path(__file__).resolve().parents[3]
SYNTHETIC_LABEL = "SYNTHETIC — NOT REAL PARTICIPANT RESEARCH DATA"


class ReportingError(ValueError):
    """Input data or output location is not safe/valid for local reporting."""


def _readonly_connection(database: Path) -> sqlite3.Connection:
    path = Path(database).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ReportingError("Database path must name an existing regular file")
    uri = f"file:{quote(str(path), safe='/')}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    tables = {row[0] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    required = {"research_responses", "research_task_observations"}
    if not required <= tables:
        connection.close()
        raise ReportingError("Database does not contain the expected research schema")
    return connection


def _parse_json(value: str, description: str) -> Any:
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ReportingError(f"Invalid stored JSON in {description}") from exc


def _tasks_for(row: sqlite3.Row) -> set[str]:
    tasks = _parse_json(row["tasks_attempted_json"], "tasks_attempted_json")
    if not isinstance(tasks, list) or any(not isinstance(item, str) for item in tasks):
        raise ReportingError("Stored task selection is not a string list")
    if not set(tasks) <= TASKS:
        raise ReportingError("Stored task selection contains unknown options")
    return {item.split(" — ", 1)[0] for item in tasks}


def _answers_for(row: sqlite3.Row) -> dict[str, str]:
    answers = _parse_json(row["answers_json"], "answers_json")
    if not isinstance(answers, dict) or not set(answers) <= QUESTION_IDS:
        raise ReportingError("Stored answers do not match the known instrument")
    if any(not isinstance(value, str) for value in answers.values()):
        raise ReportingError("Stored answer has an unsupported type")
    return answers


def _is_applicable(question_id: str, task_codes: set[str]) -> bool:
    task = CONDITIONAL.get(question_id)
    return task is None or task in task_codes


def calculate_summary(database: Path) -> dict[str, Any]:
    """Read aggregate-only reporting data from an explicit database path."""
    with closing(_readonly_connection(database)) as connection:
        rows = connection.execute(
            "SELECT instrument_version, device_category, tasks_attempted_json, route_answer, answers_json "
            "FROM research_responses ORDER BY submitted_at_utc, response_id"
        ).fetchall()
        observations = connection.execute(
            "SELECT task_id, completion_state, duration_seconds FROM research_task_observations "
            "ORDER BY task_id, created_at_utc, observation_id"
        ).fetchall()
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "research_session_observations" in tables:
            observations += connection.execute(
                "SELECT task_id, completion_state, duration_seconds FROM research_session_observations "
                "ORDER BY task_id, created_at_utc, observation_id"
            ).fetchall()

    item_counts: dict[str, dict[str, Any]] = {}
    for question_id in sorted(QUESTION_IDS, key=lambda q: int(q[1:])):
        applicable = answered = missing = not_observed = 0
        distribution = {str(n): 0 for n in range(1, 6)}
        numeric: list[int] = []
        answer_counts: Counter[str] = Counter()
        for row in rows:
            task_codes = _tasks_for(row)
            if not _is_applicable(question_id, task_codes):
                continue
            applicable += 1
            answers = _answers_for(row)
            if question_id not in answers:
                missing += 1
                continue
            value = answers[question_id]
            answered += 1
            if question_id in LIKERT_IDS:
                if value == "N/A":
                    not_observed += 1
                elif value in distribution:
                    distribution[value] += 1
                    numeric.append(int(value))
                else:
                    raise ReportingError(f"Invalid stored rating for {question_id}")
            else:
                answer_counts[value] += 1
        item_counts[question_id] = {
            "applicable": applicable,
            "answered": answered,
            "missing": missing,
            "not_applicable": len(rows) - applicable,
            "not_observed_not_applicable_answer": not_observed,
            "rating_distribution_1_to_5": distribution if question_id in LIKERT_IDS else None,
            "rating_mean": round(statistics.mean(numeric), 3) if numeric else None,
            "rating_median": statistics.median(numeric) if numeric else None,
            "answer_counts": dict(sorted(answer_counts.items())) if question_id not in LIKERT_IDS else None,
        }

    comprehension: dict[str, dict[str, int]] = {}
    for qid, key in COMPREHENSION_KEYS.items():
        counts = {"correct": 0, "incorrect": 0, "unanswered": 0}
        for row in rows:
            answer = _answers_for(row).get(qid)
            if answer is None:
                counts["unanswered"] += 1
            elif answer == key:
                counts["correct"] += 1
            else:
                counts["incorrect"] += 1
        comprehension[qid] = counts

    task_counts: Counter[str] = Counter()
    device_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    for row in rows:
        task_counts.update(_tasks_for(row))
        device_counts[row["device_category"]] += 1
        route_counts[row["route_answer"]] += 1

    observation_counts: dict[str, dict[str, Any]] = {}
    for task in sorted(TASKS):
        records = [r for r in observations if r["task_id"] == task]
        durations = [int(r["duration_seconds"]) for r in records if r["duration_seconds"] is not None]
        states = Counter(r["completion_state"] for r in records)
        unknown_states = set(states) - OBSERVATION_STATES
        if unknown_states:
            raise ReportingError(f"Unknown stored observation state for {task}")
        observation_counts[task] = {
            "observations": len(records), "completion_states": dict(sorted(states.items())),
            "duration_values_available": len(durations),
            "duration_median_seconds": statistics.median(durations) if durations else None,
        }

    versions = Counter(row["instrument_version"] for row in rows)
    if any(version != INSTRUMENT_VERSION for version in versions):
        raise ReportingError("Database contains an instrument version not supported by this report")
    context_items = {
        "device": {"responses": len(rows), "answer_counts": dict(sorted(device_counts.items()))},
        "tasks": {"responses": len(rows), "answer_counts": dict(sorted(task_counts.items())),
                  "note": "Counts are task selections; one response may select multiple tasks."},
        "route": {"responses": len(rows), "answer_counts": dict(sorted(route_counts.items()))},
    }
    return {
        "data_classification": "UNVERIFIED DATA ORIGIN",
        "instrument_version": INSTRUMENT_VERSION,
        "submitted_responses": len(rows),
        "item_counts": item_counts,
        "context_item_counts": context_items,
        "comprehension": comprehension,
        "tasks_selected_counts": dict(sorted(task_counts.items())),
        "device_counts": dict(sorted(device_counts.items())),
        "route_counts": dict(sorted(route_counts.items())),
        "observations_by_task": observation_counts,
        "qualitative_feedback_count": sum(
            bool(_answers_for(row).get(qid, "").strip()) for row in rows for qid in TEXT_IDS
        ),
        "note": "Aggregate summaries only. Conditional questions are counted only when the associated task was selected.",
    }


def safe_csv_cell(value: Any) -> str:
    """Neutralize spreadsheet formula prefixes, including whitespace-prefixed ones."""
    cell = "" if value is None else str(value)
    probe = cell.lstrip(" \t\r\n\ufeff")
    if probe.startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
        return "'" + cell
    return cell


def _safe_output_directory(output_dir: Path) -> Path:
    path = Path(output_dir).expanduser().resolve()
    try:
        path.relative_to(PROJECT_ROOT)
    except ValueError:
        pass
    else:
        raise ReportingError("Output must be outside the project repository and public directories")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def _write_csv(path: Path, header: list[str], rows: list[list[Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([safe_csv_cell(cell) for cell in header])
        writer.writerows([[safe_csv_cell(cell) for cell in row] for row in rows])
    try:
        path.chmod(0o600)
    except OSError:
        pass


def _bar_chart(title: str, values: dict[str, int]) -> str:
    maximum = max(values.values(), default=0)
    parts = [f'<section class="chart"><h3>{html.escape(title)}</h3>']
    if not values:
        parts.append('<p class="muted">No observations.</p>')
    for label, value in values.items():
        width = (value / maximum * 100) if maximum else 0
        parts.append(f'<div class="barrow"><span>{html.escape(label)}</span><div class="track"><i style="width:{width:.2f}%"></i></div><b>{value}</b></div>')
    parts.append("</section>")
    return "".join(parts)


def render_html(summary: dict[str, Any]) -> str:
    """Create a self-contained aggregate report; no response text/IDs are embedded."""
    charts = [_bar_chart("Device category", summary["device_counts"]),
              _bar_chart("Tasks selected", summary["tasks_selected_counts"]),
              _bar_chart("Reported route", summary["route_counts"])]
    for qid, item in summary["item_counts"].items():
        distribution = item["rating_distribution_1_to_5"]
        if distribution is not None and any(distribution.values()):
            charts.append(_bar_chart(f"{qid} rating distribution (1–5)", distribution))
    comp_rows = "".join(
        f'<tr><th>{html.escape(qid)}</th><td>{counts["correct"]}</td><td>{counts["incorrect"]}</td><td>{counts["unanswered"]}</td></tr>'
        for qid, counts in summary["comprehension"].items()
    )
    item_rows = "".join(
        f'<tr><th>{html.escape(qid)}</th><td>{x["applicable"]}</td><td>{x["answered"]}</td><td>{x["missing"]}</td>'
        f'<td>{x["not_observed_not_applicable_answer"]}</td><td>{"—" if x["rating_mean"] is None else x["rating_mean"]}</td>'
        f'<td>{"—" if x["rating_median"] is None else x["rating_median"]}</td></tr>'
        for qid, x in summary["item_counts"].items()
    )
    obs_rows = "".join(
        f'<tr><th>{html.escape(task)}</th><td>{x["observations"]}</td><td>{html.escape(json.dumps(x["completion_states"], ensure_ascii=False))}</td>'
        f'<td>{"—" if x["duration_median_seconds"] is None else x["duration_median_seconds"]}</td></tr>'
        for task, x in summary["observations_by_task"].items()
    )
    classification = summary.get("data_classification", "UNVERIFIED DATA ORIGIN")
    synthetic_banner = (f'<p class="synthetic">{html.escape(classification)}</p>'
                        if classification == SYNTHETIC_LABEL else "")
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WiseLanka research evaluation — local summary</title><style>
body{{font:16px/1.5 system-ui,sans-serif;color:#17324d;background:#f4f7fb;margin:0}}main{{max-width:1100px;margin:auto;padding:2rem}}h1{{color:#123a63}}.badge{{background:#fff3d6;padding:.8rem;border-left:4px solid #d99a16}}.synthetic{{background:#9e1b1b;color:white;font-weight:800;padding:1rem;border-radius:8px;text-align:center;letter-spacing:.04em}}.metric{{display:inline-block;background:white;border-radius:12px;padding:1rem 1.4rem;margin:.4rem;box-shadow:0 2px 8px #123a6318}}.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem}}.chart,table{{background:white;border-radius:10px;padding:1rem;box-shadow:0 2px 8px #123a6318}}.barrow{{display:grid;grid-template-columns:minmax(90px,auto) 1fr 2rem;align-items:center;gap:.5rem;margin:.4rem 0;font-size:.9rem}}.track{{height:12px;background:#e7edf4;border-radius:6px;overflow:hidden}}.track i{{display:block;background:#148a91;height:100%}}table{{border-collapse:collapse;width:100%;margin:1rem 0;padding:0}}th,td{{text-align:left;border-bottom:1px solid #e1e8ef;padding:.55rem}}.muted,footer{{color:#536b80}}.scroll{{overflow-x:auto}}@media(max-width:600px){{main{{padding:1rem}}th,td{{padding:.4rem;font-size:.88rem}}}}
</style><main><h1>WiseLanka research evaluation</h1>{synthetic_banner}<p class="badge"><strong>Private local report.</strong> Aggregate summaries only; no response IDs or written feedback are included. This report is not evidence of educational effectiveness or participant representativeness.</p>
<div class="metric"><strong>{summary["submitted_responses"]}</strong><br>submitted responses</div><div class="metric"><strong>{summary["qualitative_feedback_count"]}</strong><br>non-empty feedback fields</div>
<p>Instrument: <code>{html.escape(summary["instrument_version"])}</code></p><div class="charts">{"".join(charts)}</div>
<h2>Question response accounting</h2><p>Conditional items use task-based applicability. “Missing” means applicable but unanswered. “Not observed” is the explicit N/A response. Non-applicable items are excluded.</p><div class="scroll"><table><thead><tr><th>Item</th><th>Applicable</th><th>Answered</th><th>Missing</th><th>N/A</th><th>Mean rating</th><th>Median rating</th></tr></thead><tbody>{item_rows}</tbody></table></div>
<h2>Comprehension items</h2><p>Exact-match answer key counts; this author-defined check is not a validated learning measure.</p><div class="scroll"><table><thead><tr><th>Item</th><th>Keyed answer</th><th>Other answer</th><th>Unanswered</th></tr></thead><tbody>{comp_rows}</tbody></table></div>
<h2>Task observations</h2><div class="scroll"><table><thead><tr><th>Task</th><th>Records</th><th>Completion states</th><th>Median duration (seconds)</th></tr></thead><tbody>{obs_rows}</tbody></table></div>
<footer>Generated from a read-only SQLite connection. Self-reported usefulness, comprehension, software correctness, and independently judged recommendation relevance are distinct measures and are not combined into an overall accuracy score.</footer></main></html>'''


def generate_report(database: Path, output_dir: Path, *, synthetic_demo: bool = False) -> dict[str, Path]:
    summary = calculate_summary(database)
    if synthetic_demo:
        summary["data_classification"] = SYNTHETIC_LABEL
    out = _safe_output_directory(output_dir)
    json_path = out / "summary.json"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    html_path = out / "report.html"
    html_path.write_text(render_html(summary), encoding="utf-8")
    label = summary["data_classification"]
    _write_csv(out / "item_summary.csv",
               ["item_id", "applicable", "answered", "missing", "not_applicable", "not_observed_not_applicable_answer", "rating_distribution_1_to_5", "mean", "median", "data_classification"],
               [[qid, x["applicable"], x["answered"], x["missing"], x["not_applicable"],
                 x["not_observed_not_applicable_answer"], json.dumps(x["rating_distribution_1_to_5"]), x["rating_mean"], x["rating_median"], label]
                for qid, x in summary["item_counts"].items()])
    _write_csv(out / "comprehension_summary.csv", ["item_id", "correct", "incorrect", "unanswered", "data_classification"],
               [[qid, *counts.values(), label] for qid, counts in summary["comprehension"].items()])
    _write_csv(out / "task_observations.csv", ["task_id", "observations", "completion_states", "duration_values_available", "median_duration_seconds", "data_classification"],
               [[task, x["observations"], json.dumps(x["completion_states"]), x["duration_values_available"], x["duration_median_seconds"], label]
                for task, x in summary["observations_by_task"].items()])
    # Free text is intentionally separate from the aggregate HTML, without response IDs.
    # It remains potentially identifying; the restricted output requires manual review.
    with closing(_readonly_connection(database)) as connection:
        records = connection.execute("SELECT answers_json FROM research_responses ORDER BY submitted_at_utc, response_id").fetchall()
    feedback = [[qid, _answers_for(row).get(qid, "")] for row in records for qid in sorted(TEXT_IDS) if _answers_for(row).get(qid, "").strip()]
    _write_csv(out / "qualitative_feedback_for_manual_review.csv", ["question_id", "feedback_text_no_response_id", "data_classification"],
               [[qid, text, label] for qid, text in feedback])
    for path in out.iterdir():
        if path.is_file():
            try:
                path.chmod(0o600)
            except OSError:
                pass
    return {"html": html_path, "summary": json_path, "items_csv": out / "item_summary.csv",
            "comprehension_csv": out / "comprehension_summary.csv", "observations_csv": out / "task_observations.csv",
            "qualitative_csv": out / "qualitative_feedback_for_manual_review.csv"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a private, local, read-only WiseLanka research summary")
    parser.add_argument("--database", required=True, type=Path, help="Explicit path to an existing research SQLite database")
    parser.add_argument("--output-dir", required=True, type=Path, help="Explicit output directory outside the project repository")
    parser.add_argument("--synthetic-demo", action="store_true",
                        help="Label every output SYNTHETIC — NOT REAL PARTICIPANT RESEARCH DATA")
    args = parser.parse_args(argv)
    try:
        paths = generate_report(args.database, args.output_dir, synthetic_demo=args.synthetic_demo)
    except (ReportingError, OSError, sqlite3.Error) as exc:
        parser.error(str(exc))
    print(f"Local HTML report: {paths['html']}")
    print("Qualitative comments are in a separate restricted CSV; review for identifying content before sharing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
