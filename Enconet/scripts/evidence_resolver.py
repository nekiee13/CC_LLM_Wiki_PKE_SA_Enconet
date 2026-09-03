#!/usr/bin/env python3
"""Read-only, fail-closed SQLite evidence projection for one active crumb."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TypedDict

import evidence_navigation


class EvidenceIntegrityError(RuntimeError):
    """Raised when stored evidence cannot be resolved without ambiguity."""


class ResolvedCrumb(TypedDict):
    """Renderer-independent entity projection consumed by later bundle tasks."""

    crumb: dict
    document: dict
    quotes: list[dict]
    chunks: list[dict]


@contextmanager
def _connect_readonly(db_path: Path | str) -> Iterator[sqlite3.Connection]:
    """Open an existing SQLite file with both URI and connection write guards."""
    path = Path(db_path).resolve()
    connection = sqlite3.connect(f"{path.as_uri()}?mode=ro", uri=True)
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA query_only = ON")
        if connection.execute("PRAGMA query_only").fetchone()[0] != 1:
            raise RuntimeError("SQLite query-only enforcement could not be enabled")
        yield connection
    finally:
        connection.close()


def _target(entity_type: str, entity_id: str) -> str:
    try:
        return evidence_navigation.target(entity_type, entity_id)
    except (TypeError, ValueError) as exc:
        raise EvidenceIntegrityError(
            f"invalid stored {entity_type} identifier: {entity_id!r}"
        ) from exc


def resolve_crumb(db_path: Path | str, crumb_id: str) -> ResolvedCrumb | None:
    """Resolve one active crumb or return None when it is not active/present."""
    with _connect_readonly(db_path) as connection:
        crumb = connection.execute(
            """
            SELECT c.item_id, c.doc_id, c.criterion_id, c.document_side,
                   c.statement, c.item_type,
                   d.filename, d.title, d.language AS document_language,
                   d.document_side AS source_document_side, d.sha256
            FROM active_crumbs AS c
            LEFT JOIN documents AS d ON d.doc_id = c.doc_id
            WHERE c.item_id = ?
            """,
            (crumb_id,),
        ).fetchone()
        if crumb is None:
            return None
        if any(crumb[field] is None for field in (
            "filename", "title", "document_language", "source_document_side", "sha256"
        )):
            raise EvidenceIntegrityError(f"missing document for crumb {crumb_id}")

        quote_rows = connection.execute(
            """
            SELECT q.quote_id, q.quote_original, q.quote_language, q.source_locator,
                   l.chunk_id AS linked_chunk_id, l.link_method, l.confidence,
                   ch.chunk_id, ch.doc_id AS chunk_document_id, ch.heading_path,
                   ch.chunk_text, ch.char_start, ch.char_end, ch.source_sha256
            FROM crumb_quotes AS q
            LEFT JOIN crumb_chunk_links AS l
              ON l.item_id = q.item_id AND l.quote_id = q.quote_id
            LEFT JOIN document_chunks AS ch ON ch.chunk_id = l.chunk_id
            WHERE q.item_id = ?
            ORDER BY q.quote_id, l.chunk_id
            """,
            (crumb_id,),
        ).fetchall()
        if not quote_rows:
            raise EvidenceIntegrityError(f"missing quote for crumb {crumb_id}")

        rows_by_quote: dict[str, list[sqlite3.Row]] = {}
        for row in quote_rows:
            rows_by_quote.setdefault(row["quote_id"], []).append(row)

        quote_entities: list[dict] = []
        chunk_entities: dict[str, dict] = {}
        for source_order, quote_id in enumerate(sorted(rows_by_quote), start=1):
            rows = rows_by_quote[quote_id]
            if len(rows) > 1:
                raise EvidenceIntegrityError(f"ambiguous chunk links for quote {quote_id}")
            row = rows[0]
            if row["linked_chunk_id"] is None:
                raise EvidenceIntegrityError(f"missing chunk link for quote {quote_id}")
            if row["chunk_id"] is None:
                raise EvidenceIntegrityError(
                    f"missing chunk {row['linked_chunk_id']} for quote {quote_id}"
                )
            if row["chunk_document_id"] != crumb["doc_id"]:
                raise EvidenceIntegrityError(
                    f"cross-document chunk link for quote {quote_id}"
                )
            if row["source_sha256"] != crumb["sha256"]:
                raise EvidenceIntegrityError(
                    f"source hash mismatch for chunk {row['chunk_id']}"
                )
            confidence = row["confidence"]
            if (not isinstance(confidence, (int, float)) or isinstance(confidence, bool)
                    or not 0 <= confidence <= 1):
                raise EvidenceIntegrityError(f"invalid confidence for quote {quote_id}")
            if not isinstance(row["link_method"], str) or not row["link_method"]:
                raise EvidenceIntegrityError(f"missing link method for quote {quote_id}")

            quote_entities.append({
                "quote_id": quote_id,
                "crumb_id": crumb["item_id"],
                "source_order": source_order,
                "text_original": row["quote_original"],
                "language": row["quote_language"],
                "source_locator": row["source_locator"],
                "chunk_id": row["chunk_id"],
                "link_method": row["link_method"],
                "confidence": confidence,
                "viewer_target": _target("quote", quote_id),
            })
            chunk_id = row["chunk_id"]
            chunk_entities[chunk_id] = {
                "chunk_id": chunk_id,
                "document_id": row["chunk_document_id"],
                "sequence": int(chunk_id.rsplit("-", 1)[1]),
                "heading_path": row["heading_path"],
                "text": row["chunk_text"],
                "char_start": row["char_start"],
                "char_end": row["char_end"],
                "source_sha256": row["source_sha256"],
                "viewer_target": _target("chunk", chunk_id),
            }

        evaluation_ids = [
            row[0] for row in connection.execute(
                "SELECT evaluation_id FROM evaluation_evidence WHERE item_id = ? "
                "ORDER BY evaluation_id",
                (crumb_id,),
            )
        ]
        quote_ids = [row["quote_id"] for row in quote_entities]
        chunk_ids = sorted(chunk_entities)
        return {
            "crumb": {
                "crumb_id": crumb["item_id"],
                "document_id": crumb["doc_id"],
                "criterion_id": crumb["criterion_id"],
                "document_side": crumb["document_side"],
                "statement": crumb["statement"],
                "item_type": crumb["item_type"],
                "quote_ids": quote_ids,
                "chunk_ids": chunk_ids,
                "evaluation_ids": evaluation_ids,
                "viewer_target": _target("crumb", crumb["item_id"]),
            },
            "document": {
                "document_id": crumb["doc_id"],
                "filename": crumb["filename"],
                "title": crumb["title"],
                "language": crumb["document_language"],
                "document_side": crumb["source_document_side"],
                "source_sha256": crumb["sha256"],
                "viewer_target": _target("document", crumb["doc_id"]),
            },
            "quotes": quote_entities,
            "chunks": [chunk_entities[chunk_id] for chunk_id in chunk_ids],
        }
