# WP3 closure — frozen semantic relevance and hybrid guidance

Date: 2026-10-29. WP2 checkpoint: `fa5d2c9`. WP3 remains uncommitted.
No WP4 features, feedback learning, paid service or Git push were introduced.

## Architecture and algorithm

The existing eligibility engine remains authoritative. After the existing
personalisation calculation, the new relevance module partitions candidates by
canonical academic status: MET, NOT_ASSESSED, NOT_MET. Only within-group ordering
uses similarity. Legacy eligibility fields and academic scores remain unchanged;
the UI uses canonical insight status, not similarity, for its academic label.
A programme with unmet requirements remains a development/alternative route, not
an eligible admission. Unknown requirements continue to require provider review.

Three methods can be reproduced with `rank_recommendations`:

1. Existing deterministic order, also recorded before grouping as `legacy_order`.
2. TF-IDF: raw term counts, smoothed IDF, L2-normalised cosine. Fit on the fixed
   active catalogue vocabulary; transform the preference text. This is corpus
   fitting, not learned learner preferences. No scikit-learn dependency is needed.
3. Frozen pretrained MiniLM embeddings: masked mean pooling, L2 normalisation,
   cosine similarity. Corpus vectors are cached by document tuple; query vectors
   are computed locally. Scores are checked for finiteness before clamping and
   rounding. Stable baseline positions break ties within academic groups.

Source-backed programme descriptors contain title, field, domain and qualification
type. They deliberately exclude eligibility outcomes, administrative notes and
unverified course/career narratives. These are short metadata descriptions, not
full syllabus documents. Inputs are explicit interests, an optional English career
intention (maximum 300 characters) and a selected career's recorded name. Combined
query text is capped at 1,000 characters and model input at 256 wordpieces.

The endpoint remains `/personalised-recommendations`. New fields are `ranking`
and per-item `relevance`; the old `assessment_method` is retained as a legacy
rule-based personalisation identifier. `ranking.method` identifies the actual
relevance method. Qualification-only profiles retain `recommendations=[]`; their
academic catalogue exploration is ranked and annotated separately. No award
verification or equivalence is inferred.

Empty preference input does not load the model or invent relevance. Missing
runtime, missing/checksum-invalid artifacts or inference failures produce explicit
RULE_BASED_FALLBACK/UNAVAILABLE with null semantic scores. Baseline order is retained
within the academic safety groups; overall order may differ from pre-group legacy
order. Model-loading failures are cached until process restart. Corrupt inference
results discard scores and cached embeddings; no invalid float reaches the API.

## Model provenance, licence and runtime

Model: `sentence-transformers/all-MiniLM-L6-v2`.
Pinned repository revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
Official model card:
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41

The downloaded model card declares English and Apache-2.0. The ONNX export,
tokenizer JSON and model card are checksum-locked in
`backend/app/relevance/model-lock.json`. The ONNX file is approximately 86 MiB.
Weights are under ignored `.models/`, not Git. Local CPU inference uses
numpy 1.26.4, onnxruntime 1.19.2 and tokenizers 0.20.3. Binary wheels installed and
ran on Python 3.9.6/macOS 15.5 Apple Silicon. No Python version change was needed.
Direct AI pins are in `requirements-ai.txt`; the complete tested environment is
captured in `requirements-ai-lock.txt`. ONNX is the approved encoder's export,
not a replacement model. This avoids installing a PyTorch training stack.

This model was trained externally. WiseLanka performs frozen inference; it does
not train or update a preference model. TF-IDF and deterministic methods are not
presented as supervised AI. No learner profile is sent to Hugging Face or another
external service. Only the explicit setup script uses the network to download
public artifacts. Runtime loading is local-only; profiles are not persisted as
feedback. Evaluation files contain synthetic profiles only.

## Reproducible setup

From the repository root, with the intended virtual environment activated:

```sh
python -m pip install -r requirements-dev.txt -r requirements-ai.txt
python scripts/setup_semantic_model.py
python -m uvicorn backend.app.api.main:app --host 127.0.0.1 --port 8000
```

Start the static frontend separately:

```sh
python -m http.server 5500 --bind 127.0.0.1
```

Open `/frontend/pages/learner-profile.html` on that frontend. Setup requires network
access once and verifies hashes against the committed lock. Restart the API after
installing dependencies or model files. For exact tested dependency replication,
use `requirements-ai-lock.txt` in a clean Python 3.9 environment. A custom
`WISELANKA_MODEL_DIR` must contain the same locked layout; setup writes the default
`.models/<revision>` location. Without optional AI setup the ordinary app still
runs with an explicit fallback. Runtime requires no paid service or network.

## Actual final verification

| Check | Result |
|---|---|
| Complete backend suite | **177 passed**, no skips in the AI-enabled environment |
| Complete Chromium browser suite | **25 passed** |
| Complete data integrity validation | Passed |
| Original live integration | Passed |
| WP1 live integration | Passed |
| WP2 live integration | Passed |
| WP3 real-model browser integration | Passed |
| Actual project environment without optional AI dependencies | Explicit fallback passed |
| Whitespace check | Passed |

