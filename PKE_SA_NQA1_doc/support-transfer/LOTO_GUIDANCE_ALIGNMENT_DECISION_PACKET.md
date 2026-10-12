---
record_type: owner_decision_packet
decision_id: LOTO-GUIDANCE-ALIGNMENT
target: CC_Loto
target_tip: d5dc65e568ee73d82389e6e1d3fdf24122661adf
evidence_version: 2
prepared_by: codex
independent_reviewer: claude-code
state: independently_reviewed_fit_for_owner
independent_review: CC_2026-07-20T025401Z_loto-guidance-packet-v2-accepted
owner_decision: pending
target_write_authorized: false
---

# CC_Loto guidance-alignment decision packet

## Decision requested

Decide whether CC_Loto's Claude-owned `CLAUDE.md` should expose the same safety-critical support
workflow contract already exposed to Codex through `AGENTS.md`. This is a semantic-alignment choice,
not a request to make the files identical.

| Target | Exact baseline | What approval would authorize |
|---|---|---|
| CC_Loto | `d5dc65e568ee73d82389e6e1d3fdf24122661adf` | Preparation of two separately owned, exact-rendered, dry-run, independently reviewed guidance slices; no immediate target write |

This packet itself authorizes nothing. Even after an owner decision, Claude may edit `CLAUDE.md`
only through the established pre-write, committed-object, push, and live-closure gates. Codex must
not edit that file. M4 remains closed.

## Evidence bundle

- [`LOTO_GUIDANCE_ALIGNMENT_COMPARISON.md`](LOTO_GUIDANCE_ALIGNMENT_COMPARISON.md) — exact committed
  objects and the eight-anchor semantic matrix.
- [`LOTO_CC_GUIDANCE_PREJOB_BRIEFING.md`](LOTO_CC_GUIDANCE_PREJOB_BRIEFING.md) — prior correction's
  explicit boundary that the pair remained unsynchronized.
- [`LOTO_CC_GUIDANCE_IMPLEMENTATION_EVIDENCE.md`](LOTO_CC_GUIDANCE_IMPLEMENTATION_EVIDENCE.md) —
  committed evidence that the prior slice corrected one fact only.
- Target `support/current-status.md` — durable published non-synchronization disclosure.
- `M3_APPROVAL.md` item 7 — agent-owned files remain authored only by their owning agent.

## Recommended decision set

The recommendation is **approve minimal semantic alignment**:

1. Approve correcting only Codex-owned `AGENTS.md` line 86's check enumeration to use the canonical
   vocabulary. That sentence wrongly treats `blocked` as a check result and omits `not-configured`;
   the accepted contract reserves `blocked` for handoff/blocker state. Line 129's separate warning
   about a validation being blocked by a real blocker remains correct and outside the slice. The
   renderer must pin the exact corrected enumeration, not ban the word `blocked` file-wide.
2. After that correction is independently reviewed and published, approve adding one concise
   support-workflow section to Claude-owned `CLAUDE.md` covering the six
   groups defined in the comparison: ownership, read order, coordination lifecycle, validation
   truth, safe recovery, and explicit owner gates.
3. Keep existing product-development guidance intact; do not copy all of `AGENTS.md` or replace
   detailed shared-neutral authorities in `support/`.
4. Preserve ownership and independent review in both directions: Codex authors the `AGENTS.md`
   correction and Claude reviews it; Claude authors the `CLAUDE.md` alignment and Codex reviews it.
   Neither agent edits the other's file.
5. Keep `.agents/`, `.claude/`, product code, dependencies, tests, workflows, data, outputs,
   indexes, tags, and releases outside both slices unless a new owner decision names them.
6. Give each content change its own established two-commit protocol: one agent-owned content commit,
   then one shared-neutral evidence commit; require exact rendering, disposable dry run,
   committed-object review, normal fast-forward publication, and live-tip closure.
7. Do not mark the pair synchronized until both accepted corrections are published and both
   agents independently confirm the shared anchors at the live tip.
8. Keep M4 separate. Guidance alignment does not approve M4, and M4 does not retroactively approve
   a guidance edit.

## Risks and controls

| Risk | Control | Residual owner choice |
|---|---|---|
| Claude misses support messages or gates because its local guidance lacks the workflow | Add the minimum six-group section | Accept alignment or intentionally retain the risk |
| Duplicated guidance drifts | Keep the section concise and link detailed `support/` authorities | Choose minimal alignment or fuller duplication |
| Product instructions are obscured | Preserve all existing product guidance and add a clearly scoped support-only section | Decide whether `CLAUDE.md` should carry support workflow at all |
| Cross-agent ownership is violated | Each agent authors only its own guidance file; the other agent independently reviews | No residual delegation unless explicitly changed by owner |
| A known bad check vocabulary is copied during alignment | Correct `AGENTS.md` first and pin Claude's candidate to the installed schema/aggregate vocabulary | Approve the correction or intentionally retain the inconsistency |
| “Synchronized” is claimed prematurely | Require published live-tip confirmation by both agents | Owner may defer synchronization status until later |
| Guidance approval is confused with M4 acceptance | Separate claims, packets, records, and owner decisions | Decide guidance first or explicitly defer it past M4 preparation |

The first risk is already observable, not theoretical: Claude followed the complete support workflow
in this transfer because the session began in the Wiki workspace and inherited its guidance. A future
Claude session opened directly inside CC_Loto would receive no target-local instruction to read the
handoff, inspect messages and claims, require evidence before acceptance, use the fail-closed check
vocabulary, or keep M4 non-inferable. Minimal alignment closes that specific context-loss failure mode.

## Alternatives

- **Approve recommended minimal alignment:** Codex first prepares the narrow vocabulary correction;
  after its closure, Claude prepares the concise alignment candidate under a second gated slice. This
  best balances reliable support behavior with low duplication.
- **Partially approve — pointer only:** add only a short instruction to read `support/README.md`.
  This reduces duplication but leaves critical ownership, message, validation, recovery, and gate
  behavior implicit; the pair remains only partially aligned.
- **Defer:** make no target change and keep the published non-synchronization disclosure. M4 packet
  preparation must explicitly carry the unresolved guidance risk and cannot imply closure.
- **Reject and accept intentional asymmetry:** record that Claude remains product-guidance-only and
  support workflow is not guaranteed through `CLAUDE.md`. Future records must call this an accepted
  asymmetry, not synchronization.
- **Full duplication:** copy most Codex support guidance into `CLAUDE.md`. This maximizes local detail
  but creates the highest maintenance and drift burden; it is not recommended.

## Recovery impact in plain language

If an approved guidance slice later proves wrong, recovery is a new revert of that slice's named
evidence commit followed by its named agent-guidance commit, after owner/reviewer direction. The
prior guidance objects, all product files, and unrelated later work must be preserved. If later work
edits the same lines, conflict resolution is owner-directed; the completed rollback rehearsal proves
only the disjoint case.

## Owner decision record

Pending. Silence, elapsed time, independent review, or later M4 preparation is not approval.

The owner may record one of: approve recommended minimal alignment; partially approve with exact
items; defer; reject and accept intentional asymmetry; or request revision.
