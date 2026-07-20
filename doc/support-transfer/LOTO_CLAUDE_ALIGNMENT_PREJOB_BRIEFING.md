---
record_type: slice_prejob_briefing
slice: claude-guidance-alignment
step: 2
target: CC_Loto
version: 1
recorded_at_utc: 2026-07-20T03:36:40Z
authorized_by: LOTO_GUIDANCE_ALIGNMENT_APPROVAL.md item 2
implementer: claude-code
reviewer: codex
target_parent: a4ccbe144a2027745e74215e2136dbe6fe610497
status: pre-write-review-required
---

# CC_Loto Claude-owned minimal alignment — pre-job briefing v1

This packet opens independent pre-write review only. It authorizes no CC_Loto write, commit, push,
dependency/product change, or M4 transition.

**Roles are reversed for this slice**, as they were for the earlier Claude-owned correction:
`CLAUDE.md` is Claude-owned, so Claude Code authors and **Codex is the independent reviewer**. Codex
must not edit the candidate; findings return as coordination messages.

## Gate satisfied

Owner approval item 2 permits this step only after the Codex-owned `AGENTS.md` correction is
published and closed. That happened: step 1 is live at `a4ccbe14`, both agents independently
verified the live tip, and Codex released its claim. The renderer additionally refuses to run unless
the parent `AGENTS.md` object equals the published `42571a2c`, so the ordering is enforced
mechanically and not merely by intent.

## Exact content scope — one Claude-owned modification

Content commit A would copy the sole byte authority in
[`rendered/loto-claude-alignment/CLAUDE.md`](rendered/loto-claude-alignment/CLAUDE.md) exactly:

1. modify root `CLAUDE.md` — append one `## Support system and coordination` section;
   55 added lines, 0 removed.

No `AGENTS.md`, `.agents/`, `.claude/`, `CX_` record, coordination or support record, product
source, dependency, workflow, test, data/model/output, index, tag, or release path is in A.

Exact review inputs:

- [`LOTO_CLAUDE_ALIGNMENT_RENDER_EVIDENCE.md`](LOTO_CLAUDE_ALIGNMENT_RENDER_EVIDENCE.md)
- [`LOTO_CLAUDE_ALIGNMENT_DRY_RUN_EVIDENCE.md`](LOTO_CLAUDE_ALIGNMENT_DRY_RUN_EVIDENCE.md)
- [`rendered/render_loto_claude_alignment.py`](rendered/render_loto_claude_alignment.py)
- [`rendered/loto-claude-alignment/CLAUDE.md`](rendered/loto-claude-alignment/CLAUDE.md)

## What the section covers

The six groups the owner approved, kept deliberately brief and pointing at the controlling
authorities rather than restating them: ownership and shared-neutral boundaries; support-oriented
read order with live-Git preflight; the immutable coordination lifecycle including evidence-backed
message handling and confirmed-only archival; validation truth with the support-operator dependency
boundary and fail-closed semantics; named-commit revert-first recovery with unrelated-work
preservation; and explicit owner gates including that M4 is never inferred.

It also carries three points this transfer established the hard way: an applicable check that could
not run must fail closed and a zero exit must never stand in for a check that did not execute; a
passing support aggregate is evidence about the support system, not the product test suite; and a
revert conflicting with later work on the same append-only records needs owner-directed resolution.

## What it deliberately does not do

- It does not copy `AGENTS.md`, and it does not duplicate `support/` mechanics.
- It does not enumerate the check-state vocabulary. It references
  `support/schemas/handoff.schema.json` and `tools/validate_support.py` as the authority, and the
  renderer fails if any enumeration appears. This is the direct lesson of step 1, where a
  transcribed list drifted from a contract that already existed in machine-readable form.
- It does not touch existing product guidance, and the renderer asserts seven pre-existing product
  anchors survive.
- It does not claim the guidance pair is synchronized; it states the precondition for that claim,
  and the renderer fails on any synchronization overclaim.

## Preflight immediately before content commit A

1. Reverify `HEAD == origin/main == a4ccbe14...`, divergence `0 0`, empty porcelain, zero tags.
2. Reverify `CLAUDE.md` is at parent object `3edd8750` and `AGENTS.md` at `42571a2c`.
3. Require Codex's explicit acceptance of this packet and its one-path scope.
4. Require the pushed Wiki packet commit containing this exact candidate; rerun the renderer and
   require SHA-256 `0DE42FEA...7A35` and Git object `689a48b6`.

Any mismatch is a stop condition.

## Proposed two-commit protocol after acceptance

1. **Content commit A:** replace only `CLAUDE.md`; stage exactly one path; require the staged Git
   object to equal `689a48b6`; commit locally.
2. **Validation at clean A:** run the support aggregate and `python tools/support/agent_coord.py .`
   with the support-operator environment, requiring exit `0`, 0 errors, 0 warnings, and a
   byte-identical board; re-run the append/anchor/ownership checks and the three native layers.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md` to record A's
   identity, literal commands and exits, native counts, the schema-pinned vocabulary decision, and
   the fact that publication of this step still does not by itself establish synchronization.
4. **Validation at clean B:** repeat the checks; prove `B^ == A`, one-path A, two-path B, and that
   all objects match their reviewed authorities.
5. Keep A and B local until Codex independently reviews the committed objects and explicitly
   authorizes the exact fast-forward push.

Rollback, only on reviewer/owner direction, is a new revert of B followed by A. Reset, force push,
broad cleanup, or restoration of unrelated paths is prohibited.

## After publication

Synchronization is still not automatic. Once this step is live and closed, each agent must
independently confirm the shared anchors at the live tip for its own side before any record
describes the pair as synchronized. M4 remains a separate owner-gated packet and decision, and
nothing in this slice approves or advances it.

## Stop conditions

Stop on target drift; any path beyond A's one modification or B's two evidence modifications; any
non-append change to the parent bytes; byte mismatch; a prose enumeration of check states; an
unauthorized synchronization claim; loss of a pre-existing product anchor; any edit to Codex-owned
or shared-neutral content; non-zero coordination validation; board change; native regression;
sensitive or product data; or reviewer finding.
