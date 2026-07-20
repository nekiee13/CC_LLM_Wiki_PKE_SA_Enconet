---
record_type: support_decision
decision_id: ADR-SUP-0001
title: Minimal dual-agent guidance alignment
decision_state: accepted
implementation_state: complete
implementation_completed_at_utc: 2026-07-20T21:53:15Z
implementation_tip: 41e8dccf8262ca06da24eed66d3ec4ee03e94bd2
decided_by: human_project_owner
decided_at_utc: 2026-07-20T08:13:48Z
recorded_by: codex
target_tip_at_decision: 88f2c51cf54599a1f58cdadb5a6dfd31dd4f59ac
---

# ADR-SUP-0001 — Minimal dual-agent guidance alignment

## Context

At the decision tip, `AGENTS.md` contains the support read order, ownership split, coordination
command, immutable message lifecycle, generated-BOARD boundary, and literal non-pass guidance.
However, it omits target-native `not-configured` from its validation summary and does not expose the
shared safe-recovery or owner-gate anchors. `CLAUDE.md` is absent from the committed tree.

The repository's target-native alignment authority is
`coordination/templates/guidance-semantics.template.md`. It requires shared meaning for read order,
ownership, truthful validation, safe recovery, and target gates while allowing agent-specific
wording and product guidance.

The human project owner directed: **“Check if agents.md and claude.md at CC_FIN comply to minimal
alignment. Add minimal alignment to decision log.”** The five required meanings below are derived
from the installed target-native template; they are not represented as verbatim owner wording.

## Decision

CC_FIN will use minimal semantic alignment for its two agent guidance files. Both files must expose
the five target-native shared meanings:

1. support read order, live Git state, and unfinished-work inspection;
2. agent-owned versus shared-neutral ownership boundaries;
3. literal validation truth, including that non-pass states are never represented as passed;
4. evidence-first, scoped, approval-gated recovery that preserves unrelated work;
5. explicit owner gates that cannot be inferred from completed implementation or validation.

The files need not be byte-identical and should not duplicate detailed support authorities or form a
second product backlog.

## Implementation boundary

- Decision state is **Accepted**; implementation state is **Complete**.
- Codex owns any later `AGENTS.md` correction or completion. Claude Code reviews that slice.
- The existing `AGENTS.md` warning that checks prevented by a real blocker must never imply pass is
  retained; the later Codex slice adds missing `not-configured`, safe-recovery, and owner-gate
  semantics without recasting `blocked` as a successful result.
- Claude Code owns any later creation or edit of `CLAUDE.md`. Codex reviews that slice.
- Each guidance slice requires its own exact render, preflight, review, validation, committed-object
  check, and scoped recovery evidence before publication.
- The pair is not called aligned until both agents independently confirm the live shared meanings.
- This decision does not itself authorize either guidance write and does not change `.agents/`,
  `.claude/`, product code, dependencies, tests, workflows, data/model/output, indexes, tags, or
  releases.

## Implementation completion

At live tip `41e8dccf8262ca06da24eed66d3ec4ee03e94bd2`, both agent-owned guidance files are published and each owner independently
confirmed its own file against the live Git object:

- Codex confirmed `AGENTS.md` object `4cca3734d8c789038b1142a64be2eec2c5edbccc` and all five target-native meanings in
  `CX_2026-07-20T214930Z_fin-claude-guidance-live-closure-and-codex-anchor-confirmation`.
- Claude Code confirmed `CLAUDE.md` object `ecaf1abf5e7a7771d72166f17e4bd9c86c92831c` and all five target-native meanings in
  `CC_2026-07-20T215315Z_fin-claude-guidance-closed-and-claude-anchor-confirmation`.

Those two confirmations satisfy the decision's bilateral precondition. The guidance pair is
minimally aligned in shared meaning at the implementation tip; agent-specific wording and product
guidance remain intentionally distinct. This completion establishes guidance semantics only. It is
not evidence that the product test suite is green, and it does not fix or close the separate
`scripts/validate_support.py` fail-open defect for applicable `unknown` or `unavailable` results.

## Evidence

The read-only comparison is recorded in the support-transfer Wiki as
`doc/support-transfer/FIN_GUIDANCE_ALIGNMENT_ASSESSMENT.md`. At decision time CC_FIN was clean and
synchronized at the exact tip named in this record.
