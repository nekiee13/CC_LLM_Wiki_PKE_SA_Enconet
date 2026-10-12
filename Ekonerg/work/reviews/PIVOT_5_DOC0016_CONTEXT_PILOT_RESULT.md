# PIVOT-5 — DOC-0016 context-anchor pilot result

**Status:** candidate ready for review; not promoted

## Run result

After the owner-approved rejection of stale candidate `RUN-20261004-43`, the
corrected pilot was applied as `RUN-20261004-44`.

| Check | Result |
|---|---:|
| Input items | 12 |
| Imported crumbs | 12 |
| Quote links | 12/12 |
| Unmatched quotes | 0 |
| Field completeness | 100% for source, statement, item type, quote, and language |
| Candidate status | inactive (`candidate`) |
| Active run | `RUN-20261003-40` remains active |

The first candidate was rejected with approval reference
`PIVOT-5-REJECT-20261004-OWNER`. Its record remains in the database for traceability.

## Context-anchor result

All 12 candidate crumbs have a context row:

- 10 are typed `policy_or_procedure`;
- 2 are typed `candidate_lead`;
- all 12 carry `source_revision=10`;
- no project, contract, supplier, or evidence date was inferred.

The anchors add traceability. They do not upgrade candidate leads into positive audit
evidence.

## Scope and safety

This is a controlled pilot of one vendor document. It does not change the active audit
generation, audit score, findings, or conclusions. Promotion requires the normal
golden-score and human-approval gates.

## Artifacts

- Metrics: `sieving/runs/RUN-20261004-44/metrics.json`
- Diff: `sieving/runs/RUN-20261004-44/diff-RUN-20261003-40-to-RUN-20261004-44.json`
- Corrected input: `sieving/DATA/production/2026-10-04/q09_doc0016_context_pilot_corrected.json`

