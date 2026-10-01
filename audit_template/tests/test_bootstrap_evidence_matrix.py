"""Evidence-matrix copies and commands stay local and read the DB only."""
from __future__ import annotations

import hashlib
import json
import os
from contextlib import closing
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import yaml

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_sieving as sieve_bundle  # noqa: E402
import bootstrap_state as state_bundle  # noqa: E402

RUN = "RUN-20261001-01"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def seed(target: Path) -> Path:
    db = target / "db/nqa_audit.sqlite"
    taxonomy = yaml.safe_load((target / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.executemany("INSERT INTO criteria VALUES (?,?,?)", [
            (row["criterion_id"], row["criterion_name"], row["description"])
            for row in taxonomy["criteria"]
        ])
        conn.execute("INSERT INTO evaluation_runs(run_id,supplier,deliverable_language,scoring_model_version) "
                     "VALUES (?,?,?,?)", (RUN, "Fake Supplier", "en", "synthetic"))
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
                     "VALUES ('DOC-0001','fake.txt','Fake','Fake Supplier','en','RULE',?)", ("a" * 64,))
        conn.execute("INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side) "
                     "VALUES ('RUN-20261001-02','DOC-0001','synthetic','RULE')")
        conn.execute("INSERT INTO crumbs(item_id,doc_id,sieve_run_id,criterion_id,document_side,statement) "
                     "VALUES ('CRUMB-DOC-0001-APP_B_I-0001','DOC-0001','RUN-20261001-02',"
                     "'APP_B_I','RULE','Synthetic rule statement')")
    return db


class EvidenceMatrixBundleTests(unittest.TestCase):
    def test_manifest_neutral_and_hash_locked(self) -> None:
        import bootstrap_evidence_matrix as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows], ["scripts/build_matrix.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_read_only_matrix_and_sibling_isolation(self) -> None:
        import bootstrap_evidence_matrix as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="evidence-matrix-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    sibling_before = snapshot(sibling) if with_sibling else None
                    state_bundle.apply(target, "state-first")
                    sieve_bundle.apply(target, "sieve-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 1)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "matrix-first")["created"]), 1)
                    self.assertEqual(len(bundle.apply(target, "matrix-retry")["preserved"]), 1)
                    output_json = target / "outputs/matrix.json"
                    output_md = target / "outputs/matrix.md"

                    def run(*extra: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/build_matrix.py"),
                             "--run-id", RUN, "--json", str(output_json),
                             "--markdown", str(output_md), *extra],
                            cwd=sibling if with_sibling else root,
                            env=os.environ | {"PYTHONUTF8": "1"},
                            capture_output=True, text=True, encoding="utf-8", timeout=30,
                        )

                    missing = run()
                    self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    self.assertFalse(output_json.exists())
                    db = seed(target)
                    db_before = (db.read_bytes(), db.stat().st_mtime_ns)
                    unscoped = subprocess.run(
                        [sys.executable, "-B", str(target / "scripts/build_matrix.py"),
                         "--json", str(output_json), "--markdown", str(output_md)],
                        cwd=sibling if with_sibling else root,
                        env=os.environ | {"PYTHONUTF8": "1"},
                        capture_output=True, text=True, encoding="utf-8", timeout=30,
                    )
                    self.assertEqual(unscoped.returncode, 1)
                    self.assertIn("run", unscoped.stderr.lower())
                    self.assertFalse(output_json.exists())
                    invalid = run("--run-id", "RUN-20261001-99")
                    self.assertEqual(invalid.returncode, 1)
                    self.assertFalse(output_json.exists())
                    foreign_db = run("--db", str(sibling / "foreign.sqlite"))
                    self.assertEqual(foreign_db.returncode, 1)
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    foreign = run("--json", str(sibling / "foreign.json"))
                    self.assertEqual(foreign.returncode, 1)
                    self.assertFalse((sibling / "foreign.json").exists())
                    passed = run()
                    self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
                    rows = json.loads(output_json.read_text(encoding="utf-8"))
                    self.assertEqual(len(rows), 18)
                    self.assertEqual(rows[0]["rule_evidence_count"], 1)
                    self.assertEqual(rows[0]["applicability"], "unruled")
                    self.assertEqual(output_md.read_text(encoding="utf-8").count("| APP_B_"), 18)
                    output_before = (output_json.read_bytes(), output_json.stat().st_mtime_ns,
                                     output_md.read_bytes(), output_md.stat().st_mtime_ns)
                    self.assertEqual(run().returncode, 0)
                    self.assertEqual((output_json.read_bytes(), output_json.stat().st_mtime_ns,
                                      output_md.read_bytes(), output_md.stat().st_mtime_ns), output_before)
                    output_md.write_text("conflict", encoding="utf-8")
                    self.assertEqual(run().returncode, 1)
                    self.assertEqual(output_json.read_bytes(), output_before[0])
                    self.assertEqual((db.read_bytes(), db.stat().st_mtime_ns), db_before)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, sibling_before)

    def test_conflicting_script_target_blocks_bundle(self) -> None:
        import bootstrap_evidence_matrix as bundle

        with tempfile.TemporaryDirectory(prefix="matrix-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/build_matrix.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "matrix-conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
