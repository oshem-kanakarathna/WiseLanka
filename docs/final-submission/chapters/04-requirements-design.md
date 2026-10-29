# 4. Requirements analysis and system design

## 4.1 Baseline and boundaries

Appendix A preserves the supplied approved aim, eight objectives and FR1–FR9. The target categories are A/L, vocational and early-career learners; O/L results support foundation entry. Profiles collect educational evidence, interests, optional career intentions/preferences, structured awards and optional self-reported skills. Accounts or durable storage were unnecessary for the bounded prototype. The original detailed NFRs are unavailable; the quality attributes discussed here are implemented design concerns, not invented approved requirements or numerical targets.

The [WP5 matrix](../../evidence/wp5/REQUIREMENTS_TRACEABILITY.md) separates implementation status from validation. This distinction prevents the existence of a microphone button or translation catalogue from being counted as evidence of universal accessibility. It also exposes the incomplete human-evaluation element of Objective VII.

## 4.2 Information model

The CSV knowledge base represents institutions, programmes, qualifications, careers, skills, scholarships and controlled reference types. Relationship tables connect programmes to requirements, qualifications to progression, programmes to careers/skills and careers to skill requirements. Metadata records sources and recognition information. Stable identifiers support joins and integrity checks. This structure retains small editable tables while allowing repeatable validation.

A qualification has an identifier, title, framework and level where recorded. A reported catalogue award is canonicalised against its ID; inconsistent metadata is rejected. A custom award can remain without a catalogue ID and cannot establish equivalence. Qualification-framework level alone is not an admission decision. Provider, awarding body, recognition and progression have different meanings and must not be collapsed into a single “recognised” boolean.

## 4.3 Assessment semantics

For a recorded requirement, MET means supplied evidence satisfies the represented condition. NOT_MET requires evidence that the condition fails. NOT_ASSESSED covers absent evidence, unsupported criteria or provider review. In an AND group, a known failure can establish an unmet group; in an OR group, a satisfied alternative can establish that group even if another alternative is unknown. Otherwise unknown evidence propagates. Overall MET refers only to represented requirements and is never guaranteed admission.

The learner's complete-result declaration matters: absence of a named subject in a confirmed complete examination can establish it was not taken; absence in incomplete data cannot. This is still a self-report, not document authentication. For count-based requirements, omitting the completeness flag retains the legacy interpretation of submitted counts; explicitly marking the examination incomplete makes an unmet count NOT_ASSESSED. This compatibility default differs from the explicit complete-result evidence required to treat an omitted named subject as NOT_MET (eligibility/engine.py:813–821). Missing entry-rule records are not treated as an empty list of automatically satisfied constraints. State-university general-entry/selection evidence remains explicit provider review when unavailable.

## 4.4 Components and contracts

The browser submits a typed learner profile to `/personalised-recommendations`. FastAPI validates the request before invoking personalisation, which reuses eligibility, progression and skill engines. The response preserves legacy fields while adding canonical academic insights and relevance metadata. The UI displays academic status independently from content similarity. The `assessment_method` legacy label does not identify the semantic model; `ranking.method` does.

The guided assistant receives a selected intent, programme, language and optional profile. It performs read-only engine calls and supplies structured blocks and source URLs. It has no authority to mutate the profile or knowledge base. It accepts known topic aliases and refuses unsupported free text. This restriction is deliberate: a bounded educational assistant does not require an unrestricted language model.

## 4.5 Quality and interaction design

Accessible labels, live feedback, keyboard-operable controls, responsive cards, explicit errors and focus recovery support interaction. English, Sinhala and Tamil share one central catalogue. Official programme titles/source-language content remain distinguishable from interface translation. Language switching preserves inputs/results. Native browser speech is optional, consent-gated and editable before submission; denial and unavailable-language states retain text access.

The trade-off is limited language/interaction depth: semantic preferences remain English-supported, translations are drafts, and older pages are less comprehensively localised. These constraints are documented rather than hidden behind a claim of full multilingual intelligence.

## 4.6 Alternatives considered

A database could offer richer query/concurrency support, but for this small curated snapshot it would add migration and operational work without resolving source correctness. A frontend framework migration would likewise not improve admission evidence. A large or paid generative service would introduce cost, privacy and grounding challenges. The implemented modular FastAPI/CSV/vanilla-JavaScript architecture meets the bounded artifact needs and leaves deployment scaling as future work. Diagrams in appendix C show these component responsibilities and data flow.
