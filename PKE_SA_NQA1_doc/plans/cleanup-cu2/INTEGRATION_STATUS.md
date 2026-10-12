# CU-2 integration status

CU-2 remains open. This batch adds a development candidate, not a released
framework or permission to move live files.

## What changed and why

`audit_template/prepare_framework_candidate_v4.py` reads the pinned v3 manifest
and checks every payload file before writing. It creates only a fresh tree.
Inside this workspace, that tree must be under `.tmp/`. It cannot overwrite
Enconet, Ekonerg, a scaffold, or an old release.

The builder moves working payload files into `work/` and adds the local v4
layout contract. It routes recognized script path expressions through that
contract. It does not do a blanket text replacement. Comments, evidence strings,
foreign roots and shadowed local roots stay unchanged. Each change is recorded
in the candidate manifest. Scripts are local copies, not sibling imports.

The candidate has 161 payload files; 23 scripts have routed expressions.
Its status is `development-only-not-installable`. Existing release selection
still works as before. No live supplier has a v4 configuration installed.

## Tests and evidence

Command, exit code **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu2/integration-tests.xml
```

Result: **58 passed**, no skips. This includes seven new candidate tests and
the 51 existing clean-up tests. Initial tests failed because the builder was
missing. One later assertion expected changed quote marks in unchanged text;
that assertion was corrected to check byte-preserving behavior.

The four supplier cases use `Atlas Engineering` and `Žuti dobavljač`, each with
and without a sibling supplier. Commands run from both the supplier folder and
its parent. They initialize an empty test database, register a test-only manual,
extract it, store its chapters, and validate the stored chunks. Derived files
and the raw-source registry land under `work/`. Incoming text is unchanged.
The sibling's content and modification time stay unchanged. No crumbs or audit
results are claimed by these tests. Six additional command help checks pass in
each setup; these are import/CLI checks, not proof of those workflows.

Two fresh candidate builds have equal manifests and payload hashes. A bad
baseline checksum and an existing destination are refused.

Candidate command, exit code **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe audit_template/prepare_framework_candidate_v4.py --destination .tmp/cleanup-v4-candidate-20261012
```

The generated tree stays in scratch storage and is not committed as a release.

The same read-only protected-file check recorded in
`Ekonerg/handoffs/2026-10-11T234114Z-cdb6634.md` was rerun with elevated read
access for the known restricted folders. Exit code **0**: **1,976 files**
checked, **zero hash mismatches** against the CU-1 baseline.

## What is still left

- Route configuration and string-valued paths without changing evidence text.
- Test the full sieving, evaluation, report and dashboard pipeline in isolation.
- Check reset and handoff behavior under the new layout.
- Finish direct `outputs/RUN-ID/` policy and standalone dashboard delivery.
- Finish Git/history and old empty-folder handling for safe live moves.
- Review the complete CU-2 batch before any authorized live migration.

No new task IDs, owner layout questions or per-file review gates were added.
The owner's layout approval remains valid. Old releases, live data, source
editions, approvals, scores and phase gates remain unchanged.
