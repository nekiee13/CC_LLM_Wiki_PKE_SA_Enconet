# ------------------------
# src/json_extractor/extract/load_and_flatten.py
# ------------------------
"""
Load and flatten JSON extraction files into normalized tabular records.

Implements:
- JSON_Template_App_B schema parsing
- Entity flattening (structured objects → semicolon-joined strings)
- RULE vs DOCUMENT field separation
- Validation with structured error collection
- Deterministic join key construction
"""

import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from ..config import get_config
from ..contract import load_contract


@dataclass
class ValidationError:
    """A single validation error."""
    file_path: str
    item_id: Optional[str]
    rule_id: str  # e.g., "VAL-TAX-001"
    severity: str  # "ERROR" or "WARNING"
    message: str


@dataclass
class FlattenResult:
    """Result of flattening operation."""
    records: List[Dict[str, Any]]
    validation_errors: List[ValidationError] = field(default_factory=list)


def flatten_entities(entities: Optional[Dict[str, Any]]) -> Dict[str, Optional[str]]:
    """
    Flatten entity structures to semicolon-joined strings.
    
    Args:
        entities: Entity dict from JSON with structured lists.
    
    Returns:
        Dict with flattened string values:
        - entities_organizations
        - entities_people
        - entities_documents
        - entities_systems_tools
        - entities_standards_regulations
    """
    if not entities:
        return {
            "entities_organizations": None,
            "entities_people": None,
            "entities_documents": None,
            "entities_systems_tools": None,
            "entities_standards_regulations": None,
        }
    
    # Organizations: simple list of strings
    orgs = entities.get("organizations", [])
    orgs_str = "; ".join(sorted(set(orgs))) if orgs else None
    
    # People: [{name, role}] → "Name (Role)" or "Name"
    people = entities.get("people", [])
    people_parts = []
    for person in people:
        if isinstance(person, dict):
            name = person.get("name", "")
            role = person.get("role", "")
            if name and role:
                people_parts.append(f"{name} ({role})")
            elif name:
                people_parts.append(name)
        elif isinstance(person, str):
            people_parts.append(person)
    people_str = "; ".join(sorted(set(people_parts))) if people_parts else None
    
    # Documents: [{name, identifier, revision}] → "Identifier: Name Rev" variants
    docs = entities.get("documents", [])
    doc_parts = []
    for doc in docs:
        if isinstance(doc, dict):
            identifier = doc.get("identifier", "")
            name = doc.get("name", "")
            revision = doc.get("revision", "")
            
            parts = []
            if identifier:
                parts.append(identifier)
            if name:
                parts.append(name)
            if revision:
                parts.append(f"Rev {revision}")
            
            if parts:
                doc_parts.append(": ".join(parts) if identifier else " ".join(parts))
        elif isinstance(doc, str):
            doc_parts.append(doc)
    docs_str = "; ".join(sorted(set(doc_parts))) if doc_parts else None
    
    # Systems/Tools: simple list
    systems = entities.get("systems_tools", [])
    systems_str = "; ".join(sorted(set(systems))) if systems else None
    
    # Standards/Regulations: [{name, identifier}] → "Identifier: Name"
    standards = entities.get("standards_regulations", [])
    std_parts = []
    for std in standards:
        if isinstance(std, dict):
            identifier = std.get("identifier", "")
            name = std.get("name", "")
            if identifier and name:
                std_parts.append(f"{identifier}: {name}")
            elif identifier:
                std_parts.append(identifier)
            elif name:
                std_parts.append(name)
        elif isinstance(std, str):
            std_parts.append(std)
    std_str = "; ".join(sorted(set(std_parts))) if std_parts else None
    
    return {
        "entities_organizations": orgs_str,
        "entities_people": people_str,
        "entities_documents": docs_str,
        "entities_systems_tools": systems_str,
        "entities_standards_regulations": std_str,
    }


