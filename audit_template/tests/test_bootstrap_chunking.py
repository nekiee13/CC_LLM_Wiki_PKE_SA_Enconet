"""Chunk one synthetic local document without replacing prior evidence."""
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

DOC = "DOC-0001"
TEXT = "# Intro\nAlpha text.\n## Check\nBeta text.\n"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def make_db(target: Path) -> Path:
    db = target / "db/nqa_audit.sqlite"
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
                     "VALUES (?,?,?,?,?,?,?)",
                     (DOC, "invented.txt", "Invented page", "Fake Supplier", "en",
                      "DOCUMENT", "0" * 64))
    return db


class ChunkingBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_chunking as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows], ["scripts/chunk_document.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_preview_apply_retry_and_foreign_db(self) -> None:
        import bootstrap_chunking as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="chunking-", dir=TEMPLATE / "tests") as temp:
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
                    self.assertEqual(len(bundle.apply(target, "chunk-first")["created"]), 1)
                    self.assertEqual(len(bundle.apply(target, "chunk-retry")["preserved"]), 1)

                    def run(*extra: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/chunk_document.py"),
                             DOC, *extra], cwd=sibling if with_sibling else root,
                            capture_output=True, text=True, encoding="utf-8", timeout=30)

                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    db = make_db(target)
                    derived = target / "derived" / f"{DOC}.txt"
                    derived.parent.mkdir(exist_ok=True)
                    derived.write_text(TEXT, encoding="utf-8", newline="")
                    before_db = db.read_bytes()
                    preview = run()
                    self.assertEqual(preview.returncode, 0, preview.stderr)
                    planned = json.loads(preview.stdout)
                    self.assertEqual(planned["chunk_count"], 2)
                    self.assertEqual(db.read_bytes(), before_db)
                    artifact = target / "derived/chunks" / f"{DOC}.json"
                    self.assertFalse(artifact.exists())
                    applied = run("--apply")
                    self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
                    report = json.loads(artifact.read_text(encoding="utf-8"))
                    self.assertEqual(report["mode"], "apply")
                    self.assertEqual(report["derived_text_sha256"], hashlib.sha256(TEXT.encode()).hexdigest())
                    self.assertEqual([row["chunk_id"] for row in report["chunks"]],
                                     ["CHUNK-DOC-0001-0001", "CHUNK-DOC-0001-0002"])
                    with closing(sqlite3.connect(db)) as conn:
                        rows = conn.execute("SELECT chunk_id,chunk_text,char_start,char_end "
                                            "FROM document_chunks ORDER BY chunk_id").fetchall()
                    self.assertEqual(len(rows), 2)
                    self.assertEqual(rows[0][1], TEXT[rows[0][2]:rows[0][3]])
                    self.assertEqual(rows[1][1], TEXT[rows[1][2]:rows[1][3]])
                    after_db, after_artifact = db.read_bytes(), artifact.read_bytes()
                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertEqual((db.read_bytes(), artifact.read_bytes()), (after_db, after_artifact))
                    self.assertEqual(run("--apply", "--db", str(sibling / "foreign.sqlite")).returncode, 1)
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_ambiguous_document_and_late_sql_failure_make_no_chunks(self) -> None:
        import bootstrap_chunking as bundle

        with tempfile.TemporaryDirectory(prefix="chunking-failure-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "Invented Audit"
            target.mkdir()
            state_bundle.apply(target, "state-first")
            bundle.apply(target, "chunk-first")
            db = make_db(target)
            derived = target / "derived" / f"{DOC}.txt"
            derived.parent.mkdir(exist_ok=True)
            artifact = target / "derived/chunks" / f"{DOC}.json"

            def run() -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    [sys.executable, "-B", str(target / "scripts/chunk_document.py"), DOC,
                     "--apply"], cwd=target, capture_output=True, text=True,
                    encoding="utf-8", timeout=30)

            derived.write_text("No headings here.\n", encoding="utf-8", newline="")
            self.assertEqual(run().returncode, 1)
            self.assertFalse(artifact.exists())
            derived.write_text(TEXT, encoding="utf-8", newline="")
            with closing(sqlite3.connect(db)) as conn, conn:
                conn.execute("CREATE TRIGGER block_second_chunk BEFORE INSERT ON document_chunks "
                             "WHEN NEW.chunk_id='CHUNK-DOC-0001-0002' "
                             "BEGIN SELECT RAISE(ABORT,'synthetic stop'); END")
            self.assertEqual(run().returncode, 1)
            self.assertFalse(artifact.exists())
            with closing(sqlite3.connect(db)) as conn:
                self.assertEqual(conn.execute("SELECT count(*) FROM document_chunks").fetchone()[0], 0)

    def test_conflicting_target_blocks_copy(self) -> None:
        import bootstrap_chunking as bundle

        with tempfile.TemporaryDirectory(prefix="chunking-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/chunk_document.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
