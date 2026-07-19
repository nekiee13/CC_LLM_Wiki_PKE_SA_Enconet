---
record_type: slice_prejob_briefing
slice: 2
target: CC_Loto
version: 1
recorded_at_utc: 2026-07-19T21:12:37Z
authorized_by: M3_APPROVAL.md items 5-8
implementer: codex
reviewer: claude-code
roles_assigned_by: human owner, in-session, 2026-07-19
---

# CC_Loto Slice 2 pre-job briefing v1 — coordination core

This packet opens independent pre-write review only. It authorizes no CC_Loto write, commit, push,
dependency change, product change, or M4 transition. Codex is implementer; Claude Code is the
independent reviewer.

## Exact content scope — 14 creates, no modification

Content commit A would copy the byte authority in [`rendered/loto-slice2/`](rendered/loto-slice2/)
exactly:

1. `coordination/TEAM_PROTOCOL.md`
2. `coordination/BOARD.md`
3. `coordination/schemas/message.schema.json`
4. `coordination/schemas/claim.schema.json`
5. `coordination/schemas/resolution-manifest.schema.json`
6. `coordination/templates/message.template.md`
7. `coordination/templates/claim.template.yml`
8. `coordination/templates/resolution-manifest.template.md`
9. `coordination/templates/guidance-semantics.template.md`
10. `coordination/messages/README.md`
11. `coordination/archive/README.md`
12. `coordination/claims/README.md`
13. `tools/support/agent_coord.py`
14. `tools/support/_support_shared.py`

No `scripts/` path, agent-owned guidance, handoff file, support index, test, workflow, dependency
file, product source, model/data/output file, index configuration, tag, or release is in Slice 2.

Exact review inputs:

- [`LOTO_SLICE2_RENDER_EVIDENCE.md`](LOTO_SLICE2_RENDER_EVIDENCE.md)
- [`LOTO_SLICE2_DRY_RUN_EVIDENCE.md`](LOTO_SLICE2_DRY_RUN_EVIDENCE.md)
- [`rendered/render_loto_slice2.py`](rendered/render_loto_slice2.py)
- [`rendered/loto-slice2/`](rendered/loto-slice2/)

## Verified preflight state

- CC_Loto `main`, local HEAD, and `origin/main` equal published Slice 1 tip
  `496800dcf499f5bde21e52e1ea6abe917ca22e4f`.
- Divergence is `0 0`; porcelain is empty.
- All 14 creation paths are absent.
- Fixed-timestamp rerender reproduced 14/14 hashes with zero differences.
- Disposable overlay validation returned zero errors and warnings with zero byte mismatches.
- Native required short layers passed 70/70 outside the sandbox after sandbox-only filesystem
  permission failures.

## Reviewer decision required on support dependencies

The coordination implementation retains the accepted staged contract's `PyYAML` and `jsonschema`
imports. CC_Loto's product requirements environment does not include `PyYAML`; the support-capable
workspace interpreter does. This packet adds no dependency file and makes no claim that the product
environment can execute the tool. Claude must independently decide whether use of a separate
support-operator environment is consistent with the approved portable support contract. If not,
the finding blocks Slice 2 and requires an owner-reviewed scope/design disposition; Codex will not
silently add dependencies or replace the accepted validator design.

## Preflight immediately before any content commit A

1. Reverify `HEAD == origin/main == 496800dc...`, divergence `0 0`, and empty porcelain.
2. Reverify all 14 paths are absent.
3. Require Claude's explicit acceptance of this packet, including the dependency disposition.
4. Require the Wiki packet commit to be pushed and identify that accepted commit.
5. Rerun the fixed-timestamp renderer and confirm 14/14 reviewed hashes.

Any mismatch is a stop condition.

## Proposed two-commit evidence protocol after acceptance

1. **Content commit A:** copy only the 14 reviewed files; stage exact paths; compare every staged
   blob against the reviewed source; commit locally.
2. **Validation at clean A:** run `python tools/support/agent_coord.py .` using the reviewer-accepted
   support environment and require exit `0`, 0 errors, 0 warnings. Run the three native short
   layers with CC_Loto's native runner and require the accepted 70/70 baseline.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md` to record A's
   full SHA, exact commands, integer exits, native counts, and dependency/environment truth.
4. **Validation at clean B:** repeat coordination and native checks; verify A-byte identity,
   14-file inventory, exact `B^ == A`, and that `A..B` changes only the two evidence records.
5. Keep A and B local until Claude independently reviews committed objects and explicitly
   authorizes their exact push.

Rollback, only on reviewer/owner direction, is a new revert of B followed by A. Reset, force push,
broad cleanup, or restoration of unrelated paths is prohibited.

## Stop conditions

Stop on preflight drift; missing explicit dependency disposition; any path outside A's 14 creates
or B's two evidence modifications; byte mismatch; non-zero coordination validation; native
short-layer regression; sensitive/private/product data; unresolved non-template placeholder;
dangling/escaping link; runtime artifact; stale board; or reviewer finding. M4 remains closed.
