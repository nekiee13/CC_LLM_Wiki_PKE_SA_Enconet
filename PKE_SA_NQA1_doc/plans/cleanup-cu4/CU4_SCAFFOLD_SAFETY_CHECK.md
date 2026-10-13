# CU-4.1 scaffold safety check

This is Codex's technical check, not an independent Claude approval.
The owner authorized live cleanup and deferred Claude's pre-execution review.
The current request continues the same CU-4.1 task. No audit gate is waived.

## Exact scope

Apply the saved previews for IBE, TEKOL, IGH, IMK, KCPG and MOR only.
Each is an unstarted v2 scaffold. Each preview has zero blockers, 129 original
files to retain and 170 v4 files to install. `incoming/` is preserved in place.
Enconet and Ekonerg are not upgrade targets.

The tools are committed at `5583591`. The new immutable release is v4.0.0,
built from that commit. Its manifest SHA-256 is:

`2a18e0db61973b3702989de63ebcf9c1a26f6492b6a55cccba30c950c92b2cb4`

## What and why the controls matter

- **Root guard:** A target must be one existing supplier folder directly below
  this workspace. Paths cannot escape through `..`, links, junctions, drive
  aliases or hard links. Claude-owned paths are excluded from move targets.
  This stops a vendor update from changing a sibling or another agent's files.
- **Read-only preview:** The tool checks each old file against its installed
  release and records actual hashes. Apply compares the saved plan with a fresh
  preview before making any change. Edited tools, unknown files or a database
  block the upgrade. Incoming inputs are recorded but never moved.
- **Backup strategy:** Original files move to the supplier's local
  `work/migrations/framework-v4/<run>/original/` tree. Empty legacy directory
  trees are retained by native rename. No original is deleted or overwritten.
  Original Git policy files use a `.record` suffix, with their source and archive
  paths in the plan, so they cannot normalize the archived bytes on checkout.
- **Recovery:** A plan-bound journal records authority and progress. A full
  preflight checks the target states before recovery writes. Interrupted apply
  can retry or restore. Changed new files block undo before anything moves.
- **Activation:** `project-layout.json` is installed last, after legacy homes
  are archived and runtime copies are installed. Apply and verify check all new
  bytes, all retained originals and the preserved incoming hashes.
- **No audit inheritance:** State remains `setup`, all seven gates remain
  pending, edition/scope choices remain unset, approvals have headers only and
  the active-prompt map is empty. No database, source, crumb or score transfers.

## Test evidence before live use

- Full release/upgrade group: 46 passed, two subtests passed, zero failures,
  errors or skips. Receipt: `v4-publication-regression.xml`.
- Final v4 group after the exact-byte archive fix: 17 passed, no skips.
  Receipt: `v4-final-byte-policy.xml`. This includes all new release and upgrade
  tests, four synthetic intake-to-report cases, standalone light/dark dashboards,
  browser checks, interrupted retry/restore and a CRLF/Git-policy round trip.
- The prior versions and addons match their full manifests and have no Git
  changes. The old v2/v3 manifests retain their original hashes.
- Guidance drift and skill structure checks both returned exit code 0. Claude
  synchronization remains pending; no Claude file was changed.

The saved previews are `<supplier>-upgrade-preview.json` beside this note.
The live command must cite `OWNER-LIVE-CLEANUP-20261012` and the deferred-review
decision. Claude will receive one task-level review request after the batch.
