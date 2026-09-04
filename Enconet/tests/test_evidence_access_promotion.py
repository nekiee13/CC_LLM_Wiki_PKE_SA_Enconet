"""EA6.4 tests for human-gated, rollback-safe Evidence Access promotion."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import promote_evidence_access as promotion  # noqa: E402
import validate_report_links  # noqa: E402


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(tmp_path: Path) -> tuple[Path, Path, dict[str, bytes]]:
    project = tmp_path / "project"
    candidate = project / "candidate"
    outputs = project / "outputs"
    wiki = project / "wiki" / "dashboards"
    for directory in (candidate, outputs, wiki):
        directory.mkdir(parents=True)

    (candidate / "report.md").write_bytes(b"new report")
    (candidate / "viewer.html").write_bytes(b"new viewer")
    manifest = candidate / "package_manifest.json"
    manifest.write_text('{"release":"fixed"}\n', encoding="utf-8")

    destinations = {
        "outputs/report.md": b"old report",
        "outputs/report_hr.md": b"old report",
        "outputs/viewer.html": b"old viewer",
        "outputs/viewer_hr.html": b"old viewer",
        "wiki/dashboards/viewer.html": b"old viewer",
    }
    for relative, content in destinations.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    contract = {
        "schema_version": "1.0",
        "release_id": "EA6.4-RUN-20260728-01",
        "status": "awaiting_owner_promotion",
        "run_id": "RUN-20260728-01",
        "candidate_manifest": {
            "path": "candidate/package_manifest.json",
            "sha256": _digest(manifest),
        },
        "required_approvals": {
            "report": "G5-EVIDENCE-ACCESS-RUN-20260728-01",
            "dashboard": "G6-EVIDENCE-ACCESS-RUN-20260728-01",
        },
        "independent_review": "CC_REVIEW_APPROVED",
        "promotion": [
            {"source": "candidate/report.md", "destination": "outputs/report.md", "sha256": _digest(candidate / "report.md")},
            {"source": "candidate/report.md", "destination": "outputs/report_hr.md", "sha256": _digest(candidate / "report.md")},
            {"source": "candidate/viewer.html", "destination": "outputs/viewer.html", "sha256": _digest(candidate / "viewer.html")},
            {"source": "candidate/viewer.html", "destination": "outputs/viewer_hr.html", "sha256": _digest(candidate / "viewer.html")},
            {"source": "candidate/viewer.html", "destination": "wiki/dashboards/viewer.html", "sha256": _digest(candidate / "viewer.html")},
        ],
        "baseline": [
            {"path": relative, "sha256": hashlib.sha256(content).hexdigest()}
            for relative, content in destinations.items()
        ],
        "post_validation": {
            "report": "outputs/report.md",
            "viewer": "outputs/viewer.html",
            "package": "outputs/package.json",
        },
        "result_manifest": "outputs/EA6.4_release_manifest.json",
    }
    contract_path = project / "promotion.yml"
    contract_path.write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")
    return project, contract_path, destinations


def _approvals(path: Path, *decision_refs: str) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["object_id", "decision", "date", "reviewer", "notes"])
        for decision_ref in decision_refs:
            writer.writerow([decision_ref, "approved", "2026-09-04", "project-owner", "exact release"])
    return path


def _unchanged(project: Path, original: dict[str, bytes]) -> None:
    assert {relative: (project / relative).read_bytes() for relative in original} == original


def test_missing_owner_approval_fails_before_any_write(tmp_path: Path) -> None:
    project, contract, original = _fixture(tmp_path)
    approvals = _approvals(project / "approvals.csv", "G5-EVIDENCE-ACCESS-RUN-20260728-01")
    with pytest.raises(promotion.PromotionError, match="G6-EVIDENCE-ACCESS"):
        promotion.promote(contract, project_root=project, approvals=approvals)
    _unchanged(project, original)


def test_failed_preflight_validator_leaves_baseline_unchanged(tmp_path: Path) -> None:
    project, contract, original = _fixture(tmp_path)
    approvals = _approvals(
        project / "approvals.csv",
        "G5-EVIDENCE-ACCESS-RUN-20260728-01",
        "G6-EVIDENCE-ACCESS-RUN-20260728-01",
    )
    with pytest.raises(promotion.PromotionError, match="pre-promotion validation failed"):
        promotion.promote(
            contract, project_root=project, approvals=approvals,
            pre_validator=lambda _contract, _root: ["aggregate failed"],
        )
    _unchanged(project, original)


@pytest.mark.parametrize("drift", ("candidate", "baseline"))
def test_hash_drift_or_stale_candidate_fails_closed(tmp_path: Path, drift: str) -> None:
    project, contract, original = _fixture(tmp_path)
    approvals = _approvals(
        project / "approvals.csv",
        "G5-EVIDENCE-ACCESS-RUN-20260728-01",
        "G6-EVIDENCE-ACCESS-RUN-20260728-01",
    )
    target = project / ("candidate/report.md" if drift == "candidate" else "outputs/report.md")
    target.write_bytes(b"drift")
    with pytest.raises(promotion.PromotionError, match="hash mismatch"):
        promotion.promote(contract, project_root=project, approvals=approvals)
    if drift == "candidate":
        _unchanged(project, original)
    else:
        assert (project / "outputs/report_hr.md").read_bytes() == b"old report"


def test_partial_replace_is_rolled_back(tmp_path: Path) -> None:
    project, contract, original = _fixture(tmp_path)
    approvals = _approvals(
        project / "approvals.csv",
        "G5-EVIDENCE-ACCESS-RUN-20260728-01",
        "G6-EVIDENCE-ACCESS-RUN-20260728-01",
    )
    calls = 0

    def interrupted_replace(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected partial-copy failure")
        source.replace(destination)

    with pytest.raises(promotion.PromotionError, match="rolled back"):
        promotion.promote(
            contract, project_root=project, approvals=approvals,
            pre_validator=lambda _contract, _root: [],
            post_validator=lambda _contract, _root: [],
            replace=interrupted_replace,
        )
    _unchanged(project, original)
    assert not (project / "outputs/EA6.4_release_manifest.json").exists()


def test_failed_post_validation_rolls_back_every_destination(tmp_path: Path) -> None:
    project, contract, original = _fixture(tmp_path)
    approvals = _approvals(
        project / "approvals.csv",
        "G5-EVIDENCE-ACCESS-RUN-20260728-01",
        "G6-EVIDENCE-ACCESS-RUN-20260728-01",
    )
    with pytest.raises(promotion.PromotionError, match="post-promotion validation failed"):
        promotion.promote(
            contract, project_root=project, approvals=approvals,
            pre_validator=lambda _contract, _root: [],
            post_validator=lambda _contract, _root: ["published link failed"],
        )
    _unchanged(project, original)
    assert not (project / "outputs/EA6.4_release_manifest.json").exists()


def test_success_promotes_complete_set_and_records_hashes(tmp_path: Path) -> None:
    project, contract, _original = _fixture(tmp_path)
    approvals = _approvals(
        project / "approvals.csv",
        "G5-EVIDENCE-ACCESS-RUN-20260728-01",
        "G6-EVIDENCE-ACCESS-RUN-20260728-01",
    )
    result = promotion.promote(
        contract, project_root=project, approvals=approvals,
        pre_validator=lambda _contract, _root: [],
        post_validator=lambda _contract, _root: [],
    )
    assert result["status"] == "promoted"
    assert len(result["artifacts"]) == 5
    for row in result["artifacts"]:
        assert _digest(project / row["path"]) == row["sha256"]
    recorded = json.loads((project / "outputs/EA6.4_release_manifest.json").read_text(encoding="utf-8"))
    assert recorded == result


def test_real_candidate_links_resolve_from_final_published_names(tmp_path: Path) -> None:
    published = tmp_path / "published"
    published.mkdir()
    report = published / "enconet_appendix_b_evaluation_report.md"
    viewer = published / "enconet_appendix_b_dashboard.html"
    report.write_bytes((ENCONET / "outputs/candidates/evidence_access/RUN-20260728-01/enconet_appendix_b_evaluation_report.md").read_bytes())
    viewer.write_bytes((ENCONET / "outputs/candidates/evidence_access/RUN-20260728-01/enconet_appendix_b_dashboard.html").read_bytes())
    package = ENCONET / "outputs/enconet_appendix_b_evaluation_package.json"
    assert validate_report_links.validate_paths(
        report, viewer, package, project_root=ENCONET
    ) == []


def test_production_contract_records_completed_exact_five_file_promotion() -> None:
    contract = yaml.safe_load((ENCONET / "schemas/evidence_access_promotion.yml").read_text(encoding="utf-8"))
    assert contract["status"] == "promoted"
    assert contract["independent_review"] == "CC_2026-09-04T213922Z_chapter-reference-approve-with-observation"
    assert contract["required_approvals"] == {
        "report": "G5-EVIDENCE-ACCESS-RUN-20260728-01",
        "dashboard": "G6-EVIDENCE-ACCESS-RUN-20260728-01",
    }
    assert len(contract["promotion"]) == len(contract["baseline"]) == 5
    with pytest.raises(promotion.PromotionError, match="not awaiting Owner promotion"):
        promotion._load_contract(ENCONET / "schemas/evidence_access_promotion.yml")
    result = ENCONET / contract["result_manifest"]
    recorded = json.loads(result.read_text(encoding="utf-8"))
    assert recorded["status"] == "promoted"
    assert recorded["owner_approval_refs"] == contract["required_approvals"]
    assert len(recorded["artifacts"]) == 5
