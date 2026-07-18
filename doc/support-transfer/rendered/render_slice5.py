"""Render and validate the Codex-authored CC_FIN Slice-5 exact proposed diffs."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
SLICE1 = WIKI / "doc/support-transfer/rendered/slice1"
SLICE2 = WIKI / "doc/support-transfer/rendered/slice2"
SLICE3 = WIKI / "doc/support-transfer/rendered/slice3"
SLICE3C = WIKI / "doc/support-transfer/rendered/slice3c"
OUT = WIKI / "doc/support-transfer/rendered/slice5"
FIN = Path("C:/xPY/xPrj/CC_FIN")
PARENT = "9841751e13213e3e8766f41ec2b140dd8dd8fd74"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


def git_blob(path: str) -> str:
    completed = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN),
         "show", f"{PARENT}:{path}"],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"cannot read reviewed parent blob {PARENT}:{path}: "
            + completed.stderr.decode("utf-8", errors="replace")
        )
    return completed.stdout.decode("utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected one replacement site, found {count}")
    return text.replace(old, new)


agents = git_blob("AGENTS.md")
governance = git_blob("docs/governance-transition.md")
pyproject = tomllib.loads(git_blob("pyproject.toml"))
if pyproject.get("build-system", {}).get("build-backend") != "setuptools.build_meta":
    raise AssertionError("reviewed parent no longer has the expected setuptools backend")
project = pyproject.get("project", {})
if project.get("name") != "cc-fin" or project.get("version") != "2.1.0":
    raise AssertionError("reviewed parent packaging identity drifted")
where = pyproject.get("tool", {}).get("setuptools", {}).get("packages", {}).get("find", {}).get("where")
if where != ["src"]:
    raise AssertionError("reviewed parent package-discovery fact drifted")

agents = replace_once(
    agents,
    "Notes:\n- `pyproject.toml` is currently empty.\n- `pytest.ini` defines default pytest behavior.",
    "Notes:\n"
    "- `pyproject.toml` defines setuptools build metadata for `cc-fin` 2.1.0 and "
    "discovers packages under `src/`; runtime and test dependencies remain managed by "
    "`requirements.txt` and `requirements.test.txt`.\n"
    "- `pytest.ini` defines default pytest behavior.",
    "packaging fact",
)
agents = replace_once(
    agents,
    "No formal package build step is configured; verification is test-driven.",
    "Setuptools package metadata is configured, but routine verification remains "
    "test-driven; a support change does not imply a package build, tag, or release.",
    "build guidance fact",
)

support_section = """## Support Navigation and Session Continuity
The repository-local support core is navigation and evidence, not a second product backlog or
requirements authority. Start support-oriented work by reading, in order:

1. `support/README.md` for authority links, ownership, records, and exclusions.
2. `HANDOFF.md` and its referenced immutable record when one has been published.
3. `support/current-status.md` and `support/log.md` for current state and literal evidence.
4. `coordination/BOARD.md`, then active `coordination/messages/` and `coordination/claims/`.
5. Current Git/upstream/worktree state and any unfinished or risky artifacts.

Operational rules:
- Validate coordination state with `python scripts/agent_coord.py .`; regenerate BOARD only when
  its actual inputs change, using the installed CLI rather than hand-editing generated content.
- Keep only unresolved cross-agent communication active and follow the immutable archive/manifest
  lifecycle in `coordination/TEAM_PROTOCOL.md`.
- Treat skipped, unavailable, blocked, unknown, and not-run checks literally; never imply pass.
- Preserve ownership: Codex authors `AGENTS.md`, `.agents/`, and `CX_` records; Claude Code authors
  `CLAUDE.md`, `.claude/`, and `CC_` records; shared-neutral records follow their own contracts.
- Support navigation references existing product plans, docs, ADRs, workflows, and packaging
  authority; it does not copy or supersede them.

