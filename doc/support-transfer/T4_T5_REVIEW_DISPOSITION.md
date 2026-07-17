# T4/T5 independent-review disposition

## Control

- Reviewed candidate: `a29f3c4`
- Review message: `CC_2026-07-17T002449Z_t4-t5-design-review-findings`
- Reviewer verdict: revise (minor)
- Codex disposition: complete
- Owner disposition: pending explicit decision
- Target mutation: none

## Findings

| Finding | Independent reproduction | Codex disposition | Correction |
|---|---|---|---|
| T45-F1, medium | Confirmed: `git_state: absent` accepted a fabricated non-null HEAD, contradicting the handoff contract | Accept | `absent` now requires null branch/HEAD; `unknown` requires null HEAD; `current`/`stale` require non-empty root/branch and a full 40-hex HEAD |
| T45-F2, medium | Confirmed: `deferred-until` accepted `resolution: later` without an objective condition/date or owner | Accept | Manifest entries now require `deferred_until` and `deferral_owner` only for `deferred-until`; validator contract matches |

## Planning-versus-publication boundary

Codex accepts the reviewer's evidence-based boundary:

- T5.1's four definitional criteria may close after owner acceptance of these findings.
- T4.1 artifact/validator, T4.3, and T5.2 remain pending until executable staged artifacts and
  positive/fault-injection tests exist in disposable roots.
- T4.2 and target-installed T4.1/T5.3 remain pending target implementation at T7/T8. Claude alone
  authors CC_FIN's Claude-owned payload; Codex alone authors CC_Loto's Codex-owned payload.
- No T4/T5 wholesale completion record is permitted on design evidence.

M2 continues to block all FIN target writes, and M3 blocks Loto publication.
