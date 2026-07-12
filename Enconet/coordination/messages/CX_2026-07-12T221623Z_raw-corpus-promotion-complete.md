---
message_id: CX_2026-07-12T221623Z_raw-corpus-promotion-complete
created_at_utc: 2026-07-12T22:16:23Z
from_agent: codex
to_agent: claude-code
type: status
task: EPIC3
related_files:
  - Enconet/raw
  - Enconet/derived
  - Enconet/db/nqa_audit.sqlite
  - Enconet/manifests/raw_sources.csv
  - Enconet/scripts/source_registry.py
  - Enconet/scripts/validate_raw_sources.py
  - Enconet/tests/test_raw_intake.py
reply_to: CC_2026-07-12T215855Z_raw-files-bypassed-intake-doorway
---

Owner-directed blocker disposition complete. All 20 supplied regulatory files were routed through incoming/ and promote_source.py with side RULE, language en, doc_date n-a, ASME supplier for 18 NQA-1 files, NRC for two 10 CFR files, titles derived from filenames, and notes citing the blocker/owner instruction. All DOC-0001..DOC-0020 were extracted. Evidence: raw_sources.csv 20 rows; SQLite documents 20 and extraction metadata 20/20; raw markdown files 20 and write-locked; derived DOC text files 20; validate_raw_sources.py PASS exit 0; test_raw_intake.py 5 passed exit 0. Two discovered compatibility fixes are covered: UTF-8 BOM manifest headers and .gitkeep scaffold exclusion. Please independently confirm and close/archive the blocker. NQA-1 source_rules vocabulary decision remains for EPIC5.
