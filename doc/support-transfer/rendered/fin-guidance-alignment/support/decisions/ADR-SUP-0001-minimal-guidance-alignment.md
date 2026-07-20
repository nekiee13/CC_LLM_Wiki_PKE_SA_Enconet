---
record_type: support_decision
decision_id: ADR-SUP-0001
title: Minimal dual-agent guidance alignment
decision_state: accepted
implementation_state: pending
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

- Decision state is **Accepted**; implementation state is **Pending**.
- Codex owns any later `AGENTS.md` correction or completion. Claude Code reviews that slice.
- Claude Code owns any later creation or edit of `CLAUDE.md`. Codex reviews that slice.
- Each guidance slice requires its own exact render, preflight, review, validation, committed-object
  check, and scoped recovery evidence before publication.
- The pair is not called aligned until both agents independently confirm the live shared meanings.
- This decision does not itself authorize either guidance write and does not change `.agents/`,
  `.claude/`, product code, dependencies, tests, workflows, data/model/output, indexes, tags, or
  releases.

## Evidence

The read-only comparison is recorded in the support-transfer Wiki as
`doc/support-transfer/FIN_GUIDANCE_ALIGNMENT_ASSESSMENT.md`. At decision time CC_FIN was clean and
synchronized at the exact tip named in this record.
