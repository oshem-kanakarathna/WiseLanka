# Appendix E. Evidence index and terms

All paths below are relative to the repository root; the submitted electronic appendix should preserve them or provide an equivalent immutable archive.

| Claim | Evidence | Scope |
|---|---|---|
| 205 backend tests | docs/evidence/wp5/backend.log | Automated execution, not independent domain truth |
| 36 browser tests | docs/evidence/wp5/browser.log | Includes mocked speech/API states |
| Five real workflows | docs/evidence/wp5/live-original.log and live-wp1 through live-wp4.log | Local API/static server, real model |
| 14 reference cases | docs/evidence/wp5/scenarios.json and scenario-results.json | Implementer-authored synthetic profiles |
| Source-policy repair | docs/evidence/wp5/EDUCATIONAL_SOURCE_REVIEW.md; rule-evidence.csv | Selected sources, unknown provider evidence retained |
| Three ranking methods | docs/evidence/wp5/comparison.json | No independent labels or accuracy metric |
| Runtime/memory | docs/evidence/wp5/performance.json; runtime-network.json | Warm local sequential probes; whole-process RSS |
| Automated accessibility | docs/evidence/wp5/accessibility-final.json | Nine tested states and incomplete checks, not conformance |
| Fresh install/assets | docs/evidence/wp5/fresh-install.txt; provisioning-receipt.json; pip-check.log | One platform; cached browser binary reused |
| Repeat commands/exit codes | docs/evidence/wp5/verification.json; scripts/verify_wp5.py | 13 final checks, each exit0 |
| Data/model versions | docs/evidence/wp5/dataset-sha256.json; backend/app/relevance/model-lock.json | Frozen files, not assurance of future policy currency |
| Historical refinement | docs/evidence/wp1/ through wp4/; WP5 initial-failure logs | Earlier counts/outcomes superseded by final snapshot where corrected |

Measured = executed observation saved in the evidence snapshot. Synthetic = fictional input authored for evaluation. Mocked = simulated external/browser behaviour. Pending = no executed result exists. “MET” is the represented academic condition state, not confirmed admission. “AI relevance” identifies frozen pretrained inference, not a probability or ongoing learning.

Author-supplied personal reflection, supervision log, ethics approval and original signed declarations remain absent and must not be reconstructed from this technical appendix.
