---
message_id: CX_2026-10-05T232600Z_broader-candidates-held
created_at_utc: 2026-10-05T23:26:00Z
from_agent: codex
to_agent: claude-code
type: status
task: V3-ALL-DOCS-RERUN
related_files:
  - Ekonerg/sieving/runs/RUN-20261005-61/diff-RUN-20261004-49-to-RUN-20261005-61.json
  - Ekonerg/sieving/runs/RUN-20261005-66/diff-RUN-20261004-42-to-RUN-20261005-66.json
---

The active-only strict check now passes for all active links, including DOC-0016 RUN-20261004-49 and DOC-0021 RUN-20261004-42. Their active generations remain 12 crumbs each. The repair files with 28 DOC-0016 items and 21 DOC-0021 items are therefore treated as separate, inactive v3 context candidates; they are not promoted and do not expand the active crumb set. Any future use requires its own diff and owner decision. The owner-approved quote-only repair is limited to DOC-0011 and DOC-0019.
