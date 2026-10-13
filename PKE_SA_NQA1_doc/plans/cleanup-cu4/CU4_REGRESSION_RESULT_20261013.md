# CU-4 regression result — 13 October 2026

Status: regression work passed. The cleanup plan as a whole is still open.
This is work under the existing CU-4 tasks, not a new task or scope change.
Claude's review remains pending under the owner's review deferral.

## What changed and why

The live audit now uses the agreed v4 folders. Some old test helpers still
looked in the old homes. We fixed the test setup instead of putting old data
back into the live audit.

- The isolated regression workspace now lives in `Enconet/.tmp/`.
- It reads current plans, benchmarks and Codex-owned decisions from their
  configured homes. Its own historical layout is explicitly set to `legacy`.
  Historical source data still comes from the same hash-pinned archive.
- Claude infrastructure and `CC_` records are not copied. Tests read the real
  reviewer records from the explicit, read-only origin when needed.
- The runner's before/after checks now cover the moved derived files and
  manifests, rather than silently scanning their empty old homes.
- Current tests use the moved benchmark homes and include the copied layout
  helper when building a small runtime sandbox.
- Publication tests bind the real layout guard to their disposable supplier
  root. The foreign-root guard is not bypassed or relaxed.
- The aggregate validator supports the explicitly selected historical layout
  as well as v4. It does not guess a layout from which files happen to exist.

No intake, reset, new sieving, score change, gate change or promotion was run
against an active audit. The six future supplier folders were not upgraded.

## Test evidence

All commands below were run from the workspace root. `PYTHON` denotes
`C:/xPY/vEnv/WikiEnconet/python.exe`.

| Check | Command | Exit | Result |
|---|---|---:|---|
| New isolation tests, red run | `PYTHON -B -m pytest Enconet/tests/test_regression_fixture_isolation.py -q -p no:cacheprovider --basetemp Enconet/.tmp/cu4-fixture-red --tb=short` | 1 | Two new tests failed before the fix; six passed |
| Isolation tests, green run | Same test command, with `--basetemp Enconet/.tmp/cu4-fixture-green2` | 0 | Eight passed |
| First complete regression | `PYTHON -B Enconet/scripts/run_regression_tests.py --output Enconet/work/validation/2026-10-13/cu4-regression-02` | 1 | 179 current tests: 24 failed; 301 historical tests: seven failed; no skips |
| Focused path fixes | `PYTHON -B -m pytest Enconet/tests/test_publish_audit_release.py Enconet/tests/test_validate_schemas.py Enconet/tests/test_v3_context_storage.py Enconet/scripts/tests/test_seed_requirements.py -q -p no:cacheprovider --basetemp Enconet/.tmp/cu4-current-path-green --tb=short` | 0 | 31 passed |
| Final complete regression | `PYTHON -B Enconet/scripts/run_regression_tests.py --output Enconet/work/validation/2026-10-13/cu4-regression-03` | 0 | **480 passed: 179 current + 301 historical; zero failures, errors or skips** |
| Reusable v4 checks | `PYTHON -B -m pytest audit_template/tests/test_framework_pipeline_v4.py audit_template/tests/test_framework_candidate_v4.py audit_template/tests/test_project_layout_v4.py audit_template/tests/test_publication_paths_v4.py -q -p no:cacheprovider --basetemp .tmp/cu4-release-regression --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/release-regression.xml --tb=short` | 0 | 27 passed, no skips; full synthetic pipeline, Unicode/space supplier names, sibling isolation, both dashboards and synthetic reset |
| Live phase aggregate | `PYTHON -B Enconet/scripts/run_all_validations.py --no-record` | 0 | All 19 checks passed; browser, report links, frozen portable package and budgets included |

The suite now contains 480 tests, rather than the earlier 467-test release
count. No test file was left out. The runner lists every selected file and
records both pytest commands in `summary.json`.

Windows denied the first in-sandbox fixture build (`cu4-regression-01`, exit 1).
The first in-sandbox live aggregate also failed two browser-based checks
(exit 1). Their outside-sandbox reruns passed. These failures are not counted
as passes or hidden as skips. A first green attempt also exposed a test-path
expectation that needed updating; the recorded final run is the passing one.

The full regression had two existing Click/Typer deprecation warnings. They
were not errors or skips.

## Integrity

The final runner compared **749 protected file hashes** before and after and
reported `live_audit_unchanged: true`. Its detailed scope is the hash list in
`summary.json`; this is not a claim that every workspace file was hashed.

The database still matches the live-cleanup baseline:

`f17c977f8c5ffec13a279bdb909dd17f38e056e5183812a92ae5810b03251ed1`

The historical fixture archive is unchanged:

`38018c13eb9c17172c7c3486b4041dbb54e27618f78cfb9989ebb56cbfcfaedf`

Enconet remains `dashboard_ready`, with G1–G6 approved and G7 pending.
Its published score remains **80.6% (1450/1800)**. Existing owner edits stay
unstaged. No Claude-owned file was changed.

The complete logs, XML results and summary are under:

`Enconet/work/validation/2026-10-13/cu4-regression-03/`

A compact tracked copy is `enconet-regression-03.zip` beside this note.
The failed full run is retained as `enconet-regression-02.zip`.

## What is still open

1. CU-4.1: publish one immutable v4 reusable release and safely upgrade IBE,
   TEKOL, IGH, IMK, KCPG and MOR. The tested development candidate is not yet
   an installed release.
2. CU-4.2: complete the applicable Ekonerg, migration/undo and release suites,
   residual-folder checks and final baseline comparisons.
3. Resolve the existing held files and old test-folder remnants. Do not bypass
   permissions or move Claude-owned records without specific authority.
4. Claude post-execution review and Claude-owned guidance/skill updates.
5. Refresh shared indexes from committed state under an `INDEX-REFRESH` claim,
   then publish the final cleanup report.

None of these is a newly added task. No new owner decision is requested here.
