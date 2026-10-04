# PIVOT-6 — DOC-0022 context-anchor pilot result

**Status:** candidate ready for review; not promoted

## What was tested

This controlled pilot applies the context-anchor contract to DOC-0022,
`PQ08.3-1_r4_Kontrola_studijskih_projektnih_radova_.md`. The document covers
Ekonerg study and design work, so it is a useful engineering-focused test of the
audit framework.

## Run result

Candidate run: `RUN-20261004-45`  
Previous active run: `RUN-20261003-38`

| Check | Result |
|---|---:|
| Input items | 14 |
| Imported crumbs | 14 |
| Quote links | 21/21 |
| Unmatched quotes | 0 |
| Field completeness | 100% for source, statement, item type, quote, and language |
| Candidate status | inactive (`candidate`) |
| Active run | `RUN-20261003-38` remains active |

The crumb count and statements are unchanged from the active generation. The pilot
adds context anchors only.

## Context-anchor result

All 14 candidate crumbs have a context row:

- 9 are typed `policy_or_procedure`;
- 1 is typed `design_input`;
- 1 is typed `design_verification`;
- 2 are typed `objective_record`;
- 1 is typed `candidate_lead`;
- all 14 carry `source_revision=4`.

The evidence types come from each fixture item's existing `item_type`. No project,
contract, supplier, or evidence date was inferred. The one candidate lead remains a
lead and is not treated as positive audit evidence.

## Safety and decision state

The candidate is inactive and has not changed the audit score, findings, or
conclusions. Promotion still requires the normal golden-score and human-approval
gates.

## Artifacts

- Metrics: `sieving/runs/RUN-20261004-45/metrics.json`
- Diff: `sieving/runs/RUN-20261003-38-to-RUN-20261004-45.json`
- Corrected input: `sieving/DATA/production/2026-10-04/q13_doc0022_context_pilot.json`

