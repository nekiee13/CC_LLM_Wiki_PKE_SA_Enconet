---
record_type: owner_gate_decision
gate: M1
plan_id: SUPPORT-SYSTEM-TRANSFER
plan_version: "1.0"
accepted_packet_commit: dd104a2
decided_at_utc: 2026-07-16T23:31:30Z
decision: approve
owner: human-project-owner
status: accepted
---

# M1 approval — corrected support-transfer profiles v1.0

## Owner decision

The owner accepted M1-F1, M1-F2, and M1-O1 as resolved and approved the corrected
`M1_DECISION_PACKET.md`, including recommended item 8.

Accepted profiles and exact target baselines:

- `CC_FIN_SUPPORT_PROFILE.md` v1.0 at
  `238c207c73970f3d3c6dc00c2db5932ebeca7be4`;
- `CC_LOTO_SUPPORT_PROFILE.md` v1.0 at
  `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`.

Both targets were independently verified clean and unmutated at those baselines when the decision
was recorded.

## Item 8 authorization

The isolated CC_FIN branch-filter correction from `master` to `main` in
`.github/workflows/followup-ml-gate.yml` is authorized, subject to exact diff review and native and
hosted validation. No other hosted-governance mutation is authorized by M1.

## Authorization boundary

- T1 and T2 are complete; T3 planning may begin.
- CC_FIN remains the sequential pilot.
- M2 remains a separate owner gate before FIN target publication.
- CC_Loto publication remains blocked until FIN acceptance at M3.
- M2-M5, tags, releases, product-plan edits, and other hosted changes are not implied.
- Claude-owned Loto guidance correction remains Claude work and cannot begin before Loto writes
  are authorized in sequence.

## Evidence

- Corrected packet and dispositions: commit `dd104a2`.
- Independent review: archived
  `CC_2026-07-16T232129Z_m1-packet-review-findings.md`.
- Durable owner terms and re-verification:
  `Enconet/coordination/archive/CC_2026-07-16T233130Z_resolved-m1-review-manifest.md`.
- Codex disposition: `M1_REVIEW_DISPOSITION.md`.

This gate record is immutable after publication. Corrections require a superseding gate record.
