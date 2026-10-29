# Objective-to-research-question and evidence traceability

The questions below preserve the author's supplied wording exactly. Their source is the current approved-baseline excerpt, not an inspected proposal DOCX. Research questions express what is being investigated; words such as “improve” are not findings. SRQ labels are added for cross-reference only and do not alter the text.

**Main research question**

How can an AI-powered, policy-aware Education and Career Pathway Intelligence System support Sri Lankan learners through personalised, explainable, and accessible pathway recommendations?

**SRQ-I.** How can learner profiles, eligibility requirements and pathway knowledge be integrated to generate suitable recommendations?

**SRQ-II.** How can explainable recommendation mechanisms improve user understanding and trust?

**SRQ-III.** How can alternative pathway generation and skill-gap identification support educational and career planning?

**SRQ-IV.** How can multilingual support, mobile usability and voice-assisted input improve accessibility?

**SRQ-V.** How effective is the prototype in providing relevant and usable pathway guidance?

## Question → implementation → method → available evidence → unfinished research

| Question | Related objectives / FRs | Actual components | Evaluation method and available record | What remains / permitted answer |
|---|---|---|---|---|
| MRQ | I–VIII; FR1–FR9 | Integrated profile, knowledge, eligibility, ranking, explanation, alternatives, skills and access components | DSR artifact construction/refinement; WP5 tests, source review and runtime; pending human layers | Technical integration demonstrated. Whether intended learners receive relevant, understandable, trusted and accessible support is only partly investigated, not established |
| SRQ-I | I, III, IV, V, VII; FR1–FR3, FR6–FR7 | personalisation/models.py:49; personalisation/engine.py:188; eligibility/engine.py:776; data_integrity.py:28 | Typed contracts, 205 backend tests, 14 synthetic cases and source-linked requirements; CSV validation | Mechanism/integration defensible in tested cases. “Suitable” needs independent source/rule adjudication and relevance judgements; no validated nationwide suitability claim |
| SRQ-II | I, IV, V, VII; FR6, FR8 | eligibility explanations; relevance/engine.py:106; assistant/engine.py:40; UI status/source labels | Tested status/source rendering, planned E1–E5 comprehension probes and custom clarity items | No adult results, explicit trust instrument or comparison condition. Understanding/trust improvement NOT ESTABLISHED. Evaluate calibrated reliance separately from persuasive wording; any new instrument/design needs ethics review |
| SRQ-III | II, III, V, VII; FR4–FR6 | progression/engine.py:117; alternative_pathways/engine.py:244; skills/engine.py:4 | Conditional vocational/foundation cases, gap/self-report tests, planned T3–T5 and comprehension probes | Functional route/gap generation demonstrated; contribution to actual planning unmeasured. No competence verification, credential equivalence or guaranteed progression inferred |
| SRQ-IV | II, V, VI, VII; FR9 and multilingual/mobile scope | i18n.js; guided-assistant.js:99; learner-profile HTML/CSS | Language preservation tests; axe nine states; 320/390px reflow; mocked speech states; manual checklist | Fluent si/ta review, native speech, assistive technology, target-device and approved adult accessibility evaluation pending. No measured accessibility improvement or complete WCAG conformance |
| SRQ-V | IV, V, VII, VIII; FR3–FR6 | Hybrid ranker + whole web artifact | Nine synthetic method comparisons, 14 reference cases, measured runtime, proposed usability and blinded relevance protocols | Functional robustness measured. Independent relevance labels/nDCG, task/satisfaction findings and educational effectiveness unavailable; no AI quality superiority |

Source paths in this table are under backend/app/ or frontend/components/ as appropriate. The result artifacts are in docs/evidence/wp5/. Testing counts describe the saved WP5 snapshot; this review did not rerun application suites or collect human results.

## Every approved objective → relevant questions

| Objective | Related questions | Current evidence state and next action |
|---|---|---|
| I critical literature review | MRQ, SRQ-I, II, V (conceptual foundations also inform III–IV) | PARTIAL: narrative draft and checked references; deepen full-text critical comparison and source selection |
| II Sri Lankan learner challenges | MRQ, SRQ-III, IV, V; contextual foundation for I–II | PARTIAL: historical/context/design evidence; strengthen current target-group evidence without implying a new unapproved study |
| III structured knowledge | MRQ, SRQ-I, III | IMPLEMENTED bounded catalogue; independent source/route review and currency limitations remain |
| IV hybrid recommendation/explanations | MRQ, SRQ-I, II, V | IMPLEMENTED frozen semantic inference plus authoritative rules and deterministic explanations; relevance/understanding validation pending |
| V web prototype and gaps | MRQ, SRQ-I, II, III, V | IMPLEMENTED prototype; support for actual planning/usability not empirically established |
| VI accessibility | MRQ, SRQ-IV | PARTIAL validation: implemented controls and automated checks; human/fluent/native/manual work pending |
| VII evaluation | MRQ, SRQ-I–V | PARTIAL: technical evaluation complete for recorded snapshot; approved adult usability remains outstanding |
| VIII limitations and improvements | MRQ, SRQ-I–V, especially V | Explicit draft discussion exists; final synthesis must reflect actual eventual evidence and supervisor/brief review |

This is a many-to-many analytical mapping, not proof that all objectives are achieved. No objective or question is rewritten to fit the existing prototype. The original proposal DOCX and full rubric remain required for final confirmation.
