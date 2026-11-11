# Final dissertation working manuscript — word budget and structural map

**Status:** Planning document for student review. It does not establish submission readiness or the university's formal word-count calculation.

## Counting method

Counts use one reproducible method throughout: Python whitespace-token counting (`len(text.split())`). Source chapter files were counted individually; integrated chapters were counted from each numbered heading through the line before the next numbered chapter or the References heading. Counts include headings, Markdown, tables, citations, URLs and placeholders. This is a planning count, not Microsoft Word's count. The applicable guide records a 10,000-word report requirement, but the treatment of front matter, tables, references and appendices must be confirmed for this module/centre.

## Existing versus integrated chapters

| Chapter/file | Existing source words | Integrated draft words | Change | Integration note |
|---|---:|---:|---:|---|
| 00 Front matter | 448 | 528 | +80 | Provisional abstract and front-matter placeholders revised; final abstract remains pending. |
| 1 Introduction | 779 | 780 | +1 | Existing chapter retained. |
| 2 Critical literature review and research gap | 1,350 | 2,548 | +1,198 | Replaced in this working manuscript by the consolidated evidence-mapped review. |
| 3 Research methodology and ethics | 929 | 2,633 | +1,704 | Replaced by the revised methodology draft; human-study procedure remains proposed and unauthorised/unconducted. |
| 4 Requirements analysis and system design | 860 | 861 | +1 | Existing chapter retained. |
| 5 Architecture and implementation | 832 | 833 | +1 | Existing chapter retained. |
| 6 Knowledge-base construction and educational validation | 757 | 758 | +1 | Existing chapter retained. |
| 7 Hybrid AI recommendation methodology | 742 | 743 | +1 | Existing chapter retained. |
| 8 Testing and evaluation | 1,027 | 561 | -466 | Updated to distinguish completed technical tests from pending research evaluation. |
| 9 Results and critical discussion | 975 | 1,315 | +340 | Replaced by the Stage 9 evidence-grounded technical results draft. |
| 10 Limitations, future work and conclusion | 477 | 478 | +1 | Existing chapter retained; requires consistency review after genuine evaluation decisions. |
| **Chapters 00–10** | **9,176** | **12,038** | **+2,862** | Includes front matter. |

## Manuscript totals

| Component | Words |
|---|---:|
| Chapters 1–10 main body | **11,510** |
| Front matter (Chapter 00) | 528 |
| Chapters 00–10 total | 12,038 |
| References | 1,031 |
| Appendices A–I (Appendix F is not present in the integrated draft) | 1,841 |
| **Full integrated Markdown manuscript** | **14,910** |
| Existing assembled `docs/final-submission/DISSERTATION_DRAFT.md` | 12,097 |

The current main body is **1,510 words above** a 10,000-word planning target. The full-file excess is 4,910 words only if all front matter, references and appendices were counted; do not treat that as the university calculation without confirming the exclusions. The new integrated draft adds substantial analysis in Chapters 2 and 3, while shortening Chapter 8 and retaining the new technical evidence in Chapter 9.

## Structure and assessment alignment

The locally inspected report template is organised into six main report sections: Introduction; Literature Review; Research Methodology; Design and Implementation; Result and Analysis; Discussion and Conclusion, followed by References and Appendices. The integrated manuscript retains its existing numbered Chapters 1–10 and maps them as follows: Chapter 1; Chapter 2; Chapter 3; Chapters 4–7; Chapter 8; and Chapters 9–10. Final Word styles, contents/list fields, figure/table numbering, page breaks and cross-references have not been prepared.

The inspected module-guide record specifies 10,000 words and reports the assessment categories Research Method (15), Literature Review (20), Use of Evidence (25), Presentation (10), Analysis of Results (15), Conclusions (10) and References (5). The transcribed criteria are in `docs/final-submission/research-sprint1/RUBRIC_MATRIX.csv`; confirm the official guide applies to module CP6SL460 because the supplied guide and project originals show different module codes (CP60046E/CP6CS46E versus CP6SL460). The exact criterion wording, local-centre mapping and word-count exclusions need confirmation before final editing.

## Recommended planning ceilings for a 10,000-word body

These are proposed ceilings, not institutional quotas. They prioritise evidence and analysis. Do not pad a shorter section where evaluation remains pending.

| Report section / chapters | Suggested ceiling | Current words | Difference to ceiling | Specific action |
|---|---:|---:|---:|---|
| Introduction (Ch. 1) | 800 | 780 | 20 below | Keep focused; remove duplicated scope text only. |
| Literature Review (Ch. 2) | 1,950 | 2,548 | 598 above | Trim repeated implementation descriptions and peripheral context; preserve synthesis, source-quality critique and Sri Lankan evidence limitations. |
| Research Methodology (Ch. 3) | 1,900 | 2,633 | 733 above | Move detailed result values to Chapters 8–9; compress repeated ethics/validity discussion while retaining actual-versus-planned status and DSR justification. |
| Design and Implementation (Chs. 4–7) | 3,000 | 3,195 | 195 above | Remove repeated component/architecture explanations across Chapters 4, 5 and 7; retain provenance and eligibility semantics. |
| Result and Analysis (Ch. 8) | 900 | 561 | 339 below | Do not pad. Add only essential reproducible procedures or verified analysis needed by the actual rubric. |
| Discussion and Conclusion (Chs. 9–10) | 1,450 | 1,793 | 343 above | Reduce duplicated limitations and feature summaries; preserve interpretation, counter-explanations and unanswered questions. |
| **Total** | **10,000** | **11,510** | **1,510 above** | Target reductions only in over-ceiling sections would reduce the body by 1,869 words, leaving 359 words of headroom; reallocate after confirming official counting rules. |

## Priority word-count and integration actions

1. Confirm the exact centre/module assessment instructions and what counts toward 10,000; use the final Word document's count only after the template and exclusions are confirmed.
2. Make a focused reduction pass against the table above. Avoid deleting caveats, source provenance or distinctions between technical correctness, relevance and usability.
3. Preserve the Stage 9A qualification that the 269-test run used a dirty worktree at recorded HEAD `5475254…`; a clean-state rerun is needed before attributing the result to one immutable commit.
4. Keep independent relevance judgements, participant usability, comprehension and qualitative results marked **NOT COLLECTED** until eligible, authorised research actually occurs.
5. Complete final cross-references, figure/table lists, authentic required progress forms, bibliography formatting and final word count after student review and Word conversion.
