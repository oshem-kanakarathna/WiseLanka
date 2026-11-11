# WiseLanka
## DESIGN AND DEVELOPMENT OF AN AI-POWERED, POLICY-AWARE EDUCATION AND CAREER PATHWAY INTELLIGENCE SYSTEM FOR SRI LANKAN LEARNERS

University of West London — final-year project

**Integrated working manuscript — 7 November 2026. AI-assisted, student review required; not approved or ready for submission.**

Author: Oshem Thirsha Kanakarathna. Student ID: 34164665. Module: CP6SL460, School of Computing and Engineering. Supervisor as listed on both originals: Dr. Ama Kulathilake. Current cover-sheet requirements, word limit and submission date still require the actual assessment brief. The author-confirmed original proposal and interim DOCX files have now been inspected; their hashes and review coverage are recorded in alignment/SOURCE_REVIEW.json. November is the accelerated working target, not a verified university deadline.

### Abstract

**Provisional abstract — revise after the final evaluation decision and confirm the assessment brief’s requirements.** WiseLanka is a bounded web prototype exploring how structured educational requirements and learner-stated interests can be combined for Sri Lankan education and career pathway guidance. Its curated CSV catalogue covers 11 programmes across Information Technology, Business and Management, and Engineering, with selected qualification progression. A modular FastAPI backend keeps deterministic academic assessment separate from deterministic, TF–IDF and frozen MiniLM ONNX relevance ranking; outcomes distinguish MET, NOT_MET and NOT_ASSESSED. A guided support interface, draft English/Sinhala/Tamil strings and optional browser speech states extend interaction, but user accessibility and comprehension have not been empirically established.

The Stage 9A AI-enabled backend run recorded 269 passed tests, zero failures and zero skips; the data-integrity validator accepted 20 CSV datasets. A source-grounded synthetic educational evaluation recorded 42/45 agreements initially and 43/45 after a controlled examination-completeness correction, with two remaining input-contract limitations. A separate 21-scenario ranking comparison documented differences among methods and preserved academic status groups, but had no independent relevance labels. Therefore no ranking superiority, participant satisfaction or learner-outcome benefit is claimed. Adult usability, independent relevance, comprehension, fluent translation and native accessibility evaluations remain uncollected or pending. The contribution is a technically verified prototype and bounded evidence record; effectiveness for intended learners remains unresolved.

### Acknowledgements

[Author to write and approve acknowledgements. Do not invent personal or supervisory contributions.]

### Contents

[Generate the table of contents in the official Word template after chapter structure, headings and pagination are final.]

### List of Figures and Tables

[Generate figure and table lists from verified captions in the official template.]

### Author review and assistance disclosure

This draft was prepared with AI assistance from Codex using repository inspection and checked sources. It must not be represented as wholly unaided student writing. The author must review sources, revise and take responsibility for the analysis, and confirm permitted assistance and disclosure requirements against the actual assessment brief. A module-specific permission or declaration has not been verified. No declaration of originality or ethical approval is signed or fabricated here. Personal reflection, acknowledgements and approved institutional wording must be written/confirmed by the author.

### Reading guide

Chapters 1–10 provide a continuous dissertation argument. References and appendices follow. “Measured” refers to saved technical observations; “synthetic” refers to fictional profiles; “mocked” refers to simulated browser/API events; “pending” denotes work not performed. Bibliographic style is provisionally author–date and must be reconciled with the actual university instructions. The companion deliverable inventory records academic blockers.


---

# 1. Introduction

## 1.1 Problem and context

Education-to-career guidance must answer several different questions: which recorded entry requirements a learner meets, what evidence is missing, which programmes relate to stated interests, and what alternative routes remain conditional. Conflating these questions can produce plausible but misleading recommendations. A similarity score cannot determine whether an examination condition has been met, and an unreported qualification does not establish its absence.

Sri Lanka provides a concrete setting involving university and vocational routes. The National Education Commission's historical career-guidance study establishes that guidance provision has been a policy research concern; its 2014 series report, first published in 2016, is not evidence of current nationwide prevalence or of WiseLanka user needs (National Education Commission, 2016). The present project instead uses a small documented programme catalogue to investigate a defensible technical response. Its developer motivation is recorded in docs/research/A2_DOMAIN_MODEL.md, but personal experience is not presented as representative empirical research.

The practical problem addressed here is the combination of distributed educational conditions, incomplete learner evidence and preference-based exploration in one explainable prototype. WP5 source review supplied a concrete example: A/L subject passes were insufficient to resolve all UGC general-entry and selection conditions. This finding motivates explicit uncertainty rather than an optimistic eligible/not-eligible shortcut. It does not establish that existing commercial guidance systems universally lack these safeguards.

## 1.2 Approved aim and objectives

The approved aim is: “The aim of this project is to design, develop, and evaluate an AI-powered, policy-aware Education and Career Pathway Intelligence System that provides personalised, explainable, and accessible education and career guidance for Sri Lankan learners.”

The eight approved objectives are reproduced without alteration in appendix A, together with original FR1–FR9, NFR1–NFR7 and deliverables D1–D10. These have now been checked against the original proposal (Kanakarathna, 2026a), not merely conversation excerpts. In this dissertation they connect literature/problem investigation (I–II), structured knowledge and hybrid recommendation (III–IV), a usable web artifact (V–VI), and evaluation/limitations (VII–VIII). Implementation evidence is strongest for III–V; human and language/accessibility validation is incomplete. A functional prototype alone cannot establish attainment of the whole research aim.

## 1.3 Approved research questions

**MAIN RESEARCH QUESTION**

How can an AI-powered, policy-aware Education and Career Pathway Intelligence System support Sri Lankan learners through personalised, explainable, and accessible pathway recommendations?

**SUPPORTING RESEARCH QUESTIONS**

I. How can learner profiles, eligibility requirements and pathway knowledge be integrated to generate suitable recommendations?

II. How can explainable recommendation mechanisms improve user understanding and trust?

III. How can alternative pathway generation and skill-gap identification support educational and career planning?

IV. How can multilingual support, mobile usability and voice-assisted input improve accessibility?

V. How effective is the prototype in providing relevant and usable pathway guidance?

These exact questions have now been checked against original proposal §1.4 and interim §1.4 (Kanakarathna, 2026a; 2026b). Their wording and the eight objective statements agree across the confirmed documents and the previously supplied excerpts. MRQ denotes the main question and SRQ-I–V denote the supporting questions, distinct from objective numbers. The [research-question traceability](RESEARCH_QUESTION_TRACEABILITY.md) maps each question to components, methods, evidence and remaining work. Questions concerning improvement, relevance and usability do not yet have empirical answers.

## 1.4 Scope and intended contribution

Target users are A/L learners, vocational learners and early-career users. O/L results support relevant entry routes. Initial domains are IT, Business and Management, and Engineering. The delivered catalogue has seven IT, one Business and three Engineering programmes; it is deliberately uneven and cannot support national coverage claims. Nationwide production deployment, full national education coverage, advanced deep-learning predictive modelling and unrestricted conversational AI are outside the approved scope. Accounts and durable profile storage were not implemented in the author-authorised bounded prototype. Broader role/storage features in the proposal diagrams remain an explicit scope interpretation requiring supervisor acknowledgement, as discussed in section 4.6.

The interim report dated 25 August 2026 already documented a rule-driven FastAPI/HTML/CSS/JavaScript prototype with O/L/A/L input, qualification progression, career relationships and 40 passing automated tests (Kanakarathna, 2026b, §4.8–5.2). October work extended that artifact rather than starting it anew. The contribution is an integrated artifact in which sourced constraints, learner self-reports and AI-derived relevance remain distinguishable. A second contribution is an auditable evaluation record that exposes where software behaviour has been verified and where educational accuracy, relevance or usability still requires independent work. This is an application/design contribution, not a new embedding algorithm or a claim to have solved career decision-making.

## 1.5 Dissertation structure

The literature chapter establishes the choice of constraints, content similarity and multidimensional evaluation. Methodology connects iterative artifact construction to Design Science Research. Requirements, implementation and knowledge construction explain what was actually built. The evaluation and discussion chapters interpret saved evidence and identify limits. The final chapter states bounded conclusions and prioritises future work.


---

# 2. Critical literature review and research gap

> **AI-assisted working material for the student’s review; not final or submission-ready.** This integrated draft consolidates previously prepared section drafts and evidence maps. Before using it, the student must read the cited primary sources, confirm every interpretation and reference against the originals, rewrite the argument in their own voice, and check UWL’s permitted AI-assistance and referencing requirements. It reports no human-participant findings and makes no claim that WiseLanka is effective or superior.

## 2.1 Review approach and evidential limits

This chapter is a focused narrative review of literature and authoritative documents relevant to the approved WiseLanka aim. It considers educational and career recommenders, learner agency, knowledge- and constraint-based methods, lexical and semantic ranking, explanation and user experience, Sri Lankan guidance and accessibility context, and evaluation methods. These themes map to the research questions: integration of profiles, rules and pathways (Supporting Question I); explanation and trust (II); alternatives and skill gaps (III); language, mobile use and voice (IV); and recommendation relevance and usability (V). The main question and approved objectives remain unchanged. The review informs design choices; it does not answer empirical questions about WiseLanka’s users or outcomes.

Sources were located through the project’s focused review of publisher and proceedings records, accessible original papers, official reports and standards, model documentation, and references in the approved proposal and interim report. Relevant source records were checked on 29 October and 5 November 2026. The source register and Stage 1 evidence matrix distinguish full text examined, abstract or metadata only, official administrative information, and failed or limited access. No database search strategy, exhaustive screening, search counts, systematic-review flow or inter-rater process was conducted; this chapter therefore does not present itself as a systematic review. Abstract-only studies are used only for claims visible in their abstracts. The student should extend full-text searching through UWL library access before claiming comprehensive coverage or completing Objective I.

## 2.2 Educational recommendation and learner agency

Educational recommender research addresses different tasks. Learning-resource recommendation supports instructional activity, while programme and career guidance informs choices involving formal prerequisites and progression conditions. A ranking result in a learning-resource setting cannot establish that a programme is suitable for admission or career planning. Deschênes’ (2020) systematic review covers 56 studies on learner agency in learning contexts and distinguishes recommendation accuracy, satisfaction and learning-performance evaluation. It explicitly excludes learning-path recommenders. It therefore cautions against equating retrieval with learner benefit but does not establish how Sri Lankan learners should choose qualifications.

Da Silva et al. (2023) also review teaching-and-learning recommenders. Their publisher abstract reports 756 screened records and 16 included studies, with hybrid methods prominent and comparatively limited attention to pedagogical effectiveness. Since the full review was not examined, these aggregate statements do not support claims about individual methods or study quality. They suggest a measurement concern rather than a general algorithmic conclusion: technical recommendation measures do not by themselves establish a learning or decision benefit. This interpretation informs WiseLanka’s separation of software tests, ranking evaluation and user evaluation; it does not show that the prototype improves education.

