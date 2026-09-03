"""EA1.4 tests for deterministic, fail-closed evidence-bundle generation."""
from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import evidence_access_policy  # noqa: E402
import evidence_resolver  # noqa: E402
import generate_evidence_bundle as generator  # noqa: E402
import validate_evidence_bundle  # noqa: E402


PRODUCTION_DB = ENCONET / "db" / "nqa_audit.sqlite"
PRODUCTION_PACKAGE = ENCONET / "outputs" / "enconet_appendix_b_evaluation_package.json"
SOURCE_MANIFEST = ENCONET / "manifests" / "raw_sources.csv"
GOLDEN_HASH = ENCONET / "tests" / "fixtures" / "evidence_bundle_golden.sha256"
RUN_ID = "RUN-20260728-01"
GENERATED_AT = "2026-09-03T20:00:00Z"


@pytest.fixture(scope="module")
def production_bundle() -> dict:
    return generator.build_bundle(
        package_path=PRODUCTION_PACKAGE,
        db_path=PRODUCTION_DB,
        run_id=RUN_ID,
        source_manifest_path=SOURCE_MANIFEST,
        generated_at_utc=GENERATED_AT,
    )


def test_production_bundle_matches_canonical_golden_bytes(production_bundle: dict):
    canonical = validate_evidence_bundle.canonical_bytes(production_bundle)
    assert hashlib.sha256(canonical).hexdigest() == GOLDEN_HASH.read_text(
        encoding="ascii"
    ).strip()


def test_repeat_generation_is_byte_identical(production_bundle: dict):
    repeated = generator.build_bundle(
        package_path=PRODUCTION_PACKAGE,
        db_path=PRODUCTION_DB,
        run_id=RUN_ID,
        source_manifest_path=SOURCE_MANIFEST,
        generated_at_utc=GENERATED_AT,
    )
    first = validate_evidence_bundle.canonical_bytes(production_bundle)
    second = validate_evidence_bundle.canonical_bytes(repeated)
    assert first == second
    assert hashlib.sha256(first).digest() == hashlib.sha256(second).digest()


def test_production_coverage_is_62_of_62(production_bundle: dict):
    package = json.loads(PRODUCTION_PACKAGE.read_text(encoding="utf-8"))
    expected = {
        crumb_id
        for evaluation in package["evaluations"]
        for crumb_id in evaluation["evidence_ids"]
    }
    resolved = {crumb["crumb_id"] for crumb in production_bundle["crumbs"]}
    assert len(expected) == 62
    assert expected <= resolved
    assert generator.evaluation_coverage(production_bundle) == (62, 62)


def test_bundle_contains_only_selected_run_evaluation_evidence(production_bundle: dict):
    assert {row["evaluation_id"] for row in production_bundle["evaluations"]} == {
        f"EVAL-APP_B_{roman}"
        for roman in (
            "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
            "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
        )
    }
    assert all(
        crumb["evaluation_ids"]
        for crumb in production_bundle["crumbs"]
        if crumb["crumb_id"] in {
            evidence_id
            for evaluation in production_bundle["evaluations"]
            for evidence_id in evaluation["evidence_crumb_ids"]
        }
    )


