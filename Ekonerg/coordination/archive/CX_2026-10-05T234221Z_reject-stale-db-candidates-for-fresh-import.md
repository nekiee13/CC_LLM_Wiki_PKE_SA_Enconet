---
message_id: CX_2026-10-05T234221Z_reject-stale-db-candidates-for-fresh-import
created_at_utc: 2026-10-05T23:42:21Z
from_agent: codex
to_agent: both
type: question
task: MIN-2.2
related_files:
  - Ekonerg/sieving/candidates/repairs-20261005/DOC-0016.json
  - Ekonerg/sieving/candidates/repairs-20261005/DOC-0021.json
  - Ekonerg/docs/reviews/MIN_2_2_V3_SCOPE2_GOLDEN_DRAFTS_20261006.md
---

Owner decision needed before fresh DB import: authorize rejection of stale inactive candidates RUN-20261005-61 (DOC-0016) and RUN-20261005-66 (DOC-0021), because each contains one non-exact quote. This is separate from the existing scope approvals SCOPE-DOC0016-V3-20261006-OWNER and SCOPE-DOC0021-V3-20261006-OWNER. After rejection, Codex will import the corrected JSON files as new inactive generations, run strict validation, candidate diffs, and draft golden scores. No active generation will change. Please provide two rejection references or explicitly authorize use of named references.
