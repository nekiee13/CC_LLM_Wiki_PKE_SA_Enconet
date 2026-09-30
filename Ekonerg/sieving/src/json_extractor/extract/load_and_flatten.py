"""Normalize parsed sieving JSON into tabular records.

Adapted from pinned Enconet source. This module only handles already-parsed
objects; file reading, export and approval gates belong to other stages.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..config import get_config
from ..contract import load_contract


@dataclass
class ValidationError:
    file_path: str
    item_id: Optional[str]
    rule_id: str
    severity: str
    message: str


@dataclass
class FlattenResult:
    records: List[Dict[str, Any]]
    validation_errors: List[ValidationError] = field(default_factory=list)


_ENTITY_FIELDS = {
    "organizations": "entities_organizations",
    "people": "entities_people",
    "documents": "entities_documents",
    "systems_tools": "entities_systems_tools",
    "standards_regulations": "entities_standards_regulations",
}
_SOURCE_FIELDS = {
    "page": "source_page",
    "page_label": "source_page_label",
    "section_id": "source_section_id",
    "block_type": "source_block_type",
    "location_cue": "source_location_cue",
}
_RULE_FIELDS = {
    "source_rules": "rule_source_rules",
    "rule_locator": "rule_locator",
    "rule_key": "rule_key",
    "rule_strength": "rule_strength",
    "rule_citation_text": "rule_citation_text",
}


def _joined(values: List[str]) -> Optional[str]:
    return "; ".join(sorted(set(values))) if values else None


def _valid_entity_member(key: str, value: Any) -> bool:
    if isinstance(value, str):
        return True
    keys = {
        "people": ("name", "role"),
        "documents": ("identifier", "name", "revision"),
        "standards_regulations": ("identifier", "name"),
    }.get(key)
    return bool(keys and isinstance(value, dict)
                and all(isinstance(value.get(field, ""), str) for field in keys))


def flatten_entities(entities: Optional[Dict[str, Any]]) -> Dict[str, Optional[str]]:
    """Flatten valid entity lists without allowing malformed values to crash."""
    result = {column: None for column in _ENTITY_FIELDS.values()}
    if not isinstance(entities, dict):
        return result
    for source_key, column in _ENTITY_FIELDS.items():
        values = entities.get(source_key)
        if not isinstance(values, list):
            continue
        parts: List[str] = []
        for value in values:
            if not _valid_entity_member(source_key, value):
                continue
            if isinstance(value, str):
                parts.append(value)
            elif isinstance(value, dict) and source_key == "people":
                name, role = value.get("name", ""), value.get("role", "")
                if name:
                    parts.append(f"{name} ({role})" if role else name)
            elif isinstance(value, dict) and source_key == "documents":
                identifier, name, revision = (value.get(key, "") for key in ("identifier", "name", "revision"))
                pieces = [part for part in (identifier, name, f"Rev {revision}" if revision else "") if part]
                if pieces:
                    parts.append(": ".join(pieces) if identifier else " ".join(pieces))
            elif isinstance(value, dict) and source_key == "standards_regulations":
                identifier, name = value.get("identifier", ""), value.get("name", "")
                if identifier and name:
                    parts.append(f"{identifier}: {name}")
                elif identifier or name:
                    parts.append(identifier or name)
        result[column] = _joined(parts)
    return result


def flatten_source(source_list: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Use the first source entry for the source-location columns."""
    result: Dict[str, Any] = {column: None for column in _SOURCE_FIELDS.values()}
    result["source_heading_path"] = None
    if not isinstance(source_list, list) or not source_list or not isinstance(source_list[0], dict):
        return result
    source = source_list[0]
    for source_key, column in _SOURCE_FIELDS.items():
        result[column] = source.get(source_key)
    heading = source.get("heading_path")
    if isinstance(heading, list) and all(isinstance(part, str) for part in heading):
        result["source_heading_path"] = " > ".join(heading) if heading else None
    return result


def flatten_rule_fields(item: Dict[str, Any], record_side: str) -> Dict[str, Any]:
    result = {column: None for column in _RULE_FIELDS.values()}
    rule = item.get("rule") if record_side == "RULE" else None
    if isinstance(rule, dict):
        for source_key, column in _RULE_FIELDS.items():
            result[column] = rule.get(source_key)
    return result


def flatten_rule_references(item: Dict[str, Any], record_side: str) -> Dict[str, Any]:
    result = {key: None for key in ("rule_ref_keys", "rule_ref_codes", "rule_ref_locators", "rule_ref_texts_json")}
    if record_side != "DOCUMENT":
        return result
    keys = item.get("rule_reference_ids")
    if isinstance(keys, list) and keys and all(isinstance(key, str) for key in keys):
        result["rule_ref_keys"] = "; ".join(keys)
        pairs = [key.split("::", 1) for key in keys if "::" in key]
        result["rule_ref_codes"] = "; ".join(pair[0] for pair in pairs) if pairs else None
        result["rule_ref_locators"] = "; ".join(pair[1] for pair in pairs) if pairs else None
    references = item.get("rule_references")
    if isinstance(references, list):
        texts = [ref.get("ref_text") for ref in references
                 if isinstance(ref, dict) and isinstance(ref.get("ref_text"), str) and ref.get("ref_text")]
        result["rule_ref_texts_json"] = json.dumps(texts, ensure_ascii=False) if texts else None
    return result


