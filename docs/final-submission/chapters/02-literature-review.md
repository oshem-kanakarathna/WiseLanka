# 2. Critical literature review and research gap

## 2.1 Review approach and evidential limits

This is a focused narrative review, not a completed systematic review. WP6 searches on 29 October 2026 targeted original publisher/proceedings pages, research-commission publications and model documentation. Topics included educational recommenders, hybrid recommendation, sentence embeddings, explanations and evaluation. The source register records URLs, access scope and barriers. Some works were available only as publisher abstracts: those are used for high-level claims, not detailed methodological appraisal. No search-result counts, screening flow, inter-rater agreement or exhaustive coverage is invented. The author should expand database searches and full-text appraisal through the university library before finalising Objective I.

## 2.2 Educational recommendation and learner agency

Deschênes (2020) reviews 56 studies concerning learner agency and distinguishes accuracy, satisfaction and learning-performance evaluation. This distinction is valuable because an algorithm can retrieve related content without helping a learner make a justified decision. The review concerns learning contexts rather than Sri Lankan admission decisions, so direct transfer of findings would be inappropriate. WiseLanka therefore preserves exploration and official links rather than presenting its order as a uniquely correct pathway.

Da Silva et al. (2023), whose publisher abstract was checked, report that hybrid approaches were prominent in their selected studies while pedagogical effectiveness received less evaluation attention. Their sample and time window limit generalisation. The implication for this project is methodological: functional success and ranking comparisons should be accompanied by separate relevance and human-comprehension protocols. This does not establish that WiseLanka improves education or that hybridity itself produces benefit.

Lahoud et al. (2023), already cited in both original reports, directly compares university-major/career guidance approaches using a Lebanese case study. Its knowledge-based, ontology/case-based and collaborative combinations provide a closer comparator than generic course-resource retrieval. WiseLanka does not reproduce that data-rich hybrid or its study results: it lacks historical preference labels and instead constrains frozen content similarity with explicit rules. The distinction narrows the contribution to a locally curated, policy-aware integration, rather than claiming that combining techniques is novel. The article methods and population differ from this prototype and cannot supply its missing relevance or usability findings.

## 2.3 Explicit constraints and hybrid recommendation

Burke (2002) examines combinations of recommendation techniques. The useful principle here is that different mechanisms can address different weaknesses. WiseLanka adopts a constrained sequence: formal rules establish an academic assessment group, and content similarity influences exploration within that group. It is not a weighted blend in which high semantic similarity compensates for a failed entry requirement. Unlike interaction-based recommendation, this design can operate without historical preference data; its trade-off is dependence on manually curated descriptions and rules. The publisher abstract supports the general hybrid framing, not a claim that Burke evaluated this implementation.

Pure eligibility filtering would be transparent but insensitive to paraphrased interests. A purely semantic system could retrieve attractive programmes with unmet or unknown conditions. Collaborative filtering was considered inappropriate for this dataset because no legitimate interaction/rating matrix exists. Artificial feedback would allow code experimentation but would not supply evidence of learner preferences. These are project-specific design judgements, not empirical rankings of all algorithms.

## 2.4 Lexical and semantic content matching

Salton and Buckley (1988) establish term weighting as a retrieval baseline. TF–IDF is useful here because its vocabulary matches can be inspected and its corpus is small. Its limitation is lexical dependence: related intentions need not share programme words. WiseLanka implements a declared smoothed-IDF variant and cosine comparison; it does not assert exact replication of every weighting scheme in that paper.

Reimers and Gurevych (2019) introduce sentence representations compared with cosine similarity. This motivates testing contextual embeddings for paraphrased interests. Their reported benchmark results concern their own experimental tasks and do not transfer as accuracy figures for WiseLanka. The deployed model's learned representation is externally pretrained; the project only performs frozen inference. Its ability to produce nonidentical vectors for paraphrases is not evidence that a particular programme is educationally suitable.