Lahoud et al. (2023) provide a closer, although non-equivalent, comparator by comparing university-major and career-domain recommendation approaches in a Lebanese case study. Their paper describes graduate profiles and course ratings, then reports separate filtered datasets for particular collaborative-filtering and ontology/case-based experiments. The reported totals (including 869 collected profiles and 20,000 ratings, 469 cases in one collaborative-filtering experiment, and a separate 658-case base) belong to different stages or experiments and must not be pooled as one sample. The study also involves high-school students, university students and graduates. Similar-case, personalisation, usefulness or satisfaction results do not establish formal admission correctness or provide a comparable ranking benchmark for WiseLanka. Its context, data and methods limit direct transfer to Sri Lankan pathways.

Together, these works show that educational-resource recommendation and programme/career guidance are related but distinct research areas. The former offers evidence about recommendation tasks and learner outcomes; the latter is closer to qualification decisions but remains context- and data-dependent. Neither body of evidence establishes current needs across Sri Lankan A/L learners, vocational learners and early-career users. WiseLanka’s evaluation must therefore test locally grounded scenarios and avoid treating published results from other domains as evidence of its own relevance or benefit.

## 2.3 Explicit constraints and hybrid recommendation

Constraint-based recommenders model explicit requirements and domain knowledge, which can be useful when a candidate must satisfy conditions rather than merely resemble a preference description (Felfernig et al., 2015). Burke’s (2002) survey shows that “hybrid” covers multiple combinations; his empirical work concerns a restaurant recommender and historical interaction logs. These sources explain method families, not whether a hybrid system is necessarily better for education guidance. Their datasets and outcomes do not verify admission policy, source currency or learner comprehension.

This distinction motivates separating formal eligibility from relevance ranking. As described in WiseLanka’s implementation, `MET` denotes that available learner evidence satisfies a documented rule, `NOT_MET` that evidence demonstrates an unmet rule, and `NOT_ASSESSED` that information is insufficient. The content ranker orders exploration within the applicable academic assessment groups; similarity cannot compensate for unmet or unassessed academic requirements. These states and their use are project design decisions, not findings established by the recommender literature. Treating absent evidence as unknown is a conservative inference that still depends on valid source data, correct rule encoding and user comprehension.

The alternatives also depend on different evidence. Rules represent explicit conditions but do not interpret varied expressions of interest. Collaborative filtering requires interaction or rating data that WiseLanka does not possess legitimately; synthetic feedback would not be evidence of learner preference. A hybrid sequence can be useful as an architectural separation, but its value must be measured within this project rather than inferred from Burke’s or Lahoud et al.’s domain-specific results. Source errors remain possible even if a rule is executed exactly as coded.

## 2.4 Lexical and semantic content matching

Salton and Buckley (1988) examine term-weighting combinations in vector-space retrieval. Their work supports a lexical comparator using term frequency, inverse document frequency and normalisation, but does not establish the quality of WiseLanka’s specific smoothed-IDF implementation. Lexical overlap can make a match inspectable; where a learner and programme use different wording, the match may be weak. That latter point is an application-specific expectation, not a reported WiseLanka outcome.

Sentence-BERT (SBERT) uses siamese or triplet structures to produce sentence representations that can be compared by cosine similarity (Reimers and Gurevych, 2019). Its benchmark evaluations concern NLP similarity and transfer tasks, not programme suitability. Wang et al. (2020) describe MiniLM’s self-attention distillation for Transformer compression; that work supports a compact-model rationale but does not validate WiseLanka’s deployed sentence model or its educational use. Published benchmark results must not be transferred as WiseLanka accuracy. Frozen semantic similarity is a relevance signal, not an admission or career-success probability. The implementation’s English-only semantic input, described in the hybrid-recommendation section, means interface translation does not establish Sinhala or Tamil model understanding.

The three ranking approaches—deterministic ordering, TF–IDF and frozen semantic similarity—can be compared on identical learner scenarios and candidate sets within unchanged academic-status groups. Without independent relevance judgements, ranking differences, stability and runtime are descriptive observations, not evidence that one method recommends better programmes. This makes the system comparison an empirical question, not a conclusion supplied by the model literature.

## 2.5 Explanations, understanding and persuasion

Explanations may seek transparency, scrutability, trust, persuasiveness, effectiveness, satisfaction or efficiency, and these aims can conflict (Tintarev and Masthoff, 2012). The available publisher abstract describes four studies in movie and camera recommender settings; it supports the broad distinction among explanation goals, not detailed transfer to education. A persuasive or satisfying explanation does not by itself establish factual correctness or learner understanding. WiseLanka’s similarity explanation describes the matching method and is not a faithful attribution of individual embedding dimensions.

Knijnenburg et al. (2012) offer a user-centred framework that distinguishes system properties and user behaviour from perceptions and experience. The framework informs the decision to measure different outcomes, but does not validate WiseLanka’s instruments or prove education-specific trust effects. For this project, rule/source correctness, comprehension of eligibility and uncertainty, perceived clarity or usefulness, and trust should be assessed separately. A participant may rate an explanation as clear while misunderstanding a condition; observed task performance and self-reported perception can disagree.

WiseLanka displays academic assessment and its rationale separately from semantic relevance, with source links where available. This is an implementation choice intended to make the evidence inspectable, not evidence that users understand or trust the output. Traceability cannot make an outdated or incomplete source correct. Missing, conflicting or provider-controlled information should remain visible as uncertainty; whether these explanations are understood requires direct evaluation.

## 2.6 Local guidance context and accessibility

Sri Lankan pathway sources differ in purpose and date. The National Education Commission’s study documents a policy-oriented investigation of career guidance in general education (National Education Commission, 2016). It is historical context, not evidence of current provision, adult or vocational learner needs, or present programme demand. The UGC 2025/2026 handbook is a primary source for state-university rules in that intake; it does not establish later rules, learner needs or coverage of all vocational and provider routes (University Grants Commission Sri Lanka, 2025/2026). Policy evidence can substantiate a particular condition without showing that guidance is effective or understood.

Vocational evidence is also bounded. WiseLanka contains selected provider-documented vocational, foundation and conditional progression records, not a national qualification or equivalency map. A provider’s stated progression condition supports only that route and remains conditional; it does not imply guaranteed entry or transferability. The TVEC CareerOne operational document was not retrieved in full, so no detailed requirements or effectiveness claim is based on it (Tertiary and Vocational Education Commission, 2025). The knowledge base should be presented as a limited, source-linked prototype, with coverage and source dates explicit. CareerMe’s homepage advertises degree, subject and skills matching and language options (CareerMe, n.d.); this is a provider description, not independent evidence of effectiveness. No exhaustive competitor or user comparison supports a “first” or “only” claim.

UNICEF Sri Lanka’s digital-landscape study combined survey and qualitative methods, including 5,349 children aged 11–18, focus groups and key-informant work. Its tools were pretested in Sinhala, Tamil and English, and it examined access through mobile phones and computers (UNICEF Sri Lanka, 2018). This historical child-focused study makes access and language relevant design questions, but cannot establish current adult or mobile access, learner preferences, or comprehension of translated educational guidance. Its statistics must not be presented as current. The reviewed sources do not directly validate WiseLanka’s Sinhala or Tamil content: interface translation is not evidence of terminology quality or comprehension, which require fluent-speaker and user review.

WCAG 2.2 provides testable web-content criteria across devices and disability-related needs, while acknowledging that it does not address every need (W3C, 2024). It is a normative framework, not proof of conformance or task access. WiseLanka’s axe scans cover selected states and WCAG 2.0/2.1 tags; keyboard, screen-reader, high-zoom, real mobile, language and microphone checks remain pending (`docs/evidence/wp5/ACCESSIBILITY_REVIEW.md`). Responsive styling and zero detected violations therefore do not establish practical accessibility. A local visual-impairment study flagged in the reference-verification register is excluded because its statistical reporting remains unresolved.

## 2.7 Evaluation and the bounded research gap

Evaluation must distinguish rule execution, the correctness and currency of source data, and relevance to stated interests. Passing a test shows that software follows a specified path; its expected answer may still rely on stale or misinterpreted evidence. A correct source rule can also be implemented incorrectly. Source adjudication and software tests therefore need separate records of learner route, date, conditions and uncertainty. `NOT_ASSESSED` is appropriate when evidence is absent; it is neither a rejection nor proof that the catalogue is complete.

Ranking is a separate construct. Deterministic, TF–IDF and frozen MiniLM orderings can be compared on identical scenarios and candidate pools within unchanged academic-status groups; output differences and latency do not show relevance quality. Precision@K is the proportion of the top K items labelled relevant under a declared binary threshold, but ignores order within that set and depends on the threshold (Järvelin and Kekäläinen, 2002). Normalised discounted cumulative gain (nDCG) supports graded judgements and discounts lower ranks (Järvelin and Kekäläinen, 2002). It requires independent labels, consistent candidate pools and a calculable ideal ranking. For this small catalogue, nDCG@3 should be reported only for sufficiently complete rated pools; missing or unjudgeable ratings remain missing. Neither measure tests eligibility correctness or learner benefit.

Human evaluation also requires distinct measures: completion, errors and help requests describe interaction; comprehension questions test interpretation; clarity, usefulness and trust ratings capture perceptions; open comments support qualitative analysis. They may conflict—a positive clarity rating does not prove correct understanding. Knijnenburg et al. (2012) distinguish system properties, behaviour, perceptions and experience, but do not validate WiseLanka’s instruments or establish educational effects. The planned adult-user study remains prospective pending confirmation of the actual ethics conditions; no participant findings are available.

If approved and later conducted, a small convenience sample could identify exploratory usability and comprehension problems, but would not establish population effectiveness or causal improvement. Likewise, independent relevance judgements can support a bounded ranking comparison but would not establish admission correctness. The measures address different questions and should not be collapsed into one “accuracy” score.

## 2.8 Synthesis of alternatives

The literature supports design alternatives, not a universally best method. Reviews of learning-resource recommenders separate algorithmic measures from learner outcomes, while Lahoud et al. show that knowledge-based and collaborative methods have been applied to programme and career guidance in a Lebanese, data-rich case study. Burke and Felfernig et al. explain hybrid and constraint-based approaches, but their evidence does not establish WiseLanka’s effectiveness. Differences in tasks, populations and datasets limit transfer.

This comparison supports keeping formal eligibility distinct from interest relevance. The rule engine determines `MET`, `NOT_MET` or `NOT_ASSESSED` from available evidence; semantic similarity cannot compensate for a failed or unknown requirement. These are WiseLanka design decisions, not published findings. They also depend on current, correctly interpreted source data and cannot resolve unmodelled provider decisions.

Evaluation must follow the same separation. Source adjudication tests whether the encoded requirement reflects applicable evidence; functional tests test whether software applies that rule; independent judgements assess interest relevance; user tasks and questions assess interaction and comprehension; ratings describe perceived clarity, usefulness or trust. None substitutes for another. A system can execute an incorrect rule, rank an ineligible option as relevant, or present an explanation that users misunderstand. The project’s synthetic tests and comparator observations therefore cannot establish educational accuracy, ranking superiority or user benefit; human and independent relevance results remain pending.

