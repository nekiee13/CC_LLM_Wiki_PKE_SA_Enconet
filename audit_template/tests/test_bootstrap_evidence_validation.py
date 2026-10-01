"""Synthetic proof that evidence checks stay in one audit project."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_state as state_bundle  # noqa: E402
import bootstrap_sieving as sieving_bundle  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class EvidenceValidationBundleTests(unittest.TestCase):
    def test_manifest_hashes_and_exact_copy_set(self) -> None:
        import bootstrap_evidence_validation as bundle

        manifest = bundle.load_manifest()
        self.assertEqual([row["path"] for row in manifest["files"]], [
            "manifests/link_exceptions.csv", "schemas/page_types.yml",
            "schemas/required_fields.yml", "scripts/validate_frontmatter.py",
            "scripts/validate_traceability.py",
        ])
        for row in manifest["files"]:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_validate_only_local_synthetic_evidence(self) -> None:
        import bootstrap_evidence_validation as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="evidence-bundle-", dir=TEMPLATE / "tests") as temp:
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
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 5)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "evidence-first")["created"]), 5)
                    self.assertEqual(len(bundle.apply(target, "evidence-second")["preserved"]), 5)

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=sibling if with_sibling else root, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    missing = run("validate_traceability.py", "--no-record")
                    self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    for option, value in (("--db", sibling / "foreign.sqlite"),
                                          ("--exceptions", sibling / "foreign.csv")):
                        result = run("validate_traceability.py", option, str(value), "--no-record")
                        self.assertEqual(result.returncode, 1)
                        self.assertIn("local", result.stderr.lower())
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    foreign_wiki = run("validate_frontmatter.py", "--wiki", str(sibling), "--no-record")
                    self.assertEqual(foreign_wiki.returncode, 1)
                    self.assertIn("local", foreign_wiki.stderr.lower())

                    db = target / "db/nqa_audit.sqlite"
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.executescript(
                            "CREATE TABLE documents (doc_id TEXT, sha256 TEXT);"
                            "CREATE TABLE document_chunks (chunk_id TEXT, doc_id TEXT, "
                            "chunk_text TEXT, source_sha256 TEXT);"
                            "CREATE TABLE crumbs (item_id TEXT, doc_id TEXT);"
                            "CREATE TABLE crumb_quotes (item_id TEXT, quote_id TEXT, quote_original TEXT);"
                            "CREATE TABLE crumb_chunk_links (item_id TEXT, quote_id TEXT, chunk_id TEXT);"
                            "INSERT INTO documents VALUES ('DOC-0001', 'sha');"
                            "INSERT INTO document_chunks VALUES ('CHUNK-DOC-0001-0001', 'DOC-0001', 'alpha beta', 'sha');"
                            "INSERT INTO crumbs VALUES ('CRUMB-DOC-0001-APP_B_I-0001', 'DOC-0001');"
                            "INSERT INTO crumb_quotes VALUES ('CRUMB-DOC-0001-APP_B_I-0001', 'QUOTE-DOC-0001-0001-01', 'alpha beta');"
                        )
                    no_link = run("validate_traceability.py", "--no-record")
                    self.assertEqual(no_link.returncode, 1)
                    self.assertIn("without link", no_link.stderr)
                    exceptions = target / "manifests/link_exceptions.csv"
                    exceptions.write_text(
                        "crumb_id,quote_id,reason,approved_by,date\n"
                        "CRUMB-DOC-0001-APP_B_I-0001,QUOTE-DOC-0001-0001-01,missing,,2026-10-01\n",
                        encoding="utf-8",
                    )
                    incomplete = run("validate_traceability.py", "--no-record")
                    self.assertEqual(incomplete.returncode, 1)
                    self.assertIn("incomplete exception", incomplete.stderr)
                    exceptions.write_text("crumb_id,quote_id,reason,approved_by,date\n",
                                          encoding="utf-8")
                    no_log = run("validate_traceability.py")
                    self.assertEqual(no_log.returncode, 1)
                    self.assertIn("record could not be written", no_log.stderr)
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.execute("INSERT INTO crumb_chunk_links VALUES (?,?,?)",
                                     ("CRUMB-DOC-0001-APP_B_I-0001", "QUOTE-DOC-0001-0001-01",
                                      "CHUNK-DOC-0001-0001"))
                    linked = run("validate_traceability.py", "--no-record")
                    self.assertEqual(linked.returncode, 0, linked.stdout + linked.stderr)
                    self.assertFalse((target / "manifests/validation_runs.csv").exists())

                    wiki = target / "wiki"
                    for folder in ("criteria", "evidence", "findings", "actions", "gates"):
                        (wiki / folder).mkdir(parents=True)
                    empty_wiki = run("validate_frontmatter.py", "--no-record")
                    self.assertEqual(empty_wiki.returncode, 0, empty_wiki.stdout + empty_wiki.stderr)
                    page = wiki / "criteria/EVAL-APP_B_I.md"
                    page.write_text("bad page\n", encoding="utf-8")
                    bad_page = run("validate_frontmatter.py", "--no-record")
                    self.assertEqual(bad_page.returncode, 1)
                    self.assertIn("frontmatter missing", bad_page.stderr)
                    page.write_text(
                        "---\nid: EVAL-APP_B_I\ntype: criterion-evaluation\nstatus: draft\n"
                        "content_origin: human\nsource: synthetic\ncriterion_id: APP_B_I\n"
                        "applicability: applicable\nclassification: undetermined\n"
                        "evaluation_run: RUN-20261001-01\n---\nSynthetic body.\n", encoding="utf-8"
                    )
                    valid_page = run("validate_frontmatter.py", "--no-record")
                    self.assertEqual(valid_page.returncode, 0, valid_page.stdout + valid_page.stderr)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)
                    with self.assertRaises(bundle.BootstrapError):
                        bundle.apply(target, "evidence-after-ledger-edit")

    def test_existing_conflict_blocks_all_copy(self) -> None:
        import bootstrap_evidence_validation as bundle

        with tempfile.TemporaryDirectory(prefix="evidence-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/validate_traceability.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
