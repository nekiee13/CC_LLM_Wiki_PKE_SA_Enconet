# MIN-2.2: corrected generations promoted

The owner approved promotion. Before activation, the read-only reconciliation
mapped all 24 downstream evidence links (12 for each document) with no missing,
ambiguous, or colliding mappings. The owner-approved promotion references were
used for the controlled apply and promotion steps.

## Final generation state

| Document | Previous active | New active | Evidence links remapped | Decision reference |
|---|---|---|---:|---|
| DOC-0016 | `RUN-20261004-49` | `RUN-20261006-67` | 12 | `PROMOTE-DOC0016-RUN-20261006-67-20261006-OWNER` |
| DOC-0021 | `RUN-20261004-42` | `RUN-20261006-68` | 12 | `PROMOTE-DOC0021-RUN-20261006-68-20261006-OWNER` |

The old generations are retained as `superseded`. The rejected flawed
generations remain `rejected`. The fresh generations are now `active`.

## Validation

- Approved golden scores: DOC-0016 28/28; DOC-0021 21/21; zero missed and zero
  spurious items.
- Active-only traceability validation passed.
- Aggregate validation passed. Evaluation, findings, and report phases remain
  skipped by the current project phase gate.
- Dashboard outputs were rebuilt under `out/2026-10-06/`.
- Targeted sieve-generation test passed with a project-local temp directory.

The reconciliation and promotion changed only the downstream evidence links
and generation state required for the approved transition. No source documents
or crumb text were modified.