Local evidence is also limited: historical guidance and child digital-access studies are not current target-user evidence, admissions handbooks are cycle-specific, provider claims do not establish effectiveness, and the detailed TVEC source was not retrieved. The bounded gap is not the absence of hybrid recommenders. It is whether a small Sri Lankan prototype can connect selected source-linked pathway knowledge with explicit eligibility constraints, bounded AI-assisted relevance, and explanations of evidence and uncertainty, then evaluate these properties separately. This contributes to Objective I but does not make the review exhaustive; current target-group needs under Objective II remain insufficiently established. Objectives III–VII inform system and evaluation design, while Objective VIII requires limitations to remain explicit. The literature motivates this investigation but does not establish that WiseLanka is relevant, understood, trusted, accessible or effective.


# 3. Research methodology and ethics

> **Working revision for the student's critical review.** This AI-assisted draft is not approved or submission-ready. The student must verify each claim against the original records, read and understand the cited sources, and revise the prose in accordance with UWL's academic-integrity and permitted AI-use requirements. No human study or independent relevance-rating exercise has been conducted.

## 3.1 Research approach

WiseLanka uses Design Science Research (DSR) as its principal research methodology, with Agile-inspired iterative prototyping as the software-development approach. These labels describe different levels of the work. DSR structures the investigation around designing, demonstrating and evaluating an artefact for an identified problem; iterative prototyping describes how the software was incrementally built and corrected. The August interim report also describes a pragmatic orientation and deductive translation of requirements into rules (Kanakarathna, 2026b, §§3.1–3.4). In this project, deduction is visible where documented admission conditions and approved requirements were translated into explicit data and rule predicates. Iterative inspection and correction also involved interpreting source material and test failures. The project did not operationalise or compare competing philosophical paradigms, and “pragmatic” should therefore be read as the interim report's applied orientation rather than a separately tested philosophical claim.

DSR is appropriate to the approved aim because the project constructs a bounded information-system artefact and examines whether its specified components behave as intended. The methodological contribution is not code alone: it includes a traceable knowledge representation, a conservative eligibility boundary, a comparison of ranking behaviours, and evidence about the limits of the prototype. Hevner et al. (2004) is cited in the approved proposal and interim report as a DSR foundation; the current source register records metadata/abstract-level verification, so the student should inspect the primary article before relying on detailed interpretations. Peffers et al. (2007), whose paper copy is recorded as examined in the bibliography, provides a process framing of problem identification, objectives, design and development, demonstration, evaluation and communication. This project uses that framing retrospectively to organise work-package evidence; it does not claim that every activity was prospectively planned or recorded as a formal DSR cycle.

The approved project follows DSR with Agile-inspired iterative prototyping. The development record shows incremental construction and correction, but there is no complete contemporaneous sprint diary. Accordingly, iteration is evidenced through versioned artefacts, tests and documented corrections rather than a claim of strict adherence to a named Agile framework. The project also does not report a completed mixed-methods user study: questionnaire and observation instruments are prepared, but participant data collection remains pending.

## 3.2 Project problem, objectives and requirements

The approved proposal identifies the challenge of navigating education and career progression and sets the aim of designing, developing and evaluating an AI-powered, policy-aware guidance system for Sri Lankan learners. Its eight objectives and Functional Requirements FR1–FR9 remain the controlling baseline; this chapter does not revise their wording. The August interim report documents an early implementation and initial verification. Its screenshots and report record 40 passing automated tests at that stage. That count is a historical milestone, not a denominator to be added to later tests.

The requirements baseline was established through analysis of the approved proposal and interim report, then traced into implementation and verification records. This is documentary requirements analysis, not empirical research with learners. No interviews, surveys or focus groups were conducted to establish current needs among A/L students, vocational learners or early-career users. Consequently, Objective II's analysis of learner challenges is supported by approved documents and secondary/contextual sources but is not validated by newly collected target-user evidence. The prototype's design assumptions should not be presented as participant-derived requirements.

The scope was deliberately bounded to selected programmes in Information Technology, Business and Management, and Engineering, with selected vocational and alternative progression routes. The active catalogue contains 11 programmes—seven IT, one Business and Management, and three Engineering—plus 12 qualifications, 33 entry-requirement records, five progression relationships and 21 registered evidence sources in the evaluated snapshot. The unequal coverage is a feasibility boundary, not a representative sample of Sri Lankan education. The project uses CSV files to make the curated records inspectable and versionable; CSV integrity validation can identify structural defects such as duplicate identifiers or broken relationships, but cannot establish the truth, currency or completeness of the underlying educational claims.

## 3.3 Knowledge-base construction and source verification

The knowledge base separates programme and qualification descriptions, eligibility requirements, progression relationships, career mappings, scholarships and source provenance. Records link relevant rules and pathway claims to registered sources. This structure makes the basis of selected recommendations inspectable and permits a rule to remain unassessed when its requirements or a learner's evidence are incomplete. It is a curated prototype dataset, not a complete national education ontology or live institutional feed.

The construction process combined requirements-derived fields with manual extraction and checking of provider and regulator material. A data-integrity validator checked the active CSV collection; the educational correctness sprint recorded dataset identities and hashes, source URLs, access outcomes, and the scope of each source review. It reported 16 source records verified within stated scope, four partially verified and one outdated in that audit snapshot. These classifications apply only to the reviewed claims and dates; a reachable official page is not automatically independent confirmation of every interpretation. Some provider decisions, current intake rules, vocational equivalencies and selection conditions remain unresolved. No equivalence or admission condition was inferred to fill a data gap.

For a separate educational correctness exercise, 45 synthetic scenarios were defined with expected outcomes documented from source material and an explicit conservative uncertainty convention before executing the application. The original baseline recorded 42 agreements and three disagreements. A targeted remediation and controlled replay recorded 43 agreements and two remaining input-contract limitations, EC39 and EC40, concerning age-at-registration and Common General Paper attempt information not represented in the tested request. The original baseline remains preserved; these results are not pooled as independent samples. The evaluator had implemented and inspected the system, so the exercise is source-grounded but not independent domain adjudication. It assesses selected cases rather than national admissions accuracy.

## 3.4 System design and eligibility method

The implemented system uses a modular FastAPI backend, an HTML/CSS/JavaScript frontend and the structured CSV catalogue. This differs from the Streamlit/Python-oriented stack suggested in the proposal. The change retains the proposed web-based prototype, Python rules and curated dataset while separating API/domain behavior from the browser interface. It also supports direct testing of request/response contracts and a responsive client without introducing a database for educational content. The stack change is an implementation decision, not a change to the approved aim or scope.

Academic eligibility is determined by the existing deterministic rules engine. The output states `MET`, `NOT_MET` or `NOT_ASSESSED` represent the relation between supplied evidence and encoded requirements: `MET` means the recorded evidence satisfies the encoded conditions; `NOT_MET` means a documented condition is demonstrably unsatisfied; `NOT_ASSESSED` means evidence, rule coverage or provider determination is insufficient. None is an admission decision. The system does not treat missing information as failure or success where the distinction cannot be supported. Documented provider selection and general-entry conditions may keep an otherwise promising application `NOT_ASSESSED` pending provider review.

The method separates rule execution from rule validity. Automated tests establish whether the software applies encoded predicates and preserves missing-evidence semantics. Source review asks whether selected predicates correspond to stated official conditions. Neither alone proves that a provider would admit an individual learner. The source-grounded scenario exercise offers a bounded check of both layers while retaining the evaluator-independence limitation described above.

## 3.5 Hybrid recommendation methods

The recommendation design combines the authoritative eligibility engine with bounded relevance ordering. It compares three methods on equivalent candidate sets and learner-interest scenarios: the existing deterministic/grouped ordering, a TF–IDF/cosine content-similarity baseline, and local inference using a frozen pretrained `sentence-transformers/all-MiniLM-L6-v2` model exported to ONNX. TF–IDF and MiniLM similarity values express text relationship under their respective representations; they are not probabilities of admission, career success or educational suitability. MiniLM is pretrained and frozen. It was not trained or updated using WiseLanka learner feedback; TF–IDF likewise does not learn a user's preferences.

Academic status remains a separate policy boundary. The system ranks within eligibility-status groups and preserves the defined group order, so a semantically similar `NOT_MET` programme cannot become `MET` because of its relevance score. Missing-interest and model-unavailable conditions have deterministic fallback behavior. The model runs locally from pinned assets, avoiding an inference API for learner profile text; this does not remove the model's language or domain limitations.

## 3.6 Verification and evaluation methods

Evaluation was divided into software verification, data/source checks, synthetic scenario analysis, method comparison and human-centred evaluation. These answer different questions and are not combined into one “accuracy” score.

**Software verification (completed).** The current AI-enabled backend run reported 269 passed, zero failed and zero skipped; targeted tests exercised actual ONNX inference and a synthetic request confirmed semantic mode and eligibility grouping. Saved earlier evidence includes browser/live-integration, CSV integrity, fresh-environment and automated accessibility checks. The historical WP5 snapshot reported 205 backend tests, 36 browser tests and five live workflows; these are dated results, not part of the current 269. Zero findings in nine automated accessibility states is limited to the scanned states/rules and is not conformance certification. Archive the complete current run command, environment, output and exit code if not already saved.

**Educational correctness (completed, bounded).** The 45-case baseline and controlled replay are described in §3.3. Their expected results were source-grounded but assessed by the implementer; agreement is not independent adjudication or national accuracy. The 16/4/1 source classifications are similarly limited to the reviewed snapshot and claims.

**Ranking behavior (completed, descriptive).** Sprint 2B compared deterministic ordering, TF–IDF and MiniLM over 21 synthetic scenarios (63 method/scenario rows and 1,890 warm measurements). Nine scenarios were development-exposed; 12 were catalogue-aware follow-ups, not held-out cases. The methods differed in ordering, while candidate membership and eligibility partitions remained stable. On one Apple M4 with ONNX CPU threads set to one, MiniLM warm rank latency was median 3.254 ms and p95 4.674 ms; model-load median was 285.271 ms and worker peak RSS median 318.83 MiB. These operational measurements are environment-specific. With no independent relevance labels, no ranking-quality metric or superiority conclusion is supported. Independent relevance review is prepared but not conducted.

**Adult usability and explanation evaluation (prepared, not conducted).** A four-task supervised procedure is proposed to preserve the provisional baseline aligned with the existing questionnaire: (1) enter an A/L learner profile and inspect programme recommendations, eligibility and explanations; (2) explore career pathways from the prior result; (3) enter an O/L profile and inspect a foundation route; and (4) examine progression from that qualification, including conditions and next steps. These tasks use fictional profiles. The proposal would record task outcomes only if observation is authorised, and keep completion, assistance, errors, comprehension answers, clarity/usefulness ratings and qualitative comments as separate measures. Questionnaire responses are not objective measures of task success, and perceived usefulness is not recommendation correctness or trust. The current custom questionnaire is not a validated SUS or trust scale.

