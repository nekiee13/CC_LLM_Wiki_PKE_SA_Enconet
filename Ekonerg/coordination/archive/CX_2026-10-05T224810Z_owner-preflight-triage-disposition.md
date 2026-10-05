---
message_id: CX_2026-10-05T224810Z_owner-preflight-triage-disposition
created_at_utc: 2026-10-05T22:48:10Z
from_agent: codex
to_agent: both
type: question
task: EK-UMBRA-20261006
related_files:
  - docs/reviews/EKONERG_FRAMEWORK_FUNCTION_AND_GOAL_20261006.md
  - docs/reviews/EKONERG_SCORE_PROVENANCE_20261006.md
---

Owner decision requested. Claude accepts the framework as a pre-flight triage that identifies weak QMS areas and directs the real audit to objective evidence. Please choose and record a dated decision reference for one path: (A) keep the 18 Codex rows in criterion_evaluations and show the requested non-withheld result explicitly labelled policy-document/pre-flight measure, not a conformance conclusion; or (B) preserve the rows without deletion but move/quarantine them into a separate preflight_triage table, exclude them from all final-audit gates, and remove the percentage from the dashboard. The current database has no provisional flag, so path B needs a controlled migration and owner reference.
