---
record_type: local_ab_implementation_evidence
target: CC_Loto
slice: codex-guidance-correction
recorded_at_utc: 2026-07-20T03:17:17Z
wiki_packet_commit: 82c3595e666dbee5e50e78634c456c011009cc6f
owner_approval_commit: 8f808757655530fb44c9862b703f76ed2cab742c
target_parent: d5dc65e568ee73d82389e6e1d3fdf24122661adf
content_commit_a: 2aebed6bd2e96d27640776376af7a4e06a7e2030
evidence_commit_b: a4ccbe144a2027745e74215e2136dbe6fe610497
publication_state: local_unpushed
implementer: codex
reviewer: claude-code
---

# CC_Loto Codex-guidance correction — local A/B implementation evidence

## Gate and chain

- Claude accepted the pre-write packet with no findings in
  `CC_2026-07-20T030806Z_loto-codex-guidance-correction-packet-accepted`, independently reproducing
  the exact candidate, 3/2 diff, parent facts, disposable overlay, aggregate, board, and native
  42/30/3 results.
- Final preflight at published tip `d5dc65e568ee73d82389e6e1d3fdf24122661adf` found live, fetched,
  and local main equal, divergence `0 0`, clean porcelain, zero tags, `AGENTS.md` at parent object
  `34b7eb93095022bea137e2a0c2313f356bfa0f28`, and `CLAUDE.md` at
  `3edd87504e76a97d8ba46ecf40e81b8ad894299f`.
- Local chain is exactly `d5dc65e -> 2aebed6 (A) -> a4ccbe1 (B)`.
- CC_Loto is clean and two commits ahead of `origin/main` (`0 2`). **Nothing was pushed.**

## Content commit A

Commit `2aebed6bd2e96d27640776376af7a4e06a7e2030` (`guidance: correct support check
vocabulary`) has parent `d5dc65e568ee73d82389e6e1d3fdf24122661adf` and modifies exactly one path:

| Operation | Path | Committed object |
|---|---|---|
| modify, Codex-owned | `AGENTS.md` | `42571a2c5f67b5a11759f38d7d65f50f156087c3` |

The staged and committed object matched the reviewed authority. The diff is 3 additions and 2
deletions. It introduces the canonical seven literal check states and says `blocked` is a
handoff/blocker state, never a check result. The existing no-false-pass warning remains unchanged.
Claude-owned `CLAUDE.md` remains at `3edd87504e76a97d8ba46ecf40e81b8ad894299f`.

At clean A, the target support aggregate exited `0`: coordination passed at 0 errors and 0
warnings, bootstrap handoff was `not-configured`, one support schema parsed, and focused support
tests passed. Direct coordination exited `0`; `coordination/BOARD.md` remained byte-identical.
Target-native core-unit, contract, and state-integrity passed 42/42, 30/30, and 3/3, all exit `0`.

## Evidence commit B

Commit `a4ccbe144a2027745e74215e2136dbe6fe610497` (`support: record Codex guidance
correction evidence`) has parent A and changes exactly two paths:

| Path | SHA-256 | Committed object |
|---|---|---|
| `support/log.md` | `8979085740A3D7D28E60729863A1DDF7D48F2F88F33FBA336BA7166D97C9B45D` | `2cec367961c5994a42d83ce64f5d24c3f0feaa5d` |
| `support/current-status.md` | `5E0CD01F36B2C1A4DAF20CE601D9FA007D284311AC190CAC3824497ED38EA4E5` | `e45345a3b4fdf1144d869f82076f9cfb89e78d21` |

The byte authority is
[`rendered/loto-codex-guidance-correction-evidence-b/`](rendered/loto-codex-guidance-correction-evidence-b/),
produced by
[`rendered/render_loto_codex_guidance_correction_evidence_b.py`](rendered/render_loto_codex_guidance_correction_evidence_b.py).
The renderer derives `support/log.md` from the committed-A blob and requires the entire prior prefix
plus exactly two contract-shaped appended events. It fails closed on synchronization overclaims and
requires the explicit non-synchronization statement. Both staged Git objects matched the authority
before commit.

At clean B, `B^ == A`, `A^ == d5dc65e`, A changes exactly `AGENTS.md`, and B changes exactly the
two support evidence paths. The aggregate, direct coordination validation, and native layers were
rerun: all exited `0`, native counts were again 42/42, 30/30, and 3/3, and the board remained
byte-identical. The worktree is clean at `0 2`.

## Truthful exclusions and attempts

Optional, optimizer-core, integration, webapp, and hosted-CI layers were **not run** and are not
reported as passed. Product baseline health is not inferred from this documentation-only slice.

Two environment-control failures occurred and changed no target content or Git history: the first
disposable-render invocation could not create its OS-temp overlay under sandbox permissions, and the
first staging invocation could not create the target index lock. Each was rerun with the required
permission; the renderer then passed, and staging was followed by exact staged-object comparison.
No validation failure is omitted.

## Standing gate state

The guidance pair remains **not synchronized**. This is owner-approved minimal-alignment step 1
only. The Claude-owned step 2 stays closed until A/B are independently reviewed, published, and
closed. M4 remains closed.

## Reviewer handoff and recovery

Claude must independently inspect the A/B identities and parent chain, exact path sets, committed
objects against the Wiki authorities, append-only proof, status truth, aggregate and native results,
and clean `0 2` target state. No push is authorized by this record. On explicit acceptance, Codex
may push exactly A followed by B as one normal fast-forward and report live remote state. Recovery,
only on reviewer/owner direction, is a new revert of B followed by A; reset, force push, and unrelated
cleanup are prohibited.
