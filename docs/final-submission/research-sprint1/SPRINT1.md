# Research Sprint 1 — execution and report alignment

30 October 2026. Feature freeze retained. This note supersedes earlier document-availability assumptions; historical chapters, reviews and WP1–WP5 evidence remain intact. No participant recruitment, data collection or new application test execution occurred in this sprint.

## Institutional baseline actually inspected

| Document | Local location / inspected content | Finding |
|---|---|---|
| Confirmed original proposal | WORK/Final Project Proposal_ 34164665.docx; prior complete review, hash rechecked | Exact title, aim, eight objectives, six questions, FR1–9, NFR1–7 and D1–10 remain unchanged |
| August interim | WORK/Project Interim Report _Draft_Oshem.docx; prior complete review, hash rechecked | August FastAPI/JavaScript/CSV baseline and 40-test evidence remain historical |
| Module Study Guide | FP/MATERIALS/MSG CP60046E Project AY202526 - FEB-26 - JAN-27.pdf; all 10 pages read; Downloads copy has identical hash | Assessment 2: 10,000 words, 60% module weighting; report plus Semester 2 progress form; published 5pm 17 December 2026 (p5). Assessment 2 rubric pp6–7 totals100 |
| Research Methods lecture | Downloads/Lecture - Research Methods 2025_Nov.pptx; all43 slide texts and embedded notes read | Method follows question (slides4–10); descriptive versus inferential analysis (18–19); explained pseudocode/figures rather than code dumps (29–31); tests expose errors but cannot prove their absence (43). No empirical result borrowed from teaching examples |
| Project Report Template | Downloads/Project Report Template.docx; body, content-control TOC, styles, media relationships and footer inspected | Six main chapters; Harvard via UWL Cite Them Right; abstract written last. Cached TOC lists Appendix/Progress Forms1–2, but actual completed forms are not embedded |

No requested institutional document is missing. Absolute paths and hashes are in [DOCUMENT_REGISTER.json](DOCUMENT_REGISTER.json); these are locally supplied files, not a newly verified Blackboard download. Source teaching documents are not copied into the repository or uploaded.

**Applicability and deadline gate:** guide codes CP60046E/CP6CS46E differ from CP6SL460 on the project originals. Confirm centre/module mapping, current assessment instructions and deadline timezone. Retain **17 December 2026, 5pm as printed** as the contingency until written official centre extension is verified; no extension evidence was found. A flexible internal schedule does not change that deadline. The guide also establishes **one-page A3 poster using its separate template** and a10-minute oral assessment, while also describing5-minute demonstration/discussion limits (pp7–8). Existing841×594mm poster is not A3; its separate official template and timing clarification are still required. Do not resize/finalise it in this sprint.

## Official structure and current word mapping

The actual template has been used to create [an editable local working copy](local-only/WiseLanka_UWL_Template_Working_Draft.docx). It retains the original package's styles, page geometry, branding relationships and page-number footer, imports existing draft text, and adds clearly pending progress-form slots. All package parts except document body/settings are byte-identical to the source template. It is ignored by Git because it contains institutional template material. No existing Markdown chapter was overwritten.

| Required section | Existing source / working-copy treatment | Approximate words | Proposed body budget |
|---|---|---:|---:|
| Cover page | Original template cover populated from verified project baseline; submission date/second marker remain pending | — | — |
| Abstract | Existing technical summary imported with PROVISIONAL warning; revise last after genuine evaluation | Included in451 front-matter words | — |
| Acknowledgements | Student-only placeholder; assistance disclosure retained | — | — |
| Contents | Word TOC field prepared; update after final headings/pagination | — | — |
| List of Figures and Tables | Word caption-list fields; insert actual captioned figures/tables before updating | — | — |
| Introduction | Chapter01 |814 |800 |
| Literature Review | Chapter02 |1,343 |2,000 |
| Research Methodology | Chapter03 |920 |1,400 |
| Design and Implementation | Chapters04–07: requirements, architecture, knowledge, hybrid ranking |3,313 |3,100 |
| Result and Analysis | Chapter08: executed technical layers and pending research results |1,052 |1,500 |
| Discussion and Conclusion | Chapters09–10; PROVISIONAL interpretation, not final human findings |1,451 |1,200 |
| References | Existing bibliography,20 entries; Harvard conformity needs student checking | Counted separately | — |
| Appendices | ExistingA–F plus authentic Progress Forms1 and2 slots; no signatures/meetings invented | Counted separately | — |
| Six main chapters | Current text retained |**8,893** |**10,000** |

[CHAPTER_MAPPING.csv](CHAPTER_MAPPING.csv) records the same grouping. Counts use the existing Python regex `\b[\w’-]+\b`, including headings, table cells and source notation. The previous9,344 includes451 front-matter words; neither figure is an official Word-assessed count. Guide gives no exclusion list, tolerance or chapter quotas. The10,000 allocation is our provisional planning budget, subject to confirmation of how abstract/tables/captions/references/appendices count. Add substantive critique, reproducible procedures and actual analysis; prune repeated design prose rather than padding.