Wang et al. (2020) investigate attention-based distillation for smaller Transformer models. Their work supports the rationale for a lightweight encoder, but is not itself a validation of this specific sentence-transformer export or educational use. WiseLanka's actual runtime, revision and checksum-locked artifacts are evaluated locally. English semantic input is retained even when interface controls switch language. No Sinhala/Tamil semantic understanding is inferred from interface translation.

## 2.5 Explanations, understanding and persuasion

Tintarev and Masthoff (2012) distinguish several explanation goals and caution that they may conflict. The publisher abstract describes effectiveness/satisfaction trade-offs in movie and camera studies; these domains do not prove educational effects. The important design implication is to measure whether a learner understands missing evidence and conditional progression, rather than treating a persuasive explanation as accurate. WiseLanka's source links and status reasons expose evidence, but its similarity explanation is a description of the matching method, not a faithful attribution of each embedding dimension.

The proposed explanation questions separately test recognition of NOT_ASSESSED, admission uncertainty and self-reported competence. Agreement with a statement such as “the explanation was clear” is weaker than correctly explaining a condition in a task. Both observations should be retained and disagreements discussed.

## 2.6 Local guidance context and accessibility

The NEC report provides historical context for career-guidance research (National Education Commission, 2016). It cannot establish that the selected 11 programmes represent contemporary learner demand. Independent adult needs/usability evidence and review of current policy remain important. A prototype which centralises information also risks amplifying curation bias: seven IT programmes have more opportunities to appear than the single Business programme.

The original reports compare CareerMe and CareerOne, but their broad descriptions of limited integration do not establish absence of competing functionality. CareerMe's inspected homepage explicitly advertises degree, subject and skills matching and three-language career testing (CareerMe, n.d.). TVEC's published CareerOne operational guidance describes vocational career/navigation and employment support (TVEC, 2025). These are provider descriptions, not independently tested effectiveness claims. Their overlap means WiseLanka should be defended through its explicit rule/uncertainty/progression design and evidence, not an unsupported “first” or “only” platform claim. No exhaustive competitor audit or real learner comparison was performed.

WCAG supplies testable accessibility criteria (W3C, 2024). Automated checks detect some implementation faults but cannot establish all interaction or language-quality requirements. Accordingly, WiseLanka combines measured automated scans with pending manual keyboard, screen-reader, zoom and fluent-language review. Interface availability should be distinguished from practical accessibility for a particular person and browser.

## 2.7 Evaluation and the bounded research gap

Järvelin and Kekäläinen (2002) motivate graded, position-sensitive retrieval evaluation. The proposed nDCG protocol is appropriate only when legitimate relevance judgements exist; its numerical precision would otherwise conceal invented labels. The study uses a stated exponential-gain variant and within-group candidate pools, rather than assuming every nDCG formulation is identical.

The gap addressed is therefore a local design/evaluation problem: can a small, source-aware prototype keep policy assessment, missing evidence and semantic relevance separate while supporting practical pathway exploration? It is not a claim that no earlier system combines rules and AI. The current artifact demonstrates those separations in tested cases; independent relevance and usability work is needed to determine whether learners find the resulting guidance useful.

## 2.8 Synthesis of alternatives

| Approach | Potential value | Limitation for this project | Decision |
|---|---|---|---|
| Rules alone | Explicit requirements, traceable reasoning | Limited preference interpretation | Retain as authority and baseline |
| TF–IDF | Reproducible lexical comparison | Synonym/paraphrase sensitivity | Implement comparison |
| Frozen embeddings | Pretrained semantic representation, no local training corpus needed | English/corpus bias, relevance unvalidated | Implement bounded local inference |
| Collaborative/feedback learning | Could model observed preferences | No legitimate training labels | Defer; design opt-in future study |
| Unrestricted generative guidance | Flexible conversational surface | Unsupported educational claims, extra dependencies | Use read-only guided intents instead |

The review supports a justified prototype design, while its access and coverage limitations prevent a claim that Objective I is already fully satisfied. The proposal/interim bibliography was also read: malformed author strings, the incomplete conversational-review DOI and generic policy entries are flagged in alignment/CONTRADICTIONS_AND_LIMITS.md. Earlier citation presence is not verification, and those entries are not automatically promoted into this final bibliography.
