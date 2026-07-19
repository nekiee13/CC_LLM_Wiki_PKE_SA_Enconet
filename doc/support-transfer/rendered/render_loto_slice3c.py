"""Render and validate the CC_Loto Slice-3c navigation-closure tree."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
TEMPLATE = WIKI / "doc/support-transfer/templates/support-index.template.md"
OUT = WIKI / "doc/support-transfer/rendered/loto-slice3c"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
PARENT = "7100469757128defd3c437d6f9554744e57a6fa1"
ROOT_LINK = "Support and coordination: [support system](support/README.md)."
ROOT_ANCHOR = (
    "See [docs/architecture.md](docs/architecture.md) for the full "
    "module-by-module breakdown."
)

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


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


def git_blob(path: str) -> str:
    completed = subprocess.run(
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
    if completed.returncode != 0:
        raise AssertionError(
            f"cannot read reviewed parent blob {PARENT}:{path}: "
            + completed.stderr.decode("utf-8", errors="replace")
        )
    return completed.stdout.decode("utf-8")


args = parse_args()
render_timestamp = checked_timestamp(args.timestamp)

ownership = (
    "The human project owner approves gates, authority changes, destructive recovery, "
    "hosted-governance changes, tags, releases, and publication. Codex owns `AGENTS.md`, "
    "`.agents/`, and `CX_` records. Claude Code owns `CLAUDE.md`, `.claude/`, and `CC_` "
    "records. Coordination, support records, handoffs, schemas, templates, validators, "
    "and generated views are shared-neutral by contract. Each agent may inspect but "
    "must not edit or archive the other agent's owned infrastructure."
)

authorities = """- Product overview and native entry points: [root README](../README.md)
- Enhanced product plan (owner-designated product authority; its document header remains `Proposed`): [enhanced upgrade plan](../docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md)
- Architecture and current-state authorities: [architecture](../docs/architecture.md), [AS-IS](../docs/AS-IS.md), and [architectural and functional analysis](../docs/architectural_and_functional_analysis.md)
- Product progress and roadmap: [PROGRESS](../docs/PROGRESS.md) records the earlier TDD-plan scope and does not prove completion of the enhanced plan; [ROADMAP](../docs/ROADMAP.md) retains its own scope
- Hosted governance: [existing CI](../.github/workflows/ci.yml) is **integrate-existing-CI-only**; this support slice performs no hosted mutation
- Packaging authorities: [pyproject.toml](../pyproject.toml), [runtime requirements](../requirements.txt), and [locked requirements](../requirements.lock)
- Documentation/code indexes are **deferred**. This file is clone-local navigation only; it creates or refreshes no external index or corpus.
- Release/package status: release adapter is **inventory-only**. `git ls-remote --tags origin` exited `0` with no tag refs during packet preparation; GitHub release inventory was unavailable because the `gh` client is not installed, so this index makes no live-release-count claim. Creating a tag or release is outside this transfer."""

values = {
    "PROJECT_NAME": "CC_Loto",
    "PRODUCT_PLAN_PATH": "docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md",
    "PRODUCT_DOC_INDEX_PATH": "README.md (root product overview; docs/README.md is absent)",
    "SUPPORT_PROFILE_PATH": "support/PROFILE.md",
    "REPOSITORY_URL": "https://github.com/nekiee13/CC_Loto",
    "DEFAULT_BRANCH": "main",
    "AGENT_OWNERSHIP_SUMMARY": ownership,
    "TARGET_DECISION_AUTHORITIES": authorities,
    "NATIVE_VALIDATION_COMMAND": (
        "python run_tests.py --layer core-unit --pattern test*.py --verbosity 1; "
        "python run_tests.py --layer contract --pattern test*.py --verbosity 1; "
        "python run_tests.py --layer state-integrity --pattern test*.py --verbosity 1"
    ),
    "DATA_EXCLUSION_SUMMARY": (
        "secrets and machine-private paths; `DATA.csv` content; golden fixtures; "
        "model/output data, StatGrid, plots, caches, and generated artifacts per "
        "[PROFILE.md](PROFILE.md)"
    ),
}

support_index = TEMPLATE.read_text(encoding="utf-8")
for key, value in values.items():
    token = "{{" + key + "}}"
    if support_index.count(token) != 1:
        raise AssertionError(f"support template token {token} not found exactly once")
    support_index = support_index.replace(token, value)

root_readme = git_blob("README.md")
if ROOT_LINK in root_readme:
    raise AssertionError("README.md already contains the authorized support link")
if root_readme.count(ROOT_ANCHOR) != 1:
    raise AssertionError("README.md insertion anchor not found exactly once")
root_rendered = root_readme.replace(ROOT_ANCHOR, ROOT_ANCHOR + "\n" + ROOT_LINK)

outputs = {
    "README.md": root_rendered,
    "support/README.md": support_index,
}

placeholder_re = re.compile(r"\{\{([A-Z_]+)\}\}")
errors: list[str] = []
for rel, text in outputs.items():
    placeholders = sorted(set(placeholder_re.findall(text)))
    if placeholders:
        errors.append(f"{rel}: unresolved placeholders {placeholders}")
    hits = scan_sensitive(text)
    if hits:
        errors.append(f"{rel}: sensitive patterns {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "xPY", "CC_FIN"):
        if token in text:
            errors.append(f"{rel}: forbidden foreign/workspace reference {token!r}")
if errors:
    raise AssertionError("\n".join(errors))

before_lines = root_readme.splitlines()
after_lines = root_rendered.splitlines()
added = [line for line in after_lines if line not in before_lines]
if added != [ROOT_LINK] or len(after_lines) != len(before_lines) + 1:
    raise AssertionError(f"README.md diff is not exactly the approved line: {added}")

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="l3c-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        LOTO,
        target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"),
    )
    for rel, text in outputs.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    board_path = target / "coordination/BOARD.md"
    board_before = board_path.read_bytes()
    completed = subprocess.run(
        [sys.executable, str(target / "tools/support/agent_coord.py"), str(target)],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "two-path Slice-3c overlay changed BOARD inputs or failed validation\n"
            + completed.stdout
            + completed.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during Slice-3c validation")

    link_re = re.compile(r"\]\(([^)#\s]+)")
    for rel, text in outputs.items():
        path = target / rel
        for link in link_re.findall(text):
            if link.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / link).resolve()
            try:
                resolved.relative_to(target)
            except ValueError:
                errors.append(f"{rel}: escaping link {link!r}")
                continue
            if not resolved.exists():
                errors.append(f"{rel}: dangling link {link!r}")
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
for rel, text in outputs.items():
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != set(outputs):
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")

for rel in sorted(outputs):
    print("rendered", rel)
print("INVENTORY PASSED: 1 create + 1 one-line modification")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print("LINK/PLACEHOLDER/SENSITIVITY CHECKS PASSED")
print(f"RENDER_TIMESTAMP={render_timestamp}")
print(f"TARGET_PARENT={PARENT}")
