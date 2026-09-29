"""Run creation must use only local prompt and source records."""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT = Path(__file__).resolve().parents[2]


def _copy_project(root: Path) -> None:
    for folder in ("scripts", "db", "schemas", "sieving/prompts"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    for name in ("sieve_run.py", "init_db.py", "db_util.py", "project_paths.py"):
        shutil.copyfile(PROJECT / "scripts" / name, root / "scripts" / name)
    for source, target in (
        ("db/schema.sql", "db/schema.sql"),
        ("schemas/id_patterns.yml", "schemas/id_patterns.yml"),
        ("sieving/prompts/active.yml", "sieving/prompts/active.yml"),
    ):
        shutil.copyfile(PROJECT / source, root / target)


def _run(root: Path, cwd: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, "-B", str(root / "scripts" / script), *args],
        cwd=cwd, env=env, capture_output=True, text=True, check=False,
    )


def _document(root: Path, *, side: str) -> None:
    with sqlite3.connect(root / "db" / "nqa_audit.sqlite") as conn:
        conn.execute(
            "INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) "
            "VALUES (?,?,?,?,?,?,?)",
            ("DOC-0001", "fictional.txt", "Fiction", "Synthetic", "xx", side, "a" * 64),
        )


def _activate_fake_prompt(root: Path, *, side: str, version: str) -> None:
    prompt_dir = root / "sieving" / "prompts"
    (prompt_dir / "active.yml").write_text(
        f"schema_version: '1.0'\nactive:\n  {side}: {version}\n", encoding="utf-8"
    )
    (prompt_dir / f"{version}.md").write_text("Synthetic test prompt only.\n", encoding="utf-8")


def _run_args(*, side: str, version: str, refs: list[dict] | None = None) -> list[str]:
    args = ["--run-id", "RUN-20260930-01", "--doc-id", "DOC-0001",
            "--prompt-version", version, "--document-side", side]
    for ref in refs or []:
        args += ["--authority-json", json.dumps(ref)]
    return args


