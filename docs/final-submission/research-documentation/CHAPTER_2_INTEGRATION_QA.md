# Chapter 2 integration QA

**Status:** Review of an AI-assisted working draft only. This document does not approve the chapter for integration or submission. The student must inspect sources, validate claims and references, authorise/rewrite the prose, and confirm the university’s actual report instructions.

## 1. Word counts and report proportion

| Version | Words | Count basis |
|---|---:|---|
| Original `chapters/02-literature-review.md` | 1,343 | Text beginning at the Chapter 2 heading through §2.8, including headings and the original synthesis table; excludes any front-matter outside the chapter. |
| Integrated working draft | 2,502 | Text beginning at the Chapter 2 heading through §2.8, including headings and the synthesis paragraphs; excludes the AI-assisted working-status note immediately after the chapter heading. |
| Change | +1,159 (+86.3%) | Same regular-expression word-token method applied to both chapter bodies. |

At the approximately 10,000-word report target, the revised chapter represents **25.0%**. This is a sizeable allocation for a chapter assessed under a 20-mark Literature Review category, although marks are not a direct word-budget formula. The calculation includes headings and table words; UWL’s rules for counting tables, captions, references and appendices have not been checked against the official template/guide. The student should confirm the applicable count convention and rebalance if needed rather than cut critical distinctions arbitrarily.

### Section-level change

| Section | Original | Integrated | Change / focus |
|---|---:|---:|---|
| 2.1 Review approach and evidential limits | 101 | 237 | Adds theme and research-question mapping, review limits and source-access distinctions without inventing database searches or screening counts. |
| 2.2 Educational recommendation and learner agency | 244 | 394 | Integrates learning-resource versus major/career guidance evidence, source-access limits and Lahoud dataset-subset distinctions. |
| 2.3 Explicit constraints and hybrid recommendation | 164 | 266 | Adds constraint-based literature and separates formal assessment from ranking; design states are labelled as project choices. |
| 2.4 Lexical and semantic content matching | 205 | 244 | Distinguishes TF–IDF, SBERT and MiniLM contributions and limits transfer from NLP benchmarks. |
| 2.5 Explanations, understanding and persuasion | 133 | 227 | Separates explanation aims, correctness, comprehension and perceived trust/usefulness. |
| 2.6 Local guidance context and accessibility | 214 | 428 | Separates historical local evidence, cycle-specific policy, provider claims, digital access, translation and accessibility validation. |
| 2.7 Evaluation and the bounded research gap | 123 | 348 | Separates source accuracy, rule execution, relevance and human measures; defines limits on P@K/nDCG interpretation. |
| 2.8 Synthesis of alternatives | 152 | 352 | Replaces the brief alternatives table with comparative synthesis, bounded gap and links to the objectives. |

Counts use a uniform `\b[\w’\-]+\b` token pattern and may differ from Word’s count. They are reproducible comparisons, not a university-certified word count.

## 2. Integration and consistency checks

- Preserved the original chapter title and numbered headings §§2.1–2.8, including their existing titles.
- Consolidated the working revisions for §§2.2–2.7; §2.1 now states review scope and limits, and §2.8 synthesises evidence rather than merely listing alternatives.
- Kept approved project aims/objectives unchanged. The synthesis identifies Objective I as a focused, non-exhaustive review and Objective II’s current learner-needs evidence as insufficiently established.
- Standardised the distinction among policy/source correctness, rule execution, recommendation relevance, explanation comprehension, perceived trust/usefulness, accessibility and educational outcomes.
- Preserved `MET`, `NOT_MET` and `NOT_ASSESSED` as WiseLanka implementation semantics; they are not attributed to the cited studies.
- No similarity score is described as admission probability, recommendation accuracy, or career-success probability. Model benchmark findings are not transferred to WiseLanka.
- No independent relevance labels, nDCG results, participant findings, user satisfaction, accessibility conformance or educational effectiveness are reported.
- Historical UNICEF evidence is expressly not presented as current. The UGC handbook is tied to its 2025/2026 edition; the inaccessible full TVEC document supports no detailed claim. Provider marketing is distinguished from independent evaluation.
- Repetition was reduced by replacing the old synthesis table with four focused paragraphs. Some deliberate repetition remains where a distinction is needed to connect methods, risks and the research gap.

## 3. Citation-to-bibliography audit

The integrated chapter cites the following works; each has a corresponding entry in `docs/final-submission/REFERENCES.md`:

