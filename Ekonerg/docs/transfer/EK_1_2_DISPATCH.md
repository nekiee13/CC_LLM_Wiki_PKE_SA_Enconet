# EK-1.2: local audit commands

Date: 2026-09-29. Codex builds; Claude reviews.
Status: this package needs review. The whole EK-1.2 task stays open.

## What & Why

The command tool is the front door to an audit. It checks the current phase
before it starts a stage. Closeout must check the audit, then write a handoff
inside Ekonerg. It must not call the shared workspace tool.

This package adapts four files from the approved `9f20430` source:

- `scripts/audit_command.py`: use local paths and local closeout tools.
- `schemas/audit_commands.yml`: keep all 12 commands and phase lists. Change
  only the handoff route to `scripts/make_handoff.py`.
- `scripts/audit_state.py`: keep the phase and human-gate rules. Guard paths
  before reading state or writing state, a temp file, or the log.
- `scripts/db_util.py`: keep SQL safety, ID checks and foreign keys. Resolve
  the database and ID schema inside this project.

The new `scripts/project_paths.py` is a small shared helper **inside Ekonerg**.
It is not a workspace script. It anchors relative paths to this project and
rejects foreign paths, links, Windows junctions, and hard-linked files.
The new tests use fake projects, not live company data.

Source Git blobs and source/destination hashes are in
`EK_1_2_DISPATCH_ADAPTATIONS.json`. Destination hashes use LF line endings.
Four more adapt rows are submitted, not yet approved. After this package,
212 adapt rows and 49 recreate rows remain unimplemented.

## How the paths work

The project root comes from each copied file, not the caller's folder or the
shared Git root. State, database, registry and validation-history paths are
checked even for a describe request. Audit status opens an existing database
read-only and closes it. It does not create a database.

Known path-valued stage options are checked before a process starts. Both
`--output file` and `--output=file` work. Relative targets become local absolute
paths. Short path-option names are refused so they cannot bypass the check.
The gate's `--state-source` is provenance text, not a file-read option; it stays
unchanged so a packet does not gain a machine-specific path.
The list comes from inspection of the pinned stage CLIs. Unknown non-path
options still belong to the stage's own parser.

Closeout requires both local scripts to exist, even in a dry run. It checks
the two-script registry contract, runs local validation with `--no-record`,
and calls the local handoff helper only if validation returns zero. Both
processes run with Ekonerg as their working folder. A foreign handoff root is
refused before validation starts.

This guard suits a normal local workflow. It does not claim to defeat an
attacker who changes paths between a check and a later file operation.
Publication recovery and run-completion rules remain EK-4.3 work.

## Tests first: RED to GREEN

Command used for each focused run:

```powershell
python -B -m unittest discover -s Ekonerg\tools\tests -p test_local_dispatch.py -q
```

1. The first sandbox run returned 1: temp-folder access was denied. This was
   an environment failure, not product RED evidence. Rerun with approved
   temp access: exit 1, 14 failures for the missing local dispatcher file.
2. Copy the four pinned files without fixes. Exit 1: 6 test failures exposed
   the wrong handoff route, foreign database access, foreign global paths,
   false dry-run availability, registry route, and caller-relative state.
   Two extra cleanup errors came from open SQLite handles in the test harness.
   Close those handles; do not count cleanup errors as product defects.
3. Apply local routing and path checks. Exit 0: all 14 tests passed.
4. Add nine tests. Exit 1: 2 failures exposed forwarded foreign output paths
   and an unnormalized relative output. The other seven tests passed.
5. Add forwarded-path checks. Exit 0: all 23 tests passed, no skips.
6. Add three inherited-behavior checks: IDs and SQL names, one valid synthetic
   gate approval, and a hard-linked state temp file. Exit 0: 26 tests passed.
7. Add the provenance-text test. Exit 1: it exposed a wrongly rewritten gate
   source reference. Remove that text option from the file-path list. Exit 0:
   all 27 focused tests passed, no skips.

Tests cover three caller folders, Croatian characters, no Enconet folder,
all seven gate-packet phase mappings, missing dependencies, wrong phases,
foreign output options, real junctions, hard links, read-only status, local
SQL foreign keys, and refusal to skip human gates or audit phases.

The real publisher test uses a **synthetic validator**, then the actual copied
handoff tool and schema. It validates the new handoff and compares fake sibling
and nested Enconet file lists, bytes and modification times. This proves wiring,
not that the real audit aggregate passes. Separate mocked-process tests prove
call order, working folders, and no publication after a nonzero validator exit.

## Final checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 97 tests passed; no skips. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and the 275-file scan match. |
| `python -B Ekonerg\scripts\audit_command.py --describe audit-close` | 0 | Both registry routes are local. |
| `python -B Ekonerg\scripts\audit_command.py audit-status` | 1 | Missing fresh project state; no false status pass. |
| `python -B Ekonerg\scripts\check_skill_structure.py` | 0 | No local skills configured yet. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | Missing local pair map; still EK-3.3 work. |

The tool and support runs use the shared interpreter, with permission for
disposable temp fixtures. No package install or upgrade was made.

## Still pending

This is not a whole-framework release or whole EK-1.2 approval request.
The real state, ledgers, database, vocabulary and ID schemas are not set up.
The real aggregate and most stage scripts are not present. Full audit,
sieving, browser and benchmark checks were **not run**.

Each remaining stage must guard its own positional inputs, paths built from
IDs, and direct CLI calls. Dispatcher option checks do not replace those checks.
Remaining runtime and sieving copies need their own synthetic tests and review.
No production evidence, old approvals or audit outputs were copied. Enconet
audit code and data were not changed. Only the authorized neutral coordination
channel was updated on that side.

## Claude review request

Review this package only. Compare the four files to their pinned source blobs;
check the two new files and the hash record. Rerun the 27 focused tests, all 97
tool tests, the 23 support tests and manifest verify. Check phase/gate rules,
path bounds, alias handling, closeout order, and the stated limits. Return
findings or package-only approval. Keep the whole EK-1.2 task open.
