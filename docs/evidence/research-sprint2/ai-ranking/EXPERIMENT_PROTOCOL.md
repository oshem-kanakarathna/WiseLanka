# Frozen hybrid-ranking experiment — Research Sprint 2B

Protocol/scenarios frozen30October2026 before comparison outputs. Checkpoint `a8c67caed5111137989767dea28e248e01a6c19e`, API0.6.0. No tuning, retraining, new eligibility rules, independent labels or participant collection. This is descriptive algorithm/system evaluation, not a superiority trial.

## Scenario separation and candidate construction

SCENARIO_REGISTER.csv contains9 WP3/WP5 development-exposed cases and12 newly authored follow-up cases. Follow-ups cover IT, Business, Engineering, vocational/early-career routes, four literal/task-paraphrase pairs, a singleton O/L pool and mixed MET/unknown/unmet partitions. All21 profiles are synthetic. The evaluator knows the catalogue/implementation; new cases are prospectively frozen but **not independently designed or blind held-out evidence**. No target programme order is supplied or inferred from any method. Empty/noise development queries are robustness-only.

Use current personalisation for exactly the production candidate pool, then restore `ranking.legacy_order` from metadata and remove pre-existing relevance fields. Candidate generation's default semantic pass is setup only and excluded from comparator timing. This does not use a model output as a reference answer: the common baseline input order is the preserved deterministic personalisation order. Each comparator receives the identical deep-copied items, profile, catalogue and academic assessments. Save those inputs before measurement. Do not expand pools selectively per method; specifically disclose that an O/L-only learner can have just one available candidate.

## Comparators and interpretation

Call the existing `rank_recommendations` with deterministic,tfidf,semantic. All are constrained by the same MET→NOT_ASSESSED→NOT_MET partition ordering. Deterministic preserves baseline order within partitions; this grouped comparator is distinct from ungrouped historical legacy output. TF–IDF fits lexical corpus statistics on all11 programme documents, not learner preferences. Semantic uses frozen pretrained all-MiniLM-L6-v2 revision1110a243fdf4706b3f48f1d95db1a4f5529b4d41, localONNX CPU with checksum-locked artifacts. No training or automatic learning occurs.

Programme text is the existing title/subject/domain/qualification-type concatenation, not full prospectus descriptions. Preference text is the existing interests/intention/optional career title, limited to1000characters. Model tokenisation truncates at256, uses attention-masked mean pooling andL2normalisation. CPU intra/inter threads1; document-embeddingLRU4 and encoderLRU1. Similarities are not probabilities of eligibility, admission or career success. Score scales are method-specific and must not be compared as calibrated relevance.

Record requested/actual method, fallback state/reason, original candidate IDs, partitions, ordered IDs, rounded scores, global/group top1/top3 and invariant checks. Assertions: exact pool membership/uniqueness, unchanged per-ID academic states, nondecreasing partition priority, no input mutation. Keep actual exceptions/fallbacks visible. Empty preference invokes explicitNO_PREFERENCE rule fallback; unavailable model is tested in a separate process with a nonexistent model directory, without deleting/changing weights. Empty candidate input and invalid method are separate functional probes, not relevance cases.

## Repeated measurements

AppleM4,10CPU cores,16GiBRAM; Python3.9.6/macOS15.5 arm64. Full versions/hashes/config are in BASELINE.json. Host is shared/non-isolated; no power-state or background-load control is claimed.

Warm: three warmup calls per scenario/method, then30 measured calls per scenario/method. Shuffle all63 scenario-method jobs within each repetition using seed20261030. Time the existing ranking function only with perf_counter: catalogue loading/query preparation/TF–IDF calculation/sorting and semantic query inference are included; academic evaluation, browser rendering and network excluded. Retain every sample and rank/score signature. Report per-cell median/p95/range, actual fallback and stability. Aggregate only after distinguishing actual semantic execution from empty-query fallback.

Cold: five fresh Python processes per method on the sameF01 pool/profile. Record module-import time, optional explicit model-load time, first rank call with empty document cache, subprocess wall time and process peakRSS. A second call in that worker is a cache-warm diagnostic. Cold performance is separate from warm30-repetition statistics. No model download, fresh dependency installation or complete FastAPI/browser startup is included. PeakRSS is a process high-water value, not model-only memory or additive allocation.

## Analysis and future relevance judgement

Report exact/full/top1/ordered-top3 changes by development/follow-up split, group composition and pair behaviour. Descriptive overlap/order differences are not recommendation accuracy. A changed or stable paraphrase result can have multiple interpretations without labels. Do not calculate nDCG,MAP,precision or superiority scores.

Prepare a method-blinded, seeded programme-card/blank-rating pack, using the same facts and queries but hiding method identities, ranks and scores. No filled ratings. Any later appropriately approved adult independent judging must preserve disagreements, source uncertainty, group sizes and unjudgeable cases. No participant or reviewer recruitment now. The experiment cannot establish relevance quality, usefulness, trust, educational outcomes or population generalisation.