"""
agents = replace_once(
    agents,
    "## Completion Checklist for Agents\n",
    support_section + "## Completion Checklist for Agents\n",
    "support navigation insertion",
)

old_recovery = """## Divergence Recovery

Use only when local commits are intentionally discarded:

```bash
git reset --hard origin/main
```
"""
new_recovery = """## Divergence Recovery

Do not discard local commits or working-tree changes as routine synchronization. Stop writes and
capture evidence first:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git log --oneline --decorate --graph -n 20
```

Identify the exact commits and paths at risk; inspect active claims/messages; confirm the intended
recovery point and whether uncommitted work, a patch, branch, worktree, or backup must be preserved.
Prefer non-destructive recovery such as a fast-forward, preserving work on a named branch, or a
reviewed `git revert` of identified commits.

Any destructive discard requires explicit owner approval naming the exact target, recovery point,
preservation/backup evidence, validation commands, and stop conditions. This runbook does not
authorize `git reset --hard`, `git clean`, force-push, recursive deletion, or history rewriting.
After an approved recovery, rerun status, relevant native checks, and support validation; record the
literal commands, integer exit codes, and resulting Git identity.
"""
governance = replace_once(governance, old_recovery, new_recovery, "evidence-first recovery")

outputs = {"AGENTS.md": agents, "docs/governance-transition.md": governance}
placeholder_re = re.compile(r"\{\{([A-Z_]+)\}\}")
errors: list[str] = []
for rel, text in outputs.items():
    placeholders = sorted(set(placeholder_re.findall(text)))
    if placeholders:
        errors.append(f"{rel}: unresolved placeholders {placeholders}")
    hits = scan_sensitive(text)
    if hits:
        errors.append(f"{rel}: sensitive patterns {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "xPY"):
        if token in text:
            errors.append(f"{rel}: forbidden workspace reference {token!r}")
if "pyproject.toml` is currently empty" in agents:
    errors.append("AGENTS.md: stale packaging fact remains")
for required in (
    "support/README.md", "HANDOFF.md", "support/current-status.md", "support/log.md",
    "coordination/BOARD.md", "coordination/TEAM_PROTOCOL.md",
    "python scripts/agent_coord.py .",
):
    if required not in agents:
        errors.append(f"AGENTS.md: support navigation missing {required!r}")
for prohibited in ("git reset --hard origin/main",):
    if prohibited in governance:
        errors.append(f"docs/governance-transition.md: unsafe example remains {prohibited!r}")
for required in (
    "git status --short", "git rev-list --left-right --count HEAD...origin/main",
    "explicit owner approval", "reviewed `git revert`", "literal commands, integer exit codes",
):
    if required not in governance:
        errors.append(f"docs/governance-transition.md: recovery safeguard missing {required!r}")
if errors:
    raise AssertionError("\n".join(errors))

with tempfile.TemporaryDirectory(prefix="slice5-render-") as tmp:
    target = Path(tmp) / "target"
    shutil.copytree(SLICE1, target)
    for source in (SLICE2, SLICE3, SLICE3C):
        for path in source.rglob("*"):
            if path.is_file():
                rel = path.relative_to(source)
                destination = target / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
    for rel, text in outputs.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

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
            "Slice-5 overlay failed target coordination validation\n"
            + completed.stdout + completed.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during Slice-5 validation")

    for rel in (
        "support/README.md", "HANDOFF.md", "support/current-status.md", "support/log.md",
        "coordination/BOARD.md", "coordination/TEAM_PROTOCOL.md",
    ):
        if not (target / rel).is_file():
            raise AssertionError(f"support navigation target missing in overlay: {rel}")

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
print("INVENTORY PASSED: exactly two authorized modifications")
print("PACKAGING FACT PASSED: setuptools cc-fin 2.1.0, src discovery")
print("RECOVERY SAFETY PASSED: evidence-first, approval-gated, no routine hard reset")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"TARGET_PARENT={PARENT}")
