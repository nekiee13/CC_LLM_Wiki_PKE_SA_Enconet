import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "build_reviewed_candidate.py"
spec = importlib.util.spec_from_file_location("build_reviewed_candidate", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def setup_case():
    source = "# 1. Control\r\n\r\nKeep records.\r\n\r\n# 2. Follow-up\r\nCheck results.\r\n"
    config = {"doc_id": "DOC-0099", "name": "Example", "source_sha256": builder.sha(source.encode()),
              "registered_sha256": "0" * 64, "prompt_version": "test", "prefix": "REVIEW",
              "language": "en", "date": "n-a", "context": {},
              "sections": [{"start": 1, "end": 4, "chapter": "1 Control", "pass1": "Record control.", "pass2": "Traceable records support XVII."},
                           {"start": 5, "end": 6, "chapter": "2 Follow-up", "pass1": "Follow-up.", "pass2": "Effectiveness supports XVI."}]}
    entries = [{"start": "3", "end": "3", "criterion": "XVII", "strength": "objective_control", "pass": "1", "type": "control", "statement": "Retain records."},
               {"start": "6", "end": "6", "criterion": "XVI", "strength": "supporting_control", "pass": "2", "type": "control", "statement": "Check effectiveness."}]
    criteria = {"APP_B_XVII": "Quality Assurance Records", "APP_B_XVI": "Corrective Action"}
    return source, config, entries, criteria


def test_exact_quotes_and_read_coverage():
    source, config, entries, criteria = setup_case()
    payload, provenance = builder.prepare(source.encode(), config, entries, criteria)
    assert len(payload["items"]) == 2
    assert payload["items"][0]["evidence_quotes"][0]["quote_original"] == "Keep records."
    assert provenance["line_count"] == 6
    assert len(provenance["line_coverage"]) == 6
    assert provenance["source_revision_registered"] is False
    assert provenance["import_ready"] is False
    assert provenance["metrics"]["direct_items"] == 1
    assert provenance["metrics"]["concept_items"] == 1
    for q in provenance["quote_locations"]:
        assert source[q["char_start"]:q["char_end"]] == q["quote_original"]


@pytest.mark.parametrize("defect", ["hash", "range", "gap", "overlap", "missing_review", "criterion", "strength", "duplicate"])
def test_fail_closed(defect):
    source, config, entries, criteria = setup_case()
    if defect == "hash": config["source_sha256"] = "1" * 64
    if defect == "range": entries[0]["end"] = "99"
    if defect == "gap": config["sections"][0]["end"] = 3
    if defect == "overlap": config["sections"][0]["end"] = 5
    if defect == "missing_review": config["sections"][0]["pass2"] = ""
    if defect == "criterion": entries[0]["criterion"] = "XX"
    if defect == "strength": entries[0]["strength"] = "proven"
    if defect == "duplicate": entries.append(dict(entries[0]))
    with pytest.raises(ValueError):
        builder.prepare(source.encode(), config, entries, criteria)


def test_distinct_control_ideas_can_share_quote():
    source, config, entries, criteria = setup_case()
    entries.append({**entries[0], "statement": "The records provide a retrievable trail.", "pass": "2", "strength": "supporting_control"})
    payload, _ = builder.prepare(source.encode(), config, entries, criteria)
    assert len(payload["items"]) == 3


def test_context_cannot_be_invented():
    source, config, entries, criteria = setup_case()
    config["context"] = {"project_ref": "INVENTED"}
    with pytest.raises(ValueError, match="context"):
        builder.prepare(source.encode(), config, entries, criteria)


@pytest.mark.parametrize("name", ["Company A", "Čista tvrtka"])
@pytest.mark.parametrize("sibling", [True, False])
def test_intake_preview_readonly_and_company_neutral(tmp_path, name, sibling):
    source, config, entries, criteria = setup_case()
    root = tmp_path / name
    for folder in ("raw", "db", "out"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    old = b"Old source"
    config["registered_sha256"] = builder.sha(old)
    config["source"] = "out/replacement.md"
    (root / "out/replacement.md").write_bytes(source.encode())
    (root / "raw/old.md").write_bytes(old)
    db = root / "db/nqa_audit.sqlite"
    with sqlite3.connect(db) as conn:
        conn.executescript("CREATE TABLE documents(doc_id TEXT,filename TEXT,sha256 TEXT); CREATE TABLE sieve_runs(run_id TEXT,doc_id TEXT,status TEXT,is_active INT,prompt_version TEXT,generation INT); CREATE TABLE document_chunks(chunk_id TEXT,doc_id TEXT,heading_path TEXT,char_start INT,char_end INT,source_sha256 TEXT); CREATE TABLE crumbs(item_id TEXT,sieve_run_id TEXT,criterion_id TEXT,statement TEXT); CREATE TABLE crumb_quotes(item_id TEXT,quote_original TEXT);")
        conn.execute("INSERT INTO documents VALUES(?,?,?)", (config["doc_id"], "old.md", builder.sha(old)))
    if sibling:
        (tmp_path / "Other").mkdir()
        (tmp_path / "Other/source.md").write_bytes(b"other company")
    before = {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    payload, _ = builder.prepare(source.encode(), config, entries, criteria)
    preview = builder.intake_preview(root, config, payload)
    assert preview["live_writes"] == 0
    assert preview["replacement_kind"] == "unspecified_requires_review"
    assert all(Path(p).read_bytes() == data for p, data in before.items())
    with pytest.raises(ValueError):
        builder.local(tmp_path / "Other/source.md", root)
    config["registered_sha256"] = "f" * 64
    with pytest.raises(ValueError, match="predecessor"):
        builder.intake_preview(root, config, payload)
