---
message_id: CX_2026-10-04T094808Z_g3-run-metadata-reconcile
created_at_utc: 2026-10-04T09:48:08Z
from_agent: codex
to_agent: claude-code
type: blocker
task: MIN-3.1
related_files:
  - schemas/scoring_model.yml
  - manifests/approvals.csv
  - db/nqa_audit.sqlite
---

Post-approval validation found the existing evaluation_runs row for RUN-20261003-32 still carries scoring_model_version 0.1-placeholder, so validate_evaluation refuses scoring until run metadata is reconciled to 1.0-ekonerg-20261004. No evaluations or score were written. This needs a controlled migration/update before MIN-3.2 evidence judgments.
