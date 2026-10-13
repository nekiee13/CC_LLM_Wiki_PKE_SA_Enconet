"""Read-only proof of the owner-approved G4 status-only transition."""
import hashlib
import json
from pathlib import Path
import runpy
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_state
import finding_workflow
import validate_findings
import build_evaluation_package

draft = ROOT / "out/2026-10-08/findings-run17"
job = runpy.run_path(str(draft / "execute_draft.py"))
assert job["frozen"]() == json.loads((draft / "frozen-before.json").read_text(encoding="utf-8"))
expected = json.loads((draft / "prepared-records.json").read_text(encoding="utf-8"))
with sqlite3.connect((ROOT / "db/nqa_audit.sqlite").as_uri() + "?mode=ro", uri=True) as c:
    c.row_factory = sqlite3.Row
    assert not c.execute("PRAGMA foreign_key_check").fetchall()
    for table, count in (("gaps",18),("findings",12),("auditor_actions",18)):
        assert c.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] == count
    for record in expected:
        for key, table, pk in (("gap","gaps","gap_id"),("finding","findings","finding_id"),("action","auditor_actions","action_id")):
            value = record[key]
            if value is None:
                continue
            actual = dict(c.execute(f'SELECT * FROM "{table}" WHERE "{pk}"=?',(value[pk],)).fetchone())
            assert all(actual[k] == v for k,v in value.items()), (table,value[pk])
            if key != "gap":
                assert actual["status" if key == "finding" else "approval_status"] == "approved"
                assert actual["approval_ref"] == value[pk]
                assert actual["verification_status" if key == "finding" else "state"] == ("pending" if key == "finding" else "open")
                rows = [r for r in finding_workflow.approval_rows() if r["object_id"] == value[pk]]
                assert len(rows) == 1 and rows[0]["decision"] == "approved"
state = audit_state.load_state()
assert state["gates"]["G4"]["decision_ref"] == "G4-RUN-20261008-17"
assert state["gates"]["G4"]["status"] == "approved"
gate_rows = [r for r in finding_workflow.approval_rows() if r["object_id"] == "G4-RUN-20261008-17"]
assert len(gate_rows) == 1 and gate_rows[0]["decision"] == "approved"
assert state["phase"] == "findings_drafted", "Benchmark hold must remain until explicit fixture permission/checks"
assert not validate_findings.validate(ROOT / "db/nqa_audit.sqlite")
before = json.loads((ROOT / "out/2026-10-08/g3-approved-run17/enconet_appendix_b_evaluation_package.json").read_text(encoding="utf-8"))
now = build_evaluation_package.build(ROOT / "db/nqa_audit.sqlite", "RUN-20261008-17")
assert all(now[k] == before[k] for k in ("run","applicability","evaluations","metrics"))
assert hashlib.sha256((ROOT / "benchmarks/scoring/expected.yml").read_bytes()).hexdigest() == "ba77a96e76bb8ce3549ce9e47a98f2bcbfc29f343af0f268175e7bf9b7fe233a"
print("PASS:31 explicit G4/object approval rows;12 approved findings pending verification;18 approved actions open;18 unchanged coverage rows;19 original tables and score80.6 unchanged;fixture untouched;phase held")
