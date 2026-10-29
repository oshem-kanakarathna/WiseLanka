# WP2 completion evidence — 29 October 2026

Scope: a curated prototype, not comprehensive national admissions coverage.
Local checkpoints: `db1681a` preserves the pre-existing README independently;
`876466b` preserves accepted WP1. WP2 changes remain uncommitted. Nothing pushed.

## Verified catalogue additions

| Programme | ID | Domain | Official source | Supported scope |
|---|---|---|---|---|
| OUSL Bachelor of Management Studies Honours | PRG0008 | Business and Management | https://ou.ac.lk/programme/bachelor-of-management-studies-honours-2/ | Three A/L passes in one sitting is one route; age 18 at registration, alternative awards and selection conditions require provider assessment |
| Peradeniya Bachelor of the Science of Engineering Honours | PRG0009 | Engineering | https://eng.pdn.ac.lk/academic/undergraduate-programme/ | Passes in Combined Mathematics, Physics and Chemistry; government admissions policy remains separate |
| UCJ Higher National Diploma in Mechatronics Technology | PRG0010 | Engineering / vocational | https://ucj.ac.lk/hndmnt/ | Selected NVQ 4 Electrician route; other named trades and specified A/L streams remain provider-reviewed alternatives |
| UoVT Bachelor of Engineering Technology in Mechatronics Technology | PRG0011 | Engineering / vocational progression | https://uovt.ac.lk/en/academics/courses/btech-mechatronics-technology | Selected NVQ 6 Mechatronics entry category; no automatic admission or exemption |

All above pages were opened through the web tool. Recorded verification/access date:
2026-10-29. Provider names, source organisations and dates are stored in CSV records.
Detailed new-rule mapping, conditions, source URLs and applicable learner categories
are in `rule-traceability.csv`. A/L and qualification entry categories are explicit;
learner category never substitutes for an actual qualification.

Framework levels are blank for the new degrees: their precise framework placement
was not independently established. UCJ's course structure explicitly contains NVQ
levels 5 and 6; its HND is represented at NVQ 6. The NVQ 4 Electrician certificate is
an entry-category qualification record, not a newly invented training programme.
UCJ's separate awarding authority remains blank. Recognition additions establish
only official provider listings, not regulator or professional accreditation.

## Two conditional vocational progression edges

- QLF0012 (reported NVQ 4 Electrician certificate) → QLF0010 (UCJ Mechatronics HND):
  UCJ lists that certificate as an entry route. Provider document checks and current
  admissions arrangements remain unresolved; no seat is promised.
- QLF0010 (reported NVQ 6 Mechatronics HND) → QLF0011 (UoVT Mechatronics degree):
  the degree page lists the NVQ categories and Mechatronics discipline. Additional
  process evidence: https://uovt.ac.lk/en/academics/admission_page . Tests, interviews
  where applicable and document verification remain provider decisions. No bilateral
  articulation agreement, automatic credit exemption or admission is asserted.

Both edges are dated 2026-10-29, have source IDs, and emit `guaranteed=false`.
The learner profile displays held-award progression with official source links.

## Corrected existing IIT condition

Opened https://www.iit.ac.lk/foundation/it/ . The page currently specifies 40% for
four named AI progression modules. PROG0003 now records 40 percent, replacing the
previously stored 50 percent, with SRC0010 and the new verification date. The
source also supports the six-pass/three-credit foundation entry condition.
Progression remains conditional and not guaranteed. Historical WP1 evidence was
preserved rather than rewritten to pretend it originally used the new threshold.

## Correctness and architecture changes

- Removed the contradictory package-level eligibility implementation: public
  imports now re-export the canonical engine. Its previous empty-rule `all([])`
  result and invalid-grade comparison could produce unsupported eligibility.
- Consolidated application CSV reads through one rooted loader. Changed working
  directory no longer changes dataset lookup. Missing files raise errors instead
  of masquerading as empty relationships; malformed headers/row widths are rejected.
- Added startup and CLI integrity validation across all 20 CSVs under `data/`:
  identifiers, relationship references, relationship keys, group operators, count
  values and approved programme domains. Master vocabulary identifiers are checked;
  legacy free-text vocabulary fields are not all constrained as foreign keys.
- Known knowledge-data failures return HTTP 503 without an eligibility decision;
  all academic request endpoints share examination validation.
- Added explicit provider-review and reported-qualification requirement types.
  Reported framework numbers never imply equivalence. Missing rules, credentials,
  source evidence or provider decisions remain NOT_ASSESSED. An actual documented
  subject failure can still produce NOT_MET.