| In-text source | Central entry | Access/evidence qualification retained |
|---|---|---|
| Burke (2002) | Present | Full article reprint examined in Stage 2A; publisher metadata checked. Restaurant domain does not establish educational recommender performance. |
| CareerMe (n.d.) | Present | Homepage/provider feature claims only; no independent effectiveness evidence. |
| Da Silva et al. (2023) | Present | Abstract/metadata only; no detailed study-by-study claims. |
| Deschênes (2020) | Present | Targeted full-text examination; review covers learning contexts and excludes learning-path recommendation. |
| Felfernig et al. (2015) | Present | Targeted chapter examination; page range conflict remains for student/library confirmation. |
| Järvelin and Kekäläinen (2002) | Present | Original text available through recorded university-hosted copy; publisher direct access was blocked. Verify exact metric formulation and project variant. |
| Knijnenburg et al. (2012) | Present | Full article examined in Stage 1; Stage 3 reconciliation rechecked publisher metadata/abstract. General recommender setting, not an educational validation. |
| Lahoud et al. (2023) | Present | Targeted full-text examination; reported counts belong to distinct subsets/experiments, not one pooled sample. |
| National Education Commission (2016) | Present | Official historical report; not current prevalence or demand evidence. |
| Reimers and Gurevych (2019) | Present | Full ACL paper examined; NLP tasks do not validate programme relevance. |
| Salton and Buckley (1988) | Present | Full university-hosted copy examined; not the exact WiseLanka weighting scheme. |
| Tertiary and Vocational Education Commission (2025) | Present | Official indexed title/background only; full document retrieval timed out; no detailed content claim. |
| Tintarev and Masthoff (2012) | Present | Abstract/metadata only; claims remain conceptual and domain-limited. |
| UNICEF Sri Lanka (2018) | Present | Official full report examined; child digital-landscape context, not current adult or education-guidance evidence. |
| University Grants Commission Sri Lanka (2025/2026) | Present | Saved official handbook and selected pages examined; intake-specific. Verify any exact policy detail against the relevant intake. |
| Wang et al. (2020) | Present | Full NeurIPS paper examined; compression research, not education recommendation evaluation. |
| W3C (2024) | Present | Official WCAG 2.2 Recommendation checked; normative standard, not prototype conformance evidence. |

No missing bibliography entry was found for an in-text academic citation in this chapter. The check establishes entry presence and traceability, not that a source fully supports every sentence or that Harvard formatting satisfies UWL requirements. The central bibliography also contains uncited works used elsewhere in the dissertation; this chapter audit does not remove them.

## 4. Outstanding source limitations and personal verification

1. **Full-text coverage:** Da Silva et al. and Tintarev and Masthoff remain abstract/metadata-level sources. Their claims are deliberately narrow. The student should obtain and read full texts before making method- or result-specific assertions.
2. **Felfernig pagination:** Springer metadata records pp. 161–190, while the Stage 2A reconciliation records an author-affiliated record showing pp. 161–191. The central bibliography follows the publisher page range; confirm the final format with the original chapter/publisher or library record.
3. **Lahoud et al.:** Full text was examined, but the student must personally inspect tables and explain dataset subsets without aggregating them. Do not reuse headline similarity/personalisation results as directly comparable accuracy.
4. **Local current evidence:** NEC and UNICEF are historical and population-specific. The UGC source is an edition-specific admissions document. Current target-user needs and a comprehensive current TVET/progression picture are not established.
5. **TVEC and provider sources:** CareerOne full text remains inaccessible; CareerMe is a provider homepage. Neither supports an effectiveness comparison. Provider rules need current source, route and condition verification before any concrete claim.
6. **Accessibility and languages:** The local visual-impairment study’s disputed numerical results are excluded. Automated scans are limited; manual keyboard, screen-reader, zoom, mobile, microphone and fluent Sinhala/Tamil review remain pending. Translated UI text alone does not show comprehension.
7. **Evaluation evidence:** No independent relevance ratings or human-user results exist. The planned instruments are not ethics approval. The student must inspect the actual approval and conditions before recruitment or data collection.
8. **Focused search:** The chapter accurately discloses that it is not systematic. The student should search UWL library databases and document a defensible, proportionate search and screening rationale if required by the supervisor or rubric.
9. **Student authorship:** The student must read the cited works, verify claim entailment and write the final critical synthesis in their own informed voice under UWL’s AI-use and academic-integrity rules.

## 5. Critical quality review against available rubric records

