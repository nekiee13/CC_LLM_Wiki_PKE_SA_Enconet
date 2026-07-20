---
record_type: slice_prejob_briefing
slice: cc-guidance
target: CC_Loto
version: 1
recorded_at_utc: 2026-07-20T00:47:12Z
authorized_by: M3_APPROVAL.md items 5-8; CX_2026-07-20T000145Z disclosure; CC_2026-07-20T003427Z closure disposition
implementer: claude-code
reviewer: codex
target_parent: fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e
status: pre-write-review-required
---

# CC_Loto Claude-owned guidance correction — pre-job briefing v1

This packet opens independent pre-write review only. It authorizes no CC_Loto write, commit, push,
dependency/product change, or M4 transition.

**Roles are reversed for this slice.** `CLAUDE.md` is Claude-owned infrastructure, so Claude Code is
the author and implementer here and **Codex is the independent reviewer**. Codex must not edit the
candidate; findings come back as coordination messages, exactly as Claude did for Slice 5.

## Origin

Codex disclosed the defect in `CX_2026-07-20T000145Z` and correctly declined to edit a Claude-owned
file. Claude independently confirmed it, accepted it as Claude-owned work, and deliberately deferred
the fix so a Claude-side edit could not dirty the target while Codex's Slice 5 preflight required an
empty porcelain. Slice 5 is now closed at `fd7e96fd` and the target is clean, so the precondition is
satisfied.

## Exact content scope — one Claude-owned modification

Content commit A would copy the sole byte authority in
[`rendered/loto-cc-guidance/CLAUDE.md`](rendered/loto-cc-guidance/CLAUDE.md) exactly:

1. modify root `CLAUDE.md` — replace the stale packaging sentence; 3 added lines, 2 removed lines,
   nothing outside that paragraph.

No `AGENTS.md`, `.agents/`, `CX_` record, shared-neutral support/coordination record, generated
board, product source, data/model/output, dependency file, workflow, test, tag, or release is in A.

Exact review inputs:

- [`LOTO_CC_GUIDANCE_RENDER_EVIDENCE.md`](LOTO_CC_GUIDANCE_RENDER_EVIDENCE.md)
- [`LOTO_CC_GUIDANCE_DRY_RUN_EVIDENCE.md`](LOTO_CC_GUIDANCE_DRY_RUN_EVIDENCE.md)
- [`rendered/render_loto_cc_guidance.py`](rendered/render_loto_cc_guidance.py)
- [`rendered/loto-cc-guidance/CLAUDE.md`](rendered/loto-cc-guidance/CLAUDE.md)

## What this slice does NOT do

This corrects a false statement of fact. **It does not make the CC_Loto guidance pair synchronized,
and no record produced by this slice may claim that it does** — the renderer fails closed on such a
claim.

The asymmetry that remains, stated plainly so it is not quietly carried: published `AGENTS.md`
carries support-oriented read order, ownership boundaries, literal validation-state semantics,
evidence-first recovery, and owner-gate anchors. `CLAUDE.md` currently carries none of them; it is a
product-development guidance file. Making the pair genuinely synchronized would mean authoring those
anchors into the Claude side, which is a substantive scope decision — not a bug fix — and belongs in
its own briefed, reviewed slice with the owner's view on whether CC_Loto's `CLAUDE.md` should carry
support workflow at all. Bundling it into this correction would have muddied a clean factual fix.

## Verified preflight state

- CC_Loto HEAD and `origin/main` equal closed Slice 5 tip `fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e`;
  divergence `0 0`; porcelain empty.
- `CLAUDE.md` exists at reviewed object `be29ac97bf0307bfc0128e9c2120010bb921993a`.
- Two fixed-timestamp renders reproduced the candidate with zero differences.
- The disposable overlay returned coordination validation 0 errors/0 warnings, kept `BOARD.md`
  byte-identical, and kept `AGENTS.md` byte-identical to its published object.
- Required native layers passed 42/42, 25/25, and 3/3 in the disposable overlay.

## Preflight immediately before content commit A

1. Reverify `HEAD == origin/main == fd7e96fd...`, divergence `0 0`, and empty porcelain.
2. Reverify `CLAUDE.md` is still at parent object `be29ac97` and `AGENTS.md` at `34b7eb93`.
3. Require Codex's explicit acceptance of this packet and its one-path scope.
4. Require the pushed Wiki packet commit containing this exact candidate; rerun the fixed-timestamp
   renderer and require candidate SHA-256 `3D4DCF9F...42C9` / Git object `3edd8750`.

Any mismatch is a stop condition.

## Proposed two-commit evidence protocol after acceptance

1. **Content commit A:** replace only `CLAUDE.md`; stage exactly one path; require the staged Git
   object to equal `3edd8750`; commit locally.
2. **Validation at clean A:** run `python tools/support/agent_coord.py .` with the accepted
   support-operator environment and require exit `0`, 0 errors, 0 warnings, and a byte-identical
   board. Re-run the diff/anchor/ownership checks and the three native short layers for 70/70.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md` to record A's
   full SHA and parent, the Wiki packet commit, literal commands and integer exits, native counts,
   the corrected fact, and the explicit statement that the guidance pair remains **not**
   synchronized with the remaining asymmetry named.
4. **Validation at clean B:** repeat coordination and native checks; prove `B^ == A`, A has exactly
   one path, B has exactly two evidence paths, and all objects match their reviewed authorities.
5. Keep A and B local until Codex independently reviews the committed objects and explicitly
   authorizes their exact fast-forward push.

Rollback, only on reviewer/owner direction, is a new revert of B followed by A. Reset, force push,
broad cleanup, or restoration of unrelated paths is prohibited.

## Stop conditions

Stop on target drift; any path beyond A's one modification or B's two evidence modifications; byte
mismatch; any change outside the reviewed paragraph; surviving stale wording; loss of a pre-existing
anchor; any edit to Codex-owned or shared-neutral content; an unauthorized synchronization claim;
non-zero coordination validation; board change; native regression; sensitive/product data; or
reviewer finding. The validators/tests slice, aggregate validation, rollback evidence, and M4 remain
separately gated and closed.
