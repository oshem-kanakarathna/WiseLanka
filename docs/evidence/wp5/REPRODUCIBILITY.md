# Reproducibility and operating conditions

Actual fresh environment: Python 3.9.6, macOS 15.5 arm64, `/private/tmp/wiselanka-wp5-venv`. Exact optional-AI/test dependency lock installed successfully; `fresh-install.txt` retains the install output. Initial sandbox DNS restriction required network-authorised retry, not a package change. `pip-check.log` records installed dependency consistency. This verifies this platform, not all operating systems.

A separate fresh model directory `/private/tmp/wiselanka-wp5-model` was provisioned using the existing setup module with `DEFAULT_DIR` overridden to that temporary location. All three downloaded artifacts matched the lock. `provisioning-receipt.json` records actual hashes. Normal setup uses the ignored `.models/<revision>` directory. Model weights/caches remain excluded from Git.

Normal developer reproduction from repository root:

```sh
python3 -m venv .venv-wp5
.venv-wp5/bin/python -m pip install -r requirements-ai-lock.txt
.venv-wp5/bin/python scripts/setup_semantic_model.py
.venv-wp5/bin/python -m playwright install chromium
.venv-wp5/bin/python -m uvicorn backend.app.api.main:app --host 127.0.0.1 --port 8011
```

In another terminal start the static server (`python3 -m http.server 5500`) if not already running. The measured run reused the existing local static server and cached Chromium; it did not independently download Chromium again. Open `http://127.0.0.1:5500/frontend/pages/learner-profile.html` and configure the browser API base as appropriate for port 8011; normal default API port is 8000. Live scripts inject `window.WISELANKA_API_BASE` explicitly.

For the optional axe audit, download the pinned artifact to a temporary path:

```sh
curl -L https://unpkg.com/axe-core@4.10.3/axe.min.js -o /private/tmp/wiselanka-wp5-axe.min.js
```

Expected SHA256: `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`. The audit script verifies it. Use WISELANKA_AXE_PATH for another location. The downloaded third-party asset is not committed.

With both servers running, execute:

```sh
WISELANKA_API_BASE=http://127.0.0.1:8011 .venv-wp5/bin/python scripts/verify_wp5.py
```

This saves individual logs and exit codes in verification.json, including backend, browser, integrity, scenarios, ranker comparisons, all five live workflows, axe, HTTP/fallback timing and pip check. It returns nonzero on any check failure. To use a nondefault model directory set WISELANKA_MODEL_DIR for both server and runner. Historical reports remain in earlier WP folders; rerunning this runner refreshes WP5 evidence only. Absolute paths in saved command records identify this actual machine, not portability requirements.

## Runtime and failure recovery

MiniLM ONNX CPU inference is local and offline once provisioned. Model ID/revision/license and upstream provenance remain documented in docs/evidence/wp3/ and backend/app/relevance/model-lock.json. Frozen revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`; Apache-2.0 model card is included in the checksum-verified download. No model was trained on learner data. Dependencies and actual versions are in performance.json; no new runtime dependency was introduced for WP5.

Missing/corrupt model files or absent optional packages yield explicit RULE_BASED_FALLBACK. Missing model behaviour was exercised in an isolated subprocess; the valid server still returned SEMANTIC afterwards. Provision assets and restart a process that cached a failed load. Startup validates CSV integrity; missing or malformed knowledge data fails distinctly rather than masquerading as empty results. Existing tests exercise invalid grades, malformed requests and relationship errors. These checks are not a production availability or load-test guarantee.

Initial setup requires network access. Native speech may use browser-provider servers; local recommendation inference does not imply local speech processing. The simple local prototype has no accounts, durable learner store or production hardening claim. Avoid logging real learner profiles in research. A heuristic tracked-working-tree secret scan found no selected key patterns; it does not prove absence of every kind of sensitive data or inspect complete Git history. See security-review.json. Backups were excluded and preserved.

QA-only source inspection used pypdf 5.9.0 in a separate temporary environment; this is not an application dependency. Dataset file hashes are in dataset-sha256.json. Original signed academic/ethics documents remain unavailable and human research must wait for their review.
