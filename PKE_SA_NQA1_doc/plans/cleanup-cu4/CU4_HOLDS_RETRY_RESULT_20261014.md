# CU-4.2: retry of the retained cleanup holds

Owner-local date: 14 October 2026. Status: **partial, with real holds reduced**.
This continues the original cleanup task. No new task or audit gate was added.

## What moved

| Hold | Result | Retained home / receipt |
| --- | --- | --- |
| Ekonerg `outputs/candidates` | Native retry succeeded; all 10 original directory trees now verify as moved | `Ekonerg/work/migrations/cleanup-cu3-live-20261012/empty-original-homes/outputs/candidates`; original `directories.jsonl` journal appended |
| Eight old `doc/support-transfer` files | All moved; all eight working-file hashes and original Git index blobs match | Same relative paths under `PKE_SA_NQA1_doc/support-transfer`; `holds-retry-file-map.json` |
| Legacy empty pytest scratch | 63 trees moved, preserving 283 directory nodes and 74 internal symbolic shortcuts | Supplier `.tmp/cleanup-retained-20261014/` or workspace `.tmp/cleanup-retained-20261014/`; `legacy-empty-archive-plan.json` |

No content was deleted. No ACL, owner, shortcut target, source, database,
crumb, score, gate, prompt or dashboard was changed. Native same-volume
renames retain directory identity and permissions. Shortcut traversal is
refused; captured absolute targets remain historical, not runnable aliases
at their new location. Tested undo restores the original locations; no live
undo was run. Repeat apply is a no-op except for the existing journal marker.

The eight documentation moves include four unfinished owner edits. Their
bytes remain exact and **unstaged** at the new paths. Only their original
index blobs are staged as 100% renames. The other three original owner edits
remain at their original paths. The historical external-project rendering
script was not run or rewritten; its old path strings are not an active
runtime promise. The file map is the external old-to-new lookup for these
retained artifacts; frozen records were not rewritten.

The exact prepared workflow is `holds-retry-workflow.json.zip`, canonical
plan SHA-256 `6b6ce48c5f393095e4e71bba9d0d40be11b8b39e2c9c9255d9e832cc13d4e3a3`.
Its owner/review disposition is `holds-retry-authorization.json`; apply/retry
events are in `holds-retry-files-journal.jsonl`. The scratch plan canonical
SHA-256 is `2c2c4ae739e60a56ee7318a7d98453dc26fb8f5cce2dcd8e6b0f60d8b410c377`.
Authority is `OWNER_HOLDS_RETRY_20261014.md`, recording the owner's latest
retry request and existing review deferral, not a fabricated Claude approval.

## Checks actually run

`PYTHON` means `C:/xPY/vEnv/WikiEnconet/python.exe`. Native-access runs were
used for identity/ACL/Git/browser operations after sandbox access failures.

```text
PYTHON -B scripts/cleanup_empty_homes.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-live-sprint-20261012/directory-plan.json --mode apply --journal Ekonerg/work/migrations/cleanup-cu3-live-20261012/directories.jsonl --authorization PKE_SA_NQA1_doc/plans/cleanup-cu3/ekonerg-live-sprint-20261012/directory-authorization.json
PYTHON -B scripts/cleanup_migration.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/holds-retry-file-map.json --mode preview
PYTHON -B scripts/cleanup_workflow.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/holds-retry-workflow.json.zip --mode apply --journal PKE_SA_NQA1_doc/plans/cleanup-cu4/holds-retry-files-journal.jsonl --authorization PKE_SA_NQA1_doc/plans/cleanup-cu4/holds-retry-authorization.json
PYTHON -B scripts/cleanup_migration.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/holds-retry-workflow.json.zip --mode verify --journal PKE_SA_NQA1_doc/plans/cleanup-cu4/holds-retry-files-journal.jsonl
PYTHON -B scripts/archive_pytest_scratch.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/legacy-empty-archive-plan.json --authority PKE_SA_NQA1_doc/plans/cleanup-cu4/OWNER_HOLDS_RETRY_20261014.md --bundle legacy-empty --mode MODE
PYTHON -B -m pytest scripts/tests -q -p no:cacheprovider --basetemp .tmp/cu4-holds-full-tests-03 --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/holds-full-tests-03.xml
PYTHON -B Enconet/scripts/run_all_validations.py --no-record
PYTHON -B Ekonerg/scripts/run_all_validations.py --no-record
PYTHON -B scripts/check_guidance_drift.py
PYTHON -B scripts/check_skill_structure.py
```

