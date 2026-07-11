# ADR-0011 — Evidence wiki pages are per-criterion (18), not per-crumb

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet) |
| Register | Master plan §8 decision 5 |

## Context

Evidence could be projected into the wiki as one page per criterion (18 pages) or one page
per crumb (hundreds). The wiki is the human-readable surface; the DB remains the complete
store either way.

## Decision

18 per-criterion evidence pages.

## Consequences

- `wiki/evidence/` holds 18 chunk-linked pages plus the coverage matrix (EPIC 9).
- Individual crumbs stay fully queryable in the DB and exports; no information is lost,
  only the wiki projection is coarser.
- If a specific criterion's page grows unmanageable, splitting it is a page-layout change,
  not a reversal of this decision.
