# ADR-0004 — Historical context moves to an archive and is never deleted

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet), pattern applies to future entries |
| Register | D-4 |

## Context

`Enconet/docs/context/` holds session exports and source material spanning ~2 years of
project evolution, including obsolete paths and other projects' content. It is valuable
history ("hit & miss" record) but dangerous when mistaken for current instructions.

## Decision

Move the historical context to `Enconet/docs/_archive/context/`. **Never delete it** — it
is the recorded history of two years of project evolution.

## Consequences

- Executed as a reviewed migration **after G0** restores git (a pre-git move would be
  unrecoverable on error); references updated in the same change.
- Each archived file gets authority-catalog metadata (CC_ALIGNMENT_PLAN Task C1.1):
  classification + disposition.
- Archived content is exempt from controlled-doc gates (orphan/link checks) but remains
  indexed and searchable; jmunch doc profile tags it historical.
- Lessons distilled from the archive flow into `doc/LESSONS-LEARNED.md` with provenance links.
