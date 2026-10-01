"""Offline evidence links are local, safe, and repeatable in two fake audits."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))


def snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class EvidenceLinkBundleTests(unittest.TestCase):
    def test_manifest_is_neutral_and_hash_locked(self) -> None:
        import bootstrap_evidence_links as bundle

        rows = bundle.load_manifest()["files"]
        self.assertEqual([row["path"] for row in rows], [
            "schemas/evidence_navigation.yml", "scripts/citation_renderer.py",
            "scripts/evidence_navigation.py",
        ])
        for row in rows:
            data = (bundle.BUNDLE / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()),
                             (row["bytes"], row["sha256"]))
            self.assertNotIn(b"Enconet", data)
            self.assertNotIn(b"Ekonerg", data)

    def test_two_companies_preview_apply_retry_and_offline_contract(self) -> None:
        import bootstrap_evidence_links as bundle

        for company, with_sibling in (("Mali Audit", True), ("Čista Tvrtka", False)):
            with self.subTest(company=company):
                with tempfile.TemporaryDirectory(prefix="evidence-links-", dir=TEMPLATE / "tests") as temp:
                    root = Path(temp)
                    target = root / company
                    target.mkdir()
                    sibling = root / "Other Audit"
                    if with_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("keep", encoding="utf-8")
                    sibling_before = snapshot(sibling) if with_sibling else None
                    before = snapshot(target)
                    self.assertEqual(len(bundle.preview(target)["files"]), 3)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(len(bundle.apply(target, "links-first")["created"]), 3)
                    self.assertEqual(len(bundle.apply(target, "links-retry")["preserved"]), 3)
                    code = (
                        "import citation_renderer as c, evidence_navigation as n\n"
                        "assert n.target('document', 'DOC-0001') == '#evidence/document/DOC-0001'\n"
                        "assert n.parse('#evidence/document/DOC-0001') == ('document', 'DOC-0001')\n"
                        "assert n.parse('#evidence/document/DOC-%30%30%30%31') is None\n"
                        "assert n.resolve('#evidence/document/DOC-9999', set())['status'] == 'unavailable'\n"
                        "assert n.safe_text('<script>')['trusted_html'] is False\n"
                        "assert c.render('document', 'DOC-0001', viewer_path='viewer/index.html') == "
                        "'[document:DOC-0001](viewer/index.html#evidence/document/DOC-0001)'\n"
                        "for path in ('../outside', 'https://bad.test/x', '/absolute', 'x?bad=1', 'x\\\\bad'):\n"
                        "  try: c.render('document', 'DOC-0001', viewer_path=path)\n"
                        "  except ValueError: pass\n"
                        "  else: raise AssertionError(path)\n"
                        "try: c.render('document', 'BAD-ID')\n"
                        "except ValueError: pass\n"
                        "else: raise AssertionError('bad ID')\n"
                    )
                    result = subprocess.run(
                        [sys.executable, "-B", "-c", code],
                        cwd=sibling if with_sibling else root,
                        env={"PYTHONPATH": str(target / "scripts"), "PYTHONUTF8": "1"},
                        capture_output=True, text=True, encoding="utf-8", timeout=30,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(snapshot(sibling) if with_sibling else None, sibling_before)

    def test_existing_conflict_fails_without_changes(self) -> None:
        import bootstrap_evidence_links as bundle

        with tempfile.TemporaryDirectory(prefix="evidence-links-conflict-", dir=TEMPLATE / "tests") as temp:
            target = Path(temp) / "New Audit"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts/citation_renderer.py").write_text("owner", encoding="utf-8")
            before = snapshot(target)
            with self.assertRaises(bundle.BootstrapError):
                bundle.apply(target, "links-conflict")
            self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
