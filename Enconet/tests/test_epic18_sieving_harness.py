from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_matrix  # noqa: E402
import db_util  # noqa: E402
import gate_packet  # noqa: E402
import import_crumbs  # noqa: E402
import init_db  # noqa: E402
import link_crumbs  # noqa: E402
import migrate_db  # noqa: E402
import resieve_run  # noqa: E402
import score_sieving  # noqa: E402
import sieve_diff  # noqa: E402
import sieve_generation  # noqa: E402
import sieve_metrics  # noqa: E402
import sieve_run  # noqa: E402
import validate_sieving_harness  # noqa: E402
import validate_sieving_skill_drift  # noqa: E402
from audit_state import StateError  # noqa: E402


FIXTURE = ROOT / "sieving" / "prompts" / "fixtures" / "valid_document.json"


@pytest.fixture
def database(tmp_path: Path) -> Path:
    path = tmp_path / "audit.sqlite"
    init_db.initialize(path)
    with db_util.connect(path) as conn:
        db_util.insert(conn, "documents", {
            "doc_id": "DOC-0002", "filename": "pilot.txt", "title": "Pilot",
            "supplier": "Enconet", "language": "en", "document_side": "DOCUMENT",
            "sha256": "b" * 64,
        })
        text = "Independent verification is required. Procedures shall be reviewed and approved before issue."
        db_util.insert(conn, "document_chunks", {
            "chunk_id": "CHUNK-DOC-0002-0001", "doc_id": "DOC-0002",
            "heading_path": "1", "chunk_text": text, "char_start": 0,
            "char_end": len(text), "source_sha256": "b" * 64,
        })
    return path


def variant(tmp_path: Path, *, statement: str = "Independent design verification is mandatory.") -> Path:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["items"][0]["statement"] = statement
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def initial_run(database: Path) -> None:
    result = sieve_run.create_run(
        database, run_id="RUN-20260716-01", doc_id="DOC-0002",
        prompt_version="appb_document_v1", document_side="DOCUMENT", authorities=[],
    )
    assert result == {"generation": 1, "status": "active", "supersedes_run_id": None, "warning": None}
    assert import_crumbs.import_file(database, FIXTURE, run_id="RUN-20260716-01", strict=True) == 1


def test_generations_are_immutable_unique_and_active_view_excludes_candidate(
    database: Path, tmp_path: Path,
) -> None:
    initial_run(database)
    result = sieve_run.create_run(
        database, run_id="RUN-20260716-02", doc_id="DOC-0002",
        prompt_version="appb_document_v2", document_side="DOCUMENT", authorities=[],
    )
    assert result["generation"] == 2 and result["status"] == "candidate"
    assert result["supersedes_run_id"] == "RUN-20260716-01"
    assert import_crumbs.import_file(database, variant(tmp_path), run_id="RUN-20260716-02", strict=True) == 1
    with pytest.raises(ValueError, match="already completed"):
        import_crumbs.import_file(database, variant(tmp_path), run_id="RUN-20260716-02", strict=True)
    with db_util.connect(database) as conn:
        assert conn.execute("SELECT count(*) FROM crumbs").fetchone()[0] == 2
        assert conn.execute("SELECT count(*) FROM active_crumbs").fetchone()[0] == 1
        assert conn.execute("SELECT item_id FROM crumbs ORDER BY item_id").fetchall()[0][0].endswith("0001")
        assert conn.execute("SELECT item_id FROM crumbs ORDER BY item_id").fetchall()[1][0].endswith("0002")
    rows = build_matrix.build(database)
    criterion = next(row for row in rows if row["criterion_id"] == "APP_B_III")
    assert criterion["document_evidence_count"] == 1


def test_unchanged_prompt_warns_and_resieve_writes_metrics_and_diff(
    database: Path, tmp_path: Path,
) -> None:
    initial_run(database)
    repeated = sieve_run.create_run(
        database, run_id="RUN-20260716-02", doc_id="DOC-0002",
        prompt_version="appb_document_v1", document_side="DOCUMENT", authorities=[],
    )
    assert "no-op tuning" in str(repeated["warning"])
    with db_util.connect(database) as conn:
        conn.execute("DELETE FROM sieve_runs WHERE run_id='RUN-20260716-02'")
    output = tmp_path / "runs"
    result = resieve_run.execute(
        database, run_id="RUN-20260716-02", doc_id="DOC-0002",
        prompt_version="appb_document_v2", document_side="DOCUMENT",
        json_file=variant(tmp_path), authorities=[], output_root=output,
        candidates=tmp_path / "candidates.csv", rejected_item_count=2, failed_item_count=1,
    )
    assert result["previous_run_id"] == "RUN-20260716-01"
    assert Path(result["metrics"]).is_file() and Path(result["diff"]).is_file()
    metrics = json.loads(Path(result["metrics"]).read_text(encoding="utf-8"))
    assert metrics["crumb_count"] == 1
    assert metrics["crumbs_per_criterion"]["APP_B_III"] == 1
    assert "APP_B_I" in metrics["zero_crumb_criteria"]
    assert metrics["quote_verification"]["rate_percent"] == 100.0
    assert metrics["rejected_item_count"] == 2 and metrics["failed_item_count"] == 1
    diff = json.loads(Path(result["diff"]).read_text(encoding="utf-8"))
    assert len(diff["criteria"]["APP_B_III"]["changed"]) == 1


