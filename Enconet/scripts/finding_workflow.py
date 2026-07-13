"""Fail-closed EPIC10 finding/action writers and wiki projections."""
from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path

import yaml

import db_util

ENCONET = Path(__file__).resolve().parents[1]
APPROVALS = ENCONET / "manifests" / "approvals.csv"
VOCABULARIES = ENCONET / "schemas" / "vocabularies.yml"
FINDING_TEMPLATE = ENCONET / "templates" / "finding-template.md"
ACTION_TEMPLATE = ENCONET / "templates" / "action-template.md"
FINDINGS_DIR = ENCONET / "wiki" / "findings"
ACTIONS_DIR = ENCONET / "wiki" / "actions"
TOKEN = re.compile(r"{{([a-z_]+)}}")


def vocabularies() -> dict[str, set[str]]:
    raw = yaml.safe_load(VOCABULARIES.read_text(encoding="utf-8"))["vocabularies"]
    return {name: set(spec["values"]) for name, spec in raw.items()}


def approval_rows(path: Path = APPROVALS) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def approved(object_id: str, path: Path = APPROVALS) -> dict[str, str] | None:
    return next((row for row in approval_rows(path)
                 if row.get("object_id") == object_id
                 and row.get("decision", "").casefold() == "approved"
                 and row.get("date") and row.get("reviewer")), None)


def require_input_gates(run_id: str, path: Path = APPROVALS) -> None:
    missing = [gate for gate in ("G2", "G3") if approved(f"{gate}-{run_id}", path) is None]
    if missing:
        raise ValueError(f"approved {'/'.join(missing)} input gate(s) missing for {run_id}")


def _next_id(conn, table: str, column: str, prefix: str) -> str:
    values = [int(row[0].split("-")[1]) for row in conn.execute(
        f"SELECT {column} FROM {table}"  # identifiers are fixed internal constants
    )]
    return f"{prefix}-{max(values, default=0) + 1:04d}"


def render_template(path: Path, values: dict[str, object]) -> str:
    template = path.read_text(encoding="utf-8")
    missing = sorted(set(TOKEN.findall(template)) - set(values))
    if missing:
        raise ValueError(f"template values missing: {missing}")
    rendered = TOKEN.sub(lambda match: str(values[match.group(1)]), template)
    if TOKEN.search(rendered):
        raise ValueError("unresolved template token")
    return rendered


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temp, path)


def finding_page_values(row: dict) -> dict[str, object]:
    reference = row.get("evidence_item_id") or row.get("gap_id")
    return {
        "id": row["finding_id"], "status": row["status"],
        "source": f"db:findings/{row['finding_id']}; {reference}",
        "evaluation_run": row["evaluation_run_id"], "criterion_id": row["criterion_id"],
        "severity": row["severity"], "confidence": row["confidence"],
        "evidence_refs": reference, "basis": row["basis"],
        "basis_yaml": json.dumps(str(row["basis"]), ensure_ascii=False),
        "verification_status": row["verification_status"],
        "approval_ref": row.get("approval_ref") or "n-a",
        "title": row["title"], "body": row["body"],
    }


def action_page_values(row: dict) -> dict[str, object]:
    linked = row.get("finding_id") or row.get("gap_id")
    return {
        "id": row["action_id"], "approval_status": row["approval_status"],
        "source": f"db:auditor_actions/{row['action_id']}; {linked}",
        "evaluation_run": row["evaluation_run_id"], "action_type": row["action_type"],
        "linked_to": linked, "state": row["state"],
        "priority": str(bool(row["priority"])).lower(),
        "approval_ref": row.get("approval_ref") or "n-a",
        "description": row["description"],
    }


