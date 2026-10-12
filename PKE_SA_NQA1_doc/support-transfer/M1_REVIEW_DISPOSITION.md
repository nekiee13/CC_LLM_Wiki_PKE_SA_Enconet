# M1 independent-review disposition

## Control

- Reviewed candidate commit: `9038cdd`
- Review message: `CC_2026-07-16T232129Z_m1-packet-review-findings`
- Reviewer verdict: revise (minor)
- Codex disposition state: completed
- Owner disposition state: accepted; M1 approved
- Target mutation: none

## Independent reproduction and disposition

| Finding | Reproduction | Codex disposition | Correction |
|---|---|---|---|
| M1-F1, medium/blocking | Confirmed: FIN has `.github/workflows/followup-ml-gate.yml`; the manifest named nonexistent `followup-gate.yml` | Accept | Corrected the normative path to `.github/workflows/followup-ml-gate.yml` |
| M1-F2, medium/blocking | Confirmed: activated plan defines M3 as FIN acceptance/Loto authorization and M4 as Loto acceptance; eight profile/packet references to FIN M4 created a deadlock | Accept | Replaced every FIN-M4 prerequisite with FIN acceptance at M3 |
| M1-O1, low/non-blocking | Confirmed: FIN already uses `scripts/`; Loto has `tools/` and no `scripts/` | Accept proactively | Loto utilities now use `tools/`; D-13 records the intentional difference |

The corrections do not change target baselines, enabled modules, authority, product scope, native
validation, or rollback semantics. They make the allowed-path and gate contracts executable as
originally intended.

## Remaining gate condition

Claude accepted the evidence base subject to these corrections. Codex accepted and implemented all
findings. The owner accepted M1-F1, M1-F2, and M1-O1 as resolved and approved M1 with both profile
versions and exact target SHAs. The durable decision is `M1_APPROVAL.md`; M2-M5 remain pending.
