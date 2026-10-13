"""Record actual owner-approved package size/security/timing measurements."""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_dashboard
import validate_evidence_access_budgets as validator
PACKAGE = ROOT / "outputs/candidates/evidence_access/report_review_RUN-20261008-17"
PROFILE = ROOT / "schemas/evidence_access_budgets_v2.yml"
budgets = generate_dashboard.load_budget_profile(PROFILE)
errors, static = validator.validate_static(PACKAGE, budgets)
browser_errors, browser = validator.validate_browser(PACKAGE, budgets)
errors.extend(browser_errors)
result = {"profile":str(PROFILE.relative_to(ROOT)), "static":static, "browser":browser,
          "errors":errors, "passed":not errors}
(Path(__file__).parent / "budget-measurements.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(result))
raise SystemExit(int(bool(errors)))
