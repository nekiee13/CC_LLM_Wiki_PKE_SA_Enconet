"""Only a verified unstarted scaffold may be upgraded; history is retained."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import os
import subprocess

import pytest

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    import framework_release
    import prepare_vendor
    import prepare_framework_release_v4
    for name in ("v2",):
        shutil.copytree(TEMPLATE / "framework" / name, tmp_path / "framework" / name)
    prepare_framework_release_v4.build(tmp_path / "framework/v4")
    monkeypatch.setattr(framework_release, "ROOT", tmp_path)
    monkeypatch.setattr(prepare_vendor, "WORKSPACE", tmp_path)
    import upgrade_vendor_v4
    monkeypatch.setattr(upgrade_vendor_v4, "WORKSPACE", tmp_path)
    return tmp_path


def files(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


@pytest.mark.parametrize("name", ["Atlas Engineering", "Žuti dobavljač"])
def test_preview_apply_retry_undo_and_sibling_isolation(workspace, name):
    import prepare_vendor
    import upgrade_vendor_v4 as upgrade
    target = workspace / name
    prepare_vendor.setup(target, name, "old-v2", release="v2")
    (target / "incoming/owner.md").write_bytes(b"future intake, not registered")
    sibling = workspace / "Other Supplier"
    sibling.mkdir()
    (sibling / "owner.md").write_bytes(b"untouched")
    before, other = files(target), files(sibling)
    plan = upgrade.preview(target)
    assert not plan["blockers"]
    assert before == files(target)
    result = upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")
    assert result["state"] == "complete"
    assert json.loads((target / "framework-company.json").read_text(encoding="utf-8"))["framework_version"] == "4.0.0"
    assert not (target / "benchmarks").exists()
    assert not (target / "manifests").exists()
    assert not (target / ".bootstrap").exists()
    assert (target / "incoming/owner.md").read_bytes() == b"future intake, not registered"
    assert not (target / "db/nqa_audit.sqlite").exists()
    repeat_before = files(target)
    assert upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")["state"] == "complete"
    assert repeat_before == files(target)
    assert other == files(sibling)
    upgrade.undo(plan, "v4-test")
    for path, digest in before.items():
        assert files(target)[path] == digest
    assert other == files(sibling)


def test_owner_edit_blocks_before_any_write(workspace):
    import prepare_vendor
    import upgrade_vendor_v4 as upgrade
    target = workspace / "Edited Supplier"
    prepare_vendor.setup(target, target.name, "old-v2", release="v2")
    (target / "scripts/init_db.py").write_bytes(b"owner edit")
    before = files(target)
    plan = upgrade.preview(target)
    assert plan["blockers"]
    with pytest.raises(ValueError, match="blocked"):
        upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")
    assert before == files(target)


def test_stale_plan_and_live_database_are_refused(workspace):
    import prepare_vendor
    import upgrade_vendor_v4 as upgrade
    target = workspace / "Stale Supplier"
    prepare_vendor.setup(target, target.name, "old-v2", release="v2")
    plan = upgrade.preview(target)
    (target / "incoming/new.md").write_bytes(b"new owner input")
    before = files(target)
    with pytest.raises(ValueError, match="changed"):
        upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")
    assert before == files(target)
    (target / "db/nqa_audit.sqlite").write_bytes(b"live audit")
    assert upgrade.preview(target)["blockers"]


def test_tampered_new_file_blocks_undo(workspace):
    import prepare_vendor
    import upgrade_vendor_v4 as upgrade
    target = workspace / "Tampered Supplier"
    prepare_vendor.setup(target, target.name, "old-v2", release="v2")
    plan = upgrade.preview(target)
    upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")
    (target / "scripts/init_db.py").write_bytes(b"owner changed after upgrade")
    before = files(target)
    with pytest.raises(ValueError, match="changed"):
        upgrade.undo(plan, "v4-test")
    assert before == files(target)


def test_git_policy_cannot_normalize_retained_crlf_original(workspace):
    import prepare_vendor
    import upgrade_vendor_v4 as upgrade
    target = workspace / "CRLF Supplier"
    prepare_vendor.setup(target, target.name, "old-v2", release="v2")
    original = target / "scripts/init_db.py"
    body = original.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    original.write_bytes(body)
    plan = upgrade.preview(target)
    assert not plan["blockers"]
    result = upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")
    history = Path(result["journal"]).parent / "original"
    assert (history / "scripts/init_db.py").read_bytes() == body
    assert (history / ".gitattributes.record").is_file()
    assert not (history / ".gitattributes").exists()
    attrs = subprocess.check_output(
        ["git", "-C", str(target), "check-attr", "text", "--", str(history / "scripts/init_db.py")], text=True)
    assert attrs.rstrip().endswith("text: unset")
    upgrade.undo(plan, "v4-test")
    assert original.read_bytes() == body


@pytest.mark.parametrize("recovery", ["retry", "undo"])
def test_interrupted_upgrade_can_retry_or_restore(workspace, monkeypatch, recovery):
    import prepare_vendor
    import upgrade_vendor_v4 as upgrade
    target = workspace / "Interrupted Supplier"
    prepare_vendor.setup(target, target.name, "old-v2", release="v2")
    before = files(target)
    plan = upgrade.preview(target)
    native_move, calls = upgrade.move, 0
    def interrupted(source, destination):
        nonlocal calls
        calls += 1
        if calls == 3:
            raise OSError("simulated interrupted move")
        return native_move(source, destination)
    monkeypatch.setattr(upgrade, "move", interrupted)
    with pytest.raises(OSError, match="interrupted"):
        upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")
    monkeypatch.setattr(upgrade, "move", native_move)
    if recovery == "retry":
        assert upgrade.apply(plan, "v4-test", authority="OWNER-TEST-ONLY")["state"] == "complete"
    else:
        assert upgrade.undo(plan, "v4-test")["state"] == "undone"
        for path, digest in before.items():
            assert files(target)[path] == digest


@pytest.mark.parametrize("name", ["Atlas Engineering", "Žuti dobavljač"])
@pytest.mark.parametrize("sibling", [False, True])
def test_released_v4_full_pipeline_and_standalone_dashboards(workspace, name, sibling):
    import prepare_vendor
    from test_framework_pipeline_v4 import fixture_runner
    target = workspace / name
    prepare_vendor.setup(target, name, "new-v4", release="v4")
    other = workspace / "Other Supplier"
    if sibling:
        other.mkdir()
        (other / "owner.md").write_bytes(b"not this audit")
    before = files(other) if sibling else None
    runner = workspace / "synthetic-released-v4.py"
    runner.write_text(fixture_runner(), encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", str(runner), str(target)],
                            cwd=workspace, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=240,
                            env={**os.environ, "PYTHONUTF8": "1",
                                 "PLAYWRIGHT_BROWSERS_PATH": r"C:\xPY\vEnv\WikiEnconet\pw-browsers"})
    assert result.returncode == 0, result.stdout + result.stderr
    record = json.loads((target / "work/validation/pipeline-verification.json").read_text(encoding="utf-8"))
    assert record["synthetic_only"] and record["passed"] and record["score"] == 97.2
    output = target / "outputs/RUN-20261010-03"
    assert (output / "dashboard_light.html").is_file()
    assert (output / "dashboard_dark.html").is_file()
    assert not (output / "index.html").exists()
    assert not (target / "outputs/candidates").exists()
    if sibling:
        assert files(other) == before
    else:
        assert not other.exists()
