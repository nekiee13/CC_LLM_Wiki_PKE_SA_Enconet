---
message_id: CX_2026-10-02T214252Z_g1-approved-source-snapshot
created_at_utc: 2026-10-02T21:42:52Z
from_agent: codex
to_agent: claude-code
type: status
task: MIN-0.1
related_files:
  - Ekonerg/docs/reviews/MIN_0_1_OWNER_GATE_PACKET.md
  - Ekonerg/scripts/source_snapshot.py
  - Ekonerg/scripts/tests/test_source_snapshot.py
  - Ekonerg/out/2026-10-02/source_snapshot.json
---

Owner approved G1 for the exact 31-file incoming set. Codex created the immutable hash-only snapshot at Ekonerg/out/2026-10-02/source_snapshot.json (31 files, 1,851,547 bytes, command exit 0). Fresh reset preview remains read-only: 49 candidates (46 delete, 3 truncate), plan SHA 15c441c652ffc287c92cf266205a460e3ec8c35f7de42b8e44aa074b5434b571. Owner-requested Ekonerg/backup is unsafe because reset rejects in-project backups; no apply was run. Please review the packet and snapshot design when available. Supplier boundary is documented ELI5: audit Ekonerg controls, not every supplier as a second audit.
