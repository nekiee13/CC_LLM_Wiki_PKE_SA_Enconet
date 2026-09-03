"""EA4.1 deterministic registered review-package catalog tests."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import generate_review_catalog  # noqa: E402
import validate_review_catalog  # noqa: E402


REGISTRY = ENCONET / "schemas" / "review_packages.yml"
CANDIDATE_CATALOG = (
    ENCONET / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"
)


def registered(run_id: str, *, status: str = "candidate") -> dict:
    row = {
        "run_id": run_id,
        "status": status,
        "package": f"registered/{run_id}/package.json",
        "report": f"registered/{run_id}/report.md",
        "viewer": f"registered/{run_id}/viewer.html",
        "bundle": f"registered/{run_id}/bundle.json",
    }
    row.update({f"{kind}_sha256": "0" * 64 for kind in ("package", "report", "viewer", "bundle")})
    return row


def fake_validated(entry: dict, _root: Path) -> dict:
    suffix = entry["run_id"][-2:]
    artifacts = {
        kind: {"path": path, "sha256": suffix * 32}
        for kind, path in sorted(entry.items())
        if kind in {"package", "report", "viewer", "bundle"}
    }
    return {
        "run_id": entry["run_id"],
        "supplier": f"supplier-{suffix}",
        "framework": "appendix_b",
        "status": entry["status"],
        "language": "hr",
        "generated_at_utc": f"2026-09-{suffix}T00:00:00Z",
        "artifacts": artifacts,
    }


def test_zero_one_and_multiple_registered_runs_are_stable(tmp_path: Path):
    empty = generate_review_catalog.build_catalog([], tmp_path, validator=fake_validated)
    assert empty == {"schema_version": "1.0", "ordering_policy": "run-id-v1", "runs": []}

    one = generate_review_catalog.build_catalog(
        [registered("RUN-20260901-01")], tmp_path, validator=fake_validated
    )
    assert len(one["runs"]) == 1
    many = generate_review_catalog.build_catalog(
        [registered("RUN-20260903-03"), registered("RUN-20260901-01"),
         registered("RUN-20260902-02", status="approved")],
        tmp_path,
        validator=fake_validated,
    )
    assert [row["run_id"] for row in many["runs"]] == [
        "RUN-20260901-01", "RUN-20260902-02", "RUN-20260903-03"
    ]
    assert generate_review_catalog.canonical_bytes(many) == generate_review_catalog.canonical_bytes(
        generate_review_catalog.build_catalog(
            list(reversed([registered("RUN-20260903-03"), registered("RUN-20260901-01"),
                           registered("RUN-20260902-02", status="approved")])),
            tmp_path,
            validator=fake_validated,
        )
    )


def test_duplicate_run_ids_are_rejected_before_validation(tmp_path: Path):
    rows = [registered("RUN-20260901-01"), registered("RUN-20260901-01")]
    with pytest.raises(ValueError, match="duplicate registered run_id"):
        generate_review_catalog.build_catalog(rows, tmp_path, validator=fake_validated)


def test_missing_artifact_and_hash_mismatch_fail_closed(tmp_path: Path):
    entry = registered("RUN-20260901-01")
    with pytest.raises(ValueError, match=r"artifact is missing.*\.json"):
        generate_review_catalog.validate_entry(entry, tmp_path)

    target = tmp_path / entry["package"]
    target.parent.mkdir(parents=True)
    target.write_text("{}", encoding="utf-8")
    entry["package_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="package artifact hash mismatch"):
        generate_review_catalog._verified_artifact(entry, "package", tmp_path)


def test_candidate_and_approved_status_are_preserved(tmp_path: Path):
    catalog = generate_review_catalog.build_catalog(
        [registered("RUN-20260901-01", status="candidate"),
         registered("RUN-20260902-02", status="approved")],
        tmp_path,
        validator=fake_validated,
    )
    assert [row["status"] for row in catalog["runs"]] == ["candidate", "approved"]


def test_unregistered_files_are_ignored(tmp_path: Path):
    unrelated = tmp_path / "outputs" / "looks_like_a_report.md"
    unrelated.parent.mkdir()
    unrelated.write_text("not registered", encoding="utf-8")
    catalog = generate_review_catalog.build_catalog([], tmp_path, validator=fake_validated)
    assert catalog["runs"] == []
    assert unrelated.as_posix() not in json.dumps(catalog)


def test_catalog_validator_rejects_duplicate_rows_wrong_order_and_bad_hash():
    row = fake_validated(registered("RUN-20260901-01"), Path("."))
    valid = {"schema_version": "1.0", "ordering_policy": "run-id-v1", "runs": [row]}
    assert validate_review_catalog.validate(valid) == []

    duplicate = copy.deepcopy(valid)
    duplicate["runs"].append(copy.deepcopy(row))
    assert any("duplicate catalog run_id" in error for error in validate_review_catalog.validate(duplicate))

    wrong_order = copy.deepcopy(valid)
    wrong_order["runs"] = [
        fake_validated(registered("RUN-20260902-02"), Path(".")), row
    ]
    assert any("non-deterministic run order" in error for error in validate_review_catalog.validate(wrong_order))

    bad_hash = copy.deepcopy(valid)
    bad_hash["runs"][0]["artifacts"]["report"]["sha256"] = "bad"
    assert any("invalid artifact sha256" in error for error in validate_review_catalog.validate(bad_hash))


def test_controlled_registry_builds_one_fully_validated_production_run():
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    catalog = generate_review_catalog.build_catalog(registry["packages"], ENCONET)
    assert validate_review_catalog.validate(catalog) == []
    assert [row["run_id"] for row in catalog["runs"]] == ["RUN-20260728-01"]
    row = catalog["runs"][0]
    assert row["supplier"] == "enconet"
    assert row["framework"] == "appendix_b"
    assert row["status"] == "candidate"
    assert row["language"] == "hr"
    assert row["generated_at_utc"]
    assert set(row["artifacts"]) == {"bundle", "package", "report", "viewer"}
    for artifact in row["artifacts"].values():
        assert len(artifact["sha256"]) == 64


def test_cli_writes_canonical_catalog_and_is_repeatable(tmp_path: Path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    assert generate_review_catalog.main([
        "--registry", str(REGISTRY), "--output", str(first), "--project-root", str(ENCONET)
    ]) == 0
    assert generate_review_catalog.main([
        "--registry", str(REGISTRY), "--output", str(second), "--project-root", str(ENCONET)
    ]) == 0
    assert first.read_bytes() == second.read_bytes()
    assert validate_review_catalog.main([str(first)]) == 0
