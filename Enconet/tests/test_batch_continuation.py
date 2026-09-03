from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import batch_control  # noqa: E402
import gate_packet  # noqa: E402
import audit_state  # noqa: E402
from audit_state import StateError  # noqa: E402


def state_file(tmp_path: Path, phase: str = "sieved") -> Path:
    path = tmp_path / "project-state.yml"
    path.write_text(yaml.safe_dump({
        "phase": phase,
        "supplier": "enconet",
        "deliverable_language": None,
        "gates": {
            f"G{number}": {"status": "pending", "date": None, "decision_ref": None}
            for number in range(1, 8)
        },
        "benchmarks_locked": True,
    }, sort_keys=False), encoding="utf-8")
    return path


def raw_manifest(tmp_path: Path) -> Path:
    path = tmp_path / "raw_sources.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.DictWriter(handle, fieldnames=[
            "doc_id", "filename", "title", "supplier", "doc_date", "language",
            "side_hint", "sha256", "promoted_utc", "source_url", "notes",
        ]).writeheader()
    return path


def document(filename: str, *, change_type: str = "new",
             supersedes: str | None = None) -> dict[str, object]:
    return {
        "filename": filename,
        "logical_id": "PK-SUK-001",
        "change_type": change_type,
        "supersedes": supersedes,
        "doc_id": None,
    }


def test_large_continuation_batch_preserves_global_state(tmp_path: Path) -> None:
    global_state = state_file(tmp_path)
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    (incoming / "manual.md").write_text("# Manual\n", encoding="utf-8")
    output = tmp_path / "batches" / "SRC-20260728-001.yml"
    batch_control.create_batch(
        source_batch_id="SRC-20260728-001",
        ingest_batch_id="ING-20260728-001",
        size_class="large",
        documents=[document("manual.md")],
        output=output,
        global_state=global_state,
        batch_dir=output.parent,
        incoming=incoming,
        raw_manifest=raw_manifest(tmp_path),
    )
    global_data = yaml.safe_load(global_state.read_text(encoding="utf-8"))
    batch_data = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert global_data["phase"] == "sieved"
    assert batch_data["phase"] == "setup"
    assert batch_data["status"] == "active"
    assert batch_data["continuation_from_phase"] == "sieved"
    assert "G1: {status: pending, date: null, decision_ref: null}" in output.read_text(
        encoding="utf-8"
    )


@pytest.mark.parametrize(
    ("size_class", "count"),
    [("large", 2), ("small", 1), ("small", 4)],
)
def test_batch_size_rules_fail_closed(
    tmp_path: Path, size_class: str, count: int,
) -> None:
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    documents = []
    for index in range(count):
        name = f"doc-{index}.md"
        (incoming / name).write_text("x", encoding="utf-8")
        documents.append(document(name))
    with pytest.raises(StateError):
        batch_control.create_batch(
            source_batch_id="SRC-20260728-001",
            ingest_batch_id="ING-20260728-001",
            size_class=size_class,
            documents=documents,
            output=tmp_path / "batches" / "SRC-20260728-001.yml",
            global_state=state_file(tmp_path),
            batch_dir=tmp_path / "batches",
            incoming=incoming,
            raw_manifest=raw_manifest(tmp_path),
        )


def test_continuation_requires_global_sieved_and_single_active_writer(tmp_path: Path) -> None:
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    (incoming / "manual.md").write_text("x", encoding="utf-8")
    batches = tmp_path / "batches"
    batches.mkdir()
    active = batches / "SRC-20260727-001.yml"
    active.write_text(yaml.safe_dump({
        "record_type": "continuation_batch_state",
        "status": "active",
        "phase": "setup",
        "gates": {},
    }), encoding="utf-8")
    with pytest.raises(StateError, match="another continuation batch is active"):
        batch_control.create_batch(
            source_batch_id="SRC-20260728-001",
            ingest_batch_id="ING-20260728-001",
            size_class="large",
            documents=[document("manual.md")],
            output=batches / "SRC-20260728-001.yml",
            global_state=state_file(tmp_path),
            batch_dir=batches,
            incoming=incoming,
            raw_manifest=raw_manifest(tmp_path),
        )
    active.unlink()
    with pytest.raises(StateError, match="require global phase sieved"):
        batch_control.create_batch(
            source_batch_id="SRC-20260728-001",
            ingest_batch_id="ING-20260728-001",
            size_class="large",
            documents=[document("manual.md")],
            output=batches / "SRC-20260728-001.yml",
            global_state=state_file(tmp_path, "evidence_reviewed"),
            batch_dir=batches,
            incoming=incoming,
            raw_manifest=raw_manifest(tmp_path),
        )


def test_gate_packet_uniqueness_is_scoped_per_batch(tmp_path: Path) -> None:
    template = ROOT / "templates" / "gate-packet-template.md"
    first = tmp_path / "G1-first.md"
    second = tmp_path / "G1-second.md"
    gate_packet.create_packet(
        gate="G1", supplier="enconet", decision_ref="G1-FIRST",
        summary="first", evidence="- first", validation="- PASS",
        output=first, template=template, scope_id="SRC-20260723-001",
    )
    gate_packet.create_packet(
        gate="G1", supplier="enconet", decision_ref="G1-SECOND",
        summary="second", evidence="- second", validation="- PASS",
        output=second, template=template, scope_id="SRC-20260728-001",
    )
    with pytest.raises(StateError, match="scope SRC-20260728-001"):
        gate_packet.create_packet(
            gate="G1", supplier="enconet", decision_ref="G1-DUPLICATE",
            summary="duplicate", evidence="- duplicate", validation="- PASS",
            output=tmp_path / "G1-duplicate.md", template=template,
            scope_id="SRC-20260728-001",
        )


def test_batch_scoped_gate_decision_does_not_overwrite_global_state(
    tmp_path: Path,
) -> None:
    global_state = state_file(tmp_path)
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    (incoming / "manual.md").write_text("x", encoding="utf-8")
    batch_state = tmp_path / "batches" / "SRC-20260728-001.yml"
    batch_control.create_batch(
        source_batch_id="SRC-20260728-001",
        ingest_batch_id="ING-20260728-001",
        size_class="large",
        documents=[document("manual.md")],
        output=batch_state,
        global_state=global_state,
        batch_dir=batch_state.parent,
        incoming=incoming,
        raw_manifest=raw_manifest(tmp_path),
    )
    approvals = tmp_path / "approvals.csv"
    approvals.write_text(
        "object_id,decision,date,reviewer,notes\n"
        "G1-20260728-SRC001,approved,2026-07-28,owner,go\n",
        encoding="utf-8",
    )
    log = tmp_path / "log.md"
    log.write_text("# Log\n", encoding="utf-8")
    audit_state.record_gate_decision(
        "G1", "G1-20260728-SRC001", state_path=batch_state,
        approvals=approvals, log=log,
    )
    assert yaml.safe_load(batch_state.read_text(encoding="utf-8"))["gates"]["G1"][
        "status"
    ] == "approved"
    assert yaml.safe_load(global_state.read_text(encoding="utf-8"))["gates"]["G1"][
        "status"
    ] == "pending"
