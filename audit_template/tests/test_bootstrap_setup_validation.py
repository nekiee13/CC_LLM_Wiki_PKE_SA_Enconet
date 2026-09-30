"""Fresh audits get neutral setup structure checks, not another firm's pages."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_dispatch as dispatch  # noqa: E402
import bootstrap_phase_validation as phase_bundle  # noqa: E402
import bootstrap_setup_validation as setup_bundle  # noqa: E402
import bootstrap_state as state_bundle  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class SetupValidationBundleTests(unittest.TestCase):
    def test_manifest_is_hash_locked_and_source_neutral(self) -> None:
        manifest = setup_bundle.load_manifest()
        self.assertEqual(manifest["scope"], "setup-structure-and-empty-validation-log")
        self.assertEqual({row["path"] for row in manifest["files"]}, {
            ".gitattributes",
            "scripts/validate_structure.py", "schemas/wiki_structure.yml",
            "manifests/validation_runs.csv",
            *(f"wiki/{name}/.gitkeep" for name in
              ("actions", "criteria", "dashboards", "evidence", "findings", "gates")),
        })
        for row in manifest["files"]:
            data = (setup_bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)
            self.assertNotIn(b"APP_B", data)
        self.assertEqual(
            (setup_bundle.BUNDLE / "manifests/validation_runs.csv").read_text(encoding="utf-8"),
            "run_utc,validator,phase,result,exit_code,details\n",
        )

    def test_two_companies_validate_empty_local_wiki_only(self) -> None:
        for company, with_sibling in (("Čista Tvrtka", True), ("Žuti Pogon", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="setup-bundle-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Enconet"
                    caller = sibling if with_sibling else root / "outside caller"
                    caller.mkdir()
                    if with_sibling:
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    nested = target / "Enconet"
                    nested.mkdir()
                    (nested / "marker.txt").write_text("keep nested", encoding="utf-8")
                    for bundle, run_id in ((state_bundle, "state-first"),
                                           (dispatch, "dispatch-first"),
                                           (phase_bundle, "phase-first")):
                        bundle.apply(target, run_id)
                    before_sibling = snapshot(sibling) if with_sibling else None
                    before_nested = snapshot(nested)
                    before = snapshot(target)
                    plan = setup_bundle.preview(target)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(plan["files"]), 10)
                    self.assertEqual({row["state"] for row in plan["files"]}, {"create"})
                    first = setup_bundle.apply(target, "setup-first")
                    self.assertEqual(len(first["created"]), 10)
                    attributes = (target / ".gitattributes").read_bytes()
                    self.assertIn(b".gitattributes text eol=lf", attributes)
                    self.assertIn(b"scripts/*.py text eol=lf", attributes)
                    self.assertIn(b"sieving/src/**/*.py text eol=lf", attributes)
                    self.assertIn(b"sieving/cli.py text eol=lf", attributes)
                    self.assertIn(b"sieving/prompts/active.yml text eol=lf", attributes)

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=caller, capture_output=True, text=True, encoding="utf-8", timeout=30,
                        )

                    log = target / "manifests/validation_runs.csv"
                    original_log = log.read_bytes()
                    checked = run("validate_structure.py", "--no-record")
                    self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                    self.assertIn("validate_structure: PASS", checked.stdout)
                    self.assertEqual(log.read_bytes(), original_log)
                    (target / "project-state.yml").write_text(
                        "phase: setup\nsupplier: Synthetic Audit\n", encoding="utf-8"
                    )
                    aggregate = run("run_all_validations.py", "--no-record")
                    self.assertEqual(aggregate.returncode, 0, aggregate.stdout + aggregate.stderr)
                    self.assertIn("aggregate: PASS", aggregate.stdout)
                    self.assertEqual(log.read_bytes(), original_log)

                    repeated = setup_bundle.apply(target, "setup-second")
                    self.assertEqual(repeated["created"], [])
                    self.assertEqual(len(repeated["preserved"]), 10)
                    recorded = run("validate_structure.py")
                    self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
                    self.assertIn("validate_structure.py,verification,PASS,0", log.read_text(encoding="utf-8"))
                    after_record = log.read_bytes()
                    bad_phase = run("validate_structure.py", "--phase", "=bad")
                    self.assertEqual(bad_phase.returncode, 1)
                    self.assertIn("phase", bad_phase.stderr.lower())
                    self.assertEqual(log.read_bytes(), after_record)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())

                    for option, foreign in (("--wiki", sibling / "wiki"),
                                            ("--schema", sibling / "schema.yml"),
                                            ("--runs", sibling / "validation_runs.csv")):
                        rejected = run("validate_structure.py", "--no-record", option, str(foreign))
                        self.assertEqual(rejected.returncode, 1)
                        self.assertIn("local", rejected.stderr.lower())
                    self.assertFalse((sibling / "validation_runs.csv").exists())
                    if with_sibling:
                        self.assertEqual(snapshot(sibling), before_sibling)
                    else:
                        self.assertFalse(sibling.exists())
                    self.assertEqual(snapshot(nested), before_nested)

    def test_bad_wiki_page_and_schema_fail_without_record(self) -> None:
        with tempfile.TemporaryDirectory(prefix="setup-invalid-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            target.mkdir()
            state_bundle.apply(target, "state-first")
            setup_bundle.apply(target, "setup-first")
            script = target / "scripts/validate_structure.py"
            log = target / "manifests/validation_runs.csv"
            before_log = log.read_bytes()
            wrong_page = target / "wiki/findings/wrong.md"
            wrong_page.write_text("synthetic", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(script), "--no-record"],
                                    capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid findings page filename", result.stderr)
            self.assertEqual(log.read_bytes(), before_log)
            wrong_page.unlink()
            schema = target / "schemas/wiki_structure.yml"
            original = schema.read_bytes()
            schema.write_text(schema.read_text(encoding="utf-8").replace(
                "wiki/criteria/", "../Enconet/criteria/"), encoding="utf-8")
            rejected = subprocess.run([sys.executable, "-B", str(script), "--no-record"],
                                      capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("schema", rejected.stderr.lower())
            self.assertEqual(log.read_bytes(), before_log)
            schema.write_bytes(original)

    def test_conflict_is_refused_before_any_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="setup-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "manifests").mkdir(parents=True)
            (target / "manifests/validation_runs.csv").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(setup_bundle.BootstrapError):
                setup_bundle.preview(target)
            with self.assertRaises(setup_bundle.BootstrapError):
                setup_bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
