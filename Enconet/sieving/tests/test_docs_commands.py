"""C4.5 docs-vs-reality smoke checks (ADR-0007).

Every command quoted in README.md/QUICKSTART.md must execute at least through
``--help`` against the real CLI, and the user-facing docs must not advertise the
retired Streamlit GUI outside of explicit ADR-0007 retirement notices.
"""
from __future__ import annotations

import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMAND_DOCS = ["README.md", "QUICKSTART.md"]
GUARDED_DOCS = COMMAND_DOCS + ["PROJECT_INFO.md"]
FENCE_RE = re.compile(r"```(?:bash|sh|powershell)\s*\n(.*?)```", re.S)
RETIREMENT_MARKERS = ("adr-0007", "retired", "retire")


def _run(args: list[str]) -> tuple[int, str]:
    # Wide COLUMNS stops rich from wrapping long option names across table rows.
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", COLUMNS="200")
    proc = subprocess.run(
        args, cwd=PROJECT_ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=120, env=env,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _command_lines(doc: str) -> list[str]:
    text = (PROJECT_ROOT / doc).read_text(encoding="utf-8")
    lines = []
    for block in FENCE_RE.findall(text):
        for raw in block.splitlines():
            line = raw.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines


def _quoted_cli_commands() -> dict[str, set[str]]:
    """Map each documented cli.py subcommand to every flag the docs quote for it."""
    flags_by_subcommand: dict[str, set[str]] = {}
    for doc in COMMAND_DOCS:
        for line in _command_lines(doc):
            if not line.startswith("python cli.py"):
                continue
            tokens = shlex.split(line)
            assert len(tokens) >= 3, f"{doc} quotes a bare cli.py call: {line}"
            subcommand = tokens[2]
            flags = {t for t in tokens[3:] if t.startswith("--")}
            flags_by_subcommand.setdefault(subcommand, set()).update(flags)
    return flags_by_subcommand


def test_docs_quote_only_executable_command_kinds():
    """No quoted command may rely on the retired GUI or unknown entry points."""
    allowed_heads = ("python", "pip", "mkdir", "cd")
    for doc in COMMAND_DOCS:
        for line in _command_lines(doc):
            head = line.split()[0]
            # Filter-DSL example blocks quote bare "field:value" strings, not commands.
            if line.startswith(('"', "'")) or ":" in head:
                continue
            assert head in allowed_heads, f"{doc} quotes unexpected command: {line}"
            assert "streamlit" not in line, f"{doc} still advertises Streamlit: {line}"


def test_every_quoted_cli_command_reaches_help():
    flags_by_subcommand = _quoted_cli_commands()
    assert flags_by_subcommand, "docs no longer quote any cli.py commands"
    for subcommand, doc_flags in sorted(flags_by_subcommand.items()):
        code, out = _run([sys.executable, "cli.py", subcommand, "--help"])
        assert code == 0, f"`python cli.py {subcommand} --help` exited {code}:\n{out}"
        compact = re.sub(r"\s+", "", out)
        for flag in sorted(doc_flags):
            assert flag in compact, (
                f"documented flag {flag} missing from `cli.py {subcommand} --help`"
            )


def test_quoted_pip_command_is_executable():
    pip_lines = [
        line for doc in COMMAND_DOCS for line in _command_lines(doc)
        if line.startswith("pip ")
    ]
    if not pip_lines:
        pytest.skip("docs quote no pip commands")
    assert (PROJECT_ROOT / "requirements.txt").is_file()
    code, out = _run([sys.executable, "-m", "pip", "install", "--help"])
    assert code == 0, f"pip install --help exited {code}:\n{out}"


def test_gui_mentions_are_retirement_notices_only():
    """ADR-0007 regression guard: Streamlit/app.py may appear only in retirement notices."""
    for doc in GUARDED_DOCS:
        lines = (PROJECT_ROOT / doc).read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            low = line.lower()
            if "streamlit" in low or "app.py" in low:
                # A retirement notice may wrap; inspect the adjacent lines too.
                context = " ".join(lines[max(0, i - 1):i + 2]).lower()
                assert any(marker in context for marker in RETIREMENT_MARKERS), (
                    f"{doc}:{i + 1} mentions the GUI without an ADR-0007 retirement notice: {line.strip()}"
                )
