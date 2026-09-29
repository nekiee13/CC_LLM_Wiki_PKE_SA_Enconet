"""Validate the local, canonical sieving crumb interchange format.

This is a format check, not proof that a quote matches an approved source.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .contract import canonical_codes


PROJECT_ROOT = Path(__file__).resolve().parents[3]
TAXONOMY = PROJECT_ROOT / "schemas" / "app_b_taxonomy.yml"
LANGUAGES = {"sl", "en", "hr"}
ROLES = {"GOVERNING", "INTERPRETIVE"}
APPLICABILITY = {"APPLICABLE", "CONDITIONAL", "NOT_APPLICABLE"}
FORBIDDEN = {"statement_en", "translation_status", "meaning_flag"}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _allowed(value: object, choices: set[str] | dict[str, str]) -> bool:
    return isinstance(value, str) and value in choices


def check_authority_references(refs: object, where: str, result: ValidationResult) -> None:
    configured = {entry["ref_code"]: entry for entry in canonical_codes()}
    if not isinstance(refs, list):
        result.errors.append(f"{where}: authority_references must be a list")
        return
    for index, ref in enumerate(refs):
        label = f"{where}.authority_references[{index}]"
        if not isinstance(ref, dict):
            result.errors.append(f"{label}: must be an object")
            continue
        role, code = ref.get("authority_role"), ref.get("source_code")
        if not _allowed(role, ROLES):
            result.errors.append(f"{label}: invalid authority_role {role!r}")
        elif not isinstance(code, str) or code not in configured or configured[code].get("authority_role") != role:
            result.errors.append(f"{label}: {code!r} is not valid for {role}")
        locator = ref.get("source_locator")
        if not _nonempty(locator):
            result.errors.append(f"{label}: source_locator is required")
        elif isinstance(code, str) and code in configured:
            source = configured[code]
            if "allowed_locators" in source and locator not in source["allowed_locators"]:
                result.errors.append(f"{label}: source_locator is not allowed for {code}")
            elif "locator_pattern" in source and not re.fullmatch(source["locator_pattern"], locator):
                result.errors.append(f"{label}: source_locator does not match {code} pattern")
        applicability = ref.get("applicability", "APPLICABLE")
        if not _allowed(applicability, APPLICABILITY):
            result.errors.append(f"{label}: invalid applicability {applicability!r}")
        if ((isinstance(code, str) and code in configured
             and configured[code].get("requires_applicability_basis"))
                or applicability == "CONDITIONAL") and not _nonempty(ref.get("applicability_basis")):
            result.errors.append(f"{label}: applicability_basis is required")


# Existing callers use this name; retain it during the transfer.
_check_refs = check_authority_references


def validate_payload(payload: object, *, strict: bool = False) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(payload, dict):
        result.errors.append("root: must be an object")
        return result
    document, items = payload.get("document"), payload.get("items")
    if not isinstance(document, dict):
        result.errors.append("document: required object")
        return result
    if not isinstance(items, list) or not items:
        result.errors.append("items: required non-empty list")
        return result
    for key in ("name", "date"):
        if not _nonempty(document.get(key)):
            result.errors.append(f"document.{key}: required non-empty value")
    side = document.get("document_side")
    if not _allowed(side, {"RULE", "DOCUMENT"}):
        result.errors.append(f"document.document_side: invalid value {side!r}")
    refs = document.get("authority_references")
    check_authority_references(refs, "document", result)
    if side == "RULE" and isinstance(refs, list) and not refs:
        result.errors.append("document.authority_references: RULE run requires at least one reference")
    if side == "DOCUMENT" and refs != []:
        result.errors.append("document.authority_references: DOCUMENT run requires an empty list")
    if "source_rules" in document and document.get("source_rules") is not None:
        result.errors.append("document.source_rules: legacy non-null field is forbidden by ADR-0020")

    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))["criteria"]
    pairs = {entry["criterion_id"]: entry["criterion_name"] for entry in taxonomy}
    seen: set[str] = set()
    for index, item in enumerate(items):
        where = f"items[{index}]"
        if not isinstance(item, dict):
            result.errors.append(f"{where}: must be an object")
            continue
        item_id = item.get("item_id")
        if not _nonempty(item_id) or item_id in seen:
            result.errors.append(f"{where}.item_id: required and unique")
        else:
            seen.add(item_id)
        criterion = item.get("criterion_id")
        if not _allowed(criterion, pairs) or item.get("criterion_name") != pairs.get(criterion):
            result.errors.append(f"{where}: unknown criterion_id/name pair")
        if not _nonempty(item.get("statement")):
            result.errors.append(f"{where}.statement: required non-empty value")
        sources = item.get("sources", item.get("source"))
        if isinstance(sources, dict):
            sources = [sources]
        if not isinstance(sources, list) or not sources:
            result.errors.append(f"{where}.sources: required non-empty list")
        elif any(not isinstance(source, dict) or not _nonempty(source.get("source_locator")) for source in sources):
            result.errors.append(f"{where}.sources: every source requires source_locator")
        quotes = item.get("evidence_quotes")
        if not isinstance(quotes, list) or not quotes:
            result.errors.append(f"{where}.evidence_quotes: required non-empty list")
        else:
            for qindex, quote in enumerate(quotes):
                qwhere = f"{where}.evidence_quotes[{qindex}]"
                if not isinstance(quote, dict) or not _nonempty(quote.get("quote_original")):
                    result.errors.append(f"{qwhere}.quote_original: required non-empty value")
                    continue
                if not _allowed(quote.get("quote_language"), LANGUAGES):
                    result.errors.append(f"{qwhere}.quote_language: invalid or missing")
                for forbidden in FORBIDDEN & set(quote):
                    result.errors.append(f"{qwhere}.{forbidden}: forbidden transformed field")
        if "authority_references" in item:
            check_authority_references(item["authority_references"], where, result)
            if side == "DOCUMENT" and item["authority_references"]:
                result.errors.append(f"{where}.authority_references: DOCUMENT items require an empty list")
        if side == "DOCUMENT" and any(key in item for key in ("rule", "rule_locator", "rule_key", "rule_strength")):
            result.errors.append(f"{where}: RULE-only fields forbidden on DOCUMENT side")
        for optional in ("item_type", "entities"):
            if optional not in item:
                result.warnings.append(f"{where}.{optional}: optional field missing")
    if strict and result.warnings:
        result.errors.extend(f"strict warning: {warning}" for warning in result.warnings)
    return result


def _local_file(path: Path) -> Path:
    """Resolve relative paths at this project, never at the caller's directory."""
    candidate = path if path.is_absolute() else PROJECT_ROOT / path
    resolved = candidate.resolve()
    if not resolved.is_relative_to(PROJECT_ROOT):
        raise ValueError("crumb file must be inside the project")
    if resolved.relative_to(PROJECT_ROOT).parts[0:1] != ("sieving",):
        raise ValueError("crumb file must be inside the project's sieving folder")
    if resolved.exists() and resolved.stat().st_nlink > 1:
        raise ValueError("linked crumb file could share bytes with another project")
    return resolved


def validate_file(path: Path, *, strict: bool = False) -> tuple[dict, ValidationResult]:
    local = _local_file(Path(path))
    try:
        payload = json.loads(local.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, ValidationResult(errors=[f"cannot read JSON: {exc}"])
    return payload, validate_payload(payload, strict=strict)
