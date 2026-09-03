"""EA0.6 contracts for the isolated WikiEnconet Conda environment."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import yaml


ENCONET = Path(__file__).resolve().parents[1]
ENVIRONMENT_SPEC = ENCONET / "environment.yml"
REQUIREMENTS = ENCONET / "sieving" / "requirements.txt"
CONDA_PREFIX = Path(r"C:\xPY\vEnv\WikiEnconet")
CONDA_PYTHON = CONDA_PREFIX / "python.exe"
MODULE_BY_DISTRIBUTION = {
    "pandas": "pandas",
    "openpyxl": "openpyxl",
    "typer": "typer",
    "rich": "rich",
    "PyYAML": "yaml",
    "pytest": "pytest",
    "pytest-cov": "pytest_cov",
    "playwright": "playwright",
}


def _requirement_pins() -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            distribution, version = value.split("==", maxsplit=1)
            pins[distribution] = version
    return pins


def _inside(path: str, parent: Path) -> bool:
    normalized_path = os.path.normcase(str(Path(path).resolve()))
    normalized_parent = os.path.normcase(str(parent.resolve()))
    return os.path.commonpath((normalized_path, normalized_parent)) == normalized_parent


def test_environment_spec_matches_controlled_dependency_pins():
    assert ENVIRONMENT_SPEC.is_file(), "repository-controlled environment.yml is missing"
    specification = yaml.safe_load(ENVIRONMENT_SPEC.read_text(encoding="utf-8"))
    dependencies = specification["dependencies"]
    assert "python=3.13" in dependencies
    assert "pip=26.2.1" in dependencies
    pip_section = next(row["pip"] for row in dependencies if isinstance(row, dict) and "pip" in row)
    declared = dict(value.split("==", maxsplit=1) for value in pip_section)
    assert declared == _requirement_pins()


def test_target_environment_is_isolated_and_versions_are_exact():
    probe = """
import importlib.metadata as metadata
import importlib.util
import json
import site
import sys

modules = json.loads(sys.argv[1])
print(json.dumps({
    "executable": sys.executable,
    "prefix": sys.prefix,
    "enable_user_site": site.ENABLE_USER_SITE,
    "versions": {name: metadata.version(name) for name in modules},
    "origins": {name: importlib.util.find_spec(module).origin for name, module in modules.items()},
}, sort_keys=True))
"""
    completed = subprocess.run(
        [str(CONDA_PYTHON), "-c", probe, json.dumps(MODULE_BY_DISTRIBUTION)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    details = json.loads(completed.stdout)
    assert Path(details["executable"]).resolve() == CONDA_PYTHON.resolve()
    assert Path(details["prefix"]).resolve() == CONDA_PREFIX.resolve()
    assert details["versions"] == _requirement_pins()
    assert all(_inside(origin, CONDA_PREFIX) for origin in details["origins"].values())
