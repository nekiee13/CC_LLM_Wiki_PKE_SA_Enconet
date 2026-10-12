# MIN-2.2: fresh corrected scope-two candidates

## Owner decision

The owner explicitly rejected the two flawed inactive candidates. They remain
in the database for history and are not used:

| Rejected run | Decision reference |
|---|---|
| `RUN-20261005-61` (DOC-0016) | `REJECT-DOC0016-RUN-20261005-61-20261006-OWNER` |
| `RUN-20261005-66` (DOC-0021) | `REJECT-DOC0021-RUN-20261005-66-20261006-OWNER` |

## Fresh imports

The corrected JSON files were imported as new, inactive database generations.
No active generation was edited or replaced.

| Document | Fresh run | Items | Links | Quote verification | Previous active |
|---|---|---:|---:|---:|---|
| DOC-0016 | `RUN-20261006-67` | 28 | 28 | 28/28 (100%) | `RUN-20261004-49` |
| DOC-0021 | `RUN-20261006-68` | 21 | 25 | 25/25 (100%) | `RUN-20261004-42` |

The DOC-0021 link count is 25 because some crumbs contain multiple quotes; the
candidate still contains 21 items.

## Verification artifacts

- Fresh run metrics and diffs are under
  `sieving/runs/RUN-20261006-67/` and `sieving/runs/RUN-20261006-68/`.
- Exported fresh generations:
  `out/2026-10-06/RUN-20261006-67.json` and
  `out/2026-10-06/RUN-20261006-68.json`.
- Draft golden scores:
  `out/2026-10-06/RUN-20261006-67-score.json` and
  `out/2026-10-06/RUN-20261006-68-score.json`.
- Draft-only scores found 0 missed and 0 spurious items for both. They remain
  `promotion_ready=false` because the golden fixtures have no human approval.

Aggregate validation passed. Evaluation, findings, and report phases remain
skipped by the current project phase gate; this candidate task does not change
that gate.

## Next gate

Claude and the owner must review and approve the two golden fixtures. A
separate owner decision is still required before either fresh candidate can be
promoted. Until then, the active runs and dashboard stay on their current
generations.
