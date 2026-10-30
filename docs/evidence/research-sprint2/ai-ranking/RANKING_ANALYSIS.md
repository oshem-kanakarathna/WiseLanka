# Hybrid ranking findings — Research Sprint 2B

Executed30October2026 on checkpoint `a8c67caed5111137989767dea28e248e01a6c19e`, API0.6.0. No production/rule/model changes or training. The preceding checkpoint was reviewed before committing: original Sprint2A evidence stayed byte-identical, completeness tests distinguish unknown/false/true/invalid values, and old count-failure fixtures now supply the completeness declaration they require. Download caches, screenshot binaries, backups and unrelated academic preparation were excluded from that local commit; no push.

## Executed comparison and scenario provenance

**21 valid synthetic scenarios**:9 reused development cases and12 newly frozen evaluator-authored follow-ups. **63 comparator rows**, **1,890 warm measurements** (30 per case/method after3 warmups), and **15 fresh-process workers** (5 per method). Methods: current grouped deterministic personalisation order, existing custom TF–IDF/cosine, frozen MiniLM ONNX cosine. All use identical per-scenario candidate IDs, academic states and full11-programme embedding/TF–IDF corpus. The candidate pool is the production pool, not every possible programme in every scenario.

No scenario has an independent reference ranking. New follow-ups were frozen before observing outputs but designed with catalogue/implementation knowledge; none is claimed independently designed or a blind held-out case. Existing development cases were exposed during implementation and cannot become held-out merely by rerunning them. Comparator values below are changes, not accuracy or improvement.

## Observed rank differences

| Pair | All21: full order / top1 / ordered top3 differ | Development9 | Follow-up12 |
|---|---|---|---|
| Deterministic vsTF–IDF |13 / 10 / 13 |5 / 5 / 5 |8 / 5 / 8 |
| Deterministic vsMiniLM |19 / 14 / 17 |8 / 7 / 8 |11 / 7 / 9 |
| TF–IDF vsMiniLM |19 / 8 / 18 |8 / 3 / 8 |11 / 5 / 10 |

These are per-scenario counts. All21 include an empty-interest fallback and a singleton pool; no meaningful ranking discrimination is possible in the latter. Candidate-pool sizes:14 cases with5 candidates,4 with11,2 with6,1 with1. Multiple cases reuse the same fictional academic profile and are not independent participant observations.

### Literal/task-paraphrase pairs: favourable and inconclusive behaviour

- Engineering F05→F06: TF–IDF top1 changes PRG0009(Peradeniya Engineering)→PRG0001(Moratuwa IT); MiniLM remains PRG0009. This shows different response to wording, not a measured relevance gain. F06 semantic maximum is only0.044523; it is not calibrated confidence.
- Vocational F07→F08: TF–IDF changes PRG0011(UoVT Mechatronics)→PRG0007(IIT AI/Data Science); MiniLM remains PRG0010(UCJ HND Mechatronics). No judge has rated which route best serves the fictional learner.
- Business F03→F04: all methods retain PRG0008(OUSL Management) at top1. This pair supplies no top1 evidence that the semantic component adds value.
- IT F01→F02: MiniLM changes PRG0009(Engineering)→PRG0008(Management), while TF–IDF changes PRG0009→PRG0001. These are not automatic semantic successes. The production A/L pool excludes the three IIT degrees without recorded direct-entry rules; sparse title-level descriptions and candidate restriction can affect apparent IT matching. Independent judgement is needed rather than declaring an intuitively preferred label correct after the fact.

The lexical implementation has no stopword removal/stemming. Function words can contribute strongly to short programme titles: F06 overlaps through “in”, and F08 through “and”. These are implementation-specific baseline weaknesses, not proof that all TF–IDF methods are inferior. Do not tune this frozen baseline after seeing the results and then call the same cases held-out.

The unfamiliar/noise caseD08 gives all-zero TF–IDF and retains baseline ties, while MiniLM returns nonzero/negative similarities and putsPRG0003 first (0.072493). The semantic method does not abstain merely because human-meaningful intent is absent. This demonstrates that an available numeric score is not evidence of useful understanding.

