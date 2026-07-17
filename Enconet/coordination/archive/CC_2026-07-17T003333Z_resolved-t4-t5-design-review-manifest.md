---
record_type: coordination_resolution_manifest
created_at_utc: 2026-07-17T00:33:33Z
resolved_by: claude-code
authority: ADR-0018
status: complete
---

# Resolved-message archive manifest (T4/T5 design review findings)

| Archived message | Resolution | Confirmation evidence |
|---|---|---|
| `CC_2026-07-17T002449Z_t4-t5-design-review-findings.md` | Independent Claude review of the T4/T5 coordination and handoff design at planning-only candidate `a29f3c4`: verdict REVISE (minor) with T45-F1 (`handoff.schema.json` accepted a fabricated HEAD under `git_state: absent`/`unknown`, contradicting the T5 contract's "cannot fabricate a SHA") and T45-F2 (`resolution-manifest.schema.json` accepted `deferred-until` with no objective condition/date or owner, contradicting the T4 contract), plus the requested planning-versus-publication boundary assessment. Codex accepted both findings and the boundary, correcting them at `1e4b6bb`; claude-code independently re-verified at HEAD `09fcf2b` with 22/22 schema cases. The **owner explicitly accepted T45-F1, T45-F2, and the completion boundary on 2026-07-17** | `CX_2026-07-17T002827Z_ack-t4-t5-design-review-findings.md` and `CX_2026-07-17T002835Z_resolved-t4-t5-design-review-manifest.md` (both archived) — explicit Codex confirmation, not silence; `T4_T5_REVIEW_DISPOSITION.md` records the Codex disposition; owner disposition given directly to claude-code on 2026-07-17 |

## Owner disposition (durable record of the decision as given)

- **T45-F1: accepted** as resolved. Both original probes are now rejected; `absent` requires null
  branch and HEAD, `unknown` requires null HEAD, and `current`/`stale` require non-empty root/branch
  and a full 40-hex HEAD. Legitimate all-null no-Git records still validate.
- **T45-F2: accepted** as resolved. `deferred-until` now requires both `deferred_until` and
  `deferral_owner` (condition-only, owner-only, and empty-condition all rejected), and the `else`
  branch forbids stray deferral fields on other dispositions. The T4 validator contract was updated
  to match.
- **Completion boundary: accepted** as recorded in `T4_T5_REVIEW_DISPOSITION.md` — T5.1's four
  definitional criteria may close; T4.1-artifact/validator, T4.3, and T5.2 remain pending executable
  staged artifacts with positive and fault-injection tests in disposable roots; T4.2 and
  target-installed T4.1/T5.3 remain pending target implementation at T7/T8; no wholesale T4/T5
  completion record is permitted on design evidence. Claude alone authors CC_FIN's Claude-owned
  payload; Codex alone authors CC_Loto's Codex-owned payload.

## Independent re-verification at HEAD `09fcf2b`

- All four schemas remain valid Draft 2020-12; 22/22 re-check cases behaved as specified, including
  both original probes now rejected and regression cases (`resolved`/`owner-accepted` clean,
  `acknowledged` still rejected, `passed`+exit_code 1 still rejected, `skipped`+exit_code still
  rejected).
- EPIC T4/T5 remain 0 complete / 23 pending, and no criterion anywhere beyond EPIC T3 is marked —
  consistent with the accepted boundary.
- Both targets unmutated at their M1-accepted baselines: CC_FIN `238c207` clean, CC_Loto `b469afc`
  clean (both 40-hex SHA-1 heads, consistent with the new HEAD pattern).
- Non-blocking observation recorded for the future, requiring no action: the `^[a-f0-9]{40}$` HEAD
  pattern hard-codes SHA-1; a SHA-256 (64-hex) HEAD would be rejected. No live impact — both targets
  are SHA-1 today.

Marking T5.1 complete and publishing any T4/T5 partial-completion record belong to Codex, which
implements the transfer. M2 continues to block every CC_FIN write and M3 blocks CC_Loto publication;
this disposition implies neither. Moved intact with its original filename by its author, claude-code.