This four-task protocol is a review proposal, not a frozen or authorised procedure. Later moderator cards, addenda and source-lookup comparisons differ in task count or measures and are not silently substituted. The exact instrument versions, observation, optional skipping, debrief, storage and proposed sample/burden require reconciliation with the signed ethics decision and supervisor/university guidance. The documents currently available do not establish that the exact procedure is covered. No recruitment, pilot with human participants, or questionnaire collection has taken place; there are zero genuine participant responses.

**Independent relevance evaluation (prepared, not conducted).** A separate method-blinded judgement exercise is proposed so reviewers assess programme-text relevance to synthetic interests without seeing the ranking method, score or position. This is distinct from the usability study: reviewers' text-fit judgements would not measure learner satisfaction, comprehension or real-world fit. The prepared pack has version discrepancies (including 127-pair versus older 51-pair material) and needs one version frozen before any use. Reviewer eligibility, number, instructions, ethics status and data handling also require confirmation. Metrics such as nDCG@3 are appropriate only for candidate groups with adequate independently rated candidates and complete labels; no ratings or metric values currently exist.

## 3.7 Ethics, data protection and research status

The approved proposal excludes under-18 participants and unnecessary sensitive learner data. The prototype can be demonstrated with synthetic profiles, and its research collection switch defaults to disabled. Synthetic reporting demonstrations and test submissions are not participant evidence. The project has no genuine participant responses and the current chapter reports no usability, trust, comprehension or independent ranking findings.

An ethics submission receipt and draft materials do not establish final approval. The signed decision and its conditions, plus confirmation that the exact task, questionnaire, observation, recruitment and storage procedure are covered, must be inspected before recruitment or data collection. Existing reconciliation records identify unresolved differences: the ethics form's observation and optional-question entries conflict with later instruments; confidentiality, coded linked observations, withdrawal, debriefing, speech processing and the proposed independent judge/source-lookup activities need explicit determination. Do not describe the evaluation proposal as approved. Collection must remain disabled unless the applicable university authority confirms the procedure and data controls.

If authorised, the study should use only the approved adult recruitment route, fictional educational profiles and the minimum records needed for the study. Consent evidence must be handled separately from responses as required by the approved procedure; the researcher must not promise anonymity if a coded session link or distinctive comment permits re-identification. Hosting, access restriction, encryption/HTTPS, retention, withdrawal, deletion, backup and reporting controls must match the signed ethics and university data-management requirements. No names, email addresses, birthdates, real grades, certificate information or audio should be collected unless an approved protocol explicitly requires them. Voice recognition may involve browser or external service processing and cannot be described as local/offline without verification.

## 3.8 Validity, limitations and methodological alignment

**Construct validity** is protected by separating eligibility status, text similarity, task completion, comprehension, perceived clarity/usefulness and relevance judgements. The custom questionnaire is not a validated scale, and observed task performance cannot be inferred from self-report. **Internal validity** is limited by implementer-authored scenarios and expected outcomes, moderator involvement, possible assistance, and the absence of independent ranking labels. The source-grounded evaluation mitigates unsupported expectations by recording official text, but not evaluator dependence.

**External validity** is limited by 11 unevenly distributed programmes, selected rules and synthetic learner profiles. The catalogue cannot represent nationwide pathways or establish generalisability to all learners, institutions, intakes or languages. **Temporal validity** is threatened by changing admission handbooks and provider pages. **Operational validity** is limited by performance measurements on one Apple M4 environment and by pending manual mobile, screen-reader, keyboard, zoom, fluent Sinhala/Tamil and native microphone checks. The accessibility scans are not certification; mocked voice/browser capability tests do not establish native speech-recognition accuracy.

The method supports the approved objectives to different degrees. Literature and requirements analysis support Objectives I and III, though the review remains a bounded working draft and current learner needs are not directly studied. The structured catalogue supports Objective III within its limited scope. Eligibility, ranking, explanation, pathway and software checks provide technical evidence relevant to Objectives IV, V and VII, but do not establish educational effectiveness. Interface language, mobile and voice features address Objective VI at implementation level while human and manual validation remains outstanding. Limitations and future work are documented for Objective VIII. Accordingly, the system can be discussed as a technically verified prototype with bounded source-grounded evaluation, not as a validated guidance service or proven improvement to learner outcomes.

## 3.9 Chapter summary

This chapter has described the approved DSR framing, the iterative artifact-development approach, CSV knowledge construction, source-grounded eligibility, grouped hybrid ranking and the evidence used to verify the prototype. It has distinguished completed technical evaluation from prepared human and independent-judgement procedures. The next results and discussion chapters must preserve those boundaries, report only recorded evidence, and leave empirical questions unanswered where the required authorised data have not been collected.


# 4. Requirements analysis and system design

## 4.1 Baseline and boundaries

Appendix A preserves the original-document-verified aim, eight objectives, questions, FR1–FR9, NFR1–NFR7 and D1–D10. The target categories are A/L, vocational and early-career learners; O/L results support foundation entry. Profiles collect educational evidence, interests, optional career intentions/preferences, structured awards and optional self-reported skills. The approved NFRs are user-friendly interface, mobile-friendly usability, acceptable response time, reliable educational datasets, modular system architecture, future scalability support and explainable recommendation outputs (Kanakarathna, 2026a, Table 3). They are qualitative: this proposal supplies no numerical latency, load or participant target. Measured local timings therefore cannot retrospectively create a passed service-level target.

The interim introduces FR01–FR10 and NFR01–NFR08, refining implementation concerns rather than reproducing the proposal's numbering. The [updated traceability](alignment/REQUIREMENTS_TRACEABILITY.md) explicitly prefixes original P-FR/P-NFR and interim I-FR/I-NFR. For example, original FR8 is chatbot support, whereas interim FR08 is career pathway guidance. Neither that scheme nor the interim's paraphrased objective-area tables replaces the original requirements.

The original-document traceability now supersedes the baseline-availability assumptions in the historical [WP5 matrix](../evidence/wp5/REQUIREMENTS_TRACEABILITY.md), while retaining its distinction between implementation and validation. This distinction prevents the existence of a microphone button or translation catalogue from being counted as evidence of universal accessibility. It also exposes the incomplete human-evaluation element of Objective VII.

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

The proposal's conceptual architecture/use-case figures depict accounts, staff roles, notifications, analytics and persistent databases beyond its concise FR tables. These are not implemented; absence must be documented, not silently treated as an approved exclusion. Current author instructions retain the bounded account-free prototype. Supervisor acknowledgement of this interpretation is still needed; no formal academic scope amendment has been inferred.

A database could offer richer query/concurrency support, but for this small curated snapshot it would add migration and operational work without resolving source correctness. A frontend framework migration would likewise not improve admission evidence. A large or paid generative service would introduce cost, privacy and grounding challenges. The implemented modular FastAPI/CSV/vanilla-JavaScript architecture meets the bounded artifact needs and leaves deployment scaling as future work. Diagrams in appendix C show these component responsibilities and data flow.


---

# 5. Architecture and implementation

## 5.1 Proposed stack and implemented architecture

The proposal suggests Streamlit, Python, Pandas, SQLite/CSV/JSON and lightweight NLP/LLM support (Kanakarathna, 2026a, Table 8 and appendix D). By August, the interim explicitly documents Python/FastAPI, HTML/CSS/JavaScript and structured CSV files (Kanakarathna, 2026b, §§4.3–4.6). October preserved and extended that separation. It would therefore be inaccurate to describe either an unchanged Streamlit implementation or a new October frontend replacement.

The retained architecture permits direct API/domain tests and explicit browser control over dynamic rows, translation, voice and responsive cards. Its cost is coordination of separate browser/API state, CORS and accessible DOM behaviour. CSV files remain within the proposal's main-table options and suit this small versioned corpus, with strict validation compensating for absent database constraints. Neither Pandas nor an application database is currently needed by the implemented row-based rules; no comparative benchmark established that they would be inferior.

Frozen ONNX relevance supplies genuine NLP inference without a paid generation service or invented training data. Explanations and guided chat are deterministic and source-grounded, narrower than the optional LLM-assisted technology illustration. That is a justified engineering interpretation, not proof that every illustrated component was delivered. The [technology decision record](alignment/TECHNOLOGY_JUSTIFICATION.md) preserves alternatives, trade-offs and the remaining supervisor scope decision.

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


---

# 6. Knowledge-base construction and educational validation

## 6.1 Curated snapshot

The August report screenshots (appendix C, Figures 23–30), corroborated by commit `050ba57` dated 20 August 2026, show seven computing programmes, seven qualifications, 17 requirement rows, three progression edges and 14 source records. This is a source/code snapshot, not proof of national coverage or every uncommitted interim state. The WP5 snapshot has 11 programmes, 11 institutions, 12 qualifications, 33 entry-rule rows, five progression relationships, 21 source records, five careers and 13 skills. Domain counts are IT seven, Business and Management one, Engineering three, including two vocational-related programmes. The catalogue is sufficient to demonstrate different routes but too small and uneven to represent national opportunity or learner demand.

Programme titles include Moratuwa IT and AI, UCSC Computer Science, IIT Computing Foundation and three related degrees, OUSL Management Studies, Peradeniya Engineering, Jaffna University College HND Mechatronics and UoVT Engineering Technology in Mechatronics. The programme inventory in appendix B retains exact stored titles and source URLs rather than silently rewriting provider terminology.

The five progression edges comprise three foundation-to-degree routes and two conditional vocational routes. The AI/Data Science foundation route records the published 40% condition in each named module; all edges have `guaranteed=false`. Interim Figures 17/42 and its progression CSV screenshot display 50%, so the final report must state that a correction occurred rather than copying that historical condition as current policy (Kanakarathna, 2026b; Informatics Institute of Technology, n.d.). No evidence establishes that the provider changed its policy between those dates. NVQ route records do not infer universal qualification equivalence or exemption. Current provider checks are unresolved where necessary.

## 6.2 Source selection and provenance

Official regulator and programme/provider documents support represented academic conditions. `data/metadata/evidence_sources.csv` stores organisation, URL and access date; requirement and progression rows point to source IDs. A programme's application URL supports navigation, but does not independently establish every career relationship or recognition claim. Access date is not publication date and must not be interpreted as a live guarantee of currency.

WP5 reviewed selected official UGC, Moratuwa, IIT, OUSL, Peradeniya, UCJ and UoVT material. It did not independently refresh every legacy recognition, career-skill or scholarship record. The full UGC handbook was retrieved and parsed; its checksum and page locations are in the evidence register. No new accreditation, equivalent qualification or scholarship opportunity was invented. Independent provider/domain adjudication remains pending.

## 6.3 Source review as an evaluated correction

