# ADR-0003 — Canonical schema contracts start inside Enconet

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet) |
| Register | D-3 |

## Context

The APP_B taxonomy, canonical codes, enums, and column schema are duplicated across
`config.py`, `templates/app_b.py`, the sieving prompts, and documentation. Consolidation
needs one machine-readable owner; the open question was its location — `Enconet/schemas/`
or workspace level.

## Decision

`Enconet/schemas/*.yml` is the canonical owner (per master plan EPIC 1). Runtime code,
prompt checks, and generated documentation load from it.

## Consequences

- CC_ALIGNMENT_PLAN Task C4.4 dedups `config.py`/`app_b.py` against this owner; the spec
  guide §10.1 misstatement is corrected in the same change (Task C1.4).
- Promotion to workspace scope happens only when a second project reuses the exact same
  contract, and requires a superseding ADR.
