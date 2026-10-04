#!/usr/bin/env python3
"""Check this project's schema contracts without granting source approval."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

import yaml

from project_paths import local_path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
RUNS = ROOT / "manifests" / "validation_runs.csv"
APPROVALS = ROOT / "manifests" / "approvals.csv"
RUN_HEADER = ["run_utc", "validator", "phase", "result", "exit_code", "details"]
ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"]
CRITERIA = [f"APP_B_{item}" for item in ROMANS]
RATINGS = ["fully", "substantially", "partially", "minimally", "unmet", "undetermined", "na"]
PAGE_TYPES = ["criterion-evaluation", "evidence", "finding", "action", "gate-decision"]
DASH_FIELDS = ["n", "order", "title", "rating", "score", "refs", "aff", "con", "judge", "verify"]


def _load(root: Path, name: str, errors: list[str]) -> dict:
    try:
        path = local_path(root / name)
        if name == "sieving_contract.yml":
            result = json.loads(path.read_text(encoding="utf-8"))
        else:
            result = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(result, dict):
            raise ValueError("top level is not an object")
        return result
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"{name}: cannot parse: {exc}")
        return {}


def _approval_exists(reference: str, version: str) -> bool:
    path = local_path(APPROVALS)
    if not path.is_file():
        return False
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = csv.DictReader(handle)
        if rows.fieldnames != ["object_id", "decision", "date", "reviewer", "notes"]:
            return False
        return any(row.get("object_id") == reference and row.get("decision") == "approved"
                   and row.get("date") and row.get("reviewer") and version in (row.get("notes") or "")
                   for row in rows)


def validate(schemas: Path = SCHEMAS) -> tuple[list[str], list[str]]:
    root = local_path(schemas)
    errors: list[str] = []
    notes: list[str] = []
    names = ["app_b_taxonomy.yml", "id_patterns.yml", "vocabularies.yml",
             "app_b_json_schema.yml", "scoring_model.yml", "dashboard_schema.yml",
             "page_types.yml", "required_fields.yml", "evaluation_package_schema.yml",
             "sieving_contract.yml", "activity_catalog.yml", "evidence_context.yml"]
    data = {name: _load(root, name, errors) for name in names}
    tax, patterns, voc = (data[name] for name in names[:3])
    model = data["scoring_model.yml"]
    dash = data["dashboard_schema.yml"]
    pages = data["page_types.yml"]
    fields = data["required_fields.yml"]
    package = data["evaluation_package_schema.yml"]
    sieving = data["sieving_contract.yml"]
    activities = data["activity_catalog.yml"]
    evidence_context = data["evidence_context.yml"]

    criteria = tax.get("criteria") or []
    if not isinstance(criteria, list) or len(criteria) != 18:
        errors.append("app_b_taxonomy.yml: exactly 18 criteria required")
    elif [row.get("criterion_id") for row in criteria if isinstance(row, dict)] != CRITERIA:
        errors.append("app_b_taxonomy.yml: criterion sequence differs from APP_B_I..APP_B_XVIII")
    for row in criteria if isinstance(criteria, list) else []:
        if not isinstance(row, dict) or not str(row.get("criterion_name") or "").strip():
            errors.append("app_b_taxonomy.yml: criterion name missing")
        elif not str(row.get("description") or "").strip():
            errors.append(f"app_b_taxonomy.yml: description missing: {row['criterion_id']}")
    if "criteria" in sieving:
        errors.append("sieving_contract.yml must not re-declare Appendix B criteria")

    activity_rows = activities.get("activities") or []
    expected_activity_ids = [
        "ACT_CONTRACTING", "ACT_DESIGN", "ACT_COMMERCIAL_DEDICATION", "ACT_SOFTWARE_QA",
        "ACT_PROCUREMENT", "ACT_PRODUCTION_HANDLING", "ACT_SPECIAL_PROCESSES",
        "ACT_TESTING_INSPECTION", "ACT_DOCUMENT_CONTROL", "ACT_ORGANIZATION_PROGRAM",
        "ACT_NONCONFORMING_PART21", "ACT_INTERNAL_AUDITS", "ACT_CORRECTIVE_ACTION",
        "ACT_TRAINING_CERTIFICATION", "ACT_FIELD_SERVICES", "ACT_RECORDS", "ACT_ISO_CONTEXT",
    ]
    activity_ids = [row.get("activity_id") for row in activity_rows if isinstance(row, dict)]
    if activities.get("catalog_id") != "SUPPLIER_AUDIT_ACTIVITIES":
        errors.append("activity_catalog.yml: catalog_id is invalid")
    if activity_ids != expected_activity_ids:
        errors.append("activity_catalog.yml: activity sequence differs from historic report order")
    if len(activity_rows) != 17 or len(set(activity_ids)) != len(activity_ids):
        errors.append("activity_catalog.yml: exactly 17 unique activities required")
    canonical_ids = set(CRITERIA)
    for row in activity_rows:
        if not isinstance(row, dict) or not str(row.get("name") or "").strip():
            errors.append("activity_catalog.yml: activity name missing")
            continue
        mapped = row.get("criterion_ids")
        if not isinstance(mapped, list) or any(item not in canonical_ids for item in mapped):
            errors.append(f"activity_catalog.yml: invalid criterion mapping: {row.get('activity_id')}")
        if not str(row.get("description") or "").strip():
            errors.append(f"activity_catalog.yml: description missing: {row.get('activity_id')}")
    if "APP_B_XVIII" not in {item for row in activity_rows for item in (row.get("criterion_ids") or [])}:
        errors.append("activity_catalog.yml: audit activity must map to APP_B_XVIII")

    context_fields = evidence_context.get("context_fields") or {}
    evidence_types = evidence_context.get("evidence_types") or []
    required_context_fields = {"project_ref", "contract_ref", "supplier_ref", "source_revision", "evidence_date"}
    if set(context_fields) != required_context_fields:
        errors.append("evidence_context.yml: context fields differ from the local anchor contract")
    if not isinstance(evidence_types, list) or len(evidence_types) != len(set(evidence_types)) or not evidence_types:
        errors.append("evidence_context.yml: evidence_types must be a unique non-empty list")
    for field, spec in context_fields.items():
        if not isinstance(spec, dict) or spec.get("type") != "string" or not str(spec.get("meaning") or "").strip():
            errors.append(f"evidence_context.yml: invalid context field: {field}")
    if "objective_record" not in evidence_types or "candidate_lead" not in evidence_types:
        errors.append("evidence_context.yml: objective_record and candidate_lead are required evidence types")

    id_patterns = patterns.get("patterns") or {}
    required_patterns = {"doc_id", "chunk_id", "quote_id", "crumb_id", "requirement_id",
                         "evaluation_id", "gap_id", "finding_id", "action_id", "run_id",
                         "dashboard_id"}
    if missing := required_patterns - set(id_patterns):
        errors.append("id_patterns.yml: missing patterns: " + ", ".join(sorted(missing)))
    for name, spec in id_patterns.items():
        regex, example = spec.get("regex", ""), spec.get("example", "")
        if not isinstance(regex, str) or not regex.startswith("^") or not regex.endswith("$"):
            errors.append(f"id_patterns.yml: unanchored regex: {name}")
            continue
        try:
            if re.compile(regex).fullmatch(str(example)) is None:
                errors.append(f"id_patterns.yml: example does not match: {name}")
        except re.error as exc:
            errors.append(f"id_patterns.yml: invalid regex {name}: {exc}")

    vocabularies = voc.get("vocabularies") or {}
    expected = {
        "ratings": RATINGS,
        "gap_statuses": ["covered", "mostly-covered", "partially-covered", "minimally-covered",
                         "not-covered", "not-applicable", "undetermined", "missing-evidence"],
        "action_types": ["verification", "document_request", "sample_test", "interview"],
        "finding_severities": ["low", "medium", "high", "critical"],
        "finding_confidences": ["low", "medium", "high"],
        "verification_statuses": ["pending", "verified", "rejected"],
        "finding_statuses": ["draft", "approved", "closed"],
        "action_states": ["open", "closed"],
        "approval_statuses": ["draft", "approved"],
        "document_sides": ["RULE", "DOCUMENT"],
        "authority_roles": ["GOVERNING", "INTERPRETIVE"],
    }
    for name, values in expected.items():
        if (vocabularies.get(name) or {}).get("values") != values:
            errors.append(f"vocabularies.yml: {name} does not match framework values")
    for name in [*expected, "audit_states", "languages", "source_rules", "authority_sources"]:
        if not str((vocabularies.get(name) or {}).get("usage") or "").strip():
            errors.append(f"vocabularies.yml: {name} usage is missing")
    languages = (vocabularies.get("languages") or {}).get("values") or []
    if not isinstance(languages, list) or not languages or len(set(languages)) != len(languages):
        errors.append("vocabularies.yml: languages must be a unique nonempty list")
    states = (vocabularies.get("audit_states") or {}).get("values") or []
    for name in ("setup", "registered", "evaluated", "report_ready", "dashboard_ready", "closed", "failed"):
        if name not in states:
            errors.append(f"vocabularies.yml: audit_states missing {name}")
    if (sieving.get("enums") or {}).get("record_side") != expected["document_sides"]:
        errors.append("vocabularies.yml: document_sides differ from sieving contract")
    codes = sieving.get("canonical_codes") or []
    if not isinstance(codes, list):
        errors.append("sieving_contract.yml: canonical_codes must be a list")
        codes = []
    ref_codes = [row.get("ref_code") for row in codes if isinstance(row, dict)]
    regulations = [row.get("ref_code") for row in codes if isinstance(row, dict)
                   and row.get("ref_type") == "REGULATION"]
    if len(ref_codes) != len(set(ref_codes)) or len(ref_codes) != len(codes):
        errors.append("sieving_contract.yml: duplicate or malformed canonical code")
    if (vocabularies.get("source_rules") or {}).get("values") != regulations:
        errors.append("vocabularies.yml: source_rules differ from local regulatory codes")
    if (vocabularies.get("authority_sources") or {}).get("values") != ref_codes:
        errors.append("vocabularies.yml: authority_sources differ from local canonical codes")
    for row in codes:
        if isinstance(row, dict) and row.get("authority_role") not in expected["authority_roles"]:
            errors.append(f"sieving_contract.yml: invalid role for {row.get('ref_code')}")
    if not codes:
        notes.append("source selection pending; an empty source-code list is not approval")
    else:
        notes.append("source-code shape checked; applicability and editions still need owner approval")

    weights = model.get("rating_weights") or {}
    if set(weights) != set(RATINGS):
        errors.append("scoring_model.yml: rating_weights keys must be exactly the ratings vocabulary")
    if weights.get("na", "missing") is not None:
        errors.append("scoring_model.yml: na must have null weight")
    for rating in RATINGS[:-1]:
        value = weights.get(rating)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
            errors.append(f"scoring_model.yml: invalid weight for {rating}")
    for field in ("formula", "denominator", "rounding", "range"):
        if field not in (model.get("consolidated_score") or {}):
            errors.append(f"scoring_model.yml: consolidated_score missing {field}")
    thresholds = model.get("classification_thresholds") or []
    mins = [row.get("min_score") for row in thresholds if isinstance(row, dict)]
    if len(mins) != len(thresholds) or not mins or mins != sorted(mins, reverse=True) or mins[-1] != 0:
        errors.append("scoring_model.yml: thresholds must descend to zero")
    if not model.get("model_version"):
        errors.append("scoring_model.yml: model_version missing")
    status = model.get("calibration_status")
    if status == "pending human calibration approval":
        if model.get("approval_ref"):
            errors.append("scoring_model.yml: pending model cannot claim approval")
        notes.append("scoring calibration pending local human approval")
    elif status == "approved":
        reference = model.get("approval_ref")
        version = str(model.get("model_version"))
        if ("placeholder" in version.lower() or not isinstance(reference, str) or not reference
                or not _approval_exists(reference, version)):
            errors.append("scoring_model.yml: approved model lacks a matching local approval row")
    else:
        errors.append("scoring_model.yml: calibration_status must be pending or approved")

    criterion_object = dash.get("criterion_object") or {}
    if list((criterion_object.get("required_fields") or {})) != DASH_FIELDS or criterion_object.get("count") != 18:
        errors.append("dashboard_schema.yml: criterion object must have ten fields and count 18")
    top = (dash.get("top_level_metrics") or {}).get("required_fields") or {}
    for field in ("supplier", "weighted_score", "classification_counts", "deliverable_language"):
        if field not in top:
            errors.append(f"dashboard_schema.yml: top-level field missing {field}")
    forbidden = dash.get("forbidden_patterns") or []
    for marker in ("login.microsoftonline.com", "oauth", "signin"):
        if marker not in forbidden:
            errors.append(f"dashboard_schema.yml: forbidden pattern missing {marker}")

    if list((pages.get("page_types") or {})) != PAGE_TYPES:
        errors.append("page_types.yml: expected five controlled page types")
    common = fields.get("common_required") or {}
    for field in ("id", "type", "status", "content_origin", "source"):
        if field not in common:
            errors.append(f"required_fields.yml: common field missing {field}")
    if list((fields.get("per_type_required") or {})) != PAGE_TYPES:
        errors.append("required_fields.yml: page types do not match")
    if package.get("evaluation_count") != 18 or package.get("ratings") != RATINGS:
        errors.append("evaluation_package_schema.yml: count or ratings differ from local contracts")
    return errors, notes


def append_result(result: str, code: int, details: str, path: Path = RUNS) -> None:
    with local_path(path).open("r+", newline="", encoding="utf-8") as handle:
        if next(csv.reader(handle), None) != RUN_HEADER:
            raise ValueError("validation manifest header is missing or invalid")
        handle.seek(0, 2)
        csv.writer(handle).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_schemas.py", "unknown", result, code, details,
        ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schemas", type=Path, default=SCHEMAS)
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        errors, notes = validate(args.schemas)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        errors, notes = [str(exc)], []
    for note in notes:
        print(f"NOTE: {note}")
    for error in errors:
        print(f"validate_schemas: FAIL - {error}", file=sys.stderr)
    code = int(bool(errors))
    if not args.no_record:
        try:
            append_result("FAIL" if code else "PASS", code,
                          f"{len(errors)} error(s); first: {errors[0][:120]}" if errors
                          else "local schema contracts consistent; approval not inferred")
        except (OSError, ValueError) as exc:
            print(f"validate_schemas: FAIL - record could not be written: {exc}", file=sys.stderr)
            return 1
    if not code:
        print("validate_schemas: PASS - contract shapes only; no source or scoring approval")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
