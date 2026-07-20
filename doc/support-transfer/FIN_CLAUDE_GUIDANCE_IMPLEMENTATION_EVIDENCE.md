---
record_type: local_ab_implementation_evidence
target: CC_FIN
slice: claude-guidance
recorded_at_utc: 2026-07-20T21:36:00Z
wiki_packet_commit: 35a0a7b0d330bbdce2835b40f960cc47f4c4aa28
target_parent: 9308e25bbd1177ba69b8075210e1c5e079213fc5
content_commit_a: 16b8d80eea93231e984a30c61c2fa5c836e80710
evidence_commit_b: 41e8dccf8262ca06da24eed66d3ec4ee03e94bd2
publication_state: local_unpushed
implementer: claude-code
reviewer: codex
---

# CC_FIN Claude-owned guidance - local A/B implementation evidence

## Gate and chain

- Codex accepted the reparented pre-write packet with no finding in
  `CX_2026-07-20T212856Z_fin-claude-guidance-reparent-accepted`, having reproduced the unchanged
  candidate object and the reparent-only renderer diff.
- Preflight passed before any write: HEAD == `origin/main` == `9308e25bbd1177ba69b8075210e1c5e079213fc5`,
  divergence `0 0`, porcelain empty, zero tags, `CLAUDE.md` absent, `AGENTS.md` at `4cca3734`.
- Local chain is exactly `9308e25 -> 16b8d80 (A) -> 41e8dcc (B)`.
- CC_FIN is clean and two commits ahead of `origin/main` (`0 2`). **Nothing was pushed.**

## Content commit A

Commit `16b8d80eea93231e984a30c61c2fa5c836e80710` (`support: add Claude guidance file`) has parent
`9308e25...` and creates exactly one path:

| Operation | Path | Committed object |
|---|---|---|
| create, Claude-owned | `CLAUDE.md` | `ecaf1abf5e7a7771d72166f17e4bd9c86c92831c` |

- The staged object was compared to the reviewed authority before committing and matched.
- `git diff --cached --numstat` reported `73 0`; `git diff --cached --check` exited `0`.
- `AGENTS.md` remains `4cca3734` in A. No other path is touched.

At clean A, `python scripts/agent_coord.py .` exited `0` with 0 errors and 0 warnings, board
byte-identical; `python scripts/validate_support.py --no-record` exited `0` with literal states:
coordination passed, handoff not-configured, support-schemas passed, native-pytest passed,
optional-cpi not-configured, targeted-ruff not-configured, hosted-ci not-run.

## Evidence commit B

Commit `41e8dccf8262ca06da24eed66d3ec4ee03e94bd2` (`support: record Claude guidance validation
evidence`) has parent A and changes exactly:

- `support/log.md` - object `75878f3e88730bc211e03f76d9fbe88d28d82c2a`
- `support/current-status.md` - object `94adf319ce80fdd464af3ac112948fb9d97f4429`

The reviewed B authority is
[`rendered/fin-claude-guidance-evidence-b/`](rendered/fin-claude-guidance-evidence-b/), produced by
[`rendered/render_fin_claude_guidance_evidence_b.py`](rendered/render_fin_claude_guidance_evidence_b.py).
That renderer derives the log from the committed A blob and proves append-only rather than asserting
it: published prefix preserved, exactly two appended pipe-delimited events. It also refuses any
alignment overclaim, requires the explicit non-alignment statement, and asserts both `AGENTS.md` and
A's `CLAUDE.md` bytes are untouched. Both staged objects were compared to the authority before
committing and matched.

At clean B: `B^ == A`; `A^ == 9308e25`; A creates 1 path, B modifies 2; `CLAUDE.md` is `ecaf1abf`
and `AGENTS.md` is `4cca3734`; coordination exit `0` (0/0) with board byte-identical; aggregate exit
`0`; divergence `0 2`; worktree clean.

## Truthful states and disclosures

The aggregate's optional-cpi, targeted-ruff (both not-configured) and hosted-ci (not-run) states are
recorded literally and are not represented as passed. `native-pytest` passed the two focused support
test modules; broader product pytest layers are outside this documentation-only create and were not
run.

`CLAUDE.md` states the current `scripts/validate_support.py` limitation truthfully: it treats only
`failed` as failing and can emit `unavailable`, so an applicable check it could not run still yields
exit `0`. This slice does not fix that aggregate defect; it is separate owner-facing scope, already
flagged to the owner.

## Standing non-alignment

Neither A nor B claims the guidance pair is aligned, and the renderer fails closed on such a claim.
Publication is a precondition; each agent must independently confirm the live shared meanings at the
published tip before any record calls the pair aligned. ADR-SUP-0001 stays Accepted / Pending.

## Reviewer handoff and recovery

Codex must independently inspect A/B identities, the parent chain, exact path sets, committed objects
against the Wiki authorities, the append-only proof, status truth, ownership boundaries, validation,
and the clean `0 2` state. No push is authorized by this record. On explicit acceptance, Claude Code
may push exactly A followed by B as one normal fast-forward and report live remote state for closure
verification. Recovery, only on reviewer/owner direction, is a new revert of B followed by A; reset,
force push, and unrelated cleanup are prohibited.
