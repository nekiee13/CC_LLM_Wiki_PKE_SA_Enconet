"""Synthetic proof that fresh database and state tools stay project-local."""
from __future__ import annotations

import hashlib
from contextlib import closing
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import yaml


TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_state as state  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class StateBundleTests(unittest.TestCase):
    def test_criterion_scoped_ids_have_neutral_shape_only(self) -> None:
        contract = yaml.safe_load(
            (state.BUNDLE / "schemas/id_patterns.yml").read_text(encoding="utf-8")
        )
        cases = {
            "crumb_id": ("CRUMB-DOC-0001-AREA_2-0001", "CRUMB-DOC-0001-APP_B_IV-0001"),
            "requirement_id": ("REQ-AREA_2-01", "REQ-APP_B_IV-01"),
            "evaluation_id": ("EVAL-AREA_2", "EVAL-APP_B_IV"),
            "gap_id": ("GAP-AREA_2-01", "GAP-APP_B_IV-01"),
        }
        for name, valid in cases.items():
            pattern = re.compile(contract["patterns"][name]["regex"])
            for candidate in valid:
                self.assertIsNotNone(pattern.fullmatch(candidate), (name, candidate))
            for candidate in (valid[0].replace("AREA_2", "area_2"),
                              valid[0].replace("AREA_2", "AREA__2"),
                              valid[0].replace("AREA_2", "AREA/2")):
                self.assertIsNone(pattern.fullmatch(candidate), (name, candidate))
        self.assertNotIn("APP_B", (state.BUNDLE / "schemas/id_patterns.yml").read_text(encoding="utf-8"))

    def test_manifest_is_source_free_and_hash_locked(self) -> None:
        manifest = state.load_manifest()
        self.assertEqual(manifest["template_version"], "1.0.0")
        self.assertEqual(manifest["scope"], "database-and-state-runtime")
        self.assertEqual({row["path"] for row in manifest["files"]}, {
            "db/schema.sql", "schemas/id_patterns.yml", "schemas/vocabularies.yml",
            "scripts/project_paths.py", "scripts/db_util.py", "scripts/init_db.py",
            "scripts/audit_state.py",
        })
        for row in manifest["files"]:
            data = (state.BUNDLE / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
            self.assertNotIn(b"Ekonerg", data)
        vocab = (state.BUNDLE / "schemas/vocabularies.yml").read_text(encoding="utf-8")
        self.assertIn("source_rules:\n", vocab)
        self.assertIn("authority_sources:\n", vocab)
        self.assertEqual(vocab.count("values: []"), 2)

    def test_two_companies_init_empty_db_and_keep_sibling(self) -> None:
        for company, with_sibling in (("Čista Tvrtka", True), ("Žuti Pogon", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="state-bundle-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    caller = sibling if with_sibling else root / "unrelated caller"
                    caller.mkdir()
                    if with_sibling:
                        (sibling / "marker.txt").write_text("unchanged", encoding="utf-8")
                        sibling_before = snapshot(sibling)
                    before = snapshot(target)
                    plan = state.preview(target)
                    self.assertEqual(snapshot(target), before)
                    self.assertTrue(all(row["state"] == "create" for row in plan["files"]))
                    first = state.apply(target, "state-first")
                    self.assertEqual(len(first["created"]), 7)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=caller, capture_output=True, text=True, encoding="utf-8", timeout=30,
                        )

                    initialized = run("init_db.py")
                    self.assertEqual(initialized.returncode, 0, initialized.stdout + initialized.stderr)
                    database = target / "db/nqa_audit.sqlite"
                    self.assertTrue(database.is_file())
                    with closing(sqlite3.connect(database)) as conn:
                        tables = {row[0] for row in conn.execute(
                            "SELECT name FROM sqlite_master WHERE type='table'")}
                        self.assertIn("approved_sources", tables)
                        self.assertIn("documents", tables)
                        self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 1)
                        self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                        for table in ("approved_sources", "documents", "criteria", "sieve_runs"):
                            self.assertEqual(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0], 0)
                    db_before = (database.read_bytes(), database.stat().st_mtime_ns)
                    repeat = run("init_db.py")
                    self.assertEqual(repeat.returncode, 0, repeat.stdout + repeat.stderr)
                    self.assertEqual((database.read_bytes(), database.stat().st_mtime_ns), db_before)
                    absent_state = run("audit_state.py", "--status")
                    self.assertEqual(absent_state.returncode, 1)
                    self.assertFalse((target / "project-state.yml").exists())

                    foreign_db = sibling / "foreign.sqlite"
                    rejected = run("init_db.py", "--db", str(foreign_db))
                    self.assertEqual(rejected.returncode, 1)
                    self.assertFalse(foreign_db.exists())
                    second = state.apply(target, "state-second")
                    self.assertEqual(second["created"], [])
                    self.assertEqual(len(second["preserved"]), 7)
                    self.assertEqual((database.read_bytes(), database.stat().st_mtime_ns), db_before)
                    if with_sibling:
                        self.assertEqual(snapshot(sibling), sibling_before)
                    else:
                        self.assertFalse(sibling.exists())

    def test_existing_conflict_stops_copy_before_writes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="state-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            target.mkdir()
            (target / "db").mkdir()
            (target / "db/schema.sql").write_bytes(b"owner schema")
            before = snapshot(target)
            with self.assertRaises(state.BootstrapError):
                state.preview(target)
            with self.assertRaises(state.BootstrapError):
                state.apply(target, "state-conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