def approvals_file(tmp_path: Path, *references: str) -> Path:
    path = tmp_path / "approvals.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["object_id", "decision", "date", "reviewer", "notes"])
        for reference in references:
            writer.writerow([reference, "approved", "2026-07-16", "Owner", "fixture"])
    return path


def test_golden_score_requires_real_approval_and_controls_promote_rollback(
    database: Path, tmp_path: Path,
) -> None:
    initial_run(database)
    candidate = variant(tmp_path)
    resieve_run.execute(
        database, run_id="RUN-20260716-02", doc_id="DOC-0002",
        prompt_version="appb_document_v2", document_side="DOCUMENT",
        json_file=candidate, authorities=[], output_root=tmp_path / "runs",
        candidates=tmp_path / "candidates.csv",
    )
    actual = json.loads(candidate.read_text(encoding="utf-8"))
    actual["prompt_version"] = "appb_document_v2"
    expected = {
        "fixture_version": "1.0", "status": "approved", "approval_ref": "GOLDEN-001",
        "expected_crumbs": [{"criterion_id": "APP_B_III",
                             "statement": actual["items"][0]["statement"],
                             "quotes": ["Independent verification is required."]}],
    }
    approvals = approvals_file(tmp_path, "GOLDEN-001", "PROMPT-v2", "ROLLBACK-v1")
    result = score_sieving.score(expected, actual, approvals=approvals)
    assert result["found"] == 1 and result["promotion_ready"] is True
    score_path = tmp_path / "score.json"
    score_path.write_text(json.dumps(result), encoding="utf-8")
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text("appb_document_v2 | lesson: crumb-quality\n", encoding="utf-8")
    active = tmp_path / "active.yml"
    active.write_text("schema_version: '1.0'\nactive:\n  DOCUMENT: appb_document_v1\n", encoding="utf-8")
    sieve_generation.decide(
        database, run_id="RUN-20260716-02", operation="promote",
        decision_ref="PROMPT-v2", reason="fixture improvement", approvals=approvals,
        score=score_path, active_prompts=active, changelog=changelog,
    )
    with db_util.connect(database) as conn:
        assert conn.execute("SELECT run_id FROM sieve_runs WHERE is_active=1").fetchone()[0] == "RUN-20260716-02"
        assert conn.execute("SELECT count(*) FROM sieve_generation_events").fetchone()[0] == 1
    sieve_generation.decide(
        database, run_id="RUN-20260716-01", operation="rollback",
        decision_ref="ROLLBACK-v1", reason="fixture regression", approvals=approvals,
        active_prompts=active, changelog=changelog,
    )
    with db_util.connect(database) as conn:
        assert conn.execute("SELECT run_id FROM sieve_runs WHERE is_active=1").fetchone()[0] == "RUN-20260716-01"
        assert [row[0] for row in conn.execute(
            "SELECT operation FROM sieve_generation_events ORDER BY event_id"
        )] == ["promote", "rollback"]
    assert yaml.safe_load(active.read_text(encoding="utf-8"))["active"]["DOCUMENT"] == "appb_document_v1"


