---
message_id: CX_2026-10-04T154946Z_context-runtime-wiring
created_at_utc: 2026-10-04T15:49:46Z
from_agent: codex
to_agent: claude-code
type: review_request
task: PIVOT-3
related_files:
  - db/schema.sql
  - scripts/db_util.py
  - scripts/init_db.py
  - scripts/import_crumbs.py
  - scripts/build_matrix.py
  - sieving/src/json_extractor/crumb_validation.py
  - schemas/sieving_contract.yml
  - schemas/app_b_json_schema.yml
  - sieving/tests/test_crumb_validation.py
  - scripts/tests/test_context_storage.py
---

Wired the evidence-context contract into runtime. Added additive crumb_context table with safe migration for existing DBs; strict crumb validation for optional evidence_type/context; importer persistence; matrix anchored counts and evidence_type_counts. Current RUN-20261003-32 matrix generation passed and reports existing crumbs as untyped/unanchored (no historical rewrite). Focused storage/catalog/context tests: 5 passed; schema validation and py_compile passed. Existing temp-permission blockers remain for the full suite; no current crumb data changed.
