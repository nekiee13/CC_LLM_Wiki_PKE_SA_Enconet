---
record_type: milestone_decision_packet
milestone: M4
target: CC_Loto
candidate_tip: bda0db3cf913207c254064b0681f7f309a536ec6
recorded_at_utc: 2026-07-20T07:10:00Z
prepared_by: codex
independent_reviewer: claude-code
owner_decision: pending
target_write: none
---

# M4 decision packet — accept CC_Loto support implementation

## Decision requested

Approve, approve with stated conditions, defer, or reject M4 for the CC_Loto support
implementation at exact published tip `bda0db3cf913207c254064b0681f7f309a536ec6`.

Approval accepts the support-transfer result and its bounded evidence. It does not declare the
default product suite green, approve product/data/model changes, authorize a tag or release, refresh
an index, enable hosted mutation, or waive the recorded rollback-conflict limitation.

## Evidence bundle

- Exact evidence map, final-tip checks, transfer chain, preservation proof, limitations, and lessons:
  [`LOTO_M4_EVIDENCE_INDEX.md`](LOTO_M4_EVIDENCE_INDEX.md)
- Aggregate evidence and independent acceptance:
  [`LOTO_AGGREGATE_VALIDATION_EVIDENCE.md`](LOTO_AGGREGATE_VALIDATION_EVIDENCE.md),
  [`CC_2026-07-20T022641Z_resolved-loto-aggregate-acceptance-manifest.md`](../../Enconet/coordination/archive/CC_2026-07-20T022641Z_resolved-loto-aggregate-acceptance-manifest.md)
- Real named-commit rollback rehearsal and independent acceptance:
  [`LOTO_ROLLBACK_REHEARSAL_EVIDENCE.md`](LOTO_ROLLBACK_REHEARSAL_EVIDENCE.md),
  [`CX_2026-07-20T024019Z_resolved-loto-rollback-rehearsal-manifest.md`](../../Enconet/coordination/archive/CX_2026-07-20T024019Z_resolved-loto-rollback-rehearsal-manifest.md)
- Bilateral semantic guidance synchronization:
  [`CC_2026-07-20T065813Z_resolved-loto-guidance-synchronization-manifest.md`](../../Enconet/coordination/archive/CC_2026-07-20T065813Z_resolved-loto-guidance-synchronization-manifest.md)
- Governing M3 authorization and owner decision:
  [`M3_FIN_ACCEPT_LOTO_AUTH_PACKET.md`](M3_FIN_ACCEPT_LOTO_AUTH_PACKET.md),
  [`M3_APPROVAL.md`](M3_APPROVAL.md)

## Recommended decision set

1. Accept the exact 18-commit support-transfer chain from baseline
   `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481` through candidate
   `bda0db3cf913207c254064b0681f7f309a536ec6`.
2. Accept the bounded validation statement: **support validated; product baseline unchanged;
   product layers not run**. Do not treat aggregate success as proof that the default product suite
   is green.
3. Accept product and data preservation: the protected product/science/configuration paths and
   named Git objects are unchanged from the authorized baseline.
4. Accept the real revert-only recovery proof for named support commits while retaining the explicit
   limitation that later edits to the same append-only records may require owner-directed conflict
   resolution.
5. Accept semantic synchronization of the eight approved support-workflow anchors in `AGENTS.md`
   and `CLAUDE.md`; do not require or claim byte identity between agent-native guidance files.
6. Accept the navigation and governance boundaries: the enhanced product plan remains proposed,
   product backlog and authority are unchanged, indexes remain deferred, CI remains integrate-only,
   release handling remains inventory-only, and no tag or release was created.
7. Close M4 only through an explicit owner decision recorded against this exact candidate tip. No
   further CC_Loto write follows from packet publication or reviewer acceptance.

## Decision consequences and residual risks

| Topic | What the evidence supports | Residual boundary |
|---|---|---|
| Support system | Aggregate, direct coordination, focused support contracts, and proportional native layers pass; unavailable operators fail closed | Product layers were not run |
| Product/data preservation | Protected paths and named Git objects match the authorized baseline | This is preservation evidence, not behavioral product validation |
| Recovery | Named support commits were really reverted; baseline bytes and disjoint concurrent work survived; validators passed afterward | Same-record later edits may conflict and require an owner-directed recovery plan |
| Guidance | Eight shared workflow semantics independently confirmed | Files are not byte-identical; synchronization is limited to the approved anchors |
| Governance | Navigation is connected without changing product authority; no index, tag, release, or hosted mutation | Any broader product/release/index action needs separate authorization |

## Alternatives

- **Approve the recommended set:** accept M4 at the exact candidate tip with all stated boundaries.
- **Approve with conditions:** accept only the named parts and record concrete follow-up conditions;
  conditions do not retroactively convert unrun product layers into passed evidence.
- **Defer:** keep M4 closed and state the additional evidence or owner choice required. Reverify the
  exact candidate tip before returning to the decision.
- **Reject:** keep M4 closed and identify the deficient evidence or implementation scope. Recovery,
  if requested, must use a separately reviewed named-commit plan; rejection alone authorizes no
  target mutation.

## Owner decision record

**Pending.** Reviewer acceptance is necessary evidence but is not the owner's decision. Silence is
not approval. The final record must name the exact candidate tip, the selected alternative, any
conditions or exceptions, and whether the M4 claim may be released.
