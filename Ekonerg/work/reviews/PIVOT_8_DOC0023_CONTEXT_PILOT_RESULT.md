# PIVOT-8 — DOC-0023 context-anchor pilot result

**Status:** candidate ready for review; not promoted

## What was tested

This controlled pilot applies the context-anchor contract to DOC-0023,
`PQ08.4-1_r3_Kontrola_studijskih_projektnih_radova_.md`. The document covers a
study and project-work control process.

## Run result

Candidate run: `RUN-20261004-47`  
Previous active run: `RUN-20261003-19`

| Check | Result |
|---|---:|
| Input items | 6 |
| Imported crumbs | 6 |
| Quote links | 9/9 |
| Unmatched quotes | 0 |
| Field completeness | 100% for source, statement, item type, quote, and language |
| Candidate status | inactive (`candidate`) |
| Active run | `RUN-20261003-19` remains active |

The crumb count and statements are unchanged from the active generation. The pilot
adds context anchors only.

## Context-anchor result

All 6 candidate crumbs have a context row:

- 5 are typed `policy_or_procedure`;
- 1 is typed `objective_record`;
- all 6 carry `source_revision=3`.

The evidence types come from each fixture item's existing `item_type`. No project,
contract, supplier, or evidence date was inferred.

## Safety and decision state

The candidate is inactive and has not changed the audit score, findings, or
conclusions. Promotion still requires the normal golden-score and human-approval
gates.

## Artifacts

- Metrics: `sieving/runs/RUN-20261004-47/metrics.json`
- Diff: `sieving/runs/RUN-20261003-19-to-RUN-20261004-47.json`
- Corrected input: `sieving/DATA/production/2026-10-04/q07_doc0023_context_pilot.json`

