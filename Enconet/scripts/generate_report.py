#!/usr/bin/env python3
"""Render a deterministic, gate-controlled EPIC11 evaluation report from one package."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from build_evaluation_package import validate_package
from finding_workflow import render_template

ENCONET = Path(__file__).resolve().parents[1]
TEMPLATE = ENCONET / "templates" / "evaluation-report-template.md"
OUTPUTS = ENCONET / "outputs"

HEADINGS = {
    "en": ["Executive Summary", "Scope and Source Documents", "Method", "Coverage Summary",
           "Criterion-by-Criterion Evaluation", "Gap Analysis", "Priority Verification Actions",
           "Recommendations", "Consolidated Conformance Score", "Limitations", "Appendix: Evidence Matrix"],
    "sl": ["Povzetek", "Obseg in izvorni dokumenti", "Metoda", "Povzetek pokritosti",
           "Vrednotenje po merilih", "Analiza vrzeli", "Prednostni ukrepi preverjanja",
           "Priporočila", "Skupna ocena skladnosti", "Omejitve", "Priloga: matrika dokazov"],
    "hr": ["Sažetak", "Opseg i izvorni dokumenti", "Metoda", "Sažetak pokrivenosti",
           "Ocjenjivanje po kriterijima", "Analiza nedostataka", "Prioritetne radnje provjere",
           "Preporuke", "Ukupna ocjena sukladnosti", "Ograničenja", "Prilog: matrica dokaza"],
}

TEXT = {
    "en": {"title": "Appendix B Evaluation Report", "language": "Report language",
           "summary": "The package records {count} applicable criteria and a consolidated classification of **{classification}**.",
           "method": "Generated deterministically from evaluation package schema {schema}; findings and actions require manifest-backed approval.",
           "none_findings": "No approved findings are present.", "none_actions": "No approved priority actions are present.",
           "limitations": "Only evidence and human approvals contained in the package are represented; verbatim evidence remains unchanged."},
    "sl": {"title": "Poročilo o vrednotenju Dodatka B", "language": "Jezik poročila",
           "summary": "Paket vsebuje {count} veljavnih meril in skupno razvrstitev **{classification}**.",
           "method": "Poročilo je deterministično ustvarjeno iz paketa vrednotenja sheme {schema}; ugotovitve in ukrepi zahtevajo odobritev v manifestu.",
           "none_findings": "Odobrenih ugotovitev ni.", "none_actions": "Odobrenih prednostnih ukrepov ni.",
           "limitations": "Prikazani so samo dokazi in človeške odobritve iz paketa; dobesedni dokazi ostanejo nespremenjeni."},
    "hr": {"title": "Izvješće o ocjeni Dodatka B", "language": "Jezik izvješća",
           "summary": "Paket sadrži {count} primjenjivih kriterija i ukupnu klasifikaciju **{classification}**.",
           "method": "Izvješće je deterministički izrađeno iz paketa ocjene sheme {schema}; nalazi i radnje zahtijevaju odobrenje u manifestu.",
           "none_findings": "Nema odobrenih nalaza.", "none_actions": "Nema odobrenih prioritetnih radnji.",
           "limitations": "Prikazani su samo dokazi i ljudska odobrenja iz paketa; doslovni dokazi ostaju nepromijenjeni."},
}


def canonical_bytes(package: dict) -> bytes:
    return (json.dumps(package, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def approved_ids(package: dict) -> set[str]:
    return {row.get("object_id", "") for row in package.get("approvals", [])
            if row.get("decision", "").casefold() == "approved"
            and row.get("date") and row.get("reviewer")}


def require_report_gates(package: dict) -> None:
    run_id = package.get("run", {}).get("run_id", "")
    approved = approved_ids(package)
    missing = [gate for gate in ("G2", "G3", "G4") if f"{gate}-{run_id}" not in approved]
    if missing:
        raise ValueError(f"approved {'/'.join(missing)} report gate(s) missing for {run_id}")


def _citation(row: dict) -> str:
    if row.get("evidence_item_id"):
        return f"[crumb:{row['evidence_item_id']}]"
    if row.get("gap_id"):
        return f"[gap:{row['gap_id']}]"
    if row.get("finding_id"):
        return f"[finding:{row['finding_id']}]"
    return "[source:package]"


def render(package: dict, template: Path = TEMPLATE) -> str:
    errors = validate_package(package)
    if errors:
        raise ValueError("invalid evaluation package: " + "; ".join(errors))
    require_report_gates(package)
    run = package["run"]; language = run.get("deliverable_language")
    if language not in HEADINGS:
        raise ValueError("unsupported deliverable_language")
    headings, text = HEADINGS[language], TEXT[language]
    approvals = approved_ids(package)
    findings = sorted((row for row in package["findings"]
                       if row.get("status") == "approved" and row.get("finding_id") in approvals),
                      key=lambda row: row["finding_id"])
    actions = sorted((row for row in package["actions"]
                      if row.get("approval_status") == "approved"
                      and row.get("action_id") in approvals and row.get("priority")),
                     key=lambda row: row["action_id"])
    metrics = package["metrics"]
    metadata = {
        "schema_version": "1.0", "run_id": run["run_id"],
        "package_sha256": hashlib.sha256(canonical_bytes(package)).hexdigest(),
        "consolidated_score": metrics["consolidated_score"],
        "classification_counts": metrics["classification_counts"],
        "applicable_count": metrics["applicable_count"],
        "gap_ids": [row["gap_id"] for row in package["gaps"]],
        "approved_finding_ids": [row["finding_id"] for row in findings],
        "approved_action_ids": [row["action_id"] for row in actions],
        "language": language,
    }
    applicability = {row["criterion_id"]: row for row in package["applicability"]}
    criterion_blocks = []
    for row in package["evaluations"]:
        ruling = applicability.get(row["criterion_id"], {})
        evidence = " ".join(f"[crumb:{item}]" for item in row.get("evidence_ids", [])) or "[source:package]"
        criterion_blocks.append(
            f"### {row['criterion_id']} — {row.get('criterion_name', '')}\n\n"
            f"- classification: `{row['classification']}`\n"
            f"- applicability: `{'applicable' if ruling.get('applicable') else 'not-applicable'}`\n"
            f"- justification: {ruling.get('justification', 'n-a')} [document:{ruling.get('scope_source_doc_id', 'n-a')}]\n"
            f"- rationale: {row.get('rationale', '')} {evidence}"
        )
    gap_lines = [f"- {row['gap_id']}: {row['description']} {_citation(row)}" for row in package["gaps"]]
    action_lines = [f"- {row['action_id']}: {row['description']} {_citation(row)}" for row in actions]
    finding_lines = [f"- {row['finding_id']}: {row['title']} — {row['body']} {_citation(row)}" for row in findings]
    counts = ["| classification | count |", "|---|---:|"] + [
        f"| {name} | {count} |" for name, count in sorted(metrics["classification_counts"].items())
    ]
    appendix = ["| criterion | classification | evidence |", "|---|---|---|"] + [
        f"| {row['criterion_id']} | {row['classification']} | "
        f"{' '.join('[crumb:'+item+']' for item in row.get('evidence_ids', [])) or '[source:package]'} |"
        for row in package["evaluations"]
    ]
    values = {
        "report_metadata": json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        "report_title": f"{text['title']} — {run.get('supplier', '')}",
        "language_line": f"**{text['language']}:** `{language}`",
        "executive_summary": text["summary"].format(count=metrics["applicable_count"], classification=metrics["classification"]),
        "scope": f"- run_id: `{run['run_id']}`\n- supplier: `{run.get('supplier', '')}`\n- scoring_model_version: `{run.get('scoring_model_version', '')}`",
        "method": text["method"].format(schema=package["schema_version"]),
        "coverage": "\n".join(counts), "criteria": "\n\n".join(criterion_blocks),
        "gaps": "\n".join(gap_lines) or "- none [source:package]",
        "actions": "\n".join(action_lines) or text["none_actions"],
        "recommendations": "\n".join(finding_lines) or text["none_findings"],
        "score": f"**{metrics['consolidated_score']} / 100** — **{metrics['applicable_count']}** applicable criteria (`{metrics['classification']}`).",
        "limitations": text["limitations"], "appendix": "\n".join(appendix),
    }
    for index, key in enumerate(("executive_summary", "scope", "method", "coverage", "criteria", "gaps", "actions", "recommendations", "score", "limitations", "appendix")):
        values[f"heading_{key}"] = headings[index]
    return render_template(template, values).rstrip() + "\n"


def default_output(package: dict) -> Path:
    supplier = re.sub(r"[^a-z0-9_-]+", "-", package["run"].get("supplier", "supplier").casefold()).strip("-")
    return OUTPUTS / f"{supplier}_appendix_b_evaluation_report.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"))
        output = args.output or default_output(package)
        content = render(package)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8", newline="\n")
        print(f"generate_report: PASS - {output}")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI fail-closed boundary
        print(f"generate_report: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
