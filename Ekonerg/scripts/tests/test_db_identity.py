"""The copied database helper must use only its own ID contract."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


PROJECT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT / "schemas" / "id_patterns.yml"


def _copy_project(root: Path) -> None:
    (root / "scripts").mkdir(parents=True)
    (root / "schemas").mkdir()
    for name in ("db_util.py", "project_paths.py"):
        shutil.copyfile(PROJECT / "scripts" / name, root / "scripts" / name)
    shutil.copyfile(CONTRACT, root / "schemas" / "id_patterns.yml")


def _run(root: Path, code: str, *, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "scripts")
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, "-B", "-c", code], cwd=cwd, env=env,
        capture_output=True, text=True, check=False,
    )


def test_id_contract_examples_and_invalid_values() -> None:
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    required = {"doc_id", "chunk_id", "quote_id", "crumb_id", "requirement_id",
                "evaluation_id", "gap_id", "finding_id", "action_id", "run_id",
                "dashboard_id"}
    assert required == set(data["patterns"])
    for name, spec in data["patterns"].items():
        pattern = re.compile(spec["regex"])
        assert pattern.fullmatch(spec["example"]), name
        assert pattern.fullmatch(spec["example"] + "-OTHER") is None, name
    assert "Enconet" not in CONTRACT.read_text(encoding="utf-8")


@pytest.mark.parametrize(("company_name", "with_sibling"), [
    ("Audit Beta with spaces", False),
    ("Ekonerg ogled Čakovec", True),
])
def test_copied_db_helper_uses_only_local_patterns(
    tmp_path: Path, company_name: str, with_sibling: bool,
) -> None:
    root = tmp_path / company_name
    _copy_project(root)
    sibling = tmp_path / "Enconet"
    if with_sibling:
        sibling.mkdir()
        marker = sibling / "do-not-touch.txt"
        marker.write_bytes(b"other company")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
    code = """
from pathlib import Path
import db_util
root = Path(db_util.__file__).resolve().parents[1]
assert db_util.DEFAULT_DB == root / 'db' / 'nqa_audit.sqlite'
assert db_util.id_patterns()['doc_id'].fullmatch('DOC-0001')
assert not db_util.id_patterns()['doc_id'].fullmatch('DOC-EKONERG-0001')
(root / 'db').mkdir()
with db_util.connect(root / 'db' / 'test.sqlite') as conn:
    conn.execute('CREATE TABLE documents (doc_id TEXT PRIMARY KEY)')
    db_util.insert(conn, 'documents', {'doc_id': 'DOC-0001'})
    try:
        db_util.insert(conn, 'documents', {'doc_id': 'DOC-ENCONET-0002'})
    except ValueError as exc:
        assert 'invalid doc_id' in str(exc)
    else:
        raise AssertionError('foreign company ID was accepted')
    assert conn.execute('SELECT count(*) FROM documents').fetchone()[0] == 1
"""
    result = _run(root, code, cwd=sibling if with_sibling else tmp_path)
    assert result.returncode == 0, result.stderr
    assert (root / "db" / "test.sqlite").is_file()
    if with_sibling:
        assert (marker.read_bytes(), marker.stat().st_mtime_ns) == before
        assert sorted(path.name for path in sibling.iterdir()) == ["do-not-touch.txt"]


def test_copied_db_helper_rejects_foreign_database_path(tmp_path: Path) -> None:
    root = tmp_path / "Ekonerg ogled Čakovec"
    sibling = tmp_path / "Enconet"
    sibling.mkdir()
    _copy_project(root)
    code = """
from pathlib import Path
import db_util
foreign = Path(db_util.__file__).resolve().parents[2] / 'Enconet' / 'foreign.sqlite'
try:
    db_util.connect(foreign)
except ValueError as exc:
    assert 'local to project' in str(exc)
else:
    raise AssertionError('foreign DB path was accepted')
"""
    result = _run(root, code, cwd=sibling)
    assert result.returncode == 0, result.stderr
    assert list(sibling.iterdir()) == []
