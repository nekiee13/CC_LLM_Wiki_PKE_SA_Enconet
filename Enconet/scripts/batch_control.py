#!/usr/bin/env python3
"""Create and validate one controlled continuation-batch state."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

import db_util
from audit_state import StateError, load_state


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_STATE = ROOT / "project-state.yml"
BATCH_DIR = ROOT / "manifests" / "batches"
RAW_MANIFEST = ROOT / "manifests" / "raw_sources.csv"
INGEST_MANIFEST = ROOT / "manifests" / "ingest_runs.csv"
INCOMING = ROOT / "incoming"

SOURCE_ID = re.compile(r"SRC-\d{8}-\d{3}")
INGEST_ID = re.compile(r"ING-\d{8}-\d{3}")
DOC_ID = re.compile(r"DOC-\d{4}")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    class FlowMap(dict):
        pass

    class BatchDumper(yaml.SafeDumper):
        pass

    def represent_flow_map(
        dumper: yaml.SafeDumper, value: FlowMap,
    ) -> yaml.nodes.MappingNode:
        return dumper.represent_mapping(
            "tag:yaml.org,2002:map", value, flow_style=True,
        )

    BatchDumper.add_representer(FlowMap, represent_flow_map)
    rendered = dict(data)
    rendered["gates"] = {
        gate: FlowMap(record) for gate, record in data["gates"].items()
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        yaml.dump(
            rendered, Dumper=BatchDumper, sort_keys=False, allow_unicode=True,
        ),
        encoding="utf-8",
        newline="",
    )
    temp.replace(path)


def _load_batch(path: Path) -> dict[str, Any]:
    data = load_state(path)
    if data.get("record_type") != "continuation_batch_state":
        raise StateError(f"not a continuation batch state: {path}")
    if data.get("status") not in {"active", "completed", "failed"}:
        raise StateError(f"invalid continuation batch status: {data.get('status')}")
    return data


def _active_batches(batch_dir: Path, exclude: Path | None = None) -> list[Path]:
    active: list[Path] = []
    if not batch_dir.exists():
        return active
    for path in batch_dir.glob("SRC-*.yml"):
        if exclude is not None and path.resolve() == exclude.resolve():
            continue
        try:
            data = _load_batch(path)
        except (OSError, StateError, yaml.YAMLError):
            active.append(path)
            continue
        if data["status"] == "active":
            active.append(path)
    return active


def _parse_document(value: str) -> dict[str, Any]:
    try:
        item = json.loads(value)
    except json.JSONDecodeError as exc:
        raise StateError(f"invalid --document-json: {exc}") from exc
    if not isinstance(item, dict):
        raise StateError("--document-json must be an object")
    allowed = {"filename", "logical_id", "change_type", "supersedes"}
    unknown = set(item) - allowed
    if unknown:
        raise StateError(f"unknown document fields: {', '.join(sorted(unknown))}")
    filename = str(item.get("filename", ""))
    logical_id = str(item.get("logical_id", ""))
    change_type = str(item.get("change_type", ""))
    supersedes = item.get("supersedes")
    if not filename or Path(filename).name != filename:
        raise StateError(f"document filename must be a direct incoming filename: {filename!r}")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", logical_id):
        raise StateError(f"invalid logical_id: {logical_id!r}")
    if change_type not in {"new", "updated"}:
        raise StateError(f"invalid change_type: {change_type!r}")
    if change_type == "new" and supersedes not in {None, ""}:
        raise StateError("new documents must not declare supersedes")
    if change_type == "updated" and (
        not isinstance(supersedes, str) or DOC_ID.fullmatch(supersedes) is None
    ):
        raise StateError("updated documents require supersedes=DOC-nnnn")
    return {
        "filename": filename,
        "logical_id": logical_id,
        "change_type": change_type,
        "supersedes": supersedes or None,
        "doc_id": None,
    }


def create_batch(
    *, source_batch_id: str, ingest_batch_id: str, size_class: str,
    documents: list[dict[str, Any]], output: Path,
    global_state: Path = GLOBAL_STATE, batch_dir: Path = BATCH_DIR,
    incoming: Path = INCOMING, raw_manifest: Path = RAW_MANIFEST,
) -> Path:
    if SOURCE_ID.fullmatch(source_batch_id) is None:
        raise StateError(f"invalid source batch ID: {source_batch_id}")
    if INGEST_ID.fullmatch(ingest_batch_id) is None:
        raise StateError(f"invalid ingest batch ID: {ingest_batch_id}")
    if source_batch_id[4:12] != ingest_batch_id[4:12]:
        raise StateError("source and ingest batch dates must match")
    if size_class not in {"large", "small"}:
        raise StateError(f"invalid size class: {size_class}")
    if size_class == "large" and len(documents) != 1:
        raise StateError("a large batch must contain exactly one document")
    if size_class == "small" and len(documents) not in {2, 3}:
        raise StateError("a small batch must contain two or three documents")
    if output.exists():
        raise StateError(f"batch state already exists: {output}")
    global_data = load_state(global_state)
    if global_data.get("phase") != "sieved":
        raise StateError(
            f"continuation batches require global phase sieved, not {global_data.get('phase')}"
        )
    active = _active_batches(batch_dir)
    if active:
        raise StateError(f"another continuation batch is active: {active[0]}")
    filenames = [str(item["filename"]) for item in documents]
    if len(set(filenames)) != len(filenames):
        raise StateError("a batch cannot contain duplicate filenames")
    registered = _read_csv(raw_manifest)
    registered_ids = {row["doc_id"] for row in registered}
    registered_names = {row["filename"] for row in registered}
    for item in documents:
        candidate = incoming / str(item["filename"])
        if not candidate.is_file():
            raise StateError(f"incoming source is missing: {candidate}")
        if item["filename"] in registered_names:
            raise StateError(f"filename is already registered: {item['filename']}")
        if item["change_type"] == "updated" and item["supersedes"] not in registered_ids:
            raise StateError(f"unknown predecessor: {item['supersedes']}")
    data: dict[str, Any] = {
        "schema_version": "1.0",
        "record_type": "continuation_batch_state",
        "batch_id": source_batch_id,
        "ingest_batch_id": ingest_batch_id,
        "created_at_utc": utc_now(),
        "status": "active",
        "continuation_from_phase": "sieved",
        "phase": "setup",
        "supplier": str(global_data.get("supplier", "")),
        "deliverable_language": global_data.get("deliverable_language"),
        "size_class": size_class,
        "documents": documents,
        "gates": {
            f"G{number}": {"status": "pending", "date": None, "decision_ref": None}
            for number in range(1, 8)
        },
        "benchmarks_locked": bool(global_data.get("benchmarks_locked", False)),
    }
    _write_yaml(output, data)
    return output


def bind_document(
    state_path: Path, *, filename: str, doc_id: str,
    raw_manifest: Path = RAW_MANIFEST,
) -> None:
    if DOC_ID.fullmatch(doc_id) is None:
        raise StateError(f"invalid document ID: {doc_id}")
    data = _load_batch(state_path)
    matches = [item for item in data["documents"] if item["filename"] == filename]
    if len(matches) != 1:
        raise StateError(f"batch contains {len(matches)} entries for {filename}")
    item = matches[0]
    if item.get("doc_id") not in {None, doc_id}:
        raise StateError(f"{filename} is already bound to {item['doc_id']}")
    rows = [row for row in _read_csv(raw_manifest) if row.get("doc_id") == doc_id]
    if len(rows) != 1 or rows[0].get("filename") != filename:
        raise StateError(f"registry row does not bind {doc_id} to {filename}")
    required = [
        f"batch_id={data['batch_id']}",
        f"change_type={item['change_type']}",
    ]
    if item["change_type"] == "updated":
        required.append(f"supersedes={item['supersedes']}")
    if any(tag not in rows[0].get("notes", "") for tag in required):
        raise StateError(f"registry notes for {doc_id} lack continuation lineage tags")
    item["doc_id"] = doc_id
    _write_yaml(state_path, data)


def validate_batch(
    state_path: Path, *, raw_manifest: Path = RAW_MANIFEST,
    ingest_manifest: Path = INGEST_MANIFEST, database: Path = db_util.DEFAULT_DB,
    require_complete: bool = False,
) -> list[str]:
    data = _load_batch(state_path)
    errors: list[str] = []
    raw_rows = _read_csv(raw_manifest)
    ingest_rows = _read_csv(ingest_manifest)
    for item in data["documents"]:
        doc_id = item.get("doc_id")
        if not doc_id:
            errors.append(f"unbound document: {item['filename']}")
            continue
        raw = [row for row in raw_rows if row.get("doc_id") == doc_id]
        if len(raw) != 1:
            errors.append(f"{doc_id}: expected one raw registry row, found {len(raw)}")
            continue
        required = [
            f"batch_id={data['batch_id']}",
            f"change_type={item['change_type']}",
        ]
        if item["change_type"] == "updated":
            required.append(f"supersedes={item['supersedes']}")
        if any(tag not in raw[0].get("notes", "") for tag in required):
            errors.append(f"{doc_id}: raw registry lineage tags do not match batch state")
        if require_complete:
            runs = [
                row for row in ingest_rows
                if row.get("doc_id") == doc_id
                and row.get("run_type") == "initial_sieve"
                and row.get("result") == "PASS"
                and f"batch_id={data['ingest_batch_id']}" in row.get("notes", "")
            ]
            if len(runs) != 1:
                errors.append(f"{doc_id}: expected one passing initial ingestion run")
    if require_complete and data.get("phase") != "sieved":
        errors.append(f"batch phase is {data.get('phase')}, not sieved")
    if require_complete and data["gates"]["G1"].get("status") != "approved":
        errors.append("batch G1 is not approved")
    if require_complete and not errors:
        try:
            with db_util.connect(database) as connection:
                for item in data["documents"]:
                    doc_id = item["doc_id"]
                    chunks = connection.execute(
                        "SELECT count(*) FROM document_chunks WHERE doc_id=?", (doc_id,)
                    ).fetchone()[0]
                    active = connection.execute(
                        "SELECT count(*) FROM sieve_runs "
                        "WHERE doc_id=? AND is_active=1 AND completed_at IS NOT NULL",
                        (doc_id,),
                    ).fetchone()[0]
                    if not chunks:
                        errors.append(f"{doc_id}: no chunks")
                    if active != 1:
                        errors.append(f"{doc_id}: expected one completed active sieve run")
        except (OSError, sqlite3.Error) as exc:
            errors.append(f"database validation failed: {exc}")
    return errors


def complete_batch(state_path: Path) -> None:
    errors = validate_batch(state_path, require_complete=True)
    if errors:
        raise StateError("; ".join(errors))
    data = _load_batch(state_path)
    data["status"] = "completed"
    data["completed_at_utc"] = utc_now()
    _write_yaml(state_path, data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--source-batch-id", required=True)
    create.add_argument("--ingest-batch-id", required=True)
    create.add_argument("--size-class", required=True, choices=["large", "small"])
    create.add_argument("--document-json", action="append", default=[])
    create.add_argument("--filename", action="append", default=[])
    create.add_argument("--logical-id", action="append", default=[])
    create.add_argument(
        "--change-type", action="append", default=[], choices=["new", "updated"],
    )
    create.add_argument("--supersedes", action="append", default=[])
    create.add_argument("--output", type=Path)
    bind = sub.add_parser("bind")
    bind.add_argument("state", type=Path)
    bind.add_argument("--filename", required=True)
    bind.add_argument("--doc-id", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("state", type=Path)
    validate.add_argument("--require-complete", action="store_true")
    complete = sub.add_parser("complete")
    complete.add_argument("state", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            documents = [_parse_document(value) for value in args.document_json]
            if args.filename or args.logical_id or args.change_type or args.supersedes:
                if not (
                    len(args.filename) == len(args.logical_id) == len(args.change_type)
                ):
                    raise StateError(
                        "repeat --filename, --logical-id, and --change-type equally"
                    )
                if args.supersedes and len(args.supersedes) != len(args.filename):
                    raise StateError(
                        "repeat --supersedes once per simple document or omit it"
                    )
                supersedes = args.supersedes or [None] * len(args.filename)
                for index, filename in enumerate(args.filename):
                    documents.append(_parse_document(json.dumps({
                        "filename": filename,
                        "logical_id": args.logical_id[index],
                        "change_type": args.change_type[index],
                        "supersedes": supersedes[index],
                    })))
            if not documents:
                raise StateError("at least one document must be supplied")
            output = args.output or BATCH_DIR / f"{args.source_batch_id}.yml"
            created = create_batch(
                source_batch_id=args.source_batch_id,
                ingest_batch_id=args.ingest_batch_id,
                size_class=args.size_class,
                documents=documents,
                output=output,
            )
            print(f"batch_control: PASS - created {created}")
        elif args.command == "bind":
            bind_document(args.state, filename=args.filename, doc_id=args.doc_id)
            print(f"batch_control: PASS - bound {args.doc_id}")
        elif args.command == "validate":
            errors = validate_batch(args.state, require_complete=args.require_complete)
            if errors:
                raise StateError("; ".join(errors))
            print("batch_control: PASS")
        else:
            complete_batch(args.state)
            print("batch_control: PASS - completed")
        return 0
    except (OSError, sqlite3.Error, StateError, yaml.YAMLError) as exc:
        print(f"batch_control: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