def flatten_source(source_list: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Flatten source provenance list to primary source fields.
    
    Uses first source entry for primary fields.
    
    Args:
        source_list: List of source objects.
    
    Returns:
        Dict with source_page, source_page_label, source_heading_path,
        source_section_id, source_block_type, source_location_cue.
    """
    if not source_list or not isinstance(source_list, list) or len(source_list) == 0:
        return {
            "source_page": None,
            "source_page_label": None,
            "source_heading_path": None,
            "source_section_id": None,
            "source_block_type": None,
            "source_location_cue": None,
        }
    
    # Use first source
    source = source_list[0]
    
    heading_path = source.get("heading_path", [])
    heading_path_str = " > ".join(heading_path) if heading_path else None
    
    return {
        "source_page": source.get("page"),
        "source_page_label": source.get("page_label"),
        "source_heading_path": heading_path_str,
        "source_section_id": source.get("section_id"),
        "source_block_type": source.get("block_type"),
        "source_location_cue": source.get("location_cue"),
    }


def flatten_rule_fields(item: Dict[str, Any], record_side: str) -> Dict[str, Any]:
    """
    Extract RULE-specific fields.
    
    Args:
        item: Item dict from JSON.
        record_side: "RULE" or "DOCUMENT".
    
    Returns:
        Dict with rule_source_rules, rule_locator, rule_key, rule_strength, rule_citation_text.
        All None if record_side is DOCUMENT.
    """
    if record_side != "RULE":
        return {
            "rule_source_rules": None,
            "rule_locator": None,
            "rule_key": None,
            "rule_strength": None,
            "rule_citation_text": None,
        }
    
    rule = item.get("rule", {})
    if not rule:
        return {
            "rule_source_rules": None,
            "rule_locator": None,
            "rule_key": None,
            "rule_strength": None,
            "rule_citation_text": None,
        }
    
    return {
        "rule_source_rules": rule.get("source_rules"),
        "rule_locator": rule.get("rule_locator"),
        "rule_key": rule.get("rule_key"),
        "rule_strength": rule.get("rule_strength"),
        "rule_citation_text": rule.get("rule_citation_text"),
    }


def flatten_rule_references(item: Dict[str, Any], record_side: str) -> Dict[str, Any]:
    """
    Extract DOCUMENT-specific rule reference fields.
    
    Args:
        item: Item dict from JSON.
        record_side: "RULE" or "DOCUMENT".
    
    Returns:
        Dict with rule_ref_keys, rule_ref_codes, rule_ref_locators, rule_ref_texts_json.
        All None if record_side is RULE.
    """
    if record_side != "DOCUMENT":
        return {
            "rule_ref_keys": None,
            "rule_ref_codes": None,
            "rule_ref_locators": None,
            "rule_ref_texts_json": None,
        }
    
    # Use rule_reference_ids if present (pre-computed join keys)
    rule_reference_ids = item.get("rule_reference_ids", [])
    if rule_reference_ids:
        rule_ref_keys_str = "; ".join(rule_reference_ids)
        
        # Extract codes and locators from keys
        codes = []
        locators = []
        for ref_key in rule_reference_ids:
            if "::" in ref_key:
                code, locator = ref_key.split("::", 1)
                codes.append(code)
                locators.append(locator)
        
        codes_str = "; ".join(codes) if codes else None
        locators_str = "; ".join(locators) if locators else None
    else:
        rule_ref_keys_str = None
        codes_str = None
        locators_str = None
    
    # Extract ref texts from rule_references array
    rule_references = item.get("rule_references", [])
    ref_texts = []
    for ref in rule_references:
        if isinstance(ref, dict):
            ref_text = ref.get("ref_text", "")
            if ref_text:
                ref_texts.append(ref_text)
    
    ref_texts_json = json.dumps(ref_texts, ensure_ascii=False) if ref_texts else None
    
    return {
        "rule_ref_keys": rule_ref_keys_str,
        "rule_ref_codes": codes_str,
        "rule_ref_locators": locators_str,
        "rule_ref_texts_json": ref_texts_json,
    }


def validate_item(
    item: Dict[str, Any],
    file_path: str,
    config
) -> List[ValidationError]:
    """
    Validate a single item against template rules.
    
    Args:
        item: Item dict from JSON.
        file_path: Source file path for error reporting.
        config: Config instance.
    
    Returns:
        List of ValidationError objects.
    """
    errors = []
    item_id = item.get("item_id", "UNKNOWN")
    
    # VAL-COMMON-001: Template identity
    template_id = item.get("template_id", "")
    template_version = item.get("template_version", "")
    taxonomy_id = item.get("taxonomy_id", "")
    
    if not template_id:
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-COMMON-001",
            severity="ERROR",
            message="template_id is empty"
        ))
    
    if not template_version:
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-COMMON-001",
            severity="ERROR",
            message="template_version is empty"
        ))
    
    if taxonomy_id != "APP_B":
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-COMMON-001",
            severity="ERROR",
            message=f"taxonomy_id must be 'APP_B', got '{taxonomy_id}'"
        ))
    
    # VAL-TAX-001: criterion_id validation
    criterion_id = item.get("criterion_id", "")
    valid_criteria = [c["criterion_id"] for c in config.get_canonical_criteria()]
    if criterion_id not in valid_criteria:
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-TAX-001",
            severity="ERROR",
            message=f"criterion_id '{criterion_id}' not in canonical criteria"
        ))
    
    # VAL-TAX-002: criterion_name match
    criterion_name = item.get("criterion_name", "")
    expected_name = config.criterion_name_for_id(criterion_id)
    if expected_name and criterion_name != expected_name:
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-TAX-002",
            severity="ERROR",
            message=f"criterion_name '{criterion_name}' does not match canonical name '{expected_name}' for criterion_id '{criterion_id}'"
        ))
    
    # VAL-EVID-001: Evidence requirement
    evidence_quotes = item.get("evidence_quotes", [])
    if not evidence_quotes or all(not quote for quote in evidence_quotes):
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-EVID-001",
            severity="ERROR",
            message="Item must have at least one non-empty evidence_quote"
        ))
    
    # VAL-PROV-001: Provenance requirement
    source = item.get("source", [])
    if not source:
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-PROV-001",
            severity="ERROR",
            message="Item must have at least one source entry"
        ))
    
    # Record-side specific validation
    record_side = item.get("record_side", "")
    if record_side not in ("RULE", "DOCUMENT"):
        errors.append(ValidationError(
            file_path=file_path,
            item_id=item_id,
            rule_id="VAL-SIDE-001",
            severity="ERROR",
            message=f"record_side must be RULE or DOCUMENT, got '{record_side}'"
        ))
    
    if record_side == "RULE":
        # VAL-RULELEAK-001: RULE must not have DOCUMENT fields
        if any([
            item.get("rule_references"),
            item.get("rule_reference_ids"),
        ]):
            errors.append(ValidationError(
                file_path=file_path,
                item_id=item_id,
                rule_id="VAL-RULELEAK-001",
                severity="ERROR",
                message="RULE item must not have DOCUMENT-only fields (rule_references, rule_reference_ids)"
            ))
        
        # VAL-JOIN-001: RULE join key validation
        rule = item.get("rule", {})
        if rule:
            source_rules = rule.get("source_rules", "")
            rule_locator = rule.get("rule_locator", "")
            rule_key = rule.get("rule_key", "")
            rule_strength = rule.get("rule_strength", "")
            
            # Check source_rules is canonical
            canonical_codes = [c["ref_code"] for c in config.get_canonical_codes()]
            if source_rules and source_rules not in canonical_codes:
                errors.append(ValidationError(
                    file_path=file_path,
                    item_id=item_id,
                    rule_id="VAL-JOIN-001",
                    severity="ERROR",
                    message=f"rule.source_rules '{source_rules}' not in canonical code table"
                ))
            
            # Check locator is non-empty
            if not rule_locator:
                errors.append(ValidationError(
                    file_path=file_path,
                    item_id=item_id,
                    rule_id="VAL-JOIN-001",
                    severity="ERROR",
                    message="rule.rule_locator is empty for RULE item"
                ))
            
            # Check rule_key determinism
            expected_key = f"{source_rules}::{rule_locator}" if source_rules and rule_locator else None
            if expected_key and rule_key != expected_key:
                errors.append(ValidationError(
                    file_path=file_path,
                    item_id=item_id,
                    rule_id="VAL-JOIN-001",
                    severity="ERROR",
                    message=f"rule.rule_key '{rule_key}' does not match expected '{expected_key}'"
                ))
            
            # Check rule_strength
            if rule_strength not in ["MANDATORY", "NON_MANDATORY"]:
                errors.append(ValidationError(
                    file_path=file_path,
                    item_id=item_id,
                    rule_id="VAL-JOIN-001",
                    severity="ERROR",
                    message=f"rule.rule_strength must be MANDATORY or NON_MANDATORY, got '{rule_strength}'"
                ))
            
            # VAL-LOC-001: Locator normalization
            if source_rules == "10CFR50_APPB":
                if rule_locator not in valid_criteria:
                    errors.append(ValidationError(
                        file_path=file_path,
                        item_id=item_id,
                        rule_id="VAL-LOC-001",
                        severity="ERROR",
                        message=f"For 10CFR50_APPB, rule_locator '{rule_locator}' must be a valid criterion_id"
                    ))
            elif source_rules == "10CFR21":
                import re
                if not re.match(r"^21\.[0-9]+$", rule_locator):
                    errors.append(ValidationError(
                        file_path=file_path,
                        item_id=item_id,
                        rule_id="VAL-LOC-001",
                        severity="ERROR",
                        message=f"For 10CFR21, rule_locator '{rule_locator}' must match pattern '21.<n>'"
                    ))
    
    elif record_side == "DOCUMENT":
        # VAL-RULELEAK-002: DOCUMENT must not have RULE fields
        if item.get("rule"):
            errors.append(ValidationError(
                file_path=file_path,
                item_id=item_id,
                rule_id="VAL-RULELEAK-002",
                severity="ERROR",
                message="DOCUMENT item must not have 'rule' object (RULE-only field)"
            ))
        
        # VAL-JOIN-002: DOCUMENT reference key validation (WARNING)
        rule_reference_ids = item.get("rule_reference_ids", [])
        if rule_reference_ids:
            for ref_key in rule_reference_ids:
                if "::" not in ref_key:
                    errors.append(ValidationError(
                        file_path=file_path,
                        item_id=item_id,
                        rule_id="VAL-JOIN-002",
                        severity="WARNING",
                        message=f"rule_reference_id '{ref_key}' does not match '<ref_code>::<ref_locator>' format"
                    ))
    
    return errors


def flatten_item_to_record(
    item: Dict[str, Any],
    doc_metadata: Dict[str, Any],
    file_path: str,
    config
) -> Tuple[Dict[str, Any], List[ValidationError]]:
    """
    Flatten a single JSON item to a normalized record.
    
    Args:
        item: Item dict from JSON.
        doc_metadata: Document-level metadata (doc_id, filename, title, revision).
        file_path: Source file path for error reporting.
        config: Config instance.
    
    Returns:
        Tuple of (normalized_record, validation_errors).
    """
    # Validate first
    errors = validate_item(item, file_path, config)
    
    record_side = item.get("record_side", "")
    
    # Core fields
    record = {
        "template_id": item.get("template_id"),
        "template_version": item.get("template_version"),
        "taxonomy_id": item.get("taxonomy_id"),
        "record_side": record_side,
        "doc_id": doc_metadata.get("doc_id"),
        "filename": doc_metadata.get("filename"),
        "title": doc_metadata.get("title"),
        "revision": doc_metadata.get("revision"),
        "item_id": item.get("item_id"),
        "item_type": item.get("item_type"),
        "criterion_id": item.get("criterion_id"),
        "criterion_name": item.get("criterion_name"),
        "statement": item.get("statement"),
    }
    
    # Evidence
    evidence_quotes = item.get("evidence_quotes", [])
    record["evidence_quote_1"] = evidence_quotes[0] if evidence_quotes else None
    record["evidence_quotes_json"] = json.dumps(evidence_quotes, ensure_ascii=False) if evidence_quotes else None
    
    # Source provenance
    source_fields = flatten_source(item.get("source"))
    record.update(source_fields)
    
    # Entities
    entity_fields = flatten_entities(item.get("entities"))
    record.update(entity_fields)
    
    # RULE fields
    rule_fields = flatten_rule_fields(item, record_side)
    record.update(rule_fields)
    
    # DOCUMENT rule reference fields
    ref_fields = flatten_rule_references(item, record_side)
    record.update(ref_fields)
    
    return record, errors


def flatten_json_to_records(
    data: Dict[str, Any],
    file_path: str,
    strict: bool = False,
) -> FlattenResult:
    """
    Flatten a single JSON file to normalized records.
    
    Args:
        data: Parsed JSON dict.
        file_path: Source file path for error reporting.
    
    Returns:
        FlattenResult with records and validation errors.
    """
    config = get_config()
    drift_severity = "ERROR" if strict else "WARNING"
    all_errors = []

    def drift(item_id: Optional[str], message: str) -> None:
        all_errors.append(ValidationError(
            file_path=file_path, item_id=item_id, rule_id="VAL-DRIFT-001",
            severity=drift_severity, message=message,
        ))

    fields = load_contract()["input_fields"]
    root_required = set(fields["root"]["required"])
    root_allowed = set(fields["root"]["allowed"])
    for key in sorted(set(data) - root_allowed):
        drift(None, f"unexpected field: root.{key}")
    for key in sorted(root_required - set(data)):
        drift(None, f"missing expected field: root.{key}")
    
    # Extract document metadata
    document = data.get("document", {})
    if not isinstance(document, dict):
        drift(None, "document must be an object")
        document = {}
    document_required = set(fields["document"]["required"])
    document_allowed = set(fields["document"]["allowed"])
    for key in sorted(document_required - set(document)):
        drift(None, f"missing expected field: document.{key}")
    for key in sorted(set(document) - document_allowed):
        drift(None, f"unexpected field: document.{key}")
    control_metadata = document.get("control_metadata", {})
    if not isinstance(control_metadata, dict):
        drift(None, "document.control_metadata must be an object")
        control_metadata = {}
    control_allowed = set(fields["control_metadata"]["allowed"])
    for key in sorted(set(control_metadata) - control_allowed):
        drift(None, f"unexpected field: document.control_metadata.{key}")
    
    doc_metadata = {
        "doc_id": document.get("doc_id"),
        "filename": document.get("filename"),
        "title": document.get("title"),
        "revision": control_metadata.get("revision"),
    }
    
    # Flatten items
    items = data.get("items", [])
    records = []
    if not isinstance(items, list):
        drift(None, "items must be a list")
        items = []
    common_required = set(fields["item"]["required"])
    common_allowed = set(fields["item"]["allowed"])

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            drift(None, f"items[{index}] must be an object")
            continue
        item_id = item.get("item_id")
        for key in sorted(common_required - set(item)):
            drift(item_id, f"missing expected field: items[{index}].{key}")
        for key in sorted(set(item) - common_allowed):
            drift(item_id, f"unexpected field: items[{index}].{key}")
        record, errors = flatten_item_to_record(item, doc_metadata, file_path, config)
        records.append(record)
        all_errors.extend(errors)
    
    return FlattenResult(records=records, validation_errors=all_errors)


def flatten_multiple_files(
    json_data_list: List[Dict[str, Any]],
    file_paths: List[str],
    strict: bool = False,
) -> FlattenResult:
    """
    Flatten multiple JSON files to a combined normalized record set.
    
    Args:
        json_data_list: List of parsed JSON dicts.
        file_paths: Corresponding file paths for error reporting.
    
    Returns:
        FlattenResult with combined records and validation errors.
    """
    all_records = []
    all_errors = []
    
    for data, file_path in zip(json_data_list, file_paths):
        result = flatten_json_to_records(data, file_path, strict=strict)
        all_records.extend(result.records)
        all_errors.extend(result.validation_errors)
    
    return FlattenResult(records=all_records, validation_errors=all_errors)
