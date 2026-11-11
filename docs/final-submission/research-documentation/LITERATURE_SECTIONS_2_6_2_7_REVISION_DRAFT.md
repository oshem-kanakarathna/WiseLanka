# Working revision draft: Sections 2.6 and 2.7

> **Student review material — not final dissertation text.** This AI-assisted draft is based on the current Chapter 2, the Stage 1 evidence matrix, Stage 2A source reconciliation, the completed working drafts for §§2.2–2.5, the source registers and saved project-evaluation evidence. The student must inspect the sources, verify every citation and claim, and rewrite or explicitly authorise any text before integration. No human evaluation results are reported.

## 2.6 Local guidance context and accessibility

Sri Lankan pathway sources differ in purpose and date. The National Education Commission’s study documents a policy-oriented investigation of career guidance in general education (National Education Commission, 2016). It is historical context, not evidence of current provision, adult or vocational learner needs, or present programme demand. The UGC 2025/2026 handbook is a primary source for the state-university rules in that intake; it does not establish later rules, learner needs or coverage of all vocational and provider routes (University Grants Commission Sri Lanka, 2025/2026). Policy evidence can substantiate a particular condition without showing that guidance is effective or understood.

Vocational evidence is also bounded. WiseLanka contains selected provider-documented vocational, foundation and conditional progression records, not a national qualification or equivalency map. A provider’s stated progression condition supports only that route and remains conditional; it does not imply guaranteed entry or transferability. The TVEC CareerOne operational document was not retrieved in full, so no detailed requirements or effectiveness claim is based on it (Tertiary and Vocational Education Commission, 2025). The knowledge base should therefore be presented as a limited, source-linked prototype, with coverage and source dates made explicit.

UNICEF Sri Lanka’s digital-landscape study combined survey and qualitative methods, including 5,349 children aged 11–18, focus groups and key-informant work; its tools were pretested in Sinhala, Tamil and English, and it examined access through mobile phones and computers (UNICEF Sri Lanka, 2018). This historical child-focused study makes access and language relevant design questions, but cannot establish current adult or mobile access, learner preferences, or comprehension of translated educational guidance. Its statistics must not be presented as current. The reviewed sources do not directly validate WiseLanka’s Sinhala or Tamil content: interface translation is not evidence of terminology quality or comprehension, which require fluent-speaker and user review.

WCAG 2.2 provides testable web-content criteria across devices and disability-related needs, while acknowledging that it does not address every need (W3C, 2024). It is a normative framework, not proof of conformance or task access. WiseLanka’s axe scans cover selected states and WCAG 2.0/2.1 tags; keyboard, screen-reader, high-zoom, real mobile, language and microphone checks remain pending (`docs/evidence/wp5/ACCESSIBILITY_REVIEW.md`). Responsive styling and zero detected violations therefore do not establish practical accessibility. A local visual-impairment study flagged in the reference register is excluded because its statistical reporting remains unresolved.

## 2.7 Evaluation and the bounded research gap

Evaluation must distinguish rule execution, the correctness and currency of source data, and relevance to stated interests. Passing a test shows that software follows a specified path; its expected answer may still rely on stale or misinterpreted evidence. A correct source rule can also be implemented incorrectly. Source adjudication and software tests therefore need separate records of learner route, date, conditions and uncertainty. `NOT_ASSESSED` is appropriate when evidence is absent; it is neither a rejection nor proof that the catalogue is complete.

Ranking is a separate construct. Deterministic, TF–IDF and frozen MiniLM orderings can be compared on identical scenarios and candidate pools within unchanged academic-status groups; output differences and latency do not show relevance quality. Precision@K is the proportion of the top K items labelled relevant under a declared binary threshold, but ignores order within that set and depends on the threshold. nDCG supports graded judgements and discounts lower ranks (Järvelin and Kekäläinen, 2002). It requires independent labels, consistent candidate pools and a calculable ideal ranking. For this small catalogue, report nDCG@3 only for sufficiently complete rated pools; retain missing or unjudgeable ratings as such. Neither measure tests eligibility correctness or learner benefit.

Human evaluation also requires distinct measures: completion, errors and help requests describe interaction; comprehension questions test interpretation; clarity, usefulness and trust ratings capture perceptions; comments support qualitative analysis. They may conflict—for example, a clear rating does not prove correct understanding. Knijnenburg et al. (2012) distinguish system properties, behaviour, perceptions and experience, but do not validate WiseLanka’s instruments or establish educational effects. The adult-user study remains prospective pending confirmation of the actual ethics conditions; no participant findings are available.

The research gap is bounded: prior work covers educational-resource recommendation and major/career guidance, while local sources document particular rules and routes. The defensible question is whether a small Sri Lankan prototype can combine selected source-linked requirements, expose uncertainty and keep eligibility separate from relevance while supporting pathway exploration. Synthetic tests show specified software behaviour, not national accuracy, relevance, trust, accessibility or improved outcomes. If ethically approved, a small convenience sample could identify exploratory usability problems but not establish population effectiveness or causality. Independent source review, relevance judgements and user evaluation are needed before making broader claims.

### References cited in this working draft

Järvelin, K. and Kekäläinen, J. (2002) ‘Cumulated gain-based evaluation of IR techniques’, *ACM Transactions on Information Systems*, 20(4), pp. 422–446. https://doi.org/10.1145/582415.582418.

Knijnenburg, B.P., Willemsen, M.C., Gantner, Z., Soncu, H. and Newell, C. (2012) ‘Explaining the user experience of recommender systems’, *User Modeling and User-Adapted Interaction*, 22, pp. 441–504. https://doi.org/10.1007/s11257-011-9118-4.

National Education Commission (2016) *Study on Career Guidance in General Education in Sri Lanka*. Research Series (2014), No. 08. Available at: https://www.nec.gov.lk/wp-content/uploads/2016/04/8-Final-2.pdf.

Tertiary and Vocational Education Commission (TVEC) (2025) *Operational Directives/Guideline, Mandatory Requirements of the “Career One” TVET Career Platform*. Annexure I. Available at: https://www.careerone.gov.lk/storage/newsletter/Annexure_I.Operational%20directives%20guideline-mandatory%20requirements.pdf.

United Nations Children’s Fund (UNICEF) Sri Lanka (2018) *Keeping Children in Sri Lanka Safe and Empowered Online: A Study on Sri Lanka’s Digital Landscape*. Colombo: UNICEF Sri Lanka. Available at: https://www.unicef.org/srilanka/media/281/file/Digital%20landscape%20study.pdf.

University Grants Commission Sri Lanka (2025/2026) *University Admissions Handbook: Academic Year 2025/2026*. Available at: https://www.ugc.ac.lk/downloads/admissions/Handbook_2025_26/student_handbook_english.pdf.

World Wide Web Consortium (W3C) (2024) *Web Content Accessibility Guidelines (WCAG) 2.2*. Recommendation, 12 December 2024. Available at: https://www.w3.org/TR/2024/REC-WCAG22-20241212/.

### Editorial note

Original §§2.6–2.7: **337 words**. Revised working draft: **766 words** (increase: **429**). Counts use the same word-token method over headings and section body, excluding this note and the reference list. The revision expands the discussion to distinguish source types, populations, evaluation constructs and project evidence; the student should consider its proportion within the complete 10,000-word report.
