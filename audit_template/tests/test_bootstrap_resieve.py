"""A measured resieve leaves the older run active and every write local."""
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
import bootstrap_crumb_import as import_bundle  # noqa: E402
import bootstrap_crumb_link as link_bundle  # noqa: E402
import bootstrap_phase_validation as phase_bundle  # noqa: E402
import bootstrap_sieving as sieving_bundle  # noqa: E402
import bootstrap_sieving_analysis as analysis_bundle  # noqa: E402
import bootstrap_state as state_bundle  # noqa: E402

OLD = "RUN-20261001-01"
NEW = "RUN-20261001-02"


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def make_db(target: Path, *, include_old: bool = True) -> Path:
    db = target / "db/nqa_audit.sqlite"
    with closing(sqlite3.connect(db)) as conn, conn:
        conn.executescript((target / "db/schema.sql").read_text(encoding="utf-8"))
        conn.execute("INSERT INTO criteria VALUES ('APP_B_I','Organization','synthetic')")
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
                     "VALUES ('DOC-0001','invented.txt','Invented','Fake Supplier','en','DOCUMENT',?)",
                     ("0" * 64,))
        conn.execute("INSERT INTO document_chunks VALUES "
                     "('CHUNK-DOC-0001-0001','DOC-0001','section 1','Old quote and New quote',0,100,?)",
                     ("0" * 64,))
        if include_old:
            conn.execute("INSERT INTO sieve_runs(run_id,doc_id,prompt_version,document_side,completed_at) "
                         "VALUES (?,?,?,'DOCUMENT','2026-10-01')", (OLD, "DOC-0001", "appb_document_v1"))
            conn.execute("INSERT INTO crumbs(item_id,doc_id,sieve_run_id,criterion_id,document_side,statement,item_type,quote_language) "
                         "VALUES ('CRUMB-DOC-0001-APP_B_I-0001','DOC-0001',?,'APP_B_I','DOCUMENT','Old claim','control','en')",
                         (OLD,))
            conn.execute("INSERT INTO crumb_quotes VALUES "
                         "('QUOTE-DOC-0001-0001-01','CRUMB-DOC-0001-APP_B_I-0001','Old quote','en','section 1')")
    return db


def payload() -> dict:
    return {"document": {"doc_id": "DOC-0001", "name": "Invented",
                         "date": "2026-01-01", "document_side": "DOCUMENT",
                         "authority_references": []},
            "items": [{"item_id": "I-1", "criterion_id": "APP_B_I",
                       "criterion_name": "Organization", "statement": "New claim",
                       "item_type": "control", "entities": {},
                       "sources": [{"source_locator": "section 1"}],
                       "evidence_quotes": [{"quote_original": "New quote", "quote_language": "en"}]}]}


class ResieveBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_resieve as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows],
                         ["scripts/resieve_run.py", "scripts/sieve_run.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_preflight_apply_and_retry(self) -> None:
        import bootstrap_resieve as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="resieve-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    for module, run_id in ((state_bundle, "state-first"),
                                           (sieving_bundle, "sieving-first"),
                                           (phase_bundle, "phase-first"),
                                           (analysis_bundle, "analysis-first"),
                                           (import_bundle, "import-first"),
                                           (link_bundle, "link-first")):
                        module.apply(target, run_id)
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 2)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "resieve-first")["created"]), 2)
                    self.assertEqual(len(bundle.apply(target, "resieve-retry")["preserved"]), 2)
                    (target / "sieving/prompts/active.yml").write_text(
                        "schema_version: '1.0'\nactive:\n  DOCUMENT: appb_document_v1\n", encoding="utf-8")
                    (target / "sieving/prompts/appb_document_v1.md").write_text(
                        "# Synthetic prompt\nUse only invented text.\n", encoding="utf-8")
                    document = target / "sieving/synthetic-resieve.json"
                    document.write_text(json.dumps(payload()), encoding="utf-8")

                    def run(*extra: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/resieve_run.py"),
                             "--run-id", NEW, "--doc-id", "DOC-0001",
                             "--prompt-version", "appb_document_v1",
                             "--document-side", "DOCUMENT", "--json-file", str(document),
                             *extra], cwd=sibling if with_sibling else root,
                            capture_output=True, text=True, encoding="utf-8", timeout=30)

                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    db = make_db(target)
                    bad = payload()
                    del bad["items"][0]["item_type"]
                    document.write_text(json.dumps(bad), encoding="utf-8")
                    before_bad = db.read_bytes()
                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertEqual(db.read_bytes(), before_bad)
                    document.write_text(json.dumps(payload()), encoding="utf-8")
                    before_preview = db.read_bytes()
                    preview = run()
                    self.assertEqual(preview.returncode, 0, preview.stderr)
                    self.assertEqual(db.read_bytes(), before_preview)
                    self.assertFalse((target / "sieving/runs" / NEW).exists())
                    applied = run("--apply")
                    self.assertEqual(applied.returncode, 0, applied.stderr + applied.stdout)
                    result = json.loads(applied.stdout)
                    self.assertEqual((result["status"], result["previous_run_id"]), ("candidate", OLD))
                    self.assertEqual(result["unmatched"], 0)
                    out = target / "sieving/runs" / NEW
                    self.assertTrue((out / "metrics.json").is_file())
                    self.assertTrue((out / f"diff-{OLD}-to-{NEW}.json").is_file())
                    with closing(sqlite3.connect(db)) as conn:
                        rows = conn.execute("SELECT run_id,status,is_active,completed_at FROM sieve_runs "
                                            "ORDER BY generation").fetchall()
                        self.assertEqual([(r[0], r[1], r[2]) for r in rows],
                                         [(OLD, "active", 1), (NEW, "candidate", 0)])
                        self.assertIsNotNone(rows[1][3])
                    after = db.read_bytes()
                    self.assertEqual(run("--apply").returncode, 1)
                    self.assertEqual(db.read_bytes(), after)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_unmatched_quote_retains_inactive_candidate_without_metrics(self) -> None:
        import bootstrap_resieve as bundle

        with tempfile.TemporaryDirectory(prefix="resieve-unmatched-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "Invented Audit"
            target.mkdir()
            for module, run_id in ((state_bundle, "state-first"),
                                   (sieving_bundle, "sieving-first"),
                                   (phase_bundle, "phase-first"),
                                   (analysis_bundle, "analysis-first"),
                                   (import_bundle, "import-first"),
                                   (link_bundle, "link-first")):
                module.apply(target, run_id)
            bundle.apply(target, "resieve-first")
            (target / "sieving/prompts/active.yml").write_text(
                "schema_version: '1.0'\nactive:\n  DOCUMENT: appb_document_v1\n", encoding="utf-8")
            (target / "sieving/prompts/appb_document_v1.md").write_text(
                "# Synthetic prompt\n", encoding="utf-8")
            db = make_db(target)
            source = target / "sieving/synthetic-resieve.json"
            changed = payload()
            changed["items"][0]["evidence_quotes"][0]["quote_original"] = "No matching text"
            source.write_text(json.dumps(changed), encoding="utf-8")
            command = [sys.executable, "-B", str(target / "scripts/resieve_run.py"),
                       "--run-id", NEW, "--doc-id", "DOC-0001",
                       "--prompt-version", "appb_document_v1", "--document-side", "DOCUMENT",
                       "--json-file", str(source), "--apply"]
            result = subprocess.run(command, cwd=target, capture_output=True,
                                    text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 2, result.stderr)
            details = json.loads(result.stdout)
            self.assertEqual(details["unmatched"], 1)
            self.assertNotIn("metrics", details)
            self.assertFalse((target / "sieving/runs" / NEW).exists())
            with closing(sqlite3.connect(db)) as conn:
                rows = conn.execute("SELECT run_id,status,is_active,completed_at FROM sieve_runs "
                                    "ORDER BY generation").fetchall()
                self.assertEqual([(row[0], row[1], row[2]) for row in rows],
                                 [(OLD, "active", 1), (NEW, "candidate", 0)])
                self.assertIsNotNone(rows[1][3])
            self.assertEqual(subprocess.run(command, cwd=target, capture_output=True,
                                            text=True, encoding="utf-8", timeout=30).returncode, 1)

    def test_no_previous_run_does_not_create_an_active_run(self) -> None:
        import bootstrap_resieve as bundle

        with tempfile.TemporaryDirectory(prefix="resieve-no-prior-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "Invented Audit"
            target.mkdir()
            for module, run_id in ((state_bundle, "state-first"),
                                   (sieving_bundle, "sieving-first"),
                                   (phase_bundle, "phase-first"),
                                   (analysis_bundle, "analysis-first"),
                                   (import_bundle, "import-first"),
                                   (link_bundle, "link-first")):
                module.apply(target, run_id)
            bundle.apply(target, "resieve-first")
            (target / "sieving/prompts/active.yml").write_text(
                "schema_version: '1.0'\nactive:\n  DOCUMENT: appb_document_v1\n", encoding="utf-8")
            (target / "sieving/prompts/appb_document_v1.md").write_text(
                "# Synthetic prompt\n", encoding="utf-8")
            db = make_db(target, include_old=False)
            source = target / "sieving/synthetic-resieve.json"
            source.write_text(json.dumps(payload()), encoding="utf-8")
            before = db.read_bytes()
            result = subprocess.run(
                [sys.executable, "-B", str(target / "scripts/resieve_run.py"),
                 "--run-id", NEW, "--doc-id", "DOC-0001",
                 "--prompt-version", "appb_document_v1", "--document-side", "DOCUMENT",
                 "--json-file", str(source), "--apply"], cwd=target,
                capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 1)
            self.assertIn("needs one completed active generation", result.stderr)
            self.assertEqual(db.read_bytes(), before)

    def test_conflict_blocks_copy(self) -> None:
        import bootstrap_resieve as bundle

        with tempfile.TemporaryDirectory(prefix="resieve-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/resieve_run.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
