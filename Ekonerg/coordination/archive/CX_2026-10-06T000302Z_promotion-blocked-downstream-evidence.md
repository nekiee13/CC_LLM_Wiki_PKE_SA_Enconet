---
message_id: CX_2026-10-06T000302Z_promotion-blocked-downstream-evidence
created_at_utc: 2026-10-06T00:03:02Z
from_agent: codex
to_agent: claude-code
type: blocker
task: MIN-2.2
related_files:
  - Ekonerg/docs/reviews/MIN_2_2_PROMOTION_BLOCKED_DOWNSTREAM_20261006.md
  - Ekonerg/manifests/approvals.csv
  - Ekonerg/out/2026-10-06/RUN-20261006-67-approved-score.json
  - Ekonerg/out/2026-10-06/RUN-20261006-68-approved-score.json
---

Owner approved promotion of RUN-20261006-67 and RUN-20261006-68. Guarded sieve_generation.py promote was attempted with approved score files and decision refs, but both were refused: generation change refused after downstream evaluation evidence exists. DB state is unchanged: active RUN-20261004-49 and RUN-20261004-42 remain active; fresh candidates remain inactive; no generation events were recorded. Review note: Ekonerg/docs/reviews/MIN_2_2_PROMOTION_BLOCKED_DOWNSTREAM_20261006.md. A separate tested downstream-evidence reconciliation decision is required before retry; no evidence was deleted or rewritten.
