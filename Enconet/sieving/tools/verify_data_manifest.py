"""Verify (or regenerate) the sieving/DATA SHA-256 checksum manifest (ADR-0002, C0.2).

Default mode verifies the on-disk corpus against DATA_MANIFEST.json and exits
non-zero on any missing, foreign, or modified file. `--write` regenerates the
manifest (requires explicit intent; the manifest is a tracked controlled record).

Paths are resolved from this script's location, never from the CWD.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SIEVING_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = SIEVING_ROOT / "DATA"
MANIFEST_PATH = SIEVING_ROOT / "DATA_MANIFEST.json"
SOURCE_NOTE = (
    "Supplier-derived crumb JSON corpus (ADR-0002): tracked by checksum only, "
    "never committed to git."
)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_corpus() -> dict[str, dict]:
    if not DATA_DIR.is_dir():
        sys.exit(f"ERROR: DATA directory not found: {DATA_DIR}")
    files = {}
    for p in sorted(DATA_DIR.rglob("*")):
        if p.is_file():
            rel = p.relative_to(DATA_DIR).as_posix()
            files[rel] = {"size": p.stat().st_size, "sha256": sha256_of(p)}
    return files


def write_manifest() -> None:
    files = scan_corpus()
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_dir": "DATA",
        "source_note": SOURCE_NOTE,
        "file_count": len(files),
        "files": files,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {MANIFEST_PATH.name}: {len(files)} files.")


def verify() -> int:
    if not MANIFEST_PATH.is_file():
        print(f"FAIL: manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected = manifest["files"]
    actual = scan_corpus()

    missing = sorted(set(expected) - set(actual))
    foreign = sorted(set(actual) - set(expected))
    modified = sorted(
        rel
        for rel in set(expected) & set(actual)
        if expected[rel]["sha256"] != actual[rel]["sha256"]
        or expected[rel]["size"] != actual[rel]["size"]
    )

    for rel in missing:
        print(f"MISSING : {rel}", file=sys.stderr)
    for rel in foreign:
        print(f"FOREIGN : {rel}", file=sys.stderr)
    for rel in modified:
        print(f"MODIFIED: {rel}", file=sys.stderr)

    if missing or foreign or modified:
        print(
            f"FAIL: {len(missing)} missing, {len(foreign)} foreign, "
            f"{len(modified)} modified (of {len(expected)} manifest entries).",
            file=sys.stderr,
        )
        return 1
    print(f"OK: {len(expected)} files match the manifest.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="regenerate the manifest from the on-disk corpus instead of verifying",
    )
    args = parser.parse_args()
    if args.write:
        write_manifest()
    else:
        sys.exit(verify())


if __name__ == "__main__":
    main()
