# CU-2 publication and reset status

The isolated v4 audit now passes the full dashboard-ready validation spine and
can seal its results without copying or changing them. CU-2 remains open for
the remaining path-use sweep, Git/history handling and migration review.
No live supplier has been changed or moved.

## What changed and why

- Aggregate validation reads the report, data, bundle and dashboard directly
  from `outputs/RUN-ID/`, using the selected run identity.
- Catalog and portable review-package tools default to `work/reviews/`.
  These are internal validation/review artifacts. The user-facing light and
  dark dashboards stay standalone. No theme chooser is required.
- First-copy publication uses approvals and release receipts under
  `work/manifests/`. Artifact destinations must be directly under the contract's
  own run folder, not a flat output, sibling run, nested candidate tree or wiki copy.
- An explicit contract whose artifact source/destination pairs are all identical
  selects **seal-existing-snapshot**. This solves the normal v4 case: generated
  reports already sit in their final run folder. Sealing checks the same G5/G6
  decisions and hash-pinned owner exception, runs the full projected aggregate,
  rechecks hashes, and creates the release marker last without an overwrite.
  It never rewrites or deletes the existing snapshot artifacts.
- Reset handles Windows read-only files only after its existing external-plan,
  confirmation and fingerprint checks. It changes the flag on one named target,
  not folder ACLs. If deletion fails, it restores the flag on that same file.
  Incoming files, code, decisions, reviews and history remain outside reset.

These are candidate-runtime changes. They do not approve any real publication,
reset, regulatory edition, score or source intake. Claude review may follow later.

## Validation

Command, exit code **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu2/publication-tests.xml
```

**72 passed**, no skips. This includes the earlier 64 tests and eight publication
or deletion-operation cases. The two reset apply cases now include a real
read-only flag on a synthetic registered raw file, with and without a backup.
The earlier Windows deletion failure was reproduced before the fix.

Each of the four synthetic supplier audits now checks catalog generation,
portable-package validation, browser size/performance/security budgets, and
publication via the real CLI with the projected dashboard-ready aggregate.
All validators in that phase run; no validator was removed or relabeled as passed.
The run's existing artifact hashes remain unchanged after sealing, and a repeat
publication is refused. Both names still work with and without a sibling supplier.

Additional cases check:

- Missing publication approvals are refused, and preview writes no output.
- First-copy apply works; failed validation rolls back only files it created.
- Snapshot sealing succeeds or refuses failed validation/changed artifact bytes.
- A release-marker permission failure removes only the new marker and leaves
  every existing artifact alone. A simulated owner edit is retained.
- Failed deletion restores the read-only flag and bytes.
- Directory and hard-linked deletion targets are refused.

The protected-file check recorded in
`Ekonerg/handoffs/2026-10-11T234114Z-cdb6634.md` was rerun with elevated read
access for known restricted folders. Exit code **0**: **1,976 files checked,
zero hash mismatches**. Old releases and both live audit databases are intact.
Test data and test-only approvals are not real vendor evidence or owner decisions.

## What remains

1. Sweep the remaining configuration, dispatcher and other path users.
2. Complete Git/history and old empty-folder handling for reversible live moves.
3. Review the coherent CU-2 batch before any authorized installation or move.

The owner's layout choice does not need another decision. No new plan tasks or
per-file slices were added. Native live moves and live publication/reset remain
**not run**. This closes the prior packet's read-only reset and aggregate/catalog/
publication test gaps, not the entire clean-up plan.
