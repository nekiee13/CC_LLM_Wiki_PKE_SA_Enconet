"""Render and validate CC_Loto Slice 6 evidence-commit B candidates."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/loto-slice6-evidence-b"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
PARENT = "f549b40665c2321ff46168d43c67b2f2f9422bd5"
CONTENT_A = "14f0cf2638a26b08c02fccfae353957333bfb8f8"
OBJECTS = {
    "tools/validate_support.py": "40b44057048fb3083213f040bc5d769e399a42a3",
    "tests/contract/test_support_coordination.py": "75bf30a8a1cbc857bda86bd0ac85111857e38f8f",
    "tests/contract/test_support_handoff.py": "0fc854e085f19a0d2367bd5290d7e8e4b398bc98",
}

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


EVENTS = (
    "support-committed-local | 2026-07-20T01:45:13Z | LOTO-SLICE-6 | Content commit A "
    f"`{CONTENT_A}` was created locally on published parent `{PARENT}` from corrected Wiki packet "
    "commit `a7e028c85bb2a36ef6f7a330e41aa172c6bd9221`; A creates exactly target-native "
    "`tools/validate_support.py`, `tests/contract/test_support_coordination.py`, and "
    "`tests/contract/test_support_handoff.py` at independently accepted Git objects `40b44057`, "
    "`75bf30a8`, and `0fc854e0`; staged objects matched before commit; nothing pushed | codex\n"
    "support-validated | 2026-07-20T01:46:55Z | LOTO-SLICE-6-A | At clean content commit A, "
    "`python tools/validate_support.py --root . --native-python <target-python> --no-record` exited "
    "0 with coordination passed at 0 errors/0 warnings, bootstrap handoff not-configured, one "
    "support schema parsed, focused contract support tests passed 5/5, and native-optional/hosted-ci "
    "truthfully not-run; direct coordination validation exited 0 and BOARD stayed byte-identical. "
    "The original v1 review found applicable unavailable/unknown states exited 0 and the tracked "
    "digest assumed Git; v2 fails closed for failed/unknown/unavailable, keeps deliberate "
    "passed/skipped/not-run/not-configured non-failing, skips the digest outside Git, and rejects an "
    "enclosing Git root. Missing-native and wrong-support-interpreter probes both exited 1. Native "
    "core-unit, contract, and state-integrity passed 42/42, 30/30, and 3/3, all exit 0; porcelain "
    "remained empty. This validates Slice 6 installation only; milestone aggregate validation, "
    "rollback evidence, guidance alignment, and M4 remain closed | codex\n"
)


STATUS = """# CC_Loto current support status

- Observed at UTC: `2026-07-20T01:46:55Z`
- HEAD: `this status is recorded by evidence commit B, whose parent is validators/tests content commit A 14f0cf2638a26b08c02fccfae353957333bfb8f8`
- Upstream relation: `the two local Slice 6 commits remain unpushed; origin/main remains at published Claude-guidance tip f549b40665c2321ff46168d43c67b2f2f9422bd5`
- Worktree: `clean required at evidence commit B before final-tree validation and reviewer handoff`
- Support milestone: `M3 authorized Loto publication; validators/tests Slice 6 awaits committed-object review; Loto aggregate validation, rollback evidence, and M4 remain closed`
- Product plan reference: `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`

## Active work

- Content commit A adds the target-native [support aggregate](../tools/validate_support.py) and two
  focused modules in the existing contract layer. No product source, dependency, workflow, data,
  model/output, agent-owned guidance, tag, release, or index changes.
- The aggregate runs under the separate support-operator interpreter and invokes the unchanged
  layered `run_tests.py` with an explicit target-native interpreter. It introduces no pytest
  dependency or second discovery mechanism.
- Claude's v1 review found two defects before target write: applicable `unknown`/`unavailable`
  checks could exit 0, and the tracked-digest test assumed the correct Git worktree. Codex accepted
  both. The reviewed v2 fails closed for applicable `failed`, `unknown`, and `unavailable` states;
  deliberate `not-run`, `skipped`, and `not-configured` states remain non-failing. It skips the
  digest outside Git and requires Git top-level to equal the candidate root before `git ls-files`.
- This status and two appended log events form local evidence commit B. Neither A nor B may be
  pushed until Claude independently reviews the committed objects and authorizes the exact
  fast-forward.

## Messages, claims, and blockers

The installed target-local coordination queue remains empty. Cross-agent review occurs through the
Wiki neutral channel. No active product blocker is created by this support-only slice; target push
is gated on Claude's committed-object review.

## Validation state

At clean content commit A, the support aggregate exited `0` with coordination `passed` (0 errors,
0 warnings), bootstrap handoff `not-configured`, one support schema `passed`, and the focused native
contract support pattern `passed` 5/5. Native optional and hosted CI were deliberately not requested
and are `not-run`, not passed. Direct coordination validation exited `0`; `coordination/BOARD.md`
was byte-identical; `--no-record` changed no tracked content.

Fail-closed operator probes reproduced the reviewed corrections: a missing native executable made
the applicable native check `unavailable` and aggregate exit `1`; using the product interpreter as
the support operator made coordination `unavailable` and aggregate exit `1`. A non-Git export ran
five focused tests with only the tracked-digest invariant skipped. A nested enclosing-repository
context is rejected loudly rather than silently hashing the wrong tree.

With output and model-cache paths redirected outside the repository, target-native core-unit,
contract, and state-integrity layers passed 42/42, 30/30, and 3/3, all exit `0`. Optimizer-core,
integration, webapp, and optional layers were not made applicable by this focused support-tool
slice and were **not run**; that is a not-run state, not a pass.