The DOCX passes ZIP/XML checks, not visual Word validation. Source chapter numbers/cross-references remain editorial references to the ten-chapter Markdown draft. Reconcile them after merging; do not submit with those references unchanged. Open in Word, update fields, insert captioned diagrams, and review page breaks, tables, links and all numbering. The original template's sample Alani references/instructional prose are not presented as student research. Acknowledgements, authenticity declarations and actual progress forms require the student/supervisor.

## Rubric coverage — actual Assessment 2 criteria

The [18-row rubric matrix](RUBRIC_MATRIX.csv) reproduces the guide's allocations at subcriterion level and records current content, evidence, weakness, required improvement, priority and verification. It totals100; these weights are **not predicted marks**. P0 denotes an evidence/approval gate; P1 denotes essential scholarly or presentation improvement.

| Criterion | Weight | Current support | Critical gap / immediate improvement |
|---|---:|---|---|
| Research Method |15 | DSR/iteration justification and layered evaluation | Prospective frozen execution protocol; independent checks; reflexive critique of retrospective mapping |
| Literature Review |20 | Relevant narrative and20-source access register | Several abstract-only sources; student full-text comparative appraisal and stronger current local context |
| Use of Evidence |25 | Models, milestone crosswalk, extensive saved software tests/source review | Authentic S1/S2 progress records; independent rule adjudication; human research still pending. Rubric explicitly accepts differentiated evidence or appropriate software quality evidence; do not invent a mandatory sample size |
| Presentation |10 | Editable sources, figures and real template | Final Word structure/captions/cross-references, assessed word-count rules and human proofreading |
| Analysis of Results |15 | Clear distinctions between functionality, source fidelity and relevance | Real independent judgements and approved human observations; declared exclusions, units and alternative explanations |
| Conclusions |10 | Bounded technical conclusions and explicit limitations | Final answer to each question must follow collected findings; no inferred educational effectiveness |
| References |5 |20 cited entries with item-level access/verification limits | Harvard/Cite Them Right harmonisation and student verification of actual interpretations/full texts |

## Evaluation execution plan

Use existing v0.2 instruments and the blinded ranking protocol; do not create a third competing study. Proposed participant target8 (range6–10) and two independent judges remain unapproved design choices, not a module requirement or achieved sample. The lecture supports choosing methods for the research question; it does not mandate inferential tests, NVivo or a new experiment merely because they appear in slides.

| Stream / questions | Smallest execution / measures | Ready now versus gate | Interpretation |
|---|---|---|---|
| Educational correctness; SRQ-I/III | Freeze current catalogue and33 rule rows/5 progression edges. Check official condition text, programme/intake, category, source location/date and expected MET/NOT_MET/NOT_ASSESSED for14 reference cases; record unsupported/contradictory/outdated rules. Include foundation40% four-module boundary, missing UGC conditions, failed/missing subjects and conditional vocational routes | Researcher public-source checks ready. Independent human adjudication only after applicable ethics determination | Separate rule execution from underlying source truth;14 implementer cases are not independent accuracy estimates |
| Deterministic/TF–IDF/MiniLM; SRQ-I/V | Preserve existing9 cases and orders, shared candidate pools/academic groups, pinned model and catalogue hash. Check stable ties, synonyms, empty/unknown text, missing descriptions, unavailable model and unchanged academic status | Functional/synthetic rerun ready in an isolated evidence destination; no tuning | Reports behaviour/runtime, not superiority or participant preferences. Keep raw legacy order distinct from grouped deterministic baseline |
| Independent recommendation relevance; SRQ-V | Existing method-blinded packs cover51 case/candidate pairs per judge; propose two independent adults. Lock0–3/UNJUDGEABLE ratings before revealing methods. Use fixed-group nDCG@3 only for fully judged groups with≥3 candidates and positive ideal gain; disclose@2/singleton/excluded cases and disagreements | Packs ready; recruitment/ratings require applicable ethics confirmation | Existing cases remain development-exposed, not held-out. No labels means no nDCG. Independent labels do not prove educational outcomes or satisfaction |
| Explanation, trust and pathways; SRQ-II/III/V | Existing task probes/E1–E5 and proposed custom transparency/bounded-reliance items. Observe unassisted completion, comprehension0–2, help/errors/time and interpretation of conditional routes/unreported skills. Optional source-lookup comparison uses existing counterbalanced four-sequence plan only if approved | Instruments ready; actual collection blocked on confirmed conditions/amendments | Report item distributions, n/N, medians/ranges, paired differences and missingness. Small descriptive comparison cannot by itself prove causal improvement or validate a trust scale |
| Accessibility/languages/voice; SRQ-IV | Researcher keyboard/focus/zoom/reflow and owned-device checks with fictional text; preserve text fallback. Then fluent si/ta terminology review, actual screen-reader/real-mobile tasks and consented native voice capability/denial/language checks | Non-participant self-checks ready; reviewer/participant data require ethics determination. Native speech needs explicit provider-processing and consent review | Distinguish automated/mocked checks from native audio and fluent review. No universal speech support, translation certification or WCAG conformance inferred |
| Performance/robustness; SRQ-V | On one declared device/env, propose5 fresh-process load runs plus40 warm requests per method; record model load/first/warm latency, median/p95 and process RSS, failures and request count. Exercise missing-model fallback in a separate process/directory, never delete weights. Preserve response groups under failure | Synthetic local measurements ready; not executed this sprint | No proposed pass SLA is an original requirement. Warm sequential local timings do not establish production scale, device generality or relevance |

