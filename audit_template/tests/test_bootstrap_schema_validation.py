"""Neutral schema contracts stay local and do not approve source editions."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_evidence_validation as evidence_bundle  # noqa: E402
import bootstrap_sieving as sieving_bundle  # noqa: E402
import bootstrap_state as state_bundle  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class SchemaValidationBundleTests(unittest.TestCase):
    def test_manifest_hashes_and_exact_copy_set(self) -> None:
        import bootstrap_schema_validation as bundle

        manifest = bundle.load_manifest()
        self.assertEqual([row["path"] for row in manifest["files"]], [
            "schemas/app_b_json_schema.yml", "schemas/dashboard_schema.yml",
            "schemas/evaluation_package_schema.yml", "schemas/scoring_model.yml",
            "scripts/validate_schemas.py",
        ])
        for row in manifest["files"]:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_company_roots_and_pending_source_codes(self) -> None:
        import bootstrap_schema_validation as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="schema-bundle-", dir=TEMPLATE / "tests") as temp:
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
                    evidence_bundle.apply(target, "evidence-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 5)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "schema-first")["created"]), 5)
                    self.assertEqual(len(bundle.apply(target, "schema-second")["preserved"]), 5)

                    def run(*args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/validate_schemas.py"), *args],
                            cwd=sibling if with_sibling else root, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    valid = run("--no-record")
                    self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
                    self.assertIn("source selection pending", valid.stdout)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    self.assertFalse((target / "manifests/validation_runs.csv").exists())
                    contract = yaml.safe_load((target / "schemas/sieving_contract.yml").read_text(encoding="utf-8"))
                    vocabulary = yaml.safe_load((target / "schemas/vocabularies.yml").read_text(encoding="utf-8"))
                    self.assertEqual(contract["canonical_codes"], [])
                    self.assertEqual(vocabulary["vocabularies"]["source_rules"]["values"], [])

                    foreign = run("--schemas", str(sibling))
                    self.assertEqual(foreign.returncode, 1)
                    self.assertIn("local", foreign.stdout.lower() + foreign.stderr.lower())
                    self.assertFalse((sibling / "validation_runs.csv").exists())
                    no_log = run()
                    self.assertEqual(no_log.returncode, 1)
                    self.assertIn("record could not be written", no_log.stdout + no_log.stderr)
                    log = target / "manifests/validation_runs.csv"
                    log.write_text("run_utc,validator,phase,result,exit_code,details\n", encoding="utf-8")
                    recorded = run()
                    self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
                    self.assertIn("validate_schemas.py,unknown,PASS,0", log.read_text(encoding="utf-8"))

                    scoring = target / "schemas/scoring_model.yml"
                    scoring.write_text(scoring.read_text(encoding="utf-8").replace(
                        'model_version: "0.1-placeholder"', 'model_version: "1.0"').replace(
                        'calibration_status: "pending human calibration approval"',
                        'calibration_status: "approved"\napproval_ref: "G3-synthetic"'),
                        encoding="utf-8")
                    no_approval = run("--no-record")
                    self.assertEqual(no_approval.returncode, 1)
                    self.assertIn("matching local approval row", no_approval.stderr)
                    (target / "manifests/approvals.csv").write_text(
                        "object_id,decision,date,reviewer,notes\n"
                        "G3-synthetic,approved,2026-10-01,Synthetic Owner,model version 1.0\n",
                        encoding="utf-8",
                    )
                    approved_fixture = run("--no-record")
                    self.assertEqual(approved_fixture.returncode, 0,
                                     approved_fixture.stdout + approved_fixture.stderr)
                    scoring.write_text(scoring.read_text(encoding="utf-8").replace(
                        "  fully: 1.00\n", "", 1), encoding="utf-8")
                    invalid = run("--no-record")
                    self.assertEqual(invalid.returncode, 1)
                    self.assertIn("rating_weights", invalid.stdout + invalid.stderr)
                    with self.assertRaises(bundle.BootstrapError):
                        bundle.apply(target, "after-schema-edit")
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_conflict_blocks_all_copy(self) -> None:
        import bootstrap_schema_validation as bundle

        with tempfile.TemporaryDirectory(prefix="schema-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "schemas").mkdir(parents=True)
            (target / "schemas/scoring_model.yml").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
