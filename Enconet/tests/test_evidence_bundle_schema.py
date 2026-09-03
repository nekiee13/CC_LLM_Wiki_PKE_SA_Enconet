"""EA0.3 tests for the versioned evidence-bundle contract."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import validate_evidence_bundle as bundle_validation  # noqa: E402


def valid_bundle() -> dict:
    return {
        "schema_version": "1.0",
        "metadata": {
            "bundle_id": "EVIDENCE-BUNDLE-RUN-20260728-01",
            "run_id": "RUN-20260728-01",
            "supplier": "enconet",
            "framework": "appendix_b",
            "deliverable_language": "hr",
            "generated_at_utc": "2026-09-03T16:00:00Z",
            "generation_time_policy": "explicit_utc",
            "ordering_policy": "stable-id-v1",
        },
        "lineage": {
            "package": {
                "path": "outputs/enconet_appendix_b_evaluation_package.json",
                "sha256": "a" * 64,
            },
            "database": {"path": "db/nqa_audit.sqlite", "sha256": "b" * 64},
            "source_manifest": {
                "path": "manifests/raw_sources.csv",
                "sha256": "c" * 64,
            },
        },
        "documents": [
            {
                "document_id": "DOC-0021",
                "filename": "Poslovnik kvalitete.md",
                "title": "Poslovnik kvalitete",
                "language": "hr",
                "document_side": "DOCUMENT",
                "source_sha256": "d" * 64,
                "viewer_target": "#evidence/document/DOC-0021",
            }
        ],
        "chunks": [
            {
                "chunk_id": "CHUNK-DOC-0021-0105",
                "document_id": "DOC-0021",
                "sequence": 105,
                "heading_path": "4.1 Organizacija",
                "text": "Uprava društva — osiguranje kvalitete.",
                "char_start": 1200,
                "char_end": 1260,
                "source_sha256": "d" * 64,
                "previous_chunk_id": None,
                "next_chunk_id": None,
                "viewer_target": "#evidence/chunk/CHUNK-DOC-0021-0105",
            }
        ],
        "evaluations": [
            {
                "evaluation_id": "EVAL-APP_B_I",
                "criterion_id": "APP_B_I",
                "evidence_crumb_ids": ["CRUMB-DOC-0021-APP_B_I-0003"],
                "gap_ids": ["GAP-APP_B_I-01"],
                "viewer_target": "#evidence/evaluation/EVAL-APP_B_I",
            }
        ],
        "crumbs": [
            {
                "crumb_id": "CRUMB-DOC-0021-APP_B_I-0003",
                "document_id": "DOC-0021",
                "criterion_id": "APP_B_I",
                "document_side": "DOCUMENT",
                "statement": "Shema organizacije ločeno prikazuje osiguranje kvalitete.",
                "item_type": "evidence",
                "quote_ids": [
                    "QUOTE-DOC-0021-0105-01",
                    "QUOTE-DOC-0021-0105-02",
                ],
                "chunk_ids": ["CHUNK-DOC-0021-0105"],
                "evaluation_ids": ["EVAL-APP_B_I"],
                "viewer_target": "#evidence/crumb/CRUMB-DOC-0021-APP_B_I-0003",
            }
        ],
        "quotes": [
            {
                "quote_id": "QUOTE-DOC-0021-0105-01",
                "crumb_id": "CRUMB-DOC-0021-APP_B_I-0003",
                "source_order": 1,
                "text_original": "UPRAVA DRUŠTVA",
                "language": "hr",
                "source_locator": "4.1 Organizacija",
                "chunk_id": "CHUNK-DOC-0021-0105",
                "link_method": "exact",
                "confidence": 1.0,
                "viewer_target": "#evidence/quote/QUOTE-DOC-0021-0105-01",
            },
            {
                "quote_id": "QUOTE-DOC-0021-0105-02",
                "crumb_id": "CRUMB-DOC-0021-APP_B_I-0003",
                "source_order": 2,
                "text_original": "OSIGURANJE KVALITETE — področje kakovosti",
                "language": "hr",
                "source_locator": "4.1 Organizacija",
                "chunk_id": "CHUNK-DOC-0021-0105",
                "link_method": "exact",
                "confidence": 1.0,
                "viewer_target": "#evidence/quote/QUOTE-DOC-0021-0105-02",
            },
        ],
        "gaps": [
            {
                "gap_id": "GAP-APP_B_I-01",
                "evaluation_id": "EVAL-APP_B_I",
                "description": "Potrebna je dodatna potvrda odgovornosti.",
                "missing_evidence_ref": None,
                "evidence_crumb_id": "CRUMB-DOC-0021-APP_B_I-0003",
                "finding_ids": ["FIND-0001"],
                "action_ids": ["ACT-0001"],
                "viewer_target": "#evidence/gap/GAP-APP_B_I-01",
            }
        ],
        "findings": [
            {
                "finding_id": "FIND-0001",
                "evaluation_id": "EVAL-APP_B_I",
                "title": "Odgovornost nije potpuno dokazana",
                "body": "Potrebna je dodatna dokumentacija.",
                "gap_id": "GAP-APP_B_I-01",
                "evidence_crumb_id": "CRUMB-DOC-0021-APP_B_I-0003",
                "action_ids": ["ACT-0001"],
                "viewer_target": "#evidence/finding/FIND-0001",
            }
        ],
        "actions": [
            {
                "action_id": "ACT-0001",
                "description": "Dostaviti odobreni opis odgovornosti.",
                "priority": 1,
                "finding_id": "FIND-0001",
                "gap_id": "GAP-APP_B_I-01",
                "viewer_target": "#evidence/action/ACT-0001",
            }
        ],
    }


def _has_error(bundle: object, fragment: str) -> bool:
    return any(fragment in error for error in bundle_validation.validate(bundle))


def test_valid_bundle_and_machine_readable_schema_are_accepted():
    schema = json.loads(bundle_validation.SCHEMA.read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert bundle_validation.validate(valid_bundle()) == []


@pytest.mark.parametrize("field", ("metadata", "lineage", "documents", "quotes"))
def test_missing_and_extra_top_level_fields_are_rejected(field: str):
    missing = valid_bundle()
    del missing[field]
    assert _has_error(missing, f"missing field: bundle.{field}")
    extra = valid_bundle()
    extra["unexpected"] = True
    assert _has_error(extra, "extra field: bundle.unexpected")


def test_extra_nested_field_is_rejected():
    bundle = valid_bundle()
    bundle["quotes"][0]["unexpected"] = "not allowed"
    assert _has_error(bundle, "extra field: quote[0].unexpected")


@pytest.mark.parametrize(
    "mutation,fragment",
    (
        (lambda b: b["documents"][0].update(document_id="DOCUMENT-21"), "invalid document_id"),
        (lambda b: b["quotes"][0].update(source_order="1"), "wrong type: quote.source_order"),
        (lambda b: b["quotes"][0].update(confidence=1.5), "invalid confidence"),
        (lambda b: b["metadata"].update(generated_at_utc="today"), "invalid generated_at_utc"),
    ),
)
def test_invalid_ids_and_wrong_types_are_rejected(mutation, fragment: str):
    bundle = valid_bundle()
    mutation(bundle)
    assert _has_error(bundle, fragment)


def test_duplicate_quote_ids_and_source_positions_are_rejected():
    duplicate_id = valid_bundle()
    duplicate_id["quotes"][1]["quote_id"] = duplicate_id["quotes"][0]["quote_id"]
    assert _has_error(duplicate_id, "duplicate quote_id")

    duplicate_order = valid_bundle()
    duplicate_order["quotes"][1]["source_order"] = 1
    assert _has_error(duplicate_order, "duplicate quote source_order")

    skipped_order = valid_bundle()
    skipped_order["quotes"][1]["source_order"] = 3
    assert _has_error(skipped_order, "non-contiguous quote source_order")


@pytest.mark.parametrize(
    "mutation,fragment",
    (
        (lambda b: b["crumbs"][0].update(document_id="DOC-9999"), "orphan document reference"),
        (lambda b: b["crumbs"][0].update(quote_ids=["QUOTE-DOC-0021-9999-01"]), "orphan quote reference"),
        (lambda b: b["quotes"][0].update(chunk_id="CHUNK-DOC-0021-9999"), "orphan chunk reference"),
        (lambda b: b["gaps"][0].update(evaluation_id="EVAL-APP_B_II"), "orphan evaluation reference"),
        (lambda b: b["quotes"][0].update(crumb_id="CRUMB-DOC-0021-APP_B_I-9999"), "orphan crumb reference"),
    ),
)
def test_orphan_entity_references_are_rejected(mutation, fragment: str):
    bundle = valid_bundle()
    mutation(bundle)
    assert _has_error(bundle, fragment)


def test_unsupported_schema_version_and_incomplete_lineage_are_rejected():
    version = valid_bundle()
    version["schema_version"] = "2.0"
    assert _has_error(version, "unsupported schema_version")

    lineage = valid_bundle()
    del lineage["lineage"]["database"]["sha256"]
    assert _has_error(lineage, "missing field: lineage.database.sha256")


def test_source_quote_order_unicode_and_canonical_bytes_are_preserved():
    bundle = valid_bundle()
    assert bundle_validation.validate(bundle) == []
    encoded = bundle_validation.canonical_bytes(bundle)
    assert "DRUŠTVA".encode() in encoded
    assert "področje kakovosti".encode() in encoded
    assert encoded == bundle_validation.canonical_bytes(copy.deepcopy(bundle))

    reversed_quotes = valid_bundle()
    reversed_quotes["quotes"].reverse()
    assert _has_error(reversed_quotes, "non-deterministic order: quotes")


def test_entity_indexes_must_match_their_referenced_records():
    bundle = valid_bundle()
    bundle["crumbs"][0]["quote_ids"] = ["QUOTE-DOC-0021-0105-01"]
    assert _has_error(bundle, "inconsistent quote index")

    bundle = valid_bundle()
    bundle["evaluations"][0]["evidence_crumb_ids"] = []
    assert _has_error(bundle, "inconsistent evaluation evidence index")
