import hashlib
import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import evaluation_engine


def test_applicability_accepts_registered_document_scope_source(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    raw.mkdir()
    source = raw / "qms.md"
    source.write_text("# Controlled QMS procedure\n", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE documents (doc_id TEXT, filename TEXT, sha256 TEXT, document_side TEXT)"
    )
    conn.execute(
        "INSERT INTO documents VALUES (?,?,?,?)",
        ("DOC-0012", source.name, digest, "DOCUMENT"),
    )
    monkeypatch.setattr(evaluation_engine, "RAW", raw)
    monkeypatch.setattr(evaluation_engine, "local_path", lambda path: Path(path))

    evaluation_engine._raw_document(conn, "DOC-0012")
