---
message_id: CX_2026-10-05T220421Z_crumb-source-chapter-links
created_at_utc: 2026-10-05T22:04:21Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EK-UMBRA-20261006
related_files:
  - scripts/build_umbra_conformance_dashboard.py
  - scripts/tests/test_umbra_conformance_dashboard.py
  - out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.html
  - docs/reviews/EKONERG_UMBRA_DASHBOARD_PARITY_20261005.md
---

Updated the Ekonerg dashboard so each score-linked vendor crumb opens its source document filename, chapter heading path, linked quote, and stored chapter text. The data comes from evaluation_evidence -> crumbs -> crumb_quotes -> crumb_chunk_links -> document_chunks; no page IDs are used. Added HTML-safe rendering for source text and regression assertions. Generator and focused tests pass 5/5. Please review the chapter linkage and standalone click behavior.
