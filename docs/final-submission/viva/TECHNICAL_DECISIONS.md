# Technical decision notes for later tutoring

The major-engine map is in dissertation chapter5. Keep eligibility status, academic match score, career suitability, self-reported skill status and semantic relevance separate when explaining the system. The legacy `assessment_method` remains rule-based personalisation; actual relevance is `ranking.method`.

Core source anchors: personalisation/models.py:49 (profile), eligibility/engine.py:776 (canonical gaps), personalisation/engine.py:188 (orchestration), relevance/engine.py:67 (grouped ranker), relevance/encoder.py:15 (local encoder), assistant/engine.py:40 (read-only guidance), skills/engine.py:4 (self-report comparison). Paths are under backend/app/. JavaScript interaction boundaries are in frontend/components/learner-profile.js, i18n.js and guided-assistant.js.

Key alternatives rejected/deferred: user accounts/persistence, database migration, frontend rewrite, paid unrestricted LLM chat, large-model training and unvalidated feedback learning. Reasons were bounded scope, no demonstrated infrastructure need, privacy/grounding concerns and insufficient legitimate training evidence. Do not describe rejected alternatives as universally inferior; their suitability could change with data and scale.

The original WP1–WP5 checkpoints remain intact. WP6 adds academic material only. Later tutorials should inspect these actual modules and tests, then let the author explain decisions and limitations in their own words.
