# ADR-0010 — SQLite is the committed database engine

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet), pattern applies to future entries |
| Register | Master plan §8 decision 4 |

## Context

Context doc 30 said "for example sqlite"; the master plan (EPIC 2) fixed SQLite pending
confirmation. SQLite is a single-file, serverless database — appropriate for a
single-machine audit project whose DB is a rebuildable derived artifact.

## Decision

SQLite is confirmed as the committed choice for the controlled data backbone
(`db/nqa_audit.sqlite`, `db/schema.sql`).

## Consequences

- EPIC 2 proceeds as planned: DDL schema, FK enforcement (`PRAGMA foreign_keys = ON`),
  idempotent initializer, single access helper.
- `db/*.sqlite-journal` and similar artifacts stay in `.gitignore`; whether the `.sqlite`
  file itself is tracked follows the derived-artifact rule (rebuildable from raw + scripts),
  to be fixed in EPIC 2 acceptance.
