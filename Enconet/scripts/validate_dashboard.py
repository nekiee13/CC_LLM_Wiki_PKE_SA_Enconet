#!/usr/bin/env python3
"""Validate EPIC12 data/package consistency, offline HTML, and JS hooks."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import db_util
import validate_evidence_bundle
from build_dashboard_data import build, validate_data
from build_evaluation_package import validate_package, validate_source
from finding_workflow import APPROVALS

ENCONET = Path(__file__).resolve().parents[1]
SCHEMA = ENCONET / "schemas" / "dashboard_schema.yml"
STATE = ENCONET / "project-state.yml"
OUTPUTS = ENCONET / "outputs"
RUNS = ENCONET / "manifests" / "validation_runs.csv"
DATA_BLOCK = re.compile(r'<script id="dashboard-data" type="application/json">(.*?)</script>', re.DOTALL)
EVIDENCE_BLOCK = re.compile(
    r'<script id="evidence-bundle" type="application/json" '
    r'data-sha256="([0-9a-f]*)">(.*?)</script>', re.DOTALL,
)
SECTIONS = ["dashboard-header", "metric-bar", "executive-summary", "distribution",
            "dashboard-controls", "criterion-cards", "criterion-matrix", "priority-actions",
            "dashboard-footer"]
FUNCTIONS = ["renderDashboard", "filterCriteria", "searchCriteria", "sortCriteria",
             "toggleCard", "toggleAll", "printDashboard"]
HOOKS = ["onchange=\"filterCriteria()\"", "oninput=\"searchCriteria()\"",
         "onclick=\"sortCriteria()\"", "onclick=\"toggleAll(true)\"",
         "onclick=\"toggleAll(false)\"", "onclick=\"printDashboard()\""]
BINDINGS = ["weighted_score", "applicable_count", "classification_counts", "criteria",
            "priority_actions", "dash_id", "generated_date"]


def validate(package: dict, data: dict, html: str, *, db: Path | None = None,
             approvals: Path = APPROVALS, evidence_bundle: dict | None = None) -> list[str]:
    errors = validate_package(package) + validate_data(data)
    if db is not None:
        errors.extend(validate_source(package, db, approvals))
    try:
        expected = build(package, generated_date=data.get("generated_date", ""),
                         dash_id=data.get("dash_id", ""))
        for key, value in expected.items():
            if data.get(key) != value:
                errors.append(f"dashboard/package mismatch: {key}")
    except Exception as exc:  # noqa: BLE001 - collect all validation failures
        errors.append(f"dashboard/package projection failed: {exc}")

    forbidden = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))["forbidden_patterns"]
    lowered_data = json.dumps(data, ensure_ascii=False).casefold()
    lowered_html = html.casefold()
    for pattern in forbidden:
        if pattern.casefold() in lowered_data or pattern.casefold() in lowered_html:
            errors.append(f"forbidden dashboard pattern: {pattern}")
    for section in SECTIONS:
        if f'id="{section}"' not in html:
            errors.append(f"missing dashboard section: {section}")
    for function in FUNCTIONS:
        if not re.search(rf"function\s+{re.escape(function)}\s*\(", html):
            errors.append(f"missing dashboard JS function: {function}")
    for hook in HOOKS:
        if hook not in html:
            errors.append(f"missing dashboard button hook: {hook}")
    for binding in BINDINGS:
        if f'data-bind="{binding}"' not in html:
            errors.append(f"missing dashboard data binding: {binding}")
    match = DATA_BLOCK.search(html)
    if not match:
        errors.append("embedded dashboard data missing")
    else:
        try:
            embedded = json.loads(match.group(1))
            if embedded != data:
                errors.append("embedded dashboard data mismatch")
        except json.JSONDecodeError:
            errors.append("embedded dashboard data is invalid JSON")
    if evidence_bundle is not None:
        bundle_errors = validate_evidence_bundle.validate(evidence_bundle)
        errors.extend(f"invalid evidence bundle: {error}" for error in bundle_errors)
        matches = EVIDENCE_BLOCK.findall(html)
        if len(matches) != 1:
            errors.append("embedded evidence bundle count must be one")
        else:
            digest, payload = matches[0]
            try:
                embedded_bundle = json.loads(payload)
                if embedded_bundle != evidence_bundle:
                    errors.append("embedded evidence bundle mismatch")
            except json.JSONDecodeError:
                errors.append("embedded evidence bundle is invalid JSON")
            expected_hash = hashlib.sha256(
                validate_evidence_bundle.canonical_bytes(evidence_bundle)
            ).hexdigest()
            if digest != expected_hash:
                errors.append("embedded evidence bundle hash mismatch")
            if expected_hash not in html:
                errors.append("bundle hash missing from artifact metadata")
            package_hash = evidence_bundle.get("lineage", {}).get("package", {}).get("sha256")
            if not package_hash or package_hash not in html:
                errors.append("package hash missing from artifact metadata")
        for field in ("run_id", "supplier", "deliverable_language"):
            if evidence_bundle.get("metadata", {}).get(field) != data.get(field):
                errors.append(f"evidence bundle/dashboard mismatch: {field}")
        for element_id in (
            "artifact-metadata", "metadata-package-hash", "metadata-bundle-hash",
            "evidence-backdrop", "evidence-drawer", "evidence-panel-heading",
            "evidence-close", "evidence-status", "evidence-resolved-content",
            "evidence-quotes", "evidence-primary-chunk", "evidence-previous-chunk",
            "evidence-next-chunk", "evidence-current-chunk-id",
            "evidence-highlight-status", "evidence-chunk-text",
            "evidence-record-actions", "evidence-copy", "evidence-print",
            "evidence-copy-status", "evidence-citation-output",
            "evidence-citation-print",
        ):
            if f'id="{element_id}"' not in html:
                errors.append(f"missing evidence artifact metadata element: {element_id}")
        for function in (
            "evidenceControl", "appendEvidenceControls", "renderEvidenceCrumb",
            "openEvidence", "closeEvidence", "quoteRanges", "renderHighlightedText",
            "renderChunk", "navigateChunk", "buildEvidenceCitation",
            "copyEvidenceCitation", "printEvidence",
        ):
            if not re.search(rf"function\s+{re.escape(function)}\s*\(", html):
                errors.append(f"missing evidence navigation JS function: {function}")
        evidence_contract = (
            'role="dialog"', 'aria-modal="true"', 'tabindex="-1"',
            'role="status"', 'aria-live="polite"', 'data-evidence-id',
            'data-quote-ids', "document.createTextNode(source.slice(start,end))",
            "body.evidence-print>main", "window.addEventListener('afterprint'",
            "JavaScript is required to open the embedded evidence; reference IDs "
            "remain visible for manual lookup.",
        )
        for marker in evidence_contract:
            if marker not in html:
                errors.append(f"missing evidence navigation contract marker: {marker}")
    return list(dict.fromkeys(errors))


def append(result: str, code: int, details: str, path: Path = RUNS,
           phase: str = "verification") -> None:
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "validate_dashboard.py", phase, result, code, details,
        ])


def _project_paths() -> tuple[str, Path, Path, Path]:
    state = yaml.safe_load(STATE.read_text(encoding="utf-8"))
    phase = state.get("phase", "unknown")
    supplier = re.sub(r"[^a-z0-9_-]+", "-", state.get("supplier", "supplier").casefold()).strip("-")
    return (phase, OUTPUTS / f"{supplier}_appendix_b_evaluation_package.json",
            OUTPUTS / f"{supplier}_appendix_b_dashboard_data.json",
            OUTPUTS / f"{supplier}_appendix_b_dashboard.html")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, nargs="?")
    parser.add_argument("dashboard_data", type=Path, nargs="?")
    parser.add_argument("html", type=Path, nargs="?")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--no-record", action="store_true")
    parser.add_argument("--phase", default="verification")
    args = parser.parse_args()
    phase = args.phase
    if not any((args.package, args.dashboard_data, args.html)):
        phase, package_path, data_path, html_path = _project_paths()
        present = [path.is_file() for path in (package_path, data_path, html_path)]
        if phase not in {"dashboard_ready", "closed"} and not any(present):
            print(f"validate_dashboard: PASS - no dashboard artifacts required in phase {phase}")
            return 0
        args.package, args.dashboard_data, args.html = package_path, data_path, html_path
    elif not all((args.package, args.dashboard_data, args.html)):
        print("validate_dashboard: FAIL - package, dashboard_data, and html are required together", file=sys.stderr)
        return 1
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"))
        data = json.loads(args.dashboard_data.read_text(encoding="utf-8"))
        errors = validate(package, data, args.html.read_text(encoding="utf-8"),
                          db=args.db, approvals=args.approvals)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]
    if errors:
        if not args.no_record:
            append("FAIL", 1, f"{len(errors)} error(s); first: {errors[0][:120]}", phase=phase)
        for error in errors:
            print(f"validate_dashboard: FAIL - {error}", file=sys.stderr)
        return 1
    if not args.no_record:
        append("PASS", 0, "dashboard data, package source, offline structure, and JS hooks verified", phase=phase)
    print("validate_dashboard: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
