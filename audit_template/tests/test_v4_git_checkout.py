"""The workspace release must keep all installed hashes after Git checkout."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))


def test_complete_installed_payload_survives_autocrlf_checkout(tmp_path, monkeypatch):
    import prepare_vendor
    import framework_release
    monkeypatch.setattr(prepare_vendor, "WORKSPACE", tmp_path)
    target = tmp_path / "Žuti Supplier"
    prepare_vendor.setup(target, target.name, "checkout-test", release="v4")
    shutil.copyfile(TEMPLATE.parent / ".gitattributes", tmp_path / ".gitattributes")
    def git(*args):
        result = subprocess.run(["git", "-C", str(tmp_path), "-c", "core.autocrlf=true", *args],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert result.returncode == 0, result.stdout + result.stderr
    git("init", "--quiet")
    git("add", "--", ".gitattributes", target.name)
    checkout = tmp_path / "fresh-checkout"
    checkout.mkdir()
    git("checkout-index", "--all", "--prefix=" + checkout.as_posix() + "/")
    manifest = framework_release.load_manifest(framework_release.spec(release="v4"))
    for row in manifest["files"]:
        path = checkout / target.name / row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]
    for name, body in prepare_vendor.scaffold(target.name, release="v4").items():
        assert (checkout / target.name / name).read_bytes() == body, name
