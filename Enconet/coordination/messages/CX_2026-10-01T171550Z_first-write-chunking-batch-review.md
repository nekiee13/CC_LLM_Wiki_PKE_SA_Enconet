---
message_id: CX_2026-10-01T171550Z_first-write-chunking-batch-review
created_at_utc: 2026-10-01T17:15:50Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EK-1.2
related_files:
  - audit_template/bootstrap_chunking.py
  - audit_template/chunking/v1/scripts/chunk_document.py
  - audit_template/tests/test_bootstrap_chunking.py
  - Ekonerg/scripts/chunk_document.py
---

Please review commit 324b4cb. Versioned first-write chunking bundle installs Ekonerg/scripts/chunk_document.py under run chunking-20261001-01. Runtime preview is read-only; apply reads one registered local derived text, requires level-1/2 headings and bounded chunks, writes offset-preserving DB rows and a new JSON artifact, and refuses to replace existing chunks or artifact. Late SQL failure rolls back rows and removes only the artifact created by that invocation. Two synthetic company names (space and Croatian character) with/without sibling passed. TDD RED focused exit 1 (four missing-module errors), GREEN focused 4 tests exit 0, full template 58 exit 0; Ekonerg tools 111, sieving 86, scripts 40, manifest verify all exit 0. Live CLI stopped at missing DB, no incoming docs processed. Please review the first-write/rollback contract. Separately, owner was asked to choose generation activation policy; no promotion tool was copied while score/run binding and DB/file atomicity are unresolved.
