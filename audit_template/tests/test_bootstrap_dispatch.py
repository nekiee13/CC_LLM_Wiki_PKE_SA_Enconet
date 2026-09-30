"""A fresh audit gets local command routing and a fail-closed preflight runner."""
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
import bootstrap_state as state  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class DispatchBundleTests(unittest.TestCase):
    def test_manifest_is_hash_locked_and_company_neutral(self) -> None:
        manifest = dispatch.load_manifest()
        self.assertEqual(manifest["scope"], "dispatcher-and-layered-preflight")
        self.assertEqual({row["path"] for row in manifest["files"]}, {
            "schemas/audit_commands.yml", "scripts/audit_command.py",
            "scripts/run_validation.py",
        })
        for row in manifest["files"]:
            data = (dispatch.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Ekonerg", data)
            self.assertNotIn(b"ENCONET =", data)

    def test_two_companies_keep_sibling_unchanged_and_missing_validator_closed(self) -> None:
        for company, with_sibling in (("Cista Tvrtka Č", True), ("Žuti Pogon", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="dispatch-bundle-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    caller = sibling if with_sibling else root / "separate caller"
                    caller.mkdir()
                    if with_sibling:
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    state.apply(target, "state-first")
                    before = snapshot(target)
                    plan = dispatch.preview(target)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual({row["state"] for row in plan["files"]}, {"create"})
                    first = dispatch.apply(target, "dispatch-first")
                    self.assertEqual(len(first["created"]), 3)
                    self.assertFalse((target / "scripts/run_all_validations.py").exists())

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=caller, capture_output=True, text=True, encoding="utf-8", timeout=30,
                        )

                    listed = run("run_validation.py", "--list")
                    self.assertEqual(listed.returncode, 0, listed.stdout + listed.stderr)
                    for layer in ("L0", "L1", "L2", "L3", "L4", "L5"):
                        self.assertIn(layer, listed.stdout)
                    self.assertIn(str(target), listed.stdout)
                    self.assertNotIn(str(sibling), listed.stdout)
                    described = run("audit_command.py", "--describe")
                    self.assertEqual(described.returncode, 0, described.stdout + described.stderr)
                    self.assertIn("audit-validate", described.stdout)
                    self.assertIn("audit-close", described.stdout)
                    (target / "project-state.yml").write_text(
                        "phase: setup\ngates:\n" + "".join(
                            f"  G{i}: {{status: pending, decision_ref: null}}\n" for i in range(1, 8)),
                        encoding="utf-8",
                    )
                    status = run("audit_command.py", "audit-status")
                    self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
                    self.assertIn("phase: setup", status.stdout)
                    unavailable = run("audit_command.py", "--dry-run", "audit-validate")
                    self.assertEqual(unavailable.returncode, 1)
                    self.assertIn("missing run_all_validations.py", unavailable.stderr)
                    foreign = run("audit_command.py", "--db", str(sibling / "foreign.sqlite"), "--describe")
                    self.assertEqual(foreign.returncode, 1)
                    self.assertFalse((sibling / "foreign.sqlite").exists())
                    second = dispatch.apply(target, "dispatch-second")
                    self.assertEqual(second["created"], [])
                    self.assertEqual(len(second["preserved"]), 3)
                    if with_sibling:
                        self.assertEqual(snapshot(sibling), before_sibling)
                    else:
                        self.assertFalse(sibling.exists())

    def test_conflict_is_refused_before_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dispatch-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "schemas").mkdir(parents=True)
            (target / "schemas/audit_commands.yml").write_text("owner file", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(dispatch.BootstrapError):
                dispatch.preview(target)
            with self.assertRaises(dispatch.BootstrapError):
                dispatch.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
