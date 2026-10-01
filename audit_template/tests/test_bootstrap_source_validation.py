"""Source and chunk checks are local, read-only, and fail closed."""
from __future__ import annotations

import csv
import hashlib
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


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class SourceValidationBundleTests(unittest.TestCase):
    def test_manifest_is_pinned_and_has_only_three_local_scripts(self) -> None:
        import bootstrap_source_validation as bundle

        manifest = bundle.load_manifest()
        self.assertEqual([row["path"] for row in manifest["files"]], [
            "scripts/source_registry.py", "scripts/validate_chunks.py",
            "scripts/validate_raw_sources.py",
        ])
        for row in manifest["files"]:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_synthetic_audits_and_no_sibling_changes(self) -> None:
        import bootstrap_source_validation as bundle

        for name, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix="source-validators-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / name
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    state_bundle.apply(target, "state-first")
                    before = snapshot(target)
                    preview = bundle.preview(target)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(preview["files"]), 3)
                    applied = bundle.apply(target, "source-first")
                    self.assertEqual(len(applied["created"]), 3)

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=sibling if with_sibling else root, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    for script in ("validate_raw_sources.py", "validate_chunks.py"):
                        args = ("--no-record",) if script == "validate_chunks.py" else ()
                        missing = run(script, *args)
                        self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
                        self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                        foreign = run(script, "--db", str(sibling / "foreign.sqlite"), *args)
                        self.assertEqual(foreign.returncode, 1, foreign.stdout + foreign.stderr)
                        self.assertIn("local", foreign.stderr.lower())
                        self.assertFalse((sibling / "foreign.sqlite").exists())

                    db = target / "db/nqa_audit.sqlite"
                    db.parent.mkdir(exist_ok=True)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.executescript(
                            "CREATE TABLE documents (doc_id TEXT, filename TEXT, title TEXT, "
                            "supplier TEXT, doc_date TEXT, language TEXT, document_side TEXT, "
                            "sha256 TEXT, promoted_utc TEXT, source_url TEXT, notes TEXT);"
                            "CREATE TABLE document_chunks (chunk_id TEXT, doc_id TEXT, "
                            "source_sha256 TEXT, chunk_text TEXT, char_start INTEGER, char_end INTEGER);"
                        )
                    raw = target / "raw"
                    derived = target / "derived"
                    manifest = target / "manifests/raw_sources.csv"
                    raw.mkdir()
                    derived.mkdir()
                    manifest.parent.mkdir()
                    header = ["doc_id", "filename", "title", "supplier", "doc_date", "language",
                              "side_hint", "sha256", "promoted_utc", "source_url", "notes"]
                    with manifest.open("w", newline="", encoding="utf-8") as handle:
                        csv.writer(handle).writerow(header)
                    self.assertEqual(run("validate_raw_sources.py").returncode, 1)
                    self.assertEqual(run("validate_chunks.py", "--no-record").returncode, 1)

                    source = raw / "sample.txt"
                    source.write_text("hello world", encoding="utf-8")
                    source.chmod(0o444)
                    checksum = hashlib.sha256(source.read_bytes()).hexdigest()
                    fields = ["DOC-0001", "sample.txt", "Sample", "Synthetic", "n-a", "en", "RULE",
                              checksum, "2026-10-01T00:00:00Z", "n-a", ""]
                    with manifest.open("a", newline="", encoding="utf-8") as handle:
                        csv.writer(handle).writerow(fields)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                                     ("DOC-0001", "sample.txt", "Sample", "Synthetic", None, "en",
                                      "RULE", checksum, "2026-10-01T00:00:00Z", "n-a", ""))
                        conn.execute("INSERT INTO document_chunks VALUES (?,?,?,?,?,?)",
                                     ("CHUNK-DOC-0001-0001", "DOC-0001", checksum, "hello", 0, 5))
                    (derived / "DOC-0001.txt").write_text("hello world", encoding="utf-8")
                    self.assertEqual(run("validate_raw_sources.py").returncode, 0)
                    self.assertEqual(run("validate_chunks.py", "--no-record").returncode, 0)
                    self.assertFalse((target / "manifests/validation_runs.csv").exists())
                    no_log = run("validate_chunks.py")
                    self.assertEqual(no_log.returncode, 1, no_log.stdout + no_log.stderr)
                    self.assertIn("record could not be written", no_log.stderr)
                    (derived / "DOC-0001.txt").write_text("wrong", encoding="utf-8")
                    self.assertIn("offset slice mismatch", run("validate_chunks.py", "--no-record").stderr)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)
                    self.assertEqual(len(bundle.apply(target, "source-second")["preserved"]), 3)

    def test_conflict_blocks_entire_copy(self) -> None:
        import bootstrap_source_validation as bundle

        with tempfile.TemporaryDirectory(prefix="source-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/validate_chunks.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