def write_finding(db: Path, record: dict, *, approvals: Path = APPROVALS,
                  wiki_dir: Path = FINDINGS_DIR) -> str:
    run_id, criterion_id = record["evaluation_run_id"], record["criterion_id"]
    require_input_gates(run_id, approvals)
    voc = vocabularies()
    if record.get("severity") not in voc["finding_severities"]:
        raise ValueError("invalid finding severity")
    if record.get("confidence") not in voc["finding_confidences"]:
        raise ValueError("invalid finding confidence")
    verification = record.get("verification_status", "pending")
    if verification not in voc["verification_statuses"]:
        raise ValueError("invalid verification status")
    evidence, gap = record.get("evidence_item_id"), record.get("gap_id")
    if bool(evidence) == bool(gap):
        raise ValueError("exactly one evidence crumb or gap link is required")
    with db_util.connect(db) as conn:
        evaluation = conn.execute(
            "SELECT evaluation_id FROM criterion_evaluations WHERE evaluation_run_id=? AND criterion_id=?",
            (run_id, criterion_id),
        ).fetchone()
        if not evaluation:
            raise ValueError("criterion evaluation missing for finding")
        if evidence:
            linked = conn.execute(
                "SELECT 1 FROM evaluation_evidence ee JOIN crumbs c ON c.item_id=ee.item_id "
                "WHERE ee.evaluation_id=? AND ee.item_id=? AND c.criterion_id=?",
                (evaluation["evaluation_id"], evidence, criterion_id),
            ).fetchone()
            if not linked:
                raise ValueError("finding evidence is not linked to the criterion evaluation")
        if gap:
            linked = conn.execute(
                "SELECT 1 FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) "
                "WHERE g.gap_id=? AND e.evaluation_run_id=? AND e.criterion_id=?",
                (gap, run_id, criterion_id),
            ).fetchone()
            if not linked:
                raise ValueError("finding gap does not belong to the run/criterion")
        finding_id = record.get("finding_id") or _next_id(conn, "findings", "finding_id", "FIND")
        values = {
            "finding_id": finding_id, "evaluation_run_id": run_id,
            "criterion_id": criterion_id, "evidence_item_id": evidence, "gap_id": gap,
            "title": record["title"], "body": record["body"],
            "severity": record["severity"], "confidence": record["confidence"],
            "basis": record["basis"], "verification_status": verification,
        }
        db_util.insert(conn, "findings", values)
    row = {**values, "status": "draft", "approval_ref": None}
    _atomic_write(wiki_dir / f"{finding_id}.md",
                  render_template(FINDING_TEMPLATE, finding_page_values(row)))
    return finding_id


def write_action(db: Path, record: dict, *, approvals: Path = APPROVALS,
                 wiki_dir: Path = ACTIONS_DIR) -> str:
    run_id = record["evaluation_run_id"]
    require_input_gates(run_id, approvals)
    voc = vocabularies()
    if record.get("action_type") not in voc["action_types"]:
        raise ValueError("invalid action type")
    state = record.get("state", "open")
    if state not in voc["action_states"]:
        raise ValueError("invalid action state")
    finding, gap = record.get("finding_id"), record.get("gap_id")
    if bool(finding) == bool(gap):
        raise ValueError("exactly one finding or gap link is required")
    with db_util.connect(db) as conn:
        if finding:
            linked = conn.execute(
                "SELECT 1 FROM findings WHERE finding_id=? AND evaluation_run_id=?",
                (finding, run_id),
            ).fetchone()
        else:
            linked = conn.execute(
                "SELECT 1 FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) "
                "WHERE g.gap_id=? AND e.evaluation_run_id=?", (gap, run_id),
            ).fetchone()
        if not linked:
            raise ValueError("action link does not belong to the evaluation run")
        action_id = record.get("action_id") or _next_id(
            conn, "auditor_actions", "action_id", "ACT"
        )
        values = {
            "action_id": action_id, "evaluation_run_id": run_id,
            "finding_id": finding, "gap_id": gap, "action_type": record["action_type"],
            "description": record["description"], "state": state,
            "priority": int(bool(record.get("priority", False))),
        }
        db_util.insert(conn, "auditor_actions", values)
    row = {**values, "approval_status": "draft", "approval_ref": None}
    _atomic_write(wiki_dir / f"{action_id}.md",
                  render_template(ACTION_TEMPLATE, action_page_values(row)))
    return action_id


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing frontmatter: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"invalid frontmatter: {path}")
    return data
