"""EA1.2 tests for the run-scoped report-reference entity graph."""
from __future__ import annotations

import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import evidence_resolver  # noqa: E402


PRODUCTION_DB = ENCONET / "db" / "nqa_audit.sqlite"
PRODUCTION_PACKAGE = ENCONET / "outputs" / "enconet_appendix_b_evaluation_package.json"
RUN_ID = "RUN-20260728-01"


@pytest.fixture(scope="module")
def registry() -> dict:
    return evidence_resolver.build_entity_registry(
        PRODUCTION_DB, RUN_ID, package_path=PRODUCTION_PACKAGE
    )


@pytest.mark.parametrize(
    "reference,entity_type,presentation",
    (
        ("crumb:CRUMB-DOC-0021-APP_B_I-0003", "crumb", "evidence-detail"),
        ("document:DOC-0024", "document", "document-metadata"),
        ("gap:GAP-APP_B_IV-01", "gap", "gap-detail"),
        ("finding:FIND-0001", "finding", "finding-detail"),
        ("action:ACT-0002", "action", "action-detail"),
        ("source:package", "source", "package-metadata"),
    ),
)
def test_every_report_reference_type_has_a_defined_presentation(
    registry: dict, reference: str, entity_type: str, presentation: str
):
    entity = evidence_resolver.resolve_reference(registry, reference)
    assert entity is not None
    assert entity["reference"] == reference
    assert entity["entity_type"] == entity_type
    assert entity["presentation"] == presentation
    assert entity["viewer_target"].startswith("#evidence/")


def test_every_reference_currently_emitted_by_production_report_resolves(registry: dict):
    report = (ENCONET / "outputs" / "enconet_appendix_b_evaluation_report.md").read_text(
        encoding="utf-8"
    )
    references = sorted(set(re.findall(
        r"\[(?:crumb|document|gap|finding|action|source):[^\]]+\]", report
    )))
    assert references
    unresolved = [
        reference for bracketed in references
        if (reference := bracketed[1:-1])
        and evidence_resolver.resolve_reference(registry, reference) is None
    ]
    assert unresolved == []


@pytest.mark.parametrize(
    "reference",
    (
        "crumb:CRUMB-DOC-0021-APP_B_I-9999",
        "document:DOC-9999",
        "gap:GAP-APP_B_I-99",
        "finding:FIND-9999",
        "action:ACT-9999",
        "source:missing",
        "malformed",
    ),
)
def test_missing_or_malformed_reference_returns_no_match(registry: dict, reference: str):
    assert evidence_resolver.resolve_reference(registry, reference) is None


def test_forward_and_reverse_lineage_is_complete_and_reference_only(registry: dict):
    finding = evidence_resolver.resolve_reference(registry, "finding:FIND-0001")
    assert finding is not None
    assert finding["relationships"]["gap"] == "gap:GAP-APP_B_IV-01"
    assert finding["relationships"]["evaluation"] == "evaluation:EVAL-APP_B_IV"

    gap = evidence_resolver.resolve_reference(registry, finding["relationships"]["gap"])
    assert gap is not None
    assert gap["relationships"]["evaluation"] == "evaluation:EVAL-APP_B_IV"
    assert gap["relationships"]["evidence_crumb"] == (
        "crumb:CRUMB-DOC-0024-APP_B_IV-0001"
    )
    assert "finding:FIND-0001" in gap["relationships"]["findings"]

    evaluation = evidence_resolver.resolve_reference(
        registry, gap["relationships"]["evaluation"]
    )
    assert evaluation is not None
    assert "crumb:CRUMB-DOC-0024-APP_B_IV-0001" in (
        evaluation["relationships"]["evidence_crumbs"]
    )
    assert "gap:GAP-APP_B_IV-01" in evaluation["relationships"]["gaps"]


def test_action_primary_target_and_related_finding_are_distinct(registry: dict):
    action = evidence_resolver.resolve_reference(registry, "action:ACT-0002")
    assert action is not None
    assert action["viewer_target"] == "#evidence/action/ACT-0002"
    assert action["relationships"]["finding"] == "finding:FIND-0001"
    finding = evidence_resolver.resolve_reference(
        registry, action["relationships"]["finding"]
    )
    assert finding is not None
    assert finding["viewer_target"] == "#evidence/finding/FIND-0001"
    assert finding["viewer_target"] != action["viewer_target"]


def test_gap_self_reference_is_non_recursive_and_truthful(registry: dict):
    gap = evidence_resolver.resolve_reference(registry, "gap:GAP-APP_B_IV-01")
    assert gap is not None
    assert gap["viewer_target"] == "#evidence/gap/GAP-APP_B_IV-01"
    assert gap["data"]["description"]
    assert gap["data"]["evaluation_id"] == "EVAL-APP_B_IV"
    assert gap["data"]["missing_evidence_ref"] is None
    assert gap["data"]["evidence_crumb_id"] == "CRUMB-DOC-0024-APP_B_IV-0001"
    assert gap["relationships"]["self"] is None
    assert all(isinstance(value, (str, list, type(None))) for value in gap["relationships"].values())
    assert "gap:GAP-APP_B_IV-01" not in json.dumps(gap["relationships"], sort_keys=True)


