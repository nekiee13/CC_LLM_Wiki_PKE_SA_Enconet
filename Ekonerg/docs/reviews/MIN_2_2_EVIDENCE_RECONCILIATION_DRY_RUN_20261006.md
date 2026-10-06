# MIN-2.2: downstream evidence reconciliation dry run

Promotion is blocked because existing evaluation evidence points to the old
active crumb IDs. A new read-only reconciliation tool was added and run in
dry-run mode. It does not edit the database.

| Document | Old active | New candidate | Mapped crumbs | Downstream links | Missing | Ambiguous | Collisions | Ready |
|---|---|---|---:|---:|---:|---:|---:|---|
| DOC-0016 | `RUN-20261004-49` | `RUN-20261006-67` | 12 | 12 | 0 | 0 | 0 | yes |
| DOC-0021 | `RUN-20261004-42` | `RUN-20261006-68` | 12 | 12 | 0 | 0 | 0 | yes |

The mapping uses the same criterion and normalized control statement. It found
one unambiguous replacement for every old evidence link. No evaluation rows,
ratings, gaps, or active generations were changed.

Dry-run records:

- `out/2026-10-06/reconcile-doc0016-dry-run.json`
- `out/2026-10-06/reconcile-doc0021-dry-run.json`

The apply operation requires an explicit `--apply --decision-ref` and will only
update the 24 listed `evaluation_evidence.item_id` links. It refuses incomplete,
ambiguous, or colliding mappings. Promotion must still run after reconciliation,
and both steps require recorded decisions.
