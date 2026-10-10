# Six vendor folders: v3 upgrade plan

Date: 10 October 2026. Implementer: Codex. Reviewer: Claude.
State: preview complete; no upgrade applied.

## Goal

Give IBE, TEKOL, IGH, IMK, KCPG and MOR the same tested v3 tools.
Keep their names, inputs and local choices. Do this as one batch task,
not a new task for each file.

## Epic 1 — Check the real folders

What & why: compare each installed file with the pinned v2 and v3 releases.
This lets us spot local edits before any replacement.

### Task 1.1 — Build a read-only preview

What & why: list exact paths and hashes so the owner can see what will change.
The tool has no apply mode. Its output stays outside the vendor folders.

Acceptance criteria:

- [x] Check both complete release manifests and their payload hashes.
- [x] Record exact current-byte, v2 and v3 hashes for every proposed file.
- [x] Label CRLF/LF-only differences; do not call them byte-identical.
- [x] Stop on local edits, missing v2 files, linked paths or company input.
- [x] Preserve existing files and timestamps during the preview.
- [x] Test preview, local changes, new input and line-ending handling.

Result: all six folders have **zero blockers**.

| Per folder | Count | Meaning |
|---|---:|---|
| Add | 36 | New v3 files, including current delivery tools |
| Replace | 66 | Known v2 files and setup records needing v3 changes |
| Keep | 63 | Files already equal, or differing only in line endings |

These 165 entries include 159 release files and six setup records.
Across six folders, the proposed writes are 216 additions and 396 replacements.
Older v2-only files are listed separately and retained, never deleted.
Bootstrap journals are retained. No database is created.

Preview: [Exact paths and hashes](v3-existing-vendors-preview-20261010.json).

```powershell
C:/xPY/vEnv/WikiEnconet/python.exe -B audit_template/preview_vendor_upgrade.py --targets IBE TEKOL IGH IMK KCPG MOR --output doc/framework-reuse/v3-existing-vendors-preview-20261010.json
```

The saved output already exists. A repeat needs a fresh output filename.
The existing clean installer is not an upgrade tool; do not force it to overwrite.

## Epic 2 — Apply one safe batch

What & why: the owner must approve this replacement scope. The current preview
does not grant permission to overwrite anything or approve new audit sources.

### Task 2.1 — Review and approve the replacement plan

What & why: confirm that these six unstarted scaffolds should move to v3.
Claude reviews the technical plan and v3 release. The owner approves deployment.

Acceptance criteria:

- [ ] Claude reviews the release and this exact preview, or the owner explicitly
  accepts deferred review for this deployment.
- [x] v3 release review itself is closed by CC_2026-10-10T150048Z_framework-v3-ack;
  the new upgrade preview is not yet reviewed.
- [ ] Owner authorizes replacing the listed known v2 files in all six folders.
- [ ] No reset, source intake or audit approval is bundled into that authorization.

### Task 2.2 — Implement and run the guarded upgrade

What & why: replace only files whose bytes still match the approved preview.
Keep the old framework bytes so a failed software upgrade can be undone.
This is not a backup or reset of audit documents.

Acceptance criteria:

- [ ] Test stale hashes, local edits, linked paths, partial failures and safe retry
  before the first real replacement.
- [ ] Recheck every target before writes; stop if documents or a database appeared.
- [ ] Store exact old framework bytes and a per-target journal outside each target.
- [ ] Roll back only this run's writes on handled failure; preserve other files.
- [ ] Keep supplier names, pending gates and unset local source/scope choices.
- [ ] Upgrade state syntax without approving a gate or changing its value.
- [ ] Update v3 method links and version records; retain v2-only history.
- [ ] Verify final hashes and local command smoke tests in all six folders.
- [ ] Confirm Enconet, Ekonerg and all incoming files remain unchanged.
- [ ] Leave one task-level review message with the complete batch evidence.

## Tests and limits

Focused suite: `C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests/test_vendor_upgrade_preview.py -q -p no:cacheprovider --tb=short`:
exit 0, **4 passed**. The initial TDD run failed because the planner did not yet
exist. A later sandbox run hit Windows temp-folder permissions; its unrestricted
rerun passed. Neither failed run is counted as a pass.

The preview command returned exit 0. It does not prove apply/rollback behavior:
that code is not yet implemented. v3 approval and deployment remain separate
from local source editions, sieving calibration and audit findings.

Full template regression: `C:/xPY/vEnv/WikiEnconet/python.exe -m pytest audit_template/tests -q -p no:cacheprovider --tb=short --junitxml=doc/framework-reuse/v3-upgrade-preview-full-suite.xml`:
exit 0, **121 passed and 44 subtests passed**, zero skips.
The existing v2/v3 manifest hashes remain unchanged.
