"""Create an immutable, hash-only snapshot of the approved incoming set."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
import sys

from project_paths import configure_standard_streams, local_path

ROOT = Path(__file__).resolve().parents[1]


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def create(snapshot_date: str, *, g1_ref: str, output_root: Path = ROOT / "out") -> Path:
    try:
        date.fromisoformat(snapshot_date)
    except ValueError as exc:
        raise ValueError("snapshot date must use YYYY-MM-DD") from exc
    if not g1_ref.strip():
        raise ValueError("g1_ref must be non-empty")
    incoming = local_path(ROOT / "incoming")
    if not incoming.is_dir():
        raise ValueError("incoming folder is missing")
    rows = []
    for path in sorted(incoming.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        rows.append({"relative_path": relative, "bytes": path.stat().st_size, "sha256": _hash(path)})
    if not rows:
        raise ValueError("incoming folder is empty")
    payload = {
        "schema_version": "1.0",
        "snapshot_date": snapshot_date,
        "g1_ref": g1_ref,
        "source_root": "incoming",
        "file_count": len(rows),
        "total_bytes": sum(row["bytes"] for row in rows),
        "files": rows,
    }
    destination = local_path(output_root) / snapshot_date / "source_snapshot.json"
    content = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.read_bytes() != content:
            raise ValueError(f"snapshot exists with different content: {destination}")
        return destination
    with destination.open("xb") as stream:
        stream.write(content)
    return destination


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, dest="snapshot_date")
    parser.add_argument("--g1-ref", required=True)
    args = parser.parse_args()
    try:
        path = create(args.snapshot_date, g1_ref=args.g1_ref)
        print(f"source_snapshot: PASS - {path}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"source_snapshot: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
