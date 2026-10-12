"""Render and validate the CC_Loto Codex-guidance evidence-B candidate.

The candidate changes only ``support/log.md`` and ``support/current-status.md``.
The log is derived from commit A, so its published prefix is preserved by
construction.  This renderer never writes the CC_Loto worktree.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/loto-codex-guidance-correction-evidence-b"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
CONTENT_A = "2aebed6bd2e96d27640776376af7a4e06a7e2030"
PARENT = "d5dc65e568ee73d82389e6e1d3fdf24122661adf"
AGENTS_OBJECT = "42571a2c5f67b5a11759f38d7d65f50f156087c3"
CLAUDE_OBJECT = "3edd87504e76a97d8ba46ecf40e81b8ad894299f"
PACKET = "82c3595e666dbee5e50e78634c456c011009cc6f"
APPROVAL = "8f808757655530fb44c9862b703f76ed2cab742c"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


EVENTS = (
    "support-committed-local | 2026-07-20T03:12:08Z | LOTO-CODEX-GUIDANCE-CORRECTION | "
    f"Content commit A `{CONTENT_A}` was created locally on published parent `{PARENT}` from "
    f"Wiki packet `{PACKET}` and owner approval `{APPROVAL}`; A modifies exactly root `AGENTS.md` "
    f"at reviewed Git object `{AGENTS_OBJECT}`, with 3 additions and 2 deletions; Claude-owned "
    f"`CLAUDE.md` remains unchanged at `{CLAUDE_OBJECT}`; nothing pushed | codex\n"
    "support-validated | 2026-07-20T03:12:08Z | LOTO-CODEX-GUIDANCE-CORRECTION-A | At clean A, "
    "the target support aggregate exited 0 with coordination passed at 0 errors/0 warnings, "
    "bootstrap handoff not-configured, one support schema parsed, and focused support tests passed; "
    "direct coordination validation exited 0 and `coordination/BOARD.md` remained byte-identical. "
    "Target-native core-unit, contract, and state-integrity passed 42/42, 30/30, and 3/3, all exit "
    "0. Optional, optimizer-core, integration, webapp, and hosted-CI layers were not run. This is "
    "owner-approved alignment step 1 only: the guidance pair remains not synchronized; Claude-owned "
    "step 2 and M4 remain closed | codex\n"
)

STATUS = """# CC_Loto current support status

- Observed at UTC: `2026-07-20T03:12:08Z`
- HEAD: `this status is recorded by evidence commit B, whose parent is Codex-guidance correction content commit A 2aebed6bd2e96d27640776376af7a4e06a7e2030`
- Upstream relation: `the two local Codex-guidance correction commits remain unpushed; origin/main remains at published aggregate-validation tip d5dc65e568ee73d82389e6e1d3fdf24122661adf`
- Worktree: `clean required at evidence commit B before final-tree validation and reviewer handoff`
- Support milestone: `aggregate validation and rollback evidence are independently reviewed; owner approved minimal alignment; step 1 awaits committed-object review; step 2 and M4 remain closed`
- Product plan reference: `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`

## Active work

- Content commit A modifies exactly Codex-owned root [AGENTS.md](../AGENTS.md). It replaces an
  incomplete support-check vocabulary with the canonical seven literal states: `passed`, `failed`,
  `skipped`, `not-run`, `unknown`, `not-configured`, and `unavailable`.
- The same sentence now distinguishes `blocked` as a handoff/blocker state, never a check result.
  The existing warning that skipped, blocked, or unexecuted checks must never be reported as passed
  remains byte-identical.
- This is the first of two owner-approved minimal-alignment steps. Claude Code independently accepted
  the exact pre-write candidate. This status and the two appended log events form local evidence
  commit B. Neither A nor B may be pushed until Claude reviews the committed objects and explicitly
  authorizes the exact fast-forward.

## Messages, claims, and blockers

The installed target-local coordination queue remains empty. Cross-agent review occurs through the
Wiki neutral channel. Push is blocked pending Claude's independent committed-object review. The
Claude-owned alignment step remains closed until this Codex-owned step is published and closed.

## Validation state

At clean content commit A, `python tools/validate_support.py --root . --native-python
<target-python> --no-record` exited `0`: coordination passed with 0 errors and 0 warnings, bootstrap
handoff was `not-configured`, one support schema parsed, and focused support tests passed. Direct
coordination validation exited `0`, and `coordination/BOARD.md` remained byte-identical.

With output and model-cache paths redirected outside the repository, target-native core-unit,
contract, and state-integrity layers passed 42/42, 30/30, and 3/3, all exit `0`. Optional,
optimizer-core, integration, webapp, and hosted-CI layers were **not run**; that is a `not-run`
state, not a pass. The committed `AGENTS.md` object matches the reviewed authority, and `CLAUDE.md`
is unchanged.

## Guidance pair state

The two agent guidance files remain **not synchronized**. This step corrects Codex-owned check-state
vocabulary only. The separately gated Claude-owned minimal alignment has not started and remains an
owner-approved next step only after publication and closure of this one.

## Exact next action

- Owner: `claude-code (independent reviewer), then codex (implementer)`
- Prerequisites: evidence commit B exists; worktree is clean; `B^ == A`; A changes exactly
  `AGENTS.md`; B changes exactly `support/log.md` and `support/current-status.md`; all committed
  objects match their rendered authorities
