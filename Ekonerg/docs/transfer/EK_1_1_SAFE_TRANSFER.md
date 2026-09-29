# EK-1.1 — Safe preview and copy tool

Status: EK-1.1 closed after Claude approved the live one-file evidence in
`CC_2026-09-29T133153Z_ekonerg-live-transfer-approve` on 2026-09-29.
Codex implements; Claude reviews. Date: 2026-09-29.

## What & Why

The tool checks the packing list before moving any item. It refuses to replace
an existing file. A preview is the default, so a plain command only shows what
would happen. A small journal records each step if copying is later approved.

Tool: [safe_transfer.py](../../tools/safe_transfer.py).
Tests: [test_safe_transfer.py](../../tools/tests/test_safe_transfer.py).
Evidence: [EK_1_1_VALIDATION.md](EK_1_1_VALIDATION.md).
Live run: [EK_1_1_LIVE_VALIDATION.md](EK_1_1_LIVE_VALIDATION.md).

## Scope of this version

Claude approved the manifest at `574ff07` in
`CC_2026-09-29T114644Z_ekonerg-transfer-manifest-approve`. The tool pins the
approved manifest's LF SHA-256, then checks every row against source commit
`9f20430c95334daa4c3cedb7ee71b002bd3be739`. It reads source bytes from Git,
not from dirty files or installed packages.

Only one row permits an unchanged copy: `handoff_schema.yml`, 644 bytes.
Its destination is `Ekonerg/handoff_schema.yml`. The expected SHA-256 is
`79908730a5519ae245eb0418641192fe9938582c37ac7f13d33e061efb7b358f`.

The 225 adapt items and 49 recreate items are shown separately and left pending.
The 1,688 excluded items cannot be selected. An explicit `--source` request for
an unlisted, adapt, recreate, or excluded item fails. This tool does not invent
adaptations, copy old sources, or treat the whole framework as ready.

The command-line entry point pins the real project and approved manifest. Its
internal functions accept mock inputs for tests; they are not an approval API
or a general file copier. A changed source policy or allowlist requires review.

## Commands

Run from the workspace root. `-B` also disables Python's bytecode cache writes.

Preview only:

```powershell
python -B Ekonerg\tools\safe_transfer.py
```

After Claude reviews the tool, target calculation, preview, and recovery policy,
an explicitly authorized apply would use:

```powershell
python -B Ekonerg\tools\safe_transfer.py --apply --run-id EK11-001
```

The live run used ID `EK11-20260929-001`; a preservation check used
`EK11-20260929-002`. Do not rerun this example as part of evidence review.
It creates only absent copy-approved targets. It also writes a journal under
`Ekonerg/docs/transfer/runs/` and uses a short-lived lock in the project root.

A run ID uses letters, numbers, hyphens, or underscores. It cannot be a path.
Reusing an existing run requires explicit resume:

```powershell
python -B Ekonerg\tools\safe_transfer.py --apply --run-id EK11-001 --resume
```

Read-only diagnosis:

```powershell
python -B Ekonerg\tools\safe_transfer.py --diagnose EK11-001
```

If `--source` was used to select a subset, use the same selection on resume or
diagnosis. The journal binds the full plan, exact destination, selection, source
commit, and manifest content. A different plan cannot resume that run.

## Safety rules

- Only the exact workspace `Ekonerg` root is accepted. The workspace root,
  sibling Enconet, a nested Enconet folder, and traversal paths are refused.
- Existing ancestors and target paths may not be links or Windows reparse points.
  This includes directory junctions. Existing hard-linked files are refused too.
- Identical existing files are kept without rewriting their bytes or change time.
  Different content stops the operation. No overwrite switch exists.
- Copy files use exclusive creation. A file that appears after preview is checked
  again; it is not replaced. The entire source plan is rechecked before apply.
- Source bytes are copied unchanged, preserving any origin or license text within
  them. The journal records the source path, Git blob, commit, hash, and mode.
- The tool never imports or runs transferred code. No Enconet runtime file is
  read or written to obtain source bytes.
- Only existing copy-parent folders are supported. The approved copy has a
  root-level target. New nested copy destinations need a reviewed extension.
- One cooperative writer is required. The lock rejects another apply or a stale
  lock. It is not protection against a hostile process swapping paths during I/O.

The existing Ekonerg plan, review tools, handoffs, and environment stay intact.
No broad cleanup, database creation, source intake, or framework execution occurs.

## Journal and interrupted work

The journal is an append-only UTF-8 JSON-lines file. Each write is flushed and
synced. Its records are `start`, per-file `intent`, `created` or `preserved`, then
`complete`. Receipts contain the output hash, size, file identity, and change time.
Malformed, truncated, mismatched, or out-of-order records stop resume.

| Interruption point | Safe response |
|---|---|
| Before the output exists | Resume can create it after all checks pass. |
| After a complete output, before its receipt | Resume may keep the matching file, but records it as preserved. It does not claim ownership. |
| After a durable created receipt | Resume checks the exact file fingerprint and can finish without rewriting it. |
| During the output write | The partial file conflicts with the source. Stop; do not overwrite or remove it automatically. |
| During a journal write | Stop for manual inspection. Never discard a torn line silently. |
| Process termination leaves a lock | Confirm that no writer remains. Review the exact lock before any manual removal. No force-unlock command exists. |

Diagnosis reports a removal candidate only for an incomplete run with a durable
created receipt whose bytes and file fingerprint still match. It never removes
anything. Preserved files, uncertain outputs, changed files, directories, and
files from complete runs are not removal candidates.

Recovery policy: prefer checked resume. If recovery requires removal, first
review the journal's provenance and exact resolved path. Remove only a recorded,
newly created, still-unchanged file from that failed transfer under a separate
explicit action. Recheck immediately before removal. Never use recursive cleanup.
Keep the journal as evidence. The journal is a local record, not a signed security
boundary; a manual deletion decision must not trust a forged receipt.

There is no overwrite backup to restore because existing files are never changed.
Git retains the pinned original bytes. This does not replace the Owner's later
audit-data backup decision or authorize removal of ambiguous partial output.

## Acceptance and next gate

Thirty focused tests prove preview, copy, conflict, path, journal, and resume
behavior in fake workspaces. The real one-file apply is now recorded. EK-1.2 must
still prove the copied support tools' own nested/sibling path isolation; these
copier tests do not replace that work.

Claude approved the tooling at `856e838` in
`CC_2026-09-29T130213Z_ekonerg-safe-transfer-approve`. The Owner then said
to proceed. Claude also approved the live evidence at `8951b4e` in
`CC_2026-09-29T133153Z_ekonerg-live-transfer-approve`, closing EK-1.1.
Adaptations and source-free recreation remain separate work. No runtime scripts
or audit documents have been transferred.
