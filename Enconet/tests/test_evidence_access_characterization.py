"""EA0.1 characterization tests for the committed production evidence fixture."""
from __future__ import annotations

import sqlite3
from pathlib import Path


ENCONET = Path(__file__).resolve().parents[1]
PRODUCTION_DB = ENCONET / "db" / "nqa_audit.sqlite"


def test_known_production_crumb_resolves_three_quotes_to_expected_chunk():
    database_uri = f"{PRODUCTION_DB.resolve().as_uri()}?mode=ro"
    with sqlite3.connect(database_uri, uri=True) as connection:
        rows = connection.execute(
            """
            SELECT q.quote_original, link.chunk_id
            FROM active_crumbs AS crumb
            JOIN crumb_quotes AS q ON q.item_id = crumb.item_id
            JOIN crumb_chunk_links AS link
              ON link.item_id = q.item_id AND link.quote_id = q.quote_id
            WHERE crumb.item_id = ?
            ORDER BY q.quote_id
            """,
            ("CRUMB-DOC-0021-APP_B_I-0003",),
        ).fetchall()

    assert len(rows) == 3
    assert all(quote.strip() for quote, _chunk_id in rows)
    assert {chunk_id for _quote, chunk_id in rows} == {"CHUNK-DOC-0021-0105"}
