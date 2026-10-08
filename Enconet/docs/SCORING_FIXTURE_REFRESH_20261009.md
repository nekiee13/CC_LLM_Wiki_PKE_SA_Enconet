# Scoring fixture metadata refresh — approved and verified

Owner reply: **yes**, to the explicit metadata-only fixture question.
Approval: `SCORING-FIXTURE-ENCONET-1.1-20261009`.
Owner local date: 9 October 2026; recording began on 8 October UTC.

## Result

The fixture refresh is complete. **Both benchmark classes pass.**
The synthetic scoring result stays **46.9% over16 applicable criteria**.
The real Enconet result stays **80.6%,1450/1800 over18 criteria**.
Those are separate data sets and must not be forced to agree.

Exactly four metadata values changed:

- scoring/input.yml fixture_version:1.0 →1.1.
- scoring/expected.yml fixture_version:1.0 →1.1.
- expected model version:0.1-placeholder →0.2-approved.
- expected model SHA256:d16df4986562e3700a1825ba0a2d554997e5403a5f619817bbc6fd1d56a332ce.

No synthetic ratings, scores, counts, verification arithmetic or expected numbers
changed. The dashboard fixture is unchanged. The scoring model itself is unchanged.
The fixture is pinned to its owner-approved model; no further approval for this
metadata refresh is needed.

## Independent proof

[verify_metadata.py](../out/2026-10-09/scoring-fixture-refresh/verify_metadata.py)
compares the live fixture with Git baseline `bfb208b`, checks that only the four
listed fields differ, verifies the model checksum, proves unchanged numerical
model sections, and independently recomputes the original46.875 →46.9 half-up.
It also proves19 original DB table hashes unchanged. This is a read-only proof.

G1–G4 approvals remain valid. Twelve findings remain approved but pending field
verification;18 approved actions remain open. No new audit evidence, applicability,
source edition, run identity or score was changed.

## Checks actually run

| Check | Exit | Result |
|---|---:|---|
| `python Enconet/benchmarks/validate_benchmarks.py --scoring` before change | 1 | Known model version/checksum mismatch reproduced |
| Same scoring command after change | 0 | PASS |
| `python Enconet/out/2026-10-09/scoring-fixture-refresh/verify_metadata.py` | 0 | Exact metadata-only difference and arithmetic/data parity |
| `python Enconet/scripts/run_all_validations.py --benchmarks --no-record` | 0 | 11 phase checks plus both benchmark classes pass |
| Pinned interpreter, `test_epic16_benchmarks.py`, real pytest invocation | 0 | 5 passed; [test report](../out/2026-10-09/scoring-fixture-refresh/scoring-tests.xml) |
| Complete Enconet suite with default interpreter | **1** | 311 passed,56 failed,73 errors,94 warnings |
| Complete suite with dedicated pinned interpreter | **1** | **314 passed,55 failed,71 errors,111 warnings**;440 tests,zero skipped |
| `python Enconet/scripts/validate_evaluation.py --run-id RUN-20261008-17 --no-record` | 0 | Current18 ratings/evidence gates pass |
| `python Enconet/scripts/validate_findings.py --no-record` | 0 | Approved findings/action projections pass |

Full pinned-suite report:
[full-suite-pinned.xml](../out/2026-10-09/scoring-fixture-refresh/full-suite-pinned.xml).
It contains failure traces, not just a green/red summary. No full-suite pass is claimed.

The full suite selected every direct `Enconet/tests/test*.py` file, plus
`Enconet/scripts/tests` and `Enconet/sieving/tests`. It did not recurse through
generated, inaccessible old `epic13-*` temporary folders. No real test was excluded.
Pinned invocation (PowerShell, from workspace root):

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$taskEnconetTests = @(Get-ChildItem -LiteralPath Enconet/tests -File -Filter 'test*.py' | Sort-Object Name | Select-Object -ExpandProperty FullName)
& C:/xPY/vEnv/WikiEnconet/python.exe -m pytest @taskEnconetTests Enconet/scripts/tests Enconet/sieving/tests -q -p no:cacheprovider --basetemp Enconet/.test-tmp/scoring-refresh-full-pinned-20261009 --junitxml=Enconet/out/2026-10-09/scoring-fixture-refresh/full-suite-pinned.xml --tb=short
```

Focused invocation:

```powershell
& C:/xPY/vEnv/WikiEnconet/python.exe -m pytest Enconet/tests/test_epic16_benchmarks.py -q -p no:cacheprovider --basetemp Enconet/.test-tmp/scoring-refresh-focused-20261009 --junitxml=Enconet/out/2026-10-09/scoring-fixture-refresh/scoring-tests.xml
```

These temp directories already exist; a rerun must use a fresh reviewed name.
Running the test Python file directly did not execute pytest assertions and is
not counted as validation. The actual focused pytest invocation above did.

## Why the full suite failed — ELI5

We changed the label on the scoring test box, not the numbers inside it.
That test now passes. The large test set also opens files from the previous audit.
The owner-approved reset archived those results. Some tests still look in the old
location or assume old document numbers. They cannot test a fresh audit reliably.

All71 setup errors in the pinned XML group into these exact dependencies:

| Errors | Dependency |
|---:|---|
| 22 | Old RUN-20260728-01 dashboard file missing |
| 19 | Old RUN-20260728-01 absent from current DB |
| 8 | Old published evaluation package missing |
| 8 | Old candidate report missing |
| 5 | Old review_catalog.json missing |
| 4 | Bundle generation depends on old published package |
| 3 | Old DOC-0019 raw citation no longer represents the current source |
| 2 | Requirement test assumes Appendix B at derived/DOC-0019.txt; it is now a vendor source |

The55 assertion failures also include old dashboard/report/package/release/catalog
paths, old crumb counts and an empty legacy DATA corpus. Several are follow-on
assertions after those missing inputs. This is not evidence that all failing
features are correct: they still need isolated regression fixtures and a full rerun.
No test assertion was weakened and no historical data was restored into live audit
folders to hide the problem. Coverage emitted no-data warnings under the combined
invocation; no new coverage measurement is claimed.

## Phase and next action

Phase remains **findings_drafted**, with **G4 approved**. The scoring-version blocker
is resolved; the newly exposed full-suite failure is not bypassed. Report generation
and G5 release have not been performed. Benchmarks are not marked locked.

Next proposed job: one bounded regression-fixture isolation repair. Keep synthetic
tests self-contained and provide a controlled historical fixture for historical
characterization. Do not change live audit documents, findings, ratings or scores.
This goes beyond the authorized metadata-only refresh, so ask the owner before
changing the broader test infrastructure. Claude review remains deferred.