def validate_item(item: Dict[str, Any], file_path: str, config) -> List[ValidationError]:
    """Return structured errors for taxonomy, evidence, provenance and sides."""
    errors: List[ValidationError] = []
    item_id = item.get("item_id", "UNKNOWN")

    def add(rule_id: str, message: str, severity: str = "ERROR") -> None:
        errors.append(ValidationError(file_path, item_id, rule_id, severity, message))

    template = load_contract()["template"]
    for field, expected in (("template_id", template["id"]),
                            ("template_version", template["version"])):
        if item.get(field) != expected:
            add("VAL-COMMON-001", f"{field} must be '{expected}', got '{item.get(field, '')}'")
    taxonomy_id = item.get("taxonomy_id", "")
    expected_taxonomy = template["taxonomy_id"]
    if taxonomy_id != expected_taxonomy:
        add("VAL-COMMON-001", f"taxonomy_id must be '{expected_taxonomy}', got '{taxonomy_id}'")

    criterion_id = item.get("criterion_id", "")
    valid_criteria = [entry["criterion_id"] for entry in config.get_canonical_criteria()]
    if criterion_id not in valid_criteria:
        add("VAL-TAX-001", f"criterion_id '{criterion_id}' not in canonical criteria")
    expected_name = config.criterion_name_for_id(criterion_id)
    criterion_name = item.get("criterion_name", "")
    if expected_name and criterion_name != expected_name:
        add("VAL-TAX-002", f"criterion_name '{criterion_name}' does not match canonical name '{expected_name}' for criterion_id '{criterion_id}'")

    quotes = item.get("evidence_quotes")
    if not isinstance(quotes, list) or not any(isinstance(quote, str) and quote.strip() for quote in quotes):
        add("VAL-EVID-001", "Item must have at least one non-empty evidence_quote")
    elif not all(isinstance(quote, str) for quote in quotes):
        add("VAL-EVID-001", "evidence_quotes must contain only strings")
    sources = item.get("source")
    if not isinstance(sources, list) or not sources or not all(isinstance(source, dict) for source in sources):
        add("VAL-PROV-001", "Item must have at least one source entry object")
    else:
        for source in sources:
            heading = source.get("heading_path")
            if heading is not None and (not isinstance(heading, list)
                                        or not all(isinstance(part, str) for part in heading)):
                add("VAL-PROV-001", "source.heading_path must be a list of strings")

    entities = item.get("entities")
    if entities is not None and not isinstance(entities, dict):
        add("VAL-ENTITY-001", "entities must be an object")
    elif isinstance(entities, dict):
        for key in _ENTITY_FIELDS:
            if key in entities and not isinstance(entities[key], list):
                add("VAL-ENTITY-001", f"entities.{key} must be a list")
            elif isinstance(entities.get(key), list) and not all(
                _valid_entity_member(key, value) for value in entities[key]
            ):
                add("VAL-ENTITY-001", f"entities.{key} contains a non-text member")

    side = item.get("record_side", "")
    if side not in ("RULE", "DOCUMENT"):
        add("VAL-SIDE-001", f"record_side must be RULE or DOCUMENT, got '{side}'")
    if side == "RULE":
        if item.get("rule_references") or item.get("rule_reference_ids"):
            add("VAL-RULELEAK-001", "RULE item must not have DOCUMENT-only fields (rule_references, rule_reference_ids)")
        rule = item.get("rule")
        if rule and not isinstance(rule, dict):
            add("VAL-JOIN-001", "rule must be an object for RULE item")
        elif isinstance(rule, dict) and rule:
            code = rule.get("source_rules", "")
            locator = rule.get("rule_locator", "")
            key = rule.get("rule_key", "")
            strength = rule.get("rule_strength", "")
            canonical = {entry["ref_code"]: entry for entry in config.get_canonical_codes()}
            if code and (not isinstance(code, str) or code not in canonical):
                add("VAL-JOIN-001", f"rule.source_rules '{code}' not in canonical code table")
            if not locator:
                add("VAL-JOIN-001", "rule.rule_locator is empty for RULE item")
            expected_key = f"{code}::{locator}" if code and locator else None
            if expected_key and key != expected_key:
                add("VAL-JOIN-001", f"rule.rule_key '{key}' does not match expected '{expected_key}'")
            if strength not in ("MANDATORY", "NON_MANDATORY"):
                add("VAL-JOIN-001", f"rule.rule_strength must be MANDATORY or NON_MANDATORY, got '{strength}'")
            source = canonical.get(code) if isinstance(code, str) else None
            if source and "allowed_locators" in source and locator not in source["allowed_locators"]:
                add("VAL-LOC-001", f"For {code}, rule_locator '{locator}' is not allowed")
            elif source and "locator_pattern" in source and (
                not isinstance(locator, str) or not re.fullmatch(source["locator_pattern"], locator)
            ):
                add("VAL-LOC-001", f"For {code}, rule_locator '{locator}' does not match the configured pattern")
    elif side == "DOCUMENT":
        if item.get("rule"):
            add("VAL-RULELEAK-002", "DOCUMENT item must not have 'rule' object (RULE-only field)")
        refs = item.get("rule_reference_ids")
        if refs and not isinstance(refs, list):
            add("VAL-JOIN-002", "rule_reference_ids must be a list")
        elif isinstance(refs, list):
            for ref_key in refs:
                if not isinstance(ref_key, str) or "::" not in ref_key:
                    add("VAL-JOIN-002", f"rule_reference_id '{ref_key}' does not match '<ref_code>::<ref_locator>' format", "WARNING")
    return errors


