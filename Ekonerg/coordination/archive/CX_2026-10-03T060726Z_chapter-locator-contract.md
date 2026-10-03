---
message_id: CX_2026-10-03T060726Z_chapter-locator-contract
created_at_utc: 2026-10-03T06:07:26Z
from_agent: codex
to_agent: claude-code
type: status
task: MIN-2.2
related_files:
  - Ekonerg/sieving/prompts/appb_document_v1.md
  - Ekonerg/docs/reviews/MIN_2_2_PROMPT_EVALUATION.md
  - Ekonerg/db/schema.sql
  - Ekonerg/scripts/chunk_document.py
---

Owner clarified that chapter preservation, not page preservation, is required. Updated appb_document_v1, MIN-2.2 evaluation packet, minimum operational plan, and schema comment. Canonical storage is document_chunks.heading_path and crumb_sources.source_heading_path/source_locator; page metadata is optional and never an identity. Tests passed: 7 synthetic/sieve + 16 extractor normalization.
