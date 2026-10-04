"""Single project-local SQLite access helper for audit pipeline scripts."""
from __future__ import annotations

import re
import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

import yaml
from project_paths import local_path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "db" / "nqa_audit.sqlite"
PATTERNS = ROOT / "schemas" / "id_patterns.yml"
SAFE_IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
CONTEXT_SCHEMA = """
CREATE TABLE IF NOT EXISTS crumb_context (
    item_id TEXT PRIMARY KEY REFERENCES crumbs(item_id) ON DELETE CASCADE,
    evidence_type TEXT,
    project_ref TEXT,
    contract_ref TEXT,
    supplier_ref TEXT,
    source_revision TEXT,
    evidence_date TEXT,
    CHECK (evidence_type IS NULL OR length(trim(evidence_type)) > 0),
    CHECK (project_ref IS NULL OR length(trim(project_ref)) > 0),
    CHECK (contract_ref IS NULL OR length(trim(contract_ref)) > 0),
    CHECK (supplier_ref IS NULL OR length(trim(supplier_ref)) > 0),
    CHECK (source_revision IS NULL OR length(trim(source_revision)) > 0),
    CHECK (evidence_date IS NULL OR length(trim(evidence_date)) > 0)
) STRICT;
"""

ID_COLUMNS = {
    "documents": {"doc_id": "doc_id"},
    "document_chunks": {"chunk_id": "chunk_id", "doc_id": "doc_id"},
    "sieve_runs": {"run_id": "run_id", "doc_id": "doc_id"},
    "crumbs": {"item_id": "crumb_id", "doc_id": "doc_id", "sieve_run_id": "run_id"},
    "crumb_quotes": {"quote_id": "quote_id", "item_id": "crumb_id"},
    "requirements": {"requirement_id": "requirement_id", "source_item_id": "crumb_id"},
    "evaluation_runs": {"run_id": "run_id"},
    "criterion_evaluations": {"evaluation_id": "evaluation_id", "evaluation_run_id": "run_id"},
    "gaps": {"gap_id": "gap_id", "evaluation_id": "evaluation_id"},
    "findings": {"finding_id": "finding_id", "evidence_item_id": "crumb_id", "gap_id": "gap_id"},
    "auditor_actions": {"action_id": "action_id", "finding_id": "finding_id", "gap_id": "gap_id"},
    "dashboard_runs": {"dashboard_id": "dashboard_id", "evaluation_run_id": "run_id"},
}


@lru_cache(maxsize=1)
def id_patterns() -> dict[str, re.Pattern[str]]:
    raw = yaml.safe_load(local_path(PATTERNS).read_text(encoding="utf-8"))["patterns"]
    return {name: re.compile(spec["regex"]) for name, spec in raw.items()}


def connect(path: Path | str = DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(local_path(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        conn.close()
        raise RuntimeError("SQLite foreign-key enforcement could not be enabled")
    return conn


def ensure_crumb_context_schema(conn: sqlite3.Connection) -> None:
    """Apply the additive context-table migration to an older local database."""
    conn.executescript(CONTEXT_SCHEMA)


def _validate_ids(table: str, values: Mapping[str, Any]) -> None:
    for column, pattern_name in ID_COLUMNS.get(table, {}).items():
        value = values.get(column)
        if value is None:
            continue
        pattern = id_patterns().get(pattern_name)
        if pattern is None or pattern.fullmatch(str(value)) is None:
            raise ValueError(f"invalid {pattern_name} in {table}.{column}: {value!r}")


def _check_identifier(value: str) -> None:
    if SAFE_IDENTIFIER.fullmatch(value) is None:
        raise ValueError(f"unsafe SQL identifier: {value!r}")


def insert(conn: sqlite3.Connection, table: str, values: Mapping[str, Any]) -> None:
    if not values:
        raise ValueError("insert values must not be empty")
    _check_identifier(table)
    for column in values:
        _check_identifier(column)
    _validate_ids(table, values)
    columns = list(values)
    sql = (f"INSERT INTO {table} ({', '.join(columns)}) VALUES "
           f"({', '.join('?' for _ in columns)})")
    try:
        conn.execute(sql, [values[column] for column in columns])
    except sqlite3.IntegrityError as exc:
        identifier = next((values[c] for c in columns if c.endswith("_id")), "unknown")
        raise ValueError(f"insert into {table} failed for ID {identifier!r}: {exc}") from exc


def exists(conn: sqlite3.Connection, table: str, id_column: str, value: Any) -> bool:
    _check_identifier(table)
    _check_identifier(id_column)
    row = conn.execute(
        f"SELECT 1 FROM {table} WHERE {id_column} = ? LIMIT 1", (value,)
    ).fetchone()
    return row is not None


def lookup(conn: sqlite3.Connection, table: str, id_column: str,
           value: Any) -> sqlite3.Row | None:
    _check_identifier(table)
    _check_identifier(id_column)
    return conn.execute(
        f"SELECT * FROM {table} WHERE {id_column} = ?", (value,)
    ).fetchone()
