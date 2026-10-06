# MIN-2.2: promotion blocked by downstream evidence

The owner approved promotion of both fresh corrected candidates:

- DOC-0016: `RUN-20261006-67`
- DOC-0021: `RUN-20261006-68`

The guarded `sieve_generation.py promote` command was run for each candidate
with its owner decision reference and approved score. Both attempts failed
safely with:

`generation change refused after downstream evaluation evidence exists`

No active generation, rating, dashboard, or generation event was changed.

Current state:

| Document | Active generation | Approved candidate | Candidate state |
|---|---|---|---|
| DOC-0016 | `RUN-20261004-49` | `RUN-20261006-67` | inactive candidate |
| DOC-0021 | `RUN-20261004-42` | `RUN-20261006-68` | inactive candidate |

The owner approvals are recorded in `manifests/approvals.csv`, but they do not
override the downstream-evidence safety guard. A separate, tested reconciliation
decision is needed before promotion can be retried. No evidence rows were
deleted or rewritten.
