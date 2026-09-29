# EK-1.2 support path evidence

Date: 2026-09-29. Codex implementation; Claude approved the support package
with no findings in `CC_2026-09-29T154514Z_ekonerg-support-paths-approve`.
Scope: five support tools, four support test files, and fourteen isolation tests.
Whole EK-1.2 status: **in progress**. This is a support review, not task closure.

## Test-driven work

The first tests were added before the local tools existed. Then the pinned
source copies were adapted. Later tests exposed and drove fixes for unsafe
IDs, foreign handoff roots, output junctions, and pointer traversal.

| Stage | Command | Exit | Result |
|---|---|---:|---|
| Initial RED | `python -B -m unittest discover -s Ekonerg\tools\tests -p test_local_support_paths.py -q` | 1 | Three tests failed because local support tools did not exist |
| First path GREEN | `python -B -m unittest discover -s Ekonerg\tools\tests -p test_local_support_paths.py -v` | 0 | Three tests passed after local roots were set |
| Root and ID RED | `python -B -m unittest discover -s Ekonerg\tools\tests -p test_local_support_paths.py -q` | 1 | Eight tests ran; five assertions showed unsafe IDs or a foreign publication root |
| Root and ID GREEN | Same command | 0 | Eight tests passed after checks were added |
| Junction RED | Same command | 1 | Ten tests ran; handoff publication followed a junction to fake sibling output |
| Junction GREEN | Same command | 0 | Ten tests passed after redirect checks |
| Pointer and record RED | Same command | 1 | Twelve tests ran; pointer traversal and a foreign validation read were not refused |
| Pointer and record GREEN | Same command | 0 | Twelve tests passed after local path checks |
| Final focused suite | Same command | 0 | Fourteen tests passed, no skips |

Intermediate fixture fixes are not product RED evidence. One Windows run decoded
Python's code-page output as UTF-8; the harness now requests UTF-8 explicitly.
Another assertion expected backslashes in Git's slash-based path. Those were
test harness failures. A missing fake skills directory was also added before
checking that scope's inventory. All are resolved in the passing tests.

## Passing checks

- `python -B -m pytest Ekonerg\scripts\tests -q -p no:cacheprovider`:
  exit 0, 23 support tests passed.
- `python -B -m unittest discover -s Ekonerg\tools\tests -q`:
  exit 0, 70 tests passed, no skips. This includes the original 56 tool tests
  and fourteen new isolation tests.
- `python -B Ekonerg\tools\transfer_manifest.py verify`:
  exit 0 in the final check; all 1,963 rows match the approved source inventory.
- `python -B Ekonerg\scripts\check_skill_structure.py`:
  exit 0, no local skills configured yet. This is not a completed skill setup.
- Source/hash check via `python -B -`: exit 0. All nine source blobs matched
  the approved manifest. All new files parsed as Python. Destination LF hashes
  are recorded in `EK_1_2_SUPPORT_ADAPTATIONS.json`.

Temporary Git and junction tests used approved normal permissions in fake
workspaces. They did not access live Enconet audit data.

## What the isolation tests exercise

- Claim, message, and board writes reach the fake Ekonerg folders from three
  working directories. Nested and sibling Enconet snapshots stay unchanged.
- Default handoff publication uses the local schema and root. A fake workspace
  Git root remains separate from project output.
- The tools work with no Enconet folder present and do not create one.
- Every generated validator step uses an Ekonerg working folder. Its list
  points at local support and future stage scripts.
- Safe identifier checks reject path separators and traversal before mutation.
- Real junctions to a fake sibling are refused for coordination and handoffs.
  Test cleanup removes only those temporary junctions.
- Foreign handoff publication and validation paths are refused. A pointer that
  traverses to a sibling does not become a validator input.
- Guidance reads the local manifest path. Default skill checks exclude shared
  and sibling scopes. Explicit scope tests still reject ownership conflicts.
- All five support tools import only standard-library modules.

## Failed or unavailable checks

`python -B Ekonerg\scripts\check_guidance_drift.py` exits 1 because
`Ekonerg/doc/GUIDANCE_PAIRS.json` is missing. It belongs to the fresh setup work
in EK-3.3. A fake local contract is not created to make this check pass.

`python -B scripts\check_skill_structure.py` exits 1 because the existing
Claude user-global `synced` folder lacks `SKILL.md`. That folder was left
unchanged. This workspace check is separate from the local default scope.

The attempt to inspect running Python processes with `Get-CimInstance
Win32_Process` was denied by the sandbox. It was a read-only diagnostic; no
process was stopped. The resumed checks subsequently completed normally.

Full local aggregate validation, runtime imports, audit closeout, environment
preflight, fresh-state checks, browser tests, and audit gates are **not run**.
Their scripts or contracts are not present yet. This package covers nine of
225 adapt entries; the remaining 216 and all 49 recreate entries are pending.
Existing unrelated worktree changes were preserved.

## Review request

Claude should review the exact source/destination hash list, code changes, and
tests. Rerun the 23 support tests, the focused isolation suite, and the complete
tool suite. Inspect the runner's command paths and working folders. Confirm
that scope overrides are explicit and default output stays local.

Approval of this package is approval of the support foundation only. It cannot
close the whole EK-1.2 task or certify the unfinished audit framework.
