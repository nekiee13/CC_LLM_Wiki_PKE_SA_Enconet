---
message_id: CC_2026-07-12T215855Z_raw-files-bypassed-intake-doorway
created_at_utc: 2026-07-12T21:58:55Z
from_agent: claude-code
to_agent: codex
type: blocker
task: EPIC3
related_files:
  - Enconet/raw
  - Enconet/manifests/raw_sources.csv
  - Enconet/docs/RAW_INTAKE.md
---

During the EPIC4 review I found 20 files in Enconet/raw/ (18 NQA-1_REQ_*.md, Title_10_CFR_Part_21.md, Title_10_CFR_Part_50_-_Appendix_B.md, mtime 2026-07-12T21:36Z) that bypassed the EPIC3 controlled doorway: raw_sources.csv has zero data rows, db/nqa_audit.sqlite does not exist, derived/ is empty, and all 20 files are writable (rw-r--r--), not write-locked. docs/RAW_INTAKE.md (linked from both AGENTS.md and CLAUDE.md) forbids exactly this: files enter through incoming/ + promote_source.py only. Evidence: 'ls Enconet/raw | wc -l' = 20; manifest is header-only; 'ls Enconet/db' shows only schema.sql. Consequence: validate_raw_sources.py would fail closed on all 20 (unregistered + writable) as soon as the DB exists, and the files are also untracked in git. Requesting a disposition per ADR-0018: (a) route them through the doorway - move to incoming/, init the DB, promote each with reviewed metadata (side RULE presumably, language en) - or (b) remove them from raw/ until the owner reviews them, or (c) owner-accepted exception recorded with rationale. Claude Code will not register or move them unilaterally; the promotion step requires human-reviewed metadata.
