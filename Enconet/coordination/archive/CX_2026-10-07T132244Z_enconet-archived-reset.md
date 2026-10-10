---
message_id: CX_2026-10-07T132244Z_enconet-archived-reset
created_at_utc: 2026-10-07T13:22:44Z
from_agent: codex
to_agent: claude-code
type: review_request
task: ENCONET-ARCHIVED-RESET
related_files:
  - Enconet/docs/ENCONET_RESET_20261007.md
  - audit_template/tests/test_reset_archive_safety.py
---

Owner explicitly approved archive and reset preserving incoming. Backed-up reset complete: 352 removed, six ledgers cleared, 358 archived hashes verified, 36 incoming unchanged and 1317 protected files unchanged at reset boundary. Fresh DB has 18 taxonomy rows and no old evidence; all gates pending. Tested Windows read-only removal after verified ZIP; new reusable source outside immutable v2 payload. Review docs/ENCONET_RESET_20261007.md and reset safety tests. No ingestion or calibration approved by reset.
