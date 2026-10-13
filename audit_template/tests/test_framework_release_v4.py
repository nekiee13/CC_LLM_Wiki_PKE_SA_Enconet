"""CU-4 clean release: no company evidence or inherited decisions."""
import hashlib
import json
from pathlib import Path
import sys
import subprocess

import pytest
import yaml

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))


def test_release_build_is_deterministic_and_immutable(tmp_path):
    import prepare_framework_release_v4 as builder
    from bootstrap_sieving import load_manifest
    from framework_release import spec
    first, second = tmp_path / "release1", tmp_path / "release2"
    builder.build(first)
    builder.build(second)
    assert (first / "manifest.json").read_bytes() == (second / "manifest.json").read_bytes()
    manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["template_version"] == "4.0.0"
    assert manifest["review_status"] == "deferred"
    assert not (first / "candidate-manifest.json").exists()
    assert "work/migrations/** -text" in (first / ".gitattributes").read_text(encoding="utf-8")
    for row in manifest["files"]:
        assert hashlib.sha256((first / row["path"]).read_bytes()).hexdigest() == row["sha256"]
        assert not row["path"].startswith(("raw/", "incoming/", "outputs/", "sieving/DATA/", ".claude/"))
    assert not (first / "db/nqa_audit.sqlite").exists()
    assert yaml.safe_load((first / "sieving/prompts/active.yml").read_text(encoding="utf-8"))["active"] == {}
    with pytest.raises(FileExistsError):
        builder.build(first)
    import framework_release
    original = framework_release.ROOT
    # Select the test release without changing the original frozen bundles.
    framework_release.ROOT = tmp_path
    try:
        (tmp_path / "framework").mkdir()
        first.rename(tmp_path / "framework/v4")
        selected = spec(release="v4")
        assert load_manifest(selected)["template_version"] == "4.0.0"
        assert selected.journal_home == "work/bootstrap"
    finally:
        framework_release.ROOT = original


@pytest.mark.parametrize("name", ["Atlas Engineering", "Žuti dobavljač"])
def test_fresh_v4_setup_has_local_code_and_no_inherited_approval(tmp_path, monkeypatch, name):
    import prepare_framework_release_v4 as builder
    import framework_release
    import prepare_vendor
    builder.build(tmp_path / "framework/v4")
    monkeypatch.setattr(framework_release, "ROOT", tmp_path)
    monkeypatch.setattr(prepare_vendor, "WORKSPACE", tmp_path)
    target = tmp_path / name
    sibling = tmp_path / "Other Supplier"
    sibling.mkdir()
    (sibling / "owner.md").write_bytes(b"preserved")
    preview = prepare_vendor.setup(target, name, release="v4")
    assert preview["mode"] == "preview" and not target.exists()
    result = prepare_vendor.setup(target, name, "test-v4-01", release="v4")
    assert Path(result["journal"]).is_relative_to(target / "work/bootstrap")
    assert json.loads((target / "project-layout.json").read_text(encoding="utf-8"))["layout"] == "v4"
    assert json.loads((target / "framework-company.json").read_text(encoding="utf-8"))["framework_version"] == "4.0.0"
    assert "FRAMEWORK_METHOD_V4.md" in (target / "AGENTS.md").read_text(encoding="utf-8")
    assert not (target / ".bootstrap").exists()
    assert not (target / "db/nqa_audit.sqlite").exists()
    assert yaml.safe_load((target / "sieving/prompts/active.yml").read_text(encoding="utf-8"))["active"] == {}
    assert (target / "incoming").is_dir()
    assert (sibling / "owner.md").read_bytes() == b"preserved"
    repeat = prepare_vendor.setup(target, name, "test-v4-02", release="v4")
    assert not repeat["created"]


def test_v4_rejects_additive_upgrade_mode():
    from framework_release import spec
    with pytest.raises(ValueError, match="clean release"):
        spec(upgrade=True, release="v4")


def test_prior_release_and_addon_payloads_are_unchanged():
    manifests = sorted(TEMPLATE.glob("*/v1/manifest.json"))
    manifests += [TEMPLATE / "framework" / name / "manifest.json" for name in ("v2", "v3", "upgrade-v2")]
    assert len(manifests) >= 20
    for path in manifests:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        for row in manifest["files"]:
            body = (path.parent / row["path"]).read_bytes()
            assert len(body) == row["bytes"]
            assert hashlib.sha256(body).hexdigest() == row["sha256"]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD", "--",
         *[str(path.parent.relative_to(TEMPLATE.parent)) for path in manifests]],
        cwd=TEMPLATE.parent, text=True)
    assert changed == ""
