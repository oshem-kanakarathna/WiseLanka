# 7. Hybrid AI recommendation methodology

## 7.1 Separation of decisions

The interim's implemented recommendation function sorted deterministic match scores; its AI-powered title and planned hybrid discussion are not evidence of pretrained inference at that stage. WP3 subsequently introduced the frozen encoder and TF–IDF comparison. This is a methodological extension of the earlier explicit-constraint design, not retroactive training or an August model result (Kanakarathna, 2026b, §4.5.3 and appendix D).

Let A(p,x) be the canonical academic assessment of programme p using learner evidence x, with values MET, NOT_ASSESSED or NOT_MET. Let R(p,q) be a content-relevance score for stated preference text q. Ranking is lexicographic: first the fixed academic group, then decreasing available relevance, then stable baseline position and programme ID. R never changes A. A high R is neither admission probability nor evidence of career success.

The programme corpus uses recorded title, field, domain and qualification type. It excludes eligibility outcomes and administrative notes from semantic text. It therefore contains short identity/subject descriptors rather than full course curricula. The learner query combines explicit interests, optional English career intention and selected career name, capped at 1,000 characters; tokenisation truncates model input to 256 wordpieces. This restricts both interpretation depth and potential evidence content.

## 7.2 Deterministic and TF–IDF comparisons

The original deterministic order uses existing academic matching with documented career/preference context. WP3 additionally records `legacy_order` before applying fixed academic safety groups. Comparisons must distinguish that raw order from the grouped deterministic baseline; otherwise a policy/grouping change could be misattributed to AI.

TF–IDF is implemented directly in `relevance/engine.py`: term extraction uses lowercase Latin-alphabet tokens, raw counts and smoothed IDF, idf(t)=log((1+N)/(1+df(t)))+1. Document and query vectors are L2-normalised and compared using cosine. The vocabulary/IDF fit uses the frozen active catalogue, not the learner query or relevance labels. This is corpus fitting, not learning an individual user's preferences. Unknown vocabulary contributes no supported lexical match.

## 7.3 Frozen pretrained semantic inference

WiseLanka uses `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, through its ONNX export. The inspected model card records English support and Apache-2.0 licensing (Sentence Transformers, n.d.). No model training or feedback update occurs in this project. Model-artifact hashes and the actual inference implementation are stronger reproducibility evidence than citing the model family name alone.

The local encoder tokenises inputs, runs a CPU ONNX session, performs attention-mask-aware mean pooling and L2 normalisation, then compares query and cached catalogue vectors. It checks finite outputs and bounds numerical scores before returning them. Inputs remain on the local inference machine. The model family's published benchmarks are not reported as this system's educational accuracy.

The explanation states which preference text and catalogue facts were compared. It is deliberately modest: no token-attribution model or causal explanation of embedding dimensions has been implemented. Relevance language must therefore remain methodological rather than claiming the system knows a learner's personality or competence.

## 7.4 Cold start and safe failure

An education/qualification profile is still required, but no historical feedback is needed to rank explicit interests. Empty preference text produces unassessed relevance and baseline ordering. Missing descriptions/source evidence produce no supported score. Missing dependencies, checksum-invalid artifacts, loading or inference errors return explicit unavailable/fallback metadata and null semantic scores. Academic decisions still execute. Stable ties and repeated calls are tested.

Fallback preserves baseline order within safety groups, not necessarily the exact ungrouped historic order. This distinction matters for reproducibility. Optional deployment assets require explicit initial provisioning; runtime does not silently download a model or send learner data to an external service.

## 7.5 Comparison design and leakage prevention

Nine fixed synthetic cases compare the same catalogue/candidate pools using deterministic, TF–IDF and semantic methods. They cover empty preferences, literal/paraphrased IT, Business, Engineering, failed academic requirements, missing evidence, unknown vocabulary and vocational interest. These are functional examples exposed during development, not independent held-out relevance cases.

The planned study requires blinded independent graded relevance judgements on a separate frozen scenario set. For an academic group with n candidates, k=min(3,n); declared exponential gain is 2^r−1 and rank discount is log2(i+1). nDCG@k=DCG@k/IDCG@k only when the candidate pool is fully judged and ideal gain is positive. Missing labels are not zero. Report small/unequal candidate pools and per-domain results instead of concealing them in one average.

No nDCG value is currently computed. Future feedback learning would require opt-in legitimate ratings, participant-separated development/test data, model versioning, privacy controls and audited updates. It is future work, not an automatic self-learning feature. The present comparison demonstrates executable, separated methods and their observed orders; it cannot support superiority without the missing judgement layer.