- Preserved legacy booleans/categories/scores for compatibility. Canonical insight
  status takes precedence in all three academic interfaces, including the older
  eligibility/recommendations pages. Unknown is not displayed as rejection.
- Requirement explanations expose source organisation, access date and URL;
  progression exposes source links, dates and supporting admissions sources.
- Reused the canonical grade ordering for scholarship checks; missing scholarship
  information retains its existing unknown semantics. No scholarship was added.

No database, service, dependency or frontend rewrite was introduced.

## Actual verification

- Backend: **160 passed**, including 28 WP2 cases beyond the 132-case WP1 baseline.
- Browser: **23 passed**, including a new older-page uncertainty regression.
- Complete CSV integrity command: **passed**, all 20 data CSVs.
- Original live browser/API integration: **passed**.
- Expanded WP1 live workflow: **passed**, evidence redirected under WP2 so WP1
  screenshots remain unchanged.
- WP2 live workflow: **passed**: Business rendering/source, vocational rendering,
  IT readiness, Engineering subject readiness with unknown selection, unmet Physics,
  missing Physics, missing rules and both conditional vocational edges.
- Git whitespace check: passed.

See the saved logs and `verification.json` for commands, exit codes, timestamps and
source/dataset hashes. Live verification used a new API on 8011 and the existing
static frontend on 5500. User servers were not replaced. Tests use Python 3.9.6;
backend reproduction environment and browser project environment match WP1 tooling.
No new installation or human evaluation was performed.

Existing tests that assumed exactly three A/L computing records were updated for
five A/L candidates. Their original computing eligibility/score assertions remain
explicitly tested; new candidates have separate unknown-selection assertions.
The source-dependent 50-percent tests were updated to 40 percent. This is catalogue
expansion and a verified rule correction, not deletion of failing tests.

## Coverage and requirements traceability

11 programmes: **IT 7; Business and Management 1; Engineering 3**. The Engineering
count includes the vocational HND and vocational-entry degree; these are not extra
programmes counted twice. Totals: 11 institutions, 12 qualification categories,
30 entry-rule rows, 5 progression edges, 20 source records and 18 recognition rows.
See `coverage.json`; the two new vocational edges supplement three existing edges.

| Requirement | WP2 contribution/status |
|---|---|
| Objective III | Structured knowledge expanded and integrity-tested; PARTIAL at full-proposal scale because coverage is curated |
| Objective IV | Eligibility foundation improved; PARTIAL, hybrid AI remains absent |
| Objective V | Three-domain prototype and conditional alternatives demonstrated; PARTIAL for full learner/domain coverage |
| Objective VII | Functional/scenario evidence expanded; PARTIAL, usability and scientific effectiveness unverified |
| FR1–FR2 | IMPLEMENTED in prototype; structured awards retained, Business A/L subjects added |
| FR3 | IMPLEMENTED deterministic recommendations; no trained-AI claim |
| FR4 | IMPLEMENTED bounded conditional pathways, no admission guarantees |
| FR5–FR6 | IMPLEMENTED recorded requirement gaps and explanations; actual competence not assessed |
| FR7 | IMPLEMENTED official requirement/progression links and provenance |
| FR8–FR9 | MISSING; chatbot/voice belong to later packages |

## Limitations, source blocks and handover

The Ratmalana admissions URL https://www.ucr.ac.lk/admissions/ returned 403; no
Ratmalana record was added. The UoVT applicant portal programme URL timed out, so
portal-specific exemption claims were withheld. The accessible official degree
and admissions pages support the narrower conditional route above. Neither block
was silently treated as source verification.

Only the listed new sources and IIT progression page were checked during WP2.
Older source records are inherited provenance, not newly reverified claims. This
is not a regulatory accreditation audit. Active catalogue records do not mean
applications are open; OUSL's published intake dates are historical and the record
instructs users to check the next call.

Vocational matching uses selected catalogue IDs. Other trades, credentials,
framework equivalences and stream details require provider review. Non-IT career
and skill mappings remain sparse; none were invented to fill coverage. A/L stream,
selection tests, exam-sitting history, age and documents are not automatically
verified. No evidence supports broad recommendation quality, user satisfaction,
WCAG conformance or educational benefit from these functional passes.

Source-aware structured candidates are ready for WP3 development. WP3 has not
started. All WP2 changes are left for review; no push or WP2 commit was made.
Modified/new implementation and test files are listed in `modified-files.txt`;
this report, rule traceability, logs, coverage, verification and screenshots are
additional WP2 evidence artefacts. Both original JavaScript backups and the
checkpointed README/WP1 evidence are preserved.