The Moratuwa IT page identifies selection context beyond subject grades. The UGC handbook contains general-entry constraints involving one sitting, attempt limits and Common General Paper conditions, together with course/district/year-dependent selection (University Grants Commission Sri Lanka, 2025/2026). Exact source locations and caveats are in the [WP5 review](../evidence/wp5/EDUCATIONAL_SOURCE_REVIEW.md) and rule register. The application does not collect enough evidence to resolve all these conditions.

Before correction, PRG0001–3 could appear fully met from subject passes alone. WP5 added SRC0021 and provider-review rules REQ0032–34 and refreshed PRG0009's existing review condition. The repaired outcome is NOT_ASSESSED where represented subjects pass but those additional decisions remain unknown. This conservative repair is preferable to inventing Z-score thresholds or gathering unnecessary personal information during a small prototype sprint. A known failed mandatory subject remains NOT_MET.

This example distinguishes rule-execution correctness from domain completeness: an engine can perfectly execute an incomplete rule set. Updating tests to match reviewed policy semantics is legitimate only when the supporting source and reasoning are preserved. Earlier failed tests and final passing logs were retained for that purpose.

## 6.4 Integrity and update procedure

Validation checks unique identifiers, foreign-key relationships, permitted domains, grouped operators and numeric count constraints. A frozen dataset SHA256 manifest supports exact reproduction. The rule-evidence CSV inventories all 33 requirements with conditions and source references. The 14 reference cases connect supplied evidence to expected statuses, including incomplete data, a failed subject and conditional vocational investigation.

For future updates, identify the applicable intake/policy year, inspect the original source and exact route, record changes and have ambiguous rules independently reviewed. Run integrity, boundaries, affected scenarios and full regression before accepting a snapshot. Contradictory sources require adjudication or NOT_ASSESSED, not convenient averaging. Removing a provider-review flag would require evidence that the newly collected/verified inputs genuinely resolve that condition.

## 6.5 Remaining educational limitations

Limited Business coverage can distort exploration. Self-reported awards are not authenticated. Career relationships and skill proficiency expectations have weaker provenance than admission rules. One recorded scholarship is historical/closed awareness and cannot represent current financial support. Source URLs and admissions policy can change after the recorded review. The defensible claim is source-aware prototype guidance, not provider-approved advice, comprehensive recognition assurance or automated admissions determination.


---

# 7. Hybrid AI recommendation methodology

## 7.1 Separation of decisions

The interim's implemented recommendation function sorted deterministic match scores; its AI-powered title and planned hybrid discussion are not evidence of pretrained inference at that stage. WP3 subsequently introduced the frozen encoder and TF–IDF comparison. This is a methodological extension of the earlier explicit-constraint design, not retroactive training or an August model result (Kanakarathna, 2026b, §4.5.3 and appendix D).

Let A(p,x) be the canonical academic assessment of programme p using learner evidence x, with values MET, NOT_ASSESSED or NOT_MET. Let R(p,q) be a content-relevance score for stated preference text q. Ranking is lexicographic: first the fixed academic group, then decreasing available relevance, then stable baseline position and programme ID. R never changes A. A high R is neither admission probability nor evidence of career success.

The programme corpus uses recorded title, field, domain and qualification type. It excludes eligibility outcomes and administrative notes from semantic text. It therefore contains short identity/subject descriptors rather than full course curricula. The learner query combines explicit interests, optional English career intention and selected career name, capped at 1,000 characters; tokenisation truncates model input to 256 wordpieces. This restricts both interpretation depth and potential evidence content.

## 7.2 Deterministic and TF–IDF comparisons

The original deterministic order uses existing academic matching with documented career/preference context. WP3 additionally records `legacy_order` before applying fixed academic safety groups. Comparisons must distinguish that raw order from the grouped deterministic baseline; otherwise a policy/grouping change could be misattributed to AI.

TF–IDF is implemented directly in `relevance/engine.py`: term extraction uses lowercase Latin-alphabet tokens, raw counts and smoothed IDF, idf(t)=log((1+N)/(1+df(t)))+1. Document and query vectors are L2-normalised and compared using cosine. The vocabulary/IDF fit uses the frozen active catalogue, not the learner query or relevance labels. This is corpus fitting, not learning an individual user's preferences. Unknown vocabulary contributes no supported lexical match.

## 7.3 Frozen pretrained semantic inference

WiseLanka uses `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, through its ONNX export. The inspected model card records English support and Apache-2.0 licensing (Sentence Transformers, n.d.). No model training or feedback update occurs in this project. Model-artifact hashes and the actual inference implementation are stronger reproducibility evidence than citing the model family name alone.

The local encoder tokenises inputs, runs a CPU ONNX session, performs attention-mask-aware mean pooling and L2 normalisation, then compares query and cached catalogue vectors. It checks finite outputs and bounds numerical scores before returning them. Inputs remain on the local inference machine. The model family's published benchmarks are not reported as this system's educational accuracy.

The explanation states which preference text and catalogue facts were compared. It is deliberately modest: no token-attribution model or causal explanation of embedding dimensions has been implemented. Relevance language must therefore remain methodological rather than claiming the system knows a learner's personality or competence.

## 7.4 Cold start and safe failure

An education/qualification profile is still required, but no historical feedback is needed to rank explicit interests. Empty preference text produces unassessed relevance and baseline ordering. Missing descriptions/source evidence produce no supported score. Missing dependencies, checksum-invalid artifacts, loading or inference errors return explicit unavailable/fallback metadata and null semantic scores. Academic decisions still execute. Stable ties and repeated calls are tested.

Fallback preserves baseline order within safety groups, not necessarily the exact ungrouped historic order. This distinction matters for reproducibility. Optional deployment assets require explicit initial provisioning; runtime does not silently download a model or send learner data to an external service.

## 7.5 Comparison design and leakage prevention

Nine fixed synthetic cases compare the same catalogue/candidate pools using deterministic, TF–IDF and semantic methods. They cover empty preferences, literal/paraphrased IT, Business, Engineering, failed academic requirements, missing evidence, unknown vocabulary and vocational interest. These are functional examples exposed during development, not independent held-out relevance cases.

The planned study requires blinded independent graded relevance judgements on a separate frozen scenario set. For an academic group with n candidates, k=min(3,n); declared exponential gain is 2^r−1 and rank discount is log2(i+1). nDCG@k=DCG@k/IDCG@k only when the candidate pool is fully judged and ideal gain is positive. Missing labels are not zero. Report small/unequal candidate pools and per-domain results instead of concealing them in one average.

No nDCG value is currently computed. Future feedback learning would require opt-in legitimate ratings, participant-separated development/test data, model versioning, privacy controls and audited updates. It is future work, not an automatic self-learning feature. The present comparison demonstrates executable, separated methods and their observed orders; it cannot support superiority without the missing judgement layer.


---

# 8. Testing and evaluation

## 8.1 Evidence snapshots and repeatability

This chapter distinguishes test execution from domain correctness and human evaluation. Stage 9A records the complete backend command, output, timestamp, Python/package versions, Git HEAD, dirty-worktree status and relevant file hashes in `docs/evidence/stage9/STAGE9_TECHNICAL_VERIFICATION.txt`. The run applies to that recorded worktree at HEAD `547525429ab360a9643085b4f25aa0c58083f6a6`, not a clean commit in isolation. Historical work-package manifests remain separate snapshots and are not aggregated as one suite.

## 8.2 Verification layers and development chronology

The August interim report records 40 passing automated tests and an early seven-programme catalogue (Kanakarathna, 2026b). The WP5 snapshot later recorded 205 backend tests, 36 browser tests, five live workflows and selected source/scenario/accessibility checks. Stage 9A then reran the full AI-enabled backend suite; its outcome is analysed in Chapter 9. Counts from different snapshots describe development verification, not a learning curve, accuracy gain or number of learners. Browser/live figures remain the earlier saved WP5 results; they were not rerun in Stage 9A.

The checks address different properties: automated tests exercise software contracts; the CSV validator checks structural relationships; source review compares selected rules with official material; scenario harnesses compare outputs with a declared oracle; ranking experiments describe method behavior and runtime; browser/accessibility tests cover selected rendered states. Success at one layer does not establish success at another. In particular, syntactically consistent educational data can still be inaccurate or outdated.

## 8.3 Educational correctness procedure

The preserved 45-case set uses synthetic learner inputs and scenario expectations documented from source material before the application run. The original baseline and controlled examination-completeness replay are retained separately in `docs/evidence/research-sprint2/educational-correctness/` and `docs/evidence/research-sprint2/completeness-correction/`. The scenario author/evaluator also inspected and implemented the system; this is source-grounded evaluator assessment, not independent domain adjudication. Chapter 9 reports the outcomes and the remaining EC39/EC40 input limitations. No expectation or admission rule was changed to improve the replay count.

## 8.4 Recommendation comparison procedure

The later frozen comparison uses identical candidate pools and academic-status partitions for deterministic ordering, TF–IDF/cosine and pretrained MiniLM ONNX. It includes nine development-exposed and 12 catalogue-aware synthetic scenarios; neither group is an independent held-out set. Repeated warm rank calls and fresh-process observations measure operational behavior on one Apple M4 environment. Since no independent relevance labels exist, the procedure reports rank-order changes, stability, fallback, eligibility-policy preservation and latency only. It does not calculate nDCG, MAP, Precision@K or recommendation accuracy.

## 8.5 Accessibility and multilingual checks

Historical WP5 automated scans found no violations across nine selected states under configured axe rules; prior viewport checks covered selected widths. Browser tests exercised translation switching and mocked speech permission/error states. These results do not certify WCAG conformance, fluent Sinhala/Tamil translation, screen-reader usability, real mobile operation or native microphone transcription. Manual checks remain pending and are not presented as participant findings.

## 8.6 Human studies and independent ratings — not conducted

The four-task supervised usability procedure is a proposal aligned to the provisional original task sheet and questionnaire labels. It would use fictional profiles and, only if authorised, assess task completion, assistance/errors, explanation comprehension, clarity/usefulness and qualitative feedback as separate measures. Later six-card task materials and the source-lookup comparison are not silently substituted. The signed ethics decision and exact approved versions/procedures must be confirmed before recruitment or piloting. Independent relevance rating is a separate proposed activity; pack versions remain to be reconciled. Research collection is disabled, with zero genuine participant responses and zero independent ratings.

# 9. Results and critical discussion

> **AI-assisted working draft for student review only. Not final or submission-ready.** This chapter reports only preserved technical evaluation. All learner cases in the software experiments were synthetic. There are zero genuine participant responses and no independent recommendation relevance ratings. The student must verify and revise this text against the original evidence, assessment guidance and UWL academic-integrity requirements.

## 9.1 What the evidence supports

### Software verification and data integrity

The Stage 9A run recorded 269 backend tests passed, zero failures and zero skips in 1.63 seconds using Python 3.9.6 with NumPy 1.26.4, ONNX Runtime 1.19.2 and tokenizers 0.20.3. This demonstrates that exercised backend cases passed in that environment, not code coverage or correctness of untested policies. The run used Git HEAD `5475254` plus a dirty worktree; its status and relevant file hashes are preserved, so the result is not attributable to a clean commit alone.

The knowledge-base integrity command exited successfully across 20 CSV datasets. The snapshot contained 11 programmes (IT seven, Business and Management one, Engineering three), 12 qualifications, 33 entry-requirement rows, five progression links and 21 registered sources. This supports structural consistency, not the truth or currency of every educational statement. The catalogue is narrow and domain-imbalanced.

The source review classified 16 records as verified within scope, four partially verified and one outdated. These dated classifications do not cover every claim; a reachable URL is not a current provider decision. The result is a traceable bounded dataset, not national coverage.

### Academic-rule behavior and scenario comparison

The original frozen educational correctness evaluation compared 45 synthetic scenarios with source-documented expected outputs and recorded 42 agreements, three disagreements. The controlled replay retained those cases and expectations after the completeness correction; it recorded 43 agreements and two differences. Only EC08 changed: omitted O/L completeness now yields the expected `NOT_ASSESSED`, rather than treating unknown completeness as a confirmed examination failure. Explicitly complete but insufficient results remain `NOT_MET`; invalid values remain validation errors.

EC39's reference includes age 17 against OUSL's documented age condition; EC40 includes CGP marks below the UGC threshold in all allowed attempts. Neither age-at-registration nor CGP attempt history is an API input, so both actual results remain `NOT_ASSESSED`. Expectations and rules were not changed. These are input-coverage limits; adding consequential data would need separate justification.

The 43/45 agreement is bounded to a heterogeneous case set authored and assessed by the implementer, not independent adjudication or a representative admissions sample. Software can apply an outdated or incomplete rule consistently; rule execution and source validity are separate. The result informs Objectives III and VII and SRQ-I only within this prototype scope.

### Hybrid ranking and policy boundary

The saved ranking experiment compared deterministic grouped ordering, TF–IDF/cosine and frozen MiniLM ONNX on 21 synthetic scenarios: nine development-exposed and 12 catalogue-aware, not held-out. Full order differed in 13/21 deterministic–TF–IDF, 19/21 deterministic–MiniLM and 19/21 TF–IDF–MiniLM comparisons; top-1 differed in 10/21, 14/21 and 8/21 respectively. These are ordering differences, not improvements: independent relevance labels are absent.

Recorded `SEMANTIC` outputs and non-null scores confirm inference with pinned `all-MiniLM-L6-v2` ONNX revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`; the experiment also exercised TF–IDF, deterministic order, stability and unavailable-model fallback. Across 63 outputs, candidate membership and `MET` → `NOT_ASSESSED` → `NOT_MET` grouping remained intact. Similarity is not admission probability; `MET` is not guaranteed admission.

