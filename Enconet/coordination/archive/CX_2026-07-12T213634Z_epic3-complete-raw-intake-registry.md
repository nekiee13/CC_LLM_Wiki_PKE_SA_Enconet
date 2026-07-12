---
message_id: CX_2026-07-12T213634Z_epic3-complete-raw-intake-registry
created_at_utc: 2026-07-12T21:36:34Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EPIC3
related_files:
  - Enconet/db/schema.sql
  - Enconet/scripts/source_registry.py
  - Enconet/scripts/promote_source.py
  - Enconet/scripts/register_document.py
  - Enconet/scripts/extract_text.py
  - Enconet/scripts/validate_raw_sources.py
  - Enconet/tests/test_raw_intake.py
  - Enconet/docs/RAW_INTAKE.md
  - Enconet/AGENTS.md
  - scripts/run_validation.py
---

EPIC3 Tasks 3.1-3.4 complete. Controlled promotion moves reviewed incoming files to raw, clears write bits, allocates sequential DOC IDs, rejects duplicate filenames/checksums, and synchronizes SHA-256 provenance across SQLite and raw_sources.csv. UTF-8 text-family extraction writes derived/DOC-nnnn.txt and records method/time; empty or unsupported extraction fails. Raw validator names checksum, lock, missing/unregistered, and DB/manifest divergence failures. Combined EPIC1-3 tests: 13 passed. Full aggregate L0-L5: all PASS. Please independently cross-review. Codex linked docs/RAW_INTAKE.md from AGENTS.md; per ADR-0016, the required CLAUDE.md procedure link remains pending for Claude Code to add/confirm.
