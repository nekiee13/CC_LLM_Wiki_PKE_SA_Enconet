"""TDD tests for the guarded Ekonerg audit reset command."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reset_audit import NO_BACKUP_CONFIRMATION, ResetError, apply_plan, build_plan, write_plan


@pytest.fixture
def scratch() -> Path:
    base = Path(__file__).resolve().parents[3] / ".reset-test-work"
    base.mkdir(exist_ok=True)
    directory = base / uuid4().hex
    directory.mkdir()
    try:
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def _project(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "Ekonerg with spaces"
    (root / "incoming").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "db").mkdir()
    (root / "manifests").mkdir()
    (root / "wiki" / "evidence").mkdir(parents=True)
    (root / "sieving" / "runs").mkdir(parents=True)
    (root / "work" / "fast_audit").mkdir(parents=True)
    (root / "incoming" / "QMS ÄŒakovec.md").write_text("keep me\n", encoding="utf-8")
    (root / "scripts" / "framework.py").write_text("keep framework\n", encoding="utf-8")
    (root / "db" / "schema.sql").write_text("keep schema\n", encoding="utf-8")
    (root / "manifests" / "approvals.csv").write_text(
        "object_id,decision,date,reviewer,notes\nAUDIT-1,approved,2026-01-01,Ada,old\n",
        encoding="utf-8",
    )
    (root / "manifests" / "link_exceptions.csv").write_text(
        "crumb_id,quote_id,reason,approved_by,date\nC1,Q1,test,Ada,2026-01-01\n",
        encoding="utf-8",
    )
    (root / "manifests" / "validation_runs.csv").write_text(
        "run_utc,validator,phase,result,exit_code,details\n2026-01-01,v,p,PASS,0,old\n",
        encoding="utf-8",
    )
    (root / "db" / "nqa_audit.sqlite").write_bytes(b"audit data")
    (root / "work" / "fast_audit" / "draft.md").write_text("result\n", encoding="utf-8")
    (root / "sieving" / "runs" / "run.json").write_text("result\n", encoding="utf-8")
    (root / "wiki" / "evidence" / "matrix.json").write_text("result\n", encoding="utf-8")
    sibling = tmp_path / "Enconet"
    sibling.mkdir()
    (sibling / "keep.txt").write_text("other company\n", encoding="utf-8")
    return root, sibling


def test_preview_is_read_only_and_keeps_incoming_and_framework(scratch: Path) -> None:
    root, _ = _project(scratch)
    before = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}

    plan = build_plan(root)

    assert plan["summary"]["delete"] == 4
    assert plan["summary"]["truncate"] == 3
    assert (root / "incoming" / "QMS ÄŒakovec.md").read_bytes() == before[Path("incoming/QMS ÄŒakovec.md")]
    after = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
    assert after == before


def test_apply_requires_confirmation_and_external_backup(scratch: Path) -> None:
    root, _ = _project(scratch)
    plan_path = scratch / "reset-plan.json"
    backup_dir = scratch / "backups"
    plan = build_plan(root)
    write_plan(plan, plan_path)

    with pytest.raises(ResetError):
        apply_plan(plan_path, root, backup_dir, confirmation="WRONG")
    with pytest.raises(ResetError):
        apply_plan(plan_path, root, root / "backup-inside", confirmation="RESET-EKONERG")
    assert (root / "db" / "nqa_audit.sqlite").exists()


def test_apply_backs_up_then_removes_only_audit_state(scratch: Path) -> None:
    root, sibling = _project(scratch)
    plan_path = scratch / "reset-plan.json"
    backup_dir = scratch / "backups"
    write_plan(build_plan(root), plan_path)

    result = apply_plan(plan_path, root, backup_dir, confirmation="RESET-EKONERG")

    assert result["deleted"] == 4
    assert result["truncated"] == 3
    assert list(backup_dir.glob("ekonerg-reset-*.zip"))
    assert (root / "incoming" / "QMS ÄŒakovec.md").read_text(encoding="utf-8") == "keep me\n"
    assert (root / "scripts" / "framework.py").exists()
    assert (root / "db" / "schema.sql").exists()
    assert not (root / "db" / "nqa_audit.sqlite").exists()
    assert not (root / "work" / "fast_audit" / "draft.md").exists()
    assert not (root / "sieving" / "runs" / "run.json").exists()
    assert not (root / "wiki" / "evidence" / "matrix.json").exists()
    assert (root / "manifests" / "approvals.csv").read_text(encoding="utf-8") == (
        "object_id,decision,date,reviewer,notes\n"
    )
    assert (sibling / "keep.txt").read_text(encoding="utf-8") == "other company\n"


def test_apply_can_skip_local_backup_only_with_distinct_owner_token(scratch: Path) -> None:
    root, _ = _project(scratch)
    plan_path = scratch / "reset-plan.json"
    write_plan(build_plan(root), plan_path)

    with pytest.raises(ResetError, match=NO_BACKUP_CONFIRMATION):
        apply_plan(plan_path, root, None, confirmation="RESET-EKONERG")

    result = apply_plan(plan_path, root, None, confirmation=NO_BACKUP_CONFIRMATION)

    assert result["backup"] is None
    assert result["backup_status"] == "owner-waived"
    assert not (root / "db" / "nqa_audit.sqlite").exists()
    assert len(list((root / "incoming").iterdir())) == 1


def test_apply_refuses_plan_drift_before_deletion(scratch: Path) -> None:
    root, _ = _project(scratch)
    plan_path = scratch / "reset-plan.json"
    write_plan(build_plan(root), plan_path)
    (root / "work" / "fast_audit" / "draft.md").write_text("changed\n", encoding="utf-8")

    with pytest.raises(ResetError, match="changed since preview"):
        apply_plan(plan_path, root, scratch / "backups", confirmation="RESET-EKONERG")
    assert (root / "work" / "fast_audit" / "draft.md").read_text(encoding="utf-8") == "changed\n"


def test_plan_rejects_missing_incoming_or_redirected_candidate(scratch: Path) -> None:
    root, _ = _project(scratch)
    (root / "incoming").rename(root / "incoming-old")
    with pytest.raises(ResetError, match="incoming"):
        build_plan(root)

    second = scratch / "second"
    second.mkdir()
    root, _ = _project(second)
    redirected = scratch / "outside.txt"
    redirected.write_text("outside\n", encoding="utf-8")
    (root / "work" / "fast_audit" / "redirected.md").symlink_to(redirected)
    with pytest.raises(ResetError, match="redirected"):
        build_plan(root)
