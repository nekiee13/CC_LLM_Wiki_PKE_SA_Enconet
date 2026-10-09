"""Owner-approved capacity profile; no silent weakening of other limits."""
import copy
from pathlib import Path
import sys
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_dashboard
import build_review_package
import validate_evidence_bundle

PROFILE = ROOT / "schemas/evidence_access_budgets_v2.yml"

def test_profile_uses_explicit_owner_approval_and_preserves_other_limits():
    old = yaml.safe_load(generate_dashboard.EVIDENCE_BUDGETS.read_text(encoding="utf-8"))
    new = generate_dashboard.load_budget_profile(PROFILE)
    assert new["size_bytes"] == {"bundle":1048576,"viewer":1048576,"workspace":65536,"package_payload_total":2097152}
    assert all(new[k] == old[k] for k in ("projection_counts","performance_ms","security"))
    assert old["size_bytes"]["bundle"] == 524288

def test_profile_without_manifest_approval_fails_closed(tmp_path):
    data = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    data["approval"]["approval_ref"] = "EVIDENCE-SIZE-NOT-APPROVED"
    path = tmp_path / "profile.yml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(ValueError, match="approval"):
        generate_dashboard.load_budget_profile(path)

def test_profile_tampering_invalidates_approved_fingerprint(tmp_path):
    data = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    data["size_bytes"]["bundle"] *= 2
    path = tmp_path / "profile.yml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(ValueError, match="fingerprint"):
        generate_dashboard.load_budget_profile(path)

def test_explicit_profile_allows_larger_bundle_without_changing_legacy_fallback(monkeypatch, tmp_path):
    # Isolate size logic; real bundle schema/lineage is checked in integration.
    monkeypatch.setattr(validate_evidence_bundle, "validate", lambda _: [])
    state = tmp_path / "state.yml"
    state.write_text("phase: setup\n", encoding="utf-8")
    monkeypatch.setattr(generate_dashboard, "BUDGET_STATE", state)
    data = {"run_id":"RUN-20261008-17","supplier":"fixture","deliverable_language":"hr"}
    bundle = {"metadata":copy.deepcopy(data)}
    for name in ("documents","chunks","evaluations","crumbs","quotes","gaps","findings","actions"):
        bundle[name] = []
    bundle["chunks"] = [{"text":"a"*550000}]
    with pytest.raises(ValueError, match="size budget"):
        generate_dashboard._validate_bundle_for_dashboard(bundle, data)
    generate_dashboard._validate_bundle_for_dashboard(bundle, data, budget_profile=PROFILE)


def test_portable_repack_keeps_documentary_variant_and_legacy_default(monkeypatch):
    calls = []
    monkeypatch.setattr(build_review_package.generate_report, "render",
                        lambda package, **kw: calls.append(kw) or "rendered")
    source = '<!-- report-metadata: {"report_variant":"documentary"} -->'
    assert build_review_package.render_portable_report({}, source, "evidence_explorer.html") == "rendered"
    assert calls[-1]["documentary"] is True
    build_review_package.render_portable_report({}, '<!-- report-metadata: {} -->', "evidence_explorer.html")
    assert calls[-1].get("documentary", False) is False


def test_project_configuration_selects_approved_profile_and_rejects_escape(monkeypatch, tmp_path):
    assert generate_dashboard.configured_budget_profile() == PROFILE.resolve()
    assert generate_dashboard.load_budget_profile()["size_bytes"]["bundle"] == 1048576
    state = tmp_path / "state.yml"
    state.write_text("evidence_budget_profile: ../other-company/profile.yml\n", encoding="utf-8")
    monkeypatch.setattr(generate_dashboard, "BUDGET_STATE", state)
    with pytest.raises(ValueError, match="escapes"):
        generate_dashboard.configured_budget_profile()
