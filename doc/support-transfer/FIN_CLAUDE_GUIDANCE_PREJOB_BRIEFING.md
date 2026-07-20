---
record_type: slice_prejob_briefing
slice: claude-guidance
target: CC_FIN
version: 1
recorded_at_utc: 2026-07-20T13:24:00Z
authorized_by: ADR-SUP-0001 (accepted / pending)
implementer: claude-code
reviewer: codex
target_parent: e74147f3309e1835d28d7c248e00cdcbde2f1796
status: pre-write-review-required
---

# CC_FIN Claude-owned guidance creation - pre-job briefing v1

This packet opens independent pre-write review only. It authorizes no CC_FIN write, commit, push,
dependency/product change, or alignment claim.

**Roles are reversed for this slice**, as agreed: `CLAUDE.md` is Claude-owned, so Claude Code
authors and **Codex is the independent reviewer**. Codex must not edit the candidate; findings
return as coordination messages.

## Gate

ADR-SUP-0001 records the owner's minimal-alignment decision as accepted with implementation pending,
and gates the two guidance slices independently - neither depends on the other. This is the
Claude-owned side: create `CLAUDE.md`. The Codex-owned `AGENTS.md` completion is separate and may
proceed in either order.

## Exact content scope - one Claude-owned create

Content commit A would copy the sole byte authority in
[`rendered/fin-claude-guidance/CLAUDE.md`](rendered/fin-claude-guidance/CLAUDE.md) exactly:

1. create root `CLAUDE.md` (5062 bytes, LF-only).

No `AGENTS.md`, `.agents/`, `.claude/`, `CX_` record, coordination/support record, product source,
dependency, test, workflow, data, index, tag, or release path is in A.

Exact review inputs:

- [`FIN_CLAUDE_GUIDANCE_RENDER_EVIDENCE.md`](FIN_CLAUDE_GUIDANCE_RENDER_EVIDENCE.md)
- [`FIN_CLAUDE_GUIDANCE_DRY_RUN_EVIDENCE.md`](FIN_CLAUDE_GUIDANCE_DRY_RUN_EVIDENCE.md)
- [`rendered/render_fin_claude_guidance.py`](rendered/render_fin_claude_guidance.py)
- [`rendered/fin-claude-guidance/CLAUDE.md`](rendered/fin-claude-guidance/CLAUDE.md)

## What the file covers

A short product-orientation section that links CC_FIN's existing authorities (`README.md`,
`docs/refactor/phase1_rules.md`, `AGENTS.md`) without duplicating them, then a
`## Support system and coordination` section exposing the five meanings CC_FIN's installed
`coordination/templates/guidance-semantics.template.md` requires: ownership boundaries; support read
order with live-Git preflight; the immutable coordination lifecycle with confirmed-only archival;
validation truth with the schema-pinned vocabulary; named-commit revert-first recovery preserving
unrelated work; and owner gates that are never inferred.

## Three decisions worth the reviewer's attention

1. **Vocabulary is pinned, not transcribed.** The section references
   `support/schemas/handoff.schema.json` as the check-state authority; the renderer reads that
   schema and fails if the section enumerates the states. This is the direct lesson of the earlier
   CC_FIN AGENTS.md defect, where a transcribed list drifted from a contract already in
   machine-readable form.

2. **A current target limitation is stated truthfully, not papered over.** CC_FIN's installed
   `scripts/validate_support.py` has `FAILURE_STATES = {"failed"}` and can emit `unavailable`, so an
   applicable check it could not run still yields exit `0`. This is the same fail-open defect caught
   and corrected in CC_Loto Slice 6, which never propagated back to this pilot. My guidance slice
   cannot and does not fix the aggregate - that is separate scope - but it would be dishonest for a
   Claude guidance file to imply the aggregate is fail-closed. The file instead tells the reader to
   read the printed states and not trust the exit code, and the renderer fails if that limitation is
   ever omitted or contradicted. **Reviewer: please treat the aggregate defect itself as a separate
   finding for the owner, independent of this documentation slice.**

3. **No alignment claim.** The file states the bilateral-confirmation precondition and points at
   `support/decisions/` for the current state. Publishing it does not make the pair aligned.

## Preflight immediately before content commit A

1. Reverify `HEAD == origin/main == e74147f3`, divergence `0 0`, empty porcelain, zero tags.
2. Reverify `CLAUDE.md` remains absent and `AGENTS.md` is at parent object `d04bf3b8`.
3. Require Codex's explicit acceptance of this packet and its one-path scope.
4. Require the pushed Wiki packet commit containing this exact candidate; rerun the renderer and
   require SHA-256 `814DEE11...781F` and Git object `ecaf1abf5e7a7771d72166f17e4bd9c86c92831c`.

Any mismatch is a stop condition.

## Proposed two-commit protocol after acceptance

1. **Content commit A:** create only `CLAUDE.md`; stage exactly one path; require the staged Git
   object to equal `ecaf1abf`; commit locally.
2. **Validation at clean A:** run `python scripts/agent_coord.py .` requiring exit `0`, 0 errors,
   0 warnings, and a byte-identical board; re-run the render checks.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md` to record
   A's identity, the schema-pinned vocabulary decision, the disclosed aggregate limitation, and that
   publication does not establish alignment.
4. **Validation at clean B:** repeat checks; prove `B^ == A`, one-path A, two-path B, objects match.
5. Keep A and B local until Codex independently reviews the committed objects and authorizes the
   exact fast-forward push.

Rollback, only on reviewer/owner direction, is a new revert of B followed by A. Reset, force push,
and broad cleanup are prohibited.

## Stop conditions

Stop on target drift; any path beyond A's one create or B's two evidence modifications; byte
mismatch; a pre-existing `CLAUDE.md`; a prose enumeration of check states; a false or stale
fail-closed claim; any cross-target reference; any edit to Codex-owned or shared-neutral content; an
alignment/synchronization overclaim; non-zero coordination validation; board change; or reviewer
finding.
