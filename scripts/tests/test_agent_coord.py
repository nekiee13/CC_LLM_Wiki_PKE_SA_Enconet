import importlib.util
import io
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "agent_coord.py"
SPEC = importlib.util.spec_from_file_location("agent_coord", SCRIPT)
agent_coord = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(agent_coord)


def test_standard_streams_escape_characters_missing_from_cp1252(monkeypatch):
    stdout_bytes = io.BytesIO()
    stderr_bytes = io.BytesIO()
    stdout = io.TextIOWrapper(stdout_bytes, encoding="cp1252", errors="strict")
    stderr = io.TextIOWrapper(stderr_bytes, encoding="cp1252", errors="strict")
    monkeypatch.setattr(agent_coord.sys, "stdout", stdout)
    monkeypatch.setattr(agent_coord.sys, "stderr", stderr)

    agent_coord.configure_standard_streams()
    stdout.write("route: codex → claude-code")
    stderr.write("problem: →")
    stdout.flush()
    stderr.flush()

    assert stdout_bytes.getvalue() == b"route: codex \\u2192 claude-code"
    assert stderr_bytes.getvalue() == b"problem: \\u2192"


def test_board_uses_ascii_message_direction_separator(tmp_path, monkeypatch):
    messages = tmp_path / "messages"
    archive = tmp_path / "archive"
    claims = tmp_path / "claims"
    messages.mkdir()
    archive.mkdir()
    claims.mkdir()
    (messages / "CX_test.md").write_text(
        "---\n"
        "message_id: CX_test\n"
        "created_at_utc: 2026-07-13T00:00:00Z\n"
        "from_agent: codex\n"
        "to_agent: claude-code\n"
        "type: status\n"
        "task: TEST\n"
        "related_files: []\n"
        "---\n\n"
        "Test message.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(agent_coord, "MESSAGES_DIR", messages)
    monkeypatch.setattr(agent_coord, "ARCHIVE_DIR", archive)
    monkeypatch.setattr(agent_coord, "CLAIMS_DIR", claims)
    monkeypatch.setattr(agent_coord, "HANDOFF_POINTER", tmp_path / "HANDOFF.md")

    body = agent_coord.build_board_body()

    assert "codex -> claude-code: TEST" in body
    assert "→" not in body
