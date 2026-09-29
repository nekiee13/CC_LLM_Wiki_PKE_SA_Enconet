# EK-0.2 validation evidence

Date: 2026-09-29. Codex implemented this review package. Claude review is pending.

## Identity and results

Source: `9f20430c95334daa4c3cedb7ee71b002bd3be739`.
Session starting HEAD: `ca2f4173b3fb32b5f87bc84e08c7919dc305248a`.
Branch: `main`. The source baseline is fixed even though coordination commits
have advanced HEAD. The local index is not used to collect source bytes.

| Check | Result |
|---|---|
| Inventory | All 1,963 tracked source files listed once |
| Treatment | 1 copy, 225 adapt, 49 recreate, 1,688 exclude |
| Selected source items scanned | 275 |
| Selected Python files parsed | 161, all marked adapt |
| Active workspace support set | All five tools and four tests included |
| Unclassified fallback rows | Zero |
| Local import candidate groups with only excluded files | Zero; static candidates are not full import resolution |
| Framework destinations written | Zero |

Generated artifact SHA-256 values, UTF-8 with LF line endings:

- `transfer-manifest.json`:
  `fd9d69ff5c7836c1696402aa7012177de3e625efd301274f8eeddedbaeafc3a4`
- `dependency-scan.json`:
  `bc6691b0b8d327713d672e57d7b0b3275db901b6fece5f71d490edcd6b927fbb`

The manifest records exact Git blob bytes, so Windows working-tree line endings
do not affect source hashes. `verify` compares parsed artifact content and every
row against the pinned source and policy. Review commits pin artifact formatting.

## TDD evidence

Run commands from the workspace root.

| Stage | Exact command | Exit | Observed result |
|---|---|---:|---|
| Initial RED | `python -m unittest discover -s Ekonerg\tools\tests -p test_transfer_manifest.py -v` | 1 | Expected missing `transfer_manifest` module before implementation |
| First implementation run | `python -m unittest discover -s Ekonerg\tools\tests -p test_transfer_manifest.py -v` | 1 | Twelve tests passed; temporary Git fixture was blocked by sandbox permissions |
| Approved rerun | `python -m unittest discover -s Ekonerg\tools\tests -p test_transfer_manifest.py -v` | 0 | Thirteen tests passed outside the sandbox |
| Extra-field RED | `python -m unittest discover -s Ekonerg\tools\tests -p test_transfer_manifest.py -v` | 1 | Eighteen tests ran; invented approval field was not yet rejected |
| Extra-field GREEN | `python -m unittest discover -s Ekonerg\tools\tests -p test_transfer_manifest.py -v` | 0 | Eighteen tests passed after strict top-level field validation |
| Final local aggregate | `python -m unittest discover -s Ekonerg\tools\tests -v` | 0 | All 26 tests passed: 18 manifest tests plus 8 existing readability tests |
| Artifact build | `python Ekonerg\tools\transfer_manifest.py build` | 0 | Generated metadata only; final counts above |
| Pinned-source verification | `python Ekonerg\tools\transfer_manifest.py verify` | 0 | Full inventory and dependency scan match |

The initial sandbox run failed during temporary repository setup and cleanup.
That failure was not a product RED result and was not reported as a pass. The
approved rerun exercised the real isolated Git fixture. No live project file was
changed to test dirty-source rejection. No broad temporary-directory cleanup was
attempted after the failed run.

The tests cover missing and added files, changed source bytes, forged hashes,
wrong commit, duplicate rows, unsafe targets, altered treatment, invented
approval fields/status, Claude ownership, link exclusion, local support copies,
empty files, Unicode paths, and committed-versus-dirty source selection.

## What is not proved yet

These checks prove inventory integrity, not a working clean framework. They do
not run copied audit scripts, database creation, migrations, intake, browser UAT,
scoring, or release gates. Those are not-run because this task creates no runtime.
Enconet aggregate validation is not a substitute for later Ekonerg tests.

The dependency scan is conservative and can return multiple same-name candidates.
Dynamic imports, path construction, generated outputs, and third-party dependency
closure still need the isolated tests in EK-1.2 and the runtime checks in EK-1.3.

No guidance or skills were edited. No shared package or browser installation was
changed. No shared index was refreshed. Existing Enconet and support-transfer
worktree changes were left untouched.

Claude must review both the machine list and the prose dependency dispositions.
Do not close EK-0.2 or start EK-1.1 until that verdict is recorded.
