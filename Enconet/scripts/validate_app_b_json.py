#!/usr/bin/env python3
"""Validate EPIC5 crumb JSON before database import."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ENCONET = Path(__file__).resolve().parents[1]
TAXONOMY = ENCONET / "schemas" / "app_b_taxonomy.yml"
LANGUAGES = {"sl", "en", "hr"}
ROLES = {"GOVERNING", "INTERPRETIVE"}
ROLE_CODES = {"GOVERNING": {"10CFR50_APPB", "10CFR21"}, "INTERPRETIVE": {"ASME_NQA1"}}
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


def _check_refs(refs: object, where: str, result: ValidationResult) -> None:
    if not isinstance(refs, list):
        result.errors.append(f"{where}: authority_references must be a list")
        return
    for index, ref in enumerate(refs):
        label = f"{where}.authority_references[{index}]"
        if not isinstance(ref, dict):
            result.errors.append(f"{label}: must be an object")
            continue
        role, code = ref.get("authority_role"), ref.get("source_code")
        if role not in ROLES:
            result.errors.append(f"{label}: invalid authority_role {role!r}")
        elif code not in ROLE_CODES[role]:
            result.errors.append(f"{label}: {code!r} is not valid for {role}")
        if not _nonempty(ref.get("source_locator")):
            result.errors.append(f"{label}: source_locator is required")
        applicability = ref.get("applicability", "APPLICABLE")
        if applicability not in APPLICABILITY:
            result.errors.append(f"{label}: invalid applicability {applicability!r}")
        if code == "10CFR21" and not _nonempty(ref.get("applicability_basis")):
            result.errors.append(f"{label}: Part 21 requires applicability_basis")


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
    if side not in {"RULE", "DOCUMENT"}:
        result.errors.append(f"document.document_side: invalid value {side!r}")
    refs = document.get("authority_references")
    _check_refs(refs, "document", result)
    if side == "RULE" and isinstance(refs, list) and not refs:
        result.errors.append("document.authority_references: RULE run requires at least one reference")
    if side == "DOCUMENT" and refs != []:
        result.errors.append("document.authority_references: DOCUMENT run requires an empty list")
    if "source_rules" in document and document.get("source_rules") is not None:
        result.errors.append("document.source_rules: legacy non-null field is forbidden by ADR-0020")
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))["criteria"]
    pairs = {c["criterion_id"]: c["criterion_name"] for c in taxonomy}
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
        if criterion not in pairs or item.get("criterion_name") != pairs.get(criterion):
            result.errors.append(f"{where}: unknown criterion_id/name pair")
        if not _nonempty(item.get("statement")):
            result.errors.append(f"{where}.statement: required non-empty value")
        sources = item.get("sources", item.get("source"))
        if isinstance(sources, dict):
            sources = [sources]
        if not isinstance(sources, list) or not sources:
            result.errors.append(f"{where}.sources: required non-empty list")
        elif any(not isinstance(s, dict) or not _nonempty(s.get("source_locator")) for s in sources):
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
                if quote.get("quote_language") not in LANGUAGES:
                    result.errors.append(f"{qwhere}.quote_language: invalid or missing")
                for forbidden in FORBIDDEN & set(quote):
                    result.errors.append(f"{qwhere}.{forbidden}: forbidden transformed field")
        if "authority_references" in item:
            _check_refs(item["authority_references"], where, result)
            if side == "DOCUMENT" and item["authority_references"]:
                result.errors.append(
                    f"{where}.authority_references: DOCUMENT items require an empty list"
                )
        if side == "DOCUMENT" and any(k in item for k in ("rule", "rule_locator", "rule_key", "rule_strength")):
            result.errors.append(f"{where}: RULE-only fields forbidden on DOCUMENT side")
        for optional in ("item_type", "entities"):
            if optional not in item:
                result.warnings.append(f"{where}.{optional}: optional field missing")
    if strict and result.warnings:
        result.errors.extend(f"strict warning: {warning}" for warning in result.warnings)
    return result


def validate_file(path: Path, *, strict: bool = False) -> tuple[dict, ValidationResult]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, ValidationResult(errors=[f"cannot read JSON: {exc}"])
    return payload, validate_payload(payload, strict=strict)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    _, result = validate_file(args.json_file, strict=args.strict)
    for warning in result.warnings:
        print(f"WARNING {warning}")
    for error in result.errors:
        print(f"FAIL {error}", file=sys.stderr)
    print(f"validate_app_b_json: {'PASS' if result.passed else 'FAIL'}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
