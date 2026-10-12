# PIVOT-7 — DOC-0020 context-anchor pilot result

**Status:** candidate ready for review; not promoted

## What was tested

This controlled pilot applies the context-anchor contract to DOC-0020,
`PQ08.2-1_r6_Odnosi_s_Naručiteljima.md`. The document covers customer and contract
relations, including nonconformance and corrective-action controls.

## Run result

Candidate run: `RUN-20261004-46`  
Previous active run: `RUN-20261003-36`

| Check | Result |
|---|---:|
| Input items | 12 |
| Imported crumbs | 12 |
| Quote links | 14/14 |
| Unmatched quotes | 0 |
| Field completeness | 100% for source, statement, item type, quote, and language |
| Candidate status | inactive (`candidate`) |
| Active run | `RUN-20261003-36` remains active |

The crumb count and statements are unchanged from the active generation. The pilot
adds context anchors only.

## Context-anchor result

All 12 candidate crumbs have a context row:

- 6 are typed `policy_or_procedure`;
- 3 are typed `objective_record`;
- 1 is typed `nonconformance`;
- 2 are typed `corrective_action`;
- all 12 carry `source_revision=6`.

The evidence types come from each fixture item's existing `item_type`. No project,
contract, supplier, or evidence date was inferred.

## Safety and decision state

The candidate is inactive and has not changed the audit score, findings, or
conclusions. Promotion still requires the normal golden-score and human-approval
gates.

## Artifacts

- Metrics: `sieving/runs/RUN-20261004-46/metrics.json`
- Diff: `sieving/runs/RUN-20261003-36-to-RUN-20261004-46.json`
- Corrected input: `sieving/DATA/production/2026-10-04/q11_doc0020_context_pilot.json`

