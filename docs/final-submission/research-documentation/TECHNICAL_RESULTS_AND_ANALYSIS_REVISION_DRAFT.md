# Chapter 9 — Results and Critical Discussion

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
