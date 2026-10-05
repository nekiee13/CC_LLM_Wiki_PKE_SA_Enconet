"""Apply owner-approved, quote-only repairs to active Ekonerg crumbs.

The migration preserves crumb IDs, criteria, links, and ratings.  It changes
only two stored quote strings to the exact text in the registered raw source.
It defaults to a dry run; ``--apply`` is required for the database update.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "nqa_audit.sqlite"
DEFAULT_MANIFEST = ROOT / "out" / "2026-10-05" / "traceability-repair" / "strict-quote-migration-20261006.json"
OWNER_REF = "REPAIR-DOC0019-GEN2-20261006-OWNER"
OWNER_REF_0011 = "REPAIR-DOC0011-GEN3-20261006-OWNER"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _replacement_quotes() -> dict[str, tuple[str, str, str]]:
    source_0019 = ROOT / "raw" / "PQ08.1-3_r2_Plan_vođenja_projekta.md"
    lines = source_0019.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("6. 6. Verifikacija ulaznih podataka"))
    end = next(i for i, line in enumerate(lines[start:], start) if line.startswith("16. 16. Predaja projekta"))
    exact_0019 = "\n".join(lines[start:end + 1])

    source_0011 = ROOT / "raw" / "PQ07.5-2_r8_Postupci_sustava_kvalitete,_sustava_za.md"
    text = source_0011.read_text(encoding="utf-8")
    start_text = "Opći postupak sustava kvalitete sadrži sljedeće točke:"
    start_at = text.index(start_text)
    end_at = text.index("\n\n3.3.3.", start_at)
    exact_0011 = text[start_at:end_at]

    return {
        "QUOTE-DOC-0019-0004-01": (
            "CRUMB-DOC-0019-APP_B_III-0003", exact_0019, OWNER_REF,
        ),
        "QUOTE-DOC-0011-0034-01": (
            "CRUMB-DOC-0011-APP_B_VI-0008", exact_0011, OWNER_REF_0011,
        ),
    }


def plan(db_path: Path) -> list[dict[str, str]]:
    repairs = _replacement_quotes()
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        result: list[dict[str, str]] = []
        for quote_id, (item_id, replacement, decision_ref) in repairs.items():
            row = conn.execute(
                "SELECT q.quote_original, c.doc_id, r.run_id, r.is_active "
                "FROM crumb_quotes q JOIN crumbs c ON c.item_id=q.item_id "
                "JOIN sieve_runs r ON r.run_id=c.sieve_run_id "
                "WHERE q.quote_id=? AND q.item_id=?",
                (quote_id, item_id),
            ).fetchone()
            if row is None:
                raise ValueError(f"target quote is missing: {quote_id}")
            if not row["is_active"]:
                raise ValueError(f"target quote is not active: {quote_id}")
            result.append({
                "quote_id": quote_id,
                "item_id": item_id,
                "doc_id": row["doc_id"],
                "run_id": row["run_id"],
                "decision_ref": decision_ref,
                "before_sha256": hashlib.sha256(row["quote_original"].encode("utf-8")).hexdigest(),
                "after_sha256": hashlib.sha256(replacement.encode("utf-8")).hexdigest(),
                "before_length": str(len(row["quote_original"])),
                "after_length": str(len(replacement)),
                "replacement": replacement,
            })
    return result


def apply(db_path: Path, manifest_path: Path) -> list[dict[str, str]]:
    db_path = db_path.resolve()
    manifest_path = manifest_path.resolve()
    entries = plan(db_path)
    before_db = _sha(db_path)
    with sqlite3.connect(db_path) as conn:
        for entry in entries:
            conn.execute(
                "UPDATE crumb_quotes SET quote_original=? WHERE item_id=? AND quote_id=?",
                (entry["replacement"], entry["item_id"], entry["quote_id"]),
            )
        conn.commit()
    after_db = _sha(db_path)
    for entry in entries:
        entry.pop("replacement", None)
    manifest = {
        "schema_version": "1.0",
        "migration": "strict-quote-repair",
        "owner_decision": "Owner approved use of corrected source copy on 2026-10-06",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "database": str(db_path.relative_to(ROOT)),
        "database_sha256_before": before_db,
        "database_sha256_after": after_db,
        "entries": entries,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    entries = plan(args.db)
    if not args.apply:
        print(json.dumps({"mode": "dry-run", "entries": entries}, ensure_ascii=False, indent=2))
        return 0
    apply(args.db, args.manifest)
    print(f"apply_strict_quote_repairs: PASS - {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
