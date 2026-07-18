---
record_type: support_transfer_prejob_briefing
slice: 5
version: 1
recorded_at_utc: 2026-07-18T14:27:12Z
authorized_by: M1_APPROVAL.md and M2_APPROVAL.md
implementer: codex
reviewer: claude-code
target_parent: 9841751e13213e3e8766f41ec2b140dd8dd8fd74
status: pre-write-review-required
---

# Slice-5 pre-job briefing — CC_FIN guidance and recovery safety

## Authority, roles, and exact boundary

The owner assigned Codex as implementer/author and Claude Code as independent reviewer.
Slice 5 modifies exactly two existing CC_FIN files:

1. `AGENTS.md` — correct stale packaging facts and add repository-local support navigation;
2. `docs/governance-transition.md` — replace the routine hard-reset example with an
   evidence-first, preservation-aware, approval-gated divergence-recovery runbook.

No other path enters content commit A. In particular, Codex does not modify `CLAUDE.md`,
`.claude/`, or any `CC_` record. The reviewed clean parent is published Slice 3c commit
`9841751e13213e3e8766f41ec2b140dd8dd8fd74`.

## Exact rendered proposal

`rendered/slice5/` contains the two final target files. `render_slice5.py` reads both
reviewed parent blobs directly, reads the parent `pyproject.toml`, and stops unless the
packaging evidence is setuptools backend, project `cc-fin` 2.1.0, and package discovery
under `src/`.

The `AGENTS.md` proposal:

- replaces the false statement that `pyproject.toml` is empty with the observed packaging
  metadata and the existing requirements-file dependency boundary;
- clarifies that packaging metadata exists while routine verification remains test-driven
  and a support change does not imply a build, tag, or release;
- adds ordered navigation through `support/README.md`, `HANDOFF.md`, current status/log,
  coordination board/messages/claims, and live Git state;
- preserves ownership and immutable coordination lifecycle rules and makes clear that the
  support core references rather than supersedes product authority.

The recovery proposal captures status, identities, divergence, and log before action;
requires exact-at-risk identification and preservation evidence; prefers fast-forward,
named-branch preservation, or reviewed revert; and states that the runbook does not itself
authorize hard reset, clean, force-push, recursive deletion, or history rewriting.

## BOARD non-impact

Neither proposed path is an input to the generated coordination board. The renderer builds
a disposable overlay of accepted Slices 1, 2, 3, and 3c, applies only the two proposed files,
runs the installed target validator without board generation, and compares raw BOARD bytes.
Validation returned exit 0 with 0 errors and 0 warnings and BOARD was byte-identical.
Therefore Slice 5 has no BOARD modification and needs no scope amendment.

## Reproduction and preflight

Run from the Wiki root with a writable temporary directory:

`$env:PYTHONDONTWRITEBYTECODE='1'; python doc/support-transfer/rendered/render_slice5.py`

Expected exit 0: exact two-file inventory, verified packaging facts, recovery safeguards,
target validation 0/0, and unchanged BOARD. Two consecutive runs reproduced both files
byte-for-byte:

- `AGENTS.md`: `6680CA0FEE9E686D131FF9C92338A80E505D9776C4D9801CBF6FB17A014D890E`
- `docs/governance-transition.md`: `969EBB514B2F0DE03CFD75EB18D9593FB1A15282033C4FCB55EADF1674EC16AB`

Workspace guidance-drift validation also returned exit 0: 0 errors, 3 pairs, 39 anchor
rules, and 8 documented differences. Immediately before target write, require live remote,
`origin/main`, and local HEAD equal the reviewed parent, divergence `0 0`, empty porcelain,
unchanged parent blobs, and a fresh 2/2 deterministic render. Stop on any drift, collision,
scope expansion, sensitive content, runtime artifact, or validation change.

## Two-commit target protocol

1. **Content commit A:** replace exactly the two target files from the rendered tree; stage
   only those paths; require staged blobs to be byte-identical to the reviewed render; commit
   locally only after the 2/2 comparison.
2. At clean A run `$env:PYTHONDONTWRITEBYTECODE='1'; python scripts/agent_coord.py .`;
   require exit 0, 0 errors/0 warnings, and BOARD byte-identical to A's parent.
3. At clean A run
   `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --continue-on-collection-errors -q --tb=no --junitxml="$env:TEMP\fin_slice5_A.xml"`.
   Expected exit 1 only for the normative 54-tuple baseline, with 0 new, 0 gone, and
   0 mutated tuples relative to the accepted parent evidence.
4. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md`.
   Record A's full SHA and committer UTC, literal commands and integer exits, validator 0/0,
   native tuple evidence, BOARD identity, and reviewer-gate state.
5. At clean B rerun the target command and native command using `fin_slice5_B.xml`;
   require target 0/0, the same 54 tuples, and A-to-B tuple identity.
6. Confirm A is exactly the two reviewed blobs, `B^ == A`, and `A..B` changes exactly the
   two evidence files. Submit the complete evidence to Claude Code. Do not push CC_FIN before
   independent review acceptance.

Any byte, scope, authority, validation, baseline, BOARD, ownership, or reviewer defect is a
stop. Failed or unavailable commands retain their literal state and integer exit; expected
native red is never relabeled as a pass.
