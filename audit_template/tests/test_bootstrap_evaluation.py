"""Synthetic, two-company checks for the evaluation transfer and gates."""
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

import yaml

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_state as state_bundle  # noqa: E402
import bootstrap_schema_validation as schema_bundle  # noqa: E402
import bootstrap_sieving as sieving_bundle  # noqa: E402
import bootstrap_sieving_score as score_bundle  # noqa: E402

RUN = "RUN-20261001-01"
CRUMB = "CRUMB-DOC-0002-APP_B_I-0001"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def command(target: Path, script: str, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-B", str(target / "scripts" / script), *args],
                          cwd=cwd, env=os.environ | {"PYTHONUTF8": "1"},
                          capture_output=True, text=True, encoding="utf-8", timeout=30)


def seed(target: Path) -> tuple[Path, Path]:
    db = target / "db/nqa_audit.sqlite"
    raw = target / "raw"
    raw.mkdir()
    scope = raw / "scope.txt"
    scope.write_text("Synthetic governing source", encoding="utf-8")
    evidence = raw / "evidence.txt"
    evidence.write_text("Synthetic supplier evidence", encoding="utf-8")
    criteria = yaml.safe_load((target / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))["criteria"]
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.executemany("INSERT INTO criteria VALUES (?,?,?)", [(r["criterion_id"], r["criterion_name"], r["description"]) for r in criteria])
        for doc_id, path, side in (("DOC-0001", scope, "RULE"), ("DOC-0002", evidence, "DOCUMENT")):
            conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
                         "VALUES (?,?,?,?,?,?,?)", (doc_id, path.name, "Synthetic", "Synthetic", "en", side,
                          hashlib.sha256(path.read_bytes()).hexdigest()))
        conn.execute("INSERT INTO approved_sources(source_code,authority_role,edition,source_sha256,approval_ref,approved_by,approved_date) "
                     "VALUES (?,?,?,?,?,?,?)", ("SYNTH-APP-B", "GOVERNING", "synthetic", hashlib.sha256(scope.read_bytes()).hexdigest(),
                                               "SYNTH-APPROVAL", "synthetic reviewer", "2026-10-01"))
        conn.execute("INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side) VALUES (?,?,?,?)",
                     ("RUN-20261001-02", "DOC-0002", "synthetic", "DOCUMENT"))
        conn.execute("INSERT INTO crumbs(item_id,doc_id,sieve_run_id,criterion_id,document_side,statement) "
                     "VALUES (?,?,?,?,?,?)", (CRUMB, "DOC-0002", "RUN-20261001-02", "APP_B_I", "DOCUMENT", "Synthetic"))
    approvals = target / "manifests/approvals.csv"
    approvals.write_text("object_id,decision,date,reviewer,notes\n"
                         f"G2-{RUN},approved,2026-10-01,synthetic reviewer,scope\n", encoding="utf-8")
    matrix = target / "inputs/rulings.json"
    matrix.parent.mkdir()
    matrix.write_text(json.dumps([{"criterion_id": r["criterion_id"], "applicable": True,
                                   "justification": "Synthetic scope", "scope_source_doc_id": "DOC-0001"}
                                  for r in criteria]), encoding="utf-8")
    return db, matrix


