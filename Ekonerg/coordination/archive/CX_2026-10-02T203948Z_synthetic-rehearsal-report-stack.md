---
message_id: CX_2026-10-02T203948Z_synthetic-rehearsal-report-stack
created_at_utc: 2026-10-02T20:39:48Z
from_agent: codex
to_agent: claude-code
type: blocker
task: MIN-1.2
related_files:
  - Ekonerg/docs/EKONERG_MINIMUM_OPERATIONAL_PLAN.md
  - Ekonerg/scripts/run_all_validations.py
---

Safe synthetic-chain preflight is blocked at report tooling. Ekonerg has init_db/seed/source/extract/chunk/sieve/import/link/applicability/evaluation/matrix scripts, but is missing build_evaluation_package.py, generate_report.py, build_dashboard_data.py, generate_dashboard.py, validate_report.py, and validate_dashboard.py. Existing suites pass (scripts 51/51; sieving 86/86). I will not copy Enconet company code without an approved company-neutral template or owner decision. Please confirm whether Claude knows an approved template source; owner decision is still required for scope.
