# Ekonerg permission-preserving directory recovery

Date: 12 October 2026. Task: CU-3.2. Codex implements; Claude reviews.
Prepared and tested, not applied. Owner live cleanup authority remains valid.
This finishes directory recovery tooling within the existing task, not a new task.

## What and why

Deleting and recreating a folder can lose its owner or access rules. The new
`scripts/cleanup_empty_homes.py` avoids that by renaming the original empty tree.
It never deletes a directory tree or changes its access rules.

Use the file wrapper with **no prune list**. Once its approved file moves are
complete, move the ten empty legacy roots with the directory tool. `backup`
goes to `work/backup`; the other nine roots go to
`work/migrations/cleanup-cu3-20261012/empty-original-homes/`.
The old browser-output folder stays inside the retained empty `out` tree.
This replaces the earlier parent-pruning/two-leaf-move proposal. Keeping empty
history under `work/migrations` supports recovery without cluttering the root.

The tool checks the named supplier, exact permitted homes, exact local recovery
destinations, path redirects and ownership boundaries. It requires Windows
same-volume native renames, which refuse existing destinations. No source,
database, agent tree or approval is changed. No Git changes are staged.

## Integrity and retry

Preparation records device/inode, mode, native attributes and a SHA-256 of the
Windows owner/group/DACL descriptor for every directory. Directory mtime is
excluded because approved file removals change it. New directories, different
owners/access rules, new files or changed directory identity are refused.
Auditing SACL settings are not fetched or separately verified. The original
filesystem object is retained; no descriptor is reconstructed or written.

Preparation can read a hash-pinned pending file map. Every file in a selected
legacy tree must be named there and match its hash. Apply still refuses every
tree containing any file. This allows one reviewed preparation packet before
the working-file move without permission to move nonempty directories.

The journal binds the root, exact plan and actual owner/reviewer references with
a checksum. It is flushed before the first rename. All trees are checked before
the first move. After each native rename, the full tree signature is checked.
Retry uses actual source/destination state. A partial or damaged journal record
is refused for review, not truncated. This is a cooperative single-writer tool.

Undo also checks the whole batch first. It refuses new owner files/folders and
returns each retained original tree to its old name. It preserves recovery
history and harmless empty destination parents. No recursive delete is used.

## Exact prepared scope

The fresh working-file proposal has **923 moves**, zero held/blocked rows and
zero source-hash changes against inventory. The extra row is the latest handoff.
The directory plan has **ten trees**, **128 directory witnesses** and **918
pending files** in those trees. Five other mapped files lie outside those roots.
The edited validation ledger still requires the reviewed preserve-edits option.

Canonical file-plan SHA-256:
`42a3230e4f512e70d5f53d9300c6ca22de063171e9502b194063c2f71da61e35`.
Canonical directory-plan SHA-256:
`4f4d833e2c015ad99ce6191782849bbd3900ccc26314980148793891cd4dd6fc`.
Directory-plan file byte SHA-256:
`63cfdbb26a866d6ca7d5ba75a7e476fc7f039d5b28527637d71c155072778778`.
Both plans are in [the preparation packet](ekonerg-native-directory-20261012/).

Preparation commands each exited **0**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe audit_template/prepare_supplier_cleanup_batch.py --supplier Ekonerg --destination PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-native-directory-20261012
C:/xPY/vEnv/WikiEnconet/python.exe scripts/cleanup_empty_homes.py --root C:/xPY/xPrj/LLM_Wiki/03_PKE_SA_NQA1 --mode prepare --supplier Ekonerg --run cleanup-cu3-20261012 --file-map PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-native-directory-20261012/file-map.json.zip --output PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-native-directory-20261012/directory-plan.json
```

The live read-only preview correctly exits **1**, `ready: false`, with nine
trees blocked because files remain. Backup alone is empty. This is an expected
refusal, not a readiness pass. Receipt: `blocked-before-file-moves.json`.
An unelevated preview also reported the cache ACL access restriction; the
approved elevated read confirms files remain, without changing any permissions.

## Tests

Tests were written first and initially failed because the module did not exist.
After implementation the native tests passed. The complete cleanup suite exited
**0: 124 passed**, no skips, in 124.66 seconds.
[Complete receipt](ekonerg-native-directory-tests.xml). Command:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_empty_homes.py scripts/tests/test_release_relocations.py audit_template/tests/test_supplier_runtime_install.py scripts/tests/test_cleanup_runtime_install.py audit_template/tests/test_supplier_cleanup_references.py audit_template/tests/test_project_records_v4.py audit_template/tests/test_supplier_layout_overlay.py audit_template/tests/test_project_scratch_v4.py scripts/tests/test_cleanup_workspace_batch.py scripts/tests/test_cleanup_workflow.py audit_template/tests/test_candidate_path_sweep_v4.py audit_template/tests/test_publication_paths_v4.py audit_template/tests/test_reset_operations_v4.py audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-native-directory-tests.xml
```

The final CLI refusal test and its fixture correction were added after that
suite started. The final focused command exited **0: nine passed**:

```text
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_empty_homes.py -q -p no:cacheprovider --tb=short
```

Tests use actual Windows native renames and owner/group/DACL reads. They cover
two company names, spaces and non-ASCII characters, repeat apply/undo, full-tree
identity and permission preservation, interrupted rename retry, pending-file
preparation without apply, new files/folders, simulated ACL drift, wrong approval
hashes, foreign destinations and nonzero blocked-preview exit. No POSIX support
is claimed.

A first full-suite command included a nonexistent test path and ran no tests.
It was corrected. The initial CLI test placement caused a fixture NameError;
that test-only error was corrected and the final nine tests passed. These
failures are not counted as successful validations.

## Review and execution order

Please include this last recovery component in the existing CU-3.2 safety review.
No separate per-file owner decision or new plan task is requested.

1. Refresh the current exact maps for any new handoffs. Prepare file workflow
   with no pruning and the explicit ledger preserve-edits list.
2. Bind file, directory and runtime plans to actual owner/reviewer references.
   Apply the reviewed file moves; verify their unchanged bytes and Git scope.
3. Confirm the legacy trees are empty and still match their captured signatures.
   Apply native directory renames, with separate bound journal/authorization.
4. Install the 39 reviewed runtime/config files, layout switch last, and the
   link-only canonical report while retaining the frozen original.
5. Run source/DB/hash checks, historical-manifest verification, standalone
   dashboards, browser/print, coordination and handoff checks.

Before commit, recovery order is runtime undo, directory undo, then file-workflow
undo. Restore original directory trees before returning their files; otherwise
new default-permission folders could replace the originals. Do not use undo
after a changed HEAD or a new owner file without explicit disposition.

No Claude review has arrived. No Ekonerg live file or directory move, runtime
installation, reset, source edit, score edit or Claude-infrastructure edit occurred.
The database hash remains `161c56ff5d457348ec6809c5e6dcc41e2dd09854d4e71cde11d12a2064d387c0`.
