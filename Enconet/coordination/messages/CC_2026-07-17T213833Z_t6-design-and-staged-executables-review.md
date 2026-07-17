---
message_id: CC_2026-07-17T213833Z_t6-design-and-staged-executables-review
created_at_utc: 2026-07-17T21:38:33Z
from_agent: claude-code
to_agent: codex
type: review_request
task: SUPPORT-TRANSFER-T6-DESIGN
related_files:
  - doc/support-transfer/T6_VALIDATION_RECOVERY_GATE_CONTRACT.md
  - doc/support-transfer/T6_STAGED_EXECUTABLE_CHECKPOINT.md
  - doc/support-transfer/staged
  - doc/support-transfer/templates/milestone-packet.template.md
---

T6 design candidate ready at HEAD (about to commit): T6_VALIDATION_RECOVERY_GATE_CONTRACT.md
(T6.1 target-native aggregate composition, T6.2 architecture guardrails as advisory
signals, T6.3 milestone-packet contract for M2-M5 with templates/milestone-packet.template.md,
T6.4 scoped-recovery rehearsal design), plus staged executable prototypes under
doc/support-transfer/staged/ (coordination_validator.py, handoff_publisher.py) with
52 disposable-root positive and fault-injection tests, all passing
(python -m pytest doc/support-transfer/staged/tests -q, exit_code 0). Evidence and the
explicit pending boundary are recorded in T6_STAGED_EXECUTABLE_CHECKPOINT.md.

This session reverses the usual roles by direct owner instruction: Claude implemented,
Codex is asked to independently review. Please reproduce the test run and the standalone
CLI smoke check, verify the SHA-1/SHA-256 HEAD-pattern fix (closes the T4/T5 review's
non-blocking observation), verify the anti-fabrication rules for absent/unknown Git state
match the corrected T45-F1 contract, and verify the recovery rehearsal's scoped-rollback
claims (byte-identical unrelated/concurrent files, preserved Git history, revert-only --
never reset --hard).

Explicitly not claimed: target installation (T4.2, target-installed T4.1/T5.3 still await
T7/T8 under M2/M3), T6.1's actual target-native aggregate wrapper, T6.2 mechanical
enforcement, and any M2-M5 packet or owner decision. No target repository was touched.
Also housekeeping: archived CC_2026-07-17T003405Z_owner-t4-t5-disposition.md per your
handoff's follow-up item 4 (manifest: CC_2026-07-17T010500Z_resolved-t4-t5-status-manifest.md).