On Apple M4, warm rank-function median/p95 was 0.467/0.625 ms deterministic, 0.466/0.601 ms TF–IDF and 3.254/4.674 ms MiniLM. MiniLM load median was 285.271 ms; worker peak RSS median was 318.83 MiB. These measurements exclude eligibility, candidate generation, browser and network; RSS is process high-water, not model-only memory. They show machine-specific cost, not production capacity or user-perceived benefit.

### Findings still not collected

- **Independent recommendation relevance judgements — NOT COLLECTED.** No nDCG@3, MAP, Precision@K or relevance-accuracy result is available.
- **Genuine participant usability findings — NOT COLLECTED.** The supervised adult-user study has not been conducted.
- **Participant comprehension and qualitative feedback — NOT COLLECTED.** Explanation understanding, perceived clarity/usefulness, trust and open-text themes remain unmeasured.

## 9.2 What the evidence does not support

The evidence does not show MiniLM to be more relevant or accurate than TF–IDF or deterministic ordering: no independent judgements exist, and scenarios were development-exposed or catalogue-aware. Passing tests do not establish that every admission condition is complete, current or provider-approved. Eleven programmes cannot represent Sri Lanka's institutions, learners, intakes or pathways.

Rendered explanations do not demonstrate comprehension; functional route or skill-gap generation does not demonstrate better planning. Learner task completion, usefulness, trust, accessibility improvement, educational and admission outcomes are unmeasured. Historical accessibility scans cover selected states; fluent Sinhala/Tamil, assistive-technology and native microphone checks remain pending.

Results address only implementation aspects of the approved questions. Tested integration informs SRQ-I. Whether explanations improve trust/comprehension (SRQ-II), routes aid planning (SRQ-III), accessibility improves access (SRQ-IV), or guidance is relevant and usable (SRQ-V) remains unresolved. Software verification alone does not answer the main question.

## 9.3 Trade-offs and alternative interpretations

The completeness correction illustrates why uncertainty semantics matter. A strictly numeric rule can produce a deterministic result while the evidence needed to interpret it is incomplete. The corrected behavior avoids treating omission as proof of examination failure, but unresolved input fields still constrain assessment, as EC39 and EC40 demonstrate. The conservative `NOT_ASSESSED` status reduces unsupported conclusions; it can also leave users needing provider guidance. Whether learners understand and can act on that uncertainty requires the unconducted comprehension study.

The rank-order differences show that the semantic component is operational rather than decorative, but do not establish that added complexity is worthwhile. With a small catalogue and brief programme descriptions, deterministic ordering or lexical similarity may be adequate in many cases. Conversely, semantic changes for paraphrased interests might be useful; no independent judgement currently distinguishes useful changes from misleading ones. The 7:1 IT-to-Business catalogue imbalance also means that domain comparisons are confounded by coverage. Continued use of MiniLM should be justified by relevance evidence and runtime needs, not by its model label.

CSV storage makes this prototype's records inspectable and structurally testable, but source maintenance remains a human process. The integrity validator cannot detect that an institution has changed an intake condition. Scheduled source review, explicit policy-year labels and independent review would address this risk more directly than changing storage technology.

## 9.4 Objective alignment

The results provide bounded technical evidence for Objective III through the structured catalogue and integrity checks; for Objective IV through tested separation of rule eligibility and AI-assisted relevance; and for Objective V through functioning profile, pathway, explanation and resource features. Objective VII is partly supported by automated and synthetic scenario evaluation, but its usability-feedback component remains incomplete. Objective VI has implementation and selected automated evidence, not validated accessibility outcomes. Objective II remains limited by the absence of current direct learner-needs research. Objective I and Objective VIII are addressed in working literature and limitations drafts but require student validation and final synthesis. No objective should be declared empirically complete solely because the backend test suite passed.

## 9.5 Threats to validity and implications

Internal validity is limited by implementer involvement in scenario and expected-outcome construction. Holding cases constant supports attribution of EC08's correction but does not remove evaluator bias. Construct validity requires separating test passage from educational correctness, similarity from relevance, rendered explanation from comprehension, and ratings from trust.

External validity is constrained by catalogue imbalance and synthetic profiles; temporal validity by changing rules and undated provider pages. Commands, versions and hashes aid reproduction, but Stage 9A used dirty worktree HEAD `5475254`; a clean-commit rerun is needed to attribute results to a stable commit. Performance comes from one machine; accessibility and language validation remain incomplete. These limits define where the findings apply.

**Student completion note:** before integration, reconcile these results with the official assessment brief, retain the Stage 9A raw output and snapshot identity, and replace each “NOT COLLECTED” placeholder only if genuine, authorised evaluation data later exist. Do not convert synthetic scenarios or mocked browser tests into human findings.


# 10. Limitations, future work and conclusion

## 10.1 Current limitations

WiseLanka remains a curated prototype. It covers 11 programmes unevenly across three approved domains; its career-skill and recognition provenance is not uniformly as strong as the reviewed entry-rule evidence. Reported grades, examination completeness and qualifications are not authenticated. Some provider and selection conditions cannot be assessed from the collected profile, and historical scholarship information is not current award availability.

The frozen semantic model performs no feedback learning. Its English content similarity has no independently measured recommendation-quality advantage here. Draft Sinhala/Tamil interface strings are not evidence of fluent educational translation or cross-language semantic capability. Browser speech is optional, vendor-dependent and not verified with native audio. Human usability, screen-reader operation, translation quality and actual educational benefit remain unmeasured.

The author-confirmed original proposal and August interim have now been reviewed. Their title, exact aim/objectives/questions, approved FR/NFRs and deliverables are reconciled with the artifact; no replacement requirements were invented. Signed ethics conditions, actual adult feedback, independent relevance judgements, fluent/native/manual review, supervisor scope decisions and assessment/rubric/poster instructions remain outstanding. The proposal diagrams contain undelivered role/account features beyond the concise FRs, so this ambiguity cannot be declared resolved by implementation success alone. No promise of assessment classification follows from the technical evidence.

## 10.2 Prioritised future work

First resolve the remaining proposal-scope interpretation and signed ethics conditions, then complete approved adult task-based usability and explanation evaluation. Review translations with fluent speakers and test native speech, screen readers and target mobile browsers. Conduct independent source/rule adjudication, prioritising unclear provider routes and weak relationship provenance. Freeze a held-out relevance set, obtain blinded independent judgements and compare methods using appropriate within-group metrics.

Only after legitimate opt-in feedback exists should controlled learning be considered. A future ranker would need versioned training data, participant-level separation, privacy review, bias monitoring and reversible audited promotion. It must continue to rank within authoritative academic groups. No click should be silently interpreted as verified relevance, and no learned score should rewrite policy.

Broader educational coverage should proceed with source-maintenance resources rather than mass unverified scraping. Production deployment would additionally require threat modelling, operational monitoring, data-handling policy and load/device testing. These changes lie beyond the current approved bounded implementation.

## 10.3 Conclusion

The project has produced a modular prototype combining structured educational knowledge, explicit three-state academic assessment, local pretrained semantic ranking, deterministic/TF–IDF comparison and bounded accessible interaction features. Saved technical evidence demonstrates behaviour in tested scenarios and documents corrections discovered through source and accessibility review.

The defensible conclusion is that the proposed separation can be implemented and technically demonstrated within a small curated catalogue. Whether it provides better recommendations or satisfactory guidance to intended learners remains a research question requiring the pending independent and human evaluations. The draft therefore closes with a working artifact and transparent evidence boundaries, rather than an unsupported claim that its full educational value has already been established.


---

# References — provisional author–date style

Most web-source access was checked on 29 October 2026 at the depths recorded below; the UNICEF full report was re-examined on 5 November 2026. The CareerOne document was available as indexed official text while direct retrieval timed out. The two private project documents were inspected locally, not uploaded. This is a working bibliography, not confirmation of the required UWL referencing style. Access depth and restrictions are recorded in SOURCE_REGISTER.csv. Article page ranges below are bibliographic ranges, not fabricated pinpoint citations. No detailed claim is based on an inaccessible full text.

Burke, R. (2002) ‘Hybrid recommender systems: Survey and experiments’, *User Modeling and User-Adapted Interaction*, 12(4), pp. 331–370. https://doi.org/10.1023/A:1021240730564 .

