# CU-4.2 verification and retained exceptions

Date: 14 October 2026 (owner local date). Status: **partial**.
This completes the shared-index rebuild and root scratch dispositions within
the existing task. It does not claim that every held file or legacy directory
has been moved. No epic, task or audit gate was added.

## Shared indexes — rebuilt and verified

Source commit: `e4201491241e5d139c9b5d1ebafa4ca3ca210f72`.
One `INDEX-REFRESH` claim covered all four canonical indexes. No agent-owned
index was rebuilt. The three doc indexes retain their names and use a retained
clean sparse worktree under `.tmp/index-source-e4201491241e/`. Logical roots
are still `Enconet/` and `PKE_SA_NQA1_doc/`. The physical-root change is explicit
in `PKE_SA_NQA1_doc/INDEXING.md`; do not remove the snapshot while these indexes
refer to it. The snapshot excludes both agents' infrastructure and all CC files.
Owner edits in the live tree were neither stashed nor copied into the corpus.

| Canonical index | Files | Sections/symbols | Verified clean | Structural skips |
|---|---:|---:|---:|---:|
| `local/PKE_SA_NQA1_Enconet_docs` | 249 | 2,965 sections | 2,854 | 111 |
| `local/PKE_SA_NQA1_Enconet_controlled` | 238 | 2,362 sections | 2,259 | 103 |
| `local/PKE_SA_NQA1_global_docs` | 164 | 1,386 sections | 1,295 | 91 |
| `local/Enconet-0a063bd7` | 242 | 3,519 symbols | loadable, original identity | see below |

All three doc profiles are **SHA-certified**, `source_dirty:false`, not truncated,
with **zero drift, zero missing and zero errors**. Every skipped section reports
`empty_byte_range`; skips are disclosed, not counted as verified text.
Each durable doc handle is `local/<index-name>@e4201491241e5d139c9b5d1ebafa4ca3ca210f72`.

The code index keeps the **live Enconet source root and original identity**.
All 246 selected live paths match the pinned commit under Git's byte/line-ending
policy. Stored Git HEAD independently matches that commit. Tool discovery
omitted four files: oversized `project-file-relocations.json`, and unsupported
HTML templates `dashboard-template.html`, `review-workspace-template.html`,
`vendor-dashboard.html` in `templates/`. These still exist in the live tree and
snapshot; the index is not a claim to parse their contents. Eight indexed files
have no symbols. Import extractors for CSS, JSON, PowerShell and YAML are absent;
the tool warns that import/dead-code analysis for those languages is incomplete.
No parser limit was silently raised and no warning was hidden.

Receipts: `index-refresh-snapshot.json` (explicit lists and raw file hashes),
`index-refresh-results.json` (full index/verification responses).
Their raw SHA-256 hashes are respectively
`130dd1b7266369f4d2589a9a64e240a5940a0069a0bf7de5c7fa63742a172395`
and `635567e9fca17d3fbbb15403b15c4950c9f0cfefb72dcdf950460a825dec00ca`.
The local Git attributes retain receipt bytes across platform checkouts.
AI summaries and embeddings were disabled; this avoids sending source content
to another service. Code context providers were disabled, not represented as
having run. Later report/coordination/handoff commits will be newer than this
certified snapshot. Treat it as commit-scoped evidence, not all live owner edits.

## Root scratch — retained, not deleted

The final `pytest-pilot-temp` tree was confirmed to contain **49 empty real
directories, six internal symbolic shortcuts and zero regular files**. It now
resides at `.tmp/cleanup-retained-20261013/pytest-pilot-temp`. The tool never
follows a shortcut and accepts only targets captured as real empty directories
inside that original scratch tree. Directory identity/ACL and link identity,
attributes and raw target strings are unchanged. Absolute shortcuts retain old
targets and are therefore historical, not runnable at the archived location.
Tested undo restores the original tree; **no live undo was run**.

Preview/apply/verify and no-op repeat apply all exited **0**. Exact plan:
`pytest-pilot-archive-plan.json`, canonical SHA-256
`e3bf9010d6c32f16c4b04011f2a297ca59649b8dbfb6063c14e66b5bf6c4ffc2`.

