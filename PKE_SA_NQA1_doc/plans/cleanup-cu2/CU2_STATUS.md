# CU-2 tooling foundations — candidate, not installed

The shared path helper and file migration engine now exist and have fixture
tests. **CU-2 is still open:** existing runtime commands have not yet been
routed through this helper. No live folder has moved.

Owner layout decision `OWNER-LAYOUT-20261012-CLEANUP` remains valid. Do not ask
for the layout choice again. Tool safety review and exact batch authority are
separate from that decision.

## What is implemented

### Local path contract

Source: `audit_template/runtime_v4/project_layout.py`.

Copy this helper into each supplier's `scripts/` in the future v4 release.
It derives that supplier's root from its own file, not the caller's working
directory, another supplier, or an ancestor search.

It requires a local `project-layout.json`, with an explicit `legacy` or `v4`
mode. There is no silent fallback. v4 routes working records to `work`, plans
to `docs/plans`, handoffs to coordination, and results to `outputs/RUN-...`.
Source, database and sieving locations stay unchanged.

Both old and new working homes present at once are refused. `docs` and its
own `docs/plans` child are not a mixed layout. Path escape, redirected paths,
hardlinks, unknown keys and bad run IDs fail closed.

Tests copy the helper into two synthetic suppliers with spaces/non-ASCII
letters, both with and without a sibling. The command works from a foreign
working directory and leaves that sibling unchanged. No local copy or v4
config was installed in Enconet, Ekonerg or the six future suppliers.

### File migration engine

Source: `scripts/cleanup_migration.py`.

- Default `preview` reads and checks only. `verify` also does not write.
- `apply` requires a supplied authorization bound to the exact root and
  canonical map hash, with owner and review decision references.
- There is no production authorization factory or fixture bypass flag.
  Synthetic authorization records exist only inside disposable tests.
- Held/Claude-owned rows, protected audit/Git/agent homes, changed hashes,
  missing files, duplicate destinations, reparse paths and hardlinks fail.
  Case variants and Windows trailing-dot/space aliases cannot bypass guards.
- Source files are moved without overwrite. Windows uses native no-replace
  rename; same-volume file identities and read-only attributes are preserved.
- A durable journal is created before moving files. Its header binds the root,
  map, supplied authority, source identities and new-directory scope. A header
  checksum detects accidental edits; it is not a cryptographic signature.
- After interruption, resume checks actual files, hashes and identities. A
  complete batch needs an `apply-complete` record, not just missing sources.
- A torn journal tail is retained, not rewritten; apply/undo append a recovery
  marker with a suffix hash. Verify flags the incomplete tail without repair.
- Undo preflights the whole batch, then moves only matching records back. It
  refuses changed owner files. It removes only recorded empty new directories;
  nonempty directories with user files are retained and reported.

This is a cooperative, single-writer tool. It does not authenticate human
identities or defeat an attacker replacing paths between checks. A controlled
authorization must come from real owner/reviewer decisions, not made-up IDs.
No real apply authorization has been created for the workspace.

The engine does not perform database migrations, script path rewrites, Git
staging, directory moves, recursive deletion or audit resets. Tracked move
history must be recorded correctly by the later orchestration/Git step.

## Test evidence

```powershell
C:/xPY/vEnv/WikiEnconet/python.exe -m pytest scripts/tests/test_cleanup_migration.py audit_template/tests/test_project_layout_v4.py scripts/tests/test_cleanup_inventory.py scripts/tests/test_compile_cleanup_map.py -q -p no:cacheprovider --tb=short --junitxml=PKE_SA_NQA1_doc/plans/cleanup-cu2/focused-tests.xml
```

Final result: **exit 0, 51 passed, no skips**. This includes 34 new
migration/layout cases and 17 prior inventory/map cases.
The first coordination status recorded 49 passes at that time. Two final
cases for missing-source and foreign-root authority bring the saved result to 51.

Tests include preview read-only checks, the full CLI sequence in a disposable
fixture, apply retry, undo, missing/unbound authority, wrong root/map, collisions,
held files, source changes, read-only attributes, interruption after a move,
partial batch failure, incomplete journal writes, changed journal headers,
new user files, existing hardlinks and simulated Windows reparse attributes.

TDD failures were observed and fixed: missing implementation (RED), parent-file
collisions, empty-map false success, the nested docs/plans mixed-layout check,
torn journal recovery and altered header acceptance. Verification was also
checked to ensure it does not repair or write journals.

All **1,976 CU-1 protected-file hashes** were independently rechecked after the
tests: zero mismatches. The sandbox denied a historical test-artifact read;
the elevated read-only retry completed. No source text or DB data was copied
into this packet.

Not run: live preview/apply/undo, full audit/browser regression, native junction
creation tests, or execution of the POSIX link/unlink fallback. All apply/undo
operations above used disposable Windows fixtures. No such omitted check is
reported as passed.

## Remaining CU-2 work — no new slices

1. Route the existing intake, chunking, sieving, approvals, reset, report,
   export, handoff and test tools through the local path contract. Do this in
   the candidate release, not by patching every live company separately.
2. Bind safe file moves to reviewed batches and retained-history path lookup.
   Add the tracked-file Git and old-empty-directory handling needed by CU-3.
3. Run the required isolated normal-command and pipeline checks in the new
   layout. Review the completed CU-2 batch once before live application.

The live audits and immutable v1/v2/v3 releases remain unchanged. CU-3 cannot
start merely because these foundations pass their unit tests.
