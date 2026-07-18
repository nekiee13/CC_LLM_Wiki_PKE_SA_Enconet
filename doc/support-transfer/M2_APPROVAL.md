---
record_type: milestone_decision
gate: M2
decision: approved-with-amendments
decided_by: human project owner
recorded_at_utc: 2026-07-17T23:52:40Z
recorded_by: claude-code
packet: M2_DECISION_PACKET.md
packet_reviewed_at: 0d84e46 (Codex acceptance CX_2026-07-17T232749Z)
target_baseline: 238c207c73970f3d3c6dc00c2db5932ebeca7be4
---

# M2 approval — CC_FIN support publication authorized (immutable record)

The owner reviewed `M2_DECISION_PACKET.md` (independently accepted by Codex as fit for
submission at `0d84e46`) in the working session of 2026-07-18 and **approved the
recommended decision set with three amendments**, stated to the recording agent
(claude-code) in that session:

1. **Item 6 amended — baseline disposition deferred.** The non-green baseline
   (24 torch / 11 matplotlib / 19 assertion outcomes at `238c207`) is not resolved
   now. After the support system is implemented, and as its **final migration step**,
   the node-level failure fingerprint is recorded inside the FIN workspace's own
   support records: the transferred FIN support system must operate exclusively inside
   the FIN environment with no connection to this Wiki origin. Until that migration,
   the M2-RR1 tuple contract in `M2_BASELINE_FAILURE_SET.md` protects every slice.
2. **Item 7 restated — ownership is fixed, not a role.** Agent-owned guidance is
   authored only by its owning agent (`AGENTS.md` by Codex; `CLAUDE.md`/`.claude/` by
   Claude), independent of session roles.
3. **Item 9 amended — roles assigned per pre-job briefing.** Implementer and reviewer
   for each slice are assigned at that slice's pre-job briefing and may rotate between
   sessions; hard-coded actor assignments in the packet are removed. Independent
   review by the non-implementing agent remains mandatory for every slice.

## Authorized

- Slices 1, 2, 3 (shared-neutral support core), slice 5 (agent-owned/assigned edits
  per M1 item 7 under the fixed ownership rule), and slice 6 (isolated
  `followup-ml-gate.yml` one-line branch-filter correction per M1 item 8) — each under
  per-slice preflight, recorded per-slice parent HEAD, revert-only scoped rollback,
  and independent review.
- Recovery anchor `238c207` for slice 1; each later slice records its own clean
  pre-slice parent.

## Not authorized

- Slice 4 (T6.1 aggregate `validate_support.py` and the two focused support test
  modules) remains **deferred** — the artifacts are unrendered; it returns as a
  separate authorization with rendered content, disposable-copy and native-discovery
  evidence, and independent review.
- Any CC_Loto write (M3 unchanged), any product-code/data/chart/Cockpit change, any
  hosted mutation beyond slice 6, and any `.gitignore` edit (no need proven).

## Process note

No FIN write occurs before the first slice's pre-job briefing (scope, actor
assignment, preflight). The owner asked "is there anything else we need to discuss" and
closed the review with agreement to the clarifications; this record was written and
committed in the same session as the durable evidence of the decision.