`verification.json` records executed commands, zero exit codes, timestamps, source
and dataset hashes. Earlier WP1/WP2 evidence was preserved; regression screenshots
are saved below WP3. The WP2 script initially wrote its fixed snapshot paths; its
new screenshots were copied below WP3 and both original WP2 snapshots restored
byte-for-byte from the clean committed checkpoint. The final live API used 8011 to avoid user servers.

Functional cases cover empty preferences, lexical matches, paraphrases, unfamiliar
vocabulary, three domains, vocational exploration, missing descriptions, inference
and loading failures, academic-group boundaries, stable ties, checksum rejection,
real-model repeatability, invalid output and API compatibility. Browser checks
confirm score/method/preference labels, source links, unknown/unmet separation and
390px reflow. Existing keyboard/form tests still pass. Full screen-reader/WCAG or
cross-browser conformance is not claimed.

A resume-time defensive test initially failed because invalid intermediate scores
survived the fallback exception. It was fixed by discarding scores and cached
vectors. `resume-failed-nonfinite-test.txt` preserves that failure; it is not counted
as a passing run. Final tests and live checks were rerun after the fix.

## Comparison results and scientific limits

Nine frozen synthetic scenarios compare identical candidate pools and catalogue
text. `comparison.json` records raw legacy order, grouped deterministic order,
TF-IDF order and semantic order plus scores and unchanged academic statuses.

Examples (programme IDs, in returned order):

| Scenario | Grouped deterministic top three | TF-IDF top three | Semantic top three |
|---|---|---|---|
| IT paraphrase | 0001, 0002, 0003 | 0002, 0001, 0003 | 0002, 0003, 0001 |
| Business | 0001, 0008, 0009 | 0008, 0001, 0009 | 0008, 0001, 0009 |
| Vocational exploration | 0001, 0002, 0003 | 0007, 0008, 0001 | 0010, 0004, 0011 |

IDs use the PRG prefix. These are observed ordering differences, not accuracy
improvements. Overall top-k is constrained by academic groups; Engineering with
unknown selection cannot outrank MET programmes merely because of similarity.
Unfamiliar text can still receive nonzero semantic scores. The lexical baseline
uses no hand-tuned synonym expansion or stop-word list; common-word overlap can
produce weak matches. No superiority claim follows from these examples.

There are no legitimate independent relevance ratings or satisfaction data.
Therefore nDCG@3 is explicitly null, not zero, and no precision/accuracy uplift is
claimed. Synthetic inputs and implementer-authored assertions are functional tests,
not independent ground truth. There is no supervised training/validation split
because no local training occurs. Catalogue fitting uses no evaluation ratings or
query labels. These scenarios are not claimed as an independent held-out study;
future relevance evaluation needs blinded independent graded judgements and a
frozen development/test protocol before tuning. Future feedback learning would
require ethical adult-only opt-in data, participant-separated evaluation and
versioned offline updates; none is implemented here.

## Performance measurements

Final saved measurements (`performance.json`):

- Model load: **0.209 seconds**.
- Warm median: **13.1 ms**; p95: **16.2 ms**, across 40 successful ASGI requests.
- Process peak RSS before model load: **40.5 MiB**; after evaluation/requests:
  **333.2 MiB**.

Latency uses in-process FastAPI TestClient, not network or browser latency. Peak
RSS includes Python, model, runtime, embeddings and evaluation activity; it is not
isolated model memory. Startup is model loading, not a complete cold-machine
installation or server boot. Results describe one local machine/run, not a service
level guarantee or proof of deployment performance elsewhere.

## Traceability, files and limitations

Objective IV's bounded hybrid mechanism is implemented: authoritative eligibility
plus pretrained semantic relevance and source-grounded explanatory presentation.
FR3 and FR6 gain AI-assisted ordering/explanation; FR1/FR2 gain optional intention
input. FR5 remains grounded academic/self-report insight, not inferred competence.
Objective VII receives functional and scenario evidence, but full usability and
scientific relevance evaluation remain partial. No overall proposal-completion,
user-satisfaction or educational-effectiveness claim is made.

`modified-files.txt` lists the five changed tracked files, relevance module and
lock, optional requirements, setup/evaluation scripts, unit/integration/browser
checks and live WP3 check. Evidence here adds logs, comparisons, measurements,
screenshots and this report. Eligibility rules, CSVs, README and earlier evidence
were not changed by WP3. Both original JavaScript backups remain untouched.

Remaining limitations: English-only model; short and uneven catalogue descriptions;
IT-heavy coverage; opaque encoder internals despite clear UI explanations; limited
browser/accessibility testing; no independent relevance labels. A held qualification
can reappear in catalogue exploration because duplicate-award filtering is not
implemented. Low or high similarity is not verified personal suitability. No
automatic feedback learning, chatbot, language switching or voice was added.

WP3 is ready to close within this bounded implementation scope. WP4 has not begun.