## Policy compliance, stability and failure behaviour

All63 comparator outputs and all1,890 repeated calls preserved exact candidate membership, per-ID academic status and MET→NOT_ASSESSED→NOT_MET group order. Input objects were not mutated. Repeated ordered IDs and six-decimal scores were identical within each scenario/method cell.

F11 explicitly has aMET foundation route, an unknown Management route and fourNOT_MET degree routes. Engineering receives higher similarity than the foundation (MiniLM0.243827 versus0.169571;TF–IDF0.433377 versus0), but remains below theMET and unknown groups. F12 likewise keeps theMET foundation ahead of the more text-related unknown Business route. This preserves policy authority while potentially limiting global-interest ordering; usefulness of that trade-off remains a human research question.

The empty-preference caseD01 explicitly usesNO_PREFERENCE rule-based fallback for all requested modes; it is not genuine semantic execution. An isolated process configured to a nonexistent local model directory returnedLOCAL_MODEL_UNAVAILABLE/RULE_BASED_FALLBACK, null relevance scores and the grouped deterministic order. Model assets were not deleted or altered. Empty candidate input givesNO_CANDIDATES; invalid method raises the expectedValueError. No unhandled comparison exception occurred. Failure configuration is a labelled simulation of model absence, not an observed service outage.

## Measured runtime and resources

Warm figures pool600 actual-mode measurements per method (20 nonempty-query scenarios×30); D01's fallback calls are excluded. Per-scenario figures and all samples remain available.

| Existing ranking mode | Warm median | Warm p95 | Fresh-process first-rank median | Explicit model-load median | Worker peakRSS median |
|---|---:|---:|---:|---:|---:|
| Deterministic |0.467ms |0.625ms |0.761ms |Not loaded |14.06MiB |
| TF–IDF |0.466ms |0.601ms |0.751ms |Not loaded |13.83MiB |
| MiniLM |3.254ms |4.674ms |81.074ms |285.271ms |318.83MiB |

Fresh-process total wall medians:38.34ms deterministic,38.05ms TF–IDF,426.47ms semantic. First-rank excludes separately measured model load/import; total wall includes process startup. Workers use the sameF01 input, not the varied warm scenario pool. Files may be OS-cache-warm; no system cache was flushed. PeakRSS is the isolated ranking worker's high-water memory, not a whole FastAPI service measurement or model-only allocation. See raw/cold-workers.json for all5 replicates.

Measurements are from one shared AppleM4/10-core/16GiB machine with ONNXCPU intra/inter threads1. Rank-function timing includes existing CSV/text/lexical/sort work; it excludes academic assessment, candidate generation, browser, HTTP and model download. Deterministic mode also computes TF–IDF diagnostics in the existing implementation, so this is not a benchmark of a pure rule algorithm versus isolated vector maths. Do not compare these4.674ms ranking-only observations with WP5's whole-request p95 as an optimisation claim.

## Interpretation and next decision

MiniLM produces measurable ordering changes, handles some paired wording differently and runs locally at modest warm latency on the tested machine. It also adds startup/memory/dependency cost, returns scores for uninterpretable text and has no demonstrated independent relevance advantage here. These findings establish operational feasibility and behaviour, not that its complexity is educationally worthwhile or that it should be removed.

Independent relevance evaluation remains necessary. A method-blinded, unfilled pack is prepared:127 case/candidate pairs per reviewer. That is127 possible judgements, not127 people or completed ratings. No nDCG,MAP,precision,recommendation accuracy,user satisfaction or superiority statistic was computed. Next: obtain the applicable ethics/supervisor determination, collect legitimate independent judgements without exposing methods/ranks/scores, then assess whether the incremental relevance benefit justifies the observed cost. Keep scenario/pool/model snapshots fixed and report unfavourable findings. No reviewer recruitment or collection occurred in this sprint.
