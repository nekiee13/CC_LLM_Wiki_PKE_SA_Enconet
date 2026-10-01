"""The Codex skill copy is neutral, local, and safe to retry."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_sieving_harness as harness  # noqa: E402
import bootstrap_state as state  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class CodexSievingSkillsBundleTests(unittest.TestCase):
    def test_manifest_has_only_three_neutral_codex_skills(self) -> None:
        import bootstrap_codex_sieving_skills as bundle

        manifest = bundle.load_manifest()
        self.assertEqual([row["path"] for row in manifest["files"]], [
            ".agents/skills/.gitattributes",
            ".agents/skills/crumb-quality/SKILL.md",
            ".agents/skills/sieving-run/SKILL.md",
            ".agents/skills/sieving-tuning/SKILL.md",
        ])
        for row in manifest["files"]:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)
            self.assertNotIn(b".claude", data)

    def test_two_companies_copy_and_local_drift_check(self) -> None:
        import bootstrap_codex_sieving_skills as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="codex-skills-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    state.apply(target, "state-first")
                    harness.apply(target, "harness-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 4)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "skills-first")["created"]), 4)
                    self.assertEqual(len(bundle.apply(target, "skills-retry")["preserved"]), 4)
                    run = subprocess.run(
                        [sys.executable, "-B", str(target / "scripts/validate_sieving_skill_drift.py"),
                         "--allow-pending-claude"], cwd=sibling if with_sibling else root,
                        capture_output=True, text=True, encoding="utf-8", timeout=30,
                    )
                    self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                    self.assertFalse((target / ".claude").exists())
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_conflict_blocks_all_copies(self) -> None:
        import bootstrap_codex_sieving_skills as bundle

        with tempfile.TemporaryDirectory(prefix="codex-skills-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            path = target / ".agents/skills/sieving-run/SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
