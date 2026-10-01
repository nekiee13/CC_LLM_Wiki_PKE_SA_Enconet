"""Plain-text extraction accepts only one registered local raw source."""
from __future__ import annotations

from contextlib import closing
import csv
import hashlib
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_state as state_bundle  # noqa: E402
import bootstrap_source_validation as source_bundle  # noqa: E402

DOC = "DOC-0001"
BODY = b"# Invented QA rule\nA made-up sentence.\n"
HEADER = ["doc_id", "filename", "title", "supplier", "doc_date", "language",
          "side_hint", "sha256", "promoted_utc", "source_url", "notes"]


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def setup_registered_source(target: Path, *, suffix: str = ".txt") -> tuple[Path, Path]:
    raw = target / "raw" / f"invented{suffix}"
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_bytes(BODY)
    raw.chmod(raw.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    sha = hashlib.sha256(BODY).hexdigest()
    manifest = target / "manifests/raw_sources.csv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER)
        writer.writeheader()
        writer.writerow({"doc_id": DOC, "filename": raw.name, "title": "Invented",
                         "supplier": "Fake Supplier", "doc_date": "n-a", "language": "en",
                         "side_hint": "DOCUMENT", "sha256": sha,
                         "promoted_utc": "2026-10-01T00:00:00Z", "source_url": "n-a", "notes": ""})
    db = target / "db/nqa_audit.sqlite"
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256,promoted_utc) "
                     "VALUES (?,?,?,?,?,?,?,?)", (DOC, raw.name, "Invented", "Fake Supplier",
                     "en", "DOCUMENT", sha, "2026-10-01T00:00:00Z"))
    return db, raw


class TextExtractionBundleTests(unittest.TestCase):
    def test_manifest_neutral_and_hash_locked(self) -> None:
        import bootstrap_text_extraction as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows], ["scripts/extract_text.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_preview_apply_retry_and_sibling_isolation(self) -> None:
        import bootstrap_text_extraction as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="text-extract-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    sibling_before = snapshot(sibling) if with_sibling else None
                    state_bundle.apply(target, "state-first")
                    source_bundle.apply(target, "source-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 1)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "extract-first")["created"]), 1)
                    self.assertEqual(len(bundle.apply(target, "extract-retry")["preserved"]), 1)

                    def run(*extra: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/extract_text.py"),
                             DOC, *extra], cwd=sibling if with_sibling else root,
                            capture_output=True, text=True, encoding="utf-8", timeout=30)

                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    db, raw = setup_registered_source(target)
                    original_raw = raw.read_bytes()
                    before_db = db.read_bytes()
                    preview = run()
                    self.assertEqual(preview.returncode, 0, preview.stderr)
                    self.assertEqual(db.read_bytes(), before_db)
                    derived = target / "derived" / f"{DOC}.txt"
                    self.assertFalse(derived.exists())
                    applied = run("--apply")
                    self.assertEqual(applied.returncode, 0, applied.stderr)
                    self.assertEqual(derived.read_bytes(), BODY)
                    self.assertEqual(raw.read_bytes(), original_raw)
                    with closing(sqlite3.connect(db)) as conn:
                        row = conn.execute("SELECT extraction_method,extracted_at FROM documents "
                                           "WHERE doc_id=?", (DOC,)).fetchone()
                        self.assertEqual(row[0], "utf-8-text:txt")
                        self.assertIsNotNone(row[1])
                    after_db, after_derived = db.read_bytes(), derived.read_bytes()
                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertEqual((db.read_bytes(), derived.read_bytes()),
                                     (after_db, after_derived))
                    self.assertEqual(run("--apply", "--db", str(sibling / "foreign.sqlite")).returncode, 1)
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    self.assertEqual(snapshot(sibling) if with_sibling else None, sibling_before)

    def test_checksum_type_and_late_sql_failure_create_no_output(self) -> None:
        import bootstrap_text_extraction as bundle

        with tempfile.TemporaryDirectory(prefix="text-extract-fail-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "Invented Audit"
            target.mkdir()
            state_bundle.apply(target, "state-first")
            source_bundle.apply(target, "source-first")
            bundle.apply(target, "extract-first")
            db, raw = setup_registered_source(target)
            derived = target / "derived" / f"{DOC}.txt"

            def run() -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    [sys.executable, "-B", str(target / "scripts/extract_text.py"), DOC,
                     "--apply"], cwd=target, capture_output=True, text=True,
                    encoding="utf-8", timeout=30)

            raw.chmod(raw.stat().st_mode | stat.S_IWUSR)
            raw.write_bytes(b"tampered")
            raw.chmod(raw.stat().st_mode & ~stat.S_IWUSR)
            self.assertEqual(run().returncode, 1)
            self.assertFalse(derived.exists())
            raw.chmod(raw.stat().st_mode | stat.S_IWUSR)
            raw.write_bytes(BODY)
            raw.chmod(raw.stat().st_mode & ~stat.S_IWUSR)
            with closing(sqlite3.connect(db)) as conn, conn:
                conn.execute("CREATE TRIGGER block_extraction BEFORE UPDATE ON documents "
                             "BEGIN SELECT RAISE(ABORT,'synthetic stop'); END")
            self.assertEqual(run().returncode, 1)
            self.assertFalse(derived.exists())
            with closing(sqlite3.connect(db)) as conn:
                self.assertIsNone(conn.execute("SELECT extracted_at FROM documents").fetchone()[0])

        with tempfile.TemporaryDirectory(prefix="text-extract-type-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "Invented Audit"
            target.mkdir()
            state_bundle.apply(target, "state-first")
            source_bundle.apply(target, "source-first")
            bundle.apply(target, "extract-first")
            setup_registered_source(target, suffix=".pdf")
            result = subprocess.run(
                [sys.executable, "-B", str(target / "scripts/extract_text.py"), DOC, "--apply"],
                cwd=target, capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported extraction type", result.stderr)
            self.assertFalse((target / "derived" / f"{DOC}.txt").exists())

    def test_conflicting_target_blocks_copy(self) -> None:
        import bootstrap_text_extraction as bundle

        with tempfile.TemporaryDirectory(prefix="text-extract-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/extract_text.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
