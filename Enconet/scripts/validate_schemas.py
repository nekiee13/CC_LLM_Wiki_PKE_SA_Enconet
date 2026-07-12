#!/usr/bin/env python3
"""validate_schemas.py — EPIC 1 contract validator (master plan, EPIC 13 pattern).

Checks every schemas/*.yml contract for internal consistency and enforces the
single-source rules:
  - app_b_taxonomy.yml is the sole canonical criterion declaration; the broader
    sieving_contract.yml must not re-declare the pairs.
  - vocabularies.yml document_sides/source_rules must match the sieving contract enums.
  - id_patterns.yml regexes must compile, be anchored, and accept their own examples.
  - scoring_model.yml weights must cover every rating value exactly.
  - dashboard_schema.yml must carry the exact v2 criterion object fields.
  - page_types.yml and required_fields.yml must declare the same five page types.

Appends one row to manifests/validation_runs.csv. Exit 0 on PASS, 1 on FAIL.
Stdlib + PyYAML only.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ENCONET = Path(__file__).resolve().parents[1]
SCHEMAS = ENCONET / "schemas"

ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"]
CANON_IDS = [f"APP_B_{r}" for r in ROMANS]
RATINGS = ["fully", "substantially", "partially", "minimally", "unmet", "undetermined", "na"]
GAP_STATUSES = ["covered", "mostly-covered", "partially-covered", "minimally-covered",
                "not-covered", "not-applicable", "undetermined", "missing-evidence"]
ACTION_TYPES = ["verification", "document_request", "sample_test", "interview"]
LANGUAGES = ["sl", "en", "hr"]
DASH_CRITERION_FIELDS = ["n", "order", "title", "rating", "score", "refs", "aff", "con", "judge", "verify"]
PAGE_TYPES = ["criterion-evaluation", "evidence", "finding", "action", "gate-decision"]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load_yaml(name: str) -> dict:
    path = SCHEMAS / name
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report and continue with other checks
        fail(f"{name}: cannot parse — {exc}")
        return {}


def check_taxonomy(tax: dict, sieving: dict) -> None:
    criteria = tax.get("criteria") or []
    if len(criteria) != 18:
        fail(f"app_b_taxonomy.yml: expected 18 criteria, found {len(criteria)}")
    ids = [c.get("criterion_id") for c in criteria]
    if ids != CANON_IDS:
        fail(f"app_b_taxonomy.yml: criterion_id sequence differs from APP_B_I..APP_B_XVIII: {ids}")
    for c in criteria:
        if not (c.get("criterion_name") or "").strip():
            fail(f"app_b_taxonomy.yml: {c.get('criterion_id')}: empty criterion_name")
        if not (c.get("description") or "").strip():
            fail(f"app_b_taxonomy.yml: {c.get('criterion_id')}: missing description")
    if "criteria" in sieving:
        fail("sieving_contract.yml must not re-declare app_b_taxonomy criteria "
             "(ADR-0003 single-source violation)")


def check_id_patterns(pats: dict, tax: dict) -> None:
    patterns = pats.get("patterns") or {}
    expected = ["doc_id", "chunk_id", "quote_id", "crumb_id", "requirement_id",
                "evaluation_id", "gap_id", "finding_id", "action_id", "run_id", "dashboard_id"]
    missing = [k for k in expected if k not in patterns]
    if missing:
        fail(f"id_patterns.yml: missing patterns: {missing}")
    for name, spec in patterns.items():
        regex, example = spec.get("regex", ""), spec.get("example", "")
        if not (regex.startswith("^") and regex.endswith("$")):
            fail(f"id_patterns.yml: {name}: regex not anchored: {regex}")
        try:
            compiled = re.compile(regex)
        except re.error as exc:
            fail(f"id_patterns.yml: {name}: regex does not compile — {exc}")
            continue
        if not compiled.fullmatch(example):
            fail(f"id_patterns.yml: {name}: example {example!r} does not match its regex")
    # Criterion alternation must cover exactly the taxonomy numerals.
    crumb = patterns.get("crumb_id", {}).get("regex", "")
    m = re.search(r"APP_B_\(([^)]*)\)", crumb)
    if m and sorted(m.group(1).split("|")) != sorted(ROMANS):
        fail("id_patterns.yml: crumb_id criterion alternation does not cover exactly I..XVIII")


def check_vocabularies(voc: dict, sieving: dict) -> None:
    vocs = voc.get("vocabularies") or {}
    expected = {
        "ratings": RATINGS,
        "gap_statuses": GAP_STATUSES,
        "action_types": ACTION_TYPES,
        "languages": LANGUAGES,
        "document_sides": ["RULE", "DOCUMENT"],
        "source_rules": ["10CFR50_APPB", "10CFR21"],
    }
    for name, values in expected.items():
        got = (vocs.get(name) or {}).get("values")
        if got != values:
            fail(f"vocabularies.yml: {name}: expected {values}, found {got}")
    for name in list(expected) + ["audit_states"]:
        if not (vocs.get(name) or {}).get("usage", "").strip():
            fail(f"vocabularies.yml: {name}: missing usage note")
    states = (vocs.get("audit_states") or {}).get("values") or []
    for required in ["setup", "registered", "evaluated", "report_ready", "dashboard_ready", "closed", "failed"]:
        if required not in states:
            fail(f"vocabularies.yml: audit_states missing {required!r}")
    # Cross-check runtime projection.
    if (sieving.get("enums", {}).get("record_side") or []) != (vocs.get("document_sides") or {}).get("values"):
        fail("vocabularies.yml document_sides != sieving_contract enums.record_side")
    ref_codes = [c.get("ref_code") for c in sieving.get("canonical_codes", [])]
    if ref_codes != (vocs.get("source_rules") or {}).get("values"):
        fail("vocabularies.yml source_rules != sieving_contract canonical_codes ref_codes")


def check_scoring(model: dict) -> None:
    weights = model.get("rating_weights") or {}
    if sorted(weights) != sorted(RATINGS):
        fail(f"scoring_model.yml: rating_weights keys must be exactly the ratings vocabulary; found {sorted(weights)}")
    if weights.get("na") is not None:
        fail("scoring_model.yml: na must carry null weight (excluded from scoring)")
    for rating in RATINGS[:-1]:
        w = weights.get(rating)
        if not isinstance(w, (int, float)) or not 0.0 <= w <= 1.0:
            fail(f"scoring_model.yml: weight for {rating!r} must be a number in [0,1]; found {w!r}")
    cons = model.get("consolidated_score") or {}
    for field in ["formula", "denominator", "rounding", "range"]:
        if field not in cons:
            fail(f"scoring_model.yml: consolidated_score missing {field!r}")
    thresholds = model.get("classification_thresholds") or []
    mins = [t.get("min_score") for t in thresholds]
    if mins != sorted(mins, reverse=True):
        fail("scoring_model.yml: classification_thresholds must be ordered top-down")
    if not thresholds or thresholds[-1].get("min_score") != 0.0:
        fail("scoring_model.yml: classification_thresholds must end at min_score 0.0")
    if "pending human calibration approval" not in str(model.get("calibration_status", "")):
        fail("scoring_model.yml: must stay marked pending human calibration approval until G3 (ADR-0013)")
    if not model.get("model_version"):
        fail("scoring_model.yml: missing model_version")


def check_dashboard(dash: dict) -> None:
    fields = list((dash.get("criterion_object") or {}).get("required_fields") or {})
    if fields != DASH_CRITERION_FIELDS:
        fail(f"dashboard_schema.yml: criterion object fields must be exactly {DASH_CRITERION_FIELDS}; found {fields}")
    if (dash.get("criterion_object") or {}).get("count") != 18:
        fail("dashboard_schema.yml: criterion object count must be 18")
    top = list((dash.get("top_level_metrics") or {}).get("required_fields") or {})
    for required in ["supplier", "weighted_score", "classification_counts", "deliverable_language"]:
        if required not in top:
            fail(f"dashboard_schema.yml: top_level_metrics missing {required!r}")
    forbidden = dash.get("forbidden_patterns") or []
    for required in ["login.microsoftonline.com", "oauth", "signin"]:
        if required not in forbidden:
            fail(f"dashboard_schema.yml: forbidden_patterns missing {required!r}")


def check_pages(pages: dict, fields: dict) -> None:
    declared = list(pages.get("page_types") or {})
    if declared != PAGE_TYPES:
        fail(f"page_types.yml: page types must be exactly {PAGE_TYPES}; found {declared}")
    common = fields.get("common_required") or {}
    for required in ["id", "type", "status", "content_origin", "source"]:
        if required not in common:
            fail(f"required_fields.yml: common_required missing {required!r}")
    per_type = list(fields.get("per_type_required") or {})
    if per_type != PAGE_TYPES:
        fail(f"required_fields.yml: per_type_required must cover exactly {PAGE_TYPES}; found {per_type}")


def append_validation_run(result: str, exit_code: int, details: str) -> None:
    manifest = ENCONET / "manifests" / "validation_runs.csv"
    phase = "unknown"
    try:
        state = yaml.safe_load((ENCONET / "project-state.yml").read_text(encoding="utf-8"))
        phase = state.get("phase", "unknown")
    except Exception:  # noqa: BLE001 - manifest row still gets written
        pass
    with manifest.open("a", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_schemas.py", phase, result, exit_code, details,
        ])


def main() -> int:
    tax = load_yaml("app_b_taxonomy.yml")
    pats = load_yaml("id_patterns.yml")
    voc = load_yaml("vocabularies.yml")
    load_yaml("app_b_json_schema.yml")  # parse check; field semantics enforced by Task 5.3
    model = load_yaml("scoring_model.yml")
    dash = load_yaml("dashboard_schema.yml")
    pages = load_yaml("page_types.yml")
    fields = load_yaml("required_fields.yml")
    try:
        sieving = json.loads((SCHEMAS / "sieving_contract.yml").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"sieving_contract.yml: cannot parse — {exc}")
        sieving = {}

    check_taxonomy(tax, sieving)
    check_id_patterns(pats, tax)
    check_vocabularies(voc, sieving)
    check_scoring(model)
    check_dashboard(dash)
    check_pages(pages, fields)

    if errors:
        for err in errors:
            print(f"FAIL  {err}")
        print(f"validate_schemas: FAIL ({len(errors)} error(s))")
        append_validation_run("FAIL", 1, f"{len(errors)} error(s); first: {errors[0][:120]}")
        return 1
    print("validate_schemas: PASS (8 contracts; taxonomy has one canonical owner)")
    append_validation_run("PASS", 0, "8 contracts checked; taxonomy single-owner rule satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
