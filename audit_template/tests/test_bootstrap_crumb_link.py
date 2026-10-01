"""Quote linking changes only the selected synthetic run and local project."""
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
import bootstrap_state as state_bundle  # noqa: E402

RUN = "RUN-20261001-02"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def seed(target: Path) -> Path:
    db = target / "db/nqa_audit.sqlite"
    sha = "0" * 64
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.execute("INSERT INTO criteria VALUES ('APP_B_I','Organization','synthetic')")
        for doc, file in (("DOC-0001", "old.txt"), ("DOC-0002", "new.txt")):
            conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
                         "VALUES (?,?,?,?,?,?,?)", (doc, file, file, "Fake Supplier", "en", "DOCUMENT", sha if doc == "DOC-0001" else "1" * 64))
        for run, doc in (("RUN-20261001-01", "DOC-0001"), (RUN, "DOC-0002")):
            conn.execute("INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side,completed_at) "
                         "VALUES (?,?,?,'DOCUMENT','2026-10-01')", (run, doc, "synthetic"))
        for item, doc, run in (("CRUMB-DOC-0001-APP_B_I-0001", "DOC-0001", "RUN-20261001-01"),
                               ("CRUMB-DOC-0002-APP_B_I-0001", "DOC-0002", RUN)):
            conn.execute("INSERT INTO crumbs(item_id,doc_id,sieve_run_id,criterion_id,document_side,statement) "
                         "VALUES (?,?,?,'APP_B_I','DOCUMENT','Invented claim')", (item, doc, run))
        old_item = "CRUMB-DOC-0001-APP_B_I-0001"
        new_item = "CRUMB-DOC-0002-APP_B_I-0001"
        for quote, item, words in (("Q-OLD", old_item, "Old quote"),
                                   ("Q-EXACT", new_item, "Exact quote"),
                                   ("Q-NORM", new_item, "Mixed   CASE"),
                                   ("Q-MISSING", new_item, "Absent words")):
            conn.execute("INSERT INTO crumb_quotes VALUES (?,?,?,'en','section 1')", (quote, item, words))
        for chunk, doc, words, source, start in (("C-OLD", "DOC-0001", "Old quote", sha, 0),
                                                 ("C-EXACT", "DOC-0002", "Exact quote within text", "1" * 64, 0),
                                                 ("C-NORM", "DOC-0002", "mixed case in text", "1" * 64, 100)):
            conn.execute("INSERT INTO document_chunks VALUES (?,?,?,?,?,?,?)",
                         (chunk, doc, "section 1", words, start, start + 100, source))
        conn.execute("INSERT INTO crumb_chunk_links VALUES (?,?,?,'EXACT',1.0)",
                     (old_item, "Q-OLD", "C-OLD"))
    return db


class CrumbLinkBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_crumb_link as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows], ["scripts/link_crumbs.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_preview_apply_retry_and_conflict(self) -> None:
        import bootstrap_crumb_link as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="crumb-link-", dir=TEMPLATE / "tests") as temp:
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
                    self.assertEqual(len(bundle.preview(target)["files"]), 1)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "link-first")["created"]), 1)
                    self.assertEqual(len(bundle.apply(target, "link-retry")["preserved"]), 1)

                    def run(*args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/link_crumbs.py"),
                             "--run-id", RUN, *args], cwd=sibling if with_sibling else root,
                            capture_output=True, text=True, encoding="utf-8", timeout=30)

                    self.assertEqual(run("--apply").returncode, 1)  # Missing DB is not created.
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    db = seed(target)
                    before_db = db.read_bytes()
                    preview = run()
                    self.assertEqual(preview.returncode, 0, preview.stderr)
                    self.assertEqual(db.read_bytes(), before_db)
                    plan = json.loads(preview.stdout)
                    self.assertEqual((plan["links_to_add"], len(plan["unmatched"])), (2, 1))
                    self.assertEqual(plan["unmatched"][0]["quote_id"], "Q-MISSING")
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("CREATE TRIGGER block_second_link BEFORE INSERT ON crumb_chunk_links "
                                     "WHEN NEW.quote_id='Q-NORM' BEGIN SELECT RAISE(ABORT,'synthetic stop'); END")
                    self.assertEqual(run("--apply").returncode, 1)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        self.assertEqual(conn.execute("SELECT count(*) FROM crumb_chunk_links").fetchone()[0], 1)
                        conn.execute("DROP TRIGGER block_second_link")
                    applied = run("--apply")
                    self.assertEqual(applied.returncode, 2, applied.stderr)  # Partial, not verified.
                    with closing(sqlite3.connect(db)) as conn:
                        rows = conn.execute("SELECT quote_id,chunk_id,link_method FROM crumb_chunk_links "
                                            "ORDER BY quote_id").fetchall()
                    self.assertEqual(rows, [("Q-EXACT", "C-EXACT", "EXACT"),
                                            ("Q-NORM", "C-NORM", "NORMALIZED"),
                                            ("Q-OLD", "C-OLD", "EXACT")])
                    retry_db = db.read_bytes()
                    self.assertEqual(run("--apply").returncode, 2)
                    self.assertEqual(db.read_bytes(), retry_db)
                    foreign = run("--apply", "--db", str(sibling / "foreign.sqlite"))
                    self.assertEqual(foreign.returncode, 1)
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("UPDATE crumb_chunk_links SET link_method='MANUAL' "
                                     "WHERE quote_id='Q-EXACT'")
                    tampered = db.read_bytes()
                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertEqual(db.read_bytes(), tampered)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("UPDATE crumb_chunk_links SET link_method='EXACT' "
                                     "WHERE quote_id='Q-EXACT'")
                        conn.execute("INSERT INTO document_chunks VALUES "
                                     "('C-MISSING','DOC-0002','section 1','Absent words',200,300,?)",
                                     ("1" * 64,))
                    metrics_dir = target / "sieving/runs" / RUN
                    metrics_dir.mkdir(parents=True)
                    (metrics_dir / "metrics.json").write_text("{}", encoding="utf-8")
                    before_stale = db.read_bytes()
                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertEqual(db.read_bytes(), before_stale)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_conflict_blocks_copy(self) -> None:
        import bootstrap_crumb_link as bundle

        with tempfile.TemporaryDirectory(prefix="crumb-link-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/link_crumbs.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
