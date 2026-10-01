"""Golden scoring must stay local and refuse invented approval."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import bootstrap_state as state_bundle  # noqa: E402
import bootstrap_sieving_harness as harness_bundle  # noqa: E402


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class ScoreBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_sieving_score as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([r["path"] for r in rows],
                         ["manifests/approvals.csv", "scripts/score_sieving.py"])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_pending_then_synthetic_approval(self) -> None:
        import bootstrap_sieving_score as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="score-bundle-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    before_sibling = snapshot(sibling) if with_sibling else None
                    state_bundle.apply(target, "state-first")
                    harness_bundle.apply(target, "harness-first")
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 2)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "score-first")["created"]), 2)
                    self.assertEqual(len(bundle.apply(target, "score-retry")["preserved"]), 2)
                    actual = target / "sieving" / "actual.json"
                    actual.write_text(json.dumps({"prompt_version": "candidate_v1",
                                                  "document": {"doc_id": "DOC-0001"}, "items": [
                        {"criterion_id": "APP_B_I", "statement": "One claim",
                         "quotes": ["Exact quote"]}]}), encoding="utf-8")
                    golden = target / "benchmarks/sieving_golden/manifest.yml"
                    output = target / "sieving/score.json"

                    def run(*extra: str) -> subprocess.CompletedProcess[str]:
                        return subprocess.run(
                            [sys.executable, "-B", str(target / "scripts/score_sieving.py"),
                             "--golden", str(golden), "--actual", str(actual),
                             "--output", str(output), *extra],
                            cwd=sibling if with_sibling else root, capture_output=True,
                            text=True, encoding="utf-8", timeout=30,
                        )

                    strict = run()
                    self.assertEqual(strict.returncode, 2, strict.stdout + strict.stderr)
                    self.assertFalse(output.exists())
                    draft = run("--allow-draft")
                    self.assertEqual(draft.returncode, 0, draft.stdout + draft.stderr)
                    self.assertFalse(json.loads(output.read_text(encoding="utf-8"))["promotion_ready"])
                    output.unlink()
                    golden.write_text(
                        "schema_version: '1.0'\nfixture_version: '1.0'\nstatus: approved\n"
                        "approval_ref: GOLDEN-001\ndocument: {doc_id: DOC-0001}\n"
                        "expected_crumbs:\n  - criterion_id: APP_B_I\n"
                        "    statement: One claim\n    quotes: [Exact quote]\n", encoding="utf-8"
                    )
                    self.assertEqual(run().returncode, 2)
                    self.assertFalse(output.exists())
                    approvals = target / "manifests/approvals.csv"
                    approvals.write_text(
                        "object_id,decision,date,reviewer,notes\n"
                        "GOLDEN-001,approved,2026-01-01,synthetic-reviewer,test-only\n",
                        encoding="utf-8",
                    )
                    accepted = run()
                    self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
                    self.assertTrue(json.loads(output.read_text(encoding="utf-8"))["promotion_ready"])
                    output.unlink()
                    actual.write_text(json.dumps({"prompt_version": "candidate_v1",
                                                  "document": {"doc_id": "DOC-OTHER"}, "items": [
                        {"criterion_id": "APP_B_I", "statement": "One claim", "quotes": ["Exact quote"]}]}),
                        encoding="utf-8")
                    wrong_doc = run()
                    self.assertEqual(wrong_doc.returncode, 1)
                    self.assertIn("document", wrong_doc.stderr.lower())
                    self.assertFalse(output.exists())
                    actual.write_text(json.dumps({"prompt_version": "candidate_v1",
                                                  "document": {"doc_id": "DOC-0001"}, "items": [
                        {"criterion_id": "APP_B_I", "statement": "One claim", "quotes": ["Exact quote"]},
                        {"criterion_id": "APP_B_I", "statement": "One claim", "quotes": ["Exact quote"]}]}),
                        encoding="utf-8")
                    duplicate = run()
                    self.assertEqual(duplicate.returncode, 1)
                    self.assertIn("duplicate", duplicate.stderr.lower())
                    self.assertFalse(output.exists())
                    foreign = run("--output", str(sibling / "foreign.json"))
                    self.assertEqual(foreign.returncode, 1)
                    self.assertFalse((sibling / "foreign.json").exists())
                    self.assertEqual(snapshot(sibling) if with_sibling else None, before_sibling)

    def test_conflicting_target_blocks_copy(self) -> None:
        import bootstrap_sieving_score as bundle

        with tempfile.TemporaryDirectory(prefix="score-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/score_sieving.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "score-conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