All final commands exited **0**. Scratch MODE was `preview`, `apply`,
`verify`, then `apply` again. Both directory/file workflows also passed
repeat apply. Final workspace suite: **126 passed**, no skips. Enconet:
**19 passed**. Ekonerg: **8 passed, 9 phase skips**; no phase advancement.
Guidance: zero errors, 47 anchors, eight documented differences. Skill
structure: zero errors, 32 locations. Historical 480-test audit regression
and previous standalone PDF tests were not rerun by this hold-only change.

Failures are retained, not counted as passes: the first focused sandbox run
failed with temporary-directory WinError 5 (17 setup errors; XML retained).
The native focused rerun passed 17 tests. The first full suite had 125 passes
and one stale historical-patch test failure. That test now reads Claude's
original blob at the recorded preparation HEAD instead of comparing the old
patch to newly synchronized live guidance. It creates no Claude file. Both
subsequent full runs passed 126 tests; the last also tests no-follow discovery.
The first sandbox Enconet aggregate failed browser evidence/budgets with
WinError 5; native retry passed all 19. Initial read-only `audit.db`/journal
path probes named nonexistent files; canonical paths were then verified.

Final database SHA-256 values still equal their pre-cleanup baselines:

- Enconet `db/nqa_audit.sqlite`: `f17c977f8c5ffec13a279bdb909dd17f38e056e5183812a92ae5810b03251ed1`.
- Ekonerg `db/nqa_audit.sqlite`: `161c56ff5d457348ec6809c5e6dcc41e2dd09854d4e71cde11d12a2064d387c0`.

## What remains, and why

Old `doc` now has **seven tracked files**, all Claude-owned:

- `support-transfer/CC_FIN_EVIDENCE_INVENTORY.md`
- `support-transfer/CC_FIN_SUPPORT_PROFILE.md`
- `support-transfer/CC_LOTO_EVIDENCE_INVENTORY.md`
- `support-transfer/CC_LOTO_SUPPORT_PROFILE.md`
- `support-transfer/rendered/fin-claude-guidance/CLAUDE.md`
- `support-transfer/rendered/loto-cc-guidance/CLAUDE.md`
- `support-transfer/rendered/loto-claude-alignment/CLAUDE.md`

Their proposed homes are the same relative paths under `PKE_SA_NQA1_doc`.
Codex did not move or edit them. Claude must handle its own records after
checking hashes/collisions. Empty old directory shells are not a second
active documentation home and were not recursively removed.

The scratch plan records **20 held trees** with exact paths and reasons:

- 15 Enconet `.test-tmp` trees contain generated `.claude` fixtures. Moving
  a parent would also move those protected files, so they remain untouched.
  Any Codex move requires specific owner authorization for that exception.
- Four `audit_template/tests` trees contain actual synthetic test data:
  `analysis-bundle-yupz4b7d`, `phase-criteria-382h_mz1`,
  `source-validators-0ex7vaq2`, `source-validators-94s0r7sf`.
- `audit_template/tests/__pycache__` contains compiled files. The empty-tree
  archiver deliberately does not delete or move populated trees.

Claude's previous cleanup review and docs-home synchronization are already
confirmed; they are no longer pending. This new retry needs its own
post-execution review. The Windows candidates hold is now **resolved**.
Final all-path closure remains in the original CU-4.2 checklist. Shared
indexes remain certified at `e420149`, not refreshed to this new worktree;
agent-owned indexes were not touched. Do not claim complete cleanup yet.
