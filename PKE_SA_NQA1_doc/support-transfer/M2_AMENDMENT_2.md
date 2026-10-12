---
record_type: milestone_decision_amendment
gate: M2
amendment: 2
decision: approved
decided_by: human project owner
recorded_at_utc: 2026-07-18T13:12:34Z
recorded_by: claude-code
trigger: slice-2 boundary rule (SLICE2_PREJOB_BRIEFING.md v2) and reviewer scope flag
  CC_2026-07-18T131112Z_ack-slice3-roles-board-scope-flag
---

# M2 amendment 2 — slice-3 generated BOARD modification (immutable record)

Amendment 1 defines slice 3 (handoff core) as create-only. Creating `HANDOFF.md`
necessarily makes the generated `coordination/BOARD.md` stale, and the installed
validator correctly fails until regeneration — a modification outside the authorized
create-only inventory. Per the accepted slice-2 boundary rule, the briefing may not
expand its own scope; the owner decided the amendment in-session on 2026-07-18.

## Decision

Slice 3's authorized inventory becomes **7 creates + 1 generated modification**: the
seven handoff-core creates from the amended manifest, plus regeneration of
`coordination/BOARD.md` by the installed `scripts/agent_coord.py`
(`--write-board --timestamp <reviewed UTC>`) so the board truthfully names the new
pointer. The regenerated board must appear in the slice's exact evidence diff and in
its byte-authority tree.

## Boundary

Nothing else changes: no other existing-file modification enters slice 3; slices 3c,
5, 6 keep their inventories; slice 4 stays deferred; M3 stays closed; per-slice
preflight, two-commit evidence protocol, independent review, and revert-only recovery
apply unchanged. This amendment is available to Codex's slice-3 pre-job briefing,
which remains subject to Claude Code's independent review before any target write.