**Evidence isolation before reruns:** `scripts/verify_wp5.py` writes into saved WP5; do not run it over the accepted snapshot. Use a separate temporary checkout/run directory or override each runner's output destination in a research-only wrapper. Record code/data/model/dependency hashes, command, exit code and environment for each new run. Existing `evaluate_wp3.py` exposes `OUTPUT`; comparison output can be redirected without changing application code. Freeze new held-out scenarios before any tuning if a genuinely held-out study is later feasible. Native participant data and completed ratings belong in approved restricted storage, never Git or AI prompts.

Current evidence inspection: WP1 has132 backend/22 browser, WP2 160/23, WP3 177/25, WP4 200/36 and WP5 205/36 in saved final logs; their verification manifests contain4/6/8/8/13 zero-exit checks respectively. WP5 additionally records5 live workflows,14 synthetic reference cases, CSV/fresh-install verification and zero detected axe violations in9 states. These are different snapshots and test categories, not summed learners or comparative accuracy. No new results, performance improvements or feedback were generated here.

## Ethics release and student responsibility

Additional local files were found and text-inspected: the9-page May2026 ethics/risk form in WORK, Participant Information Sheet, blank Consent Form and four-task Evaluation Task Sheet under FP. Their existence no longer needs to be guessed. The ethics form contains a **typed supervisor endorsement dated10 May2026**; its office-use classification/conditions are not established by the available text. No signature authenticity or panel disposition was independently verified. Do not call this automatically approved or automatically unsigned.

Specific issues to resolve with the supervisor: ethics SectionB marks questionnaire omission NO, confidentiality N/A and debrief NO, while the outline promises voluntary/confidential/anonymised feedback and newer drafts permit skipping/debriefing. Observational consent is N/A while v0.2 adds observed/timed tasks. The local information sheet names withdrawal/anonymisation but lacks precise retention, access/withdrawal cutoff and complaint arrangements. The revised comparison, judge protocol, trust/reliance items, native vendor speech and reviewer work may need clarification/amendment. Only the authorised university/supervisor process can determine their applicability; no recruitment, pilot, ratings or collection is released by this review. Keep original versions intact.

The student must personally read and critically appraise the key full-text literature, verify source-to-claim entailment, understand the algorithms/limitations, write genuine acknowledgements/reflection and interpret actual findings. Guide p9 expressly treats unauthorised AI use as misconduct: **acknowledgement alone does not establish permission**. Obtain module-specific permitted-use/declaration guidance; review and take responsibility for assisted drafts before including them. Do not present prepared prose as wholly unaided work. Authentic progress forms and supervision history cannot be inferred from Git or reconstructed as signatures/meetings.

## Immediate actions and next three tasks

1. **Student/supervisor release decision:** confirm centre/module applicability, published deadline/timezone or written extension,10,000-word counting rules, signed ethics disposition and authorised instruments/amendments. Supply actual S1/S2 progress forms and supervisor feedback; obtain the separate A3 poster template and clarify oral timing. Do not wait for a possible extension before planning to17December.
2. **Student scholarly work plus independent-source preparation:** prioritise full texts for Lahoud, hybrid recommendation, sentence embeddings, explanation evaluation and DSR. Add comparative reading notes and perform public-source rule spot checks against the14 reference cases. Freeze the existing methods/candidate pools before any permitted judging; arrange independent reviewers only after release.
3. **Execute the frozen evaluation and revise once:** run isolated synthetic robustness/performance checks and researcher manual checks now; collect only approved adult/judge/fluent/native observations after release. Preserve negative findings, then fill actual Result and Analysis and revise Discussion/Conclusion/Abstract last. Finish Word fields/figures and formal count after substantive analysis.

No application feature/refactor, commit, push, external submission or participant collection was performed. Previous commits, teaching originals, dissertation sources, saved testing evidence and both JavaScript backups are preserved. This sprint stops for review.
