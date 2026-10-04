#!/usr/bin/env python3
"""Preview or append same-document quote links for one completed local run."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

import db_util
from evidence_matching import quote_matches
from project_paths import configure_standard_streams, local_path

ROOT = Path(__file__).resolve().parents[1]


def _plan(conn: sqlite3.Connection, run_id: str) -> tuple[dict, list[tuple]]:
    run = db_util.lookup(conn, "sieve_runs", "run_id", run_id)
    if run is None or run["completed_at"] is None:
        raise ValueError("sieve run is missing or not completed")
    document = db_util.lookup(conn, "documents", "doc_id", run["doc_id"])
    if document is None:
        raise ValueError("sieve run document is missing")
    chunks = conn.execute(
        "SELECT chunk_id,chunk_text,source_sha256 FROM document_chunks "
        "WHERE doc_id=? ORDER BY chunk_id", (run["doc_id"],)
    ).fetchall()
    if any(chunk["source_sha256"] != document["sha256"] for chunk in chunks):
        raise ValueError("same-document chunk hash differs from the registered source")
    quotes = conn.execute(
        "SELECT q.quote_id,q.item_id,q.quote_original FROM crumb_quotes q "
        "JOIN crumbs c ON c.item_id=q.item_id WHERE c.sieve_run_id=? "
        "ORDER BY q.quote_id", (run_id,)
    ).fetchall()
    if not quotes:
        raise ValueError("completed sieve run has no quotes to link")
    existing = conn.execute(
        "SELECT l.item_id,l.quote_id,l.chunk_id,l.link_method,l.confidence "
        "FROM crumb_chunk_links l JOIN crumbs c ON c.item_id=l.item_id "
        "WHERE c.sieve_run_id=?", (run_id,)
    ).fetchall()
    current: dict[str, set[tuple]] = {}
    for row in existing:
        current.setdefault(row["quote_id"], set()).add(tuple(row))
    unknown_links = set(current) - {quote["quote_id"] for quote in quotes}
    if unknown_links:
        raise ValueError("run contains links to quotes outside this run")
    unmatched: list[dict[str, str]] = []
    additions: list[tuple] = []
    for quote in quotes:
        literal = quote["quote_original"]
        exact = [chunk for chunk in chunks if literal in chunk["chunk_text"]]
        matches = exact or [chunk for chunk in chunks
                            if quote_matches(literal, chunk["chunk_text"])]
        method = "EXACT" if exact else "NORMALIZED"
        expected = {(quote["item_id"], quote["quote_id"], chunk["chunk_id"],
                     method, 1.0 if exact else 0.95) for chunk in matches}
        prior = current.get(quote["quote_id"], set())
        if prior and prior != expected:
            raise ValueError(f"existing quote links differ; refusing rewrite: {quote['quote_id']}")
        if not matches:
            unmatched.append({"item_id": quote["item_id"], "quote_id": quote["quote_id"],
                              "doc_id": run["doc_id"], "reason": "quote not found in same-document chunks"})
        elif not prior:
            additions.extend(sorted(expected))
    metrics = local_path(ROOT / "sieving" / "runs" / run_id / "metrics.json")
    metrics_md = local_path(ROOT / "sieving" / "runs" / run_id / "metrics.md")
    if additions and (metrics.exists() or metrics_md.exists()):
        raise ValueError("prior metrics exist; new links would make them stale")
    summary = {"run_id": run_id, "doc_id": run["doc_id"], "quotes": len(quotes),
               "links_to_add": len(additions), "existing_links": len(existing),
               "unmatched": unmatched}
    return summary, additions


def link(db: Path, run_id: str, *, apply: bool = False) -> dict:
    if db_util.id_patterns()["run_id"].fullmatch(run_id) is None:
        raise ValueError(f"invalid sieve run ID: {run_id}")
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    if apply:
        with closing(db_util.connect(database)) as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                summary, additions = _plan(conn, run_id)
                conn.executemany(
                    "INSERT INTO crumb_chunk_links "
                    "(item_id,quote_id,chunk_id,link_method,confidence) VALUES (?,?,?,?,?)",
                    additions,
                )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    else:
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            summary, _ = _plan(conn, run_id)
    summary["mode"] = "apply" if apply else "preview"
    summary["verification"] = "incomplete" if summary["unmatched"] else "linked-not-human-approved"
    return summary


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        result = link(args.db, args.run_id, apply=args.apply)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 2 if args.apply and result["unmatched"] else 0
    except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"link_crumbs: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
