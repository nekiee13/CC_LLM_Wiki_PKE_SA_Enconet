"""Render and validate the Claude-owned CC_Loto guidance correction candidate.

Scope is one modification: replace the stale packaging sentence in `CLAUDE.md`
with the verified current packaging facts. The candidate is derived from the
reviewed parent blob so every unrelated byte is preserved. No CC_Loto file is
written by this renderer.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/loto-cc-guidance"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
PARENT = "fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


STALE = (
    "portfolio optimize) over 7 positional lottery series (`TS_1`..`TS_7`). Pure Python, run\n"
    "directly from the repo root with `sys.path` bootstrapping; no packaging or `requirements.txt`.\n"
)

CORRECTED = (
    "portfolio optimize) over 7 positional lottery series (`TS_1`..`TS_7`). Pure Python, packaged\n"
    "with setuptools as `dynamix-lottery` (`pyproject.toml`, Python `>=3.11`) and normally used as\n"
    "an editable install; `requirements.txt` and `requirements.lock` are the dependency"
    " authorities.\n"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", required=True, help="reviewed UTC ISO-8601 timestamp")
    parser.add_argument(
        "--native-python",
        help="optional target-requirements interpreter for disposable native validation",
    )
    return parser.parse_args()


def checked_timestamp(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise AssertionError("--timestamp must be UTC")
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")


def git_blob(path: str) -> bytes:
    result = subprocess.run(
        [
            "git",
            "-c",
            "safe.directory=C:/xPY/xPrj/CC_Loto",
            "-C",
            str(LOTO),
            "show",
            f"{PARENT}:{path}",
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"cannot read reviewed parent blob {PARENT}:{path}: "
            + result.stderr.decode("utf-8", errors="replace")
        )
    return result.stdout


def parent_has(path: str) -> bool:
    return (
        subprocess.run(
            [
                "git",
                "-c",
                "safe.directory=C:/xPY/xPrj/CC_Loto",
                "-C",
                str(LOTO),
                "cat-file",
                "-e",
                f"{PARENT}:{path}",
            ],
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )


args = parse_args()
render_timestamp = checked_timestamp(args.timestamp)

# 1. The corrected claims must be true of the reviewed parent, not assumed.
pyproject = tomllib.loads(git_blob("pyproject.toml").decode("utf-8"))
if pyproject.get("build-system", {}).get("build-backend") != "setuptools.build_meta":
    raise AssertionError("parent is not a setuptools project; correction text would be false")
project = pyproject.get("project", {})
if project.get("name") != "dynamix-lottery" or project.get("requires-python") != ">=3.11":
    raise AssertionError("parent packaging identity does not match the correction text")
for required in ("requirements.txt", "requirements.lock"):
    if not parent_has(required):
        raise AssertionError(f"correction text names {required!r}, absent at the reviewed parent")

# 2. Derive the candidate from the parent blob so unrelated bytes cannot drift.
parent_text = git_blob("CLAUDE.md").decode("utf-8")
if "\r" in parent_text:
    raise AssertionError("parent CLAUDE.md blob is not LF-normalized; re-review required")
if parent_text.count(STALE) != 1:
    raise AssertionError("stale packaging sentence not found exactly once at the reviewed parent")
candidate = parent_text.replace(STALE, CORRECTED)

# 3. The candidate must not reintroduce the stale claim or contradict the file's own rules.
errors: list[str] = []
for prohibited in (
    "no packaging or `requirements.txt`",
    "`sys.path` bootstrapping; no packaging",
):
    if prohibited in candidate:
        errors.append(f"CLAUDE.md: stale packaging wording survived: {prohibited!r}")
for anchor in (
    "The project is an installable package; entrypoints live inside it.",
    "pip install -e .",
    "python run_tests.py",
    "`DATA.csv`",
):
    if anchor not in candidate:
        errors.append(f"CLAUDE.md: pre-existing anchor lost: {anchor!r}")
if re.search(r"\{\{[A-Z_]+\}\}", candidate):
    errors.append("CLAUDE.md: unresolved placeholder")
hits = scan_sensitive(candidate)
if hits:
    errors.append(f"CLAUDE.md: sensitive patterns {hits}")
for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_FIN", "C:/xPY", "C:\\xPY"):
    if token in candidate:
        errors.append(f"CLAUDE.md: forbidden foreign/workspace reference {token!r}")
# This slice corrects a fact; it does not and must not assert pair synchronization.
for overclaim in ("synchronized with AGENTS.md", "guidance pair is synchronized"):
    if overclaim in candidate:
        errors.append(f"CLAUDE.md: unauthorized synchronization claim {overclaim!r}")

# 4. The diff must be exactly the reviewed paragraph edit.
parent_lines = parent_text.splitlines()
candidate_lines = candidate.splitlines()
removed = [line for line in parent_lines if line not in candidate_lines]
added = [line for line in candidate_lines if line not in parent_lines]
if len(removed) != 2 or len(added) != 3:
    errors.append(f"CLAUDE.md: diff is not the reviewed 2-removed/3-added edit: -{removed} +{added}")
if len(candidate_lines) != len(parent_lines) + 1:
    errors.append("CLAUDE.md: line count changed by more than the reviewed reflow")
if parent_lines[:7] != candidate_lines[:7] or parent_lines[9:] != candidate_lines[10:]:
    errors.append("CLAUDE.md: a line outside the reviewed paragraph changed")
if errors:
    raise AssertionError("\n".join(errors))

# 5. Prove the candidate is inert for support state: overlay, validate, keep BOARD identical.
temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="lcc-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        LOTO,
        target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"),
    )
    (target / "CLAUDE.md").write_text(candidate, encoding="utf-8", newline="\n")

    board_path = target / "coordination/BOARD.md"
    board_before = board_path.read_bytes()
    validation = subprocess.run(
        [sys.executable, str(target / "tools/support/agent_coord.py"), str(target)],
        text=True,
        capture_output=True,
        check=False,
    )
    if validation.returncode != 0:
        raise AssertionError(
            "guidance-correction overlay failed target coordination validation\n"
            + validation.stdout
            + validation.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during guidance-correction validation")
    if (target / "AGENTS.md").read_bytes() != git_blob("AGENTS.md"):
        raise AssertionError("Codex-owned AGENTS.md must remain untouched by this slice")

    link_re = re.compile(r"\]\(([^)#\s]+)")
    for link in link_re.findall(candidate):
        if link.startswith(("http://", "https://")):
            continue
        resolved = (target / link).resolve()
        try:
            resolved.relative_to(target)
        except ValueError:
            errors.append(f"CLAUDE.md: escaping link {link!r}")
            continue
        if not resolved.exists():
            errors.append(f"CLAUDE.md: dangling link {link!r}")
    if errors:
        raise AssertionError("\n".join(errors))

    if args.native_python:
        native_env = os.environ.copy()
        native_env["PYTHONDONTWRITEBYTECODE"] = "1"
        native_env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime" / "Output")
        native_env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime" / "ModelCache")
        expected = {"core-unit": 42, "contract": 25, "state-integrity": 3}
        for layer, expected_count in expected.items():
            native = subprocess.run(
                [
                    args.native_python,
                    "run_tests.py",
                    "--layer",
                    layer,
                    "--pattern",
                    "test*.py",
                    "--verbosity",
                    "1",
                ],
                cwd=target,
                env=native_env,
                text=True,
                capture_output=True,
                check=False,
            )
            combined = native.stdout + "\n" + native.stderr
            counts = [int(value) for value in re.findall(r"Ran (\d+) tests?", combined)]
            if native.returncode != 0 or counts != [expected_count]:
                raise AssertionError(
                    f"native layer {layer} failed: exit={native.returncode}, counts={counts}\n"
                    + combined
                )
            print(f"NATIVE PASSED: {layer} {expected_count}/{expected_count}, exit 0")

out_resolved = OUT.resolve()
expected_parent = (WIKI / "doc/support-transfer/rendered").resolve()
if out_resolved.parent != expected_parent:
    raise AssertionError(f"unsafe output path: {out_resolved}")
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
(OUT / "CLAUDE.md").write_text(candidate, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != {"CLAUDE.md"}:
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")

print("rendered CLAUDE.md")
print("INVENTORY PASSED: exactly one Claude-owned modification")
print("PARENT FACTS PASSED: setuptools dynamix-lottery, Python >=3.11, requirements.txt/.lock")
print("DIFF PASSED: 2 removed / 3 added lines, confined to the reviewed paragraph")
print("OWNERSHIP PASSED: AGENTS.md untouched; no synchronization claim asserted")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"RENDER_TIMESTAMP={render_timestamp}")
print(f"TARGET_PARENT={PARENT}")
