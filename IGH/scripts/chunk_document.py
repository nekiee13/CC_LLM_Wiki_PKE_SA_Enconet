#!/usr/bin/env python3
"""Preview or first-write chunks for one registered local derived document."""
from __future__ import annotations

import argparse
from contextlib import closing
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys

import db_util
from project_paths import configure_standard_streams, local_path

ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"(?m)^(?P<number>\d+(?:\.\d+)*)(?:\.(?=\s|$)|(?=\s))[^\r\n]*$")
MARKDOWN = re.compile(r"(?m)^(?P<marks>#{1,2})[ \t]+(?P<title>.*?\S)[ \t]*#*[ \t]*$")


@dataclass(frozen=True)
class Chunk:
    heading_path: str
    chunk_text: str
    char_start: int
    char_end: int


def parse_chunks(text: str, *, min_chars: int = 1, max_chars: int = 50_000) -> list[Chunk]:
    if min_chars < 1 or max_chars < min_chars:
        raise ValueError("chunk bounds require 1 <= min_chars <= max_chars")
    if not text.strip():
        raise ValueError("empty derived document cannot be chunked")
    boundaries: list[tuple[int, str]] = []
    markdown = list(MARKDOWN.finditer(text))
    if markdown:
        parent: str | None = None
        for match in markdown:
            line = text.count("\n", 0, match.start()) + 1
            locator = f"{match.group('title').strip()} [line {line}]"
            if len(match.group("marks")) == 1:
                parent = locator
                path = locator
            else:
                path = f"{parent} > {locator}" if parent else locator
            boundaries.append((match.start(), path))
    else:
        for match in HEADING.finditer(text):
            parts = match.group("number").split(".")
            if len(parts) > 2:
                continue
            path = parts[0] if len(parts) == 1 else f"{parts[0]} > {parts[0]}.{parts[1]}"
            boundaries.append((match.start(), path))
    if not boundaries:
        raise ValueError("no level-1/2 headings; manual chunk plan required")
    if len(boundaries) > 9999:
        raise ValueError("more than 9999 chunks; manual split required")
    chunks: list[Chunk] = []
    seen: set[str] = set()
    for index, (start, path) in enumerate(boundaries):
        if path in seen:
            raise ValueError(f"duplicate heading path: {path}")
        seen.add(path)
        start = 0 if index == 0 else start
        end = boundaries[index + 1][0] if index + 1 < len(boundaries) else len(text)
        value = text[start:end]
        if not value.strip() or not min_chars <= len(value) <= max_chars:
            raise ValueError(f"chunk {path} is empty or outside character bounds")
        chunks.append(Chunk(path, value, start, end))
    return chunks


def _plan(db: Path, doc_id: str, min_chars: int, max_chars: int) -> tuple[dict, list[Chunk], Path]:
    if db_util.id_patterns()["doc_id"].fullmatch(doc_id) is None:
        raise ValueError(f"invalid document ID: {doc_id}")
    database = local_path(db)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    source = local_path(ROOT / "derived" / f"{doc_id}.txt")
    if not source.is_file():
        raise ValueError(f"local derived text is missing: {source}")
    text = source.read_text(encoding="utf-8")
    chunks = parse_chunks(text, min_chars=min_chars, max_chars=max_chars)
    artifact = local_path(ROOT / "derived" / "chunks" / f"{doc_id}.json")
    if artifact.exists():
        raise ValueError("chunk artifact already exists; prior evidence is immutable")
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        document = db_util.lookup(conn, "documents", "doc_id", doc_id)
        if document is None:
            raise ValueError(f"document is not registered: {doc_id}")
        if conn.execute("SELECT 1 FROM document_chunks WHERE doc_id=?", (doc_id,)).fetchone():
            raise ValueError("document already has chunks; prior evidence is immutable")
    plan = {"doc_id": doc_id, "chunk_count": len(chunks),
            "derived_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "registered_source_sha256": document["sha256"], "artifact": str(artifact),
            "mode": "preview", "status": "candidate-chunks-not-human-approved"}
    return plan, chunks, source


def chunk_document(db: Path, doc_id: str, *, min_chars: int = 1,
                   max_chars: int = 50_000, apply: bool = False) -> dict:
    plan, chunks, source = _plan(db, doc_id, min_chars, max_chars)
    if not apply:
        return plan
    database = local_path(db)
    artifact = local_path(plan["artifact"])
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact_created = False
    with closing(db_util.connect(database)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            document = db_util.lookup(conn, "documents", "doc_id", doc_id)
            if document is None or document["sha256"] != plan["registered_source_sha256"]:
                raise ValueError("registered document changed since preview")
            if conn.execute("SELECT 1 FROM document_chunks WHERE doc_id=?", (doc_id,)).fetchone():
                raise ValueError("document already has chunks; prior evidence is immutable")
            if hashlib.sha256(source.read_text(encoding="utf-8").encode("utf-8")).hexdigest() != plan["derived_text_sha256"]:
                raise ValueError("derived text changed since preview")
            rows = [{"chunk_id": f"CHUNK-{doc_id}-{index:04d}", "doc_id": doc_id,
                     "heading_path": chunk.heading_path, "chunk_text": chunk.chunk_text,
                     "char_start": chunk.char_start, "char_end": chunk.char_end,
                     "source_sha256": document["sha256"]}
                    for index, chunk in enumerate(chunks, 1)]
            with artifact.open("x", encoding="utf-8", newline="\n") as handle:
                artifact_created = True
                json.dump({"schema_version": "1.0", **plan, "mode": "apply",
                           "chunks": rows},
                          handle, ensure_ascii=False, sort_keys=True, indent=2)
                handle.write("\n")
            for row in rows:
                db_util.insert(conn, "document_chunks", row)
            conn.commit()
        except Exception:
            conn.rollback()
            if artifact_created:
                artifact.unlink()
            raise
    plan["mode"] = "apply"
    return plan


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doc_id")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--min-chars", type=int, default=1)
    parser.add_argument("--max-chars", type=int, default=50_000)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(chunk_document(args.db, args.doc_id, min_chars=args.min_chars,
                                        max_chars=args.max_chars, apply=args.apply),
                         ensure_ascii=False, sort_keys=True))
        return 0
    except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"chunk_document: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