## Guidance pair state

The two agent guidance files remain **not** synchronized. This validators/tests slice neither edits
them nor changes the separate owner-scoped decision about support workflow in `CLAUDE.md`.

## Exact next action

- Owner: `claude-code (independent reviewer), then codex (implementer)`
- Prerequisites: evidence commit B exists; target is clean; `B^ == A`; A changes exactly three
  reviewed paths; B changes exactly two evidence paths; all committed objects match authorities
- Action: independently review local A and B, then authorize or reject one fast-forward containing
  exactly A followed by B
- Stop condition: amended/rebased identity, extra path/commit, byte mismatch, stale board,
  unavailable applicable check returning zero, native regression, target drift, or reviewer finding

## Evidence

- Slice preparation and local validation events in [log.md](log.md)
- Handoff state in [HANDOFF.md](../HANDOFF.md)
- Record classes in [RECORD-KEEPING.md](RECORD-KEEPING.md)
- Native and recovery authority in [PROFILE.md](PROFILE.md)
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-python", required=True)
    return parser.parse_args()


def git_blob(ref: str, path: str) -> bytes:
    result = subprocess.run([
        "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "-C", str(LOTO),
        "show", f"{ref}:{path}",
    ], capture_output=True, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def checked(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise AssertionError(f"command failed {result.returncode}: {' '.join(command)}\n{result.stdout}{result.stderr}")
    return result


args = parse_args()
native_python = str(Path(args.native_python).resolve())

actual_head = checked([
    "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "rev-parse", "HEAD"
], LOTO).stdout.strip()
if actual_head != CONTENT_A:
    raise AssertionError(f"target must be clean at content A; got {actual_head}")
if checked([
    "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "rev-parse", "HEAD^"
], LOTO).stdout.strip() != PARENT:
    raise AssertionError("content A parent drift")
if checked([
    "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "status", "--porcelain"
], LOTO).stdout:
    raise AssertionError("target is dirty before evidence-B render")
for rel, expected in OBJECTS.items():
    actual = checked([
        "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "rev-parse", f"{CONTENT_A}:{rel}"
    ], LOTO).stdout.strip()
    if actual != expected:
        raise AssertionError(f"A object mismatch {rel}: {actual} != {expected}")

a_paths = checked([
    "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "diff-tree",
    "--no-commit-id", "--name-only", "-r", CONTENT_A,
], LOTO).stdout.splitlines()
if set(a_paths) != set(OBJECTS) or len(a_paths) != 3:
    raise AssertionError(f"content A path set mismatch: {a_paths}")

parent_log = git_blob(CONTENT_A, "support/log.md").decode("utf-8")
if "\r" in parent_log or not parent_log.endswith("\n"):
    raise AssertionError("content-A log is not append-safe LF text")
log = parent_log + EVENTS
if not log.startswith(parent_log):
    raise AssertionError("log prefix changed")
added = log.splitlines()[len(parent_log.splitlines()):]
if len(added) != 2 or any(line.count(" | ") < 4 or not line.endswith(" | codex") for line in added):
    raise AssertionError("log append is not exactly two canonical events")

outputs = {"support/log.md": log, "support/current-status.md": STATUS}
errors = []
for rel, content in outputs.items():
    if re.search(r"\{\{[A-Z_]+\}\}", content):
        errors.append(f"{rel}: unresolved placeholder")
    hits = scan_sensitive(content)
    if hits:
        errors.append(f"{rel}: sensitive patterns {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_FIN", "C:/xPY", "C:\\xPY"):
        if token in content:
            errors.append(f"{rel}: forbidden foreign/workspace token {token!r}")
if errors:
    raise AssertionError("\n".join(errors))

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="ls6b-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(LOTO, target, ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"))
    for rel, content in outputs.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    board = target / "coordination/BOARD.md"
    board_before = board.read_bytes()
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime" / "Output")
    env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime" / "ModelCache")
    checked([
        sys.executable, "tools/validate_support.py", "--root", ".",
        "--native-python", native_python, "--no-record",
    ], target, env)
    checked([sys.executable, "tools/support/agent_coord.py", "."], target, env)
    if board.read_bytes() != board_before:
        raise AssertionError("BOARD changed in evidence-B overlay")

    expected = {"core-unit": 42, "contract": 30, "state-integrity": 3}
    for layer, count in expected.items():
        result = checked([
            native_python, "run_tests.py", "--layer", layer,
            "--pattern", "test*.py", "--verbosity", "1",
        ], target, env)
        combined = result.stdout + "\n" + result.stderr
        counts = [int(value) for value in re.findall(r"Ran (\d+) tests?", combined)]
        if counts != [count]:
            raise AssertionError(f"native count mismatch {layer}: {counts}")
        print(f"NATIVE PASSED: {layer} {count}/{count}, exit 0")

out_resolved = OUT.resolve()
if out_resolved.parent != (WIKI / "doc/support-transfer/rendered").resolve():
    raise AssertionError(f"unsafe output path: {out_resolved}")
if OUT.exists():
    shutil.rmtree(OUT)
for rel, content in outputs.items():
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")

actual_paths = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual_paths != set(outputs):
    raise AssertionError(f"inventory mismatch: {sorted(actual_paths)}")
for rel in sorted(outputs):
    print(f"RENDERED {rel} SHA256={hashlib.sha256((OUT / rel).read_bytes()).hexdigest().upper()}")
print("APPEND-ONLY PASSED: published log prefix plus exactly two events")
print("TARGET VALIDATION PASSED: aggregate/coordination 0; BOARD byte-identical; native 42/30/3")
print(f"CONTENT_A={CONTENT_A}")
