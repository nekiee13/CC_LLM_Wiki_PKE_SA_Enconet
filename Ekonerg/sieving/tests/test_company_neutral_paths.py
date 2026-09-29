"""The copied sieving guards must work for any company name."""
from __future__ import annotations

import importlib
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
SOURCE = PROJECT / "sieving" / "src" / "json_extractor"


class CompanyNeutralPathTests(unittest.TestCase):
    @staticmethod
    def _snapshot(folder: Path) -> dict[str, tuple[bytes, int]]:
        return {
            path.relative_to(folder).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in folder.rglob("*") if path.is_file()
        }

    def test_two_company_names_with_and_without_sibling(self) -> None:
        for index, (company, has_sibling) in enumerate((
            ("Čista Tvrtka", True), ("Zeleni Pogon", False),
        )):
            with self.subTest(company=company, has_sibling=has_sibling):
                with tempfile.TemporaryDirectory(prefix="neutral-sieving-") as temp:
                    project = Path(temp) / company
                    package = project / "sieving" / "src" / "json_extractor"
                    io_package = package / "io"
                    io_package.mkdir(parents=True)
                    schemas = project / "schemas"
                    schemas.mkdir()
                    for name in ("config.py", "contract.py"):
                        shutil.copyfile(SOURCE / name, package / name)
                    shutil.copyfile(SOURCE / "io" / "_paths.py", io_package / "_paths.py")
                    for name in ("sieving_contract.yml", "app_b_taxonomy.yml"):
                        shutil.copyfile(PROJECT / "schemas" / name, schemas / name)

                    sibling = project.parent / "Other Audit"
                    if has_sibling:
                        sibling.mkdir()
                        (sibling / "marker.txt").write_text("unchanged", encoding="utf-8")
                        before = self._snapshot(sibling)

                    prefix = f"neutral_sieving_fixture_{index}"
                    fixture = types.ModuleType(prefix)
                    fixture.__path__ = [str(package)]
                    sys.modules[prefix] = fixture
                    io_fixture = types.ModuleType(prefix + ".io")
                    io_fixture.__path__ = [str(io_package)]
                    sys.modules[io_fixture.__name__] = io_fixture
                    try:
                        config = importlib.import_module(prefix + ".config")
                        paths = importlib.import_module(prefix + ".io._paths")
                        local = project / "sieving" / "DATA" / "made-up.json"
                        self.assertEqual(config.Config().data_dir, project / "sieving" / "DATA")
                        self.assertEqual(paths.local_io_path(local), local)
                        self.assertEqual(paths.local_io_path(project), project)

                        nested = project / "Other Audit" / "sieving" / "DATA"
                        for field in ("data_dir", "config_dir"):
                            with self.assertRaises(ValueError):
                                config.Config(**{field: nested})
                        with self.assertRaises(ValueError):
                            paths.local_io_path(nested / "made-up.json")
                        with self.assertRaises(ValueError):
                            paths.local_io_path(sibling / "marker.txt")
                        self.assertFalse(nested.exists())
                        if has_sibling:
                            self.assertEqual(self._snapshot(sibling), before)
                        else:
                            self.assertFalse(sibling.exists())
                    finally:
                        for name in tuple(sys.modules):
                            if name == prefix or name.startswith(prefix + "."):
                                del sys.modules[name]


if __name__ == "__main__":
    unittest.main()
