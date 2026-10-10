"""First-cycle publication must never overwrite existing audit artifacts."""
import hashlib
import json
import sys
from types import SimpleNamespace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import publish_audit_release as release


def fixture(root):
    (root / "manifests").mkdir()
    (root / "manifests/approvals.csv").write_text(
        "object_id,decision,date,reviewer,notes\n"
        "G5-RUN-1,approved,2026-10-09,project-owner,report\n"
        "G6-RUN-1,approved,2026-10-09,project-owner,dashboard\n"
        "PUBLICATION-RUN-1,approved,2026-10-09,project-owner,deferred review\n",
        encoding="utf-8",
    )
    rows = []
    for name in ("report.md", "dashboard.html"):
        source = root / "candidate" / name
        source.parent.mkdir(exist_ok=True)
        source.write_bytes(name.encode())
        rows.append({"source": f"candidate/{name}", "destination": f"outputs/{name}",
                     "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    contract = {"schema_version": 1, "run_id": "RUN-1", "review_status": "deferred",
                "owner_exception": "PUBLICATION-RUN-1",
                "gate_approvals": ["G5-RUN-1", "G6-RUN-1"], "artifacts": rows,
                "result_manifest": "manifests/release.json"}
    path = root / "release.json"
    path.write_text(json.dumps(contract), encoding="utf-8")
    approvals = root / "manifests/approvals.csv"
    text = approvals.read_text(encoding="utf-8").replace(
        "project-owner,deferred review", f"project-owner,review deferred contract_sha256={release.fingerprint(contract)}")
    approvals.write_text(text, encoding="utf-8")
    return path, contract


def test_preview_writes_nothing_and_apply_keeps_exact_bytes(tmp_path):
    path, contract = fixture(tmp_path)
    before = sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*"))
    release.publish(path, root=tmp_path)
    assert before == sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*"))
    result = release.publish(path, root=tmp_path, execute=True, validator=lambda: None)
    assert result["review_status"] == "deferred"
    for row in contract["artifacts"]:
        assert (tmp_path / row["destination"]).read_bytes() == (tmp_path / row["source"]).read_bytes()
    with pytest.raises(release.ReleaseError, match="exists"):
        release.publish(path, root=tmp_path, execute=True, validator=lambda: None)


@pytest.mark.parametrize("defect", ["escape", "tamper", "unsigned", "duplicate", "existing"])
def test_invalid_plan_never_publishes(tmp_path, defect):
    path, contract = fixture(tmp_path)
    if defect == "escape":
        contract["artifacts"][0]["destination"] = "../other-company/report.md"
    elif defect == "tamper":
        (tmp_path / "candidate/report.md").write_bytes(b"changed")
    elif defect == "unsigned":
        contract["owner_exception"] = "MISSING"
    elif defect == "duplicate":
        contract["artifacts"][1]["destination"] = contract["artifacts"][0]["destination"]
    else:
        (tmp_path / "outputs").mkdir()
        (tmp_path / "outputs/report.md").write_bytes(b"existing")
    path.write_text(json.dumps(contract), encoding="utf-8")
    with pytest.raises(release.ReleaseError):
        release.publish(path, root=tmp_path, execute=True, validator=lambda: None)
    assert not (tmp_path / "outputs/dashboard.html").exists()
    assert not (tmp_path / "manifests/release.json").exists()


def test_validation_failure_rolls_back_only_own_files(tmp_path):
    path, contract = fixture(tmp_path)
    unrelated = tmp_path / "manifests/unrelated.txt"
    unrelated.write_bytes(b"keep")
    def fail():
        assert (tmp_path / "outputs/dashboard.html").is_file()
        raise ValueError("failed browser validation")
    with pytest.raises(release.ReleaseError, match="rolled back"):
        release.publish(path, root=tmp_path, execute=True, validator=fail)
    assert unrelated.read_bytes() == b"keep"
    assert all(not (tmp_path / row["destination"]).exists() for row in contract["artifacts"])
    assert not (tmp_path / "manifests/release.json").exists()


def test_execution_requires_validator(tmp_path):
    path, _ = fixture(tmp_path)
    with pytest.raises(release.ReleaseError, match="validator"):
        release.publish(path, root=tmp_path, execute=True)


def test_racing_destination_is_preserved(tmp_path):
    path, _ = fixture(tmp_path)
    calls = 0
    def racing_link(source, destination):
        nonlocal calls
        calls += 1
        if calls == 2:
            destination.write_bytes(b"other writer")
        release.os.link(source, destination)
    with pytest.raises(release.ReleaseError, match="rolled back"):
        release.publish(path, root=tmp_path, execute=True, validator=lambda: None, link=racing_link)
    assert not (tmp_path / "outputs/report.md").exists()
    assert (tmp_path / "outputs/dashboard.html").read_bytes() == b"other writer"


def test_destination_permissions_restored_before_validation_and_marker(tmp_path):
    path, contract = fixture(tmp_path)
    restored = []
    def permissions(target):
        assert target.is_file()
        restored.append(target.relative_to(tmp_path).as_posix())
    def validate():
        assert restored == [row["destination"] for row in contract["artifacts"]]
    release.publish(path, root=tmp_path, execute=True, validator=validate, permissions=permissions)
    assert restored[-1] == "manifests/release.json"


def test_marker_permission_failure_rolls_back_marker_and_payload(tmp_path):
    path, contract = fixture(tmp_path)
    def fail_marker(target):
        if target.name == "release.json":
            raise OSError("ACL restore failed")
    with pytest.raises(release.ReleaseError, match="rolled back"):
        release.publish(path, root=tmp_path, execute=True, validator=lambda: None, permissions=fail_marker)
    assert not (tmp_path / "manifests/release.json").exists()
    assert all(not (tmp_path / row["destination"]).exists() for row in contract["artifacts"])


def test_windows_acl_helper_resets_only_exact_file(monkeypatch, tmp_path):
    target = tmp_path / "dashboard.html"
    calls = []
    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stderr="")
    monkeypatch.setattr(release, "os", SimpleNamespace(name="nt"))
    monkeypatch.setattr(release.subprocess, "run", run)
    release.inherit_destination_permissions(target)
    assert calls == [["icacls", str(target), "/reset"]]


def test_windows_acl_helper_failure_is_not_ignored(monkeypatch, tmp_path):
    target = tmp_path / "dashboard.html"
    monkeypatch.setattr(release, "os", SimpleNamespace(name="nt"))
    monkeypatch.setattr(release.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=1, stderr="denied"))
    with pytest.raises(release.ReleaseError, match="ACL inheritance failed"):
        release.inherit_destination_permissions(target)


@pytest.mark.parametrize("company", ["QA Example", "Tvrtka Č"])
def test_native_publication_inherits_acl_and_preserves_sibling(tmp_path, company):
    root = tmp_path / company
    root.mkdir()
    sibling = tmp_path / "Another company.txt"
    sibling.write_bytes(b"unchanged")
    path, contract = fixture(root)
    release.publish(path, root=root, execute=True, validator=lambda: None)
    assert sibling.read_bytes() == b"unchanged"
    for row in contract["artifacts"]:
        target = root / row["destination"]
        assert target.read_bytes() == (root / row["source"]).read_bytes()
        if release.os.name == "nt":
            literal = str(target).replace("'", "''")
            command = ["powershell", "-NoProfile", "-Command",
                       f"if ((Get-Acl -LiteralPath '{literal}').AreAccessRulesProtected) {{ exit 1 }}"]
            assert release.subprocess.run(command, check=False).returncode == 0