def test_tampered_or_draft_golden_cannot_promote(database: Path, tmp_path: Path) -> None:
    initial_run(database)
    sieve_run.create_run(database, run_id="RUN-20260716-02", doc_id="DOC-0002",
                         prompt_version="appb_document_v2", document_side="DOCUMENT", authorities=[])
    import_crumbs.import_file(database, variant(tmp_path), run_id="RUN-20260716-02", strict=True)
    approvals = approvals_file(tmp_path, "PROMPT-v2")
    score = tmp_path / "score.json"
    score.write_text(json.dumps({"prompt_version": "appb_document_v2", "golden_approved": True,
                                 "golden_approval_ref": "NOT-APPROVED", "promotion_ready": True}), encoding="utf-8")
    changelog = tmp_path / "CHANGELOG.md"; changelog.write_text("appb_document_v2 | crumb-quality", encoding="utf-8")
    active = tmp_path / "active.yml"; active.write_text("active: {DOCUMENT: appb_document_v1}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="not approved"):
        sieve_generation.decide(database, run_id="RUN-20260716-02", operation="promote",
                                decision_ref="PROMPT-v2", reason="tamper", approvals=approvals,
                                score=score, active_prompts=active, changelog=changelog)
    draft = {"fixture_version": "draft", "status": "pending_human_approval", "approval_ref": None,
             "expected_crumbs": []}
    assert score_sieving.score(draft, {"prompt_version": "v", "items": []}, approvals=approvals)["golden_approved"] is False


def test_harness_validator_and_g2_packet_metrics_requirement(database: Path, tmp_path: Path) -> None:
    initial_run(database)
    runs = tmp_path / "runs"
    sieve_metrics.generate(database, "RUN-20260716-01", runs / "RUN-20260716-01")
    errors, notes = validate_sieving_harness.validate(
        database, runs=runs, allow_pending_claude=True,
    )
    assert errors == [] and any("pending human approval" in note for note in notes)
    with pytest.raises(StateError, match="active generation metrics"):
        gate_packet.create_packet(gate="G2", supplier="enconet", decision_ref="G2-RUN-fixture",
                                  summary="x", evidence="- crumbs", validation="PASS",
                                  output=tmp_path / "bad.md")
    gate_packet.create_packet(
        gate="G2", supplier="enconet", decision_ref="G2-RUN-fixture",
        summary="x", evidence="- sieving/runs/RUN-20260716-01/metrics.json",
        validation="PASS", output=tmp_path / "good.md",
    )


def legacy_database(tmp_path: Path, duplicate: bool = False) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "legacy.sqlite"
    with sqlite3.connect(path) as conn:
        conn.executescript("""
        CREATE TABLE documents(doc_id TEXT PRIMARY KEY);
        CREATE TABLE sieve_runs(run_id TEXT PRIMARY KEY,doc_id TEXT,prompt_version TEXT,document_side TEXT,source_rule TEXT,started_at TEXT);
        CREATE TABLE crumbs(item_id TEXT); CREATE TABLE crumb_quotes(quote_id TEXT);
        CREATE TABLE crumb_chunk_links(item_id TEXT,quote_id TEXT);
        CREATE TABLE requirements(requirement_id TEXT,parent_requirement_id TEXT,is_subrequirement INTEGER);
        CREATE TABLE criterion_evaluations(evaluation_id TEXT,coverage REAL);
        CREATE TABLE gaps(gap_id TEXT,evidence_item_id TEXT);
        CREATE TABLE findings(finding_id TEXT,evaluation_run_id TEXT);
        CREATE TABLE auditor_actions(action_id TEXT,approval_status TEXT);
        """)
        conn.execute("INSERT INTO documents VALUES ('DOC-0001')")
        conn.execute("INSERT INTO sieve_runs VALUES ('RUN-20260716-01','DOC-0001','v1','DOCUMENT',NULL,'now')")
        if duplicate:
            conn.execute("INSERT INTO sieve_runs VALUES ('RUN-20260716-02','DOC-0001','v2','DOCUMENT',NULL,'later')")
    return path


def test_migration_plans_generation_controls_without_mutating_and_refuses_ambiguity(tmp_path: Path) -> None:
    path = legacy_database(tmp_path)
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    assert "add EPIC18 sieve generation controls" in migrate_db.plan(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
    ambiguous = legacy_database(tmp_path / "other", duplicate=True)
    with pytest.raises(ValueError, match="run-by-run disposition"):
        migrate_db.plan(ambiguous)


def test_paired_skill_drift_validator_accepts_semantics_and_rejects_loss(tmp_path: Path) -> None:
    contract = yaml.safe_load(
        (ROOT / "schemas" / "sieving_skill_contract.yml").read_text(encoding="utf-8")
    )
    codex, claude = tmp_path / "codex", tmp_path / "claude"
    for name, spec in contract["skills"].items():
        text = "\n".join(str(marker) for marker in spec["required_semantics"])
        for root in (codex, claude):
            path = root / name / "SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    assert validate_sieving_skill_drift.validate(codex=codex, claude=claude) == []
    (claude / "crumb-quality" / "SKILL.md").write_text("verbatim only", encoding="utf-8")
    assert any("Claude crumb-quality" in error for error in
               validate_sieving_skill_drift.validate(codex=codex, claude=claude))