- Action: independently review local commits A and B, then authorize or reject one fast-forward push
  containing exactly A followed by B
- Stop condition: amended or rebased identity, extra path or commit, byte mismatch, stale board,
  applicable unavailable check returning zero, native regression, target drift, synchronization
  overclaim, or reviewer finding

## Evidence

- Slice preparation and local validation events in [log.md](log.md)
- Handoff state in [HANDOFF.md](../HANDOFF.md)
- Record classes in [RECORD-KEEPING.md](RECORD-KEEPING.md)
- Native and recovery authority in [PROFILE.md](PROFILE.md)
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-python")
    return parser.parse_args()


def run_git(*args: str, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "-C", str(LOTO), *args],
        capture_output=True,
        text=text,
        check=False,
    )


args = parse_args()
if run_git("rev-parse", "HEAD").stdout.strip() != CONTENT_A:
    raise AssertionError("target HEAD is not the reviewed content commit A")
if run_git("status", "--porcelain=v1").stdout:
    raise AssertionError("target worktree is not clean")
if run_git("rev-parse", f"{CONTENT_A}^").stdout.strip() != PARENT:
    raise AssertionError("content commit A is not based on the published parent")
if run_git("diff-tree", "--no-commit-id", "--name-only", "-r", CONTENT_A).stdout.splitlines() != ["AGENTS.md"]:
    raise AssertionError("content commit A does not change exactly AGENTS.md")
for path, expected in (("AGENTS.md", AGENTS_OBJECT), ("CLAUDE.md", CLAUDE_OBJECT)):
    actual = run_git("rev-parse", f"{CONTENT_A}:{path}").stdout.strip()
    if actual != expected:
        raise AssertionError(f"commit A {path} object {actual} != reviewed {expected}")

blob = run_git("show", f"{CONTENT_A}:support/log.md", text=False)
if blob.returncode:
    raise AssertionError(blob.stderr.decode("utf-8", errors="replace"))
parent_log = blob.stdout.decode("utf-8")
if "\r" in parent_log or not parent_log.endswith("\n"):
    raise AssertionError("parent log is not append-safe LF text")
log = parent_log + EVENTS
added = log.splitlines()[len(parent_log.splitlines()):]
if not log.startswith(parent_log) or len(added) != 2:
    raise AssertionError("append-only proof failed")
if any(line.count(" | ") < 4 or not line.endswith(" | codex") for line in added):
    raise AssertionError("appended event contract failed")

outputs = {"support/log.md": log, "support/current-status.md": STATUS}
errors: list[str] = []
for rel, body in outputs.items():
    if scan_sensitive(body):
        errors.append(f"{rel}: sensitive pattern")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_FIN", "C:/xPY", "C:\\xPY"):
        if token in body:
            errors.append(f"{rel}: foreign/workspace token {token}")
    for overclaim in ("pair is synchronized", "guidance is synchronized", "now synchronized"):
        if overclaim in body:
            errors.append(f"{rel}: synchronization overclaim")
if "remain **not synchronized**" not in STATUS:
    errors.append("required non-synchronization statement missing")
if errors:
    raise AssertionError("\n".join(errors))

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="lcgb-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(LOTO, target, ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"))
    for rel, body in outputs.items():
        (target / rel).write_text(body, encoding="utf-8", newline="\n")
    board = target / "coordination/BOARD.md"
    before = board.read_bytes()
    coord = subprocess.run([sys.executable, str(target / "tools/support/agent_coord.py"), str(target)], capture_output=True, text=True, check=False)
    if coord.returncode or board.read_bytes() != before:
        raise AssertionError("overlay coordination validation failed or changed BOARD\n" + coord.stdout + coord.stderr)
    if args.native_python:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime/Output")
        env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime/ModelCache")
        aggregate = subprocess.run([sys.executable, str(target / "tools/validate_support.py"), "--root", str(target), "--native-python", args.native_python, "--no-record"], capture_output=True, text=True, check=False)
        if aggregate.returncode:
            raise AssertionError("overlay aggregate failed\n" + aggregate.stdout + aggregate.stderr)
        for layer, count in (("core-unit", 42), ("contract", 30), ("state-integrity", 3)):
            native = subprocess.run([args.native_python, "run_tests.py", "--layer", layer, "--pattern", "test*.py", "--verbosity", "1"], cwd=target, env=env, capture_output=True, text=True, check=False)
            counts = [int(n) for n in re.findall(r"Ran (\d+) tests?", native.stdout + native.stderr)]
            if native.returncode or counts != [count]:
                raise AssertionError(f"native {layer} failed: exit={native.returncode}, counts={counts}\n" + native.stdout + native.stderr)
            print(f"NATIVE PASSED: {layer} {count}/{count}, exit 0")

if OUT.exists():
    shutil.rmtree(OUT)
for rel, body in outputs.items():
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")
print("APPEND-ONLY PASSED: parent prefix preserved; exactly two events appended")
print("TRUTH GUARDS PASSED: pair remains not synchronized; step 2 and M4 remain closed")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"CONTENT_A={CONTENT_A}")
