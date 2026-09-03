#!/usr/bin/env python3
"""Read-only, fail-closed SQLite evidence projection for one active crumb."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Collection, Iterator, TypedDict

import evidence_navigation


ENCONET = Path(__file__).resolve().parents[1]
MAX_CONTEXT_RADIUS = 2


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


def resolve_crumb(
    db_path: Path | str, crumb_id: str, *, context_radius: int = 1
) -> ResolvedCrumb | None:
    """Resolve one active crumb with at most two adjacent chunks on each side."""
    if (not isinstance(context_radius, int) or isinstance(context_radius, bool)
            or not 0 <= context_radius <= MAX_CONTEXT_RADIUS):
        raise ValueError(
            f"context_radius must be an integer from 0 to {MAX_CONTEXT_RADIUS}"
        )
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
        linked_chunk_ids: set[str] = set()
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
            linked_chunk_ids.add(row["chunk_id"])

        ordered_chunks = connection.execute(
            "SELECT * FROM document_chunks WHERE doc_id = ? "
            "ORDER BY char_start, char_end, chunk_id",
            (crumb["doc_id"],),
        ).fetchall()
        position_by_id = {
            row["chunk_id"]: position for position, row in enumerate(ordered_chunks)
        }
        missing_positions = linked_chunk_ids - set(position_by_id)
        if missing_positions:
            raise EvidenceIntegrityError(
                f"missing chunk {sorted(missing_positions)[0]} for crumb {crumb_id}"
            )
        included_positions: set[int] = set()
        for chunk_id in linked_chunk_ids:
            position = position_by_id[chunk_id]
            start = max(0, position - context_radius)
            end = min(len(ordered_chunks), position + context_radius + 1)
            included_positions.update(range(start, end))

        chunk_entities: dict[str, dict] = {}
        projected_chunk_ids: list[str] = []
        for position in sorted(included_positions):
            row = ordered_chunks[position]
            chunk_id = row["chunk_id"]
            if row["source_sha256"] != crumb["sha256"]:
                raise EvidenceIntegrityError(
                    f"source hash mismatch for context chunk {chunk_id}"
                )
            previous_position = position - 1
            next_position = position + 1
            previous_id = (
                ordered_chunks[previous_position]["chunk_id"]
                if previous_position in included_positions else None
            )
            next_id = (
                ordered_chunks[next_position]["chunk_id"]
                if next_position in included_positions else None
            )
            chunk_entities[chunk_id] = {
                "chunk_id": chunk_id,
                "document_id": row["doc_id"],
                "sequence": int(chunk_id.rsplit("-", 1)[1]),
                "heading_path": row["heading_path"],
                "text": row["chunk_text"],
                "char_start": row["char_start"],
                "char_end": row["char_end"],
                "source_sha256": row["source_sha256"],
                "previous_chunk_id": previous_id,
                "next_chunk_id": next_id,
                "context_truncated_before": position > 0 and previous_id is None,
                "context_truncated_after": (
                    position < len(ordered_chunks) - 1 and next_id is None
                ),
                "viewer_target": _target("chunk", chunk_id),
            }
            projected_chunk_ids.append(chunk_id)

        evaluation_ids = [
            row[0] for row in connection.execute(
                "SELECT evaluation_id FROM evaluation_evidence WHERE item_id = ? "
                "ORDER BY evaluation_id",
                (crumb_id,),
            )
        ]
        quote_ids = [row["quote_id"] for row in quote_entities]
        chunk_ids = sorted(linked_chunk_ids)
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
            "chunks": [chunk_entities[chunk_id] for chunk_id in projected_chunk_ids],
        }


PRESENTATIONS = {
    "crumb": "evidence-detail",
    "document": "document-metadata",
    "chunk": "chunk-detail",
    "quote": "quote-detail",
    "evaluation": "evaluation-detail",
    "gap": "gap-detail",
    "finding": "finding-detail",
    "action": "action-detail",
    "source": "package-metadata",
}


def _reference(entity_type: str, entity_id: str) -> str:
    return f"{entity_type}:{entity_id}"


def _entity(entity_type: str, entity_id: str, data: dict, relationships: dict) -> dict:
    """Create a non-recursive registry record whose relationships are references only."""
    return {
        "reference": _reference(entity_type, entity_id),
        "entity_type": entity_type,
        "presentation": PRESENTATIONS[entity_type],
        "viewer_target": _target(entity_type, entity_id),
        "data": data,
        "relationships": relationships,
    }


def _where_in(values: list[str]) -> str:
    return ",".join("?" for _value in values)


def _package_entity(package_path: Path | str, run_id: str) -> dict:
    path = Path(package_path).resolve()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        package_run_id = payload["run"]["run_id"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise EvidenceIntegrityError(f"invalid evaluation package: {path}") from exc
    if package_run_id != run_id:
        raise EvidenceIntegrityError(
            f"package run mismatch: expected {run_id}, found {package_run_id}"
        )
    try:
        display_path = path.relative_to(ENCONET).as_posix()
    except ValueError:
        display_path = path.name
    data = {
        "run_id": run_id,
        "path": display_path,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "schema_version": payload.get("schema_version"),
        "supplier": payload.get("run", {}).get("supplier"),
        "deliverable_language": payload.get("run", {}).get("deliverable_language"),
    }
    return _entity(
        "source", "package", data, {"evaluation_run": run_id}
    )


def build_entity_registry(
    db_path: Path | str,
    run_id: str,
    *,
    package_path: Path | str | None = None,
    included_run_ids: Collection[str] = (),
) -> dict:
    """Build a deterministic reference registry limited to explicitly selected runs."""
    run_ids = [run_id] + sorted(set(included_run_ids) - {run_id})
    placeholders = _where_in(run_ids)
    with _connect_readonly(db_path) as connection:
        stored_runs = {
            row["run_id"]: dict(row)
            for row in connection.execute(
                f"SELECT * FROM evaluation_runs WHERE run_id IN ({placeholders}) ORDER BY run_id",
                run_ids,
            )
        }
        missing_runs = [value for value in run_ids if value not in stored_runs]
        if missing_runs:
            raise EvidenceIntegrityError(f"unknown evaluation run: {missing_runs[0]}")

        evaluations = [dict(row) for row in connection.execute(
            f"SELECT * FROM criterion_evaluations WHERE evaluation_run_id IN ({placeholders}) "
            "ORDER BY evaluation_run_id, evaluation_id",
            run_ids,
        )]
        evidence_links = [dict(row) for row in connection.execute(
            f"SELECT ee.evaluation_id, ee.item_id FROM evaluation_evidence AS ee "
            "JOIN criterion_evaluations AS e ON e.evaluation_id=ee.evaluation_id "
            f"WHERE e.evaluation_run_id IN ({placeholders}) "
            "ORDER BY ee.evaluation_id, ee.item_id",
            run_ids,
        )]
        gaps = [dict(row) for row in connection.execute(
            "SELECT g.*, e.evaluation_run_id, e.criterion_id FROM gaps AS g "
            "JOIN criterion_evaluations AS e ON e.evaluation_id=g.evaluation_id "
            f"WHERE e.evaluation_run_id IN ({placeholders}) ORDER BY g.gap_id",
            run_ids,
        )]
        findings = [dict(row) for row in connection.execute(
            f"SELECT * FROM findings WHERE evaluation_run_id IN ({placeholders}) "
            "ORDER BY finding_id",
            run_ids,
        )]
        actions = [dict(row) for row in connection.execute(
            f"SELECT * FROM auditor_actions WHERE evaluation_run_id IN ({placeholders}) "
            "ORDER BY action_id",
            run_ids,
        )]
        scope_document_ids = {
            row[0] for row in connection.execute(
                f"SELECT DISTINCT scope_source_doc_id FROM criterion_applicability "
                f"WHERE evaluation_run_id IN ({placeholders}) ORDER BY scope_source_doc_id",
                run_ids,
            )
        }

    evaluation_ids = {row["evaluation_id"] for row in evaluations}
    gap_runs = {row["gap_id"]: row["evaluation_run_id"] for row in gaps}
    finding_runs = {row["finding_id"]: row["evaluation_run_id"] for row in findings}
    for row in findings:
        if row["gap_id"] and gap_runs.get(row["gap_id"]) != row["evaluation_run_id"]:
            raise EvidenceIntegrityError(
                f"cross-run relationship: finding {row['finding_id']} -> gap {row['gap_id']}"
            )
    for row in actions:
        if (row["finding_id"]
                and finding_runs.get(row["finding_id"]) != row["evaluation_run_id"]):
            raise EvidenceIntegrityError(
                f"cross-run relationship: action {row['action_id']} -> "
                f"finding {row['finding_id']}"
            )
        if row["gap_id"] and gap_runs.get(row["gap_id"]) != row["evaluation_run_id"]:
            raise EvidenceIntegrityError(
                f"cross-run relationship: action {row['action_id']} -> gap {row['gap_id']}"
            )
    evidence_by_evaluation: dict[str, list[str]] = {}
    for link in evidence_links:
        evidence_by_evaluation.setdefault(link["evaluation_id"], []).append(link["item_id"])
    required_crumb_ids = {link["item_id"] for link in evidence_links}
    required_crumb_ids.update(row["evidence_item_id"] for row in gaps if row["evidence_item_id"])
    required_crumb_ids.update(
        row["evidence_item_id"] for row in findings if row["evidence_item_id"]
    )

    crumb_projections: dict[str, ResolvedCrumb] = {}
    for crumb_id in sorted(required_crumb_ids):
        projection = resolve_crumb(db_path, crumb_id)
        if projection is None:
            raise EvidenceIntegrityError(f"inactive or missing referenced crumb: {crumb_id}")
        projection["crumb"]["evaluation_ids"] = sorted(
            set(projection["crumb"]["evaluation_ids"]) & evaluation_ids
        )
        crumb_projections[crumb_id] = projection

    document_ids = set(scope_document_ids)
    document_ids.update(
        projection["document"]["document_id"] for projection in crumb_projections.values()
    )
    documents: dict[str, dict] = {
        projection["document"]["document_id"]: projection["document"]
        for projection in crumb_projections.values()
    }
    if document_ids:
        ordered_doc_ids = sorted(document_ids)
        with _connect_readonly(db_path) as connection:
            for row in connection.execute(
                f"SELECT * FROM documents WHERE doc_id IN ({_where_in(ordered_doc_ids)}) "
                "ORDER BY doc_id",
                ordered_doc_ids,
            ):
                documents[row["doc_id"]] = {
                    "document_id": row["doc_id"],
                    "filename": row["filename"],
                    "title": row["title"],
                    "language": row["language"],
                    "document_side": row["document_side"],
                    "source_sha256": row["sha256"],
                    "viewer_target": _target("document", row["doc_id"]),
                }
        absent_documents = document_ids - set(documents)
        if absent_documents:
            raise EvidenceIntegrityError(
                f"missing document: {sorted(absent_documents)[0]}"
            )

    entities: dict[str, dict] = {}

    def add(entity: dict) -> None:
        reference = entity["reference"]
        if reference in entities:
            raise EvidenceIntegrityError(f"duplicate entity reference: {reference}")
        entities[reference] = entity

    for doc_id in sorted(documents):
        related_crumbs = sorted(
            _reference("crumb", crumb_id)
            for crumb_id, projection in crumb_projections.items()
            if projection["crumb"]["document_id"] == doc_id
        )
        add(_entity("document", doc_id, documents[doc_id], {"crumbs": related_crumbs}))

    merged_chunks: dict[str, dict] = {}
    context_for_chunks: dict[str, set[str]] = {}
    for crumb_id, projection in sorted(crumb_projections.items()):
        for chunk in projection["chunks"]:
            chunk_id = chunk["chunk_id"]
            context_for_chunks.setdefault(chunk_id, set()).add(crumb_id)
            existing = merged_chunks.get(chunk_id)
            if existing is None:
                merged_chunks[chunk_id] = dict(chunk)
                continue
            stable_fields = (
                "document_id", "sequence", "heading_path", "text", "char_start",
                "char_end", "source_sha256", "viewer_target",
            )
            if any(existing[field] != chunk[field] for field in stable_fields):
                raise EvidenceIntegrityError(f"conflicting context chunk: {chunk_id}")
            for pointer in ("previous_chunk_id", "next_chunk_id"):
                if existing[pointer] is None:
                    existing[pointer] = chunk[pointer]
                elif chunk[pointer] is not None and existing[pointer] != chunk[pointer]:
                    raise EvidenceIntegrityError(
                        f"conflicting {pointer} for context chunk: {chunk_id}"
                    )
            existing["context_truncated_before"] = (
                existing["context_truncated_before"]
                or chunk["context_truncated_before"]
            )
            existing["context_truncated_after"] = (
                existing["context_truncated_after"]
                or chunk["context_truncated_after"]
            )

    # A chunk may appear at the truncated edge of one crumb window and in the middle of another.
    # Merge the known edge before deriving final truncation flags.
    for chunk_id, chunk in sorted(merged_chunks.items()):
        previous = chunk["previous_chunk_id"]
        following = chunk["next_chunk_id"]
        if previous is not None:
            neighbor = merged_chunks.get(previous)
            if neighbor is None:
                raise EvidenceIntegrityError(f"missing merged previous chunk: {previous}")
            if neighbor["next_chunk_id"] not in {None, chunk_id}:
                raise EvidenceIntegrityError(f"conflicting merged chunk edge: {previous}")
            neighbor["next_chunk_id"] = chunk_id
        if following is not None:
            neighbor = merged_chunks.get(following)
            if neighbor is None:
                raise EvidenceIntegrityError(f"missing merged next chunk: {following}")
            if neighbor["previous_chunk_id"] not in {None, chunk_id}:
                raise EvidenceIntegrityError(f"conflicting merged chunk edge: {following}")
            neighbor["previous_chunk_id"] = chunk_id
    for chunk in merged_chunks.values():
        if chunk["previous_chunk_id"] is not None:
            chunk["context_truncated_before"] = False
        if chunk["next_chunk_id"] is not None:
            chunk["context_truncated_after"] = False

    for crumb_id, projection in sorted(crumb_projections.items()):
        crumb_data = projection["crumb"]
        add(_entity("crumb", crumb_id, crumb_data, {
            "document": _reference("document", crumb_data["document_id"]),
            "quotes": [_reference("quote", value) for value in crumb_data["quote_ids"]],
            "chunks": [_reference("chunk", value) for value in crumb_data["chunk_ids"]],
            "evaluations": [
                _reference("evaluation", value) for value in crumb_data["evaluation_ids"]
            ],
        }))
        for quote in projection["quotes"]:
            reference = _reference("quote", quote["quote_id"])
            if reference not in entities:
                add(_entity("quote", quote["quote_id"], quote, {
                    "crumb": _reference("crumb", crumb_id),
                    "chunk": _reference("chunk", quote["chunk_id"]),
                    "document": _reference("document", crumb_data["document_id"]),
                }))

    for chunk_id, chunk in sorted(
        merged_chunks.items(),
        key=lambda item: (
            item[1]["document_id"], item[1]["char_start"], item[1]["char_end"], item[0]
        ),
    ):
        direct_crumbs = sorted(
            _reference("crumb", other_id)
            for other_id, other in crumb_projections.items()
            if chunk_id in other["crumb"]["chunk_ids"]
        )
        context_crumbs = sorted(
            _reference("crumb", value) for value in context_for_chunks[chunk_id]
        )
        add(_entity("chunk", chunk_id, chunk, {
            "document": _reference("document", chunk["document_id"]),
            "crumbs": direct_crumbs,
            "context_for_crumbs": context_crumbs,
        }))

    gaps_by_evaluation: dict[str, list[str]] = {}
    for row in gaps:
        gaps_by_evaluation.setdefault(row["evaluation_id"], []).append(row["gap_id"])
    findings_by_key: dict[tuple[str, str], list[str]] = {}
    for row in findings:
        findings_by_key.setdefault(
            (row["evaluation_run_id"], row["criterion_id"]), []
        ).append(row["finding_id"])
    evaluation_by_key = {
        (row["evaluation_run_id"], row["criterion_id"]): row["evaluation_id"]
        for row in evaluations
    }
    for row in evaluations:
        evaluation_id = row["evaluation_id"]
        crumb_ids = sorted(set(evidence_by_evaluation.get(evaluation_id, [])))
        gap_ids = sorted(set(gaps_by_evaluation.get(evaluation_id, [])))
        finding_ids = sorted(set(findings_by_key.get(
            (row["evaluation_run_id"], row["criterion_id"]), []
        )))
        data = {
            "evaluation_id": evaluation_id,
            "criterion_id": row["criterion_id"],
            "evidence_crumb_ids": crumb_ids,
            "gap_ids": gap_ids,
            "viewer_target": _target("evaluation", evaluation_id),
        }
        add(_entity("evaluation", evaluation_id, data, {
            "evidence_crumbs": [_reference("crumb", value) for value in crumb_ids],
            "gaps": [_reference("gap", value) for value in gap_ids],
            "findings": [_reference("finding", value) for value in finding_ids],
        }))

    actions_by_finding: dict[str, list[str]] = {}
    actions_by_gap: dict[str, list[str]] = {}
    for row in actions:
        if row["finding_id"]:
            actions_by_finding.setdefault(row["finding_id"], []).append(row["action_id"])
        if row["gap_id"]:
            actions_by_gap.setdefault(row["gap_id"], []).append(row["action_id"])
    findings_by_gap: dict[str, list[str]] = {}
    for row in findings:
        if row["gap_id"]:
            findings_by_gap.setdefault(row["gap_id"], []).append(row["finding_id"])

    for row in gaps:
        gap_id = row["gap_id"]
        finding_ids = sorted(set(findings_by_gap.get(gap_id, [])))
        action_ids = sorted(set(actions_by_gap.get(gap_id, [])))
        data = {
            "gap_id": gap_id,
            "evaluation_id": row["evaluation_id"],
            "description": row["description"],
            "missing_evidence_ref": row["missing_evidence_ref"],
            "evidence_crumb_id": row["evidence_item_id"],
            "finding_ids": finding_ids,
            "action_ids": action_ids,
            "viewer_target": _target("gap", gap_id),
        }
        add(_entity("gap", gap_id, data, {
            "self": None,
            "evaluation": _reference("evaluation", row["evaluation_id"]),
            "evidence_crumb": (
                _reference("crumb", row["evidence_item_id"])
                if row["evidence_item_id"] else None
            ),
            "findings": [_reference("finding", value) for value in finding_ids],
            "actions": [_reference("action", value) for value in action_ids],
        }))

    for row in findings:
        finding_id = row["finding_id"]
        evaluation_id = evaluation_by_key.get(
            (row["evaluation_run_id"], row["criterion_id"])
        )
        if evaluation_id is None:
            raise EvidenceIntegrityError(
                f"finding without same-run evaluation: {finding_id}"
            )
        action_ids = sorted(set(actions_by_finding.get(finding_id, [])))
        data = {
            "finding_id": finding_id,
            "evaluation_id": evaluation_id,
            "title": row["title"],
            "body": row["body"],
            "gap_id": row["gap_id"],
            "evidence_crumb_id": row["evidence_item_id"],
            "action_ids": action_ids,
            "viewer_target": _target("finding", finding_id),
        }
        add(_entity("finding", finding_id, data, {
            "evaluation": _reference("evaluation", evaluation_id),
            "gap": _reference("gap", row["gap_id"]) if row["gap_id"] else None,
            "evidence_crumb": (
                _reference("crumb", row["evidence_item_id"])
                if row["evidence_item_id"] else None
            ),
            "actions": [_reference("action", value) for value in action_ids],
        }))

    for row in actions:
        action_id = row["action_id"]
        data = {
            "action_id": action_id,
            "description": row["description"],
            "priority": row["priority"],
            "finding_id": row["finding_id"],
            "gap_id": row["gap_id"],
            "viewer_target": _target("action", action_id),
        }
        add(_entity("action", action_id, data, {
            "finding": (
                _reference("finding", row["finding_id"]) if row["finding_id"] else None
            ),
            "gap": _reference("gap", row["gap_id"]) if row["gap_id"] else None,
        }))

    if package_path is not None:
        add(_package_entity(package_path, run_id))

    return {
        "run_id": run_id,
        "included_run_ids": run_ids,
        "entities": {key: entities[key] for key in sorted(entities)},
    }


def resolve_reference(registry: dict, reference: str) -> dict | None:
    """Resolve an exact report reference without interpreting paths, URLs, or SQL."""
    if not isinstance(reference, str):
        return None
    return registry.get("entities", {}).get(reference)
