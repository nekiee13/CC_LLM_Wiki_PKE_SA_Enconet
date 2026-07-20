---
record_type: disposable_dry_run_evidence
target: CC_Loto
slice: 6
recorded_at_utc: 2026-07-20T01:34:11Z
target_parent: f549b40665c2321ff46168d43c67b2f2f9422bd5
---

# CC_Loto Slice 6 validators/tests — disposable dry-run evidence

## Result

The exact three-file candidate was overlaid twice on copies of published CC_Loto under short
disposable `%TEMP%\ls6-*` roots. Each copy was initialized as a fixture Git repository before
validation, so the final empty porcelain independently proves that `--no-record`, focused tests,
native checks, and the failure probe did not alter tracked content. The real target remained clean,
unchanged, and synchronized at `f549b40`.

| Check | Result | Disposition |
|---|---:|---|
| Exact candidate paths | 3 new, 0 modified | passed |
| Python syntax compilation | 3/3 | passed |
| Fixed content rerender differences | 0/3 | passed |
| Installed coordination check | `passed`, 0 errors/0 warnings | passed |
| Bootstrap handoff check | `not-configured` | truthful non-pass |
| Support schema check | `passed`, 1 parsed | passed |
| Focused native support pattern | 5/5, exit `0` | passed |
| Optional native layer in aggregate | `not-run` | truthful non-pass |
| Hosted CI in local aggregate | `not-run` | truthful non-pass |
| Generated board after aggregate | byte-identical | passed |
| `--no-record` tracked mutation | none | passed |
| Applicable `failed`, `unknown`, `unavailable` probes | aggregate exit `1` each | passed |
| Deliberate/non-failure state probes | aggregate exit `0` each | passed |
| Missing `--native-python` executable | native check `unavailable`, aggregate exit `1` | passed |
| Product interpreter used as support operator | coordination `unavailable`, aggregate exit `1` | passed |
| Non-Git source export | 5 discovered; tracked digest skipped 1 | passed |
| Enclosing-repository guard | top-level must equal candidate root | enforced |
| Final disposable porcelain | empty | passed |
| Real target divergence/porcelain | `0 0` / empty | passed |

## Proportional target-native layers

The isolated target-requirements interpreter ran the existing Loto runner with output and model
cache redirected outside each disposable repository:

| Layer | Tests after candidate | Exit | Result |
|---|---:|---:|---|
| `core-unit` | 42 | 0 | passed |
| `contract` | 30 | 0 | passed |
| `state-integrity` | 3 | 0 | passed |
| Required proportional total | 75 | 0 | passed |

The contract layer grows from 25 to 30 solely because the candidate adds five focused tests.
Optimizer-core, integration, webapp, and optional layers were not made applicable by this focused
support-tool slice and were **not run**; that is not a pass.

## Attempt accounting

For v1, the initial invocation was blocked before overlay creation by the filesystem sandbox denying
the renderer access to its system-temporary child directory. The same command was approved outside
that sandbox and completed successfully; a second approved v1 invocation also succeeded. Claude's
independent review then found the unavailable/unknown exit-code and Git-root defects. Codex accepted
both findings and produced v2. Two approved complete v2 invocations succeeded, reproduced all
corrected hashes, exercised the non-Git skip, and passed the expanded fail-closed probes. No attempt
or superseded result is excluded.

## Stop conditions

Stop before any CC_Loto write on target drift, dirty status, path collision, a fourth content path,
byte mismatch, pytest/dependency/product/workflow/agent-owned change, false state, tracked mutation,
board change, focused/native regression, sensitive content, or reviewer finding. Aggregate
validation, rollback evidence, guidance-alignment scope, and M4 remain separately gated.
