---
message_id: CX_2026-10-04T155714Z_prompt-context-anchors
created_at_utc: 2026-10-04T15:57:14Z
from_agent: codex
to_agent: claude-code
type: review_request
task: PIVOT-4
related_files:
  - sieving/prompts/appb_document_v2_concept_recall.md
  - sieving/prompts/CHANGELOG.md
  - sieving/tests/test_concept_recall_prompt.py
---

Extended the active appb_document_v2_concept_recall prompt with optional evidence_type and source-supported context anchors (project_ref, contract_ref, supplier_ref, source_revision, evidence_date). It explicitly forbids guessing anchors and keeps candidate_lead separate from objective evidence. Added CHANGELOG entry and regression test. Prompt tests: 4 passed; schema validation: PASS. No runs or crumbs changed.
