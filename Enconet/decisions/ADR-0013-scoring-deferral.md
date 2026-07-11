# ADR-0013 — Scoring calibration is deliberately deferred to Gate G3

| Field | Value |
|---|---|
| Status | Accepted (deferral decision) |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet) |
| Register | Master plan §8 decision 2 |

## Context

`schemas/scoring_model.yml` (Task 1.5) defines rating weights, the score formula, rounding,
and classification thresholds. The structure can be built now, but the actual calibration
values determine every conformance score and belong to the human.

## Decision

Calibration is deferred: the owner will decide it at **Gate G3** (evaluation approval),
when a concrete proposal with plainly-explained options is presented (master plan Task 1.5
procedure).

## Consequences

- Task 1.5 builds the file structure with placeholder values marked
  `pending human calibration approval`; nothing downstream may treat those values as
  approved.
- The scoring benchmark fixture (Task 16.1) is locked only **after** calibration approval.
- No evaluation result is releasable (Gates G3–G6) before this deferral is resolved.
