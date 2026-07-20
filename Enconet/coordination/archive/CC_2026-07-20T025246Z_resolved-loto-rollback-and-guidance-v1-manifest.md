---
record_type: coordination_resolution_manifest
created_at_utc: 2026-07-20T02:52:46Z
resolved_by: claude-code
authority: ADR-0018 confirmed-resolution path
status: complete
resolved_messages:
  - message_id: CC_2026-07-20T023829Z_loto-rollback-rehearsal-accepted
    disposition: resolved
    resolution: Claude reproduced the rollback rehearsal bit-for-bit (deterministic commits d88f8588/f30373bc/9e46f95d, reverts 44123c04/b454e275, 165 baseline hashes, concurrent preservation, post-recovery aggregate/coordination/native) and accepted it, recording the non-blocking limitation that only disjoint concurrent work is proven.
    confirmation_evidence:
      - CX_2026-07-20T024013Z accepted after independent recheck, closed rollback evidence, and explicitly carried the limitation forward as an M4 requirement that the proof covers disjoint concurrent-work preservation and not owner-directed conflict resolution for later edits to the same append-only records.
  - message_id: CC_2026-07-20T024919Z_loto-guidance-packet-fit-for-owner-with-scope-finding
    disposition: resolved
    resolution: Claude confirmed the AGENTS.md line-86 vocabulary defect against handoff.schema.json and the installed aggregate, accepted the decision packet as fit for owner decision, recorded its own Slice 5 anchor-presence miss, and raised a scope finding that AGENTS.md contains two "blocked" occurrences of which only line 86 is a contract violation.
    confirmation_evidence:
      - CX_2026-07-20T025119Z acknowledged the finding, independently confirmed the schema/aggregate vocabulary and the distinct semantics of line 129, and delivered packet v2 at Wiki commit 55c6f2cb scoping the correction to line 86, preserving line 129, and requiring an exact-enumeration renderer guard.
---

# Resolved-message archive manifest — Claude rollback acceptance and guidance packet v1 review

Both Claude-owned records are resolved and confirmed by their Codex replies. CC_Loto remains
frozen and unmodified at `d5dc65e568ee73d82389e6e1d3fdf24122661adf`, with `AGENTS.md` at
`34b7eb93` and `CLAUDE.md` at `3edd8750`.

Two review lessons are recorded here because they are durable and belong in the M4 lessons
set rather than only in message bodies:

1. **Anchor presence is not anchor correctness.** The `AGENTS.md` line-86 defect survived
   Slice 5 review partly because the reviewer (Claude) treated the renderer's required
   semantic-anchor string as evidence of truthful-validation semantics. The anchor was
   present; its enumerated content was wrong. Semantic anchors must be validated against the
   authority they claim to encode.
2. **Cross-check prose against executable authority.** The defect was found by comparing
   guidance prose to `support/schemas/handoff.schema.json` and `tools/validate_support.py`,
   which encode the same check vocabulary. Where a contract exists in both prose and code, the
   code is the cheaper and stricter oracle.

Standing state: the CC_Loto guidance pair is **not** synchronized. The owner decision on
alignment is pending; approval would authorize only separately gated preparation, and each
agent may edit only its own guidance file. M4 remains closed and is not advanced by these
acceptances.
