# 5. Architecture and implementation

## 5.1 Proposed stack and implemented architecture

The proposal suggests Streamlit, Python, Pandas, SQLite/CSV/JSON and lightweight NLP/LLM support (Kanakarathna, 2026a, Table 8 and appendix D). By August, the interim explicitly documents Python/FastAPI, HTML/CSS/JavaScript and structured CSV files (Kanakarathna, 2026b, §§4.3–4.6). October preserved and extended that separation. It would therefore be inaccurate to describe either an unchanged Streamlit implementation or a new October frontend replacement.

The retained architecture permits direct API/domain tests and explicit browser control over dynamic rows, translation, voice and responsive cards. Its cost is coordination of separate browser/API state, CORS and accessible DOM behaviour. CSV files remain within the proposal's main-table options and suit this small versioned corpus, with strict validation compensating for absent database constraints. Neither Pandas nor an application database is currently needed by the implemented row-based rules; no comparative benchmark established that they would be inferior.

Frozen ONNX relevance supplies genuine NLP inference without a paid generation service or invented training data. Explanations and guided chat are deterministic and source-grounded, narrower than the optional LLM-assisted technology illustration. That is a justified engineering interpretation, not proof that every illustrated component was delivered. The [technology decision record](../alignment/TECHNOLOGY_JUSTIFICATION.md) preserves alternatives, trade-offs and the remaining supervisor scope decision.

## 5.2 Request lifecycle

The browser builds a learner profile from examination rows, category, structured qualifications, skills and interests. Validation rejects duplicate subjects and invalid grades while supporting existing six-subject profiles and nine-subject O/L entry. It does not force nine subjects for every assessment. The FastAPI route delegates to typed models and domain engines rather than embedding separate educational logic in JavaScript.

`backend/app/data_loader.py` resolves project-root-relative paths and distinguishes missing/malformed files from genuine empty data. Startup invokes `data_integrity.validate_catalogue()`. This protects against broken relationships and malformed data before returning guidance, although syntactically valid but inaccurate policy text still requires source review.

## 5.3 Domain engines

| Module | Responsibility | Boundary |
|---|---|---|
| eligibility/engine.py | Requirement evaluation, group logic, canonical academic gaps | Does not infer undocumented equivalence or selection decisions |
| recommendation/engine.py | Legacy academic matching and catalogue/career enrichment | Numeric subject-match score is not admission probability |
| personalisation/engine.py | Typed profile orchestration, career/interests/preferences, gaps and ranking | Reuses formal assessments |
| relevance/engine.py and encoder.py | TF–IDF/semantic ranking within academic groups, local inference, fallback | Cannot change academic group |
| progression/engine.py | Conditional qualification relationships and linked programmes | Does not authenticate awards or guarantee progression |
| alternative_pathways/engine.py | Curated alternative routes | Limited by recorded relationships |
| skills/engine.py | Programme/career mappings and explicit self-report comparison | No competence testing |
| scholarships/engine.py | Recorded scholarship conditions/unknown context | Historical availability differs from eligibility |
| assistant/engine.py | Read-only structured guidance with supported intents | Not unrestricted generative chat |

Programme–career alignment and learner-specific skill comparison are separate operations. An unreported skill produces no negative competence conclusion. Reported skills remain self-reports, while a learner-marked development opportunity is an expressed goal. Career-skill mappings lack per-edge source citations; the interface states this evidential weakness.

## 5.4 Hybrid integration and compatibility

The personalisation response contains `recommendations`, `academic_insights`, `learner_skill_insights`, held-qualification progression and `ranking`. Per-programme `relevance` identifies the method, score, input summary, catalogue facts and source link. Qualification-only profiles can explore `academic_insights` while `recommendations` remains empty; the system does not manufacture grade evidence from a reported award.

Canonical academic status determines the outer ordering MET → NOT_ASSESSED → NOT_MET. Similarity orders only inside a group. Existing baseline position and programme ID provide stable ties. Thus an attractive but failed Engineering programme remains unmet, and a source-incomplete programme cannot be silently promoted to eligible. Prior UI/API fields remain available for compatibility, with clearer uncertainty labels where WP5 corrected policy omissions.

## 5.5 Interface, guided support and voice

`frontend/components/learner-profile.js` manages forms/results; `i18n.js` applies the shared translation catalogue; `guided-assistant.js` handles structured guidance and browser speech states. The 135-key catalogues cover major controls, validation, status and assistant labels in each language. Detailed educational content retains its original language where translation is unverified.

Speech recognition uses browser-provided interfaces where available. Explicit opt-in precedes microphone activation; transcripts enter editable text and do not automatically submit. Unsupported browsers, denied permission, errors and unavailable languages produce recoverable states. No audio store was added. Mocked event tests verify those transitions, but do not establish actual microphone permission behaviour, transcription quality or offline operation.

## 5.6 Reproducible runtime

The tested environment uses Python 3.9.6 with pinned optional AI dependencies and CPU inference. Weights are downloaded explicitly, checksum-verified and excluded from Git; runtime model loading is local-only. A missing optional runtime or model produces explicit RULE_BASED_FALLBACK and null semantic scores. Empty interests yield NOT_ASSESSED relevance instead of invented preference evidence. Model-load failure is cached, so provisioning a model into a previously failed process requires a restart.

The architecture avoids accounts, databases, microservices and paid inference. This reduces prototype operational complexity, but does not constitute production security assurance. The recorded secret scan covered selected patterns in tracked working-tree text; it was not a full history, penetration or privacy audit.
