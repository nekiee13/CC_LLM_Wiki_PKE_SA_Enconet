"""Gap tools remain local, transaction-safe, and draft-only in fake audits."""
from __future__ import annotations

from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_state as state_bundle  # noqa: E402

EVAL_RUN = "RUN-20261001-01"
EVAL = "EVAL-APP_B_I"
GAP = "GAP-APP_B_I-01"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def seed(target: Path) -> Path:
    db = target / "db/nqa_audit.sqlite"
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.execute("INSERT INTO criteria VALUES ('APP_B_I','Organization','synthetic')")
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
                     "VALUES ('DOC-0001','fake.txt','Fake','Fake Supplier','en','DOCUMENT',?)", ("a" * 64,))
        conn.execute("INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side) "
                     "VALUES ('RUN-20261001-02','DOC-0001','synthetic','DOCUMENT')")
        conn.execute("INSERT INTO crumbs(item_id,doc_id,sieve_run_id,criterion_id,document_side,statement) "
                     "VALUES ('CRUMB-DOC-0001-APP_B_I-0001','DOC-0001','RUN-20261001-02',"
                     "'APP_B_I','DOCUMENT','Synthetic claim')")
        conn.execute("INSERT INTO evaluation_runs(run_id,supplier,deliverable_language,scoring_model_version) "
                     "VALUES (?,?,?,?)", (EVAL_RUN, "Fake Supplier", "en", "synthetic"))
        conn.execute("INSERT INTO criterion_evaluations "
                     "(evaluation_id,evaluation_run_id,criterion_id,rating,score,coverage,completeness,"
                     "accuracy,clarity,alignment,evidence_supported,affirmative_summary,contrary_summary,"
                     "judge_ruling,rationale) VALUES (?,?,?,'undetermined',0,0,0,0,0,0,0,'','','','synthetic')",
                     (EVAL, EVAL_RUN, "APP_B_I"))
    return db


class GapWorkflowBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_gap_workflow as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows],
                         ["scripts/gap_register.py", "scripts/validate_gaps.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_preview_apply_retry_and_validation(self) -> None:
        import bootstrap_gap_workflow as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="gap-workflow-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                        nested = target / "Enconet"
                        nested.mkdir()
                        (nested / "marker.txt").write_text("keep nested", encoding="utf-8")
                        nested_before = snapshot(nested)
                    sibling_before = snapshot(sibling) if with_sibling else None
                    state_bundle.apply(target, "state-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 2)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "gap-first")["created"]), 2)
                    self.assertEqual(len(bundle.apply(target, "gap-retry")["preserved"]), 2)
                    record = target / "inputs/gap.json"
                    record.parent.mkdir()
                    body = {"gap_id": GAP, "evaluation_id": EVAL, "status": "missing-evidence",
                            "description": "Need a procedure", "missing_evidence_ref": "procedure P",
                            "action_type": "document_request", "action_description": "Ask for procedure P"}
                    record.write_text(json.dumps(body), encoding="utf-8")

                    def register(*extra: str, record_path: Path = record) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/gap_register.py"),
                             str(record_path), *extra], cwd=sibling if with_sibling else root,
                            env=os.environ | {"PYTHONUTF8": "1"}, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    missing = register("--apply")
                    self.assertEqual(missing.returncode, 1)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    db = seed(target)
                    db_before = (db.read_bytes(), db.stat().st_mtime_ns)
                    no_action = dict(body)
                    no_action.pop("action_type")
                    record.write_text(json.dumps(no_action), encoding="utf-8")
                    self.assertEqual(register("--apply").returncode, 1)
                    self.assertEqual((db.read_bytes(), db.stat().st_mtime_ns), db_before)
                    record.write_text(json.dumps(body), encoding="utf-8")
                    preview = register()
                    self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
                    self.assertEqual(json.loads(preview.stdout)["mode"], "preview")
                    self.assertEqual((db.read_bytes(), db.stat().st_mtime_ns), db_before)
                    foreign = register("--db", str(sibling / "foreign.sqlite"), "--apply")
                    self.assertEqual(foreign.returncode, 1)
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    foreign_record = register("--apply", record_path=sibling / "foreign.json")
                    self.assertEqual(foreign_record.returncode, 1)
                    applied = register("--apply")
                    self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
                    self.assertEqual(json.loads(applied.stdout)["action_id"], "ACT-0001")
                    self.assertEqual(json.loads(register("--apply").stdout)["mode"], "preserve")
                    with closing(sqlite3.connect(db)) as conn:
                        self.assertEqual(conn.execute("SELECT count(*) FROM gaps").fetchone()[0], 1)
                        self.assertEqual(conn.execute("SELECT count(*) FROM auditor_actions").fetchone()[0], 1)
                        self.assertEqual(conn.execute("SELECT approval_status FROM auditor_actions").fetchone()[0],
                                         "draft")
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("CREATE TRIGGER synthetic_action_failure BEFORE INSERT ON auditor_actions "
                                     "BEGIN SELECT RAISE(ABORT, 'synthetic action failure'); END")
                    second = dict(body, gap_id="GAP-APP_B_I-02", description="Need another procedure")
                    record.write_text(json.dumps(second), encoding="utf-8")
                    self.assertEqual(register("--apply").returncode, 1)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        self.assertEqual(conn.execute("SELECT count(*) FROM gaps").fetchone()[0], 1)
                        self.assertEqual(conn.execute("SELECT count(*) FROM auditor_actions").fetchone()[0], 1)
                        conn.execute("DROP TRIGGER synthetic_action_failure")
                    validator = subprocess.run(
                        [sys.executable, "-B", str(target / "scripts/validate_gaps.py")],
                        cwd=sibling if with_sibling else root,
                        env=os.environ | {"PYTHONUTF8": "1"}, capture_output=True,
                        text=True, encoding="utf-8", timeout=30,
                    )
                    self.assertEqual(validator.returncode, 0, validator.stdout + validator.stderr)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("DELETE FROM auditor_actions")
                    broken = subprocess.run(
                        [sys.executable, "-B", str(target / "scripts/validate_gaps.py")],
                        cwd=sibling if with_sibling else root,
                        env=os.environ | {"PYTHONUTF8": "1"}, capture_output=True,
                        text=True, encoding="utf-8", timeout=30,
                    )
                    self.assertEqual(broken.returncode, 1)
                    self.assertIn("missing-evidence", broken.stderr)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, sibling_before)
                    if with_sibling:
                        self.assertEqual(snapshot(nested), nested_before)

    def test_conflict_blocks_copy(self) -> None:
        import bootstrap_gap_workflow as bundle

        with tempfile.TemporaryDirectory(prefix="gap-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/gap_register.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "gap-conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
