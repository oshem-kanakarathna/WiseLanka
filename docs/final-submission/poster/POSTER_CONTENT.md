# WiseLanka — policy-aware education and career guidance

**Working research poster; author, module, dimensions and university branding require official confirmation.** No official template/logo is invented. Proposed layout is three columns with one architecture figure; print-ready dimensions remain subject to the poster brief.

## Problem and aim

Learners need to distinguish educational requirements, missing evidence and programme relevance. WiseLanka's approved aim is to design, develop and evaluate personalised, explainable and accessible AI-powered, policy-aware guidance for Sri Lankan learners.

## Approved research question

How can an AI-powered, policy-aware Education and Career Pathway Intelligence System support Sri Lankan learners through personalised, explainable, and accessible pathway recommendations?

Supporting questions investigate: profile/rule/knowledge integration; understanding and trust; alternatives and skill gaps; accessibility; relevance and usability. These are the same five questions reproduced verbatim in appendix A, not findings.

## Artifact and method

A curated CSV knowledge base connects programmes, qualifications, rules, careers and conditional progression. FastAPI domain engines power a responsive web interface. DSR guides iterative construction, demonstration and evaluation. Objectives cover literature/context, knowledge, hybrid recommendations, web/accessibility features, evaluation and limitations.

## Hybrid design

1. Authoritative rules produce MET / NOT_MET / NOT_ASSESSED.
2. Frozen local MiniLM ONNX ranks only within these academic groups.
3. TF–IDF and deterministic orders provide reproducible comparisons.
4. Explanations show catalogue facts, uncertainty and official links.

Similarity is not admission probability. No learner-feedback training occurs. The guided assistant reuses the engines and refuses unsupported questions. Draft English/Sinhala/Tamil controls and optional browser speech retain text fallback.

## Actual evidence — WP5 checkpoint 07f4b97

- 11 programmes: IT7, Business1, Engineering3; five progression edges; 21 sources.
- 205 backend and36 browser tests passed; five live workflows passed.
- 14 synthetic reference cases passed; CSV/fresh installation checks passed.
- Three rankers compared on nine synthetic cases; no independent labels or nDCG.
- Zero automated accessibility violations in nine tested states; manual checks pending.
- Model load0.29s; warm in-process p95~15ms; whole-process peak RSS302MiB on the measured Mac.

Source review found omitted UGC conditions and prompted conservative NOT_ASSESSED outcomes. This is evidence of an evaluated correction, not comprehensive admissions validation.

## Limits and next evaluation

Small uneven catalogue; reported awards/skills unverified; English semantic inputs; draft translations; native voice/manual accessibility pending. No user-satisfaction or learner-outcome results. Approved adult usability, independent source/relevance judgements and fluent review are next. No educational or ranking-quality improvement is claimed.

## Selected references and evidence

Hevner et al. (2004), MISQ28(1); Reimers and Gurevych (2019), DOI10.18653/v1/D19-1410; UGC Admissions Handbook2025/2026. Complete references and reproducible logs accompany the dissertation draft. These sources support design/context; they do not endorse the artifact.
