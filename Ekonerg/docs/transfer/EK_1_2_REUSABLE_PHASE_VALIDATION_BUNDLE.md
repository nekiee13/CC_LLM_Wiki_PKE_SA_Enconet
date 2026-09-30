# EK-1.2 candidate: phase-aware validation runner

## What & Why

The dispatcher needs a local aggregate command. This slice copies the
phase-aware runner from a versioned, hash-locked template. It keeps the
Enconet phase order and the rule that checks stay active in later phases.
The code now finds its own project from its file path. It cannot send a
validator command to a sibling audit through a path option.

The bundle contains one script, not the child validators, project state,
database, manifest records, or approved sources. A missing required child
validator fails. The runner's own database discovery opens SQLite read-only,
so checking for a run cannot create an empty database. A recorded run needs
an existing `manifests/validation_runs.csv` with the correct header. An
absent or bad header cannot become a false PASS.

## TDD evidence

1. Red: `python -B -m unittest discover -s audit_template/tests -p
   test_bootstrap_phase_validation.py -q` exited 1 because the new bootstrap
   module was absent.
2. Green: the four synthetic tests now pass. They use two invented company
   names with spaces and Croatian letters, one with a fake sibling Enconet
   and one without. They also protect a fake nested Enconet folder. Preview
   writes nothing; apply and retry use pinned bytes. From another working
   folder, `audit-validate` reaches the copied runner and reports failure
   when `validate_structure.py` is missing. A small fake structure checker
   proves setup PASS only in the synthetic test project. No database is
   created, and `--no-record` writes no aggregate row.
3. A second red test found that append mode made a headerless CSV if the
   `manifests` folder existed. The runner now requires a real CSV header.
   The test checks missing and invalid headers fail with no PASS claim, then
   checks that a valid header gets one synthetic PASS row.
4. The copied phase matrix remains monotonic; failed phase checks the full
   set. Report and dashboard checks start only at their intended phases.
   Explicit or late-phase benchmarks remain required by the matrix.
5. Foreign state, database, output, and data-root paths are refused. Unsafe
   supplier and run-ID path fragments are refused. The fake sibling and
   nested Enconet file bytes and times stay unchanged.
6. `python -B -m unittest discover -s audit_template/tests -q` exited 0:
   16 tests passed. `python -B -m pytest Ekonerg/scripts/tests -q -p
   no:cacheprovider --tb=short --basetemp
   C:\Users\PC\AppData\Local\Temp\ekonerg-phase-bundle-20260930-03` exited
   0 outside the sandbox: 39 tests passed. The Ekonerg tools and sieving
   unittest suites exited 0 with 111 and 83 tests, respectively.
7. `python -B audit_template/bootstrap_phase_validation.py --target Ekonerg`
   exited 0 in read-only preview: the one file would be preserved. No live
   apply ran. `python -B Ekonerg/tools/transfer_manifest.py verify` exited 0
   against pinned commit `9f20430`, 1,963 rows, and 275 dependency files.
8. `python scripts/check_guidance_drift.py` exited 0. The Ekonerg-local
   guidance check exited 1 because planned EK-3.3
   `Ekonerg/doc/GUIDANCE_PAIRS.json` is absent. It did **not** pass.

## Gate and limits

Claude review is pending. EK-1.2 stays open because child validators and
their own tests are still missing. No live aggregate, browser check,
benchmark, database initialization, or intake ran. The owner files in
`Ekonerg/incoming/` remain untouched. Source scope, editions, storage,
intake, and approval remain owner gates.
