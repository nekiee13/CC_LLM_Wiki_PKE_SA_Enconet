"""EA2.1 tests for safe evidence-bundle embedding in the offline dashboard."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import evidence_access_policy  # noqa: E402
import generate_dashboard  # noqa: E402
import validate_dashboard  # noqa: E402
import validate_evidence_bundle  # noqa: E402


PACKAGE_PATH = ENCONET / "outputs" / "enconet_appendix_b_evaluation_package.json"
DASHBOARD_DATA_PATH = ENCONET / "outputs" / "enconet_appendix_b_dashboard_data.json"
BUNDLE_PATH = (
    ENCONET / "outputs" / "candidates" / "evidence_access" /
    "RUN-20260728-01" / "evidence_bundle.json"
)
RUN_ID = "RUN-20260728-01"
EVIDENCE_BLOCK = re.compile(
    r'<script id="evidence-bundle" type="application/json" '
    r'data-sha256="([0-9a-f]{64})">(.*?)</script>',
    re.DOTALL,
)


@pytest.fixture(scope="module")
def production_inputs() -> tuple[dict, dict, dict]:
    return tuple(
        json.loads(path.read_text(encoding="utf-8"))
        for path in (PACKAGE_PATH, DASHBOARD_DATA_PATH, BUNDLE_PATH)
    )


def _embedded(html: str) -> tuple[str, dict]:
    matches = EVIDENCE_BLOCK.findall(html)
    assert len(matches) == 1
    digest, payload = matches[0]
    return digest, json.loads(payload)


def test_renderer_embeds_one_validated_bundle_with_matching_hash(production_inputs):
    package, data, bundle = production_inputs
    html = generate_dashboard.render(data, evidence_bundle=bundle)
    digest, embedded = _embedded(html)
    expected_digest = hashlib.sha256(
        validate_evidence_bundle.canonical_bytes(bundle)
    ).hexdigest()
    assert embedded == bundle
    assert digest == expected_digest
    assert html.count('id="evidence-bundle"') == 1
    assert validate_dashboard.validate(
        package, data, html, evidence_bundle=bundle
    ) == []


def test_embedded_payload_escapes_script_html_controls_and_preserves_unicode(
    production_inputs,
):
    _package, data, source_bundle = production_inputs
    bundle = copy.deepcopy(source_bundle)
    hostile = "</script><img src=x onerror=alert(1)> & \x00 čćžšđ Œuvre"
    bundle["chunks"][0]["text"] = hostile
    html = generate_dashboard.render(data, evidence_bundle=bundle)
    digest, embedded = _embedded(html)
    assert "</script><img" not in html
    assert "<img src=x" not in html
    assert "\\u003c/script>" in html
    assert "\\u0000" in html
    assert embedded["chunks"][0]["text"] == hostile
    assert "čćžšđ Œuvre" in html
    assert digest == hashlib.sha256(
        validate_evidence_bundle.canonical_bytes(bundle)
    ).hexdigest()


def test_package_and_bundle_hashes_are_visible_in_artifact_metadata(production_inputs):
    _package, data, bundle = production_inputs
    html = generate_dashboard.render(data, evidence_bundle=bundle)
    bundle_hash = hashlib.sha256(
        validate_evidence_bundle.canonical_bytes(bundle)
    ).hexdigest()
    package_hash = bundle["lineage"]["package"]["sha256"]
    assert 'id="artifact-metadata"' in html
    assert 'id="metadata-package-hash"' in html
    assert 'id="metadata-bundle-hash"' in html
    assert package_hash in html
    assert bundle_hash in html


def test_validator_rejects_tampered_embedded_payload_or_hash(production_inputs):
    package, data, bundle = production_inputs
    html = generate_dashboard.render(data, evidence_bundle=bundle)
    tampered_payload = html.replace(bundle["chunks"][0]["chunk_id"], "CHUNK-DOC-9999-9999", 1)
    assert "embedded evidence bundle mismatch" in validate_dashboard.validate(
        package, data, tampered_payload, evidence_bundle=bundle
    )
    digest = hashlib.sha256(validate_evidence_bundle.canonical_bytes(bundle)).hexdigest()
    tampered_hash = html.replace(digest, "0" * 64, 1)
    assert "embedded evidence bundle hash mismatch" in validate_dashboard.validate(
        package, data, tampered_hash, evidence_bundle=bundle
    )


def test_bundle_must_be_valid_and_match_dashboard_run_language_and_supplier(
    production_inputs,
):
    _package, data, source_bundle = production_inputs
    for field, value in (
        ("run_id", "RUN-20260903-99"),
        ("deliverable_language", "en"),
        ("supplier", "other"),
    ):
        bundle = copy.deepcopy(source_bundle)
        bundle["metadata"][field] = value
        with pytest.raises(ValueError, match="evidence bundle/dashboard mismatch"):
            generate_dashboard.render(data, evidence_bundle=bundle)
    bundle = copy.deepcopy(source_bundle)
    bundle["chunks"][0]["viewer_target"] = "#wrong"
    with pytest.raises(ValueError, match="invalid evidence bundle"):
        generate_dashboard.render(data, evidence_bundle=bundle)


def test_evidence_integration_adds_no_network_dependency(production_inputs):
    _package, data, bundle = production_inputs
    html = generate_dashboard.render(data, evidence_bundle=bundle)
    assert not re.search(
        r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)\s*=\s*["\']https?://',
        html,
        re.IGNORECASE,
    )
    assert "fetch(" not in html
    assert "XMLHttpRequest" not in html


def test_cli_writes_only_one_candidate_dashboard(monkeypatch, tmp_path: Path, capsys):
    candidate_root = tmp_path / "candidates" / "evidence_access"
    monkeypatch.setattr(evidence_access_policy, "CANDIDATE_ROOT", candidate_root)
    target = candidate_root / RUN_ID / "enconet_appendix_b_dashboard.html"
    result = generate_dashboard.main([
        str(PACKAGE_PATH),
        str(DASHBOARD_DATA_PATH),
        "--evidence-bundle", str(BUNDLE_PATH),
        "--output", str(target),
    ])
    assert result == 0
    assert target.is_file()
    assert "evidence bundle embedded" in capsys.readouterr().out
    assert len(list(candidate_root.rglob("*.html"))) == 1
    assert _embedded(target.read_text(encoding="utf-8"))[1]["metadata"]["run_id"] == RUN_ID


def test_cli_rejects_published_or_wrong_run_output_before_writing(
    monkeypatch, tmp_path: Path, production_inputs
):
    _package, _data, bundle = production_inputs
    candidate_root = tmp_path / "candidates" / "evidence_access"
    monkeypatch.setattr(evidence_access_policy, "CANDIDATE_ROOT", candidate_root)
    protected = ENCONET / "outputs" / "enconet_appendix_b_dashboard.html"
    original = protected.read_bytes()
    assert generate_dashboard.main([
        str(PACKAGE_PATH), str(DASHBOARD_DATA_PATH),
        "--evidence-bundle", str(BUNDLE_PATH), "--output", str(protected),
    ]) == 1
    assert protected.read_bytes() == original

    wrong_run = candidate_root / "RUN-20260903-99" / "dashboard.html"
    assert bundle["metadata"]["run_id"] == RUN_ID
    assert generate_dashboard.main([
        str(PACKAGE_PATH), str(DASHBOARD_DATA_PATH),
        "--evidence-bundle", str(BUNDLE_PATH), "--output", str(wrong_run),
    ]) == 1
    assert not wrong_run.exists()


def test_cli_rejects_package_bytes_that_do_not_match_bundle_lineage(
    monkeypatch, tmp_path: Path, production_inputs
):
    package, _data, _bundle = production_inputs
    candidate_root = tmp_path / "candidates" / "evidence_access"
    monkeypatch.setattr(evidence_access_policy, "CANDIDATE_ROOT", candidate_root)
    reformatted_package = tmp_path / "reformatted-package.json"
    reformatted_package.write_text(json.dumps(package), encoding="utf-8")
    target = candidate_root / RUN_ID / "dashboard.html"
    assert generate_dashboard.main([
        str(reformatted_package), str(DASHBOARD_DATA_PATH),
        "--evidence-bundle", str(BUNDLE_PATH), "--output", str(target),
    ]) == 1
    assert not target.exists()