def flatten_item_to_record(
    item: Dict[str, Any], doc_metadata: Dict[str, Any], file_path: str, config,
) -> Tuple[Dict[str, Any], List[ValidationError]]:
    errors = validate_item(item, file_path, config)
    side = item.get("record_side", "")
    record = {
        "template_id": item.get("template_id"), "template_version": item.get("template_version"),
        "taxonomy_id": item.get("taxonomy_id"), "record_side": side,
        "doc_id": doc_metadata.get("doc_id"), "filename": doc_metadata.get("filename"),
        "title": doc_metadata.get("title"), "revision": doc_metadata.get("revision"),
        "item_id": item.get("item_id"), "item_type": item.get("item_type"),
        "criterion_id": item.get("criterion_id"), "criterion_name": item.get("criterion_name"),
        "statement": item.get("statement"),
    }
    quotes = item.get("evidence_quotes")
    if isinstance(quotes, list) and quotes and all(isinstance(quote, str) for quote in quotes):
        record["evidence_quote_1"] = next((quote for quote in quotes if quote.strip()), None)
        record["evidence_quotes_json"] = json.dumps(quotes, ensure_ascii=False)
    else:
        record["evidence_quote_1"] = None
        record["evidence_quotes_json"] = None
    record.update(flatten_source(item.get("source")))
    record.update(flatten_entities(item.get("entities")))
    record.update(flatten_rule_fields(item, side))
    record.update(flatten_rule_references(item, side))
    return record, errors


def flatten_json_to_records(data: Dict[str, Any], file_path: str, strict: bool = False) -> FlattenResult:
    """Flatten one parsed object and record schema drift without hiding it."""
    if not isinstance(data, dict):
        raise TypeError("sieving JSON root must be an object")
    config = get_config()
    errors: List[ValidationError] = []
    severity = "ERROR" if strict else "WARNING"

    def drift(item_id: Optional[str], message: str) -> None:
        errors.append(ValidationError(file_path, item_id, "VAL-DRIFT-001", severity, message))

    fields = load_contract()["input_fields"]
    root_required, root_allowed = (set(fields["root"][key]) for key in ("required", "allowed"))
    for key in sorted(set(data) - root_allowed):
        drift(None, f"unexpected field: root.{key}")
    for key in sorted(root_required - set(data)):
        drift(None, f"missing expected field: root.{key}")

    document = data.get("document", {})
    if not isinstance(document, dict):
        drift(None, "document must be an object")
        document = {}
    for key in sorted(set(fields["document"]["required"]) - set(document)):
        drift(None, f"missing expected field: document.{key}")
    for key in sorted(set(document) - set(fields["document"]["allowed"])):
        drift(None, f"unexpected field: document.{key}")
    control = document.get("control_metadata", {})
    if not isinstance(control, dict):
        drift(None, "document.control_metadata must be an object")
        control = {}
    for key in sorted(set(control) - set(fields["control_metadata"]["allowed"])):
        drift(None, f"unexpected field: document.control_metadata.{key}")
    metadata = {
        "doc_id": document.get("doc_id"), "filename": document.get("filename"),
        "title": document.get("title"), "revision": control.get("revision"),
    }

    items = data.get("items", [])
    if not isinstance(items, list):
        drift(None, "items must be a list")
        items = []
    required, allowed = (set(fields["item"][key]) for key in ("required", "allowed"))
    records: List[Dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            drift(None, f"items[{index}] must be an object")
            continue
        item_id = item.get("item_id")
        for key in sorted(required - set(item)):
            drift(item_id, f"missing expected field: items[{index}].{key}")
        for key in sorted(set(item) - allowed):
            drift(item_id, f"unexpected field: items[{index}].{key}")
        record, item_errors = flatten_item_to_record(item, metadata, file_path, config)
        records.append(record)
        errors.extend(item_errors)
    return FlattenResult(records, errors)


def flatten_multiple_files(
    json_data_list: List[Dict[str, Any]], file_paths: List[str], strict: bool = False,
) -> FlattenResult:
    """Keep every payload paired with its provenance path."""
    if len(json_data_list) != len(file_paths):
        raise ValueError("One file path is required for each JSON payload")
    records: List[Dict[str, Any]] = []
    errors: List[ValidationError] = []
    for data, path in zip(json_data_list, file_paths):
        result = flatten_json_to_records(data, path, strict=strict)
        records.extend(result.records)
        errors.extend(result.validation_errors)
    return FlattenResult(records, errors)
