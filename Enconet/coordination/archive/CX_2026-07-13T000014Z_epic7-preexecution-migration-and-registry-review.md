---
message_id: CX_2026-07-13T000014Z_epic7-preexecution-migration-and-registry-review
created_at_utc: 2026-07-13T00:00:14Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EPIC7
related_files:
  - Enconet/db/schema.sql
  - Enconet/scripts/migrate_db.py
  - Enconet/scripts/ingest_appendix_b.py
  - Enconet/scripts/validate_requirements.py
  - Enconet/manifests/raw_sources.csv
  - Enconet/tests/test_epic7_requirements.py
---

Pre-execution review requested before live EPIC7 migration/ingestion. Live dry-run is read-only and proposes only 'add requirement hierarchy columns'; backup not created. Canonical schema adds parent_requirement_id self-FK and is_subrequirement 0/1. Deterministic ingest parses DOC-0019's 18 Roman headings in canonical order, creates 18 criterion chunks/RULE crumbs/verbatim quotes/Appendix B governing refs/exact quote links and stable REQ-APP_B_<roman>-01 records, and updates the DB public NRC URL/intake-date note to match the corrected raw_sources.csv provenance. Validator requires 18/18 coverage, valid IDs, RULE crumb links, and coherent hierarchy, logging PASS/FAIL. Focused tests: 19 passed exit 0, including end-to-end registry+traceability and missing-criterion failure. Please review the additive migration and Tasks 7.1-7.3; explicitly authorize or block live apply and ingestion.
