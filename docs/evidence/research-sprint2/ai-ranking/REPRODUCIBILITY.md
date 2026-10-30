# Reproducing Research Sprint 2B

## Identity and prerequisites

Research checkpoint: `a8c67caed5111137989767dea28e248e01a6c19e`; declared application version0.6.0. PartA committed the reviewed correction/tests and small textual Sprint2A/2A.1 evidence; actual downloaded source caches, binaries and unrelated academic changes were excluded. PartB does not change that code snapshot. BASELINE.json records all20 CSV hashes, model lock and actual artifact hashes, package versions, interpreter/platform, exact inference configuration and preservation hashes. The tracked application/data must match the checkpoint; the workspace also contains unrelated uncommitted academic preparation, which was preserved.

Actual interpreter: `/private/tmp/wiselanka-repro-venv/bin/python`, Python3.9.6/macOS15.5arm64. Hardware read via authorised read-only sysctl: AppleM4,10 logical CPUs,17,179,869,184 bytes RAM(16GiB). No serial numbers or device identifiers collected. Optional AI packages/assets were already installed; no dependency or model installation was changed during this experiment. The dependency list in BASELINE.json and raw/pip-freeze.txt is observational, not a claim of every supported OS.

Model: `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, Apache-2.0 model card/lock. Normal assets remain in ignored `.models/<revision>/`, not this evidence folder or Git. Inference is local CPU; model setup and the frozen model lock are already documented in WP3. No learner query is sent to an external inference service.

## Commands and outputs

From the repository root, with the verified AI/test environment and local model provisioned:

```sh
/private/tmp/wiselanka-repro-venv/bin/python docs/evidence/research-sprint2/ai-ranking/run_experiment.py
python3 docs/evidence/research-sprint2/ai-ranking/analyse_results.py
```

The actual first command exited0; raw/run-stdout.txt and raw/run-stderr.txt are preserved. It produced21 scenario comparisons across3 requested modes,63 rows,1,890 warm samples and15 fresh-process workers. raw/cold-*-stderr.txt preserves each worker's stderr; cold-workers.json includes each zero exit and measured wall time. The expected invalid-methodValueError is a functional probe, not an unhandled failure. No full regression suite was rerun for this research-only harness; the correction's228/36/live verification is separate preserved evidence.

`run_experiment.py` checks the scenario/protocol hashes before running, snapshots production candidates, calls existing ranker modes on deep copies, asserts policy/membership/immutability, measures the fixed repetition schedule and runs isolated fallback probes. `analyse_results.py` derives split-wise order differences, runtime summaries, pair comparisons and unfilled blinded packs. SUMMARY.json contains no relevance-quality metric or synthetic label.

run_experiment.py can also run a single fresh worker using `--worker deterministic`, `--worker tfidf` or `--worker semantic`; `--missing-model` is used with a deliberately nonexistent WISELANKA_MODEL_DIR in the failure probe. The real model directory was never deleted or altered. Fresh-process workers inherit the same fixed benchmark inputF01 in raw/benchmark-input.json. Absolute model/interpreter paths identify the tested machine, not universal installation paths.

## What was fixed and measured

- SCENARIO_REGISTER.csv was frozen before comparison, distinguishing9 development-exposed from12 evaluator-authored follow-ups. No output-derived reference answer exists.
- raw/frozen-candidates.json captures profiles/items in restored deterministic input order. Current personalisation's initial semantic call is candidate setup, not a target ranking or a timed comparator. The same pool/partition maps feed all3 methods.
- Documents are the actual full11-programme corpus in raw/catalogue-documents.json. Tokenisation/mean-pooling/normalisation/CPU-thread/cache settings are in BASELINE.json. TF–IDF uses the same corpus and the production custom weighting.
- Three warmups per scenario/method precede30 measured calls each. All63 jobs are shuffled per repetition with seed20261030. raw/warm-samples.csv retains every duration, method, policy assertion and order/score signature. Global p95 uses the nearest-rankceil(0.95n) definition; per-cell rows retain their own p95. D01'sNO_PREFERENCE fallbacks are excluded from actual-mode pooled runtime summaries.
- Cold measurements use5 separate processes per method. Model load is timed separately before the first semantic rank call, which also builds document embeddings. Import/process wall/second-call timings are in cold-workers.json. No OS cache flush, clean-machine startup, download, service/network or concurrency test occurred. All15 cold-worker orders/scores matched their corresponding warmF01 output; raw/cold-stability-checks.json records that comparison.
- Memory is macOS process peakRSS divided by1024², not current/averageRSS, model-only bytes or complete service footprint. The parent process also held a model; worker high-water values should not be added as physical memory allocations.

## Preserve the observed run

Do not rerun in this evidence directory: commands write local outputs. Copy the full ai-ranking directory to a sibling replay directory at the same depth under docs/evidence/research-sprint2, then run that copy. Current scripts derive repository root from that depth. For the same workspace, original preservation hashes must match. A different machine/path/dependency set requires a separately documented replication baseline and verified identical computational inputs; do not silently edit these original JSON identities and call it the same run. Timings will vary with host state.

The generated reports are interpretations of this saved run, not live-computed claims. Preserve first-run raw outputs and unfavourable cases. Do not substitute oldWP5 rankings when comparing methods after the completeness correction: all3 comparators here use the current same assessment state.

## Blinded review material

BLANK_RELEVANCE_REVIEW.csv is packA's127-pair blank response sheet. blinded-review/CARDS_A.md andCARDS_B.md independently permute case/candidate order with seeds20261030/20261031; matchingBLANK_A/B.csv sheets contain no ratings. raw/blinding-researcher-key.json maps opaque IDs to scenarios/programmes and must be withheld from judges, together with method outputs, analysis and scores. Send only the assigned card/sheet/protocol after applicable ethics approval; no reviewers were contacted here.

Judging should address interest relevance, not admission certainty. Use0–3 only when justified, orUNJUDGEABLE; preserve reasons and independent initial ratings. Empty/noise cases are robustness-only; future analysis must retain exclusions and actual academic-group sizes. Independent labels on these exposed cases would not create an independently designed held-out study. No nDCG/MAP/precision/relevance accuracy has been computed.

## Integrity

The final preservation check compares all protected tracked files,20 CSVs,actual model hashes and both backups. No source/eligibility/ranker/model/academic draft changes, recruitment, dissertation rewrite or remote push occurred in PartB. The only Git commit in this task is the authorised PartA checkpoint. PartB evidence remains uncommitted for review.
