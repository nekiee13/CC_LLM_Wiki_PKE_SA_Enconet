"""Recorded, bounded G4 drafting job; normal project writers own all DB writes.

Preview is read-only. Apply refuses existing draft rows, preventing double import.
Verify proves all original tables/ratings retained and draft records/pages resolve.
This is a run artifact, not a new framework API or scoring implementation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import finding_workflow as workflow
import gap_register
import validate_findings
import validate_gaps
import audit_state
import build_evaluation_package

DB = ROOT / "db/nqa_audit.sqlite"
PACKAGE = ROOT / "out/2026-10-08/g3-approved-run17/enconet_appendix_b_evaluation_package.json"

def frozen():
    with sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True) as conn:
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        return {t: hashlib.sha256(json.dumps(conn.execute(f'SELECT * FROM "{t}" ORDER BY rowid').fetchall(), ensure_ascii=False, sort_keys=True).encode()).hexdigest()
                for t in tables if t not in {"gaps", "findings", "auditor_actions"}}

def prepare():
    plan = json.loads((HERE / "draft-plan.json").read_text(encoding="utf-8"))
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    run = plan["run_id"]
    assert package["run"]["run_id"] == run
    current = build_evaluation_package.build(DB, run)
    assert all(current[k] == package[k] for k in ("run", "applicability", "evaluations", "metrics", "approvals")), "approved assessment changed"
    workflow.require_input_gates(run)
    records = []
    with sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True) as conn:
        for index, spec in enumerate(plan["criteria"], 1):
            cid = "APP_B_" + spec["criterion"]
            evaluation = next(e for e in package["evaluations"] if e["criterion_id"] == cid)
            source = json.loads((ROOT / "out/2026-10-08/conformance-run17/records" / f"{cid}.json").read_text(encoding="utf-8"))
            # Select an exact same-criterion evaluated DOCUMENT anchor, not a RULE crumb.
            evidence = next(item for item in evaluation["evidence_ids"] if conn.execute(
                "SELECT 1 FROM active_crumbs WHERE item_id=? AND criterion_id=? AND document_side='DOCUMENT'", (item, cid)).fetchone())
            full = evaluation["classification"] == "fully"
            status = {"fully": "covered", "substantially": "mostly-covered", "partially": "partially-covered"}[evaluation["classification"]]
            gap_id = f"GAP-{cid}-01"
            gap = dict(gap_id=gap_id, evaluation_id=evaluation["evaluation_id"], status=status,
                       description=("Dokumentacijski pokriveno; rutinska terenska provjera nije dokumentarni nedostatak. " if full else "Dokumentarna praznina/ograničenje u odobrenoj procjeni: ") + evaluation["contrary_summary"],
                       evidence_item_id=evidence)
            finding = None
            if not full:
                count = sum(r["finding"] is not None for r in records) + 1
                finding = dict(finding_id=f"FIND-{count:04d}", evaluation_run_id=run, criterion_id=cid, gap_id=gap_id,
                    title=spec["title"], severity="medium" if evaluation["classification"] == "partially" else "low", confidence="medium",
                    verification_status="pending", basis=f"10 CFR 50 Appendix B {spec['criterion']}; NQA-1:2015 Part I Requirement {index}; approved G2/G3 scope" + ("; Req18 §201.3" if index == 18 else ""),
                    body="Dokumentacijski pre-flight nalaz; nije potvrđena terenska nesukladnost.\n\nU prilog: " + evaluation["affirmative_summary"] + "\n\nOgraničenje: " + evaluation["contrary_summary"] + "\n\nZaključak: " + evaluation["judge_ruling"] + "\n\nDokazni crumbs: " + ", ".join(evaluation["evidence_ids"]) + "\n\nIzvorni citati i poglavlja: out/2026-10-08/conformance-run17/evidence-trace.json. Ocjena i izvori ostaju nepromijenjeni.")
            action = dict(action_id=f"ACT-{index:04d}", evaluation_run_id=run, gap_id=gap_id, action_type=spec["type"],
                description=spec.get("action", source["verification_actions"][0]["description"]) + (" Rutinska provjera provedbe; nije dokumentarni nalaz." if full else " Provjeriti objektivne zapise prije zaključka o provedbi."), priority=spec["priority"])
            records.append(dict(gap=gap, finding=finding, action=action))
    assert len(records) == 18 and sum(r["finding"] is not None for r in records) == 12
    return records

def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    assert not (args.apply and args.verify)
    records = prepare()
    if args.verify:
        assert frozen() == json.loads((HERE / "frozen-before.json").read_text(encoding="utf-8")), "original table changed"
        with sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True) as c:
            for table, count in (("gaps", 18), ("findings", 12), ("auditor_actions", 18)):
                assert c.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] == count
            assert c.execute("SELECT count(*) FROM findings WHERE status!='draft' OR approval_ref IS NOT NULL").fetchone()[0] == 0
            assert c.execute("SELECT count(*) FROM auditor_actions WHERE approval_status!='draft' OR approval_ref IS NOT NULL OR state!='open'").fetchone()[0] == 0
            for record in records:
                for key, table, id_column in (("gap", "gaps", "gap_id"), ("finding", "findings", "finding_id"), ("action", "auditor_actions", "action_id")):
                    expected = record[key]
                    if expected is None:
                        continue
                    c.row_factory = sqlite3.Row
                    row = dict(c.execute(f'SELECT * FROM "{table}" WHERE "{id_column}"=?', (expected[id_column],)).fetchone())
                    assert all(row[k] == v for k, v in expected.items()), (table, expected[id_column])
        assert not validate_gaps.validate(DB)
        assert not validate_findings.validate(DB)
        print("VERIFY PASS: 18 coverage rows,12 draft findings,18 open draft actions; original tables and ratings unchanged")
        return
    with sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True) as c:
        assert all(c.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] == 0 for t in ("gaps", "findings", "auditor_actions")), "draft rows already present; use --verify, never repeat apply"
    if not args.apply:
        for r in records:
            print(r["gap"]["gap_id"], r["gap"]["status"], r["finding"]["finding_id"] if r["finding"] else "routine-only", r["action"]["action_id"], r["action"]["action_type"])
        print("PREVIEW: read-only,18 coverage rows,12 findings,18 actions; no approval or score write")
        return
    assert not (HERE / "frozen-before.json").exists(), "apply snapshot exists; inspect before resuming"
    assert audit_state.load_state()["phase"] == "evaluated", "apply requires evaluated phase"
    (HERE / "frozen-before.json").write_text(json.dumps(frozen(), indent=2) + "\n", encoding="utf-8", newline="\n")
    (HERE / "prepared-records.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    for record in records:
        gap_register.write_gap(DB, record["gap"])
        if record["finding"]:
            workflow.write_finding(DB, record["finding"])
        workflow.write_action(DB, record["action"])
    print("APPLY:18 coverage rows,12 draft findings,18 draft actions; G4 not approved")

if __name__ == "__main__":
    main()
