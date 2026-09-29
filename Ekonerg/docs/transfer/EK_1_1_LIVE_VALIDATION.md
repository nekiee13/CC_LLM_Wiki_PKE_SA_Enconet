# EK-1.1 live transfer evidence

Date: 2026-09-29. Implementer: Codex. Reviewer: Claude.
Status: live run complete; Claude review pending. EK-1.2 has not started.
Starting HEAD: `d22614bb999750300ad6e86389ffb4e19ddb8af0`.

## What happened and why

We copied the one file that needs no edits: `handoff_schema.yml`. It defines
the fields in a handoff note. It holds no audit sources or company data.
The second run checked that a matching file is kept, not rewritten.

The Owner's `proceed` followed Claude's tool approval at `856e838`, recorded in
`CC_2026-09-29T130213Z_ekonerg-safe-transfer-approve`. The approved code and tests
had no changes. No tool code changed in this live step.

Source commit: `9f20430c95334daa4c3cedb7ee71b002bd3be739`.
Source path: `handoff_schema.yml`. Target: `Ekonerg/handoff_schema.yml`.
Git blob: `b2db225c0163e00f40759b27d15d51c30c4d156f`.
Size: **644 bytes**. Raw SHA-256:
`79908730a5519ae245eb0418641192fe9938582c37ac7f13d33e061efb7b358f`.

All 225 adapt and 49 recreate entries remain pending. All 1,688 excluded
entries stayed excluded. No audit documents, databases, or runtime scripts
were copied. Existing owner files and the shared environment were left intact.

## Commands and results

Commands ran from the workspace root. `python` resolved to
`C:\xAppz\miniconda\python.exe`. Each row below exited **0**.

| Check | Command | Result |
|---|---|---|
| Regression | `python -B -m unittest discover -s Ekonerg\tools\tests -v` | 56 passed, no skips; tests used disposable workspaces |
| Before and after integrity | `python -B Ekonerg\tools\transfer_manifest.py verify` | All 1,963 rows and the dependency scan match |
| Before preview | `python -B Ekonerg\tools\safe_transfer.py` | One `create` candidate, expected source and hash |
| First apply | `python -B Ekonerg\tools\safe_transfer.py --apply --run-id EK11-20260929-001` | Created one schema file; run complete |
| Repeat apply | `python -B Ekonerg\tools\safe_transfer.py --apply --run-id EK11-20260929-002` | Created no framework files; preserved the schema |
| Resume complete run | `python -B Ekonerg\tools\safe_transfer.py --apply --run-id EK11-20260929-001 --resume` | No file or journal changes |
| First diagnosis | `python -B Ekonerg\tools\safe_transfer.py --diagnose EK11-20260929-001` | Complete; no changed, missing, uncertain, or removal-candidate files |
| Second diagnosis | `python -B Ekonerg\tools\safe_transfer.py --diagnose EK11-20260929-002` | Same clean diagnosis |
| After preview | `python -B Ekonerg\tools\safe_transfer.py` | One `preserve` candidate; no writes |

The manifest verifier's `framework_files_copied: 0` describes that verifier's
own work. It is not a count of files now present in Ekonerg.
Resume reports the first run's original `created` receipt; it did not copy again.

## Journals and file identity

Both journals have four records: `start`, `intent`, one receipt, then `complete`.
The start record binds the source, full plan, selection, and exact target root.

| Journal | Receipt | Raw journal SHA-256 |
|---|---|---|
| [EK11-20260929-001.jsonl](runs/EK11-20260929-001.jsonl) | `created` | `2bc1b80623f40cff5a432f0a53b93b104f2756ba5307b64ad76f148a2cffe7ab` |
| [EK11-20260929-002.jsonl](runs/EK11-20260929-002.jsonl) | `preserved` | `5f14dbc0c10b45cde011e6ddb9b4bb2a3e404d6e846e9d981f695b0aed1cc5d4` |

Both receipts match the file after all checks:

- `st_size`: `644`
- `st_mtime_ns`: `1790688071332117900`
- `st_ino`: `11821949021937345`
- `st_dev`: `13858915109679781494`
- `sha256`: the schema hash above

These identities are local to this filesystem. A fresh checkout may have a new
file identity or line endings. Do not alter receipts to fit another checkout.
The temporary transfer lock was absent after every command.

## Before and after checks

A Python wrapper, run through `python -B -` (exit 0), called the real CLI with
`subprocess.run` and required each exit code to be 0. It checked these conditions
in order and stopped on any failed assertion:

1. The schema, run folder, and transfer lock were absent before the first preview.
2. It captured all Ekonerg files as `(SHA-256, size, mtime_ns, inode)` plus the
   directory names. It excluded `.venv` and `__pycache__`, as in the tool review.
3. The first preview left that snapshot unchanged: 25 entries.
4. The first apply added only the schema, the run folder, and the first journal.
   Every existing snapshot entry still matched.
5. The repeat apply added only the second journal. It left all prior entries,
   including the schema fingerprint and first journal, unchanged: 29 entries.
6. Resume, both diagnoses, and the final preview left that snapshot unchanged.
7. Both journal event lists and receipt fingerprints matched the expected values.
8. Enconet's `git diff --binary HEAD -- Enconet` and
   `git status --short --untracked-files=no -- Enconet` outputs matched before
   and after. This checks tracked changes, not the contents of untracked files.

A separate `python -B -` check (exit 0) compared the schema bytes directly to
`git show 9f20430c95334daa4c3cedb7ee71b002bd3be739:handoff_schema.yml`.
It also checked the expected hash and size, parsed the JSON-compatible YAML,
and confirmed the lock was absent. All assertions passed.

Git emitted line-ending warnings for two pre-existing Enconet worktree changes.
Neither file was changed by this step. Existing Claude-owned unstaged message
deletions were also left alone.

## Review and limits

Claude should inspect the committed schema and journals, rerun the 56 tests,
manifest verify, preview, and read-only diagnoses. Do not create a third live
run just to review this evidence. Prior timestamps cannot be independently
reconstructed; the journals and this recorded before/after observation preserve
the live evidence. The deterministic tests check the same preservation rules.

The tool still assumes one cooperative writer. No hostile race or power-loss
guarantee is claimed. No recovery deletion was needed or performed.
EK-1.2 isolation tests and all audit runtime/gate checks are not run: that
framework is not present yet. The earlier `EK_1_1_VALIDATION.md` is historical
pre-apply evidence, not the current live status.
