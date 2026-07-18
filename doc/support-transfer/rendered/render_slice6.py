"""Render and validate the Codex-authored CC_FIN Slice-6 one-line workflow diff."""

from __future__ import annotations

import io
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/slice6"
FIN = Path("C:/xPY/xPrj/CC_FIN")
PARENT = "9b79b5eff70bda8c04d8b4d3eb578b99a24fac25"
WORKFLOW = ".github/workflows/followup-ml-gate.yml"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


def git_blob(path: str) -> str:
    completed = subprocess.run(
        [
            "git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN),
            "show", f"{PARENT}:{path}",
        ],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"cannot read reviewed parent blob {PARENT}:{path}: "
            + completed.stderr.decode("utf-8", errors="replace")
        )
    return completed.stdout.decode("utf-8")


old = git_blob(WORKFLOW)
newline = "\r\n" if "\r\n" in old else "\n"
old_block = newline.join(("on:", "  push:", "    branches:", "      - master", "  pull_request:"))
new_block = newline.join(("on:", "  push:", "    branches:", "      - main", "  pull_request:"))
if old.count(old_block) != 1:
    raise AssertionError("reviewed parent branch-filter block drifted")
candidate = old.replace(old_block, new_block)

old_lines = old.splitlines()
new_lines = candidate.splitlines()
changed = [index for index, pair in enumerate(zip(old_lines, new_lines)) if pair[0] != pair[1]]
if len(old_lines) != len(new_lines) or changed != [5]:
    raise AssertionError(f"expected exactly one changed line at index 5, got {changed}")
if old_lines[5] != "      - master" or new_lines[5] != "      - main":
    raise AssertionError("branch-filter replacement is not exactly master to main")
if candidate.count("      - main") != 1 or "      - master" in candidate:
    raise AssertionError("candidate branch filter is ambiguous")

errors: list[str] = []
hits = scan_sensitive(candidate)
if hits:
    errors.append(f"sensitive patterns {hits}")
for token in ("LLM_Wiki", "03_PKE", "Enconet", "xPY"):
    if token in candidate:
        errors.append(f"forbidden workspace reference {token!r}")
if "${{ github.run_id }}" not in candidate:
    errors.append("existing GitHub expression was not preserved")
for required in (
    "pull_request:",
    "python -m py_compile scripts/followup_ml.py",
    "python -m pytest tests/test_followup_ml_parity_tool.py",
    "python scripts/followup_ml_ci_parity_gate.py",
    "python -m pytest tests/test_infra.py::test_fetch_data_parses_comma_thousands_numeric_fields -q",
):
    if required not in candidate:
        errors.append(f"existing workflow command missing {required!r}")
if errors:
    raise AssertionError("\n".join(errors))

archive = subprocess.run(
    [
        "git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN),
        "archive", "--format=tar", PARENT,
    ],
    capture_output=True,
    check=False,
)
if archive.returncode != 0:
    raise AssertionError(
        "cannot archive reviewed parent: "
        + archive.stderr.decode("utf-8", errors="replace")
    )

with tempfile.TemporaryDirectory(prefix="slice6-render-") as tmp:
    target = Path(tmp) / "target"
    target.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as tar:
        tar.extractall(target, filter="data")
    workflow_path = target / WORKFLOW
    workflow_path.write_bytes(candidate.encode("utf-8"))

    board_path = target / "coordination/BOARD.md"
    board_before = board_path.read_bytes()
    completed = subprocess.run(
        [sys.executable, str(target / "scripts/agent_coord.py"), str(target)],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "Slice-6 overlay failed target coordination validation\n"
            + completed.stdout + completed.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during Slice-6 validation")

if OUT.exists():
    shutil.rmtree(OUT)
path = OUT / WORKFLOW
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(candidate.encode("utf-8"))

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != {WORKFLOW}:
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")

print("rendered", WORKFLOW)
print("INVENTORY PASSED: exactly one authorized modification")
print("DIFF PASSED: exactly one line, master -> main")
print("WORKFLOW PRESERVATION PASSED: pull_request and all native commands unchanged")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"TARGET_PARENT={PARENT}")
