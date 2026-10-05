# Ekonerg DOCUMENT v3 rerun — 2026-10-05

## Result

All 24 Ekonerg vendor-document payloads were prepared with the owner-approved
`appb_document_v3_context_anchors` prompt. The old generations were kept.

- 24/24 v3 payloads passed strict JSON validation.
- 17/24 v3 candidates were imported into the local database.
- 15/17 imported candidates have complete quote linking.
- 2/17 imported candidates have one unmatched quote each; they remain inactive
  and are not promotion-ready.
- 7/24 payloads are held because an earlier inactive candidate already exists.
- No v3 candidate was promoted, and no audit score or evaluation was changed.

The v3 preparation keeps prior source-quoted crumbs and adds only
source-supported `candidate_lead` items from the v3 concept sweep. A candidate
lead is a review clue, not a conformance decision.

## Candidate locations

- Payloads: `sieving/candidates/v3-20261005/DOC-*.json`
- Source and payload hashes: `sieving/candidates/v3-20261005/manifest.json`
- Imported run evidence: `sieving/runs/RUN-20261005-53` through
  `RUN-20261005-76` (only runs listed below were created)
- Reproducible preparation script: `scripts/rerun_document_v3_candidates.py`

## Per-document status

| Document | v3 run | Status | Crumbs | Note |
|---|---|---:|---:|---|
| DOC-0008 | RUN-20261005-53 | candidate | 17 | quote-complete |
| DOC-0009 | RUN-20261005-54 | candidate | 12 | quote-complete |
| DOC-0010 | RUN-20261005-55 | candidate | 13 | quote-complete |
| DOC-0011 | — | held | 24 payload | earlier candidate RUN-20261005-52 |
| DOC-0012 | RUN-20261005-57 | candidate | 20 | quote-complete |
| DOC-0013 | RUN-20261005-58 | candidate | 22 | quote-complete |
| DOC-0014 | RUN-20261005-59 | candidate | 17 | quote-complete |
| DOC-0015 | RUN-20261005-60 | candidate | 15 | quote-complete |
| DOC-0016 | RUN-20261005-61 | candidate | 28 | 27/28 quotes linked |
| DOC-0017 | RUN-20261005-62 | candidate | 17 | quote-complete |
| DOC-0018 | RUN-20261005-63 | candidate | 15 | quote-complete |
| DOC-0019 | — | held | 11 payload | earlier candidate RUN-20261003-16 |
| DOC-0020 | — | held | 22 payload | earlier candidate RUN-20261004-46 |
| DOC-0021 | RUN-20261005-66 | candidate | 21 | 24/25 quotes linked |
| DOC-0022 | — | held | 24 payload | earlier candidate RUN-20261004-45 |
| DOC-0023 | — | held | 15 payload | earlier candidate RUN-20261004-47 |
| DOC-0024 | — | held | 22 payload | earlier candidate RUN-20261004-48 |
| DOC-0025 | RUN-20261005-70 | candidate | 22 | quote-complete |
| DOC-0026 | RUN-20261005-71 | candidate | 10 | quote-complete |
| DOC-0027 | — | held | 29 payload | earlier candidate RUN-20261003-08 |
| DOC-0028 | RUN-20261005-73 | candidate | 21 | quote-complete |
| DOC-0029 | RUN-20261005-74 | candidate | 23 | quote-complete |
| DOC-0030 | RUN-20261005-75 | candidate | 20 | quote-complete |
| DOC-0031 | RUN-20261005-76 | candidate | 32 | quote-complete |

## Coverage signal

The imported v3 candidates add source-supported leads for the previously empty
areas. Across the 17 imported runs, the new candidate counts are:

| Criterion | Candidate crumbs |
|---|---:|
| Appendix B VIII | 35 |
| Appendix B IX | 15 |
| Appendix B XI | 42 |
| Appendix B XIII | 49 |
| Appendix B XIV | 59 |

These counts do not mean the requirements are met. They show where the source
text contains a clue that needs audit review and objective records.

## Validation

- `python scripts/validate_schemas.py --no-record` — exit 0.
- `python scripts/check_sieve_coverage.py --db db/nqa_audit.sqlite --document-side DOCUMENT` — exit 0; all 24 documents retain active crumbs.
- `python scripts/validate_traceability.py --db db/nqa_audit.sqlite --active-only --no-record` — exit 0.
- `python scripts/validate_sieving_harness.py --db db/nqa_audit.sqlite --allow-pending-claude` — exit 0; golden calibration remains a human-approval gate.
- `python -m pytest sieving/tests/test_prompt_registry.py -q` — 5 passed.

The complete sieving test suite was attempted but is not a clean gate in this
Windows workspace: it produced 90 failures and 134 permission-related errors
while cleaning temporary test folders. That result is recorded as failed, not
silently treated as a pass.

## Next action

Review the 17 inactive v3 candidates, resolve the two unmatched quotes, and
obtain decisions for the seven older candidates before importing their v3
payloads. Promotion still requires the existing golden-set and owner approval
gates.
