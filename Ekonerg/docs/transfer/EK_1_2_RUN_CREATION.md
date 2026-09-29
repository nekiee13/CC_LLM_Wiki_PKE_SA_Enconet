# EK-1.2: local, guarded run creation

Date: 2026-09-30. Codex implements; Claude reviews later. EK-1.2 is
still open.

## What & Why

The pinned run command imported an Enconet-specific source validator.
The Ekonerg command now reads only its copied project files. It requires
an existing local database, a registered document, an active local
prompt, and that prompt's local text file. A first run must use the
active version. A later candidate may use a new version only when its
file and CHANGELOG row exist. The real Ekonerg active registry is empty,
so it blocks real run creation now.

For RULE runs, each source code and role must match a row in the local
`approved_sources` table. A governing source is required. DOCUMENT runs
must have no authority references. The command checks basic reference
shape and conditional applicability, then saves a run and references
in one database transaction. It rejects a foreign database path before
opening it. No regulation code, supplier name, or sibling-project import
is embedded in the command.

The database row is a **claim of approval**, not independent proof.
Only future owner-reviewed intake may populate it. The command does not
make a scope decision and cannot run against the empty real Ekonerg
database state, which has no document or active prompt.

## Tests first

Five tests failed before the local command existed. All six pass now.
Two later red checks caught bugs: malformed authority roles produced a
traceback, and a backtick-wrapped candidate version in the local
CHANGELOG was not found. Both now fail or succeed cleanly as intended.

Tests copy local files into two fake company projects, with spaces and
Croatian text. One has a fake sibling Enconet. They create invented
database and prompt records, then check empty-registry refusal,
first-run and candidate generations, a new candidate's history row,
unregistered and wrong-role sources, malformed references, foreign-path
refusal, and unchanged sibling bytes, file time, and file list. No real
audit data is used.

## Source and limits

`EK_1_2_RUN_CREATION_ADAPTATIONS.json` maps the adapted command to
pinned commit `9f20430`, including source blob and hash, local hash, and
test hash. After this batch, 183 adapt and 45 recreate rows remain.
Claude review is queued, not approved.

The broader crumb validator and sieving contract still have inherited
source-code choices. This command does not import them, but they must
be made company-neutral and tested before any real sieving. Prompt
approval, source editions, storage, and scope remain owner decisions.
Generation, import, metrics, scoring, and the full audit aggregate are
not ready. No real database or run was created.

## Checks

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m pytest Ekonerg\scripts\tests\test_sieve_run_local.py -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-run-local-20260930` | 0 | Six isolated run-creation tests passed. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-run-local-20260930` | 0 | 39 support tests passed. |
| `python -B -m unittest discover -s Ekonerg\sieving\tests -q` | 0 | 75 sieving tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 transfer-tool tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 pinned rows and 275 dependency files verified. |
| `python -B Ekonerg\scripts\check_guidance_drift.py` | 1 | Planned EK-3.3 guidance-pair file is absent. |

The adaptation map matched both local file hashes and the pinned source
hash: zero mismatches.

The full audit aggregate, real corpus, browser, and benchmark checks
were **not run**. Claude: review the local-path gates, source-role
lookup, empty-prompt refusal, transaction behavior, and pinned hash
map. Please review this batch without closing EK-1.2.
