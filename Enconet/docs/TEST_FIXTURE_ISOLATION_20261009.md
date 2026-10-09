# Enconet — regression dependencies repaired in one batch

Owner authorization: **yes**, to one bounded test-dependency repair with no
audit-document or score changes. Decision: `TEST-FIXTURE-ISOLATION-ENCONET-20261009`.

## Result

**447 tests passed. Zero failed, zero errors, zero skipped.**
This includes all440 earlier tests and seven added safety/negative tests.
Current-code group:146 passed. Historical-characterization group:301 passed.
Two existing Typer/Click deprecation warnings remain; they are not hidden.

Both benchmark classes and all11 current phase checks pass. Guidance drift
check passes with0 errors. The project is now **findings_approved**, using
the already recorded G4 approval. G5–G7 remain pending.

The real conformance score remains **80.6%,1450/1800**. No evidence, source,
chapter, crumb, applicability ruling, evaluation or finding/action text changed.
The12 approved findings still await field verification. The18 approved actions
remain open. All36 incoming files remain hash-exact.

## Why this fixed the failures — ELI5

The old tests were opening the previous audit's files in today's audit folders.
After the approved reset, those files were no longer there. We moved the tests'
historical inputs into a separate test room. The tests still check the same
facts and numbers. Nothing was put back into the real audit.

The test room uses **current code and contracts**, with a verified historical
input/result snapshot. It does not run an old implementation to get green tests.
Assertions about62 historical evidence crumbs,68 legacy DATA files and exact
golden bytes are retained. The current audit's2,700 vendor crumbs are not changed
to match those historical numbers.

## Complete-suite command

From the workspace root, using the pinned interpreter:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& C:/xPY/vEnv/WikiEnconet/python.exe Enconet/scripts/run_regression_tests.py --output Enconet/out/2026-10-09/test-fixture-isolation/final
```

That exact final command exited0. The output already exists; a rerun must use
a new output directory. The runner refuses to overwrite prior test evidence.

- [Final group counts and exact subprocess commands](../out/2026-10-09/test-fixture-isolation/final/summary.json).
- [Current test report](../out/2026-10-09/test-fixture-isolation/final/current.xml).
- [Historical test report](../out/2026-10-09/test-fixture-isolation/final/historical.xml).
- [Current full log](../out/2026-10-09/test-fixture-isolation/final/current.log).
- [Historical full log](../out/2026-10-09/test-fixture-isolation/final/historical.log).

Running every historical test directly against live folders is not the complete
release method: those tests intentionally describe a frozen historical data set.
The documented runner executes every test file, with no skip list or weakened
assertions. Codex guidance now names it. Claude guidance remains unchanged;
Claude-side synchronization and substantive review are pending.

## Changes made

1. `scripts/regression_fixture.py` validates the archive checksum, CRC, exact
   manifest entries and358 payload hashes before extraction. It rejects unsafe
   archive paths, duplicates, agent infrastructure and existing/live targets.
   Current code is copied into a fresh `.test-tmp` workspace. Old evidence is
   extracted only there. Quarantined tools are copied for AST/inventory checks,
   never executed as repair scripts.
2. `scripts/run_regression_tests.py` routes all tests to the correct data context.
   It uses fresh temporary folders, writes full logs/XML, and checks live file
   hashes before and after. It also guards `CLAUDE.md`, `.claude` and all CC_
   messages/archive records. It keeps temporary workspaces for diagnostics.
3. Historical review validation can explicitly read the genuine reviewer record
   from its original location with `--decision-record-root`. No CC_ record is
   copied, rewritten or synthesized. The default remains project-local. A new
   negative test proves that an empty origin still fails.
4. Aggregate validation can explicitly use `--skill-origin` for a historical
   test workspace. Both agents' skills are read-only in the original project;
   neither skill tree is copied. Default runtime behavior remains local and
   strict; no pending-review exception or validator downgrade is introduced.
5. Only two existing test files changed to pass those explicit read-only origins.
   All their original assertions remain. Six new isolation safety tests and
   one reviewer-record negative test were added.

## Historical fixture control and limitations

The verified pre-reset ZIP SHA256 is
`38018c13eb9c17172c7c3486b4041dbb54e27618f78cfb9989ebb56cbfcfaedf`.
Provenance is recorded in [the reset record](ENCONET_RESET_20261007.md).
Its original reset-plan manifest verifies358 payload entries.

The local copy at `tests/fixtures/history/enconet-pre-reset-20261007.zip` is
Git-ignored under ADR-0002: full supplier data is not smuggled into Git as a
fixture. Provision its hash-exact copy from the controlled reset archive before
historical tests run on another machine. Missing/corrupt fixture data fails
explicitly; it does not skip tests. Historical reviewer-record checks also
require the genuine preserved record in this project's neutral coordination
archive. Normal audit runtime does not read the historical fixture.

Only hashes, test reports, code and documentation are committed. Test reports
contain traces; raw input documents remain in their controlled store.
Four generated isolated workspaces from the attempts/final run are retained
under `.test-tmp`; none is active audit data. No directories were deleted.

## Test-first and validation record

| Command/check | Exit | Result |
|---|---:|---|
| New safety pytest before helper existed | 1 | Expected ModuleNotFoundError; red stage reproduced |
| Safety pytest after implementation | 0 | Six safety tests passed |
| Complete runner, attempt1 | 1 | 152 current +288 historical passed; six fixture-routing/copy failures,zero errors |
| Complete runner, attempt2 | 1 | 146 current +300 historical passed; one remaining missing test-workspace dependency,zero errors |
| Complete runner, attempt3 | 0 | 146 current +301 historical passed;447total,zero skips |
| Complete runner, final, after stronger ownership guard | 0 | Same447tests; live audit and Claude-owned files unchanged |
| `python Enconet/scripts/run_all_validations.py --benchmarks --no-record` | 0 | 11 phase checks and both benchmark classes pass |
| `python Enconet/scripts/run_all_validations.py --no-record` after transition | 0 | Same checks including mandatory benchmarks at findings_approved |
| `python scripts/check_guidance_drift.py` | 0 | Zero errors; new full-suite wording remains Codex-only pending Claude sync |
| `python Enconet/out/2026-10-09/scoring-fixture-refresh/verify_metadata.py` | 0 | All19 original DB table hashes and rating mathematics unchanged |

All attempt logs/reports are preserved under `out/2026-10-09/test-fixture-isolation/`.
The earlier failed pinned suite remains historical evidence, not the latest result.

## Next action

Generate the Croatian evaluation report from the approved RUN-20261008-17
package, validate it and prepare the single G5 owner-review packet.
G4 and scoring-fixture permissions are resolved; do not ask for them again.
This repair did not release a report/dashboard or close field audit actions.
