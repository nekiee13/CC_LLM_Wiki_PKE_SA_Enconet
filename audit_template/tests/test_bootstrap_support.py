"""Synthetic checks for the project-local support bundle and empty inbox."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_support as support  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class SupportBundleTests(unittest.TestCase):
    def test_manifest_is_complete_clean_and_hash_locked(self) -> None:
        manifest = support.load_manifest()
        self.assertEqual(manifest["template_version"], "1.0.0")
        self.assertEqual(manifest["scope"], "project-support-and-empty-incoming")
        paths = {entry["path"] for entry in manifest["files"]}
        self.assertEqual(paths, {
            "incoming/.gitkeep", "handoff_schema.yml", "scripts/agent_coord.py",
            "scripts/make_handoff.py", "scripts/check_guidance_drift.py",
            "scripts/check_skill_structure.py",
        })
        for entry in manifest["files"]:
            source = support.BUNDLE / entry["path"]
            data = source.read_bytes()
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])
            if source.suffix == ".py":
                self.assertNotIn("Ekonerg", data.decode("utf-8"))
        self.assertEqual((support.BUNDLE / "incoming/.gitkeep").read_bytes(), b"\n")

    def test_two_companies_copy_run_retry_and_keep_sibling(self) -> None:
        for company, with_sibling in (("Čista Tvrtka", True), ("Žuti Pogon", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="support-bundle-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    caller = sibling if with_sibling else root / "unrelated caller"
                    caller.mkdir()
                    if with_sibling:
                        (sibling / "marker.txt").write_text("same", encoding="utf-8")
                        sibling_before = snapshot(sibling)
                    before = snapshot(target)
                    plan = support.preview(target)
                    self.assertTrue(all(row["state"] == "create" for row in plan["files"]))
                    self.assertEqual(snapshot(target), before)
                    first = support.apply(target, "support-first")
                    self.assertEqual(len(first["created"]), len(plan["files"]))
                    self.assertTrue((target / "incoming").is_dir())
                    self.assertEqual(list((target / "incoming").iterdir()), [target / "incoming/.gitkeep"])

                    def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts" / script), *args],
                            cwd=caller, capture_output=True, text=True, encoding="utf-8",
                            env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=30,
                        )

                    for args in (
                        ("claim", "SYNTHETIC", "--agent", "codex"),
                        ("message", "--from", "codex", "--to", "claude-code", "--type", "note",
                         "--task", "SYNTHETIC", "--topic", "synthetic", "--body", "test only"),
                        ("status", "--write"),
                        ("validate",),
                    ):
                        result = run("agent_coord.py", *args)
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertTrue((target / "coordination/BOARD.md").is_file())
                    self.assertEqual(len(list((target / "coordination/messages").glob("CX_*.md"))), 1)

                    handoff = run("make_handoff.py", "--status", "partial",
                                  "--next-action", "Synthetic next action")
                    self.assertEqual(handoff.returncode, 0, handoff.stdout + handoff.stderr)
                    records = list((target / "handoffs").glob("*.md"))
                    self.assertEqual(len(records), 1)
                    self.assertIn(f"project: {company}", records[0].read_text(encoding="utf-8"))
                    validated = run("make_handoff.py", "--validate", str(records[0]))
                    self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
                    self.assertEqual(run("check_skill_structure.py", "--list").returncode, 0)
                    missing_guidance = run("check_guidance_drift.py")
                    self.assertEqual(missing_guidance.returncode, 1)
                    self.assertIn("GUIDANCE_PAIRS.json", missing_guidance.stderr)

                    # Raw owner drop-offs are not intake or approval records.
                    (target / "incoming" / "company-note.txt").write_text("invented QMS", encoding="utf-8")
                    (target / "incoming" / "rule-note.txt").write_text("invented rule", encoding="utf-8")
                    before_retry = snapshot(target)
                    second = support.apply(target, "support-second")
                    self.assertEqual(second["created"], [])
                    self.assertEqual(len(second["preserved"]), len(plan["files"]))
                    for path, value in before_retry.items():
                        if path.startswith(".bootstrap/"):
                            continue
                        self.assertEqual(snapshot(target)[path], value)
                    if with_sibling:
                        self.assertEqual(snapshot(sibling), sibling_before)
                    else:
                        self.assertFalse(sibling.exists())

    def test_conflict_blocks_all_copies(self) -> None:
        with tempfile.TemporaryDirectory(prefix="support-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            target.mkdir()
            (target / "handoff_schema.yml").write_bytes(b"owner file")
            before = snapshot(target)
            with self.assertRaises(support.BootstrapError):
                support.preview(target)
            with self.assertRaises(support.BootstrapError):
                support.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
