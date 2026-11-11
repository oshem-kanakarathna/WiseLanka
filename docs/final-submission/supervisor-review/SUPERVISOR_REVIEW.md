# WiseLanka — supervisor discussion pack

Draft for review,29 October2026. University of West London final-year project. Academic draft checkpoint: **9ffb2f3**, explicitly draft/not approved; no push or submission. Aim/objectives/questions below now agree with the inspected original proposal and August interim; signed ethics conditions and actual rubric remain unverified.

## Aim

“The aim of this project is to design, develop, and evaluate an AI-powered, policy-aware Education and Career Pathway Intelligence System that provides personalised, explainable, and accessible education and career guidance for Sri Lankan learners.”

## Objectives

I. To critically review existing literature related to AI-based recommender systems, educational decision-support systems, and career guidance technologies.

II. To analyse the challenges faced by Sri Lankan learners when navigating educational and career progression pathways.

III. To design a structured knowledge base representing learner categories, educational pathways, eligibility rules, scholarship information, and career progression routes.

IV. To develop a hybrid recommendation mechanism combining rule-based eligibility filtering with AI-assisted pathway recommendation and explanation generation.

V. To implement a web-based prototype capable of generating personalised pathway recommendations, alternative routes, skill-gap insights, and official resource links.

VI. To integrate accessibility-focused features such as mobile-friendly usability, multilingual support, and voice-assisted interaction.

VII. To evaluate the proposed system using scenario-based testing, functional testing, and usability feedback.

VIII. To identify limitations of the proposed solution and recommend future improvements for wider deployment and enhanced AI integration.

## Approved research questions

**MAIN RESEARCH QUESTION**

How can an AI-powered, policy-aware Education and Career Pathway Intelligence System support Sri Lankan learners through personalised, explainable, and accessible pathway recommendations?

**SUPPORTING RESEARCH QUESTIONS**

I. How can learner profiles, eligibility requirements and pathway knowledge be integrated to generate suitable recommendations?

II. How can explainable recommendation mechanisms improve user understanding and trust?

III. How can alternative pathway generation and skill-gap identification support educational and career planning?

IV. How can multilingual support, mobile usability and voice-assisted input improve accessibility?

V. How effective is the prototype in providing relevant and usable pathway guidance?

Provenance: exact text now confirmed against proposal §1.4 and interim §1.4 in the author-identified WORK originals; see alignment/SOURCE_REVIEW.json. The signed ethics decision and assessment requirements remain unverified.

## Current artifact and verified evidence

WiseLanka provides temporary structured O/L/A/L, vocational and early-career profiles; three-state academic requirements; alternative/conditional progression; self-reported skill comparisons; official links; local frozen MiniLM ONNX relevance with deterministic/TF–IDF comparison; read-only guided support; draft English/Sinhala/Tamil controls; optional browser speech/text fallback. Eligibility remains authoritative; similarity is not admission probability or evidence of competence. There is no automatic feedback learning or unrestricted generative chatbot.

The curated snapshot has11 programmes (IT7, Business1, Engineering3),12 qualifications,33 requirement rows,5 non-guaranteed progression edges and21 sources. WP5 recorded205 backend tests,36 browser tests,5 live workflows and14 synthetic reference cases passing; CSV integrity/fresh installation passed; axe detected zero violations in9 scanned states. These are executed technical results, not educational accuracy/satisfaction findings. Model load~0.29s, warm in-process p95~15ms, whole-process RSS~302MiB on one Mac. Nine functional ranking scenarios have no independent relevance labels or nDCG.

## Drafts for discussion

- [Dissertation](../DISSERTATION_DRAFT.md) and [reference review](../review/REFERENCE_FINDINGS.md).
- [One-page poster PDF](../poster/research-poster-draft.pdf), provisional dimensions/template.
- [Viva/demo materials](../viva/PRESENTATION_OUTLINE.md).
- [Question/evidence mapping](../RESEARCH_QUESTION_TRACEABILITY.md).
- [Evaluation plan v0.2](../research-evaluation/EVALUATION_PLAN_v2.md), [instrument addendum](../research-evaluation/MEASURES_ADDENDUM_v2.md) and [independent-ranking protocol](../research-evaluation/independent-ranking/PROTOCOL.md).

## Proposed remaining evaluation

Exploratory adult task study, target8 (range6–10 if agreed), with explicit consent and synthetic profiles. Where approved, counterbalance official-source lookup versus WiseLanka across two matched-status tasks and four sequences. Observe completion/time/help and interpretation, then collect custom perceived relevance/usefulness, transparency and bounded reliance items. Use separate pathways/skills probes and pending manual/fluent-language checks. No participant feedback exists. Small descriptive differences would not establish causal improvement or real educational outcomes.

Separately, two independent adult judges are proposed for51 case/candidate pairs across nine existing development cases. Method-blinded seeded packs are prepared. Rate interest relevance0–3/UNJUDGEABLE, preserve disagreement, compare fixed-group deterministic/TF–IDF/MiniLM orders only after labels are locked. Existing cases do not become held-out evidence merely because judges are independent.

## Ethics and human work outstanding

No recruitment/data collection until the actual approval and conditions are checked. Contacts, approved recruitment, inclusion/sample, storage/access/retention, withdrawal, comparison/trust amendments and complaint route need confirmation. Native participant voice is excluded until its browser-provider processing and optional consent are authorised. Fluent translation, native microphone, screen-reader/mobile and educational-source review remain pending. No gains in trust, comprehension, accessibility, recommendation quality or learner outcomes are claimed.

## Five decisions requested from the supervisor

1. **Academic alignment:** review the completed original/interim reconciliation and undelivered account/role/storage diagram features; confirm the bounded prototype interpretation and essential corrections. Provide genuine feedback, dissertation rubric/word limit/referencing and permitted AI-assistance conditions.
2. **Ethics release:** inspect the signed decision and determine required amendment(s) for adult usability, independent judges, new reliance/transparency items and source-lookup comparison. Confirm recruitment, data handling and participant voice exclusion/conditions.
3. **Feasible study design:** approve/revise the proposed8-adult exploratory sample, two-task/four-sequence comparison, burden and custom measures; or accept a clearly descriptive WiseLanka-only study without improvement claims.
4. **Independent evidence:** agree judge independence/qualifications and relevance rubric/exclusions; nominate suitable domain/fluent reviewers where possible. Confirm that unlabelled/zero-gain/singleton cases and unavailable metrics must remain visible.
5. **Completion priorities and format:** agree the minimum outstanding human/manual/full-text work, final chapter/poster/viva specifications and achievable November review dates. Identify any mandatory work that cannot be deferred or replaced by technical tests.

Decision/date/action-owner fields are deliberately unfilled. Discussion of this document is not an ethics or submission approval. No message has been sent to the supervisor.
