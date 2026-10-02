from __future__ import annotations

import csv
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "report_stack" / "v1" / "scripts"))
sys.path.insert(0, str(ROOT))

from bootstrap_report_stack import apply, preview  # noqa: E402
from report_stack_core import (  # noqa: E402
    build_dashboard_data,
    build_package,
    render_dashboard,
    render_report,
    validate_dashboard,
    validate_report,
)


def _fixture(tmp_path: Path) -> tuple[Path, Path, str]:
    project = tmp_path / "Company with č spaces"
    db = project / "db" / "audit.sqlite"
    schemas = project / "schemas"
    schemas.mkdir(parents=True)
    db.parent.mkdir(parents=True)
    (schemas / "scoring_model.yml").write_text(
        """model_version: test-1
rating_weights:
  fully: 1.0
  substantially: 0.75
  partially: 0.5
  minimally: 0.25
  unmet: 0.0
  undetermined: 0.0
  na: null
classification_thresholds:
  - {min_score: 90.0, class: fully}
  - {min_score: 70.0, class: substantially}
  - {min_score: 40.0, class: partially}
  - {min_score: 10.0, class: minimally}
  - {min_score: 0.0, class: unmet}
""",
        encoding="utf-8",
    )
    run_id = "RUN-20261002-01"
    with sqlite3.connect(db) as conn:
        conn.executescript(
            """CREATE TABLE criteria (criterion_id TEXT PRIMARY KEY, criterion_name TEXT);
CREATE TABLE evaluation_runs (run_id TEXT PRIMARY KEY, supplier TEXT, deliverable_language TEXT, scoring_model_version TEXT);
CREATE TABLE criterion_applicability (evaluation_run_id TEXT, criterion_id TEXT, applicable INTEGER, justification TEXT, scope_source_doc_id TEXT, approved_by TEXT, approved_date TEXT, decision_ref TEXT);
CREATE TABLE criterion_evaluations (evaluation_id TEXT, evaluation_run_id TEXT, criterion_id TEXT, rating TEXT, score REAL, coverage REAL, completeness REAL, accuracy REAL, clarity REAL, alignment REAL, evidence_supported INTEGER, affirmative_summary TEXT, contrary_summary TEXT, judge_ruling TEXT, rationale TEXT);
CREATE TABLE evaluation_evidence (evaluation_id TEXT, item_id TEXT);
CREATE TABLE gaps (gap_id TEXT, evaluation_id TEXT, status TEXT, description TEXT, evidence_item_id TEXT, missing_evidence_ref TEXT);
CREATE TABLE findings (finding_id TEXT, evaluation_run_id TEXT, criterion_id TEXT, title TEXT, body TEXT, status TEXT);
CREATE TABLE auditor_actions (action_id TEXT, evaluation_run_id TEXT, description TEXT, priority INTEGER, approval_status TEXT);"""
        )
        conn.execute("INSERT INTO evaluation_runs VALUES (?,?,?,?)", (run_id, "Četa  Audit", "en", "test-1"))
        for index in range(1, 19):
            cid = f"B-{index:02d}"
            conn.execute("INSERT INTO criteria VALUES (?,?)", (cid, f"Criterion {index}"))
            conn.execute("INSERT INTO criterion_applicability VALUES (?,?,?,?,?,?,?,?)", (run_id, cid, 1, "synthetic scope", "DOC-0001", "owner", "2026-10-02", f"G2-{run_id}"))
            rating = "unmet" if index == 18 else "fully"
            eid = f"EVAL-{index:02d}"
            conn.execute("INSERT INTO criterion_evaluations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (eid, run_id, cid, rating, 0.0 if rating == "unmet" else 100.0, 1, 1, 1, 1, 1, 0, "", "missing proof" if rating == "unmet" else "", "open", "synthetic"))
            if index != 18:
                conn.execute("INSERT INTO evaluation_evidence VALUES (?,?)", (eid, f"CRUMB-{index:02d}"))
            else:
                conn.execute("INSERT INTO gaps VALUES (?,?,?,?,?,?)", ("GAP-18-01", eid, "missing-evidence", "sample evidence is missing", None, "request-18"))
        conn.commit()
    approvals = project / "manifests" / "approvals.csv"
    approvals.parent.mkdir(parents=True)
    with approvals.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["object_id", "decision", "date", "reviewer", "notes"])
        for gate in ("G2", "G3", "G4"):
            writer.writerow([f"{gate}-{run_id}", "approved", "2026-10-02", "owner", "synthetic"])
    return db, approvals, run_id


def test_report_stack_projects_one_run_and_keeps_missing_evidence_open(tmp_path: Path):
    db, approvals, run_id = _fixture(tmp_path)
    package = build_package(db, run_id, approvals)
    assert package["metrics"]["applicable_count"] == 18
    assert package["gaps"][0]["status"] == "missing-evidence"
    report = render_report(package)
    assert not validate_report(package, report)
    data = build_dashboard_data(package, "2026-10-02T00:00:00Z", "DASH-20261002-0001")
    dashboard = render_dashboard(data)
    assert not validate_dashboard(package, data, dashboard)
    assert "missing-evidence" not in report or "GAP-18-01" in report
    assert "Četa  Audit" in dashboard


def test_report_requires_gate_and_dashboard_is_offline(tmp_path: Path):
    db, approvals, run_id = _fixture(tmp_path)
    package = build_package(db, run_id, approvals)
    package["approvals"] = [row for row in package["approvals"] if row["object_id"] != f"G4-{run_id}"]
    with pytest.raises(ValueError, match="G4"):
        render_report(package)
    data = build_dashboard_data(build_package(db, run_id, approvals), "2026-10-02T00:00:00Z", "DASH-20261002-0001")
    assert "https://" not in render_dashboard(data)


def test_bootstrap_preview_is_read_only(tmp_path: Path):
    target = tmp_path / "Synthetic č Audit"
    target.mkdir()
    before = sorted(path.relative_to(target).as_posix() for path in target.rglob("*"))
    result = preview(target)
    assert result["mode"] == "preview"
    assert all(row["state"] == "create" for row in result["files"])
    assert sorted(path.relative_to(target).as_posix() for path in target.rglob("*")) == before


def test_bootstrap_apply_is_local_and_retryable(tmp_path: Path):
    first = tmp_path / "A company č"
    sibling = tmp_path / "B company with spaces"
    first.mkdir()
    sibling.mkdir()
    sentinel = sibling / "owner-note.txt"
    sentinel.write_text("keep", encoding="utf-8")
    result = apply(first, "report-stack-test-01")
    assert len(result["created"]) == 7
    assert sentinel.read_text(encoding="utf-8") == "keep"
    retry = apply(first, "report-stack-test-02")
    assert retry["created"] == []
    assert len(retry["preserved"]) == 7
