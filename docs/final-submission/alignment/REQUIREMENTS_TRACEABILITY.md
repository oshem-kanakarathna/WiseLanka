# Updated requirements traceability — original IDs remain authoritative

P-FR1–9 and P-NFR1–7 refer to proposal Tables2–3. I-FR01–10 and I-NFR01–08 refer to interim Tables9–10; these are refinements, not formally approved replacements. The bare FR/NFR numbers in the first column retain their proposal meaning. In particular **P-FR8 chatbot ≠ I-FR08 career guidance** and **P-NFR4 reliable data ≠ I-NFR04 deterministic reliability**. Implementation status is distinct from scientific validation. All evidence filenames below are under docs/evidence/wp5/ unless another WP is named.

## Approved functional requirements

| Original ID and exact wording | Interim refinement | Actual implementation anchors | Verification | Status | Limits |
|---|---|---|---|---|---|
| P-FR1: Allow users to create learner profiles | I-FR01, I-FR10 | `backend/app/personalisation/models.py:49; frontend/components/learner-profile.js` | WP1/live-wp1.log; backend.log; browser.log | IMPLEMENTED | Temporary validated profiles; no account/persistence. Diagram account scope remains an explicit unresolved interpretation |
| P-FR2: Collect educational qualifications and interests | I-FR01 (academic input only); I-FR03 | `backend/app/personalisation/models.py:10,49; frontend/components/learner-profile.js` | WP1 qualification/grade tests; live-wp1.log | IMPLEMENTED | Interim input did not demonstrate all present award/interests/self-report fields; reported awards unauthenticated |
| P-FR3: Generate personalised pathway recommendations | I-FR02, I-FR03, I-FR05, I-FR08 | `backend/app/personalisation/engine.py:188; backend/app/relevance/engine.py:67` | comparison.json; live-wp3.log; backend.log | IMPLEMENTED | Rules plus frozen semantic inference; independent relevance improvement unverified |
| P-FR4: Provide alternative progression routes | I-FR06, I-FR07 | `backend/app/progression/engine.py:117; backend/app/alternative_pathways/engine.py:244` | live-wp2.log; source review; progression tests | IMPLEMENTED | Only curated routes; no guarantee or inferred qualification equivalence |
| P-FR5: Identify skill or qualification gaps | I-FR02, I-FR04 (qualification gaps); no explicit interim skill-gap item | `backend/app/eligibility/engine.py:776; backend/app/skills/engine.py:4` | WP1 self-report/gap regressions; scenario-results.json | IMPLEMENTED | Unreported skills are not failed skills; weak per-edge skill provenance |
| P-FR6: Explain recommendation outputs | I-FR04, I-FR07, I-FR10 | `backend/app/eligibility/explainer.py:11; backend/app/assistant/engine.py:40; frontend/components/learner-profile.js` | backend/browser logs; live-wp4.log | IMPLEMENTED | Generated explanations are deterministic grounded text; comprehension/trust unmeasured |
| P-FR7: Display official educational resource links | I-FR09, I-FR10 | `data/metadata/evidence_sources.csv; backend/app/assistant/engine.py:40; frontend/components/guided-assistant.js` | rule-evidence.csv; official source review; live logs | IMPLEMENTED | Links and stored recognition do not verify all recognition/career relationships or future currency |
| P-FR8: Provide chatbot-assisted support | No direct I-FR item (I-FR08 is career guidance) | `backend/app/assistant/engine.py:17,40; frontend/components/guided-assistant.js` | WP4 tests; live-wp4.log | IMPLEMENTED | Bounded guided assistant, not unrestricted or generative chat |
| P-FR9: Support basic voice-assisted input | No direct I-FR item | `frontend/components/guided-assistant.js:99` | Mocked voice tests; voice-capability.json | PARTIAL | Implemented optional states/text fallback; native microphone/language performance pending |

## Approved non-functional requirements

