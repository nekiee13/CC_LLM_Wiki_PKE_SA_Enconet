---
record_type: rollback_review_briefing
target: CC_Loto
gate_dependency: M4
target_tip: d5dc65e568ee73d82389e6e1d3fdf24122661adf
prepared_by: codex
independent_reviewer: claude-code
state: awaiting_independent_review
live_target_write: none
---

# CC_Loto scoped rollback rehearsal briefing

## Review boundary

This packet asks Claude Code to reproduce a real Git recovery sequence in a disposable clone of the
exact published CC_Loto tip. Acceptance closes only the rollback-evidence prerequisite for a future
M4 packet. It does not authorize a revert or other write in live CC_Loto, guidance alignment, an M4
decision, a tag, release, hosted mutation, or index refresh. M4 remains closed.

## Authority and harness

- Read-only source: `C:\xPY\xPrj\CC_Loto` / `nekiee13/CC_Loto`.
- Required live, fetched, and local tip: `d5dc65e568ee73d82389e6e1d3fdf24122661adf`.
- Required source state: divergence `0/0`, empty porcelain, zero live tags.
- Harness: [`rendered/run_loto_rollback_rehearsal.py`](rendered/run_loto_rollback_rehearsal.py).
- Harness SHA-256: `960C7489079BA5A3EDF422B1CD7E15B13C772D9E799D0182419DB4F92A49F6A7`.

The harness writes only inside a newly created OS-temporary clone and isolated output/cache roots.
It requires the live source to be clean at the frozen tip before cloning and never invokes Git with
a live-target write operation.

## Rehearsal sequence

The planned disposable slice has support skeleton, coordination evidence, and a later handoff step.
The harness performs and proves this sequence:

1. Clone the frozen target without hardlinks and hash all 165 baseline tracked files.
2. Commit support skeleton `d88f8588e8d9a7be1b8572d93aa2ffa28169dbf8`.
3. Commit unrelated concurrent owner work `f30373bca9c335d0a2e8b2d76a5116a44f99ae1a`.
4. Commit support coordination evidence `9e46f95d87cb49af48c79bb816849f61dd8d41f0`.
5. Inject an unavailable native interpreter into the installed aggregate; require exit `1` and
   `native-contract-support: unavailable`. Abort before the planned handoff step.
6. Run real `git revert --no-edit 9e46f95...`, creating revert `44123c0...`.
7. Run real `git revert --no-edit d88f858...`, creating revert `b454e27...`.
8. Prove both support paths are absent, every baseline tracked-file hash is unchanged, concurrent
   owner bytes retain SHA-256 `9DA8FE15...D0657`, and the only baseline-to-recovered diff is
   `owner-concurrent.txt`.
9. Require clean porcelain and preserved history containing all five named disposable commits.
10. Rerun the installed aggregate, direct coordination validator, and proportional native layers.

The fixed commit identity and timestamps make the disposable commit IDs deterministic at the frozen
tip. The Git history is preserved; the harness never uses reset, checkout restoration, recursive
cleanup of the clone, force push, or history rewriting.

## Exact reproduction

From the Wiki root:

```powershell
$native = Join-Path $env:TEMP 'cc-loto-support-venv\Scripts\python.exe'
python doc\support-transfer\rendered\run_loto_rollback_rehearsal.py `
  --source C:\xPY\xPrj\CC_Loto --native-python $native
git -c safe.directory=C:/xPY/xPrj/CC_Loto -C C:\xPY\xPrj\CC_Loto `
  ls-remote origin refs/heads/main refs/tags/*
```

## Required reviewer findings

Claude should independently confirm the harness hash and scope, reproduce all five disposable commit
IDs, inspect both revert parents/diffs, verify the 165-file before/after hash equality and concurrent
file preservation, rerun post-recovery validators/tests, and recheck the live target unchanged.

Post-recovery expected states are: aggregate exit `0`; coordination 0 errors/0 warnings; handoff
`not-configured`; support schema parsed=1; focused support contract passed; native core-unit 42/42,
contract 30/30, and state-integrity 3/3. Optimization-core, integration, webapp, optional, and hosted
CI remain `not-run` under the accepted support-only profile.
