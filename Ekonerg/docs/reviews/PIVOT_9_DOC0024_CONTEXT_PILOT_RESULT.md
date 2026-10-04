# PIVOT-9 — DOC-0024 context-anchor pilot result

**Status:** candidate ready for review; not promoted

## What was tested

This controlled pilot applies the context-anchor contract to DOC-0024,
`PQ08.4-2_r9_Kontrola_nabave.md`. The document covers procurement controls.

## Run result

Candidate run: `RUN-20261004-48`  
Previous active run: `RUN-20261003-17`

| Check | Result |
|---|---:|
| Input items | 7 |
| Imported crumbs | 7 |
| Quote links | 14/14 |
| Unmatched quotes | 0 |
| Field completeness | 100% for source, statement, item type, quote, and language |
| Candidate status | inactive (`candidate`) |
| Active run | `RUN-20261003-17` remains active |

The crumb count and statements are unchanged from the active generation. The pilot
adds context anchors only.

## Context-anchor result

All 7 candidate crumbs have a context row:

- 6 are typed `policy_or_procedure`;
- 1 is typed `objective_record`;
- all 7 carry `source_revision=9`.

The evidence types come from each fixture item's existing `item_type`. No project,
contract, supplier, or evidence date was inferred.

## Safety and decision state

The candidate is inactive and has not changed the audit score, findings, or
conclusions. Promotion still requires the normal golden-score and human-approval
gates.

## Artifacts

- Metrics: `sieving/runs/RUN-20261004-48/metrics.json`
- Diff: `sieving/runs/RUN-20261003-17-to-RUN-20261004-48.json`
- Corrected input: `sieving/DATA/production/2026-10-04/q07_doc0024_context_pilot.json`

