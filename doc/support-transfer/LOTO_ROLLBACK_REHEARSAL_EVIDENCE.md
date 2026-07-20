---
record_type: rollback_rehearsal_evidence
target: CC_Loto
target_tip: d5dc65e568ee73d82389e6e1d3fdf24122661adf
recorded_at_utc: 2026-07-20T02:33:32Z
executed_by: codex
review_state: awaiting_claude
live_target_write: none
---

# CC_Loto scoped rollback rehearsal evidence

## Outcome

The corrected disposable-clone rehearsal exited `0`. It created two named support commits around a
real unrelated concurrent commit, injected a required validation failure, reverted only the two
support commits with new Git commits, preserved every original tracked byte and the concurrent work,
and passed all required post-recovery validation. Live CC_Loto remained clean and unchanged.

## Source and recovery point

| Fact | Observed |
|---|---|
| Live/local/fetched target tip | `d5dc65e568ee73d82389e6e1d3fdf24122661adf` |
| Live tags | zero |
| Target divergence / porcelain | `0 0` / empty |
| Disposable baseline tree | `55cde0d29686a5220a775ee97e6793e805a4e2ee` |
| Baseline tracked files hashed | 165 |
| Disposable BOARD SHA-256 before/after | `9F1D6C74F96AB967E91B621A3FBB1B3520DA2F072F22E976C97E05A3DED265C9` / same |
| Live target writes | none |

## Exact disposable history

| Role | Commit |
|---|---|
| Support slice commit 1 | `d88f8588e8d9a7be1b8572d93aa2ffa28169dbf8` |
| Concurrent unrelated commit | `f30373bca9c335d0a2e8b2d76a5116a44f99ae1a` |
| Support slice commit 2 | `9e46f95d87cb49af48c79bb816849f61dd8d41f0` |
| Revert of support commit 2 | `44123c047519faa77fd73d97bbe5ffa4556d64f1` |
| Revert of support commit 1 | `b454e275561b1a5f215fb531da0c878fe89b75a2` |

Both revert commands were literal `git revert --no-edit <named-support-commit>`. The concurrent
commit was never named for reversal. All five commits remained reachable from the recovered HEAD.

## Failure and recovery proof

- The installed aggregate was invoked after the second support commit with a deliberately absent
  native executable. It returned exit `1` and reported `native-contract-support: unavailable`.
- No third slice commit was made after the abort trigger.
- After the two reverts, both rehearsal support paths were absent.
- The SHA-256 map of all 165 pre-existing tracked paths matched byte-for-byte.
- `owner-concurrent.txt` remained byte-identical at SHA-256
  `9DA8FE15112208C2513D6AEC73D7D2CFB0589CD03771A0E1CCA08772A89D0657`.
- `git diff --name-only d5dc65e..HEAD` returned exactly `owner-concurrent.txt`.
- Porcelain was empty before post-recovery validation and after it.

## Post-recovery validation

| Check | Exit | Result |
|---|---:|---|
| Installed aggregate `--no-record` | 0 | coordination passed 0/0; handoff not-configured; schemas parsed=1; focused support contract passed; optional and hosted not-run |
| Direct `tools/support/agent_coord.py .` | 0 | 0 errors, 0 warnings |
| Native core-unit | 0 | 42/42 |
| Native contract | 0 | 30/30 |
| Native state-integrity | 0 | 3/3 |

Optimization-core, integration, webapp, optional, and hosted CI were not run and are not represented
as passed. The rollback proof concerns support publication recovery, not default product-suite health.

## Attempt accounting

The first harness invocation successfully cloned, created the three disposable commits, and produced
the intended fail-closed aggregate result. Its first revert was then refused with exit `128` because
the harness provided committer identity but omitted the author identity Git also requires when making
a revert commit. No recovery success was claimed. The harness was corrected to supply both identities
and rerun from a fresh disposable clone. The corrected run produced the deterministic commits and
successful evidence above. The failed clone was automatically discarded; neither attempt wrote the
live target.

## Remaining gates

Claude's independent reproduction and acceptance are still required. The guidance pair remains not
synchronized and needs an owner-scoped decision. M4 packet preparation and the owner decision remain
separate and closed.