Da Silva, F.L., Slodkowski, B.K., da Silva, K.K.A. and Cazella, S.C. (2023) ‘A systematic literature review on educational recommender systems for teaching and learning: research trends, limitations and opportunities’, *Education and Information Technologies*, 28, pp. 3289–3328. https://doi.org/10.1007/s10639-022-11341-9 . Online publication was in 2022; this draft uses the 2023 volume year.

Deschênes, M. (2020) ‘Recommender systems to support learners’ Agency in a Learning Context: a systematic review’, *International Journal of Educational Technology in Higher Education*, 17, article 50. https://doi.org/10.1186/s41239-020-00219-w .

Felfernig, A., Friedrich, G., Jannach, D. and Zanker, M. (2015) ‘Constraint-based recommender systems’, in Ricci, F., Rokach, L. and Shapira, B. (eds.) *Recommender Systems Handbook*. 2nd edn. Boston, MA: Springer, pp. 161–190. https://doi.org/10.1007/978-1-4899-7637-6_5 .

Hevner, A.R., March, S.T., Park, J. and Ram, S. (2004) ‘Design science in information systems research’, *MIS Quarterly*, 28(1), pp. 75–105. Available at: https://aisel.aisnet.org/misq/vol28/iss1/6/ .

Järvelin, K. and Kekäläinen, J. (2002) ‘Cumulated gain-based evaluation of IR techniques’, *ACM Transactions on Information Systems*, 20(4), pp. 422–446. https://doi.org/10.1145/582415.582418 . Publisher fetch was blocked; original-paper text was accessible at https://faculty.cc.gatech.edu/~zha/CS8803WST/dcg.pdf .

Knijnenburg, B.P., Willemsen, M.C., Gantner, Z., Soncu, H. and Newell, C. (2012) ‘Explaining the user experience of recommender systems’, *User Modeling and User-Adapted Interaction*, 22, pp. 441–504. https://doi.org/10.1007/s11257-011-9118-4 .

National Education Commission (2016) *Study on Career Guidance in General Education in Sri Lanka*. Research Series (2014), No. 08. First published 2016. Available at: https://www.nec.gov.lk/wp-content/uploads/2016/04/8-Final-2.pdf . This is historical context, not current survey evidence collected by this project.

United Nations Children’s Fund (UNICEF) Sri Lanka (2018) *Keeping Children in Sri Lanka Safe and Empowered Online: A Study on Sri Lanka’s Digital Landscape*. Colombo: UNICEF Sri Lanka. Available at: https://www.unicef.org/srilanka/media/281/file/Digital%20landscape%20study.pdf . Full report examined on 5 November 2026. The study concerns children aged 11–18 and digital access/online safety; its historical findings are not current adult-user or educational-guidance evidence.

Peffers, K., Tuunanen, T., Rothenberger, M.A. and Chatterjee, S. (2007) ‘A design science research methodology for information systems research’, *Journal of Management Information Systems*, 24(3), pp. 45–77. https://doi.org/10.2753/MIS0742-1222240302 . Original-paper copy inspected at https://zhang.ist.psu.edu/teaching/504/readings/Peffers.pdf . Citation follows the paper’s supplied 2007 reference rather than its 2014 online posting date.

Reimers, N. and Gurevych, I. (2019) ‘Sentence-BERT: Sentence embeddings using Siamese BERT-networks’, *Proceedings of EMNLP-IJCNLP 2019*, pp. 3982–3992. https://doi.org/10.18653/v1/D19-1410 . Available at: https://aclanthology.org/D19-1410/ .

Salton, G. and Buckley, C. (1988) ‘Term-weighting approaches in automatic text retrieval’, *Information Processing & Management*, 24(5), pp. 513–523. https://doi.org/10.1016/0306-4573(88)90021-0 . Publisher preview: https://www.sciencedirect.com/science/article/pii/0306457388900210 .

Sentence Transformers (n.d.) *all-MiniLM-L6-v2 model card*, revision 1110a243fdf4706b3f48f1d95db1a4f5529b4d41. Available at: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/blob/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/README.md . The repository model lock identifies the actual artifacts, rather than relying on a changing default branch.

Tintarev, N. and Masthoff, J. (2012) ‘Evaluating the effectiveness of explanations for recommender systems’, *User Modeling and User-Adapted Interaction*, 22, pp. 399–439. https://doi.org/10.1007/s11257-011-9117-5 . Publisher preview: https://link.springer.com/article/10.1007/s11257-011-9117-5 .

University Grants Commission Sri Lanka (2025/2026) *University Admissions Handbook: Academic Year 2025/2026*. Available at: https://www.ugc.ac.lk/downloads/admissions/Handbook_2025_26/student_handbook_english.pdf . Policy year is used as the document identifier; a separate publication date was not established. Actual downloaded-file hash and source locations are retained in WP5.

Wang, W., Wei, F., Dong, L., Bao, H., Yang, N. and Zhou, M. (2020) ‘MiniLM: Deep self-attention distillation for task-agnostic compression of pre-trained Transformers’, *Advances in Neural Information Processing Systems*, 33. Available at: https://proceedings.neurips.cc/paper_files/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf .

World Wide Web Consortium (W3C) (2024) *Web Content Accessibility Guidelines (WCAG) 2.2*. Recommendation, 12 December 2024. Version checked: https://www.w3.org/TR/2024/REC-WCAG22-20241212/ . The executed axe scan used the narrower WCAG 2.0/2.1 tag set, not a complete WCAG 2.2 audit.

## Sources added during original-document reconciliation

Kanakarathna, O.T. (2026a) *Design and Development of an AI-Powered, Policy-Aware Education and Career Pathway Intelligence System for Sri Lankan Learners*. Final Project Proposal, CP6SL460, University of West London. Unpublished author-supplied private document; inspected locally. No public URL or unverified submission/approval date is assigned.

Kanakarathna, O.T. (2026b) *Design and Development of an AI-Powered, Policy-Aware Education and Career Pathway Intelligence System for Sri Lankan Learners*. Project Interim Report, 25 August 2026, CP6SL460, University of West London. Unpublished author-supplied private document; inspected locally. Document identities/hashes are recorded in alignment/SOURCE_REVIEW.json; original files are not distributed with this pack.

Lahoud, C., Moussa, S., Obeid, C., El Khoury, H. and Champin, P.-A. (2023) ‘A comparative analysis of different recommender systems for university major and career domain guidance’, *Education and Information Technologies*, 28, pp. 8733–8759. https://doi.org/10.1007/s10639-022-11541-3 . Online publication 28 December 2022; this draft uses the 2023 volume year. Publisher metadata, abstract and introductory comparison inspected; full methodological appraisal remains pending.

CareerMe (n.d.) *CareerMe — Get Personalized Career Guidance — Sri Lanka*. Available at: https://careerme.lk/ . Homepage features checked; these are provider claims, not independent effectiveness evidence.

Tertiary and Vocational Education Commission (TVEC) (2025) *Operational Directives/Guideline, Mandatory Requirements of the “Career One” TVET Career Platform*. Annexure I, effective September 2025. Available at: https://www.careerone.gov.lk/storage/newsletter/Annexure_I.Operational%20directives%20guideline-mandatory%20requirements.pdf . Official indexed title/background text inspected; direct PDF retrieval timed out. Used only to identify advertised scope, not evaluate platform quality.

Informatics Institute of Technology (n.d.) *IIT International Foundation*. Available at: https://www.iit.ac.lk/foundation/it/ . Official entry/progression section checked on 29 October 2026; no publication date established. The four-module 40% condition and conditional year-one progression are distinct from guaranteed admission.

## Educational and technical supporting registers

Official provider/source URLs, organisations, conditions and stored verification dates are listed in appendix B and data/metadata/evidence_sources.csv. The full rule-to-source inventory is docs/evidence/wp5/rule-evidence.csv. These records must be retained with the dissertation; a provider link is not independent verification of every career or recognition relationship.

Repository evidence is cited by artifact path and WP5 commit 07f4b97 throughout the draft. It is project evidence, not external peer-reviewed research. Do not cite Codex as authority for educational or scientific facts.


# Appendix A. Original approved proposal baseline

Both author-confirmed WORK DOCX files have been inspected. The original proposal is the requirements authority; the interim refines implementation concerns without replacing its IDs. Hashes and actual sections/tables/figures reviewed are in alignment/SOURCE_REVIEW.json. Source text below is reproduced without changing approved wording.

## Exact project title

DESIGN AND DEVELOPMENT OF AN AI-POWERED, POLICY-AWARE EDUCATION AND CAREER PATHWAY INTELLIGENCE SYSTEM FOR SRI LANKAN LEARNERS

## Aim

The aim of this project is to design, develop, and evaluate an AI-powered, policy-aware Education and Career Pathway Intelligence System that provides personalised, explainable, and accessible education and career guidance for Sri Lankan learners.

## Objectives

I. To critically review existing literature related to AI-based recommender systems, educational decision-support systems, and career guidance technologies.

II. To analyse the challenges faced by Sri Lankan learners when navigating educational and career progression pathways.

III. To design a structured knowledge base representing learner categories, educational pathways, eligibility rules, scholarship information, and career progression routes.

IV. To develop a hybrid recommendation mechanism combining rule-based eligibility filtering with AI-assisted pathway recommendation and explanation generation.

V. To implement a web-based prototype capable of generating personalised pathway recommendations, alternative routes, skill-gap insights, and official resource links.

VI. To integrate accessibility-focused features such as mobile-friendly usability, multilingual support, and voice-assisted interaction.

VII. To evaluate the proposed system using scenario-based testing, functional testing, and usability feedback.

VIII. To identify limitations of the proposed solution and recommend future improvements for wider deployment and enhanced AI integration.

## Functional requirements

| ID | Original wording |
|---|---|
| FR1 | Allow users to create learner profiles |
| FR2 | Collect educational qualifications and interests |
| FR3 | Generate personalised pathway recommendations |
| FR4 | Provide alternative progression routes |
| FR5 | Identify skill or qualification gaps |
| FR6 | Explain recommendation outputs |
| FR7 | Display official educational resource links |
| FR8 | Provide chatbot-assisted support |
| FR9 | Support basic voice-assisted input |

## Non-functional requirements

| ID | Original wording |
|---|---|
| NFR1 | User-friendly interface |
| NFR2 | Mobile-friendly usability |
| NFR3 | Acceptable response time |
| NFR4 | Reliable educational datasets |
| NFR5 | Modular system architecture |
| NFR6 | Future scalability support |
| NFR7 | Explainable recommendation outputs |

## Intended deliverables

| ID | Original wording |
|---|---|
| D1 | Project proposal |
| D2 | Literature review |
| D3 | Requirements specification |
| D4 | Structured pathway knowledge base |
| D5 | Web-based prototype |
| D6 | Recommendation engine |
| D7 | Chatbot support module |
| D8 | Evaluation and testing report |
| D9 | Final project report |
| D10 | Poster and viva presentation |

