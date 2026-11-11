# WiseLanka final academic review pack

**First complete working draft — not finalised or submitted.** University of West London. Technical evidence date: 29 October 2026. Research Sprint 1 on 30 October located and inspected the module guide, Research Methods lecture and report template. The guide specifies 10,000 words and the 17 December 2026, 5pm report deadline; any centre extension remains unverified. Ethics clearance and centre/module applicability still require confirmation.

Start with the current [Research Sprint 1 plan](research-sprint1/SPRINT1.md), [official-criteria matrix](research-sprint1/RUBRIC_MATRIX.csv) and [chapter mapping](research-sprint1/CHAPTER_MAPPING.csv). An editable copy populated from the actual template is available locally under research-sprint1/local-only/ and excluded from Git. Older availability/rubric assumptions in the drafts are superseded by this review; substantive chapter revision remains for the next approved step.

Start with the [dissertation draft](DISSERTATION_DRAFT.md), then the [deliverable inventory](DELIVERABLE_INVENTORY.md) and [baseline/blockers](BASELINE_AND_BLOCKERS.md). The [quality review](QUALITY_REVIEW.md) maps every objective and FR to evidence and limitations.

- [Editable chapters](chapters/00-front-matter.md), [references](REFERENCES.md) and source-access register SOURCE_REGISTER.csv.
- [Ethics-review package](research-evaluation/README.md), with adult-only draft consent/tasks and empty data templates; no recruitment approval implied.
- [Poster content](poster/POSTER_CONTENT.md), [editable poster layout](poster/research-poster.html) and [rendered preview](poster/poster-preview.png). Size is provisional; no university logo/template assumed.
- [Viva outline](viva/PRESENTATION_OUTLINE.md), [live-demo script](viva/LIVE_DEMONSTRATION.md) and [examiner questions](viva/EXAMINER_QUESTIONS.md).
- [Architecture](figures/architecture.svg); editable Mermaid sources in figures/.

The draft openly distinguishes executed tests, synthetic cases, mocked speech and pending human review. AI assistance in drafting is disclosed; the author must verify module permission, sources and required declaration. Do not use this pack as an unaided-authorship declaration or fabricate missing results.

Rebuild the continuous Markdown and link/hash checks from the repository root:

```sh
python3 docs/final-submission/tools/build_draft.py
```

Edit chapter/appendix sources rather than the generated combined file. Historical WP5 execution logs and their13 zero exit codes are preserved in commit `07f4b97`. WP6 changes academic documents only; it does not claim a new application test run.

The draft poster PDF is available at poster/research-poster-draft.pdf. It uses a provisional 841×594mm landscape canvas pending the official brief. Its local rendering check found one PDF page, a loaded architecture figure and no JavaScript page errors. The editable renderer is tools/render_poster.py; it requires Playwright/Chromium and QA-only pypdf (5.9.0 in the checked temporary environment). These are layout tools, not added application dependencies.

CLAIM_REGISTER.csv links each numerical or pending claim to its actual evidence and limits.

## Academic alignment review

The exact main and five supporting research questions have now been confirmed against proposal §1.4 and interim §1.4. Begin with the [chapter quality audit](review/DISSERTATION_QUALITY_AUDIT.md), [objective/question traceability](RESEARCH_QUESTION_TRACEABILITY.md), [reference findings](review/REFERENCE_FINDINGS.md) and [missing-document checklist](review/MISSING_DOCUMENTS_CHECKLIST.md). The item-level reference register is review/REFERENCE_VERIFICATION_REGISTER.csv. Verdict: not submission-ready; approved adult evaluation and other identified validation remain pending.

## Supervisor discussion and final research preparation

Academic drafts are checkpointed locally as9ffb2f3. The [supervisor discussion pack](supervisor-review/SUPERVISOR_REVIEW.md), [personal handover](supervisor-review/PERSONAL_HANDOVER.md), [evaluation plan v0.2](research-evaluation/EVALUATION_PLAN_v2.md) and [manual checklist guide](supervisor-review/MANUAL_VALIDATION_README.md) provide the next research steps without another implementation audit. New study proposals remain subject to actual ethics/supervisor decisions; no participant data or independent relevance ratings have been collected.

## Original proposal and interim reconciliation — current review

Start with the [academic alignment report](alignment/ACADEMIC_ALIGNMENT_REPORT.md). The [exact baseline](alignment/APPROVED_BASELINE.md), [proposal-to-delivery matrix](alignment/PROPOSAL_TO_IMPLEMENTATION.md), [August-to-October comparison](alignment/INTERIM_TO_FINAL.md), [requirements crosswalk](alignment/REQUIREMENTS_TRACEABILITY.md) and [technology justification](alignment/TECHNOLOGY_JUSTIFICATION.md) supersede earlier assumptions that these originals were unavailable. [Significant discrepancies](alignment/CONTRADICTIONS_AND_LIMITS.md) require explicit acknowledgement, not silent scope changes. Private originals/raw extraction are excluded from this repository. This review made no application changes or Git commit.
