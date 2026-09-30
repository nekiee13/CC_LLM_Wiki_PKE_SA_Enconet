# EK-1.2 candidate: copied database and audit-state runtime

## What & Why

The next audit should get its own database and state tools from a versioned,
tested source. This slice adds a seven-file bundle: project-local path guard,
database helper and initializer, audit-state command, database schema, ID
patterns, and empty source vocabularies. The guarded bootstrap previews and
copies these files. It does **not** initialize a database, make a state file,
copy old rows, or approve a source.

The local vocabulary comments were made company-neutral. Runtime SQL and
approval logic were not changed. A Windows console bug was fixed in the local
CLI path output: commands now print UTF-8 paths for project names with
Croatian characters. The fix lives in the copied `project_paths.py` helper.

## TDD evidence

1. Red: `python -B -m unittest discover -s audit_template/tests -p
   test_bootstrap_state.py -q` exited 1 because `bootstrap_state` did not
   exist. The first full run then found a real Unicode path failure on
   Windows. It also exposed a test-only SQLite handle that needed closing.
2. Green: `python -B -m unittest discover -s audit_template/tests -q` exited
   0 outside the sandbox: nine tests passed. Two invented company roots were
   used, one with a sibling and one without. Each copied initializer created
   an empty local database; retry preserved its bytes and file time. A
   foreign database path was refused. The absent state file failed closed.
3. `python -B audit_template/bootstrap_state.py --target Ekonerg` exited 0
   in read-only preview mode: all seven files matched and would be preserved.
   `Ekonerg/db/nqa_audit.sqlite` remained absent. No live apply or init ran.
4. `python -B -m pytest Ekonerg/scripts/tests -q -p no:cacheprovider
   --tb=short --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-state-bundle-20260930-01`
   exited 0: 39 tests passed. This covers the copied path, database, and
   state commands in their current Ekonerg location.
5. `python -B -m unittest discover -s Ekonerg/tools/tests -q` exited 0:
   111 tests passed. `python -B -m unittest discover -s Ekonerg/sieving/tests
   -q` exited 0: 83 tests passed. The tools suite prints one expected
   failure message while testing a stop condition; the suite itself passed.
6. `python -B Ekonerg/tools/transfer_manifest.py verify` exited 0: the
   pinned Enconet source commit is `9f20430`, with 1,963 manifest rows and
   275 dependency-scan files.
7. `python -B Ekonerg/scripts/check_guidance_drift.py` exited 1 because
   `Ekonerg/doc/GUIDANCE_PAIRS.json` is not present yet (planned EK-3.3).
   This check did **not** pass. Workspace-level
   `python scripts/check_guidance_drift.py` exited 0 with zero errors.

## Gate and limits

Claude review is pending. EK-1.2 stays open. The remaining dispatcher and
aggregate validation tools need their own tested transfer. The owner files
in `Ekonerg/incoming/` were not read, hashed, copied, or processed. Real
source editions, scope, storage, intake, and state decisions remain for the
owner and later gates. The full audit aggregate was not run: this is a
framework transfer candidate, not an initialized or ingested audit.
