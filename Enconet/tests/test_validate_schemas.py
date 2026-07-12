"""EPIC1 negative-path tests for the schema-contract validator."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]


def _sandbox(tmp_path: Path) -> Path:
    root = tmp_path / "Enconet"
    shutil.copytree(ENCONET / "schemas", root / "schemas")
    (root / "scripts").mkdir(parents=True)
    shutil.copy2(ENCONET / "scripts" / "validate_schemas.py", root / "scripts")
    shutil.copy2(ENCONET / "project-state.yml", root)
    (root / "manifests").mkdir()
    (root / "manifests" / "validation_runs.csv").write_text(
        "run_utc,validator,phase,result,exit_code,details\n", encoding="utf-8"
    )
    return root


def _run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_schemas.py")],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )


def test_validator_rejects_taxonomy_runtime_divergence(tmp_path: Path):
    root = _sandbox(tmp_path)
    contract = root / "schemas" / "sieving_contract.yml"
    text = contract.read_text(encoding="utf-8")
    contract.write_text(text.replace(
        "{\n", '{\n  "criteria": [{"criterion_id": "APP_B_I", '
        '"criterion_name": "Divergent Organization"}],\n', 1
    ), encoding="utf-8")

    result = _run(root)

    assert result.returncode == 1
    assert "must not re-declare app_b_taxonomy criteria" in result.stdout


def test_validator_rejects_scoring_weight_gap(tmp_path: Path):
    root = _sandbox(tmp_path)
    scoring = root / "schemas" / "scoring_model.yml"
    text = scoring.read_text(encoding="utf-8")
    scoring.write_text(text.replace("  fully: 1.00\n", "", 1), encoding="utf-8")

    result = _run(root)

    assert result.returncode == 1
    assert "rating_weights keys must be exactly" in result.stdout
    assert "weight for 'fully'" in result.stdout
