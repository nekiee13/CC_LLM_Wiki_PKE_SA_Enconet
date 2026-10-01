"""Strict crumb import is local, transactional, and never reads a sibling."""
from __future__ import annotations

from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_phase_validation as phase_bundle  # noqa: E402
import bootstrap_sieving as sieving_bundle  # noqa: E402
import bootstrap_state as state_bundle  # noqa: E402

RUN_ID = "RUN-20261001-01"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def payload() -> dict:
    return {
        "document": {"doc_id": "DOC-0001", "name": "Invented QA page",
                     "date": "2026-01-01", "document_side": "DOCUMENT",
                     "authority_references": []},
        "items": [{"item_id": "I-1", "criterion_id": "APP_B_I",
                   "criterion_name": "Organization", "statement": "Invented claim",
                   "item_type": "control", "entities": {},
                   "sources": [{"source_locator": "section 1"}],
                   "evidence_quotes": [{"quote_original": "Invented exact quote",
                                        "quote_language": "en"}]}],
    }


def make_db(target: Path) -> Path:
    db = target / "db/nqa_audit.sqlite"
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.execute("INSERT INTO criteria VALUES ('APP_B_I','Organization','synthetic')")
        conn.execute(
            "INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
            "VALUES (?,?,?,?,?,?,?)",
            ("DOC-0001", "invented.txt", "Invented QA page", "Fake Supplier", "en",
             "DOCUMENT", "0" * 64),
        )
        conn.execute(
            "INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side,source_rule) "
            "VALUES (?,?,?,?,?)", (RUN_ID, "DOC-0001", "candidate_v1", "DOCUMENT", None),
        )
    return db


class CrumbImportBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_crumb_import as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows], ["scripts/import_crumbs.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_strict_transaction_and_retry(self) -> None:
        import bootstrap_crumb_import as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="crumb-import-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    state_bundle.apply(target, "state-first")
                    sieving_bundle.apply(target, "sieving-first")
                    phase_bundle.apply(target, "phase-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 1)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "import-first")["created"]), 1)
                    self.assertEqual(len(bundle.apply(target, "import-retry")["preserved"]), 1)
                    document = target / "sieving/synthetic.json"
                    document.write_text(json.dumps(payload()), encoding="utf-8")

                    def run(*extra: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/import_crumbs.py"),
                             str(document), "--run-id", RUN_ID, *extra],
                            cwd=sibling if with_sibling else root, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    missing = run()
                    self.assertEqual(missing.returncode, 1)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    db = make_db(target)
                    bad = payload()
                    del bad["items"][0]["item_type"]
                    document.write_text(json.dumps(bad), encoding="utf-8")
                    before_db = db.read_bytes()
                    rejected = run()
                    self.assertEqual(rejected.returncode, 1)
                    self.assertIn("strict warning", rejected.stderr)
                    self.assertEqual(db.read_bytes(), before_db)
                    late_failure = payload()
                    second = dict(late_failure["items"][0])
                    second.update(item_id="I-2", criterion_id="APP_B_II",
                                  criterion_name="Quality Assurance Program")
                    late_failure["items"].append(second)
                    document.write_text(json.dumps(late_failure), encoding="utf-8")
                    failed_insert = run()
                    self.assertEqual(failed_insert.returncode, 1)
                    with closing(sqlite3.connect(db)) as conn:
                        self.assertEqual(conn.execute("SELECT count(*) FROM crumbs").fetchone()[0], 0)
                        self.assertIsNone(conn.execute(
                            "SELECT completed_at FROM sieve_runs WHERE run_id=?", (RUN_ID,)
                        ).fetchone()[0])
                    document.write_text(json.dumps(payload()), encoding="utf-8")
                    good = run()
                    self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
                    with closing(sqlite3.connect(db)) as conn:
                        self.assertEqual(conn.execute("SELECT count(*) FROM crumbs").fetchone()[0], 1)
                        self.assertEqual(conn.execute("SELECT quote_original FROM crumb_quotes").fetchone()[0],
                                         "Invented exact quote")
                        self.assertIsNotNone(conn.execute(
                            "SELECT completed_at FROM sieve_runs WHERE run_id=?", (RUN_ID,)
                        ).fetchone()[0])
                    self.assertEqual(run().returncode, 1)
                    foreign = run("--db", str(sibling / "foreign.sqlite"))
                    self.assertEqual(foreign.returncode, 1)
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_conflict_blocks_copy(self) -> None:
        import bootstrap_crumb_import as bundle

        with tempfile.TemporaryDirectory(prefix="crumb-import-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/import_crumbs.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