def test_empty_active_registry_blocks_even_a_registered_document(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta with spaces"
    _copy_project(root)
    assert _run(root, tmp_path, "init_db.py").returncode == 0
    _document(root, side="DOCUMENT")
    result = _run(root, tmp_path, "sieve_run.py", *_run_args(
        side="DOCUMENT", version="candidate_document_v1"
    ))
    assert result.returncode != 0
    assert "active prompt" in result.stderr.lower()
    with sqlite3.connect(root / "db" / "nqa_audit.sqlite") as conn:
        assert conn.execute("SELECT count(*) FROM sieve_runs").fetchone()[0] == 0


@pytest.mark.parametrize(("name", "with_sibling"), [
    ("Audit Beta with spaces", False),
    ("Ekonerg ogled Čakovec", True),
])
def test_local_document_run_and_candidate_preserve_sibling(
    tmp_path: Path, name: str, with_sibling: bool,
) -> None:
    root = tmp_path / name
    sibling = tmp_path / "Enconet"
    sibling.mkdir()
    marker = sibling / "marker.txt"
    if with_sibling:
        marker.write_bytes(b"other company")
        before = (marker.read_bytes(), marker.stat().st_mtime_ns)
    _copy_project(root)
    assert _run(root, sibling, "init_db.py").returncode == 0
    _document(root, side="DOCUMENT")
    _activate_fake_prompt(root, side="DOCUMENT", version="candidate_document_v1")
    first = _run(root, sibling, "sieve_run.py", *_run_args(
        side="DOCUMENT", version="candidate_document_v1"
    ))
    assert first.returncode == 0, first.stderr
    assert "generation=1" in first.stdout and "status=active" in first.stdout
    second = _run(root, sibling, "sieve_run.py", "--run-id", "RUN-20260930-02",
                  "--doc-id", "DOC-0001", "--prompt-version", "candidate_document_v1",
                  "--document-side", "DOCUMENT")
    assert second.returncode == 0, second.stderr
    assert "generation=2" in second.stdout and "status=candidate" in second.stdout
    assert "no-op tuning" in second.stdout
    with sqlite3.connect(root / "db" / "nqa_audit.sqlite") as conn:
        assert conn.execute("SELECT count(*) FROM sieve_runs WHERE is_active=1").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM sieve_runs").fetchone()[0] == 2
    assert not (root / "Enconet").exists()
    if with_sibling:
        assert (marker.read_bytes(), marker.stat().st_mtime_ns) == before
        assert sorted(path.name for path in sibling.iterdir()) == ["marker.txt"]
    else:
        assert list(sibling.iterdir()) == []


def test_rule_run_requires_matching_registered_source(tmp_path: Path) -> None:
    root = tmp_path / "Ekonerg ogled Čakovec"
    _copy_project(root)
    assert _run(root, tmp_path, "init_db.py").returncode == 0
    _document(root, side="RULE")
    _activate_fake_prompt(root, side="RULE", version="candidate_rule_v1")
    ref = {"authority_role": "GOVERNING", "source_code": "DEMO_RULE",
           "source_locator": "invented-1", "applicability": "APPLICABLE"}
    missing = _run(root, tmp_path, "sieve_run.py", *_run_args(
        side="RULE", version="candidate_rule_v1", refs=[ref]
    ))
    assert missing.returncode != 0
    assert "registered" in missing.stderr.lower()
    with sqlite3.connect(root / "db" / "nqa_audit.sqlite") as conn:
        conn.execute(
            "INSERT INTO approved_sources(source_code,authority_role,edition,source_sha256,"
            "approval_ref,approved_by,approved_date) VALUES (?,?,?,?,?,?,?)",
            ("DEMO_RULE", "GOVERNING", "test-only", "b" * 64,
             "TEST-ONLY", "Synthetic", "2026-09-30"),
        )
    wrong_role = dict(ref, authority_role="INTERPRETIVE")
    rejected = _run(root, tmp_path, "sieve_run.py", *_run_args(
        side="RULE", version="candidate_rule_v1", refs=[wrong_role]
    ))
    assert rejected.returncode != 0
    bad_locator = dict(ref, source_locator=" ")
    rejected = _run(root, tmp_path, "sieve_run.py", *_run_args(
        side="RULE", version="candidate_rule_v1", refs=[bad_locator]
    ))
    assert rejected.returncode != 0
    malformed_role = dict(ref, authority_role=["GOVERNING"])
    rejected = _run(root, tmp_path, "sieve_run.py", *_run_args(
        side="RULE", version="candidate_rule_v1", refs=[malformed_role]
    ))
    assert rejected.returncode != 0
    assert "Traceback" not in rejected.stderr
    with sqlite3.connect(root / "db" / "nqa_audit.sqlite") as conn:
        assert conn.execute("SELECT count(*) FROM sieve_runs").fetchone()[0] == 0
    good = _run(root, tmp_path, "sieve_run.py", *_run_args(
        side="RULE", version="candidate_rule_v1", refs=[ref]
    ))
    assert good.returncode == 0, good.stderr
    with sqlite3.connect(root / "db" / "nqa_audit.sqlite") as conn:
        assert conn.execute("SELECT source_rule FROM sieve_runs").fetchone()[0] == "DEMO_RULE"
        assert conn.execute("SELECT source_code FROM sieve_run_authorities").fetchone()[0] == "DEMO_RULE"


def test_foreign_database_path_is_refused_without_writing(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta with spaces"
    sibling = tmp_path / "Enconet"
    sibling.mkdir()
    _copy_project(root)
    _activate_fake_prompt(root, side="DOCUMENT", version="candidate_document_v1")
    result = _run(root, sibling, "sieve_run.py", "--db", str(sibling / "foreign.sqlite"),
                  *_run_args(side="DOCUMENT", version="candidate_document_v1"))
    assert result.returncode != 0
    assert list(sibling.iterdir()) == []
    assert not (root / "db" / "nqa_audit.sqlite").exists()


def test_new_candidate_prompt_needs_a_local_history_row(tmp_path: Path) -> None:
    root = tmp_path / "Audit Beta with spaces"
    _copy_project(root)
    assert _run(root, tmp_path, "init_db.py").returncode == 0
    _document(root, side="DOCUMENT")
    _activate_fake_prompt(root, side="DOCUMENT", version="candidate_document_v1")
    assert _run(root, tmp_path, "sieve_run.py", *_run_args(
        side="DOCUMENT", version="candidate_document_v1"
    )).returncode == 0
    prompt_dir = root / "sieving" / "prompts"
    (prompt_dir / "candidate_document_v2.md").write_text(
        "Synthetic revised prompt.\n", encoding="utf-8"
    )
    args = ["--run-id", "RUN-20260930-02", "--doc-id", "DOC-0001",
            "--prompt-version", "candidate_document_v2", "--document-side", "DOCUMENT"]
    missing = _run(root, tmp_path, "sieve_run.py", *args)
    assert missing.returncode != 0
    (prompt_dir / "CHANGELOG.md").write_text(
        "| Candidate | Side | State |\n|---|---|---|\n"
        "| `candidate_document_v2` | DOCUMENT | synthetic test |\n", encoding="utf-8"
    )
    candidate = _run(root, tmp_path, "sieve_run.py", *args)
    assert candidate.returncode == 0, candidate.stderr
    assert "generation=2" in candidate.stdout and "status=candidate" in candidate.stdout
