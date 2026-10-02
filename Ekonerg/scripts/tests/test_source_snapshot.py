from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from source_snapshot import create  # noqa: E402


def test_snapshot_is_hash_only_dated_and_repeatable(tmp_path: Path):
    # The live project is read-only for this test; use a temporary copied module root.
    project = tmp_path / "Ekonerg"
    (project / "incoming").mkdir(parents=True)
    (project / "out").mkdir()
    (project / "incoming" / "a.txt").write_text("approved source", encoding="utf-8")
    import source_snapshot
    original_root = source_snapshot.ROOT
    original_local_path = source_snapshot.local_path
    source_snapshot.ROOT = project
    source_snapshot.local_path = lambda value: Path(value)
    try:
        path = create("2026-10-02", g1_ref="G1-EKONERG-2026-10-02", output_root=project / "out")
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["file_count"] == 1
        assert payload["files"][0]["relative_path"] == "incoming/a.txt"
        assert "approved source" not in path.read_text(encoding="utf-8")
        assert create("2026-10-02", g1_ref="G1-EKONERG-2026-10-02", output_root=project / "out") == path
    finally:
        source_snapshot.ROOT = original_root
        source_snapshot.local_path = original_local_path


def test_snapshot_rejects_changed_repeat(tmp_path: Path):
    project = tmp_path / "Ekonerg"
    (project / "incoming").mkdir(parents=True)
    (project / "out").mkdir()
    source = project / "incoming" / "a.txt"
    source.write_text("one", encoding="utf-8")
    import source_snapshot
    original_root = source_snapshot.ROOT
    original_local_path = source_snapshot.local_path
    source_snapshot.ROOT = project
    source_snapshot.local_path = lambda value: Path(value)
    try:
        create("2026-10-02", g1_ref="G1", output_root=project / "out")
        source.write_text("two", encoding="utf-8")
        with pytest.raises(ValueError, match="different content"):
            create("2026-10-02", g1_ref="G1", output_root=project / "out")
    finally:
        source_snapshot.ROOT = original_root
        source_snapshot.local_path = original_local_path
