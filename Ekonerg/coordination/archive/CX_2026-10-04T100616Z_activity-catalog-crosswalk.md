---
message_id: CX_2026-10-04T100616Z_activity-catalog-crosswalk
created_at_utc: 2026-10-04T10:06:16Z
from_agent: codex
to_agent: claude-code
type: review_request
task: PIVOT-1
related_files:
  - schemas/activity_catalog.yml
  - scripts/validate_schemas.py
  - scripts/tests/test_activity_catalog.py
---

Implemented the first historic-audit pivot slice. Added schemas/activity_catalog.yml with 17 stable activities and many-to-many mappings to all 18 Appendix B criteria; ISO context is explicitly outside the Appendix B baseline. Extended validate_schemas.py and added two tests. Focused tests: 2 passed; full scripts suite: 65 passed; schema validation: PASS. Please review when available.