class EvaluationBundleTests(unittest.TestCase):
    def test_manifest_hashes_and_neutrality(self) -> None:
        import bootstrap_evaluation as bundle
        rows = bundle.load_manifest()["files"]
        self.assertEqual([r["path"] for r in rows], sorted(bundle.EVALUATION.exact_paths))
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_gates_preview_apply_retry_and_isolation(self) -> None:
        import bootstrap_evaluation as bundle
        for company, sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="evaluation-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    other = root / "Other Audit"
                    if sibling:
                        other.mkdir()
                        (other / "marker.txt").write_text("keep", encoding="utf-8")
                        nested = target / "Enconet"
                        nested.mkdir()
                        (nested / "marker.txt").write_text("keep nested", encoding="utf-8")
                        nested_before = snapshot(nested)
                    other_before = snapshot(other) if sibling else None
                    state_bundle.apply(target, "state-first")
                    schema_bundle.apply(target, "schema-first")
                    sieving_bundle.apply(target, "sieving-first")
                    score_bundle.apply(target, "score-first")
                    model_path = target / "schemas/scoring_model.yml"
                    model = yaml.safe_load(model_path.read_text(encoding="utf-8"))
                    model["model_version"] = "synthetic-v1"
                    model_path.write_text(yaml.safe_dump(model), encoding="utf-8")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 5)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "evaluation-first")["created"]), 5)
                    self.assertEqual(len(bundle.apply(target, "evaluation-retry")["preserved"]), 5)
                    db, matrix = seed(target)
                    work = other if sibling else root
                    args = (str(matrix), "--run-id", RUN, "--supplier", "Synthetic", "--language", "en")
                    db_before = (db.read_bytes(), db.stat().st_mtime_ns)
                    approvals = target / "manifests/approvals.csv"
                    approval_text = approvals.read_text(encoding="utf-8")
                    approvals.write_text("object_id,decision,date,reviewer,notes\n", encoding="utf-8")
                    no_g2 = command(target, "rule_applicability.py", *args, "--apply", cwd=work)
                    self.assertEqual(no_g2.returncode, 1)
                    self.assertIn("G2", no_g2.stderr)
                    self.assertEqual((db.read_bytes(), db.stat().st_mtime_ns), db_before)
                    approvals.write_text(approval_text, encoding="utf-8")
                    preview = command(target, "rule_applicability.py", *args, cwd=work)
                    self.assertEqual(preview.returncode, 0, preview.stderr)
                    self.assertEqual((db.read_bytes(), db.stat().st_mtime_ns), db_before)
                    foreign = command(target, "rule_applicability.py", *args, "--db", str(other / "foreign.sqlite"), "--apply", cwd=work)
                    self.assertEqual(foreign.returncode, 1)
                    self.assertFalse((other / "foreign.sqlite").exists())
                    foreign_matrix = command(target, "rule_applicability.py", str(other / "foreign.json"),
                                             "--run-id", RUN, "--supplier", "Synthetic", "--language", "en", cwd=work)
                    self.assertEqual(foreign_matrix.returncode, 1)
                    applied = command(target, "rule_applicability.py", *args, "--apply", cwd=work)
                    self.assertEqual(applied.returncode, 0, applied.stderr)
                    self.assertEqual(command(target, "rule_applicability.py", *args, "--apply", cwd=work).returncode, 0)
                    record = target / "inputs/evaluation.json"
                    record.write_text(json.dumps({"criterion_id": "APP_B_I", "classification": "fully",
                                                  "judge_ruling": "Synthetic", "rationale": "Synthetic evidence"}), encoding="utf-8")
                    eval_args = (str(record), "--run-id", RUN, "--evidence", CRUMB)
                    no_g3 = command(target, "write_evaluation.py", *eval_args, "--apply", cwd=work)
                    self.assertEqual(no_g3.returncode, 1)
                    self.assertIn("G3", no_g3.stderr)
                    model.update(calibration_status="approved", approval_ref=f"G3-{RUN}")
                    model_path.write_text(yaml.safe_dump(model), encoding="utf-8")
                    with approvals.open("a", encoding="utf-8") as handle:
                        handle.write(f"G3-{RUN},approved,2026-10-01,synthetic reviewer,synthetic-v1\n")
                    db_before = (db.read_bytes(), db.stat().st_mtime_ns)
                    self.assertEqual(command(target, "write_evaluation.py", *eval_args, cwd=work).returncode, 0)
                    self.assertEqual((db.read_bytes(), db.stat().st_mtime_ns), db_before)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("CREATE TRIGGER synthetic_evidence_failure BEFORE INSERT ON evaluation_evidence "
                                     "BEGIN SELECT RAISE(ABORT,'synthetic failure'); END")
                    failed = command(target, "write_evaluation.py", *eval_args, "--apply", cwd=work)
                    self.assertEqual(failed.returncode, 1)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        self.assertEqual(conn.execute("SELECT count(*) FROM criterion_evaluations").fetchone()[0], 0)
                        conn.execute("DROP TRIGGER synthetic_evidence_failure")
                    self.assertEqual(command(target, "write_evaluation.py", *eval_args, "--apply", cwd=work).returncode, 0)
                    self.assertEqual(command(target, "write_evaluation.py", *eval_args, "--apply", cwd=work).returncode, 0)
                    with closing(sqlite3.connect(db)) as conn:
                        self.assertEqual(conn.execute("SELECT count(*) FROM criterion_evaluations").fetchone()[0], 1)
                    score = command(target, "score_evaluation.py", "--run-id", RUN, cwd=work)
                    self.assertEqual(score.returncode, 1)  # full matrix not written yet
                    check = command(target, "validate_evaluation.py", "--run-id", RUN, cwd=work)
                    self.assertEqual(check.returncode, 1)
                    self.assertIn("incomplete", check.stderr)
                    criteria = yaml.safe_load((target / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))["criteria"]
                    for item in criteria[1:]:
                        cid = item["criterion_id"]
                        rating = "na" if cid == "APP_B_XVIII" else "undetermined"
                        if rating == "na":
                            with closing(sqlite3.connect(db)) as conn, conn:
                                conn.execute("UPDATE criterion_applicability SET applicable=0 WHERE evaluation_run_id=? AND criterion_id=?",
                                             (RUN, cid))
                        record.write_text(json.dumps({"criterion_id": cid, "classification": rating,
                                                      "judge_ruling": "Synthetic", "rationale": "Synthetic scope"}), encoding="utf-8")
                        result = command(target, "write_evaluation.py", str(record), "--run-id", RUN, "--apply", cwd=work)
                        self.assertEqual(result.returncode, 0, result.stderr)
                    complete = command(target, "validate_evaluation.py", "--run-id", RUN, cwd=work)
                    self.assertEqual(complete.returncode, 0, complete.stderr)
                    db_before = (db.read_bytes(), db.stat().st_mtime_ns)
                    score = command(target, "score_evaluation.py", "--run-id", RUN, cwd=work)
                    self.assertEqual(score.returncode, 0, score.stderr)
                    self.assertEqual(json.loads(score.stdout)["applicable_count"], 17)
                    self.assertEqual((db.read_bytes(), db.stat().st_mtime_ns), db_before)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("UPDATE sieve_runs SET status='superseded',is_active=0 WHERE run_id='RUN-20261001-02'")
                    broken = command(target, "validate_evaluation.py", "--run-id", RUN, cwd=work)
                    self.assertEqual(broken.returncode, 1)
                    self.assertIn("active DOCUMENT", broken.stderr)
                    self.assertEqual(snapshot(other) if sibling else None, other_before)
                    if sibling:
                        self.assertEqual(snapshot(nested), nested_before)

    def test_conflict_refuses_overwrite(self) -> None:
        import bootstrap_evaluation as bundle
        with tempfile.TemporaryDirectory(prefix="evaluation-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/evaluation_engine.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "evaluation-conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