The empty root `.pytest_cache` tree and `.reset-test-work` were also retained
under `.tmp/cleanup-retained-20261013/`, preserving identity and ACL.
Preview/apply/verify exited **0**, two top-level trees. Exact plan and journal:
`root-caches-plan.json`, `root-caches-journal.jsonl`; canonical plan SHA-256
`158fc448d7a8da6e2b4aad98f46848e5234e7123d9291350b5d1c655ffb89b33`.
The previously applied five-folder plan still verifies after the tool's separate
cache-bundle option was added. Nothing was deleted and no ACL was changed.
Root-level pytest/reset scratch names are now absent; `.tmp` is their approved home.

## Commands and test evidence

`PYTHON` below means `C:/xPY/vEnv/WikiEnconet/python.exe`.

```text
PYTHON -B -m pytest scripts/tests/test_shared_index_snapshot.py -q -p no:cacheprovider --basetemp .tmp/cu4-index-snapshot-tests-02 --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/index-snapshot-tests-02.xml
python -B scripts/prepare_shared_index_snapshot.py --root . --output PKE_SA_NQA1_doc/plans/cleanup-cu4/index-refresh-snapshot.json
python -B scripts/refresh_shared_indexes.py --snapshot PKE_SA_NQA1_doc/plans/cleanup-cu4/index-refresh-snapshot.json --output PKE_SA_NQA1_doc/plans/cleanup-cu4/index-refresh-results.json
PYTHON -B -m pytest scripts/tests -q -p no:cacheprovider --basetemp .tmp/cu4-workspace-final-tests --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/workspace-final-tests.xml
```

All exited **0**. Snapshot tests: **2 passed**. Complete workspace tooling:
**119 passed**, no skips. After adding a neutral-corpus tamper guard, the final
complete rerun passed **120 tests**, no skips, using the same command with
`.tmp/cu4-workspace-final-tests-02` and `workspace-final-tests-02.xml`.
The guard refuses a changed file list or dropped exclusions before backend writes.
The focused alias/snapshot/residual group passed eight
tests, and the final root-cache group passed nine; its separate XMLs are retained.
The existing native rename, retry, undo and failure tests are not replaced by a
manual guess. Real read-only code-store verification initially failed in the
sandbox; approved native-access retry proved HEAD/root/242 files/3,519 symbols.
MCP `resolve_repo` and `get_repo_outline` independently confirmed loadability.

For `archive_pytest_scratch.py`, the following exact command was run with MODE
`preview`, `apply`, `verify`, then `apply` again, each exit **0**:

```text
PYTHON -B scripts/archive_pytest_scratch.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/pytest-pilot-archive-plan.json --authority PKE_SA_NQA1_doc/plans/cleanup-cu3/OWNER_LIVE_AUTHORIZATION.md --mode MODE
```

For `cleanup_residual_empty.py`, MODE was `preview`, `apply`, then `verify`,
each exit **0**:

```text
PYTHON -B scripts/cleanup_residual_empty.py --root . --bundle root-caches --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/root-caches-plan.json --mode MODE --authority PKE_SA_NQA1_doc/plans/cleanup-cu3/OWNER_LIVE_AUTHORIZATION.md --journal PKE_SA_NQA1_doc/plans/cleanup-cu4/root-caches-journal.jsonl
```

Initial snapshot test failed because a `--no-checkout` worktree starts with an
empty index. The helper now populates it **after** explicit sparse rules exist;
the clean-worktree/owner-edit/Claude-exclusion test passed. Failed XML remains.
That failed XML contains traceback trailing whitespace; a staged diff check
reported it. Source whitespace checks pass; the diagnostic log was not rewritten.
An inline scratch count incorrectly expected eight nodes; its read-only check
failed and was replaced by the complete 49-node witness and tested archiver.
The remote tool wrapper did not deliver the doc-index completion response; its
orchestration was stopped, stored metadata was checked, and the installed local
indexer completed the same profiles under the same claim. No unconfirmed wrapper
result is counted as a pass. A stale-board validation while the claim was active
is resolved by normal board regeneration, not by suppressing its check.

