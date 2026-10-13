"""Read-only proof: only explicitly approved scoring-fixture metadata changed."""
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[3]
WORKSPACE = ROOT.parent
BASELINE = "bfb208bc61f973f0055a54fed15194c0384ea2f9"

def old_bytes(relative):
    return subprocess.check_output(["git","show",f"{BASELINE}:Enconet/{relative}"], cwd=WORKSPACE)

for filename, allowed in (("input.yml", {"fixture_version"}),
                          ("expected.yml", {"fixture_version","scoring_model_version","scoring_model_sha256"})):
    relative = f"benchmarks/scoring/{filename}"
    before = yaml.safe_load(old_bytes(relative))
    after = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
    assert set(before) == set(after)
    changed = {k for k in before if before[k] != after[k]}
    assert changed == allowed, (filename, changed)
    assert before["fixture_version"] == "1.0" and after["fixture_version"] == "1.1"
for filename in ("package.yml","expected.yml"):
    relative = f"benchmarks/dashboard_rendering/{filename}"
    # Git may normalize CRLF; compare only EOL-normalized bytes, not values.
    assert old_bytes(relative).replace(b"\r\n",b"\n") == (ROOT / relative).read_bytes().replace(b"\r\n",b"\n")
expected = yaml.safe_load((ROOT / "benchmarks/scoring/expected.yml").read_text(encoding="utf-8"))
model = yaml.safe_load((ROOT / "schemas/scoring_model.yml").read_text(encoding="utf-8"))
assert expected["scoring_model_version"] == model["model_version"] == "0.2-approved"
assert expected["scoring_model_sha256"] == hashlib.sha256((ROOT / "schemas/scoring_model.yml").read_bytes()).hexdigest()
old_model = yaml.safe_load((ROOT / "out/2026-10-08/g3-approved-run17/scoring_model_0.1_snapshot.yml").read_text(encoding="utf-8"))
assert all(model[k] == old_model[k] for k in ("rating_weights","consolidated_score","classification_thresholds"))
ratings = yaml.safe_load((ROOT / "benchmarks/scoring/input.yml").read_text(encoding="utf-8"))["ratings"]
weights = {"fully":Decimal(100),"substantially":Decimal(75),"partially":Decimal(50),"minimally":Decimal(25),"unmet":Decimal(0),"undetermined":Decimal(0)}
points = {k:float(weights[v]) if v != "na" else None for k,v in ratings.items()}
assert points == expected["per_criterion_scores"]
assert dict(Counter(ratings.values())) == expected["metrics"]["classification_counts"]
applicable = sum(v != "na" for v in ratings.values())
manual = (sum(weights[v] for v in ratings.values() if v != "na") / applicable).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
assert applicable == 16 and manual == Decimal("46.9") and float(manual) == expected["metrics"]["consolidated_score"]
sys.path.insert(0, str(ROOT / "scripts"))
import finding_workflow
rows = [r for r in finding_workflow.approval_rows() if r["object_id"] == "SCORING-FIXTURE-ENCONET-1.1-20261009"]
assert len(rows) == 1 and rows[0]["decision"] == "approved"
frozen = runpy.run_path(str(ROOT / "out/2026-10-08/findings-run17/execute_draft.py"))["frozen"]()
assert frozen == json.loads((ROOT / "out/2026-10-08/findings-run17/frozen-before.json").read_text(encoding="utf-8"))
print("PASS: only1input/3expected metadata fields changed;all18ratings/scores/counts/arithmetic unchanged;manual46.9 matches;dashboardfixture unchanged;19original DBtables unchanged;explicitownerpermission recorded")