The local `docs/final-submission/research-sprint1/RUBRIC_MATRIX.csv` records Literature Review criteria as four five-mark subcriteria (20 total), and Use of Evidence as three criteria totalling 25 marks. The criteria below are the wording recorded in that matrix. The original official module guide/marking document was not independently inspected for this review, so exact wording and any rubric updates remain **unverified**; confirm them before treating this as an official rubric audit.

### Literature Review — 20 marks in the local matrix

| Recorded criterion | Current draft evidence | Critical judgement and remaining work |
|---|---|---|
| “A complete report of the background study which shows very good understanding of the topic” (5) | The chapter compares recommender tasks, constraints, content-matching approaches, explanations, Sri Lankan context and evaluation. | Broader and more coherent than the original. It is still a focused, selective review; current local needs, vocational evidence and several source areas remain thin. Do not call it complete until the student confirms scope against supervisor expectations and performs proportionate library searching. |
| “The report has clearly distinguished between facts, speculations, and opinions” (5) | Published findings, provider claims, project design choices, analytical implications and pending outcomes are explicitly distinguished. | Stronger boundary-setting. The student must verify every attributed finding and preserve those labels during final editing; some implications are the author’s reasoning rather than source results. |
| “Quality and quantity of selected references to support argument” (5) | The draft uses peer-reviewed studies, original proceedings, official policy/report sources and a web standard, with access limitations documented. | Relevance and provenance are prioritised over count. Abstract-only sources, pagination uncertainty and gaps in current local scholarship limit confidence. Verify citations, UWL format and claim-to-source support manually. |
| “There is evidence that the researcher has read, analysed, and reflected on the knowledge relevant to the topic” (5) | Comparative treatment identifies domain/data/metric differences, transfer limits and design trade-offs. | The draft shows a stronger analytical structure, but AI-generated prose is not evidence that the student has read or reflected. Student reading notes, own critique and accurate source explanations are essential. |

### Use of Evidence — 25 marks in the local matrix

| Recorded criterion | Relationship to Chapter 2 | Critical judgement and remaining work |
|---|---|---|
| “Design models demonstrated in the report” (5) | Chapter 2 justifies constraints, grouped relevance and evaluation distinctions conceptually. | The chapter itself does not demonstrate the implemented models. Later design/implementation chapters must show actual architecture, diagrams and traceable mapping from literature to code. |
| “Clarity of evidence of progress towards project aims and objectives” (5) | §2.8 links the review’s design and evaluation implications to Objectives I–VIII without asserting completion. | Objective-level progress must be demonstrated across the whole report and evidence appendices, not inferred from the literature review. Objective II current learner-needs evidence and human parts of Objectives VI–VII remain limited/pending. |
| “EITHER distinguishes between different types of evidence collected OR provides appropriate evidence of software analysis/design/development/quality/testing” (15) | The chapter distinguishes published research, policy evidence, project design reasoning and pending evaluation. | Chapter 2 is not test evidence. Chapters on method/results must separate source checks, code tests, ranking observations, human evaluation and accessibility checks, and cite saved artifacts. No absent result should be implied. |

These are developmental judgements, not a grade prediction. The 20/25 weights and criterion text are taken from the saved matrix; their match to the currently applicable official rubric is not independently verified here.

## 6. Improvements required before integration

1. Student reads and annotates every cited primary source, particularly abstract-only sources, and personally rewrites the synthesis; retain distinctions among source finding, inference and project decision.
2. Verify the live official rubric, module guide, template, word-count rules and Harvard/Cite Them Right variant; adjust chapter length and citations accordingly.
3. Resolve the Felfernig page range and verify every bibliographic detail against the selected source record.
4. Recheck any policy/provider claim against the exact intake and route before repeating it in Chapters 4–8; do not broaden a selected catalogue into national coverage.
5. Confirm that the complete dissertation’s Results and Discussion chapters cite actual logs and label synthetic, measured, mocked and pending evidence correctly.
6. Do not state conclusions about ranking superiority, explanation comprehension, user trust, multilingual accessibility, voice usability or educational effectiveness until the corresponding valid evaluations exist.
7. Revisit the chapter’s 25.0% share of a 10,000-word target after official counting rules and remaining chapter needs are known; trim redundant detail rather than removing necessary methodological qualifications.

**QA conclusion:** The integrated draft is a coherent working chapter with clearer critical synthesis and claim boundaries than the original. It is not ready for direct integration until student source verification, independent authorship, reference/style confirmation, and rubric/template checks are complete.
