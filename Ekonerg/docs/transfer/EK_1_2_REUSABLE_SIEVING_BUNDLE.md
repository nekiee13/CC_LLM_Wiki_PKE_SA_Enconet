# EK-1.2 candidate: reusable sieving bundle

## What changed, and why

The next company should not need new code edits just to get a clean sieving
tool. `audit_template/sieving/v1/` now holds 21 versioned runtime files.
`audit_template/bootstrap_sieving.py` previews or copies them into an existing
project. The copied command runs from that project, even with no sibling audit.
The Ekonerg-local source copy only had company-specific comments made neutral;
no parsing or audit decision logic changed.

The bundle has an empty `canonical_codes` list and an empty active prompt map.
The Appendix B taxonomy is a **template**, not a ruling that Appendix B
applies. This batch did not add or approve sources, editions, QMS documents,
prompts, storage, or an audit run. Nothing was applied to the live Ekonerg
project by the new bootstrap.

## TDD evidence

1. Red: `python -B -m unittest discover -s audit_template/tests -q` exited 1
   because `bootstrap_sieving` did not exist.
2. Green: the same command exited 0 outside the sandbox: 3 tests passed.
   The tests check file hashes, empty intake settings, no Ekonerg name in the
   bundle code, preview with no writes, apply and safe repeat, and copied CLI
   use in two invented company roots. They also test conflicts and links.
3. Regression: `python -B -m unittest discover -s Ekonerg/sieving/tests -q`
   exited 0 outside the sandbox: 83 tests passed.
4. Regression: `python -B -m unittest discover -s Ekonerg/tools/tests -q`
   exited 0 outside the sandbox: 111 tests passed.
5. Regression: `python -B -m pytest Ekonerg/scripts/tests -q -p no:cacheprovider
   --tb=short --basetemp C:\Users\PC\AppData\Local\Temp\ekonerg-template-20260930-01`
   exited 0 outside the sandbox: 39 tests passed.
6. Provenance: `python -B Ekonerg/tools/transfer_manifest.py verify` exited 0:
   1,963 pinned rows and 275 dependency-scan files verified.

The first sandboxed attempts at the tests exited 1 because Windows denied
temporary-directory access. The same suites passed with approved execution
outside the sandbox. Those first attempts are **not** counted as passing.

## Review gate and limit

Claude review is pending. EK-1.2 stays open: this bundle covers the sieving
runtime, not every local support tool named in the plan. Do not infer that
Epic 1 or the full audit framework is complete. The owner must still decide
real source scope, editions, storage, and intake approval before ingestion.
