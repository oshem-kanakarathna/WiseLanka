# Stage 14 — Official-source knowledge-base expansion

**Run date:** 7 November 2026
**Status:** Implemented catalogue/data-integrity work; no live Gemini request, participant collection, or admission-rule change to the existing programmes.
**Interpretation:** `MET`/`NOT_MET`/`NOT_ASSESSED` are local rule assessments. `MET` is not an admission decision.

## Official sources inspected

| Source | Official URL | Publication / access | Facts used | Limits retained |
|---|---|---|---|---|
| IIT Computing Foundation | https://www.iit.ac.lk/foundation/it/ | Page has no publication date shown; accessed 2026-11-07 | O/L Sri Lanka or London (Cambridge/Edexcel): six passes, at least three credits including English and Mathematics; eight months; successful completion may permit entry to year 1 of the listed IIT degrees; AI/Data Science needs at least 40% in four named modules; learners below that threshold may still progress to CS or Software Engineering. | No guaranteed admission. Catalogue's grade model does not map London grades to Sri Lankan grades. Provider confirmation remains necessary. Existing progression edges remain `guaranteed=false`.
| IIT BEng Software Engineering | https://www.iit.ac.lk/course/beng-software-engineering/ | Page has no publication date shown; accessed 2026-11-07 | Four-year full-time, University of Westminster award, IIT page recognition claims, January 2027 next intake and January/September intake pattern. | No direct academic entry requirement was published on the reviewed course page. PRG0005 remains without a direct-entry rule and therefore `NOT_ASSESSED`.
| IIT BSc Computer Science | https://www.iit.ac.lk/course/bsc-computer-science/ | Page has no publication date shown; accessed 2026-11-07 | Four-year full-time, Westminster award, IIT page recognition claims and January 2027 intake information. | No direct academic entry requirement was published on the reviewed course page. PRG0006 remains `NOT_ASSESSED` for direct eligibility.
| IIT BSc AI and Data Science | https://www.iit.ac.lk/course/bsc-artificial-intelligence-and-data-science/ | Page has no publication date shown; accessed 2026-11-07 | Four-year full-time, Robert Gordon University award, IIT page recognition claim and January 2027 intake information. | No direct academic entry requirement was published on the reviewed course page. PRG0007 remains `NOT_ASSESSED` for direct eligibility; the Foundation page's separate four-module progression condition remains recorded.
| SLIATE HNDIT | https://www.sliate.ac.lk/course/hndit | No publication/intake year shown; accessed 2026-11-07 | 2½ years; one-sitting A/L in any stream; ordinary O/L English and Mathematics; selection by A/L merit and aptitude/IQ test; multiple ATIs listed. | Page does not state an explicit A/L pass count. Sitting history, merit and aptitude are not represented in the learner profile. No framework equivalence or degree credit transfer added.
| SLIATE HNDM | https://www.sliate.ac.lk/course/hndm | No publication/intake year shown; accessed 2026-11-07 | One-sitting A/L in any stream plus ordinary O/L English and Mathematics, OR named DTET National Certificate for Accounting Technicians / National Certificate in Business Studies (Public Administration or Marketing) plus the same O/L passes. | Named alternative awards are not yet separate catalogue qualifications; current intake and award authenticity require provider confirmation. No framework level inferred.
| DTET ICT sector course list | https://dtet.gov.lk/en/sectors/information-communication-multimedia-technology/ | Current listing page accessed 2026-11-07; copyright footer 2026 | Lists ICT Technician K72S004 under NVQ 3/4 and National Diploma in ICT ETB 11 under NVQ 5/6. | Listing establishes current catalogue presence, not current intake availability or campus-specific delivery/requirements.
| DTET Gazette notice | https://dtet.gov.lk/wp-content/uploads/2026/02/2025-10-31I-IIAE.pdf | Gazette dated 2025-10-31; accessed 2026-11-07 | K72S004F4.2: six O/L passes including medium language and English within two sittings, OR relevant-field NVQ 3; six-month course plus six-month OJT; NVQ 4. K72T001F5.2: relevant-field NVQ 4, OR three A/L subjects including ICT in one sitting (excluding GIT/General English); 1½-year course plus six-month OJT; NVQ 5. | Conditions are from a 2025 notice and do not establish a 2027 intake. “Relevant field”, exact medium-language evidence and sitting count require provider confirmation. Rules remain `NOT_ASSESSED`.

## Changes and catalogue coverage

Preserved all identifiers PRG0001–PRG0011, QLF0001–QLF0012 and PROG0001–PROG0005. Added:

- PRG0012 / QLF0013 — SLIATE Higher National Diploma in Information Technology.
- PRG0013 / QLF0014 — SLIATE Higher National Diploma in Management.
- PRG0014 / QLF0015 — DTET Information and Communication Technology Technician, course K72S004F4.2, NVQ Level 4.
- PRG0015 / QLF0016 — DTET National Diploma in Information and Communication Technology, course K72T001F5.2, NVQ Level 5.

| Coverage | Before | After |
|---|---:|---:|
| Active programme records | 11 | 15 |
| IT | 7 | 10 |
| Business and Management | 1 | 2 |
| Engineering | 3 | 3 |
| Qualification records | 12 | 16 |
| Programme requirement rows | 33 | 42 |
| Progression edges | 5 | 5 |
| Evidence-source records | 21 | 25 |

