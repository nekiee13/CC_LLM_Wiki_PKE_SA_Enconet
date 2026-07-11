# ADR-0006 — v1.3-CX becomes the canonical master plan

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner), on concurring recommendation of both agents |
| Scope | Project (Enconet) |
| Register | D-6 |

## Context

Three master-plan variants existed after the relocation preparation: the live
`MASTER_DEVELOPMENT_PLAN.md` (v1.1), `CC_MASTER_DEVELOPMENT_PLAN.md` (v1.2-CC proposed
revision), and `CX_MASTER_DEVELOPMENT_PLAN.md` (v1.3-CX reconciled candidate merging the
v1.2-CC changes plus dual-agent surfaces). Both agents verified v1.3-CX contains all
accepted changes.

## Decision

The v1.3-CX reconciled candidate becomes the canonical plan: it is published as
`MASTER_DEVELOPMENT_PLAN.md` (version 1.3) and the superseded variants are archived —
retained per ADR-0004 philosophy, never deleted.

## Consequences

- Publication executes in wave G1 (after G0 restores git, so the supersession is a
  recorded commit): rename candidate → `MASTER_DEVELOPMENT_PLAN.md`, move v1.1 content and
  `CC_MASTER_DEVELOPMENT_PLAN.md` to the archive.
- Exactly one live master plan exists afterwards; prefixed variants are review history.
- Plan amendments required by ADR-0009 (language policy) and ADR-0012 (scope ruling) are
  applied to the canonical plan as amendment A4 with a document-control log entry.
