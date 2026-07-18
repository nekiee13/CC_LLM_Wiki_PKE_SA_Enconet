# Support-system transfer evidence index

This directory contains controlled planning and gate evidence for
`SUPPORT_SYSTEM_TRANSFER_MASTER_PLAN.md`. Target repositories remain unchanged until the
applicable owner gate authorizes publication.

| Record | Purpose | Status |
|---|---|---|
| `M0_ACTIVATION.md` | Immutable activation of plan v1.0 | Accepted |
| `M1_APPROVAL.md` | Immutable approval of corrected profiles v1.0 and exact baselines | Accepted |
| `CC_FIN_EVIDENCE_INVENTORY.md` | T1.1 read-only inventory and drift dispositions | Complete candidate |
| `CC_LOTO_EVIDENCE_INVENTORY.md` | T1.2 read-only inventory and drift dispositions | Complete candidate |
| `GAP_COLLISION_SENSITIVITY_MATRIX.md` | T1.3 cross-target gaps, collisions, sensitivity, and scale | Complete candidate |
| `CC_FIN_SUPPORT_PROFILE.md` | T2.1 target support profile | M1 candidate v1.0 |
| `CC_LOTO_SUPPORT_PROFILE.md` | T2.2 target support profile | M1 candidate v1.0 |
| `DIFFERENCE_REGISTER.md` | T2.3 intentional semantic differences | M1 candidate v1.0 |
| `PUBLICATION_ROLLBACK_MANIFESTS.md` | T2.4 allowed paths, ownership, preflight, abort, rollback | M1 candidate v1.0 |
| `M1_DECISION_PACKET.md` | T2.5 consolidated owner decision packet | Approved at M1 |
| `M1_REVIEW_DISPOSITION.md` | Independent review findings and explicit dispositions | Complete |
| `T3_GOVERNANCE_RECORD_CONTRACT.md` | Authority, record taxonomy, ADR, AFI, lesson, and good-practice semantics | Accepted T3 v1.0 |
| `T3_TARGET_TEMPLATE_CONTRACT.md` | Explicit rendering/configuration and target-local asset contract | Accepted T3 v1.0 |
| `templates/` | Neutral governance and record templates for later gated publication | Accepted T3 |
| `T3_REVIEW_DISPOSITION.md` | Independent T3 findings and explicit dispositions | Complete |
| `T3_COMPLETION.md` | Immutable T3 closure evidence and authorization boundary | Complete |
| `T4_COORDINATION_BOOTSTRAP_CONTRACT.md` | Neutral protocol, lifecycle, ownership, claims, board, guidance, and validator design | T4 design candidate v1.0 |
| `T5_HANDOFF_CONTINUITY_CONTRACT.md` | Clone-complete handoff, atomic publication, staleness, and continuity design | T5 design candidate v1.0 |
| `templates/coordination/` | Neutral coordination schemas and templates | T4 design candidate |
| `templates/handoff/` | Neutral handoff schema and templates | T5 design candidate |
| `T4_T5_REVIEW_DISPOSITION.md` | T4/T5 findings and design-versus-publication boundary | Complete |
| `T4_T5_DESIGN_CHECKPOINT.md` | Partial checkpoint closing T5.1 only and preserving pending boundaries | Accepted |
| `T6_VALIDATION_RECOVERY_GATE_CONTRACT.md` | T6.1-T6.4 target-native aggregates, guardrails, milestone-packet, and recovery-rehearsal design | T6 design candidate v1.0 |
| `templates/milestone-packet.template.md` | T6.3 neutral M2-M5 decision-packet template | T6 design candidate |
| `staged/` | Staged coordination-validator and handoff-publisher prototypes plus disposable-root positive/fault-injection tests (T4.1-artifact, T4.3, T5.2, T6.4 evidence) | Accepted (`CX_2026-07-17T222326Z`, staged-level only) |
| `T6_STAGED_EXECUTABLE_CHECKPOINT.md` | Staged-executable evidence, 67/67 passing tests, all review-round corrections, and explicit pending boundary | Accepted (staged-level only) |
| `M2_PREFLIGHT_EVIDENCE.md` | Read-only CC_FIN baseline reverification, native-check results, dry-run collision check, recovery anchor | Corrected per M2-F1/F4/F5 |
| `M2_BASELINE_FAILURE_SET.md` | Tuple-based baseline failure fingerprint with deterministic normalization rule (normative T7.3 comparison contract) | Corrected per M2-RR1/RR3 |
| `M2_DRY_RUN_MANIFEST.md` | Exact per-slice file inventory (slice 4 deferred), existing-file dispositions, disposable-copy validation | Corrected per M2-RR2 |
| `M2_DECISION_PACKET.md` | T6.3 consolidated owner decision packet for FIN publication | Accepted by Codex (`CX_2026-07-17T232749Z`); owner-approved with amendments |
| `M2_APPROVAL.md` | Immutable owner M2 decision: slices 1-3/5/6 authorized, slice 4 deferred, baseline deferred to FIN-side final migration, roles per pre-job briefing | Accepted |
| `M2_AMENDMENT_1.md` | Immutable owner-approved M2 amendment: T3-rule-5 resequencing, slice 3c index closure, support/PROFILE.md, target-local evidence rules | Current M2 authority; direction accepted by Codex, implementation-readiness corrections applied |
| `SLICE1_PREJOB_BRIEFING.md` | Slice-1 v6 protocol (roles owner-reassigned) | Executed; slice 1 published at CC_FIN `879bcb5` |
| `SLICE1_RENDER_EVIDENCE.md` | Rendered slice-1 tree evidence: fail-closed render, disposable-root read-back, content decisions | Complete candidate |
| `rendered/slice1/` | Byte authority for slice-1 content commit A `339026c` | Published; byte-verified by both agents |

Records marked candidate become accepted only through the gate named in the Master Plan.
