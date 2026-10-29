# 6. Knowledge-base construction and educational validation

## 6.1 Curated snapshot

The WP5 snapshot has 11 programmes, 11 institutions, 12 qualifications, 33 entry-rule rows, five progression relationships, 21 source records, five careers and 13 skills. Domain counts are IT seven, Business and Management one, Engineering three, including two vocational-related programmes. The catalogue is sufficient to demonstrate different routes but too small and uneven to represent national opportunity or learner demand.

Programme titles include Moratuwa IT and AI, UCSC Computer Science, IIT Computing Foundation and three related degrees, OUSL Management Studies, Peradeniya Engineering, Jaffna University College HND Mechatronics and UoVT Engineering Technology in Mechatronics. The programme inventory in appendix B retains exact stored titles and source URLs rather than silently rewriting provider terminology.

The five progression edges comprise three foundation-to-degree routes and two conditional vocational routes. The AI/Data Science foundation route records the published 40% condition in each named module; all edges have `guaranteed=false`. NVQ route records do not infer universal qualification equivalence or exemption. Current provider checks are unresolved where necessary.

## 6.2 Source selection and provenance

Official regulator and programme/provider documents support represented academic conditions. `data/metadata/evidence_sources.csv` stores organisation, URL and access date; requirement and progression rows point to source IDs. A programme's application URL supports navigation, but does not independently establish every career relationship or recognition claim. Access date is not publication date and must not be interpreted as a live guarantee of currency.

WP5 reviewed selected official UGC, Moratuwa, IIT, OUSL, Peradeniya, UCJ and UoVT material. It did not independently refresh every legacy recognition, career-skill or scholarship record. The full UGC handbook was retrieved and parsed; its checksum and page locations are in the evidence register. No new accreditation, equivalent qualification or scholarship opportunity was invented. Independent provider/domain adjudication remains pending.

## 6.3 Source review as an evaluated correction

The Moratuwa IT page identifies selection context beyond subject grades. The UGC handbook contains general-entry constraints involving one sitting, attempt limits and Common General Paper conditions, together with course/district/year-dependent selection (University Grants Commission Sri Lanka, 2025/2026). Exact source locations and caveats are in the [WP5 review](../../evidence/wp5/EDUCATIONAL_SOURCE_REVIEW.md) and rule register. The application does not collect enough evidence to resolve all these conditions.

Before correction, PRG0001–3 could appear fully met from subject passes alone. WP5 added SRC0021 and provider-review rules REQ0032–34 and refreshed PRG0009's existing review condition. The repaired outcome is NOT_ASSESSED where represented subjects pass but those additional decisions remain unknown. This conservative repair is preferable to inventing Z-score thresholds or gathering unnecessary personal information during a small prototype sprint. A known failed mandatory subject remains NOT_MET.

This example distinguishes rule-execution correctness from domain completeness: an engine can perfectly execute an incomplete rule set. Updating tests to match reviewed policy semantics is legitimate only when the supporting source and reasoning are preserved. Earlier failed tests and final passing logs were retained for that purpose.

## 6.4 Integrity and update procedure

Validation checks unique identifiers, foreign-key relationships, permitted domains, grouped operators and numeric count constraints. A frozen dataset SHA256 manifest supports exact reproduction. The rule-evidence CSV inventories all 33 requirements with conditions and source references. The 14 reference cases connect supplied evidence to expected statuses, including incomplete data, a failed subject and conditional vocational investigation.

For future updates, identify the applicable intake/policy year, inspect the original source and exact route, record changes and have ambiguous rules independently reviewed. Run integrity, boundaries, affected scenarios and full regression before accepting a snapshot. Contradictory sources require adjudication or NOT_ASSESSED, not convenient averaging. Removing a provider-review flag would require evidence that the newly collected/verified inputs genuinely resolve that condition.

## 6.5 Remaining educational limitations

Limited Business coverage can distort exploration. Self-reported awards are not authenticated. Career relationships and skill proficiency expectations have weaker provenance than admission rules. One recorded scholarship is historical/closed awareness and cannot represent current financial support. Source URLs and admissions policy can change after the recorded review. The defensible claim is source-aware prototype guidance, not provider-approved advice, comprehensive recognition assurance or automated admissions determination.
