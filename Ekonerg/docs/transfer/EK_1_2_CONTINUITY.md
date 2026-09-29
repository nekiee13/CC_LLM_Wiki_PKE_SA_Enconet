# EK-1.2: local session checks

Date: 2026-09-29. Codex builds; Claude reviews.
Status: one runtime slice ready for review. The whole EK-1.2 task is open.

## What & Why

The session check tells the next worker what changed. It reads the handoff,
project status, index, state and database. It must read Ekonerg's records, not
Enconet's. It must warn when a run is unfinished. It must not change a phase or
make an approval.

This slice adapts one file from the approved `9f20430` source:
`scripts/session_continuity.py`. It uses the already approved local state,
database and path helpers. The new test file uses made-up records in temporary
folders. Source and destination hashes are in
`EK_1_2_CONTINUITY_ADAPTATIONS.json`. The destination hash uses LF endings.
After this submission, 211 adapt rows and 49 recreate rows remain open.

## What changed

- Each record path is checked against the Ekonerg root before any read.
  Relative CLI paths start at that root, not the caller's folder. Foreign
  paths, links, junctions and hard-linked files are refused.
- The database probe opens an existing local file read-only and closes it.
  A missing database stays missing. The check never creates or edits one.
- The Git command finds the real repository root from Ekonerg. The Git root
  may be above Ekonerg or inside Ekonerg. It is only read; it is not treated
  as an audit output root. If Git is missing after all records are present,
  the check reports an error instead of inventing a commit ID.
- The old warning rules remain: a mismatched Git hash or phase warns; an
  in-progress phase calls for a human RESUME or approved ROLLBACK; an
  unfinished evaluation run needs an explicit choice. The check makes no
  automatic state change.

The live Ekonerg project does not yet have its fresh status, index or state.
The command prints those missing paths with `WARNING` and exits 0 because
this is an **informational probe**. Exit 0 here does not mean a full audit
check passed. The real validation gate is still pending later tasks.

## Tests first: RED to GREEN

Focused command:

```powershell
python -B -m unittest discover -s Ekonerg\tools\tests -p test_local_continuity.py -q
```

1. Before the local file existed, exit 1: all 13 first tests failed because
   their required local script was missing.
2. Copy the pinned source without changes. Exit 1: six checks failed on
   foreign paths, read-only database access, a hard link and caller-relative
   paths. Two test cleanups also failed because the source left SQLite files
   open on Windows. Those cleanup errors were not counted as new product
   behavior.
3. Add local path checks, close the read-only database, and find the real
   Git root. Add one more Git-root case. Exit 0: all 14 tests passed.

The tests check three caller folders; a workspace with no Enconet at all;
sibling and nested fake Enconet folders; local warning paths; a foreign CLI
argument for each of the five record inputs; direct API calls; hard links and
a real Windows junction; no database creation; no file change on a database
read; both Git-root layouts; phase and Git drift; and an unfinished run.
Fake Enconet file names, bytes and modification times stay unchanged.

## Checks and limits

| Exact command | Exit | Result |
|---|---:|---|
| `python -B -m unittest discover -s Ekonerg\tools\tests -p test_local_continuity.py -q` | 0 | 14 focused tests passed. |
| `python -B -m unittest discover -s Ekonerg\tools\tests -q` | 0 | 111 tool tests passed; no skips. |
| `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider` | 0 | 23 support tests passed. |
| `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | 1,963 rows and the 275-file scan match. |
| `python -B Ekonerg\scripts\session_continuity.py` | 0 | Prints three missing local records as warnings; no audit approval. |

The shared interpreter ran the tests. No package was installed or changed.
No real data, database, approval, source document or output was copied.
Enconet audit code and data were not edited; neutral coordination alone is
updated there.

The full audit aggregate, sieving tests, browser and benchmark checks were
**not run**. Their runtime, fresh state, schemas and inputs are not ready.
The path guard is for a normal local workflow; it is not a guarantee against
an attacker changing a file between the check and the read.

## Claude review request

Review only this continuity slice. Verify the pinned source blob and both
destination hashes. Read the adapted file and tests. Rerun the 14 focused
tests, all 111 tool tests, 23 support tests and manifest check. Check both
Git layouts, path bounds, read-only database access, and the unchanged human
resume warnings. Give findings or slice-only approval. Keep EK-1.2 open.