| Original ID and exact wording | Interim refinement | Actual implementation anchors | Verification | Status | Limits |
|---|---|---|---|---|---|
| P-NFR1: User-friendly interface | I-NFR01, I-NFR07 | `frontend/pages/learner-profile.html; frontend/components/learner-profile.js` | browser.log; accessibility-final.json | PARTIAL | Interface implemented; user-friendly quality needs actual adult usability evidence |
| P-NFR2: Mobile-friendly usability | I-NFR07 | `frontend/components/learner-profile.css; frontend/components/guided-assistant.js` | 320/390px reflow and narrow-viewport live screenshots | PARTIAL | Automated layouts passed; real mobile/touch/zoom/manual operation pending |
| P-NFR3: Acceptable response time | I-NFR03 | `backend/app/relevance/encoder.py:15; backend/app/relevance/engine.py:56,67` | performance.json; runtime-network.json | PARTIAL | Measured warm local latency; proposal sets no pass threshold; perceived acceptability/concurrency/cold-device performance unverified |
| P-NFR4: Reliable educational datasets | I-NFR04, I-NFR05 | `backend/app/data_integrity.py:28; backend/app/data_loader.py:13; data/metadata/evidence_sources.csv` | csv-integrity.log; rule-evidence.csv; educational-source review | PARTIAL | Structural integrity and selected sources checked; comprehensive independent accuracy/currentness not established |
| P-NFR5: Modular system architecture | I-NFR06 | `backend/app/api/main.py; backend/app/{eligibility,personalisation,relevance,progression,skills,assistant}/` | Modular source inspection; backend/API regressions | IMPLEMENTED | Architecture is modular within one FastAPI application; no independent microservices implied |
| P-NFR6: Future scalability support | I-NFR06, I-NFR08 | `backend/app/data_loader.py; backend/app/data_integrity.py; CSV IDs/relationships; modular engines` | Catalogue extended7→11 programmes without database migration | PARTIAL | Extensibility demonstrated, not national scale, high-load operation or production deployment |
| P-NFR7: Explainable recommendation outputs | I-NFR02 | `backend/app/eligibility/explainer.py:11; backend/app/assistant/engine.py:40; backend/app/relevance/engine.py:106` | Status/source/rendering tests; live workflows | IMPLEMENTED | Output explanations present; actual understandability remains human-evaluation pending |

## Complete interim functional crosswalk

| Interim ID | Exact refined requirement / description | Links to original requirements | Interpretation |
|---|---|---|---|
| I-FR01 | Learner Profile Input — The system shall allow learners to provide academic results according to the relevant education level. | P-FR1, P-FR2 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR02 | Eligibility Evaluation — The system shall evaluate learner results against structured programme entry requirements. | P-FR3, P-FR5, P-FR6 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR03 | Programme Recommendation — The system shall identify and rank programmes applicable to the learner's academic profile. | P-FR3 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR04 | Eligibility Explanation — The system shall indicate satisfied and unmet requirements contributing to an eligibility outcome. | P-FR5, P-FR6 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR05 | Education-Level Filtering — The system shall distinguish between education levels when identifying applicable programmes. | P-FR2, P-FR3 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR06 | Qualification Progression — The system shall identify recorded progression opportunities associated with relevant qualifications. | P-FR4 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR07 | Progression Conditions — The system shall preserve and display conditions associated with conditional progression routes. | P-FR4, P-FR6 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR08 | Career Pathway Guidance — The system shall associate relevant career pathways with programme recommendations. | P-FR3 (career relationships), P-FR5 context | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR09 | Evidence and Recognition Information — The system shall maintain available evidence and recognition-related information within the structured knowledge base. | P-FR7; P-NFR4 | Refinement/supporting mechanism; no one-to-one renumbering |
| I-FR10 | Web-Based Presentation — The system shall present recommendations, eligibility information and pathway guidance through a web interface. | P-FR1, P-FR3, P-FR6, P-FR7 | Refinement/supporting mechanism; no one-to-one renumbering |

## Complete interim non-functional crosswalk

| Interim ID | Exact refined requirement / description | Links to original requirements |
|---|---|---|
| I-NFR01 | Usability — The interface should present pathway information clearly and minimise unnecessary complexity for learners. | P-NFR1 |
| I-NFR02 | Explainability — Eligibility and recommendation outcomes should be accompanied by understandable supporting information. | P-NFR7 |
| I-NFR03 | Performance — Core recommendation and pathway requests should return results within a practical response time for interactive use. | P-NFR3 |
| I-NFR04 | Reliability — The system should produce consistent outputs for equivalent learner profiles and defined academic rules. | P-NFR4; execution consistency additionally refines P-FR3 |
| I-NFR05 | Data Integrity — Structured educational records and relationships should remain internally consistent and traceable to available evidence. | P-NFR4 |
| I-NFR06 | Maintainability — The modular architecture should allow individual engines, data records and interface components to be updated without unnecessary modification of unrelated components. | P-NFR5, P-NFR6 |
| I-NFR07 | Accessibility — The interface should support clear, readable and responsive interaction across commonly used screen sizes. | P-NFR1, P-NFR2 |
| I-NFR08 | Extensibility — The system structure should support future expansion of programmes, institutions, qualifications, progression relationships and additional pathway-intelligence capabilities. | P-NFR6 |

Original objectives/research questions remain mapped in ../RESEARCH_QUESTION_TRACEABILITY.md. No interim progress table with paraphrased “objective areas” replaces the eight approved objectives. NFRs are qualitative; the measured response times are observations, not retroactively invented acceptance thresholds.
