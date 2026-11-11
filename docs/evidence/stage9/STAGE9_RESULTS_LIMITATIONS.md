# Stage 9A — Results interpretation and limitations

## What was verified

- The current recorded test run in the AI-enabled Python environment completed with **269 backend tests passed, zero failed and zero skipped**. Its exact command, package inventory, timestamp, Git HEAD/worktree status, relevant file hashes and raw terminal output are preserved in `STAGE9_TECHNICAL_VERIFICATION.txt`.
- The current CSV integrity command exited 0 and reported all 20 dataset record counts. This is a structural validation result.
- `RESEARCH_COLLECTION_ENABLED` was unset and the implementation's fail-closed function returned `False`. There are **zero genuine participant responses**; synthetic fixtures and temporary demonstrations are not human research.
- The original educational correctness baseline remains **42 agreements and 3 disagreements across 45 scenarios**. The separately preserved correction replay reports **43 agreements and 2 remaining input limitations**. EC39 and EC40 are not supported by the request contract: age-at-registration and Common General Paper results across allowed attempts are absent, so the engine conservatively returns `NOT_ASSESSED`. Their source-grounded expected `NOT_MET` cases are retained; neither is evidence of guaranteed or erroneous eligibility.
- The frozen ranking comparison executed deterministic, TF–IDF and MiniLM methods on equivalent synthetic scenario candidates. Status-group ordering and candidate membership were preserved. MiniLM's actual execution is evidenced by `SEMANTIC` result rows, non-null scores, pinned model hashes and repeated runtime records. The unavailable-model fallback was also tested.

## What these results do not establish

1. **No universal educational correctness.** Passing tests demonstrate expected implementation behavior for tested inputs. CSV integrity and the selected source checks do not establish that every record is current, complete or accepted by an institution.
2. **No independent scenario oracle.** The educational correctness expected outcomes and scenario set were prepared by the implementer, who had inspected the system. The 45-case agreement totals are bounded evaluator comparisons, not an independent accuracy estimate.
3. **No ranking superiority.** The 21 scenarios comprise nine development-exposed cases and 12 catalogue-aware follow-ups; neither group is an independent held-out evaluation. There are no independent relevance labels. Therefore no nDCG, MAP, Precision@K, recommendation accuracy, user satisfaction or superiority result is available.
4. **No participant findings.** There have been zero genuine participant responses, no adult-user usability study and no independent reviewer ratings. Prepared instruments are not results and do not prove ethics authorisation.
5. **No broad performance guarantee.** The rank timings and memory observations come from one Apple M4 environment. They exclude parts of end-to-end service and deployment workload; they are not production capacity or a response-time guarantee.
6. **No accessibility certification.** Historical automated scans cover selected page states/rules only. Manual assistive-technology, fluent Sinhala/Tamil review, real-device mobile use and native microphone behavior remain pending.
7. **Snapshot and worktree qualification.** Stage 9A tests ran with HEAD `5475254…` plus the dirty worktree recorded in the raw log, not a clean commit alone. The historical scenario and ranking evidence uses its own dated commits/snapshots and should not be described as if all results came from one immutable application revision.

## Appropriate dissertation use

The evidence is sufficient to begin drafting technical Results and Critical Analysis sections **for software verification, structural data checks, bounded scenario behavior, ranking-method differences, fallback/policy-boundary behavior and machine-specific runtime**. The text must state the snapshot, method, synthetic nature and limitations beside each result. Educational effectiveness, ranking relevance, explanation comprehension, trust, usability and learner outcomes must remain unanswered until suitable evidence is actually and ethically collected.
