"""Metrics and diffs use only local synthetic sieve generations."""
from __future__ import annotations

import hashlib
import json
from contextlib import closing
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_state as state_bundle  # noqa: E402

OLD = "RUN-20261001-01"
NEW = "RUN-20261001-02"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def make_db(path: Path) -> None:
    with closing(sqlite3.connect(path)) as conn, conn:
        conn.executescript(
            "CREATE TABLE criteria (criterion_id TEXT);"
            "CREATE TABLE sieve_runs (run_id TEXT, doc_id TEXT, generation INTEGER, "
            "prompt_version TEXT, status TEXT, supersedes_run_id TEXT, "
            "completed_at TEXT, rejected_item_count INTEGER, failed_item_count INTEGER);"
            "CREATE TABLE crumbs (item_id TEXT, sieve_run_id TEXT, criterion_id TEXT, "
            "statement TEXT, item_type TEXT, quote_language TEXT);"
            "CREATE TABLE crumb_sources (item_id TEXT);"
            "CREATE TABLE crumb_quotes (item_id TEXT, quote_id TEXT, quote_original TEXT);"
            "CREATE TABLE crumb_chunk_links (item_id TEXT, quote_id TEXT);"
            "INSERT INTO criteria VALUES ('APP_B_I'),('APP_B_II');"
            "INSERT INTO sieve_runs VALUES ('RUN-20261001-01','DOC-0001',1,'old','superseded',NULL,"
            "'2026-10-01',0,0);"
            "INSERT INTO sieve_runs VALUES ('RUN-20261001-02','DOC-0001',2,'new','candidate',"
            "'RUN-20261001-01','2026-10-01',1,0);"
            "INSERT INTO crumbs VALUES ('OLD1','RUN-20261001-01','APP_B_I','Repeat','control','en');"
            "INSERT INTO crumbs VALUES ('OLD2','RUN-20261001-01','APP_B_I','Repeat','control','en');"
            "INSERT INTO crumbs VALUES ('OLD3','RUN-20261001-01','APP_B_I','Old claim','control','en');"
            "INSERT INTO crumbs VALUES ('NEW1','RUN-20261001-02','APP_B_I','Repeat','control','en');"
            "INSERT INTO crumbs VALUES ('NEW3','RUN-20261001-02','APP_B_I','New claim','control','en');"
            "INSERT INTO crumb_quotes VALUES ('OLD1','Q1','Same quote');"
            "INSERT INTO crumb_quotes VALUES ('OLD2','Q2','Same quote');"
            "INSERT INTO crumb_quotes VALUES ('OLD3','Q3','Change quote');"
            "INSERT INTO crumb_quotes VALUES ('NEW1','Q4','Same quote');"
            "INSERT INTO crumb_quotes VALUES ('NEW3','Q5','Change quote');"
            "INSERT INTO crumb_sources VALUES ('NEW1'),('NEW3');"
            "INSERT INTO crumb_chunk_links VALUES ('NEW1','Q4'),('NEW3','Q5');"
        )


class AnalysisBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_sieving_analysis as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows],
                         ["scripts/sieve_diff.py", "scripts/sieve_metrics.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_read_only_db_and_duplicate_preserving_diff(self) -> None:
        import bootstrap_sieving_analysis as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="analysis-bundle-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    state_bundle.apply(target, "state-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 2)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "analysis-first")["created"]), 2)
                    self.assertEqual(len(bundle.apply(target, "analysis-retry")["preserved"]), 2)

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=sibling if with_sibling else root, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    missing = run("sieve_metrics.py", "--run-id", NEW)
                    self.assertEqual(missing.returncode, 1)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    db = target / "db/nqa_audit.sqlite"
                    make_db(db)
                    db_before = db.read_bytes()
                    metrics = run("sieve_metrics.py", "--run-id", NEW)
                    self.assertEqual(metrics.returncode, 0, metrics.stdout + metrics.stderr)
                    result = json.loads((target / "sieving/runs" / NEW / "metrics.json").read_text(encoding="utf-8"))
                    self.assertEqual(result["crumb_count"], 2)
                    self.assertEqual(result["zero_crumb_criteria"], ["APP_B_II"])
                    self.assertEqual(result["quote_verification"]["rate_percent"], 100.0)
                    self.assertEqual(result["previous_generation"]["crumb_delta"], -1)
                    self.assertEqual(run("sieve_metrics.py", "--run-id", NEW).returncode, 1)
                    diff = run("sieve_diff.py", OLD, NEW, "--output-dir", f"sieving/runs/{NEW}")
                    self.assertEqual(diff.returncode, 0, diff.stdout + diff.stderr)
                    data = json.loads((target / "sieving/runs" / NEW /
                                       f"diff-{OLD}-to-{NEW}.json").read_text(encoding="utf-8"))
                    changes = data["criteria"]["APP_B_I"]
                    self.assertEqual(len(changes["added"]), 0)
                    self.assertEqual(len(changes["removed"]), 1)
                    self.assertEqual(len(changes["changed"]), 1)
                    self.assertEqual(run("sieve_diff.py", OLD, NEW,
                                         "--output-dir", f"sieving/runs/{NEW}").returncode, 1)
                    foreign = run("sieve_diff.py", OLD, NEW, "--output-dir", str(sibling))
                    self.assertEqual(foreign.returncode, 1)
                    self.assertEqual(db.read_bytes(), db_before)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_conflicting_target_blocks_copy(self) -> None:
        import bootstrap_sieving_analysis as bundle

        with tempfile.TemporaryDirectory(prefix="analysis-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/sieve_diff.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
