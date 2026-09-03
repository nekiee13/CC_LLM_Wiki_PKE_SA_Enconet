"""EA3.3 exhaustive report-link publication validation tests."""
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

import generate_dashboard  # noqa: E402
import validate_evidence_bundle  # noqa: E402
import validate_report_links  # noqa: E402


RUN_ID = "RUN-20260728-01"
CANDIDATE = ENCONET / "outputs" / "candidates" / "evidence_access" / RUN_ID
REPORT = CANDIDATE / "enconet_appendix_b_evaluation_report.md"
VIEWER = CANDIDATE / "enconet_appendix_b_dashboard.html"
PACKAGE = ENCONET / "outputs" / "enconet_appendix_b_evaluation_package.json"
BUNDLE = CANDIDATE / "evidence_bundle.json"


@pytest.fixture(scope="module")
def artifacts() -> tuple[str, str, dict, dict]:
    return (
        REPORT.read_text(encoding="utf-8"),
        VIEWER.read_text(encoding="utf-8"),
        json.loads(PACKAGE.read_text(encoding="utf-8")),
        json.loads(BUNDLE.read_text(encoding="utf-8")),
    )


def _viewer_with_bundle(html: str, bundle: dict) -> str:
    payload = generate_dashboard._script_json(bundle)
    digest = hashlib.sha256(validate_evidence_bundle.canonical_bytes(bundle)).hexdigest()
    pattern = re.compile(
        r'(<script id="evidence-bundle" type="application/json" data-sha256=")[^"]*'
        r'(">).*?(</script>)',
        re.DOTALL,
    )
    replaced, count = pattern.subn(
        lambda match: f"{match.group(1)}{digest}{match.group(2)}{payload}{match.group(3)}",
        html,
    )
    assert count == 1
    return replaced


def _validate(report: str, viewer: str, package: dict) -> list[str]:
    return validate_report_links.validate(
        report,
        viewer,
        package,
        report_path=REPORT,
        viewer_path=VIEWER,
        package_path=PACKAGE,
        project_root=ENCONET,
    )


def test_every_production_candidate_citation_is_valid(artifacts):
    report, viewer, package, _bundle = artifacts
    assert _validate(report, viewer, package) == []
    links, malformed = validate_report_links.parse_evidence_links(report, REPORT)
    assert malformed == []
    assert len(links) == 200
    assert {link.entity_type for link in links} == {
        "crumb", "document", "evaluation", "gap", "finding", "action"
    }


def test_missing_viewer_file_fails_with_exact_artifact_path(tmp_path: Path):
    missing = tmp_path / "missing-viewer.html"
    errors = validate_report_links.validate_paths(REPORT, missing, PACKAGE)
    assert errors == [f"{missing}: viewer file is missing"]


def test_unknown_target_reports_report_location_and_target(artifacts):
    report, viewer, package, _bundle = artifacts
    broken = report.replace(
        "#evidence/document/DOC-0024", "#evidence/document/DOC-9999", 1
    )
    errors = _validate(broken, viewer, package)
    assert any(
        re.search(r"report\.md:\d+:\d+: unknown evidence target: "
                  r"#evidence/document/DOC-9999$", error)
        for error in errors
    )


def test_duplicate_bundle_target_is_rejected_deterministically(artifacts):
    report, viewer, package, bundle = artifacts
    duplicate = copy.deepcopy(bundle)
    duplicate["documents"].append(copy.deepcopy(duplicate["documents"][0]))
    errors = _validate(report, _viewer_with_bundle(viewer, duplicate), package)
    assert any("duplicate document_id: DOC-0021" in error for error in errors)
    assert any("duplicate viewer target: #evidence/document/DOC-0021" in error for error in errors)


def test_extra_and_missing_repeated_report_citations_are_rejected(artifacts):
    report, viewer, package, _bundle = artifacts
    match = re.search(r"\[[^\]]+\]\([^)]+#evidence/[^)]+\)", report)
    assert match is not None
    duplicated = report[:match.end()] + " " + match.group(0) + report[match.end():]
    errors = _validate(duplicated, viewer, package)
    assert any("duplicate report citation:" in error for error in errors)

    missing = report[:match.start()] + report[match.end():]
    errors = _validate(missing, viewer, package)
    assert any("missing report citation:" in error for error in errors)


def test_wrong_run_and_wrong_package_hash_are_rejected(artifacts):
    report, viewer, package, bundle = artifacts
    wrong_run = copy.deepcopy(bundle)
    wrong_run["metadata"]["run_id"] = "RUN-20260903-99"
    errors = _validate(report, _viewer_with_bundle(viewer, wrong_run), package)
    assert "report/viewer mismatch: run_id" in errors
    assert "package/viewer mismatch: run_id" in errors
    assert "viewer metadata/bundle mismatch: run_id" in errors

    wrong_hash = copy.deepcopy(bundle)
    wrong_hash["lineage"]["package"]["sha256"] = "0" * 64
    errors = _validate(report, _viewer_with_bundle(viewer, wrong_hash), package)
    assert any("stale lineage artifact: package" in error for error in errors)

    report_hash = re.search(r'"package_sha256":"([0-9a-f]{64})"', report)
    assert report_hash is not None
    tampered_report = report.replace(report_hash.group(1), "1" * 64, 1)
    errors = _validate(tampered_report, viewer, package)
    assert any("report/package mismatch: package_sha256" in error for error in errors)


def test_malformed_markdown_url_is_rejected_at_its_report_location(artifacts):
    report, viewer, package, _bundle = artifacts
    first = re.search(r"\]\([^)]+#evidence/[^)]+\)", report)
    assert first is not None
    broken = report[: first.end() - 1] + report[first.end():]
    errors = _validate(broken, viewer, package)
    assert any(
        re.search(r"report\.md:\d+:\d+: malformed evidence Markdown URL$", error)
        for error in errors
    )


def test_stale_bundle_database_lineage_is_rejected(artifacts):
    report, viewer, package, bundle = artifacts
    stale = copy.deepcopy(bundle)
    stale["lineage"]["database"]["sha256"] = "f" * 64
    errors = _validate(report, _viewer_with_bundle(viewer, stale), package)
    assert any("stale lineage artifact: database" in error for error in errors)
    assert errors == _validate(report, _viewer_with_bundle(viewer, stale), package)


def test_cli_exit_code_is_zero_for_candidate_and_nonzero_for_broken_copy(
    artifacts, tmp_path: Path, capsys
):
    assert validate_report_links.main([str(REPORT), str(VIEWER), str(PACKAGE)]) == 0
    assert "validate_report_links: PASS - 200 evidence link(s)" in capsys.readouterr().out

    report, _viewer, _package, _bundle = artifacts
    broken = tmp_path / "broken-report.md"
    broken.write_text(report.replace("#evidence/crumb/", "#evidence/crumb/BROKEN-", 1), encoding="utf-8")
    assert validate_report_links.main([str(broken), str(VIEWER), str(PACKAGE)]) == 1
    assert f"{broken}:" in capsys.readouterr().err
