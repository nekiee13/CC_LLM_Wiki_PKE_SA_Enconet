"""EPIC5 run guard, validator, fixtures, and transactional importer tests."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))
import db_util  # noqa: E402
import import_crumbs  # noqa: E402
import init_db  # noqa: E402
import sieve_run  # noqa: E402
from validate_app_b_json import validate_file, validate_payload  # noqa: E402

FIXTURES = ENCONET / "sieving" / "prompts" / "fixtures"


@pytest.fixture
def database(tmp_path: Path) -> Path:
    db = tmp_path / "test.sqlite"
    init_db.initialize(db)
    with db_util.connect(db) as conn:
        for doc_id, side, sha in (("DOC-0001", "RULE", "a" * 64), ("DOC-0002", "DOCUMENT", "b" * 64)):
            db_util.insert(conn, "documents", {"doc_id": doc_id, "filename": f"{doc_id}.md",
                "title": doc_id, "supplier": "ASME" if side == "RULE" else "Enconet",
                "language": "en", "document_side": side, "sha256": sha})
    return db


def test_prompt_fixtures_pass_pass_fail():
    assert validate_file(FIXTURES / "valid_rule.json")[1].passed
    assert validate_file(FIXTURES / "valid_document.json")[1].passed
    malformed = validate_file(FIXTURES / "malformed_placeholder.json")[1]
    assert not malformed.passed
    assert any("document_side" in error for error in malformed.errors)


def test_validator_rejects_side_leakage_bad_pairs_and_bad_quotes():
    payload = json.loads((FIXTURES / "valid_document.json").read_text(encoding="utf-8"))
    payload["document"]["authority_references"] = [{"authority_role":"GOVERNING","source_code":"10CFR21","source_locator":"21.21"}]
    payload["items"][0]["criterion_name"] = "Wrong"
    payload["items"][0]["evidence_quotes"][0]["quote_language"] = "de"
    result = validate_payload(payload)
    assert not result.passed
    assert len(result.errors) >= 4


def test_validator_rejects_document_item_authority_override():
    payload = json.loads((FIXTURES / "valid_document.json").read_text(encoding="utf-8"))
    payload["items"][0]["authority_references"] = [
        {"authority_role": "GOVERNING", "source_code": "10CFR50_APPB",
         "source_locator": "APP_B_I"}
    ]
    result = validate_payload(payload, strict=True)
    assert not result.passed
    assert any("DOCUMENT items require an empty list" in error for error in result.errors)


def test_run_guard_and_authority_roles(database: Path):
    with pytest.raises(ValueError, match="RULE run requires"):
        sieve_run.create_run(database, run_id="RUN-20260713-01", doc_id="DOC-0001",
            prompt_version="appb_rule_v1", document_side="RULE", authorities=[])
    with pytest.raises(ValueError, match="not valid for GOVERNING"):
        sieve_run.create_run(database, run_id="RUN-20260713-01", doc_id="DOC-0001",
            prompt_version="appb_rule_v1", document_side="RULE", authorities=[
                {"authority_role":"GOVERNING","source_code":"ASME_NQA1","source_locator":"REQ_03"}])
    sieve_run.create_run(database, run_id="RUN-20260713-01", doc_id="DOC-0001",
        prompt_version="appb_rule_v1", document_side="RULE", authorities=[
            {"authority_role":"INTERPRETIVE","source_code":"ASME_NQA1","source_locator":"REQ_03"}])


def test_import_preserves_all_sources_quotes_and_authorities(database: Path):
    sieve_run.create_run(database, run_id="RUN-20260713-01", doc_id="DOC-0001",
        prompt_version="appb_rule_v1", document_side="RULE", authorities=[
            {"authority_role":"INTERPRETIVE","source_code":"ASME_NQA1","source_locator":"REQ_03"}])
    assert import_crumbs.import_file(database, FIXTURES / "valid_rule.json", run_id="RUN-20260713-01") == 1
    with db_util.connect(database) as conn:
        assert conn.execute("SELECT count(*) FROM crumbs").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM crumb_sources").fetchone()[0] == 2
        assert conn.execute("SELECT count(*) FROM crumb_quotes").fetchone()[0] == 1
        assert conn.execute("SELECT source_code FROM crumb_authority_refs").fetchone()[0] == "ASME_NQA1"


def test_import_rolls_back_whole_file_on_database_failure(database: Path, tmp_path: Path):
    sieve_run.create_run(database, run_id="RUN-20260713-01", doc_id="DOC-0001",
        prompt_version="appb_rule_v1", document_side="RULE", authorities=[
            {"authority_role":"INTERPRETIVE","source_code":"ASME_NQA1","source_locator":"REQ_03"}])
    payload = json.loads((FIXTURES / "valid_rule.json").read_text(encoding="utf-8"))
    payload["items"][0]["sources"].append(copy.deepcopy(payload["items"][0]["sources"][0]))
    bad = tmp_path / "duplicate-source.json"
    bad.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        import_crumbs.import_file(database, bad, run_id="RUN-20260713-01")
    with db_util.connect(database) as conn:
        assert conn.execute("SELECT count(*) FROM crumbs").fetchone()[0] == 0
