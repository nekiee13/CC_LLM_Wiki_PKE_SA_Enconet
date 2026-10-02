"""Criteria seeding must be deterministic, local, and repeatable."""

from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[2]


def _copy_project(root: Path) -> None:
    (root / "scripts").mkdir(parents=True)
    (root / "db").mkdir()
    (root / "schemas").mkdir()
    for name in ("init_db.py", "seed_criteria.py", "db_util.py", "project_paths.py"):
        shutil.copyfile(PROJECT / "scripts" / name, root / "scripts" / name)
    shutil.copyfile(PROJECT / "db" / "schema.sql", root / "db" / "schema.sql")
    shutil.copyfile(PROJECT / "schemas" / "app_b_taxonomy.yml",
                    root / "schemas" / "app_b_taxonomy.yml")


def _run(root: Path, script: str, *, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, "-B", str(root / "scripts" / script)],
        cwd=cwd, env=env, capture_output=True, text=True, check=False,
    )


def test_seed_criteria_is_exactly_18_and_repeatable(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta with spaces ÄŒakovec"
    sibling = tmp_path / "Enconet"
    sibling.mkdir()
    marker = sibling / "marker.txt"
    marker.write_bytes(b"other-company")
    before_marker = (marker.read_bytes(), marker.stat().st_mtime_ns)
    _copy_project(root)

    initialized = _run(root, "init_db.py", cwd=sibling)
    assert initialized.returncode == 0, initialized.stderr
    first = _run(root, "seed_criteria.py", cwd=sibling)
    assert first.returncode == 0, first.stderr
    assert "18" in first.stdout

    db = root / "db" / "nqa_audit.sqlite"
    taxonomy = yaml.safe_load(
        (root / "schemas" / "app_b_taxonomy.yml").read_text(encoding="utf-8")
    )
    expected = [
        (item["criterion_id"], item["criterion_name"], item["description"])
        for item in taxonomy["criteria"]
    ]
    with sqlite3.connect(db) as conn:
        actual = conn.execute(
            "SELECT criterion_id, criterion_name, description "
            "FROM criteria ORDER BY rowid"
        ).fetchall()
    assert actual == expected
    before_db = (db.read_bytes(), db.stat().st_mtime_ns)

    second = _run(root, "seed_criteria.py", cwd=tmp_path)
    assert second.returncode == 0, second.stderr
    assert "preserved" in second.stdout
    assert (db.read_bytes(), db.stat().st_mtime_ns) == before_db
    assert (marker.read_bytes(), marker.stat().st_mtime_ns) == before_marker


def test_seed_refuses_a_different_existing_taxonomy(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta"
    _copy_project(root)
    assert _run(root, "init_db.py", cwd=tmp_path).returncode == 0
    assert _run(root, "seed_criteria.py", cwd=tmp_path).returncode == 0
    taxonomy = root / "schemas" / "app_b_taxonomy.yml"
    text = taxonomy.read_text(encoding="utf-8")
    taxonomy.write_text(text.replace("Organization", "Changed organization", 1),
                        encoding="utf-8")
    refused = _run(root, "seed_criteria.py", cwd=tmp_path)
    assert refused.returncode != 0
    assert "mismatch" in refused.stderr.lower()
