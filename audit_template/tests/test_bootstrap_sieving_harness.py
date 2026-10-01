"""The sieving harness checks local readiness without approving a source."""
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
import bootstrap_sieving as sieving_bundle  # noqa: E402
import bootstrap_state as state_bundle  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class SievingHarnessBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_sieving_harness as bundle

        manifest = bundle.load_manifest()
        self.assertEqual([row["path"] for row in manifest["files"]], [
            "benchmarks/sieving_golden/manifest.yml", "schemas/sieving_skill_contract.yml",
            "scripts/validate_sieving_harness.py", "scripts/validate_sieving_skill_drift.py",
            "sieving/SIEVING_PLAYBOOK.md", "sieving/prompts/.gitattributes",
            "sieving/prompts/CHANGELOG.md", "sieving/prompts/appb_document_v1.md",
            "sieving/prompts/appb_rule_v1.md",
        ])
        for row in manifest["files"]:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_fail_closed_then_pass_synthetic_readiness(self) -> None:
        import bootstrap_sieving_harness as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="harness-bundle-", dir=TEMPLATE / "tests") as temp:
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
                    self.assertEqual(len(bundle.preview(target)["files"]), 9)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "harness-first")["created"]), 9)
                    self.assertEqual(len(bundle.apply(target, "harness-second")["preserved"]), 9)

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=sibling if with_sibling else root, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    missing = run("validate_sieving_harness.py", "--allow-pending-claude")
                    self.assertEqual(missing.returncode, 1)
                    self.assertIn("local database is missing", missing.stderr)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    foreign = run("validate_sieving_harness.py", "--db",
                                  str(sibling / "foreign.sqlite"), "--allow-pending-claude")
                    self.assertEqual(foreign.returncode, 1)
                    self.assertIn("local", foreign.stderr.lower())
                    self.assertFalse((sibling / "foreign.sqlite").exists())

                    db = target / "db/nqa_audit.sqlite"
                    with closing(sqlite3.connect(db)) as conn, conn:
                        conn.executescript(
                            "CREATE TABLE sieve_runs (run_id TEXT, doc_id TEXT, generation INTEGER, "
                            "status TEXT, is_active INTEGER, supersedes_run_id TEXT, "
                            "completed_at TEXT, decision_ref TEXT, rejected_item_count INTEGER, "
                            "failed_item_count INTEGER);"
                            "CREATE TABLE crumbs (item_id TEXT, sieve_run_id TEXT);"
                            "CREATE VIEW active_crumbs AS SELECT c.* FROM crumbs c JOIN sieve_runs r "
                            "ON r.run_id=c.sieve_run_id WHERE r.is_active=1;"
                        )
                    incomplete = run("validate_sieving_harness.py", "--allow-pending-claude")
                    self.assertEqual(incomplete.returncode, 1)
                    self.assertIn("active prompt is missing", incomplete.stderr)

                    prompts = target / "sieving/prompts"
                    (prompts / "active.yml").write_text(
                        "schema_version: '1.0'\nactive:\n  RULE: appb_rule_v1\n"
                        "  DOCUMENT: appb_document_v1\n", encoding="utf-8"
                    )
                    (prompts / "CHANGELOG.md").write_text(
                        "appb_rule_v1\nappb_document_v1\n", encoding="utf-8"
                    )
                    for name in ("appb_rule_v1", "appb_document_v1"):
                        (prompts / f"{name}.md").write_text("Synthetic prompt\n", encoding="utf-8")
                    for name in ("sieve_run.py", "import_crumbs.py", "link_crumbs.py",
                                 "resieve_run.py", "sieve_metrics.py", "sieve_diff.py",
                                 "score_sieving.py", "sieve_generation.py"):
                        (target / "scripts" / name).write_text("# synthetic stub\n", encoding="utf-8")
                    markers = {
                        "sieving-run": "SIEVING_PLAYBOOK.md new RUN-id strict candidate unfiltered failure",
                        "crumb-quality": "verbatim quote language authority V / VI / XVII IV / VII X / XI",
                        "sieving-tuning": "metrics diff golden human approval promotion-ready deposit",
                    }
                    for name, content in markers.items():
                        path = target / ".agents/skills" / name / "SKILL.md"
                        path.parent.mkdir(parents=True)
                        path.write_text(content, encoding="utf-8")
                    pending_claude = run("validate_sieving_harness.py", "--allow-pending-claude")
                    self.assertEqual(pending_claude.returncode, 0,
                                     pending_claude.stdout + pending_claude.stderr)
                    self.assertIn("golden calibration set remains pending", pending_claude.stdout)
                    strict = run("validate_sieving_harness.py")
                    self.assertEqual(strict.returncode, 1)
                    self.assertIn("Claude skill missing", strict.stderr)
                    self.assertFalse((target / ".claude").exists())
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_existing_conflict_blocks_copy(self) -> None:
        import bootstrap_sieving_harness as bundle

        with tempfile.TemporaryDirectory(prefix="harness-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/validate_sieving_harness.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