def _candidate_target(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    root = tmp_path / "candidates" / "evidence_access"
    monkeypatch.setattr(evidence_access_policy, "CANDIDATE_ROOT", root)
    return root / RUN_ID / "evidence_bundle.json"


def test_missing_package_fails_before_publication(monkeypatch, tmp_path: Path):
    target = _candidate_target(monkeypatch, tmp_path)
    with pytest.raises(generator.BundleGenerationError, match="package does not exist"):
        generator.generate(
            package_path=tmp_path / "missing.json",
            db_path=PRODUCTION_DB,
            run_id=RUN_ID,
            source_manifest_path=SOURCE_MANIFEST,
            generated_at_utc=GENERATED_AT,
            output_path=target,
        )
    assert not target.exists()


def test_package_database_mismatch_fails_before_publication(monkeypatch, tmp_path: Path):
    target = _candidate_target(monkeypatch, tmp_path)
    package_path = tmp_path / "mismatch.json"
    package = json.loads(PRODUCTION_PACKAGE.read_text(encoding="utf-8"))
    package["run"]["supplier"] = "wrong-supplier"
    package_path.write_text(json.dumps(package), encoding="utf-8")
    with pytest.raises(generator.BundleGenerationError, match="package/database mismatch"):
        generator.generate(
            package_path=package_path,
            db_path=PRODUCTION_DB,
            run_id=RUN_ID,
            source_manifest_path=SOURCE_MANIFEST,
            generated_at_utc=GENERATED_AT,
            output_path=target,
        )
    assert not target.exists()


def test_unresolved_evidence_fails_before_publication(monkeypatch, tmp_path: Path):
    target = _candidate_target(monkeypatch, tmp_path)
    database = tmp_path / "broken.sqlite"
    shutil.copy2(PRODUCTION_DB, database)
    with sqlite3.connect(database) as connection:
        quote_id = connection.execute(
            "SELECT q.quote_id FROM crumb_quotes AS q "
            "JOIN evaluation_evidence AS ee ON ee.item_id=q.item_id "
            "ORDER BY q.quote_id LIMIT 1"
        ).fetchone()[0]
        connection.execute("DELETE FROM crumb_chunk_links WHERE quote_id=?", (quote_id,))
    with pytest.raises(generator.BundleGenerationError, match="missing chunk link"):
        generator.generate(
            package_path=PRODUCTION_PACKAGE,
            db_path=database,
            run_id=RUN_ID,
            source_manifest_path=SOURCE_MANIFEST,
            generated_at_utc=GENERATED_AT,
            output_path=target,
        )
    assert not target.exists()


def test_invalid_output_path_is_rejected_before_publication(tmp_path: Path):
    target = tmp_path / "outside-candidate-root.json"
    with pytest.raises(evidence_access_policy.PolicyError, match="neither"):
        generator.generate(
            package_path=PRODUCTION_PACKAGE,
            db_path=PRODUCTION_DB,
            run_id=RUN_ID,
            source_manifest_path=SOURCE_MANIFEST,
            generated_at_utc=GENERATED_AT,
            output_path=target,
        )
    assert not target.exists()


def test_approved_artifact_overwrite_is_rejected_without_gate_evidence():
    protected = ENCONET / "outputs" / "enconet_appendix_b_dashboard_data.json"
    original = protected.read_bytes()
    with pytest.raises(evidence_access_policy.PolicyError, match="G6 owner approval"):
        generator.generate(
            package_path=PRODUCTION_PACKAGE,
            db_path=PRODUCTION_DB,
            run_id=RUN_ID,
            source_manifest_path=SOURCE_MANIFEST,
            generated_at_utc=GENERATED_AT,
            output_path=protected,
        )
    assert protected.read_bytes() == original


def test_validation_failure_preserves_existing_candidate(monkeypatch, tmp_path: Path):
    target = _candidate_target(monkeypatch, tmp_path)
    target.parent.mkdir(parents=True)
    target.write_bytes(b"existing-candidate\n")
    monkeypatch.setattr(
        generator.validate_evidence_bundle,
        "validate",
        lambda _bundle: ["injected validation failure"],
    )
    with pytest.raises(generator.BundleGenerationError, match="injected validation failure"):
        generator.generate(
            package_path=PRODUCTION_PACKAGE,
            db_path=PRODUCTION_DB,
            run_id=RUN_ID,
            source_manifest_path=SOURCE_MANIFEST,
            generated_at_utc=GENERATED_AT,
            output_path=target,
        )
    assert target.read_bytes() == b"existing-candidate\n"


def test_cli_writes_valid_candidate_atomically_and_reports_coverage(
    monkeypatch, tmp_path: Path, capsys
):
    target = _candidate_target(monkeypatch, tmp_path)
    result = generator.main([
        "--package", str(PRODUCTION_PACKAGE),
        "--db", str(PRODUCTION_DB),
        "--run-id", RUN_ID,
        "--source-manifest", str(SOURCE_MANIFEST),
        "--generated-at-utc", GENERATED_AT,
        "--output", str(target),
    ])
    assert result == 0
    assert "62/62 evaluation crumbs resolved" in capsys.readouterr().out
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert validate_evidence_bundle.validate(payload) == []
    assert not list(target.parent.glob(f".{target.name}.*.tmp"))


def test_invalid_generated_timestamp_fails_before_publication(monkeypatch, tmp_path: Path):
    target = _candidate_target(monkeypatch, tmp_path)
    with pytest.raises(generator.BundleGenerationError, match="generated-at-utc"):
        generator.generate(
            package_path=PRODUCTION_PACKAGE,
            db_path=PRODUCTION_DB,
            run_id=RUN_ID,
            source_manifest_path=SOURCE_MANIFEST,
            generated_at_utc="today",
            output_path=target,
        )
    assert not target.exists()
