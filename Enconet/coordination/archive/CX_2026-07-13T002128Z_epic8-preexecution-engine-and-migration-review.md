---
message_id: CX_2026-07-13T002128Z_epic8-preexecution-engine-and-migration-review
created_at_utc: 2026-07-13T00:21:28Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EPIC8
related_files:
  - Enconet/db/schema.sql
  - Enconet/scripts/migrate_db.py
  - Enconet/scripts/evaluation_engine.py
  - Enconet/scripts/rule_applicability.py
  - Enconet/scripts/write_evaluation.py
  - Enconet/scripts/score_evaluation.py
  - Enconet/scripts/build_evaluation_package.py
  - Enconet/scripts/validate_evaluation.py
  - Enconet/schemas/evaluation_package_schema.yml
  - Enconet/tests/test_epic8_evaluation.py
---

EPIC8 engine and destructive-capable empty-table migration are ready for pre-execution review. Live dry-run only: actions=['recreate empty EPIC8 evaluation tables']; no backup/change. Migration refuses if any evaluation/applicability/gap/finding/action/dashboard data exists. Engine requires a G2-<run_id> approved approvals.csv row, exactly 18 rulings, and raw document citations; prevents ruling changes while evaluations exist; expands evaluation rows with five quality dimensions, evidence flag, affirmative/contrary/judge fields; positive ratings require linked DOCUMENT crumbs or explicit auto-downgrade to undetermined plus missing-evidence gap; na is restricted to approved not-applicable rulings. Scores read only scoring_model.yml with half-up rounding; package is stable sorted JSON with all records/metrics/gaps/actions; validator rechecks completeness, citations, evidence, applicability, and stored scores. Evidence: focused 16 passed; full 103 passed; validate_schemas 9 contracts PASS. Operational boundary: no live Enconet rulings/evaluations may be fabricated; G2 applicability approval, supplier DOCUMENT crumbs, and G3 model calibration remain human/input gates. Please review migration safety and Tasks 8.1-8.6; explicitly authorize or block live schema apply.
