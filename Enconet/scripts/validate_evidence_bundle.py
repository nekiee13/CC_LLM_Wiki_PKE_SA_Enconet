#!/usr/bin/env python3
"""Validate the versioned offline evidence bundle."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

import evidence_navigation


ENCONET = Path(__file__).resolve().parents[1]
SCHEMA = ENCONET / "schemas" / "evidence_bundle.schema.json"
ID_PATTERNS = ENCONET / "schemas" / "id_patterns.yml"

ROOT_FIELDS = {
    "schema_version", "metadata", "lineage", "documents", "chunks", "evaluations",
    "crumbs", "quotes", "gaps", "findings", "actions",
}
METADATA_FIELDS = {
    "bundle_id", "run_id", "supplier", "framework", "deliverable_language",
    "generated_at_utc", "generation_time_policy", "ordering_policy",
}
LINEAGE_FIELDS = {"package", "database", "source_manifest"}
LINEAGE_ENTRY_FIELDS = {"path", "sha256"}
ENTITY_FIELDS = {
    "documents": {
        "document_id", "filename", "title", "language", "document_side", "source_sha256",
        "viewer_target",
    },
    "chunks": {
        "chunk_id", "document_id", "sequence", "heading_path", "text", "char_start",
        "char_end", "source_sha256", "previous_chunk_id", "next_chunk_id", "viewer_target",
    },
    "evaluations": {
        "evaluation_id", "criterion_id", "evidence_crumb_ids", "gap_ids", "viewer_target",
    },
    "crumbs": {
        "crumb_id", "document_id", "criterion_id", "document_side", "statement", "item_type",
        "quote_ids", "chunk_ids", "evaluation_ids", "viewer_target",
    },
    "quotes": {
        "quote_id", "crumb_id", "source_order", "text_original", "language",
        "source_locator", "chunk_id", "link_method", "confidence", "viewer_target",
    },
    "gaps": {
        "gap_id", "evaluation_id", "description", "missing_evidence_ref", "evidence_crumb_id",
        "finding_ids", "action_ids", "viewer_target",
    },
    "findings": {
        "finding_id", "evaluation_id", "title", "body", "gap_id", "evidence_crumb_id",
        "action_ids", "viewer_target",
    },
    "actions": {
        "action_id", "description", "priority", "finding_id", "gap_id", "viewer_target",
    },
}
ID_FIELD_PATTERN = {
    "document_id": "doc_id", "chunk_id": "chunk_id", "evaluation_id": "evaluation_id",
    "crumb_id": "crumb_id", "quote_id": "quote_id", "gap_id": "gap_id",
    "finding_id": "finding_id", "action_id": "action_id", "run_id": "run_id",
}
VIEWER_TYPES = {
    "documents": ("document", "document_id"), "chunks": ("chunk", "chunk_id"),
    "evaluations": ("evaluation", "evaluation_id"), "crumbs": ("crumb", "crumb_id"),
    "quotes": ("quote", "quote_id"), "gaps": ("gap", "gap_id"),
    "findings": ("finding", "finding_id"), "actions": ("action", "action_id"),
}


def canonical_bytes(bundle: dict) -> bytes:
    """Return stable readable UTF-8 JSON bytes."""
    return (
        json.dumps(bundle, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _shape(value: Any, fields: set[str], path: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"wrong type: {path}")
        return False
    for field in sorted(fields - set(value)):
        errors.append(f"missing field: {path}.{field}")
    for field in sorted(set(value) - fields):
        errors.append(f"extra field: {path}.{field}")
    return fields <= set(value)


def _patterns() -> dict[str, re.Pattern[str]]:
    data = yaml.safe_load(ID_PATTERNS.read_text(encoding="utf-8"))["patterns"]
    return {name: re.compile(spec["regex"]) for name, spec in data.items()}


def _valid_id(value: Any, field: str, path: str, patterns: dict[str, re.Pattern[str]],
              errors: list[str]) -> bool:
    pattern_name = ID_FIELD_PATTERN[field]
    if not isinstance(value, str) or patterns[pattern_name].fullmatch(value) is None:
        errors.append(f"invalid {field}: {path}")
        return False
    return True


def _strings(value: Any, path: str, errors: list[str]) -> bool:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"wrong type: {path}")
        return False
    if len(value) != len(set(value)):
        errors.append(f"duplicate reference: {path}")
        return False
    return True


def _nonempty(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
        errors.append(f"wrong type: {path}")


def _index(rows: list[dict], id_field: str, errors: list[str]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for row in rows:
        identifier = row.get(id_field)
        if isinstance(identifier, str):
            if identifier in result:
                errors.append(f"duplicate {id_field}: {identifier}")
            else:
                result[identifier] = row
    return result


def _orphan(value: Any, available: set[str], kind: str, owner: str, errors: list[str]) -> None:
    if value is not None and value not in available:
        errors.append(f"orphan {kind} reference: {owner} -> {value}")


def _orphan_many(values: Any, available: set[str], kind: str, owner: str,
                 errors: list[str]) -> None:
    if isinstance(values, list):
        for value in values:
            _orphan(value, available, kind, owner, errors)


def validate(bundle: object, schema_path: Path = SCHEMA) -> list[str]:
    """Return deterministic structural and cross-reference errors without mutating the bundle."""
    errors: list[str] = []
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append("unsupported evidence bundle schema declaration")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"evidence bundle schema unavailable: {exc}"]

    if not _shape(bundle, ROOT_FIELDS, "bundle", errors):
        return errors
    assert isinstance(bundle, dict)
    if bundle["schema_version"] != "1.0":
        errors.append(f"unsupported schema_version: {bundle['schema_version']}")

    metadata = bundle["metadata"]
    if _shape(metadata, METADATA_FIELDS, "metadata", errors):
        patterns = _patterns()
        _valid_id(metadata["run_id"], "run_id", "metadata.run_id", patterns, errors)
        expected_bundle_id = f"EVIDENCE-BUNDLE-{metadata['run_id']}"
        if metadata["bundle_id"] != expected_bundle_id:
            errors.append("invalid bundle_id")
        for field in ("supplier", "framework"):
            if not isinstance(metadata[field], str) or re.fullmatch(r"[a-z0-9_-]+", metadata[field]) is None:
                errors.append(f"invalid metadata.{field}")
        if metadata["deliverable_language"] not in {"hr", "sl", "en"}:
            errors.append("invalid metadata.deliverable_language")
        if not isinstance(metadata["generated_at_utc"], str) or re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", metadata["generated_at_utc"]
        ) is None:
            errors.append("invalid generated_at_utc")
        if metadata["generation_time_policy"] not in {"explicit_utc", "source_date_epoch_utc"}:
            errors.append("invalid generation_time_policy")
        if metadata["ordering_policy"] != "stable-id-v1":
            errors.append("unsupported ordering_policy")
    else:
        patterns = _patterns()

    lineage = bundle["lineage"]
    if _shape(lineage, LINEAGE_FIELDS, "lineage", errors):
        for name in sorted(LINEAGE_FIELDS):
            entry = lineage[name]
            if _shape(entry, LINEAGE_ENTRY_FIELDS, f"lineage.{name}", errors):
                path = entry["path"]
                if (not isinstance(path, str) or not path or Path(path).is_absolute()
                        or ".." in Path(path).parts):
                    errors.append(f"invalid lineage path: {name}")
                if not isinstance(entry["sha256"], str) or re.fullmatch(
                    r"[0-9a-f]{64}", entry["sha256"]
                ) is None:
                    errors.append(f"invalid lineage sha256: {name}")

    collections: dict[str, list[dict]] = {}
    for name, fields in ENTITY_FIELDS.items():
        value = bundle[name]
        if not isinstance(value, list):
            errors.append(f"wrong type: bundle.{name}")
            collections[name] = []
            continue
        collections[name] = []
        singular = name[:-1] if name != "entities" else "entity"
        for index, row in enumerate(value):
            if _shape(row, fields, f"{singular}[{index}]", errors):
                collections[name].append(row)

    id_fields = {
        "documents": "document_id", "chunks": "chunk_id", "evaluations": "evaluation_id",
        "crumbs": "crumb_id", "quotes": "quote_id", "gaps": "gap_id",
        "findings": "finding_id", "actions": "action_id",
    }
    indexes: dict[str, dict[str, dict]] = {}
    for name, id_field in id_fields.items():
        for index, row in enumerate(collections[name]):
            _valid_id(row[id_field], id_field, f"{name}[{index}].{id_field}", patterns, errors)
        indexes[name] = _index(collections[name], id_field, errors)

    string_fields = {
        "documents": ("filename", "title", "language", "source_sha256"),
        "chunks": ("heading_path", "text", "source_sha256"),
        "evaluations": ("criterion_id",),
        "crumbs": ("criterion_id", "statement", "item_type"),
        "quotes": ("text_original", "language", "source_locator", "link_method"),
        "gaps": ("description",), "findings": ("title", "body"),
        "actions": ("description",),
    }
    for name, fields in string_fields.items():
        for row in collections[name]:
            for field in fields:
                _nonempty(row[field], f"{name[:-1]}.{field}", errors)

    for row in collections["documents"]:
        if row["document_side"] not in {"RULE", "DOCUMENT"}:
            errors.append("invalid document.document_side")
        if not isinstance(row["source_sha256"], str) or re.fullmatch(r"[0-9a-f]{64}", row["source_sha256"]) is None:
            errors.append("invalid document.source_sha256")
    for row in collections["crumbs"]:
        if row["document_side"] not in {"RULE", "DOCUMENT"}:
            errors.append("invalid crumb.document_side")
        for field in ("quote_ids", "chunk_ids", "evaluation_ids"):
            _strings(row[field], f"crumb.{field}", errors)
    for row in collections["evaluations"]:
        _strings(row["evidence_crumb_ids"], "evaluation.evidence_crumb_ids", errors)
        _strings(row["gap_ids"], "evaluation.gap_ids", errors)
    for row in collections["gaps"]:
        _strings(row["finding_ids"], "gap.finding_ids", errors)
        _strings(row["action_ids"], "gap.action_ids", errors)
    for row in collections["findings"]:
        _strings(row["action_ids"], "finding.action_ids", errors)

    for row in collections["chunks"]:
        for field in ("sequence", "char_start", "char_end"):
            if not isinstance(row[field], int) or isinstance(row[field], bool) or row[field] < 0:
                errors.append(f"wrong type: chunk.{field}")
        if (isinstance(row["char_start"], int) and isinstance(row["char_end"], int)
                and row["char_end"] < row["char_start"]):
            errors.append("invalid chunk character range")
    for row in collections["quotes"]:
        if not isinstance(row["source_order"], int) or isinstance(row["source_order"], bool):
            errors.append("wrong type: quote.source_order")
        elif row["source_order"] < 1:
            errors.append("invalid quote.source_order")
        confidence = row["confidence"]
        if (not isinstance(confidence, (int, float)) or isinstance(confidence, bool)
                or not 0 <= confidence <= 1):
            errors.append("invalid confidence")
    for row in collections["actions"]:
        if (not isinstance(row["priority"], int) or isinstance(row["priority"], bool)
                or row["priority"] not in {0, 1}):
            errors.append("wrong type: action.priority")

    for name, (viewer_type, id_field) in VIEWER_TYPES.items():
        for row in collections[name]:
            try:
                expected_target = evidence_navigation.target(viewer_type, row[id_field])
            except (TypeError, ValueError):
                expected_target = None
            if row["viewer_target"] != expected_target:
                errors.append(f"invalid viewer_target: {row.get(id_field)}")

    order_keys = {
        "documents": lambda row: str(row.get("document_id", "")),
        "chunks": lambda row: (str(row.get("document_id", "")),
                               row.get("sequence") if isinstance(row.get("sequence"), int) else -1,
                               str(row.get("chunk_id", ""))),
        "evaluations": lambda row: str(row.get("evaluation_id", "")),
        "crumbs": lambda row: str(row.get("crumb_id", "")),
        "quotes": lambda row: (str(row.get("crumb_id", "")),
                               row.get("source_order") if isinstance(row.get("source_order"), int) else -1,
                               str(row.get("quote_id", ""))),
        "gaps": lambda row: str(row.get("gap_id", "")),
        "findings": lambda row: str(row.get("finding_id", "")),
        "actions": lambda row: str(row.get("action_id", "")),
    }
    for name, key in order_keys.items():
        if collections[name] != sorted(collections[name], key=key):
            errors.append(f"non-deterministic order: {name}")

    quote_positions: set[tuple[Any, Any]] = set()
    positions_by_crumb: dict[str, list[int]] = {}
    for row in collections["quotes"]:
        position = (row["crumb_id"], row["source_order"])
        if position in quote_positions:
            errors.append(f"duplicate quote source_order: {position[0]} {position[1]}")
        quote_positions.add(position)
        if isinstance(row["crumb_id"], str) and isinstance(row["source_order"], int):
            positions_by_crumb.setdefault(row["crumb_id"], []).append(row["source_order"])
    for crumb_id, positions in positions_by_crumb.items():
        if sorted(positions) != list(range(1, len(positions) + 1)):
            errors.append(f"non-contiguous quote source_order: {crumb_id}")

    ids = {name: set(index) for name, index in indexes.items()}
    for row in collections["chunks"]:
        _orphan(row["document_id"], ids["documents"], "document", row["chunk_id"], errors)
        _orphan(row["previous_chunk_id"], ids["chunks"], "chunk", row["chunk_id"], errors)
        _orphan(row["next_chunk_id"], ids["chunks"], "chunk", row["chunk_id"], errors)
    for row in collections["evaluations"]:
        _orphan_many(row["evidence_crumb_ids"], ids["crumbs"], "crumb", row["evaluation_id"], errors)
        _orphan_many(row["gap_ids"], ids["gaps"], "gap", row["evaluation_id"], errors)
    for row in collections["crumbs"]:
        _orphan(row["document_id"], ids["documents"], "document", row["crumb_id"], errors)
        _orphan_many(row["quote_ids"], ids["quotes"], "quote", row["crumb_id"], errors)
        _orphan_many(row["chunk_ids"], ids["chunks"], "chunk", row["crumb_id"], errors)
        _orphan_many(row["evaluation_ids"], ids["evaluations"], "evaluation", row["crumb_id"], errors)
    for row in collections["quotes"]:
        _orphan(row["crumb_id"], ids["crumbs"], "crumb", row["quote_id"], errors)
        _orphan(row["chunk_id"], ids["chunks"], "chunk", row["quote_id"], errors)
    for row in collections["gaps"]:
        _orphan(row["evaluation_id"], ids["evaluations"], "evaluation", row["gap_id"], errors)
        _orphan(row["evidence_crumb_id"], ids["crumbs"], "crumb", row["gap_id"], errors)
        _orphan_many(row["finding_ids"], ids["findings"], "finding", row["gap_id"], errors)
        _orphan_many(row["action_ids"], ids["actions"], "action", row["gap_id"], errors)
    for row in collections["findings"]:
        _orphan(row["evaluation_id"], ids["evaluations"], "evaluation", row["finding_id"], errors)
        _orphan(row["gap_id"], ids["gaps"], "gap", row["finding_id"], errors)
        _orphan(row["evidence_crumb_id"], ids["crumbs"], "crumb", row["finding_id"], errors)
        _orphan_many(row["action_ids"], ids["actions"], "action", row["finding_id"], errors)
    for row in collections["actions"]:
        _orphan(row["finding_id"], ids["findings"], "finding", row["action_id"], errors)
        _orphan(row["gap_id"], ids["gaps"], "gap", row["action_id"], errors)

    for crumb in collections["crumbs"]:
        related_quotes = sorted(
            (quote for quote in collections["quotes"] if quote["crumb_id"] == crumb["crumb_id"]),
            key=lambda quote: (
                quote["source_order"] if isinstance(quote["source_order"], int) else -1,
                str(quote["quote_id"]),
            ),
        )
        expected_quote_ids = [quote["quote_id"] for quote in related_quotes]
        if crumb["quote_ids"] != expected_quote_ids:
            errors.append(f"inconsistent quote index: {crumb['crumb_id']}")
        expected_chunk_ids = sorted({quote["chunk_id"] for quote in related_quotes})
        if crumb["chunk_ids"] != expected_chunk_ids:
            errors.append(f"inconsistent chunk index: {crumb['crumb_id']}")

    for evaluation in collections["evaluations"]:
        expected_crumb_ids = sorted(
            crumb["crumb_id"] for crumb in collections["crumbs"]
            if evaluation["evaluation_id"] in crumb["evaluation_ids"]
        )
        if evaluation["evidence_crumb_ids"] != expected_crumb_ids:
            errors.append(
                f"inconsistent evaluation evidence index: {evaluation['evaluation_id']}"
            )
        expected_gap_ids = sorted(
            gap["gap_id"] for gap in collections["gaps"]
            if gap["evaluation_id"] == evaluation["evaluation_id"]
        )
        if evaluation["gap_ids"] != expected_gap_ids:
            errors.append(f"inconsistent evaluation gap index: {evaluation['evaluation_id']}")

    return sorted(set(errors))
