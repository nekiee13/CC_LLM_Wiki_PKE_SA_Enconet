"""Company-neutral package, report, and offline dashboard projections.

This module reads one local SQLite run and writes deterministic projections. It
does not select sources, approve evidence, or make an audit judgment.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import sqlite3
from typing import Any

RATINGS = ("fully", "substantially", "partially", "minimally", "unmet", "undetermined", "na")
PACKAGE_VERSION = "1.0"
HEADINGS = (
    "Executive Summary", "Scope and Source Documents", "Method", "Coverage Summary",
    "Criterion-by-Criterion Evaluation", "Gap Analysis", "Priority Verification Actions",
    "Recommendations", "Consolidated Conformance Score", "Limitations", "Appendix: Evidence Matrix",
)
FORBIDDEN_HTML = ("login.microsoftonline.com", "oauth", "signin", "https://cdn.",
                  "cdnjs.cloudflare.com", "unpkg.com", "jsdelivr.net", "googleapis.com",
                  "<script src=\"http", "<link href=\"http", "@import url(http")


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _load_model(db: Path) -> dict[str, Any]:
    model_path = db.resolve().parent.parent / "schemas" / "scoring_model.yml"
    if not model_path.is_file():
        raise ValueError(f"local scoring model is missing: {model_path}")
    try:
        import yaml
        data = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"cannot read scoring model: {exc}") from exc
    if not isinstance(data, dict) or set(data.get("rating_weights", {})) != set(RATINGS):
        raise ValueError("local scoring model has invalid rating weights")
    return data


def _metrics(ratings: list[str], model: dict[str, Any]) -> dict[str, Any]:
    if len(ratings) != 18 or any(rating not in RATINGS for rating in ratings):
        raise ValueError("exactly 18 valid ratings are required")
    applicable = [rating for rating in ratings if rating != "na"]
    if not applicable:
        raise ValueError("at least one criterion must be applicable")
    weights = model["rating_weights"]
    score = round(100 * sum(float(weights[rating]) for rating in applicable) / len(applicable), 1)
    thresholds = model.get("classification_thresholds", [])
    classification = next((row["class"] for row in thresholds if score >= row["min_score"]), "undetermined")
    return {
        "consolidated_score": score,
        "classification": classification,
        "applicable_count": len(applicable),
        "classification_counts": {rating: ratings.count(rating) for rating in RATINGS},
    }


def _approval_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        expected = ["object_id", "decision", "date", "reviewer", "notes"]
        if reader.fieldnames != expected:
            raise ValueError("approval ledger header is invalid")
        return [dict(row) for row in reader]


def approved_ids(package: dict[str, Any]) -> set[str]:
    return {row.get("object_id", "") for row in package.get("approvals", [])
            if row.get("decision", "").casefold() == "approved" and row.get("date") and row.get("reviewer")}


def build_package(db: Path, run_id: str, approvals: Path) -> dict[str, Any]:
    db = Path(db).resolve()
    if not db.is_file():
        raise ValueError(f"database is missing: {db}")
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        run = dict(conn.execute("SELECT * FROM evaluation_runs WHERE run_id=?", (run_id,)).fetchone() or {})
        if not run:
            raise ValueError(f"unknown evaluation run: {run_id}")
        applicability = [dict(row) for row in conn.execute(
            "SELECT * FROM criterion_applicability WHERE evaluation_run_id=? ORDER BY criterion_id", (run_id,))]
        evaluations: list[dict[str, Any]] = []
        for row in conn.execute(
                "SELECT e.*, c.criterion_name FROM criterion_evaluations e "
                "JOIN criteria c USING(criterion_id) WHERE evaluation_run_id=? ORDER BY criterion_id", (run_id,)):
            item = dict(row)
            item["classification"] = item.pop("rating")
            item["evidence_ids"] = [value[0] for value in conn.execute(
                "SELECT item_id FROM evaluation_evidence WHERE evaluation_id=? ORDER BY item_id", (item["evaluation_id"],))]
            evaluations.append(item)
        gaps = [dict(row) for row in conn.execute(
            "SELECT g.* FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) "
            "WHERE e.evaluation_run_id=? ORDER BY gap_id", (run_id,))]
        findings = [dict(row) for row in conn.execute(
            "SELECT * FROM findings WHERE evaluation_run_id=? ORDER BY finding_id", (run_id,))]
        actions = [dict(row) for row in conn.execute(
            "SELECT * FROM auditor_actions WHERE evaluation_run_id=? ORDER BY action_id", (run_id,))]
    ratings = [row["classification"] for row in evaluations]
    package = {
        "schema_version": PACKAGE_VERSION,
        "run": run,
        "applicability": applicability,
        "evaluations": evaluations,
        "metrics": _metrics(ratings, _load_model(db)),
        "gaps": gaps,
        "findings": findings,
        "actions": actions,
    }
    object_ids = {f"G{gate}-{run_id}" for gate in (2, 3, 4)}
    object_ids.update(row["finding_id"] for row in findings)
    object_ids.update(row["action_id"] for row in actions)
    package["approvals"] = [row for row in _approval_rows(Path(approvals)) if row.get("object_id") in object_ids]
    package["approvals"].sort(key=lambda row: (row.get("object_id", ""), row.get("date", "")))
    return package


def validate_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "run", "applicability", "evaluations", "metrics", "gaps", "findings", "actions", "approvals"}
    errors.extend(f"missing top-level field: {key}" for key in sorted(required - set(package)))
    if package.get("schema_version") != PACKAGE_VERSION:
        errors.append("schema_version mismatch")
    evaluations = package.get("evaluations", [])
    if not isinstance(evaluations, list) or len(evaluations) != 18:
        errors.append("expected 18 evaluations")
    else:
        ratings = [row.get("classification") for row in evaluations]
        if any(rating not in RATINGS for rating in ratings):
            errors.append("invalid evaluation classification")
        else:
            try:
                # Package builders have already used the model; compare counts only here.
                counts = package.get("metrics", {}).get("classification_counts", {})
                if any(counts.get(rating) != ratings.count(rating) for rating in RATINGS):
                    errors.append("classification counts do not recompute")
            except AttributeError:
                errors.append("metrics are invalid")
    if not isinstance(package.get("approvals"), list):
        errors.append("approvals must be a list")
    if not isinstance(package.get("run", {}).get("run_id"), str):
        errors.append("run_id is missing")
    return errors


def validate_source(package: dict[str, Any], db: Path, approvals: Path) -> list[str]:
    run_id = package.get("run", {}).get("run_id")
    if not run_id:
        return ["package run_id missing"]
    rebuilt = build_package(db, run_id, approvals)
    return [] if _json_bytes(rebuilt) == _json_bytes(package) else ["package/source mismatch"]


def require_report_gates(package: dict[str, Any]) -> None:
    run_id = package.get("run", {}).get("run_id", "")
    approved = approved_ids(package)
    missing = [gate for gate in ("G2", "G3", "G4") if f"{gate}-{run_id}" not in approved]
    if missing:
        raise ValueError(f"approved {'/'.join(missing)} report gate(s) missing for {run_id}")


def _citation(kind: str, identifier: str) -> str:
    return f"[{kind}:{identifier}]" if identifier else "[source:package]"


def render_report(package: dict[str, Any]) -> str:
    errors = validate_package(package)
    if errors:
        raise ValueError("invalid package: " + "; ".join(errors))
    require_report_gates(package)
    run = package["run"]
    metrics = package["metrics"]
    metadata = {
        "schema_version": PACKAGE_VERSION,
        "run_id": run["run_id"],
        "package_sha256": hashlib.sha256(_json_bytes(package)).hexdigest(),
        "consolidated_score": metrics["consolidated_score"],
        "classification_counts": metrics["classification_counts"],
        "applicable_count": metrics["applicable_count"],
    }
    lines = ["---", "type: generated-audit-report", f"run_id: {run['run_id']}", "---", "",
             f"<!-- report-metadata: {json.dumps(metadata, sort_keys=True, separators=(',', ':'))} -->", "",
             f"# Appendix B Evaluation Report — {run.get('supplier', '')}", "",
             f"**Language:** `{run.get('deliverable_language', '')}`", ""]
    sections = {
        "Executive Summary": f"The package records {metrics['applicable_count']} applicable criteria and a consolidated classification of **{metrics['classification']}**.",
        "Scope and Source Documents": f"- run_id: `{run['run_id']}`\n- supplier: `{run.get('supplier', '')}`\n- scoring model: `{run.get('scoring_model_version', '')}`",
        "Method": "This report is generated from one validated package. Findings and actions remain subject to human approval.",
        "Coverage Summary": "| classification | count |\n|---|---:|\n" + "\n".join(
            f"| {rating} | {metrics['classification_counts'][rating]} |" for rating in RATINGS),
        "Criterion-by-Criterion Evaluation": "\n\n".join(
            f"### {row['criterion_id']} — {row.get('criterion_name', '')}\n\n"
            f"- classification: `{row['classification']}`\n"
            f"- evidence: {' '.join(_citation('crumb', item) for item in row.get('evidence_ids', [])) or '[source:package]'}\n"
            f"- ruling: {row.get('judge_ruling', '')}\n"
            f"- rationale: {row.get('rationale', '')}"
            for row in package["evaluations"]),
        "Gap Analysis": "\n".join(
            f"- {_citation('gap', row['gap_id'])}: {row.get('description', '')}"
            for row in package["gaps"]) or "- No gaps recorded.",
        "Priority Verification Actions": "\n".join(
            f"- {_citation('action', row['action_id'])}: {row.get('description', '')}"
            for row in package["actions"] if row.get("priority")) or "- No priority actions recorded.",
        "Recommendations": "\n".join(
            f"- {_citation('finding', row['finding_id'])}: {row.get('title', '')} — {row.get('body', '')}"
            for row in package["findings"] if row.get("status") in {"approved", "closed"}) or "- No approved findings are present.",
        "Consolidated Conformance Score": f"**{metrics['consolidated_score']} / 100** — **{metrics['applicable_count']}** applicable criteria.",
        "Limitations": "Only evidence and approvals in the package are represented. Missing evidence remains an open gap.",
        "Appendix: Evidence Matrix": "| criterion | classification | evidence |\n|---|---|---|\n" + "\n".join(
            f"| {row['criterion_id']} | {row['classification']} | "
            f"{' '.join(_citation('crumb', item) for item in row.get('evidence_ids', [])) or '[source:package]'} |"
            for row in package["evaluations"]),
    }
    for heading in HEADINGS:
        lines.extend([f"## {heading}", "", sections[heading], ""])
    return "\n".join(lines).rstrip() + "\n"


def build_dashboard_data(package: dict[str, Any], generated_date: str, dash_id: str) -> dict[str, Any]:
    if not re.fullmatch(r"DASH-\d{8}-\d{4}", dash_id):
        raise ValueError("invalid dashboard ID")
    datetime.fromisoformat(generated_date.replace("Z", "+00:00"))
    metrics = package["metrics"]
    return {
        "schema_version": PACKAGE_VERSION,
        "supplier": package["run"].get("supplier", ""),
        "generated_date": generated_date,
        "dash_id": dash_id,
        "run_id": package["run"]["run_id"],
        "deliverable_language": package["run"].get("deliverable_language", ""),
        "weighted_score": metrics["consolidated_score"],
        "applicable_count": metrics["applicable_count"],
        "classification_counts": metrics["classification_counts"],
        "criteria": [{
            "n": row["criterion_id"], "order": index, "title": row.get("criterion_name", ""),
            "rating": row["classification"], "score": row.get("score"),
            "refs": row.get("evidence_ids", []), "aff": row.get("affirmative_summary", ""),
            "con": row.get("contrary_summary", ""), "judge": row.get("judge_ruling", ""),
            "verify": [],
        } for index, row in enumerate(package["evaluations"], 1)],
        "priority_actions": [row for row in package["actions"] if row.get("priority")],
    }


def render_dashboard(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    title = html.escape(f"Appendix B dashboard — {data['supplier']}")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>body{{font-family:system-ui,sans-serif;margin:2rem;max-width:1000px}}.card{{border:1px solid #bbb;padding:1rem;margin:.5rem 0}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.5rem}}</style></head>
<body><main id="dashboard-header"><h1>{title}</h1><p id="metric-bar" data-bind="weighted_score"></p>
<section id="executive-summary" class="card" data-bind="applicable_count"></section><section id="distribution" class="card" data-bind="classification_counts"></section>
<section id="dashboard-controls"><label>Search <input id="search" oninput="searchCriteria()"></label><button onclick="sortCriteria()">Sort</button><button onclick="toggleAll(true)">Open all</button><button onclick="toggleAll(false)">Close all</button><button onclick="printDashboard()">Print</button></section>
<section id="criterion-cards" class="grid" data-bind="criteria"></section><section id="criterion-matrix" class="card"></section><section id="priority-actions" class="card"></section><footer id="dashboard-footer"></footer>
<script id="dashboard-data" type="application/json">{payload}</script>
<script>
const DATA=JSON.parse(document.getElementById('dashboard-data').textContent);
function renderDashboard(){{document.querySelector('[data-bind="weighted_score"]').textContent='Score: '+DATA.weighted_score;document.querySelector('[data-bind="applicable_count"]').textContent='Applicable: '+DATA.applicable_count;document.querySelector('[data-bind="classification_counts"]').textContent=JSON.stringify(DATA.classification_counts);document.getElementById('criterion-cards').innerHTML=DATA.criteria.map(c=>'<article class="card"><h3>'+c.n+' — '+c.title+'</h3><p>'+c.rating+'</p></article>').join('');document.getElementById('priority-actions').textContent=DATA.priority_actions.length+' priority actions';}}
function filterCriteria(){{searchCriteria();}} function searchCriteria(){{const q=document.getElementById('search').value.toLowerCase();document.querySelectorAll('#criterion-cards article').forEach(x=>x.hidden=!x.textContent.toLowerCase().includes(q));}} function sortCriteria(){{DATA.criteria.sort((a,b)=>a.n.localeCompare(b.n));renderDashboard();}} function toggleCard(){{}} function toggleAll(){{}} function printDashboard(){{window.print();}} renderDashboard();
</script></main></body></html>
'''


def validate_report(package: dict[str, Any], report: str) -> list[str]:
    errors = validate_package(package)
    for heading in HEADINGS:
        if f"## {heading}" not in report:
            errors.append(f"missing report section: {heading}")
    match = re.search(r"<!-- report-metadata: (\{.*?\}) -->", report)
    if not match:
        errors.append("report metadata missing")
    else:
        metadata = json.loads(match.group(1))
        expected = {
            "schema_version": PACKAGE_VERSION, "run_id": package["run"]["run_id"],
            "package_sha256": hashlib.sha256(_json_bytes(package)).hexdigest(),
            "consolidated_score": package["metrics"]["consolidated_score"],
            "classification_counts": package["metrics"]["classification_counts"],
            "applicable_count": package["metrics"]["applicable_count"],
        }
        for key, value in expected.items():
            if metadata.get(key) != value:
                errors.append(f"report/package mismatch: {key}")
    return list(dict.fromkeys(errors))


def validate_dashboard(package: dict[str, Any], data: dict[str, Any], dashboard: str) -> list[str]:
    errors = validate_package(package)
    expected = build_dashboard_data(package, data.get("generated_date", ""), data.get("dash_id", ""))
    if data != expected:
        errors.append("dashboard/package mismatch")
    for pattern in FORBIDDEN_HTML:
        if pattern.casefold() in dashboard.casefold():
            errors.append(f"forbidden dashboard pattern: {pattern}")
    match = re.search(r'<script id="dashboard-data" type="application/json">(.*?)</script>', dashboard, re.DOTALL)
    if not match:
        errors.append("embedded dashboard data missing")
    else:
        try:
            if json.loads(match.group(1)) != data:
                errors.append("embedded dashboard data mismatch")
        except json.JSONDecodeError:
            errors.append("embedded dashboard data is invalid JSON")
    for section in ("dashboard-header", "metric-bar", "executive-summary", "distribution", "dashboard-controls", "criterion-cards", "criterion-matrix", "priority-actions", "dashboard-footer"):
        if f'id="{section}"' not in dashboard:
            errors.append(f"missing dashboard section: {section}")
    return list(dict.fromkeys(errors))