Prior CU-4 evidence still applies to unchanged active audit code: Enconet full
isolated regression **480 passed**, its aggregate **19 passed**; Ekonerg applicable
aggregate **8 passed/9 phase skips**, light/dark real browser/PDF **29 each**;
v4 release/scaffold tests and eight-supplier layout routing passed. Exact commands
and preservation scopes are in the linked CU-4 and CU-3 result records. This note
does not falsely report those suites as rerun by the index operation.

Final live re-hashing also confirms **1,861 Ekonerg files unchanged** and
**2,300 Enconet files unchanged** against the pre-scaffold receipts. Enconet's
unscoped comparison exited **1** for exactly four expected metadata files:
`HANDOFF.md`, `coordination/BOARD.md`, `coordination/claims/INDEX-REFRESH.yml`
and `wiki/log.md`. A separate check required that exact set, excluded only
those four mutable session records, and re-hashed the other 2,300 files with
exit **0**. Ekonerg's unscoped check exited **0**. No audit-data difference
was allowed. See `final-audit-preservation.json`; the original receipts were
not rewritten. The capture scope is tracked project files plus all raw/DB
files, not a claim to inventory every untracked incoming/scratch file.
The final Codex-owned `Enconet/AGENTS.md` registry pointer was then corrected
to the active `work/manifests/raw_sources.csv` home, with Claude synchronization
explicitly pending. A second scoped receipt, `post-guidance-audit-preservation.json`,
allows exactly that additional guidance edit: **2,299 Enconet files unchanged**,
five named session/guidance differences, **zero audit-data differences**. It
does not replace or rewrite the earlier four-difference receipt.

## Retained exceptions — no forced full-closure claim

1. **Ekonerg empty `outputs/candidates` tree:** the existing authorized native
   batch was retried with native access and still exited **1**, WinError 5.
   Nine of ten original homes remain archived; this one remains original.
   Owner and access rules were read; they do not establish the cause as either
   an ACL defect or a lock. No ACL takeover, process termination or recursive
   removal was attempted. This does not affect the active RUN output paths.
2. **Old root `doc` holds:** four original edited files, four CC records and
   seven rendered agent-guidance files remain. The six original root pytest
   redirect entries have now been retained with their tree. Old `doc` is not a
   second active documentation home. Preserve edits; Claude must handle its
   own files. No ownership override has been inferred from cleanup permission.
3. **Other legacy test scratch and Claude-owned Enconet archived plans:** still
   held in their recorded locations. This report does not claim every supplier
   test folder is empty, classified or relocated. Current tests write under `.tmp`.
4. **Claude post-review and guidance synchronization:** pending, not approved.
   Active CX records remain unresolved until confirmation; none is eligible for
   unilateral archive on the basis of the owner's deferred review alone.
5. **All current/historical path dispositions and final preservation closure:**
   retain the explicit original-plan checklist until all held cases are resolved.
   The indexes and working dashboards are not proof that every old prose link
   was rewritten; immutable history is resolved through relocation records.

The Windows hold and Claude-owned relocation are the remaining external actions;
do not invent another implementation slice or alter audit sources to hide them.

## Owner entry paths — unchanged audit results

- Enconet: `Enconet/outputs/RUN-20261008-17/dashboard_light.html`,
  `dashboard_dark.html`, `report.md` — **80.6%, 1450/1800**.
- Ekonerg: `Ekonerg/outputs/RUN-20261003-32/dashboard_light.html`,
  `dashboard_dark.html`, `report.md` — **77.8%, 1400/1800**.
- Reusable package: `audit_template/framework/v4/`, manifest SHA-256
  `2a18e0db61973b3702989de63ebcf9c1a26f6492b6a55cccba30c950c92b2cb4`.
- IBE, TEKOL, IGH, IMK, KCPG and MOR: 170 installed files and 129 retained
  originals each; setup, no inherited approvals or vendor evidence.

This operation edited no incoming document, raw source, database, crumb,
evaluation, approval, prompt or dashboard. The original seven owner edits remain
unstaged. Session publication may append its own Enconet log/handoff/board records.
