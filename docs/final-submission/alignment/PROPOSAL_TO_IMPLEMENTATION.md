# Original proposal versus final implementation

P and I identify the two author-confirmed original WORK documents. Locations refer to their actual sections/tables/figures, not an invented page number. This matrix records changes and uncertainties; it is not a declaration of complete assessment compliance.

| Area | Proposal commitment/location | August interim record | October/WP5 delivered state | Alignment / limit |
|---|---|---|---|---|
| Aim, objectives, research questions | P§1.2/1.4; I§1.2/1.4 | Same exact aim,8 objectives,MRQ+5SRQs | Preserved in appendixA and chapter1; traceability distinguishes implementation from outcomes | MATCH; effectiveness questions remain partly unanswered |
| Functional/non-functional baseline | P Tables2–3:FR1–9,NFR1–7 | I Tables9–10:FR01–10,NFR01–08 refine different concepts | Namespaced P-/I- mapping in REQUIREMENTS_TRACEABILITY.md | IDs are not interchangeable; no approved renumbering presumed |
| Domains and learner groups | P§1.7/Table1: IT,Business,Engineering; A/L,vocational,early-career | Seven computing programmes; O/L/A/L interaction demonstrated | Eleven programmes across all3 domains; structured awards/categories | Implemented bounded coverage, not national representativeness |
| Educational knowledge | P objectiveIII;§3.3: curated source-aware records | Programmes,qualifications,requirements,progression,careers,evidence | CSV corpus retained; strict loading/integrity and source-review refinements | Reliable datasets partially evaluated; source fidelity not proved by joins |
| Hybrid recommendations | P objectiveIV; technology Table8 rules/scoring + lightweight NLP/LLM support | Implemented eligibility/match-score mechanism is deterministic; hybrid discussed as intended direction | Local frozen MiniLM ONNX within academic groups; TF–IDF/deterministic comparison | No feedback training or independently demonstrated quality advantage |
| Explanations and chatbot | P FR6/FR8, objectiveIV/V; explanation/chat layer | Eligibility/progression explanations implemented; no evaluated chatbot module demonstrated | Deterministic explanations and bounded read-only guided intents | No unrestricted/generative chatbot or model-generated rationale claimed |
| Accessibility | P objectiveVI/FR9/NFR1–2; advanced multilingual NLP excluded | Responsive academic form; multilingual/voice marked planned | Draft135-key en/si/ta interface; optional browser voice/text fallback; axe/reflow | Native/fluent/manual and adult usefulness remain pending |
| Frontend/backend | P Tables8/10 propose Streamlit/Python | I§4.3–4.6 already documents FastAPI + HTML/CSS/JavaScript | Same separation retained and extended; no framework migration in October | Engineering substitution documented, not stack unchanged |
| Storage/data handling | P Table8 allows SQLite/CSV/JSON; appendixD Table10 listsSQLite/JSON and Pandas | Structured CSV files and Python loaders visible | CSV and standard-library loaders retained; typed validation; no database/Pandas pipeline | Main proposal permitsCSV; internal technology options differ, no invented DB benefit |
| Role/accounts/database diagrams | P appendixA Figs3/5 show authentication,counsellor/admin,notifications,saved data | Interim main architecture centres learner interface/domain engines; no accounts evidenced | No accounts,role administration,notifications,persistent profiles or analytics store | MISSING diagram elements; explicit prototype interpretation needs supervisor acknowledgement |
| Evaluation | P§3.4/Table7 functional,scenario,adult usability,explanation,accessibility | 40 automated tests/screenshots and representative cases; formal users pending | 205 backend,36 browser,5 live,14 synthetic cases;9 ranker cases; runtime/axe/fresh install | Technical evidence expanded; independent relevance/human evaluation still pending |
| Exclusions and AI boundary | P§1.7 excludes national production/full coverage/advanced deep prediction/open-domain chat | Controlled prototype | Frozen pretrained encoder inference, bounded knowledge/assistant, no learner-outcome predictive training | No claim that using pretrained deep embeddings creates a trained educational predictor |
| Schedule | P milestoneTable9; I AppendixA plan | December dissertation/January poster-viva milestones; Gantt/submission timing differs | November is the user-requested accelerated working target | Official final deadlines and formatting remain to be supplied |

## D1–D10 deliverables

| Original ID and exact wording | Current evidence | Status / remaining work |
|---|---|---|
| D1: Project proposal | Confirmed private original proposal read; chapter/appendix baseline extracted | Present; approval designation supplied by author, submission receipt not independently checked |
| D2: Literature review | Proposal/interim literature plus revised chapter2 and source register | PARTIAL: critical/full-text breadth and author review still required |
| D3: Requirements specification | Approved FR/NFR baseline and complete original/refinement traceability | Working specification documented; rubric/supervisor interpretation of diagram extras pending |
| D4: Structured pathway knowledge base | data/reference/, relationships/, metadata/; source/integrity evidence | IMPLEMENTED curated prototype; independent accuracy/currency limits |
| D5: Web-based prototype | FastAPI + HTML/CSS/JS; WP5 live logs | IMPLEMENTED bounded prototype |
| D6: Recommendation engine | Eligibility/personalisation/relevance modules;9-case comparison | IMPLEMENTED hybrid; relevance quality unverified |
| D7: Chatbot support module | assistant/engine.py; guided-assistant.js; WP4/live tests | IMPLEMENTED bounded deterministic support |
| D8: Evaluation and testing report | WP5 logs/exit codes/source/scenario/runtime/axe evidence; planned human study | PARTIAL: human/relevance/fluent/native/manual results pending |
| D9: Final project report | Existing revised DISSERTATION_DRAFT.md and editable chapters | PARTIAL working draft; not final approved/submitted report |
| D10: Poster and viva presentation | Editable one-page poster and viva outline/demo/Q&A materials | PARTIAL drafts; actual specifications, author delivery and assessment outstanding |
