# WiseLanka final academic review pack

**First complete working draft — not finalised or submitted.** University of West London. Evidence date: 29 October 2026; November is the project completion target. The actual module brief/rubric and original academic documents remain unavailable.

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

The exact main and five supporting research questions have now been restored from the author's supplied text. Begin with the [chapter quality audit](review/DISSERTATION_QUALITY_AUDIT.md), [objective/question traceability](RESEARCH_QUESTION_TRACEABILITY.md), [reference findings](review/REFERENCE_FINDINGS.md) and [missing-document checklist](review/MISSING_DOCUMENTS_CHECKLIST.md). The item-level reference register is review/REFERENCE_VERIFICATION_REGISTER.csv. Verdict: not submission-ready; approved adult evaluation and other identified validation remain pending.
