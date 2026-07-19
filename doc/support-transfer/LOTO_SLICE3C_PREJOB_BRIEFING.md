---
record_type: slice_prejob_briefing
slice: 3c
target: CC_Loto
version: 1
recorded_at_utc: 2026-07-19T23:13:35Z
authorized_by: M3_APPROVAL.md items 5-8 and CC_2026-07-19T230622Z scope acceptance
implementer: codex
reviewer: claude-code
target_parent: 7100469757128defd3c437d6f9554744e57a6fa1
status: pre-write-review-required
---

# CC_Loto Slice 3c pre-job briefing v1 — index/navigation closure

This packet opens independent pre-write review only. It authorizes no CC_Loto write, commit, push,
external index action, dependency/product change, or M4 transition. Codex is implementer; Claude
Code is independent reviewer.

## Exact content scope — one create plus one one-line modification

Content commit A would copy the byte authority in
[`rendered/loto-slice3c/`](rendered/loto-slice3c/) exactly:

1. create `support/README.md`;
2. modify root `README.md` by adding exactly this one line after its existing architecture link:
   `Support and coordination: [support system](support/README.md).`

The target has no `docs/README.md`; this packet does not fabricate one to copy the FIN layout.
`support/README.md` links the installed shared-neutral support core and existing Loto authorities.
It keeps documentation/code indexes deferred, hosted governance integrate-existing-CI-only, and
the release adapter inventory-only. This is clone-local navigation/discoverability closure, not an
external index or corpus creation/refresh.

No guidance, validator, test, workflow, dependency, product source, data/model/output, handoff,
coordination state, tag, or release is in content A. Exact review inputs:

- [`LOTO_SLICE3C_RENDER_EVIDENCE.md`](LOTO_SLICE3C_RENDER_EVIDENCE.md)
- [`LOTO_SLICE3C_DRY_RUN_EVIDENCE.md`](LOTO_SLICE3C_DRY_RUN_EVIDENCE.md)
- [`rendered/render_loto_slice3c.py`](rendered/render_loto_slice3c.py)
- [`rendered/loto-slice3c/`](rendered/loto-slice3c/)

## Verified preflight state

- CC_Loto local HEAD and `origin/main` equal closed Slice 3 tip
  `7100469757128defd3c437d6f9554744e57a6fa1`; divergence `0 0`; porcelain empty.
- `support/README.md` and `docs/README.md` are absent; root `README.md` exists at Git blob
  `a79799c3ca4893ff269762089243afa13043fd21`.
- The root README candidate has exactly one added line and zero deleted lines.
- A fixed-timestamp rerender reproduced both candidate hashes with zero differences.
- The short-root disposable overlay returned coordination validation 0 errors/0 warnings, kept the
  board byte-identical, and resolved every target-local link.
- Required native layers passed 42/42, 25/25, and 3/3 in the disposable overlay.
- `git ls-remote --tags origin` exited `0` with no tag refs. GitHub release inventory is not
  claimed: `gh` is unavailable in this environment.

## Preflight immediately before any content commit A

1. Reverify `HEAD == origin/main == 710046975...`, divergence `0 0`, and empty porcelain.
2. Reverify `support/README.md` remains absent and root `README.md` still has reviewed blob
   `a79799c...`; require exactly one addition and zero deletions.
3. Rerun the tag inventory command and report its integer exit; do not infer GitHub release state
   while `gh` remains unavailable.
4. Require Claude's explicit acceptance of this complete packet and exact two-path scope.
5. Require the pushed Wiki packet commit containing this exact byte authority, then rerun the
   fixed-timestamp renderer and confirm 2/2 hashes and all disposable checks.

Any mismatch is a stop condition.

## Proposed two-commit evidence protocol after acceptance

1. **Content commit A:** create `support/README.md` and replace only root `README.md` with the
   one-line-addition candidate; stage exactly two paths; compare both staged blobs with the reviewed
   sources; commit locally.
2. **Validation at clean A:** run installed coordination validation and require exit `0`, 0 errors,
   0 warnings, and byte-identical board. Resolve all index links and run the three native short
   layers for 70/70.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md` to record A's
   full SHA/parent, exact scope and bytes, commands and integer exits, tag/release inventory truth,
   installed/native validation, later gated slices, and M4 closure.
4. **Validation at clean B:** repeat coordination/link/native checks; prove `B^ == A`, A has the
   exact two-path scope, B has the exact two evidence paths, and all committed objects match their
   reviewed authorities.
5. Keep A and B local until Claude independently reviews the committed objects and explicitly
   authorizes their exact fast-forward push.

Rollback, only on reviewer/owner direction, is a new revert of B followed by A. Reset, force push,
broad cleanup, or restoration of unrelated paths is prohibited.

## Stop conditions

Stop on target drift; collision at `support/README.md`; root README change beyond the one approved
line; byte mismatch; unresolved/dangling/escaping link; false plan/progress/index/hosted/release
state; non-zero coordination validation; board change; native regression; sensitive/private/product
data; target artifact; or reviewer finding. M4 remains closed.
