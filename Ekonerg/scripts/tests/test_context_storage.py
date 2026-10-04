import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import db_util


def test_context_table_is_additive_and_keeps_anchor_values():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        "CREATE TABLE crumbs (item_id TEXT PRIMARY KEY);"
        "INSERT INTO crumbs VALUES ('CRUMB-DOC-0001-APP_B_I-0001');"
    )
    db_util.ensure_crumb_context_schema(conn)
    db_util.insert(conn, "crumb_context", {
        "item_id": "CRUMB-DOC-0001-APP_B_I-0001",
        "evidence_type": "objective_record",
        "project_ref": "MOD-1281",
        "contract_ref": "PO-17",
        "supplier_ref": "Synthetic supplier",
        "source_revision": "rev. 2",
        "evidence_date": "2026-10-04",
    })
    row = conn.execute("SELECT * FROM crumb_context").fetchone()
    assert row["project_ref"] == "MOD-1281"
    assert row["evidence_type"] == "objective_record"
