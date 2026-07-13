#!/usr/bin/env python3
"""Cross-check an EPIC11 report against its sole evaluation package source."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import db_util
from build_evaluation_package import validate_package, validate_source
from finding_workflow import APPROVALS
from generate_report import HEADINGS, approved_ids, canonical_bytes

ENCONET = Path(__file__).resolve().parents[1]
RUNS = ENCONET / "manifests" / "validation_runs.csv"
META = re.compile(r"<!-- report-metadata: (\{.*?\}) -->")
SCORE = re.compile(r"\*\*([0-9]+(?:\.[0-9]+)?) / 100\*\*.*?\*\*([0-9]+)\*\*")


def validate(package: dict, report: str, *, db: Path | None = None,
             approvals: Path = APPROVALS) -> list[str]:
    errors = validate_package(package)
    if db is not None:
        errors.extend(validate_source(package, db, approvals))
    language = package.get("run", {}).get("deliverable_language")
    headings = HEADINGS.get(language, [])
    positions = [report.find(f"## {heading}") for heading in headings]
    if len(positions) != 11 or any(position < 0 for position in positions):
        errors.append("missing required report section")
    elif positions != sorted(positions):
        errors.append("required report sections are out of order")
    match = META.search(report)
    if not match:
        errors.append("report metadata missing")
        metadata = {}
    else:
        try:
            metadata = json.loads(match.group(1))
        except json.JSONDecodeError:
            errors.append("report metadata is invalid JSON")
            metadata = {}
    approvals = approved_ids(package)
    findings = sorted(row["finding_id"] for row in package.get("findings", [])
                      if row.get("status") == "approved" and row.get("finding_id") in approvals)
    actions = sorted(row["action_id"] for row in package.get("actions", [])
                     if row.get("approval_status") == "approved"
                     and row.get("action_id") in approvals and row.get("priority"))
    expected = {
        "run_id": package.get("run", {}).get("run_id"),
        "package_sha256": hashlib.sha256(canonical_bytes(package)).hexdigest(),
        "consolidated_score": package.get("metrics", {}).get("consolidated_score"),
        "classification_counts": package.get("metrics", {}).get("classification_counts"),
        "applicable_count": package.get("metrics", {}).get("applicable_count"),
        "gap_ids": [row["gap_id"] for row in package.get("gaps", [])],
        "approved_finding_ids": findings, "approved_action_ids": actions,
        "language": language,
    }
    for key, value in expected.items():
        if metadata.get(key) != value:
            errors.append(f"report/package mismatch: {key}")
    score_match = SCORE.search(report)
    if not score_match or float(score_match.group(1)) != float(expected["consolidated_score"] or 0):
        errors.append("visible consolidated score mismatch")
    elif int(score_match.group(2)) != int(expected["applicable_count"] or 0):
        errors.append("visible applicable count mismatch")
    for name, count in (expected["classification_counts"] or {}).items():
        if f"| {name} | {count} |" not in report:
            errors.append(f"classification count mismatch: {name}")
    for identifier in expected["gap_ids"] + findings + actions:
        if identifier not in report:
            errors.append(f"report omits package object: {identifier}")
    if headings:
        start = report.find(f"## {headings[7]}")
        end = report.find(f"## {headings[8]}")
        recommendations = report[start:end]
        for line in recommendations.splitlines():
            if line.startswith("- ") and not re.search(r"\[(?:crumb|gap|finding):[^]]+\]", line):
                errors.append("citation-less recommendation")
    return errors


def append(result: str, code: int, details: str, path: Path = RUNS,
           phase: str = "verification") -> None:
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_report.py", phase, result, code, details,
        ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--no-record", action="store_true")
    parser.add_argument("--phase", default="verification")
    args = parser.parse_args()
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"))
        errors = validate(package, args.report.read_text(encoding="utf-8"),
                          db=args.db, approvals=args.approvals)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]
    if errors:
        if not args.no_record:
            append("FAIL", 1, f"{len(errors)} error(s); first: {errors[0][:120]}", phase=args.phase)
        for error in errors:
            print(f"validate_report: FAIL - {error}", file=sys.stderr)
        return 1
    if not args.no_record:
        append("PASS", 0, "report, package hash, DB projection, and approvals verified", phase=args.phase)
    print("validate_report: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
