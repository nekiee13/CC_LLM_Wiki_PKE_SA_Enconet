#!/usr/bin/env python3
"""Build a diagnostic 18-criterion evidence matrix from a local database."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

import yaml

import db_util
from project_paths import configure_standard_streams, local_path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ROOT / "schemas" / "app_b_taxonomy.yml"


def _baseline() -> list[str]:
    data = yaml.safe_load(local_path(TAXONOMY).read_text(encoding="utf-8"))
    rows = data.get("criteria") if isinstance(data, dict) else None
    if not isinstance(rows, list) or len(rows) != 18:
        raise ValueError("local Appendix B taxonomy must contain 18 criteria")
    ids = [row.get("criterion_id") for row in rows if isinstance(row, dict)]
    if len(ids) != 18 or any(not isinstance(value, str) for value in ids) or len(set(ids)) != 18:
        raise ValueError("local Appendix B taxonomy has invalid or duplicate criterion IDs")
    return ids


def _count(conn: sqlite3.Connection, query: str, params: tuple[str, ...]) -> int:
    return conn.execute(query, params).fetchone()[0]


def _evidence_types(conn: sqlite3.Connection, criterion_id: str) -> dict[str, int]:
    rows = conn.execute(
        "SELECT COALESCE(x.evidence_type, 'untyped') AS evidence_type, count(*) AS count "
        "FROM active_crumbs c LEFT JOIN crumb_context x ON x.item_id=c.item_id "
        "WHERE c.criterion_id=? AND c.document_side='DOCUMENT' "
        "GROUP BY COALESCE(x.evidence_type, 'untyped') ORDER BY evidence_type", (criterion_id,)
    )
    return {row["evidence_type"]: int(row["count"]) for row in rows}


def build(db: Path, run_id: str | None = None) -> list[dict]:
    """Read a complete local baseline; never initialize or mutate the database."""
    if run_id is not None and db_util.id_patterns()["run_id"].fullmatch(run_id) is None:
        raise ValueError(f"invalid evaluation run ID: {run_id}")
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    baseline = _baseline()
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = ON")
        criteria = {row["criterion_id"]: row["criterion_name"]
                    for row in conn.execute("SELECT criterion_id,criterion_name FROM criteria")}
        if set(criteria) != set(baseline):
            raise ValueError("database criteria differ from the 18-criterion local taxonomy")
        if run_id is None and conn.execute("SELECT 1 FROM evaluation_runs LIMIT 1").fetchone() is not None:
            raise ValueError("specify an evaluation run; unscoped counts would mix runs")
        if run_id is not None and db_util.lookup(conn, "evaluation_runs", "run_id", run_id) is None:
            raise ValueError(f"unknown evaluation run: {run_id}")
        rows: list[dict] = []
        for cid in baseline:
            app = conn.execute(
                "SELECT applicable, applicability_state, conditional_confirmation_ref "
                "FROM criterion_applicability "
                "WHERE evaluation_run_id=? AND criterion_id=?", (run_id, cid),
            ).fetchone() if run_id is not None else None
            run_filter = " AND e.evaluation_run_id=?" if run_id is not None else ""
            gap_params = (cid, run_id) if run_id is not None else (cid,)
            finding_filter = " AND evaluation_run_id=?" if run_id is not None else ""
            action_filter = " AND a.evaluation_run_id=?" if run_id is not None else ""
            rows.append({
                "criterion_id": cid,
                "criterion_name": criteria[cid],
                "applicability": app["applicability_state"] if app is not None else "unruled",
                "conditional_confirmation_ref": (
                    app["conditional_confirmation_ref"] if app is not None else None
                ),
                "rule_evidence_count": _count(conn,
                    "SELECT count(*) FROM active_crumbs WHERE criterion_id=? AND document_side='RULE'", (cid,)),
                "document_evidence_count": _count(conn,
                    "SELECT count(*) FROM active_crumbs WHERE criterion_id=? AND document_side='DOCUMENT'", (cid,)),
                "anchored_document_evidence_count": _count(conn,
                    "SELECT count(*) FROM active_crumbs c JOIN crumb_context x ON x.item_id=c.item_id "
                    "WHERE c.criterion_id=? AND c.document_side='DOCUMENT' "
                    "AND (x.project_ref IS NOT NULL OR x.contract_ref IS NOT NULL OR "
                    "x.supplier_ref IS NOT NULL OR x.source_revision IS NOT NULL OR x.evidence_date IS NOT NULL)", (cid,)),
                "evidence_type_counts": _evidence_types(conn, cid),
                "gap_count": _count(conn,
                    "SELECT count(*) FROM gaps g JOIN criterion_evaluations e USING(evaluation_id) "
                    "WHERE e.criterion_id=?" + run_filter, gap_params),
                "finding_count": _count(conn,
                    "SELECT count(*) FROM findings WHERE criterion_id=?" + finding_filter, gap_params),
                "action_count": _count(conn,
                    "SELECT count(*) FROM auditor_actions a "
                    "LEFT JOIN findings f ON f.finding_id=a.finding_id "
                    "LEFT JOIN gaps g ON g.gap_id=a.gap_id "
                    "LEFT JOIN criterion_evaluations e ON e.evaluation_id=g.evaluation_id "
                    "WHERE COALESCE(f.criterion_id,e.criterion_id)=?" + action_filter,
                    gap_params),
            })
    return rows


def render_json(rows: list[dict]) -> bytes:
    return (json.dumps(rows, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def render_md(rows: list[dict], run_id: str | None = None) -> str:
    source = f"db:{run_id}" if run_id else "db:pre-execution-evidence-matrix"
    lines = [
        "---", "id: evidence-matrix", "type: evidence", "status: generated",
        "content_origin: generated", f"source: {source}", "criterion_id: n-a",
        "generated_by: scripts/build_matrix.py", "---",
        "| Criterion | Applicability | RULE | DOCUMENT | Anchored | Evidence types | Gaps | Findings | Actions |",
        "|---|---:|---:|---:|---:|---|---:|---:|---:|",
    ]
    for row in rows:
        name = row["criterion_name"].replace("|", "\\|").replace("\r", " ").replace("\n", " ")
        lines.append(
            f"| {row['criterion_id']} {name} | {row['applicability']} | "
            f"{row['rule_evidence_count']} | {row['document_evidence_count']} | "
            f"{row['anchored_document_evidence_count']} | "
            f"{', '.join(f'{key}:{value}' for key, value in row['evidence_type_counts'].items()) or 'none'} | "
            f"{row['gap_count']} | {row['finding_count']} | {row['action_count']} |"
        )
    return "\n".join(lines) + "\n"


def write_matrix(db: Path, run_id: str | None, json_output: Path, md_output: Path) -> str:
    json_path = local_path(json_output)
    md_path = local_path(md_output)
    if json_path == md_path:
        raise ValueError("JSON and Markdown targets must differ")
    rows = build(db, run_id)
    json_bytes = render_json(rows)
    md_bytes = render_md(rows, run_id).encode("utf-8")
    if json_path.exists() or md_path.exists():
        if (json_path.is_file() and md_path.is_file() and
                json_path.read_bytes() == json_bytes and md_path.read_bytes() == md_bytes):
            return "preserved"
        raise ValueError("matrix output exists or is incomplete; refusing rewrite")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        with json_path.open("xb") as handle:
            created.append(json_path)
            handle.write(json_bytes)
        with md_path.open("xb") as handle:
            created.append(md_path)
            handle.write(md_bytes)
    except Exception:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    return "created"


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id")
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    try:
        mode = write_matrix(args.db, args.run_id, args.json, args.markdown)
        print(f"build_matrix: PASS - criteria=18; {mode}; diagnostic only")
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, yaml.YAMLError) as exc:
        print(f"build_matrix: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
