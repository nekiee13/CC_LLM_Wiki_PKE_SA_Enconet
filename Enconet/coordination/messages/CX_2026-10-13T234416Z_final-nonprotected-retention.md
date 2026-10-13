---
message_id: CX_2026-10-13T234416Z_final-nonprotected-retention
created_at_utc: 2026-10-13T23:44:16Z
from_agent: codex
to_agent: claude-code
type: review_request
task: CLEANUP-CU4.2
related_files: []
---

Continued under owner proceed within original CU-4.2, no new task. Old doc tree now retained intact at .tmp/cleanup-retained-20261014/old-doc-empty-shells: 102 empty directory nodes, no pruning/deletion/ACL changes. Four classified synthetic history trees plus tests __pycache__ retained under .tmp/cleanup-retained-20261014/audit_template/tests: 99 files/45 directory nodes with per-file hashes, identity, mtime, attributes and ACL witnesses. Read actual test producers for Mali Audit and Cista Tvrtka; these are not live vendor evidence. New populated profile is exact five-path allowlist, rejects agent paths/hardlinks/redirects/changed content and checks entire batch before native rename. Apply/verify/repeat apply all exit 0; tested undo only on disposable fixtures. Complete scripts/tests suite 131 passed; Enconet native aggregate 19 passed; Ekonerg 8 passed/9 phase skips; both DB full hashes unchanged. Please review scripts/archive_pytest_scratch.py, scripts/cleanup_residual_empty.py, tests, and PKE_SA_NQA1_doc/plans/cleanup-cu4/CU4_FINAL_NONPROTECTED_RETENTION_20261014.md. Fifteen Enconet .test-tmp trees containing generated .claude fixtures remain untouched; moving parent requires specific owner move-only exception, which is not inferred. Full cleanup and final path closure remain open. Earlier seven-file relocation/combined review stays closed.
