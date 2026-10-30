# Sprint 2A.1 — examination completeness correction

## Cause and minimum change

EC08 was reproduced from the exact original request before editing. ROOT_CAUSE_BEFORE_EDIT.md and raw/before-reproduction.json preserve the investigation. Omitted or empty completeness became `{}` in the request contract; failed count predicates then used `complete.get(level, True)`, treating unknown completeness as a confirmed full examination. The same default affected O/L pass/credit counts and A/L pass/approved-subject counts. Named-subject absence already required an explicit completeness declaration.

The production change is limited to `backend/app/eligibility/engine.py`: failed counts now remain NOT_ASSESSED unless the relevant level has explicit true. The unknown-count explanation says completeness is not confirmed. One stale comment in `backend/app/personalisation/models.py` was updated. CSV thresholds, sources, qualification evaluation, schema validation, numerical scoring and ranking algorithms were not changed. Existing canonical consumers also propagate the corrected state to recommendations and guided support.

Sufficient positive counts still satisfy their predicates without a completeness declaration. Supplied mandatory subject grades below the minimum still establish NOT_MET. An explicitly complete examination with an insufficient count remains NOT_MET. No grade authentication or admission guarantee is inferred.

| Input / context | Before | After |
|---|---|---|
| EC08, five O/L passes, flag omitted or empty dictionary | NOT_MET | NOT_ASSESSED |
| Same grades, explicit false | NOT_ASSESSED | NOT_ASSESSED |
| Same grades, explicit true | NOT_MET | NOT_MET |
| Null top-level flag, null level value, empty-string value | HTTP422 | HTTP422; invalid input is not an academic decision |
| A/L partial pass count or approved-subject count, omitted flag | NOT_MET | NOT_ASSESSED |
| Qualification-only self-report | NOT_ASSESSED | NOT_ASSESSED |

Direct engine None/empty completeness follows the same conservative interpretation. Unrelated examination-level flags cannot confirm completeness of the assessed level. Empty examination evidence remains unknown. Positive-count regressions protect six-subject compatibility; existing nine-subject and live profiles remain covered.

## Tests and controlled comparison

Added23 parameterised integration/engine regression cases in `tests/integration/test_exam_completeness.py`, covering both eligibility and personalised endpoints, missing/empty/false/true/unrelated-level flags, invalid null/empty-string values, both A/L count kinds, known low grades, positive counts, empty examination evidence and qualification-only uncertainty.

The new tests first produced9 failures/14 passes against the original engine. The first full run after the correction produced4 failures/224 passes: two old fixtures asserted count failure without declaring completeness, and two recommendation tests classified absent approved subjects as confirmed ineligibility. Those four tests were retained and revised explicitly: complete-count failure fixtures now declare true, while undeclared unrelated lists expect unknown. Their grade inputs, scores and qualifying-profile checks were not removed to hide a failure. The final tests confirm the approved conservative semantics.

| Verification actually executed | Result |
|---|---|
| Complete backend suite | **228 passed** |
| Complete browser suite | **36 passed** |
| Original + WP1–WP4 live workflows | **5 passed** against a fresh API process |
| EC08 over real HTTP | NOT_ASSESSED; empty failed list |
| CSV integrity | Passed |
| Frozen45-case replay | **43 agreements / 2 disagreements** |
| Decision changes against original replay | **EC08 only**, NOT_MET → NOT_ASSESSED |

The original Sprint2A evidence still records42 agreements/3 disagreements and is unchanged. The separate recheck/ directory uses byte-identical SCENARIO_DEFINITIONS.csv and ORACLE_LOCK.json; it updates only the working-code preservation snapshot needed to run the corrected source. controlled_recheck.py imports the original harness and redirects output, without editing that harness. CONTROLLED_COMPARISON.json identifies the only changed decision. This is a controlled regression comparison on exposed synthetic cases, not new independent educational validation or a model-quality improvement.

EC39 andEC40 still differ because age and Common General Paper reference facts are absent from the API contract. The foundation rule-citation gap and other Sprint2A limitations remain unresolved; they are outside this correction.

## Reproduction and preservation

The application remains declared version0.6.0 at HEADa19b68fa5b872fa9639eb653c3b528e803071a78 plus the recorded uncommitted patch. application-and-test-changes.patch and CHANGE_MANIFEST.json identify the exact working-tree correction, including the separately hashed new test file. The tests ran with `/private/tmp/wiselanka-repro-venv/bin/python`, Python3.9.6/macOS15.5; dependencies were not changed.

From the repository root:

```sh
/private/tmp/wiselanka-repro-venv/bin/python -m pytest tests/ -q
/private/tmp/wiselanka-repro-venv/bin/python -m unittest discover -s frontend/browser_tests -p 'test_*.py'
/private/tmp/wiselanka-repro-venv/bin/python docs/evidence/research-sprint2/completeness-correction/controlled_recheck.py
/private/tmp/wiselanka-repro-venv/bin/python docs/evidence/research-sprint2/completeness-correction/verify_live.py
```

Use a separately copied correction evidence directory for future reruns to preserve these observations. The live verifier starts a fresh API process, redirects every screenshot/output away from old WP evidence and stops only processes it started. It requires local model assets and a Chromium-capable environment. Original outputs and exit codes are retained in raw/, LIVE_RESULTS.json and VERIFICATION.json. The initial browser run failed at sandbox Chromium launch; the authorised retry passed. The initial replay wrapper lacked its new raw/ output directory; that wrapper setup error and the corrected run are both retained. Neither was an application result silently corrected.

Preservation checks cover the full original educational-correctness directory, all20 CSVs, existing academic materials, previous WP evidence and both backups. No original result/oracle was revised, no educational data was changed, and no commit or push was performed. Stop for review before any other fix.
