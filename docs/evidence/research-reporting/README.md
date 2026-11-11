# WiseLanka local research reporting foundation

## Scope and safety

`backend.app.research.reporting` is a local, read-only analysis utility. It requires an explicit SQLite database path, uses SQLite `mode=ro` plus `query_only`, and refuses output directories inside the project repository (including the frontend/static tree). It adds no API route, dashboard, startup database initialization, or connection from the questionnaire. `RESEARCH_COLLECTION_ENABLED` remains `false`; the existing route still rejects submissions by default. Automated fixtures are synthetic and live in `tests/integration/test_research_reporting.py`.

Run it from the repository root, providing both paths explicitly:

```sh
RESEARCH_COLLECTION_ENABLED=false PYTHONPATH=. python -m backend.app.research.reporting \
  --database "$HOME/Library/Application Support/WiseLanka/research-responses.sqlite3" \
  --output-dir "$HOME/WiseLanka-private-report"
```

For a demonstration database built entirely from synthetic records, add `--synthetic-demo`. The HTML, JSON and every CSV row are then explicitly labelled `SYNTHETIC — NOT REAL PARTICIPANT RESEARCH DATA`. This flag is an operator-supplied provenance label; it does not inspect or certify the underlying records.

The database must already exist and contain the expected research tables. This command does not initialize it. The output directory is created with owner-only permissions where supported. Open `report.html` locally in a browser. The tool is intended for a researcher-controlled machine only; do not sync or publish its output. The qualitative CSV has free text without response IDs, but text may still identify a person. Review it manually in a restricted location before analysis or sharing. CSV values are neutralized against common spreadsheet formula injection prefixes.

## Instrument and scoring definitions

The supported version is `evaluation-prototype-v2-2026-10-31`. Questionnaire item IDs are Q5–Q29; context fields are device, tasks, and route. For Q6, Q7, Q14, Q15, Q16, Q17 and Q24, applicability is determined by the selected Task 1, 3, 2, 2, 4, 4 and 4 respectively. A conditional item not applicable to a response is excluded from its missing denominator. An applicable item absent from `answers` is missing. A Likert answer `N/A` (“Not observed / Cannot assess”) is counted separately from missing and from non-applicability. Means and medians use only numeric 1–5 values; N/A is never numerically imputed.

Comprehension keys are exact option-text matches, defined in `backend/app/research/reporting.py`: Q20 is the option saying checked requirements appear satisfied while additional admission conditions may apply; Q21 says more information is needed; Q22 says progression may be possible if stated conditions are satisfied; Q23 says to verify current requirements with official sources. Other selected options count as incorrect, and absent answers as unanswered. This is an author-defined descriptive rubric, not a validated psychometric instrument or a measure of learning gain.

The report keeps distinct constructs separate. Self-reported usefulness is a perception; comprehension items are responses to four author-defined questions; software correctness is established through technical tests against expected behavior; independently judged recommendation relevance requires separate blinded judgements. These cannot defensibly be collapsed into a single “accuracy” score.

## Output files

- `report.html`: aggregate counts, response accounting, ratings, comprehension summaries and task-observation summaries; no participant-level records, response IDs or feedback text.
- `summary.json`, `item_summary.csv`, `comprehension_summary.csv`, `task_observations.csv`: aggregate machine-readable outputs.
- `qualitative_feedback_for_manual_review.csv`: non-empty Q25–Q29 free-text values without response identifiers. This is restricted working material, not guaranteed anonymous data. Do not share before manual disclosure review and approval.

An empty database yields zero counts and an explanatory empty report. Existing observations summarize the current `research_task_observations` table and are linked to a response by `response_id`.

## Observation linkage limitation

In the current Phase 2 schema, `response_id` is generated when the questionnaire is submitted; the observation table requires that ID. Thus it can link observations entered after submission, but it cannot reliably link task observations captured before submission. Before an approved study records task observations, the design needs a random study-session UUID created before tasks begin, supplied to the observer workflow, and included in both the eventual response and each observation. A uniqueness/foreign-key constraint should enforce one session-to-response relationship, with access restricted to the researcher. Do not use names, email, date of birth, IP address, or real academic records as linkage keys. Implementing that session lifecycle is a separate schema/API decision and is not part of this reporting-only phase.

## Research data governance prerequisites

No retention duration or approval is presumed here. Before real collection, confirm the approved instrument and consent verification process, lawful retention period, who may access the database and exports, encrypted storage/backups, withdrawal cutoff and deletion process (including backups), and audit/logging policy with the supervisor and relevant university contacts. SQLite file permissions are not encryption. Do not enable collection or expose a dashboard as a consequence of generating reports.

## Tests

Focused synthetic tests:

```sh
PYTHONPATH=. pytest -q tests/integration/test_research_reporting.py
```

Full backend regression:

```sh
PYTHONPATH=. pytest -q tests
```

The tests cover aggregation, optional/missing values, task-dependent applicability, exact-key comprehension summaries, available observations, empty stores, read-only access, output location restriction and formula-safe CSV output. They do not validate educational outcomes, instrument validity, participant privacy in real comments, or human interpretation of findings.
