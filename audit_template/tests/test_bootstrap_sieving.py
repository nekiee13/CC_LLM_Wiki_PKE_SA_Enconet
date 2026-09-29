"""Synthetic proof that one versioned bundle can start two clean audits."""
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
import bootstrap_sieving as bootstrap  # noqa: E402


def snapshot(folder: Path) -> dict[str, tuple[bytes, int]]:
    return {
        path.relative_to(folder).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
        for path in folder.rglob("*") if path.is_file()
    }


def synthetic_document() -> dict:
    return {
        "document": {"doc_id": "SYN-BOOT-1", "filename": "made-up.json", "title": "Synthetic"},
        "items": [{
            "item_id": "D-1", "record_side": "DOCUMENT", "template_id": "JSON_Template_App_B",
            "template_version": "1.1", "taxonomy_id": "APP_B", "criterion_id": "APP_B_I",
            "criterion_name": "Organization", "item_type": "control", "statement": "Made-up control",
            "evidence_quotes": ["Made-up quote"], "source": [{"page": 1}],
        }],
    }


class BootstrapSievingTests(unittest.TestCase):
    def test_bundle_is_versioned_clean_and_hash_locked(self) -> None:
        manifest = json.loads(bootstrap.MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["template_version"], "1.0.0")
        self.assertEqual(manifest["scope"], "sieving-runtime-only")
        self.assertGreaterEqual(len(manifest["files"]), 20)
        paths = {entry["path"] for entry in manifest["files"]}
        self.assertIn("sieving/cli.py", paths)
        self.assertIn("schemas/sieving_contract.yml", paths)
        self.assertIn("sieving/prompts/active.yml", paths)
        self.assertFalse(any("DATA/" in path or "fixtures/" in path for path in paths))
        for entry in manifest["files"]:
            source = bootstrap.BUNDLE.joinpath(*entry["path"].split("/"))
            data = source.read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])
            self.assertEqual(len(data), entry["bytes"])
            if source.suffix == ".py":
                self.assertNotIn("Ekonerg", data.decode("utf-8"))
        contract = json.loads((bootstrap.BUNDLE / "schemas/sieving_contract.yml").read_text(encoding="utf-8"))
        self.assertEqual(contract["canonical_codes"], [])
        active = (bootstrap.BUNDLE / "sieving/prompts/active.yml").read_text(encoding="utf-8")
        self.assertIn("active: {}", active)

    def test_preview_apply_retry_and_runtime_in_two_companies(self) -> None:
        for company, has_sibling in (("Čista Tvrtka", True), ("Žuti Pogon", False)):
            with self.subTest(company=company, has_sibling=has_sibling):
                with tempfile.TemporaryDirectory(prefix="bootstrap-sieving-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    caller = sibling if has_sibling else root / "unrelated caller"
                    caller.mkdir()
                    if has_sibling:
                        (sibling / "marker.txt").write_text("unchanged", encoding="utf-8")
                        before_sibling = snapshot(sibling)
                    before_target = snapshot(target)
                    plan = bootstrap.preview(target)
                    self.assertEqual(plan["mode"], "preview")
                    self.assertTrue(all(row["state"] == "create" for row in plan["files"]))
                    self.assertEqual(snapshot(target), before_target)

                    first = bootstrap.apply(target, "first-run")
                    self.assertEqual(len(first["created"]), len(plan["files"]))
                    self.assertEqual(first["preserved"], [])
                    copied = {row["path"]: (target / row["path"]).stat().st_mtime_ns
                              for row in plan["files"]}
                    second = bootstrap.apply(target, "second-run")
                    self.assertEqual(second["created"], [])
                    self.assertEqual(len(second["preserved"]), len(plan["files"]))
                    self.assertEqual(
                        {path: (target / path).stat().st_mtime_ns for path in copied}, copied
                    )
                    self.assertTrue(Path(first["journal"]).is_file())
                    self.assertTrue(Path(second["journal"]).is_file())

                    data_dir = target / "sieving/DATA"
                    output_dir = target / "sieving/outputs"
                    data_dir.mkdir()
                    output_dir.mkdir()
                    (data_dir / "made-up.json").write_text(json.dumps(synthetic_document()), encoding="utf-8")
                    cli = target / "sieving/cli.py"
                    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
                    info = subprocess.run(
                        [sys.executable, "-B", str(cli), "info"], cwd=caller,
                        capture_output=True, text=True, encoding="utf-8", env=env, timeout=30,
                    )
                    self.assertEqual(info.returncode, 0, info.stdout + info.stderr)
                    self.assertIn(f"{company} JSON Sieving", info.stdout)
                    query = subprocess.run(
                        [sys.executable, "-B", str(cli), "query", "--files", "sieving/DATA/made-up.json",
                         "--output", "sieving/outputs/result.csv", "--format", "csv"],
                        cwd=caller, capture_output=True, text=True, encoding="utf-8", env=env, timeout=30,
                    )
                    self.assertEqual(query.returncode, 0, query.stdout + query.stderr)
                    self.assertTrue((output_dir / "result.csv").is_file())
                    if has_sibling:
                        self.assertEqual(snapshot(sibling), before_sibling)
                    else:
                        self.assertFalse(sibling.exists())

    def test_conflict_and_links_fail_before_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bootstrap-safety-", dir=TEMPLATE / "tests") as temp:
            root = Path(temp)
            target = root / "New Audit"
            target.mkdir()
            first_path = bootstrap.load_manifest()["files"][0]["path"]
            conflict = target / first_path
            conflict.parent.mkdir(parents=True)
            conflict.write_bytes(b"owner data")
            before = snapshot(target)
            with self.assertRaises(bootstrap.BootstrapError):
                bootstrap.preview(target)
            self.assertEqual(snapshot(target), before)
            with self.assertRaises(bootstrap.BootstrapError):
                bootstrap.apply(target, "conflict-run")
            self.assertEqual(snapshot(target), before)
            with self.assertRaises(bootstrap.BootstrapError):
                bootstrap.preview(target / ".." / "New Audit")

            foreign = root / "Other Audit"
            foreign.mkdir()
            linked = root / "linked-target"
            try:
                linked.symlink_to(foreign, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            before_foreign = snapshot(foreign)
            with self.assertRaises(bootstrap.BootstrapError):
                bootstrap.preview(linked)
            self.assertEqual(snapshot(foreign), before_foreign)


if __name__ == "__main__":
    unittest.main()
