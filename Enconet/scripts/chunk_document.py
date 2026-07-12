#!/usr/bin/env python3
"""Split one registered derived document into reviewable level-1/2 chunks."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import db_util
from source_registry import ENCONET

DERIVED = ENCONET / "derived"
HEADING = re.compile(r"(?m)^(?P<number>\d+(?:\.\d+)*)(?:\.(?=\s|$)|(?=\s))[^\r\n]*$")


@dataclass(frozen=True)
class Chunk:
    heading_path: str
    text: str
    char_start: int
    char_end: int


def _heading_path(number: str) -> str:
    parts = number.split(".")
    return parts[0] if len(parts) == 1 else f"{parts[0]} > {parts[0]}.{parts[1]}"


def parse_chunks(text: str, *, min_chars: int = 1,
                 max_chars: int = 50_000) -> tuple[list[Chunk], list[str]]:
    if min_chars < 1 or max_chars < min_chars:
        raise ValueError("chunk bounds require 1 <= min_chars <= max_chars")
    if not text.strip():
        raise ValueError("empty document cannot be chunked")
    boundaries = [m for m in HEADING.finditer(text) if len(m.group("number").split(".")) <= 2]
    warnings: list[str] = []
    if not boundaries:
        chunks = [Chunk("whole-document", text, 0, len(text))]
        warnings.append("no level-1/2 numeric headings; used whole-document fallback")
    else:
        chunks = []
        seen: set[str] = set()
        for index, match in enumerate(boundaries):
            path = _heading_path(match.group("number"))
            if path in seen:
                raise ValueError(f"duplicate heading path: {path}")
            seen.add(path)
            start = 0 if index == 0 else match.start()
            end = boundaries[index + 1].start() if index + 1 < len(boundaries) else len(text)
            chunk_text = text[start:end]
            if not chunk_text.strip():
                raise ValueError(f"empty chunk at heading path: {path}")
            chunks.append(Chunk(path, chunk_text, start, end))
    for chunk in chunks:
        size = len(chunk.text)
        if size < min_chars:
            warnings.append(f"{chunk.heading_path}: {size} chars below minimum {min_chars}")
        if size > max_chars:
            warnings.append(f"{chunk.heading_path}: {size} chars exceeds maximum {max_chars}; manual split required")
    return chunks, warnings


def write_chunks(doc_id: str, *, db_path: Path, derived_root: Path = DERIVED,
                 min_chars: int = 1, max_chars: int = 50_000) -> tuple[int, list[str]]:
    with db_util.connect(db_path) as conn:
        document = db_util.lookup(conn, "documents", "doc_id", doc_id)
        if document is None:
            raise ValueError(f"unknown document: {doc_id}")
        source = derived_root / f"{doc_id}.txt"
        if not source.is_file():
            raise FileNotFoundError(f"derived text missing: {source}")
        text = source.read_text(encoding="utf-8")
        chunks, warnings = parse_chunks(text, min_chars=min_chars, max_chars=max_chars)
        try:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("DELETE FROM document_chunks WHERE doc_id = ?", (doc_id,))
            for index, chunk in enumerate(chunks, 1):
                db_util.insert(conn, "document_chunks", {
                    "chunk_id": f"CHUNK-{doc_id}-{index:04d}", "doc_id": doc_id,
                    "heading_path": chunk.heading_path, "chunk_text": chunk.text,
                    "char_start": chunk.char_start, "char_end": chunk.char_end,
                    "source_sha256": document["sha256"],
                })
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    return len(chunks), warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doc_id")
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--min-chars", type=int, default=1)
    parser.add_argument("--max-chars", type=int, default=50_000)
    args = parser.parse_args()
    try:
        count, warnings = write_chunks(args.doc_id, db_path=args.db,
                                       min_chars=args.min_chars, max_chars=args.max_chars)
        for warning in warnings:
            print(f"chunk_document: WARNING - {warning}")
        print(f"chunk_document: PASS - chunks created={count}; warnings={len(warnings)}; rejections=0")
        return 0
    except Exception as exc:
        print(f"chunk_document: FAIL - chunks created=0; warnings=0; rejections=1; {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
