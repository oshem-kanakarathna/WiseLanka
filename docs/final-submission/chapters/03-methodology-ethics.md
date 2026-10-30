# 3. Research methodology and ethics

## 3.1 Design Science Research

WiseLanka follows the approved Design Science Research (DSR) methodology with Agile-inspired iterative prototyping. Hevner et al. (2004) position artifact construction and evaluation as a route to knowledge about a problem and its solution. This project applies that framing to a web decision-support artifact; code completion is a necessary activity rather than the entire research contribution.

Peffers et al. (2007) describe a process involving problem identification, solution objectives, design/development, demonstration, evaluation and communication. Table 3.1 maps the project's work to those activities. The mapping is a reconstruction from work-package artifacts and Git checkpoints, not proof that every activity was completed prospectively exactly as now described.

| DSR activity | WiseLanka evidence | Status |
|---|---|---|
| Problem identification | Approved excerpts; historical policy context; developer motivation | Needs broader current learner evidence |
| Objectives for solution | Approved objectives and FR1–FR9 | Original aim/objectives/questions/FRs/NFRs/deliverables now checked; broader current learner evidence remains limited |
| Design/development | CSV knowledge, modular engines, web UI, WP1–WP4 | Implemented bounded artifact |
| Demonstration | Synthetic profiles and five live workflows | Executed technical demonstrations |
| Evaluation | Automated/scenario/source review, runtime and accessibility checks | Executed technical evaluation; human/relevance work pending |
| Communication | This draft, poster and viva materials | Working drafts for author/supervisor review |

## 3.2 Iteration and traceability

The August report describes applied DSR, a pragmatic orientation and deductive translation of requirements into rules, with iteration informed by testing (Kanakarathna, 2026b, §§3.1–3.4). This characterises the research's practical orientation; it does not establish a complete mixed-method human study. Its technical demonstrations precede the unfinished user-evaluation stage.

| Stage | Evidence-grounded development |
|---|---|
| August interim | Layered FastAPI/HTML/CSS/JS artifact, seven computing records, three foundation routes and 40 passing tests in report screenshots |
| WP1 | More complete O/L entry, typed categories/awards, self-report skills and evidence-aware gaps |
| WP2 | Four programme additions, two vocational progression edges, source/integrity refinements and threshold correction |
| WP3 | Actual frozen MiniLM ONNX inference, grouped relevance, TF–IDF comparison and explicit fallback |
| WP4 | Read-only guided assistant, draft interface languages and browser voice/text states |
| WP5 | Integration/reproducibility/source/accessibility evaluation and conservative policy corrections |

This chronology distinguishes implemented evidence from the earlier hybrid/accessibility ambition. The full [interim-to-final comparison](../alignment/INTERIM_TO_FINAL.md) records source locations and the corroborating August Git snapshot. Local checkpoints establish an inspectable artifact history, but they do not document every development conversation or substitute for a research diary. The author should add genuine dated supervisor feedback and decisions where available.

A concrete refinement cycle occurred in WP5. Source inspection revealed omitted UGC general-entry evidence; the rules were revised to retain NOT_ASSESSED, regression expectations were updated and affected suites rerun. Automated accessibility findings also led to specific semantic/contrast repairs. These cases show how evaluation informed the artifact, rather than asserting usefulness from test counts alone.

## 3.3 Evaluation layers

The evaluation separates: (a) code execution against specified rules; (b) fidelity and currency of those rules to educational sources; (c) content-ranking behaviour; (d) relevance judgements; (e) usability and explanation comprehension; and (f) actual educational outcomes. Completed evidence principally covers (a), selected parts of (b), functional/runtime aspects of (c), and automated accessibility. The remaining layers are not inferred from a successful API response.

Synthetic profiles allow repeatability without personal records. The 14 reference cases were authored by the implementer, so they share interpretation risks with the code. Independent review is necessary to reduce circular validation. The nine ranking scenarios are development/functional examples, not a held-out relevance test. Future independent cases must be frozen before parameter or corpus tuning.

## 3.4 Ethics and data handling

No human participation is reported. The known approved-baseline condition excludes under-18 participants; the signed ethics document and additional conditions have not been accessed. Draft instruments are prepared for review, not recruitment. Researcher/supervisor contact details, ethics reference, approved recruitment channel, retention period, storage/access arrangements and withdrawal process must be supplied from approved documentation before use.

The standard proposed session uses fictional learner details, study IDs and deidentified observations. It does not require names, dates of birth, certificate identifiers, real grades or audio/video recording. Consent and any contact information should be handled separately as required by approval. Do not promise anonymity where a small sample or distinctive comment could identify someone. Participants should be free to decline tasks without disadvantage.

Browser speech can involve third-party processing. Native voice testing with participants requires specific approval and optional informed consent; typing must remain available. The local embedding runtime sends no learner profile to an inference API, but this does not make browser recognition local. Draft translations must not be represented as certified or used for consequential advice.

## 3.5 Validity and research integrity

Internal validity is limited by implementation-authored expectations and lack of independent ranking labels. Construct validity requires distinguishing task completion from satisfaction and similarity from educational suitability. External validity is limited by 11 programmes, uneven domain coverage and one measured machine/browser setup. Reproducibility is strengthened by logs, exit codes, CSV hashes, pinned model revision and dependency lock, but changing official pages can still alter the underlying evidence.

The researcher must preserve negative findings and exclusions. No invented participants, source endorsements or superiority claims fill missing results. AI-assisted drafting must be disclosed according to the actual module conditions; this draft is not a signed originality statement. The supplied exact research questions are now mapped in RESEARCH_QUESTION_TRACEABILITY.md. The original-document comparison is now recorded; signed ethics conditions, the actual rubric and genuine human/independent evaluation remain prerequisites for final methodological closure.