def test_relationships_are_sorted_unique_and_registry_is_deterministic(registry: dict):
    rebuilt = evidence_resolver.build_entity_registry(
        PRODUCTION_DB, RUN_ID, package_path=PRODUCTION_PACKAGE
    )
    assert rebuilt == registry
    for entity in registry["entities"].values():
        for value in entity["relationships"].values():
            if isinstance(value, list):
                assert value == sorted(set(value))


def test_package_reference_has_verified_selected_run_lineage(registry: dict):
    source = evidence_resolver.resolve_reference(registry, "source:package")
    assert source is not None
    assert source["data"]["run_id"] == RUN_ID
    assert source["data"]["path"] == "outputs/enconet_appendix_b_evaluation_package.json"
    assert len(source["data"]["sha256"]) == 64
    assert source["relationships"]["evaluation_run"] == RUN_ID


def test_package_reference_is_missing_when_no_package_is_explicitly_supplied():
    without_package = evidence_resolver.build_entity_registry(PRODUCTION_DB, RUN_ID)
    assert evidence_resolver.resolve_reference(without_package, "source:package") is None


def test_package_with_wrong_run_fails_closed(tmp_path: Path):
    package = tmp_path / "wrong.json"
    payload = json.loads(PRODUCTION_PACKAGE.read_text(encoding="utf-8"))
    payload["run"]["run_id"] = "RUN-20260903-99"
    package.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(evidence_resolver.EvidenceIntegrityError, match="package run mismatch"):
        evidence_resolver.build_entity_registry(PRODUCTION_DB, RUN_ID, package_path=package)


def test_other_run_is_excluded_unless_explicitly_included(tmp_path: Path):
    database = tmp_path / "runs.sqlite"
    shutil.copy2(PRODUCTION_DB, database)
    with sqlite3.connect(database) as connection:
        connection.execute(
            "DELETE FROM auditor_actions WHERE finding_id IN "
            "(SELECT finding_id FROM findings WHERE criterion_id='APP_B_XVIII') OR gap_id IN "
            "(SELECT gap_id FROM gaps WHERE evaluation_id='EVAL-APP_B_XVIII')"
        )
        connection.execute("DELETE FROM findings WHERE criterion_id='APP_B_XVIII'")
        connection.execute("DELETE FROM gaps WHERE evaluation_id='EVAL-APP_B_XVIII'")
        connection.execute("DELETE FROM evaluation_evidence WHERE evaluation_id='EVAL-APP_B_XVIII'")
        connection.execute("DELETE FROM criterion_evaluations WHERE evaluation_id='EVAL-APP_B_XVIII'")
        connection.execute(
            "INSERT INTO evaluation_runs(run_id,supplier,deliverable_language,scoring_model_version) "
            "VALUES(?,?,?,?)",
            ("RUN-20260903-99", "other", "en", "v1"),
        )
        connection.execute(
            "INSERT INTO criterion_evaluations(evaluation_id,evaluation_run_id,criterion_id,rating,"
            "score,coverage,completeness,accuracy,clarity,alignment,evidence_supported,"
            "affirmative_summary,contrary_summary,judge_ruling,rationale) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "EVAL-APP_B_XVIII", "RUN-20260903-99", "APP_B_XVIII", "fully", 100.0,
                1.0, 1.0, 1.0, 1.0, 1.0, 1, "yes", "none", "pass", "test",
            ),
        )
        connection.execute(
            "INSERT INTO findings(finding_id,evaluation_run_id,criterion_id,evidence_item_id,"
            "title,body,severity,confidence,basis) VALUES(?,?,?,?,?,?,?,?,?)",
            (
                "FIND-9999", "RUN-20260903-99", "APP_B_XVIII",
                "CRUMB-DOC-0030-APP_B_XVIII-0001", "Foreign", "Foreign run finding",
                "low", "high", "explicit test",
            ),
        )
        connection.execute(
            "INSERT INTO auditor_actions(action_id,evaluation_run_id,finding_id,action_type,"
            "description) VALUES(?,?,?,?,?)",
            ("ACT-9999", "RUN-20260903-99", "FIND-9999", "verification", "Foreign action"),
        )

    selected = evidence_resolver.build_entity_registry(database, RUN_ID)
    assert evidence_resolver.resolve_reference(selected, "finding:FIND-9999") is None
    assert evidence_resolver.resolve_reference(selected, "action:ACT-9999") is None

    included = evidence_resolver.build_entity_registry(
        database, RUN_ID, included_run_ids=("RUN-20260903-99",)
    )
    assert evidence_resolver.resolve_reference(included, "finding:FIND-9999") is not None
    assert evidence_resolver.resolve_reference(included, "action:ACT-9999") is not None
    assert included["included_run_ids"] == [RUN_ID, "RUN-20260903-99"]

    with sqlite3.connect(database) as connection:
        connection.execute(
            "UPDATE auditor_actions SET finding_id='FIND-0001' WHERE action_id='ACT-9999'"
        )
    with pytest.raises(evidence_resolver.EvidenceIntegrityError, match="cross-run relationship"):
        evidence_resolver.build_entity_registry(
            database, RUN_ID, included_run_ids=("RUN-20260903-99",)
        )
