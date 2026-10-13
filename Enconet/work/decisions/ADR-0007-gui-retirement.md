# ADR-0007 — No standalone sieving GUI (backfilled record)

| Field | Value |
|---|---|
| Status | Accepted (backfilled — original decision 2026-07-04) |
| Date | 2026-07-04 (decision) / 2026-07-11 (this record) |
| Decided by | Human (project owner) |
| Scope | Project (Enconet sieving subsystem) |
| Register | pre-dates the D-register; backfill per CC_ALIGNMENT_PLAN Task C5.1 |

## Context

The vendored JSON Extractor originally shipped a Streamlit review GUI (`app.py`,
`adapters/`). At vendoring (2026-07-04) the human decided sieving would be operated
through project scripts and slash commands, and reviewed through generated reports, wiki
pages, DB queries, and CSV/XLSX exports.

## Decision

Sieving has **no separate GUI**. The Streamlit adapter was removed at vendoring
(recoverable from upstream history; see `sieving/PROVENANCE.md` divergence log).

## Consequences

- Existing evidence of the decision: `sieving/PROVENANCE.md`, master plan EPIC 15,
  `Sieving_method_specification_Guide.md` §10.1.
- Stale GUI references in `README.md`, `QUICKSTART.md`, `PROJECT_INFO.md`, and archived
  tools are documentation defects, not open questions (cleanup: CC_ALIGNMENT_PLAN C4.5).
- Reintroducing any GUI requires a superseding ADR.
