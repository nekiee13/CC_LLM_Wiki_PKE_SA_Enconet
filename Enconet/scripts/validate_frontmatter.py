#!/usr/bin/env python3
"""Validate controlled wiki-page frontmatter against EPIC13 contracts."""
from __future__ import annotations

import argparse
import csv
import fnmatch
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import db_util

ENCONET = Path(__file__).resolve().parents[1]
WIKI = ENCONET / "wiki"
PAGE_TYPES = ENCONET / "schemas" / "page_types.yml"
REQUIRED = ENCONET / "schemas" / "required_fields.yml"
VOCABULARIES = ENCONET / "schemas" / "vocabularies.yml"
TAXONOMY = ENCONET / "schemas" / "app_b_taxonomy.yml"
RUNS = ENCONET / "manifests" / "validation_runs.csv"
STATUSES = {"draft", "approved", "closed", "generated", "superseded"}
ORIGINS = {"generated", "human", "mixed"}


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError(f"frontmatter missing: {path.name}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter must be an object: {path.name}")
    return data


def validate(root: Path = WIKI, *, page_types_path: Path = PAGE_TYPES,
             required_path: Path = REQUIRED) -> list[str]:
    types = yaml.safe_load(page_types_path.read_text(encoding="utf-8"))["page_types"]
    required = yaml.safe_load(required_path.read_text(encoding="utf-8"))
    vocabularies = yaml.safe_load(VOCABULARIES.read_text(encoding="utf-8"))["vocabularies"]
    canonical_criteria = {row["criterion_id"] for row in
                          yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))["criteria"]}
    errors: list[str] = []
    patterns = db_util.id_patterns()
    for expected_type, spec in types.items():
        directory = root / Path(spec["location"]).name
        if not directory.is_dir():
            errors.append(f"controlled page directory missing: {directory.name}")
            continue
        for path in sorted(directory.glob("*.md")):
            if not fnmatch.fnmatchcase(path.name, spec["filename_pattern"]):
                errors.append(f"invalid {expected_type} filename: {path.name}")
                continue
            try:
                data = parse(path)
            except (OSError, ValueError, yaml.YAMLError) as exc:
                errors.append(str(exc))
                continue
            for field in list(required["common_required"]) + list(required["per_type_required"][expected_type]):
                if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                    errors.append(f"missing frontmatter field {path.name}: {field}")
            if data.get("type") != expected_type:
                errors.append(f"page type/location mismatch {path.name}: {data.get('type')}")
            if data.get("status") not in STATUSES:
                errors.append(f"invalid page status {path.name}: {data.get('status')}")
            if data.get("content_origin") not in ORIGINS:
                errors.append(f"invalid content_origin {path.name}: {data.get('content_origin')}")
            pattern_name = spec.get("id_pattern")
            if pattern_name and data.get("id") is not None:
                if patterns[pattern_name].fullmatch(str(data["id"])) is None:
                    errors.append(f"invalid page id {path.name}: {data['id']}")
                if path.stem != str(data["id"]):
                    errors.append(f"page filename/id mismatch: {path.name}")
            criterion = data.get("criterion_id")
            if criterion is not None and criterion != "n-a" and criterion not in canonical_criteria:
                errors.append(f"invalid criterion_id {path.name}: {criterion}")
            run_id = data.get("evaluation_run")
            if run_id is not None and patterns["run_id"].fullmatch(str(run_id)) is None:
                errors.append(f"invalid evaluation_run {path.name}: {run_id}")
            if expected_type == "criterion-evaluation":
                if data.get("applicability") not in {"applicable", "not-applicable"}:
                    errors.append(f"invalid applicability {path.name}: {data.get('applicability')}")
                if data.get("classification") not in vocabularies["ratings"]["values"]:
                    errors.append(f"invalid classification {path.name}: {data.get('classification')}")
            elif expected_type == "finding":
                for field, vocabulary in (("severity", "finding_severities"),
                                          ("confidence", "finding_confidences"),
                                          ("verification_status", "verification_statuses")):
                    if data.get(field) not in vocabularies[vocabulary]["values"]:
                        errors.append(f"invalid {field} {path.name}: {data.get(field)}")
            elif expected_type == "action":
                if data.get("action_type") not in vocabularies["action_types"]["values"]:
                    errors.append(f"invalid action_type {path.name}: {data.get('action_type')}")
                if data.get("state") not in vocabularies["action_states"]["values"]:
                    errors.append(f"invalid action state {path.name}: {data.get('state')}")
                if not isinstance(data.get("priority"), bool):
                    errors.append(f"invalid action priority {path.name}: {data.get('priority')}")
            elif expected_type == "gate-decision":
                if not re.fullmatch(r"G[1-7]", str(data.get("gate", ""))):
                    errors.append(f"invalid gate {path.name}: {data.get('gate')}")
                if data.get("decision") not in {"approved", "rejected", "deferred"}:
                    errors.append(f"invalid gate decision {path.name}: {data.get('decision')}")
    return errors


def append(result: str, code: int, details: str, *, path: Path = RUNS,
           phase: str = "verification") -> None:
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     "validate_frontmatter.py", phase, result, code, details])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki", type=Path, default=WIKI)
    parser.add_argument("--page-types", type=Path, default=PAGE_TYPES)
    parser.add_argument("--required", type=Path, default=REQUIRED)
    parser.add_argument("--phase", default="verification")
    parser.add_argument("--no-record", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(args.wiki, page_types_path=args.page_types, required_path=args.required)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]
    code = int(bool(errors))
    if not args.no_record:
        append("FAIL" if code else "PASS", code,
               f"{len(errors)} error(s); first: {errors[0][:120]}" if errors else "controlled wiki frontmatter verified",
               phase=args.phase)
    for error in errors:
        print(f"validate_frontmatter: FAIL - {error}", file=sys.stderr)
    print(f"validate_frontmatter: {'FAIL' if code else 'PASS'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
