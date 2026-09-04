"""EA0.2 tests for offline architecture and controlled-output governance."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pytest
import yaml


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import evidence_access_policy as policy  # noqa: E402


ADR = ENCONET / "decisions" / "CX_ADR-0024-offline-evidence-explorer-and-candidate-output-policy.md"


def _adr_policy() -> dict:
    assert ADR.is_file(), "owner-approved EA0.2 ADR is missing"
    text = ADR.read_text(encoding="utf-8")
    match = re.search(r"<!-- evidence-access-policy\n(.*?)\n-->", text, re.DOTALL)
    assert match, "ADR-0024 machine-readable policy block is missing"
    return yaml.safe_load(match.group(1))


@pytest.mark.parametrize(
    "entrypoint",
    (
        "streamlit run app.py",
        "uvicorn evidence_app:app",
        "python -m flask run",
        "python -m http.server",
        "gunicorn evidence_app:app",
        "hypercorn evidence_app:app",
        "python evidence_server.py",
    ),
)
def test_offline_policy_rejects_streamlit_and_app_server_entrypoints(entrypoint: str):
    with pytest.raises(policy.PolicyError, match="ADR-0007"):
        policy.require_offline_entrypoint(entrypoint)


def test_candidate_writes_are_allowed_but_published_overwrite_requires_all_gates():
    candidate = policy.candidate_path(
        "RUN-20260728-01", "enconet_appendix_b_evaluation_report.md"
    )
    assert candidate == (
        ENCONET
        / "outputs"
        / "candidates"
        / "evidence_access"
        / "RUN-20260728-01"
        / "enconet_appendix_b_evaluation_report.md"
    )
    policy.require_output_target(candidate)

    published = ENCONET / "outputs" / "enconet_appendix_b_evaluation_report.md"
    with pytest.raises(policy.PolicyError, match="owner approval"):
        policy.require_output_target(published)
    with pytest.raises(policy.PolicyError, match="independent review"):
        policy.require_output_target(published, owner_approval_ref="G5-EVIDENCE-ACCESS-RUN-20260728-01")
    with pytest.raises(policy.PolicyError, match="validation"):
        policy.require_output_target(
            published,
            owner_approval_ref="G5-EVIDENCE-ACCESS-RUN-20260728-01",
            independent_review_ref="CC_EA6_APPROVAL",
        )
    with pytest.raises(policy.PolicyError, match="atomic"):
        policy.require_output_target(
            published,
            owner_approval_ref="G5-EVIDENCE-ACCESS-RUN-20260728-01",
            independent_review_ref="CC_EA6_APPROVAL",
            validations_passed=True,
        )
    policy.require_output_target(
        published,
        owner_approval_ref="G5-EVIDENCE-ACCESS-RUN-20260728-01",
        independent_review_ref="CC_EA6_APPROVAL",
        validations_passed=True,
        atomic_promotion=True,
    )


def test_approved_artifact_hashes_are_frozen_during_candidate_development():
    assert policy.APPROVED_ARTIFACT_SHA256
    release_manifest = ENCONET / "outputs/evidence_access_release_manifest_RUN-20260728-01.json"
    if not release_manifest.exists():
        for relative_path, expected_hash in policy.APPROVED_ARTIFACT_SHA256.items():
            content = (ENCONET / relative_path).read_bytes()
            assert hashlib.sha256(content).hexdigest() == expected_hash
    else:
        release = json.loads(release_manifest.read_text(encoding="utf-8"))
        released = {row["path"]: row["sha256"] for row in release["artifacts"]}
        assert release["status"] == "promoted"
        for relative_path, expected_hash in released.items():
            assert hashlib.sha256((ENCONET / relative_path).read_bytes()).hexdigest() == expected_hash


def test_owner_adr_selects_offline_delivery_and_defers_any_live_service():
    decision = _adr_policy()
    assert decision["delivery_mode"] == "offline_static"
    assert decision["candidate_root"] == "outputs/candidates/evidence_access/<run_id>/"
    assert decision["preserve_canonical_names_after_promotion"] is True
    assert decision["read_only_evidence"] is True
    assert decision["future_live_service_requires_superseding_adr"] == "ADR-0007"
    assert decision["browser_test_dependencies"] == "deferred_to_EA5.1_owner_approval"
    assert decision["approved_artifacts"] == policy.APPROVED_ARTIFACT_SHA256