## Main research question

How can an AI-powered, policy-aware Education and Career Pathway Intelligence System support Sri Lankan learners through personalised, explainable, and accessible pathway recommendations?

## Supporting research questions

I. How can learner profiles, eligibility requirements and pathway knowledge be integrated to generate suitable recommendations?

II. How can explainable recommendation mechanisms improve user understanding and trust?

III. How can alternative pathway generation and skill-gap identification support educational and career planning?

IV. How can multilingual support, mobile usability and voice-assisted input improve accessibility?

V. How effective is the prototype in providing relevant and usable pathway guidance?

## Scope, methodology and evaluation

The system will primarily target A/L students, vocational learners, and early-career users seeking educational or career progression guidance. The prototype will initially focus on selected domains including Information Technology, Business and Management, and Engineering.

The recommendation process will utilise structured pathway knowledge, rule-based eligibility filtering, and lightweight AI-assisted recommendation techniques. The system will operate using curated educational and career-related datasets rather than real-time nationwide institutional integration.

The project will not include large-scale production deployment, full national educational coverage, advanced deep-learning-based predictive modelling, or unrestricted conversational AI functionality. These areas are identified as potential future enhancements beyond the scope of Version 1.

This project adopts Design Science Research (DSR) as the main research methodology because the study involves designing, developing and evaluating a software artefact that addresses a real educational guidance problem. DSR is suitable for Information Systems projects where knowledge is generated through the construction and evaluation of an artefact (Hevner, March, Park, & Ram, 2004).

The project will also use an Agile-inspired iterative prototyping approach for development. DSR provides the research structure, while iterative prototyping supports incremental construction of the knowledge base, recommendation engine, explanation layer, chatbot support and accessibility features.

The prototype will be evaluated using a mixed evaluation approach. Functional testing will check whether the system features work correctly, while scenario-based testing will assess whether recommendations are suitable for different learner profiles. Usability feedback will be collected from adult users where appropriate, using simple rating-scale and open-ended questions.

The [full extracted baseline](alignment/APPROVED_BASELINE.md) also preserves the scope/evaluation tables. [Original/refined traceability](alignment/REQUIREMENTS_TRACEABILITY.md) distinguishes P-FR1–9/P-NFR1–7 from I-FR01–10/I-NFR01–08. Proposed diagrams contain additional undelivered role/account features; see the explicit discrepancy register rather than silently expanding or reducing the approved scope. Signed ethics conditions and the actual assessment brief are separate outstanding evidence.


---

# Appendix B. Programme and educational evidence inventory

This is the frozen stored catalogue at WP5, not a new source verification exercise. Last-verified dates below are stored record dates; WP5 refreshed selected rules without rewriting every programme metadata date.

| ID | Programme | Domain | Official source URL | Stored date |
|---|---|---|---|---|
| PRG0001 | Bachelor of Science Honours in Information Technology | Information Technology | https://www.uom.lk/itfac/education/undergraduate/it | 2026-08-08 |
| PRG0002 | Bachelor of Science in Computer Science | Information Technology | https://cmb.ac.lk/undergraduate-programmes | 2026-08-11 |
| PRG0003 | Bachelor of Science Honours in Artificial Intelligence | Information Technology | https://uom.lk/itfac/bachelor-science-honours-artificial-intelligence | 2026-08-11 |
| PRG0004 | IIT International Foundation - Computing (IT) Pathway | Information Technology | https://www.iit.ac.lk/foundation/it/ | 2026-08-18 |
| PRG0005 | BEng (Hons) Software Engineering | Information Technology | https://www.iit.ac.lk/course/beng-software-engineering/ | 2026-08-19 |
| PRG0006 | BSc (Hons) Computer Science | Information Technology | https://www.iit.ac.lk/course/bsc-computer-science/ | 2026-08-19 |
| PRG0007 | BSc (Hons) Artificial Intelligence and Data Science | Information Technology | https://www.iit.ac.lk/course/bsc-artificial-intelligence-and-data-science/ | 2026-08-19 |
| PRG0008 | Bachelor of Management Studies Honours | Business and Management | https://ou.ac.lk/programme/bachelor-of-management-studies-honours-2/ | 2026-10-29 |
| PRG0009 | Bachelor of the Science of Engineering Honours | Engineering | https://eng.pdn.ac.lk/academic/undergraduate-programme/ | 2026-10-29 |
| PRG0010 | Higher National Diploma in Mechatronics Technology | Engineering | https://ucj.ac.lk/hndmnt/ | 2026-10-29 |
| PRG0011 | Bachelor of Engineering Technology in Mechatronics Technology | Engineering | https://uovt.ac.lk/en/academics/courses/btech-mechatronics-technology | 2026-10-29 |

The [WP5 educational review](../evidence/wp5/EDUCATIONAL_SOURCE_REVIEW.md) records actual selected-source checks, limitations and UGC page references. [Rule evidence](../evidence/wp5/rule-evidence.csv) links each requirement to its source. [Dataset hashes](../evidence/wp5/dataset-sha256.json) identify all CSV files. None of the five recorded progression edges guarantees admission. Missing awarding-body/framework/recognition information must remain unresolved.


---

# Appendix C. Architecture and data flow

![WiseLanka architecture](figures/architecture.svg)

Editable sources: figures/architecture.svg and architecture.mmd. The diagram separates authoritative assessments from within-group relevance and shows the supporting engines. “Read-only guide” means a deterministic intent interface reusing engines, not a generative LLM. The optional browser speech service has separate processing/privacy behaviour from local inference.

The sequence in figures/request-flow.mmd describes the personalised request path, including model unavailable and no-preference states. The qualification-only branch returns academic_insights rather than fabricated examination recommendations. Diagrams describe actual module boundaries, not separate network microservices. All backend engines execute within the modular FastAPI application.


---

# Appendix D. Historical WP5 ranking comparison

These are top-three IDs from the saved nine-scenario WP5 method outputs, not relevance judgements. They predate the later 21-scenario Sprint 2B comparison reported in Chapter 9 and must not be pooled with it. Group sizes and academic status must accompany interpretation; full orders/scores remain in comparison.json. All profiles are synthetic. Cold-start ties can be identical across methods.

| Case | Grouped deterministic top 3 | TF–IDF top 3 | Semantic top 3 |
|---|---|---|---|
| empty | PRG0001, PRG0002, PRG0003 | PRG0001, PRG0002, PRG0003 | PRG0001, PRG0002, PRG0003 |
| it_literal | PRG0001, PRG0002, PRG0003 | PRG0002, PRG0009, PRG0008 | PRG0002, PRG0003, PRG0001 |
| it_paraphrase | PRG0001, PRG0002, PRG0003 | PRG0002, PRG0008, PRG0001 | PRG0002, PRG0003, PRG0001 |
| business | PRG0008, PRG0001, PRG0009 | PRG0008, PRG0001, PRG0009 | PRG0008, PRG0001, PRG0009 |
| engineering | PRG0001, PRG0002, PRG0003 | PRG0009, PRG0008, PRG0001 | PRG0009, PRG0003, PRG0008 |
| unmet_engineering | PRG0008, PRG0001, PRG0002 | PRG0008, PRG0009, PRG0001 | PRG0008, PRG0009, PRG0003 |
| missing_evidence | PRG0008, PRG0009, PRG0001 | PRG0009, PRG0008, PRG0001 | PRG0009, PRG0008, PRG0003 |
| unfamiliar | PRG0001, PRG0002, PRG0003 | PRG0001, PRG0002, PRG0003 | PRG0003, PRG0001, PRG0009 |
| vocational | PRG0001, PRG0002, PRG0003 | PRG0007, PRG0008, PRG0001 | PRG0010, PRG0004, PRG0011 |

Independent labels: unavailable. nDCG@3: not computed. These orders cannot establish educational accuracy, quality uplift or satisfaction. The full [comparison](../evidence/wp5/comparison.json) records the catalogue hash and per-candidate statuses; [protocol](../evidence/wp5/AI_EVALUATION_PROTOCOL.md) describes blinded evaluation and leakage controls.


---

# Appendix E. Evidence index and terms

All paths below are relative to the repository root; preserve these artifacts or an equivalent immutable evidence archive with the submitted project.

| Claim | Evidence | Scope |
|---|---|---|
| Stage 9A backend verification | `docs/evidence/stage9/STAGE9_TECHNICAL_VERIFICATION.txt` | 269 passed, zero failed/skipped; AI-enabled Python environment; dirty worktree identity recorded |
| CSV structural integrity | Same Stage 9A log; `docs/evidence/wp5/csv-integrity.log` | Validator output for 20 CSV datasets; not source truth/currentness |
| Educational correctness | `docs/evidence/research-sprint2/educational-correctness/`; `docs/evidence/research-sprint2/completeness-correction/` | Original 42/45 baseline and separate 43/45 replay; synthetic evaluator-authored scenarios |
| AI ranking comparison | `docs/evidence/research-sprint2/ai-ranking/` | 21 scenarios; deterministic, TF–IDF, MiniLM; no independent labels or quality metric |
| Model/runtime provenance | AI-ranking `BASELINE.json`, `PERFORMANCE_RESULTS.csv`, `RANKING_ANALYSIS.md`; `docs/evidence/wp5/runtime-network.json` | Pinned ONNX model and measured local behavior; machine-specific |
| Browser/live/accessibility snapshot | `docs/evidence/wp5/` | Earlier WP5 browser/live/automated scan results; selected states, not certification |
| Requirements and objective traceability | `docs/final-submission/alignment/REQUIREMENTS_TRACEABILITY.md`; `docs/final-submission/RESEARCH_QUESTION_TRACEABILITY.md` | Implementation versus validation status and research gaps |

Measured = executed observation with saved output. Synthetic = fictional profile used in software evaluation. Mocked = simulated browser/API behavior. Pending = no result exists. `MET` means only the represented requirements are satisfied by supplied evidence; it is not confirmed admission. Semantic relevance is a content similarity signal, not probability or ongoing learning. There are zero genuine participant responses and zero independent relevance judgements.



# Appendix G. Project Progress Form 1 — TO INSERT

[Insert the authentic, completed university project progress form if required. Do not recreate signatures, dates or meeting records. Confirm whether the official form is available and required.]

# Appendix H. Project Progress Form 2 — TO INSERT

[Insert the authentic, completed university project progress form if required. Do not recreate signatures, dates or meeting records. Confirm whether the official form is available and required.]

# Appendix I. Stage 9A technical verification record

The full Stage 9A evidence log and interpretation index are preserved at `docs/evidence/stage9/STAGE9_TECHNICAL_VERIFICATION.txt`, `STAGE9_TECHNICAL_EVIDENCE_INDEX.md` and `STAGE9_RESULTS_LIMITATIONS.md`. These files retain the actual command/output, worktree qualification, environment versions, CSV validator output, scenario evidence references and ranking benchmark sources. They document no participant data.
