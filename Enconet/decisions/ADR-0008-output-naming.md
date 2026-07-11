# ADR-0008 — Output naming: `<supplier>_<framework>_<artifact>`, framework label `appendix_b`

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet), pattern reusable by future entries |
| Register | Master plan §8 decision 1 |

## Context

Generated deliverables are named `<supplier>_appendix_b_<artifact>` (e.g.
`enconet_appendix_b_evaluation_report.md`). The owner confirmed the labeling with a
forward-looking qualification: today only Appendix B evaluation is performed, but more
evaluation frameworks are expected — ISO 9001 is a candidate once the Appendix B framework
reaches a mature state.

## Decision

- Supplier code for the first production run: `enconet`.
- The framework label (`appendix_b`) is an explicit naming component:
  `<supplier>_<framework>_<artifact>`. The scheme accommodates future frameworks
  (e.g. `<supplier>_iso9001_<artifact>`) without renaming existing outputs.

## Consequences

- The evaluation engine treats the framework label as a parameter alongside `<supplier>`
  (naming only for now — no ISO 9001 implementation is scheduled until Appendix B matures).
- Adding a new framework is a future scope decision with its own taxonomy/schema contracts;
  this ADR only guarantees the naming scheme won't need to change.
