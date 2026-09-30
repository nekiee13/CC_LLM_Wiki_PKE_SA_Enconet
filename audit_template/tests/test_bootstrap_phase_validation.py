"""Synthetic proof that phase validation stays local and fails closed."""
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
import bootstrap_state as state_bundle  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class PhaseValidationBundleTests(unittest.TestCase):
    def test_manifest_is_hash_locked_and_company_neutral(self) -> None:
        manifest = phase_bundle.load_manifest()
        self.assertEqual(manifest["scope"], "phase-aware-validation-runtime")
        self.assertEqual([row["path"] for row in manifest["files"]],
                         ["scripts/run_all_validations.py"])
        row = manifest["files"][0]
        data = (phase_bundle.BUNDLE / row["path"]).read_bytes()
        self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                         (row["bytes"], row["sha256"]))
        self.assertNotIn(b"Enconet", data)
        self.assertNotIn(b"Ekonerg", data)

    def test_copied_phase_matrix_is_monotonic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phase-matrix-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "Mali Audit"
            target.mkdir()
            state_bundle.apply(target, "state-first")
            phase_bundle.apply(target, "phase-first")
            code = (
                "import run_all_validations as m\n"
                "assert m.PHASES + ['failed'] == m.AUDIT_STATES\n"
                "previous = set()\n"
                "for phase in m.PHASES:\n"
                "    current = {name for name in m.ORDER if m.applicable(name, phase)}\n"
                "    assert previous <= current\n"
                "    previous = current\n"
                "assert all(m.applicable(name, 'failed') for name in m.ORDER)\n"
                "assert not m.applicable('report', 'findings_approved')\n"
                "assert m.applicable('report', 'report_ready')\n"
                "assert not m.applicable('dashboard', 'report_ready')\n"
                "assert m.applicable('dashboard', 'dashboard_ready')\n"
                "assert m.benchmarks_required('findings_approved')\n"
            )
            result = subprocess.run([sys.executable, "-B", "-c", code],
                                    cwd=target / "scripts", capture_output=True, text=True,
                                    encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_two_companies_fail_closed_without_touching_sibling(self) -> None:
        for company, with_sibling in (("Čista Tvrtka", True), ("Žuti Pogon", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="phase-bundle-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Enconet"
                    caller = sibling if with_sibling else root / "outside caller"
                    caller.mkdir()
                    nested = target / "Enconet"
                    nested.mkdir()
                    (nested / "marker.txt").write_text("keep nested", encoding="utf-8")
                    before_nested = snapshot(nested)
                    if with_sibling:
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    state_bundle.apply(target, "state-first")
                    dispatch.apply(target, "dispatch-first")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    before = snapshot(target)
                    plan = phase_bundle.preview(target)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(plan["files"][0]["state"], "create")
                    applied = phase_bundle.apply(target, "phase-first")
                    self.assertEqual(len(applied["created"]), 1)

                    def run(*args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/run_all_validations.py"), *args],
                            cwd=caller, capture_output=True, text=True, encoding="utf-8", timeout=30,
                        )

                    state_file = target / "project-state.yml"

                    def set_state(phase: str, supplier: str = "Synthetic Audit") -> None:
                        gates = "gates:\n" + "".join(
                            f"  G{i}: {{status: pending, decision_ref: null}}\n"
                            for i in range(1, 8)
                        )
                        state_file.write_text(
                            f"phase: {phase}\nsupplier: {supplier}\n{gates}", encoding="utf-8"
                        )

                    set_state("setup")
                    missing = run("--no-record")
                    self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
                    self.assertIn("structure", missing.stdout)
                    self.assertIn("FAIL", missing.stdout)
                    self.assertIn("[SKIPPED] raw_sources", missing.stdout)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    self.assertFalse((target / "manifests/validation_runs.csv").exists())
                    routed = subprocess.run(
                        [sys.executable, "-B", str(target / "scripts/audit_command.py"),
                         "audit-validate", "--no-record"], cwd=caller,
                        capture_output=True, text=True, encoding="utf-8", timeout=30,
                    )
                    self.assertEqual(routed.returncode, 1)
                    self.assertIn("aggregate: FAIL", routed.stdout)

                    for option, foreign in (("--state", sibling / "state.yml"),
                                            ("--db", sibling / "foreign.sqlite"),
                                            ("--outputs", sibling / "outputs"),
                                            ("--data-root", sibling / "DATA"),
                                            ("--app-b-json", sibling / "crumbs.json")):
                        rejected = run("--no-record", option, str(foreign))
                        self.assertEqual(rejected.returncode, 1)
                        self.assertIn("local", rejected.stderr.lower())
                    self.assertFalse((sibling / "foreign.sqlite").exists())

                    set_state("registered")
                    registered = run("--no-record")
                    self.assertEqual(registered.returncode, 1)
                    self.assertFalse((target / "db/nqa_audit.sqlite").exists())
                    set_state("setup", "../Enconet")
                    unsafe_supplier = run("--no-record")
                    self.assertEqual(unsafe_supplier.returncode, 1)
                    self.assertIn("supplier", unsafe_supplier.stderr.lower())
                    set_state("setup")
                    unsafe_run_id = run("--no-record", "--run-id", "../Enconet")
                    self.assertEqual(unsafe_run_id.returncode, 1)
                    self.assertIn("run id", unsafe_run_id.stderr.lower())

                    (target / "scripts/validate_structure.py").write_text(
                        "raise SystemExit(0)\n", encoding="utf-8")
                    setup = run("--no-record")
                    self.assertEqual(setup.returncode, 0, setup.stdout + setup.stderr)
                    self.assertIn("[PASS] structure", setup.stdout)
                    self.assertIn("aggregate: PASS", setup.stdout)
                    self.assertFalse((target / "manifests/validation_runs.csv").exists())
                    (target / "manifests").mkdir()
                    missing_log = run()
                    self.assertEqual(missing_log.returncode, 1)
                    self.assertIn("record could not be written", missing_log.stderr)
                    self.assertNotIn("aggregate: PASS", missing_log.stdout)
                    self.assertFalse((target / "manifests/validation_runs.csv").exists())
                    manifest = target / "manifests/validation_runs.csv"
                    manifest.write_text("wrong\n", encoding="utf-8")
                    bad_header = run()
                    self.assertEqual(bad_header.returncode, 1)
                    self.assertEqual(manifest.read_text(encoding="utf-8"), "wrong\n")
                    manifest.write_text(
                        "run_utc,validator,phase,result,exit_code,details\n", encoding="utf-8"
                    )
                    recorded = run()
                    self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
                    self.assertIn("aggregate: PASS", recorded.stdout)
                    self.assertIn("run_all_validations.py,setup,PASS,0", manifest.read_text(encoding="utf-8"))
                    repeat = phase_bundle.apply(target, "phase-second")
                    self.assertEqual(repeat["created"], [])
                    self.assertEqual(len(repeat["preserved"]), 1)
                    if with_sibling:
                        self.assertEqual(snapshot(sibling), before_sibling)
                    else:
                        self.assertFalse(sibling.exists())
                    self.assertEqual(snapshot(nested), before_nested)

    def test_existing_conflict_stops_before_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phase-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/run_all_validations.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(phase_bundle.BootstrapError):
                phase_bundle.preview(target)
            with self.assertRaises(phase_bundle.BootstrapError):
                phase_bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
