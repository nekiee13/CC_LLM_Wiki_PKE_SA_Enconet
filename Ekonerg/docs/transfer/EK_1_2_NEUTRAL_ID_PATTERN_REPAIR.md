# EK-1.2 candidate: neutral criterion-scoped ID shapes

## What & Why

The copied ID contract still named Appendix B and its 18 Roman-numeral
criteria. That would reject IDs from another approved criterion set. This
repair changes four patterns in the versioned state bundle and the Ekonerg
copy: crumb, requirement, evaluation, and gap IDs now accept a safe
uppercase criterion token. For example, `AREA_2` fits. Existing
`APP_B_IV` IDs still fit. The token is only an ID shape. It does **not**
approve a criterion, rule, source edition, or audit scope.
If a future approved criterion ID uses another spelling, update this shape
through review; do not silently rename that criterion.

The old source and Ekonerg file had the same SHA-256
`5e70697495f10d7c8be605307f24f197569895052dad547609be6ed858d1ad02`.
The old bytes remain in Git commit `6d1f3ed`. The repaired source and copy
match at SHA-256
`4746fd8d347373bd7800327055770a98b43a9d803958e97c46b9cc0a02f22174`.
The state bundle manifest now pins that exact hash; its own SHA-256 is
`ed584f5f09ed6527a52d1ff87f06387c5e090ecbb3b56d81a902fdb86250d0b3`.

## TDD proof

1. Red: the new Ekonerg ID test exited 1: one failed, four passed, because
   `CRUMB-DOC-0001-AREA_2-0001` did not match. The new bootstrap test also
   found that mismatch, but its full run had sandbox temporary-folder
   permission errors, so that run is not a clean test-suite result.
2. Green: `python -B -m unittest discover -s audit_template/tests -p
   test_bootstrap_state.py -q` exited 0 outside the sandbox: four tests
   passed. `python -B -m pytest Ekonerg/scripts/tests/test_db_identity.py
   -q -p no:cacheprovider --tb=short --basetemp
   C:\Users\PC\AppData\Local\Temp\ekonerg-neutral-ids-20260930-green2`
   exited 0: five tests passed. The tests reject lowercase, double
   underscores, and slash tokens. They keep old Appendix B IDs valid and
   insert a synthetic neutral requirement through the copied DB helper.
3. Full bootstrap suite exited 0 with 21 tests. Ekonerg script, tool, and
   sieving suites exited 0 with 40, 111, and 83 tests, respectively.
   `python -B Ekonerg/tools/transfer_manifest.py verify` exited 0 against
   source commit `9f20430`, 1,963 rows, and 275 dependency files.
4. Workspace `python scripts/check_guidance_drift.py` exited 0 with zero
   errors. Ekonerg `python -B Ekonerg/scripts/check_guidance_drift.py`
   exited 1: planned EK-3.3 `doc/GUIDANCE_PAIRS.json` is absent. This local
   check did **not** pass. The full live aggregate, browser, and benchmark
   checks were not run.

## Live sync and limits

No repair script or database migration ran. The only live change was the
tracked Ekonerg schema copy; the old bytes are recoverable from Git.
`python -B audit_template/bootstrap_state.py --target Ekonerg` exited 0:
all seven files showed `preserve`, with no conflict. Apply run ID
`neutral-id-patterns-20260930-01` exited 0 with zero creates and seven
preserves. Its immutable journal is
`Ekonerg/.bootstrap/state-v1/neutral-id-patterns-20260930-01.jsonl`
(SHA-256 `c9da4fa3c8f011a3caee9fe1ab8d7fbf51b1b89008b4568d7858d72b4fe34115`).
Git marks the schema and journal LF on checkout. No Ekonerg database or
project-state file exists. The header-only validation log is unchanged.
All 31 owner files in `incoming/` remain untouched.

The sieving bundle still contains Appendix B taxonomy and extractor logic.
This ID repair does not make that intake path company-neutral. Fix it in a
separate tested task before any criterion-bearing Ekonerg intake. Claude
review of this candidate is pending.
