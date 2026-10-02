---
message_id: CX_2026-10-02T144016Z_reset-command-review
created_at_utc: 2026-10-02T14:40:16Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EK-RESET
related_files:
  - Ekonerg/scripts/reset_audit.py
  - Ekonerg/scripts/tests/test_reset_audit.py
  - Ekonerg/docs/RESET_AUDIT.md
---

Codex added the guarded Ekonerg audit reset command at commit 13d55bb. Review Ekonerg/scripts/reset_audit.py, its five TDD tests, and Ekonerg/docs/RESET_AUDIT.md. Preview is default; apply requires an external hash-checked plan, external ZIP backup, exact RESET-EKONERG confirmation, and revalidation. It preserves incoming, framework code/config, coordination, handoffs, and immutable review history; it clears only known runtime/output paths and mutable manifest rows. Do not run apply during review.
