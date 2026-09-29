"""Synthetic I/O isolation tests; no real corpus or output is used."""
from __future__ import annotations

import importlib
import os
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path

import pandas as pd


PROJECT = Path(__file__).resolve().parents[2]
PACKAGE_FILES = ("config.py", "contract.py")
IO_FILES = ("__init__.py", "_paths.py", "files.py", "export.py")


class IOPathsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ekonerg-io-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "Županija with spaces" / "Ekonerg"
        self.package = self.project / "sieving" / "src" / "json_extractor"
        self.io_dir = self.package / "io"
        self.io_dir.mkdir(parents=True)
        schema_dir = self.project / "schemas"
        schema_dir.mkdir()
        for name in PACKAGE_FILES:
            shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / name,
                            self.package / name)
        for name in IO_FILES:
            shutil.copyfile(PROJECT / "sieving" / "src" / "json_extractor" / "io" / name,
                            self.io_dir / name)
        for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
            shutil.copyfile(PROJECT / "schemas" / name, schema_dir / name)
        self.addCleanup(self._forget_modules)
        self._forget_modules()
        package = types.ModuleType("ekonerg_io_fixture")
        package.__path__ = [str(self.package)]
        sys.modules[package.__name__] = package
        self.io = importlib.import_module("ekonerg_io_fixture.io")
        self.files = importlib.import_module("ekonerg_io_fixture.io.files")
        self.export = importlib.import_module("ekonerg_io_fixture.io.export")
        self.data = self.project / "sieving" / "DATA"
        self.data.mkdir()

    @staticmethod
    def _forget_modules() -> None:
        for name in tuple(sys.modules):
            if name == "ekonerg_io_fixture" or name.startswith("ekonerg_io_fixture."):
                del sys.modules[name]

    def _foreign_marker(self) -> Path:
        sibling = self.project.parent / "Enconet"
        sibling.mkdir(exist_ok=True)
        marker = sibling / "source.json"
        marker.write_text('{"company":"Enconet"}', encoding="utf-8")
        return marker

    def test_public_io_import_and_local_discovery_are_deterministic(self) -> None:
        (self.data / "DOCUMENT").mkdir()
        (self.data / "RULE").mkdir()
        for name in ("RULE/z.json", "DOCUMENT/b.json", "RULE/a.json"):
            (self.data / name).write_text('{"ok":true}', encoding="utf-8")
        found = self.io.discover_json_files(Path("sieving/DATA"), ["*.json", "*.json"])
        self.assertEqual([p.relative_to(self.data).as_posix() for p in found],
                         ["DOCUMENT/b.json", "RULE/a.json", "RULE/z.json"])
        self.assertEqual(self.io.read_json_file(found[0])[0], {"ok": True})

    def test_read_and_discovery_reject_sibling_and_nested_enconet(self) -> None:
        marker = self._foreign_marker()
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
        for path in (marker, self.project / "Enconet" / "source.json"):
            with self.assertRaises(ValueError):
                self.files.read_json_file(path)
            with self.assertRaises(ValueError):
                self.files.discover_json_files(path.parent)
        self.assertFalse((self.project / "Enconet").exists())
        self.assertEqual((marker.read_bytes(), marker.stat().st_mtime_ns), before)

    def test_link_to_foreign_file_is_rejected(self) -> None:
        marker = self._foreign_marker()
        link = self.data / "foreign.json"
        try:
            link.symlink_to(marker)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")
        with self.assertRaises(ValueError):
            self.files.read_json_file(link)
        with self.assertRaises(ValueError):
            self.files.discover_json_files(self.data)

    def test_hard_link_to_foreign_file_is_rejected(self) -> None:
        marker = self._foreign_marker()
        link = self.data / "foreign-hardlink.json"
        try:
            os.link(marker, link)
        except OSError as exc:
            self.skipTest(f"hard link unavailable: {exc}")
        with self.assertRaises(ValueError):
            self.files.read_json_file(link)

    def test_bad_local_json_is_reported_without_foreign_access(self) -> None:
        bad = self.data / "bad.json"
        bad.write_text("{broken", encoding="utf-8")
        data, report = self.files.read_json_file(bad)
        self.assertIsNone(data)
        self.assertEqual(report.error_type, "JSON_DECODE_ERROR")

    def test_pattern_traversal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.files.discover_json_files(self.data, ["../*.json"])

    def test_relative_paths_do_not_depend_on_caller_directory(self) -> None:
        source = self.data / "source.json"
        source.write_text('{"company":"Ekonerg"}', encoding="utf-8")
        caller = self.project.parent / "another caller"
        caller.mkdir()
        before = Path.cwd()
        try:
            os.chdir(caller)
            found = self.files.discover_json_files(Path("sieving/DATA"))
            self.assertEqual(found, [source])
            self.assertEqual(self.files.read_json_file(Path("sieving/DATA/source.json"))[0],
                             {"company": "Ekonerg"})
        finally:
            os.chdir(before)

    def test_local_exports_preserve_values_and_selected_columns(self) -> None:
        output = self.project / "sieving" / "outputs"
        output.mkdir()
        df = pd.DataFrame([{"name": "Ekonerg", "value": 2, "ignore": "x"}])
        for extension in (".csv", ".xlsx", ".md"):
            target = self.export.export_dataframe(df, Path("sieving/outputs/result" + extension),
                                                  columns=["name", "value"])
            self.assertEqual(target, output / ("result" + extension))
            self.assertTrue(target.is_file())
        self.assertEqual(list(pd.read_csv(output / "result.csv").columns), ["name", "value"])
        self.assertEqual(list(pd.read_excel(output / "result.xlsx").columns), ["name", "value"])
        self.assertIn("Ekonerg", (output / "result.md").read_text(encoding="utf-8"))

    def test_every_export_rejects_foreign_targets_before_write(self) -> None:
        marker = self._foreign_marker()
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
        df = pd.DataFrame([{"name": "Ekonerg"}])
        for function, extension in ((self.export.export_to_csv, ".csv"),
                                    (self.export.export_to_xlsx, ".xlsx"),
                                    (self.export.export_to_markdown, ".md"),
                                    (self.export.export_dataframe, ".csv")):
            target = marker.parent / ("result" + extension)
            with self.assertRaises(ValueError):
                function(df, target)
            self.assertFalse(target.exists())
        self.assertEqual((marker.read_bytes(), marker.stat().st_mtime_ns), before)

    def test_export_rejects_nested_enconet_and_linked_output(self) -> None:
        marker = self._foreign_marker()
        df = pd.DataFrame([{"name": "Ekonerg"}])
        with self.assertRaises(ValueError):
            self.export.export_dataframe(df, self.project / "Enconet" / "result.csv")
        link = self.project / "sieving" / "external"
        try:
            link.symlink_to(marker.parent, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")
        with self.assertRaises(ValueError):
            self.export.export_dataframe(df, link / "result.csv")
        self.assertFalse((marker.parent / "result.csv").exists())

    def test_export_rejects_existing_hard_link(self) -> None:
        marker = self._foreign_marker()
        target = self.project / "sieving" / "foreign-hardlink.csv"
        try:
            os.link(marker, target)
        except OSError as exc:
            self.skipTest(f"hard link unavailable: {exc}")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
        with self.assertRaises(ValueError):
            self.export.export_to_csv(pd.DataFrame([{"name": "Ekonerg"}]), target)
        self.assertEqual((marker.read_bytes(), marker.stat().st_mtime_ns), before)


if __name__ == "__main__":
    unittest.main()
