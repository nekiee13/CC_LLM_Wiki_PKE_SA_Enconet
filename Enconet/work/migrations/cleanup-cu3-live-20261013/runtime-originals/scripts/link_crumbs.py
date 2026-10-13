#!/usr/bin/env python3
"""Link every crumb quote to a containing chunk in the same document."""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import db_util

ENCONET = Path(__file__).resolve().parents[1]
CANDIDATES = ENCONET / "manifests" / "link_exception_candidates.csv"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def link(db_path: Path, *, candidates_path: Path = CANDIDATES) -> tuple[int, list[dict[str, str]]]:
    unmatched: list[dict[str, str]] = []
    linked = 0
    with db_util.connect(db_path) as conn:
        quotes = conn.execute(
            "SELECT q.*, c.doc_id FROM crumb_quotes q JOIN crumbs c ON c.item_id=q.item_id ORDER BY q.quote_id"
        ).fetchall()
        conn.execute("DELETE FROM crumb_chunk_links")
        for quote in quotes:
            chunks = conn.execute("SELECT * FROM document_chunks WHERE doc_id=? ORDER BY chunk_id", (quote["doc_id"],)).fetchall()
            exact = [c for c in chunks if quote["quote_original"] in c["chunk_text"]]
            matches = exact or [c for c in chunks if normalize(quote["quote_original"]) in normalize(c["chunk_text"])]
            if not matches:
                unmatched.append({"crumb_id": quote["item_id"], "quote_id": quote["quote_id"],
                                  "doc_id": quote["doc_id"], "reason": "quote not found in same-document chunks"})
                continue
            method = "EXACT" if exact else "NORMALIZED"
            for chunk in matches:
                db_util.insert(conn, "crumb_chunk_links", {"item_id": quote["item_id"],
                    "quote_id": quote["quote_id"], "chunk_id": chunk["chunk_id"],
                    "link_method": method, "confidence": 1.0 if exact else 0.95})
                linked += 1
    candidates_path.parent.mkdir(parents=True, exist_ok=True)
    with candidates_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["crumb_id", "quote_id", "doc_id", "reason"])
        writer.writeheader(); writer.writerows(unmatched)
    return linked, unmatched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--candidates", type=Path, default=CANDIDATES)
    parser.add_argument("--metrics-root", type=Path, default=ENCONET / "sieving" / "runs")
    args = parser.parse_args()
    try:
        count, unmatched = link(args.db, candidates_path=args.candidates)
        import sieve_metrics
        with db_util.connect(args.db) as conn:
            run_ids = [row[0] for row in conn.execute("SELECT run_id FROM sieve_runs WHERE completed_at IS NOT NULL")]
        for run_id in run_ids:
            sieve_metrics.generate(args.db, run_id, args.metrics_root / run_id)
        print(f"link_crumbs: PASS - links={count}; exception_candidates={len(unmatched)}; metrics={len(run_ids)} run(s)")
        return 0
    except Exception as exc:
        print(f"link_crumbs: FAIL - {exc}", file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
