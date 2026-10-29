# Appendix D. Observed ranking comparison

These are top-three IDs from the saved WP5 method outputs, not relevance judgements. Group sizes and academic status must accompany interpretation; full orders/scores remain in comparison.json. All profiles are synthetic. Cold-start ties can be identical across methods.

| Case | Grouped deterministic top 3 | TF–IDF top 3 | Semantic top 3 |
|---|---|---|---|
| empty | PRG0001, PRG0002, PRG0003 | PRG0001, PRG0002, PRG0003 | PRG0001, PRG0002, PRG0003 |
| it_literal | PRG0001, PRG0002, PRG0003 | PRG0002, PRG0009, PRG0008 | PRG0002, PRG0003, PRG0001 |
| it_paraphrase | PRG0001, PRG0002, PRG0003 | PRG0002, PRG0008, PRG0001 | PRG0002, PRG0003, PRG0001 |
| business | PRG0008, PRG0001, PRG0009 | PRG0008, PRG0001, PRG0009 | PRG0008, PRG0001, PRG0009 |
| engineering | PRG0001, PRG0002, PRG0003 | PRG0009, PRG0008, PRG0001 | PRG0009, PRG0003, PRG0008 |
| unmet_engineering | PRG0008, PRG0001, PRG0002 | PRG0008, PRG0009, PRG0001 | PRG0008, PRG0009, PRG0003 |
| missing_evidence | PRG0008, PRG0009, PRG0001 | PRG0009, PRG0008, PRG0001 | PRG0009, PRG0008, PRG0003 |
| unfamiliar | PRG0001, PRG0002, PRG0003 | PRG0001, PRG0002, PRG0003 | PRG0003, PRG0001, PRG0009 |
| vocational | PRG0001, PRG0002, PRG0003 | PRG0007, PRG0008, PRG0001 | PRG0010, PRG0004, PRG0011 |

Independent labels: unavailable. nDCG@3: not computed. These orders cannot establish educational accuracy, quality uplift or satisfaction. The full [comparison](../../evidence/wp5/comparison.json) records the catalogue hash and per-candidate statuses; [protocol](../../evidence/wp5/AI_EVALUATION_PROTOCOL.md) describes blinded evaluation and leakage controls.
