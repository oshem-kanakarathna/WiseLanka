# WiseLanka
## DESIGN AND DEVELOPMENT OF AN AI-POWERED, POLICY-AWARE EDUCATION AND CAREER PATHWAY INTELLIGENCE SYSTEM FOR SRI LANKAN LEARNERS

University of West London — final-year project

**Working draft revised against original proposal and August interim — 29 October 2026. Not approved for submission.**

Author: Oshem Thirsha Kanakarathna. Student ID: 34164665. Module: CP6SL460, School of Computing and Engineering. Supervisor as listed on both originals: Dr. Ama Kulathilake. Current cover-sheet requirements, word limit and submission date still require the actual assessment brief. The author-confirmed original proposal and interim DOCX files have now been inspected; their hashes and review coverage are recorded in alignment/SOURCE_REVIEW.json. November is the accelerated working target, not a verified university deadline.

### Abstract

WiseLanka investigates how a bounded web prototype can combine explicit educational requirements with personalised programme exploration. Its curated CSV knowledge base contains 11 programmes across Information Technology, Business and Management, and Engineering, including vocational progression. A FastAPI backend separates authoritative academic rule assessment from relevance ranking. Outcomes distinguish MET, NOT_MET and NOT_ASSESSED. A frozen pretrained MiniLM sentence encoder performs local ONNX inference; TF–IDF and deterministic ordering provide comparison methods. Guided support, draft English/Sinhala/Tamil interface strings and optional browser speech input extend interaction without allowing conversational or relevance outputs to alter academic rules.

At the WP5 checkpoint, 205 backend tests, 36 browser tests, five live integration workflows and 14 implementer-authored synthetic reference cases passed. Integrity checks and a fresh optional-AI installation succeeded. Automated accessibility scans detected no violations in nine tested states after targeted corrections. A nine-scenario ranking comparison was completed, but independent relevance judgements were unavailable. No ranking-quality improvement, satisfaction score or learner-outcome benefit is claimed. Adult usability evaluation, fluent translation review and native speech/assistive-technology testing remain pending. The resulting contribution is a reproducible, evidence-aware prototype and a documented evaluation design; the broader research claim remains provisional.

### Author review and assistance disclosure

This draft was prepared with AI assistance from Codex using repository inspection and checked sources. It must not be represented as wholly unaided student writing. The author must review sources, revise and take responsibility for the analysis, and confirm permitted assistance and disclosure requirements against the actual assessment brief. A module-specific permission or declaration has not been verified. No declaration of originality or ethical approval is signed or fabricated here. Personal reflection, acknowledgements and approved institutional wording must be written/confirmed by the author.

### Reading guide

Chapters 1–10 provide a continuous dissertation argument. References and appendices follow. “Measured” refers to saved technical observations; “synthetic” refers to fictional profiles; “mocked” refers to simulated browser/API events; “pending” denotes work not performed. Bibliographic style is provisionally author–date and must be reconciled with the actual university instructions. The companion deliverable inventory records academic blockers.