Existing engineering coverage remains the Peradeniya A/L degree, UCJ Mechatronics HND, and UoVT Mechatronics degree with its documented non-guaranteed conditional progression. No new engineering requirement was added.

The DTET ICT Technician NVQ4 to ICT National Diploma NVQ5 route was not encoded as a progression edge. The Gazette provides the general "relevant-field NVQ 4" entry condition, but the reviewed source does not explicitly confirm that this named certificate is accepted as relevant for this exact diploma. It remains a verification backlog item rather than a claimed pathway.

### Existing IIT direct-entry gap

PRG0005–PRG0007 course pages were re-opened and programme facts refreshed. The pages did not publish direct academic entry conditions. The IIT Foundation page independently supports the existing PRG0004 entry rules and its three progression relationships, including the corrected **40%** AI/Data Science threshold in Mathematics for Computing, Mathematics for Data Science, Introduction to Programming, and Computer Programming. The stored PROG0001–PROG0003 edges remain non-guaranteed. The direct-entry rows for PRG0005–PRG0007 were deliberately left absent: this is evidence that the gap was checked, not a reason to infer requirements.

## Eligibility and data representation decisions

- SLIATE's O/L subject minimums are encoded with the existing grade engine. A/L one-sitting conditions, unspecified pass-count interpretation, and HNDIT aptitude/merit selection are provider-review rows; WiseLanka cannot derive them from subjects alone.
- DTET alternative-route conditions have multiple branches with sitting, medium-language, and relevant-field requirements. The current learner profile cannot represent those facts safely. Rather than flattening alternatives into incorrect AND/OR rules, the records expose the official conditions in a sourced `PROVIDER_REVIEW` rule and remain `NOT_ASSESSED`.
- HND framework levels and separate awarding-authority claims are blank because the sources reviewed did not establish those facts.
- No accreditation, equivalence, scholarship, admission guarantee, course fee, or credit-transfer claim was added.
- HNDM's alternative DTET National Certificate categories are described in the source-backed requirement text but are not separately selectable qualification IDs yet.
- The expanded catalogue revealed that the legacy recommender's “any supplied entry level overlaps” filter could show an A/L-entry HND to an O/L-only learner when the HND also required O/L English/Maths. The filter now uses the highest academic stage in the programme's requirements: A/L-only or multi-stage programmes require an A/L profile to appear as an immediate recommendation; O/L-only routes remain available to O/L learners. Regression tests confirm the O/L ICT certificate and IIT Foundation stay visible with `NOT_ASSESSED` preserved for uncollected details, while HNDIT/HNDM are not misrepresented as direct O/L options.

## Gemini shortlist privacy review

Before this expansion, the optional Gemini endpoint selected a top eight candidate subset using local profile-dependent route/status/interests scoring. With ten IT records, candidate IDs in the provider request could have indirectly signalled educational stage or an existing qualification, even though profile data itself was not in the prompt.

The endpoint now supplies the **complete domain or explicitly requested comparison pool** to the provider, with stable public-ID ordering. Local learner-specific status and scoring remain inside WiseLanka and affect response ordering/retention only after generation. Regression tests compare the actual provider prompt/schema for distinct O/L and vocational profiles. The request still transmits the user's selected exploration domain and, when explicitly provided, comparison programme IDs; those are not exam results, qualification profiles, interests, or identifiers. Domain choice can reveal a broad topic interest, so Gemini remains optional and disabled by default.

No grades, learner interests, career-intention text, learner category, qualification profile, identifiers, or research responses are included in Gemini prompts. Future catalogue growth must retain the complete-pool rule or introduce a profile-independent candidate pool; reintroducing profile-based top-N filtering would restore the inference risk.

## Validation

The CSV integrity validator completed with 15 programmes, 16 qualifications, 42 requirement records, five progression edges and 25 source records. Focused Stage 14 data/Gemini tests: **34 passed**. Complete backend regression suite: **290 passed, 0 failed, 0 skipped** using `/private/tmp/wiselanka-minilm-runtime-venv`. Test commands: `python -m pytest tests/unit/test_data_integrity.py tests/integration/test_gemini_pathway_exploration.py -q`, then `python -m pytest tests -q`, then `python -m backend.app.data_integrity`. Tests use synthetic profiles only. No live Gemini call or participant data was used.

## Remaining limitations

1. PRG0005–PRG0007 direct entry conditions still require written, current IIT confirmation; current website pages alone do not provide them.
2. DTET detailed entry conditions need a current intake notice beyond the 2025-10-31 Gazette before any positive eligibility status is possible.
3. The application does not capture exam sittings, examination-medium language, A/L selection rank, aptitude-test results, provider decisions, or authenticity of learner-reported awards.
4. SLIATE page publication/intake dates were not stated, and HNDM alternate awards are not structured catalogue qualification IDs.
5. HNDIT degree exemptions on the SLIATE page are not treated as admission/progression guarantees; conditions need direct provider verification.
6. Catalogue coverage remains curated and representative, not a comprehensive national directory. There are no new programme-to-career or learner skill mappings for the added records.
