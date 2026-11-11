# Working revision draft: Sections 2.4 and 2.5

> **For the student’s critical review only — not final submission text.** This AI-assisted draft is based on the existing Chapter 2, Stage 1 evidence matrix, source registers and the Stage 2A reconciliation. The student must read and validate the sources, check the claims and citation style, and rewrite or authorise any wording before integration.

## 2.4 Lexical and semantic content matching

Lexical retrieval and sentence embeddings offer different ways to match learner interests to programme descriptions. Salton and Buckley (1988) examine term-weighting combinations using term frequency, inverse document frequency and vector normalisation. Their information-retrieval work supports a lexical baseline, but neither prescribes WiseLanka’s smoothed-IDF calculation nor establishes educational quality. Shared vocabulary can make a lexical match inspectable, while differing wording may weaken it; this limitation is an inference for this use case, not their measured result.

Sentence-BERT (SBERT) uses siamese or triplet structures to produce sentence vectors compared by cosine similarity (Reimers and Gurevych, 2019). Its semantic-similarity and transfer evaluations concern NLP tasks, not education programmes; they motivate comparison, not transfer of benchmark performance. Wang et al. (2020) describe MiniLM’s self-attention distillation for Transformer compression. This supports a compact-model rationale, not validation of WiseLanka’s sentence model or ranking. Neither method yields an admission or career-success probability.

Accordingly, WiseLanka’s deterministic, TF–IDF and frozen semantic methods should be compared on identical candidate sets. Their scores are not probabilities. Without independent relevance judgements, ordering and runtime differences cannot show which method recommends better programmes.

## 2.5 Explanations, understanding and persuasion

Explanations may aim at transparency, scrutability, trust, persuasiveness, effectiveness, satisfaction or efficiency, and these aims can conflict (Tintarev and Masthoff, 2012). The source register records abstract/metadata access; its four empirical studies concern movie and camera recommenders. It supports this conceptual distinction, not detailed transfer to education. Persuasion or satisfaction alone does not show that a learner understood a condition or received a correct recommendation.

Knijnenburg et al. (2012) relate objective system properties and user behaviour to perceptions and experience in a user-centred evaluation framework, examined through four field trials and two controlled experiments. This supports evaluating beyond algorithmic accuracy, but does not validate WiseLanka’s instrument or establish educational trust effects. Behaviour, perceived quality, usefulness, satisfaction and comprehension should remain distinct measures.

In WiseLanka, the explanation displays the academic state and reasons separately from semantic relevance, with available source links. This is an implementation choice, not evidence that users understand or trust it. Traceability cannot make an outdated or incomplete source correct. Where requirements are ambiguous or evidence missing, the system should expose uncertainty rather than infer failure. This design inference requires independent rule/source review and user evaluation.

Evaluation should test rule/source correctness, user comprehension of conditions and uncertainty, and self-reported clarity, usefulness or trust separately. Correct educational data, correct rule execution and positive user perception are different outcomes. No current WiseLanka evidence establishes improved comprehension, trust or educational benefit.

### References cited in this working draft

Knijnenburg, B.P., Willemsen, M.C., Gantner, Z., Soncu, H. and Newell, C. (2012) ‘Explaining the user experience of recommender systems’, *User Modeling and User-Adapted Interaction*, 22, pp. 441–504. https://doi.org/10.1007/s11257-011-9118-4.

Reimers, N. and Gurevych, I. (2019) ‘Sentence-BERT: Sentence embeddings using Siamese BERT-networks’, in *Proceedings of EMNLP-IJCNLP 2019*, pp. 3982–3992. https://doi.org/10.18653/v1/D19-1410.

Salton, G. and Buckley, C. (1988) ‘Term-weighting approaches in automatic text retrieval’, *Information Processing & Management*, 24(5), pp. 513–523. https://doi.org/10.1016/0306-4573(88)90021-0.

Tintarev, N. and Masthoff, J. (2012) ‘Evaluating the effectiveness of explanations for recommender systems’, *User Modeling and User-Adapted Interaction*, 22, pp. 399–439. https://doi.org/10.1007/s11257-011-9117-5.

Wang, W., Wei, F., Dong, L., Bao, H., Yang, N. and Zhou, M. (2020) ‘MiniLM: Deep self-attention distillation for task-agnostic compression of pre-trained Transformers’, *Advances in Neural Information Processing Systems*, 33. Available at: https://proceedings.neurips.cc/paper_files/paper/2020/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf.

### Editorial comparison (not dissertation prose)

Original §§2.4–2.5 word count: **335 words**. Revised section word count: **426 words** (increase: 91). Counts use a word-token regular expression over section headings and body up to the references; they exclude this note and bibliography. The revision distinguishes model contributions from local relevance evidence and explanation aims from comprehension, correctness and perception measures. The student should check that this allocation is proportionate within the 10,000-word report.
