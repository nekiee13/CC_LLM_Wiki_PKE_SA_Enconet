"""Render and validate the Claude alignment evidence-B candidate.

Two modifications of existing support records: append exactly two events to
`support/log.md` and replace `support/current-status.md`. The log is derived
from the reviewed commit-A blob so the published prefix is preserved by
construction. No CC_Loto file is written by this renderer.
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
OUT = WIKI / "doc/support-transfer/rendered/loto-claude-alignment-evidence-b"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
CONTENT_A = "843906eb3b01b4154110f089e29f553c7f8b1ca2"
PARENT = "a4ccbe144a2027745e74215e2136dbe6fe610497"
CLAUDE_OBJECT = "689a48b669c009baf79f1349e64f352532a5e444"
AGENTS_OBJECT = "42571a2c5f67b5a11759f38d7d65f50f156087c3"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


EVENTS = (
    "support-committed-local | 2026-07-20T03:42:34Z | LOTO-CLAUDE-GUIDANCE-ALIGNMENT | Content "
    f"commit A `{CONTENT_A}` was created locally on published step-1 parent `{PARENT}` from Wiki "
    "packet commit `37099a1730b81923fa4d2500a9c250d3f228bb21`; A modifies exactly root `CLAUDE.md` "
    f"at the independently reviewed Git object `{CLAUDE_OBJECT}`, appending one support-workflow "
    "section with 55 additions and 0 deletions and changing no pre-existing byte; the staged object "
    "was compared to the reviewed authority before commit and matched; Codex-owned `AGENTS.md` "
    f"remains unchanged at `{AGENTS_OBJECT}`; nothing pushed | claude-code\n"
    "support-validated | 2026-07-20T03:42:49Z | LOTO-CLAUDE-GUIDANCE-ALIGNMENT-A | Using the "
    "separate support-operator interpreter with PyYAML 6.0.3 and jsonschema 4.26.0, `python "
    "tools/validate_support.py --root . --native-python <target-interpreter> --no-record` exited 0 "
    "and `python tools/support/agent_coord.py .` exited 0 with 0 errors and 0 warnings; "
    "`coordination/BOARD.md` remained byte-identical. With output and model-cache directories "
    "redirected outside the repository, `run_tests.py --layer core-unit`, `--layer contract`, and "
    "`--layer state-integrity` (pattern `test*.py`, verbosity 1) exited 0, 0, and 0 with 42/42, "
    "30/30, and 3/3 passing; the worktree stayed clean. The appended section pins the check-state "
    "vocabulary to `support/schemas/handoff.schema.json` and `tools/validate_support.py` by "
    "reference instead of transcribing it, so the enumeration defect corrected in the Codex "
    "guidance step cannot recur here. Publication of this step does not by itself synchronize the "
    "guidance pair | claude-code\n"
)

STATUS = """# CC_Loto current support status

- Observed at UTC: `2026-07-20T03:42:49Z`
- HEAD: `this status is recorded by evidence commit B, whose parent is Claude alignment content \
commit A 843906eb3b01b4154110f089e29f553c7f8b1ca2`
- Upstream relation: `the two local alignment commits remain unpushed; origin/main remains at \
published step-1 tip a4ccbe144a2027745e74215e2136dbe6fe610497`
- Worktree: `clean required at evidence commit B before final-tree validation and reviewer handoff`
- Support milestone: `owner approved minimal guidance alignment; step 1 (Codex AGENTS.md \
vocabulary) is published and closed; step 2 (Claude CLAUDE.md alignment) awaits committed-object \
review; M4 remains closed`
- Product plan reference: `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`

## Active work

- Content commit A appends one `## Support system and coordination` section to Claude-owned
  [CLAUDE.md](../CLAUDE.md): 55 added lines, 0 removed, and no pre-existing byte changed. It covers
  the six owner-approved groups - ownership boundaries, support read order with live-Git preflight,
  the immutable coordination lifecycle, validation truth, revert-first recovery, and owner gates.
- The section references [support/README.md](README.md), [support/PROFILE.md](PROFILE.md),
  [coordination/TEAM_PROTOCOL.md](../coordination/TEAM_PROTOCOL.md), and the installed tools as the
  controlling authorities rather than restating their detail.
- It does not enumerate the check-state vocabulary. It points at
  [support/schemas/handoff.schema.json](schemas/handoff.schema.json) and
  `tools/validate_support.py`, which are the machine-readable authority. The renderer reads that
  schema, resolves its `$defs/check` reference, requires the canonical seven states, and fails if
  the section enumerates them at all.
- Roles were reversed for this slice: Claude Code authored the Claude-owned change and Codex was the
  independent reviewer, accepting the pre-write packet with no findings.
- This status and the appended events form evidence commit B. Neither A nor B is pushed until Codex
  independently reviews the committed objects and explicitly authorizes the push.

## Messages, claims, and blockers

The installed target-local coordination queue remains empty; cross-agent review runs through the
Wiki workspace neutral channel. Push is blocked pending Codex's independent review of local A and B.

## Guidance pair state

The two agent guidance files are **not** synchronized by this commit. Publication of step 2 is a
precondition, not the conclusion: each agent must independently confirm the shared anchors at the
live tip for its own side before any record describes the pair as synchronized. No record may make
that claim earlier.

## Validation state

At content commit A `843906eb3b01b4154110f089e29f553c7f8b1ca2`, the separate support-operator
interpreter provided PyYAML `6.0.3` and jsonschema `4.26.0`; the installed aggregate exited `0` and
`python tools/support/agent_coord.py .` exited `0` with 0 errors and 0 warnings, with
`coordination/BOARD.md` byte-identical. CC_Loto product requirements were not changed and its
product environment is not claimed support-capable.

With output and model-cache directories redirected outside the repository, target-native
`run_tests.py --layer core-unit`, `--layer contract`, and `--layer state-integrity` exited `0`, `0`,
and `0`: 42, 30, and 3 tests passed. Optional, optimization-core, integration, webapp, and hosted-CI
layers were **not run**; a documentation-only guidance change makes no integration applicable. That
is a not-run state, never a pass, and it is not evidence about product-suite health.

## Exact next action

- Owner: `codex (independent reviewer), then claude-code (implementer)`
- Prerequisites: evidence commit B exists; worktree is clean; `B^ == A`; A changes exactly one path
  and B exactly two; committed objects match their reviewed authorities
- Action: independently review local commits A and B, then authorize or reject one fast-forward push
  containing exactly A followed by B
- Stop condition: any amended/rebased commit, unexpected path, byte mismatch, stale board,
  coordination error, native-layer regression, target drift, premature synchronization claim, or
  reviewer finding

## Evidence

- Slice preparation, local commit, review, and validation events in [log.md](log.md)
- Handoff state in [HANDOFF.md](../HANDOFF.md)
- Record classes in [RECORD-KEEPING.md](RECORD-KEEPING.md)
- Sensitivity, native-runner, module, and recovery authority in [PROFILE.md](PROFILE.md)
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native-python", help="target-requirements interpreter")
    return parser.parse_args()


def git_blob(ref: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "-C", str(LOTO),
         "show", f"{ref}:{path}"],
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"cannot read blob {ref}:{path}")
    return result.stdout


def git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "-C", str(LOTO), *args],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr.strip() or "git failed")
    return result.stdout.strip()


args = parse_args()

for path, expected in (("CLAUDE.md", CLAUDE_OBJECT), ("AGENTS.md", AGENTS_OBJECT)):
    actual = git_text("rev-parse", f"{CONTENT_A}:{path}")
    if actual != expected:
        raise AssertionError(f"commit A {path} object {actual} != reviewed {expected}")

parent_log = git_blob(CONTENT_A, "support/log.md").decode("utf-8")
if "\r" in parent_log or not parent_log.endswith("\n"):
    raise AssertionError("parent log is not LF-normalized or lacks a trailing newline")
log = parent_log + EVENTS
if not log.startswith(parent_log):
    raise AssertionError("log candidate does not preserve the published prefix")
appended = log.splitlines()[len(parent_log.splitlines()):]
if len(appended) != 2:
    raise AssertionError(f"expected exactly two appended events, got {len(appended)}")
for line in appended:
    if line.count(" | ") < 4 or not line.endswith(" | claude-code"):
        raise AssertionError(f"appended event breaks the pipe-delimited contract: {line!r}")

outputs = {"support/log.md": log, "support/current-status.md": STATUS}

errors: list[str] = []
for rel, text in outputs.items():
    if re.search(r"\{\{[A-Z_]+\}\}", text):
        errors.append(f"{rel}: unresolved placeholder")
    hits = scan_sensitive(text)
    if hits:
        errors.append(f"{rel}: sensitive patterns {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_FIN", "C:/xPY", "C:\\xPY"):
        if token in text:
            errors.append(f"{rel}: forbidden reference {token!r}")
    for overclaim in ("pair is synchronized", "now synchronized", "files are synchronized",
                      "guidance is synchronized"):
        if overclaim in text:
            errors.append(f"{rel}: unauthorized synchronization claim {overclaim!r}")
if "**not** synchronized by this commit" not in STATUS:
    errors.append("current-status.md: required non-synchronization statement missing")
if errors:
    raise AssertionError("\n".join(errors))

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="lcab-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        LOTO, target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"),
    )
    for rel, text in outputs.items():
        (target / rel).write_text(text, encoding="utf-8", newline="\n")

    if (target / "AGENTS.md").read_bytes() != git_blob(CONTENT_A, "AGENTS.md"):
        raise AssertionError("Codex-owned AGENTS.md must remain untouched")

    board_before = (target / "coordination/BOARD.md").read_bytes()
    validation = subprocess.run(
        [sys.executable, str(target / "tools/support/agent_coord.py"), str(target)],
        text=True, capture_output=True, check=False,
    )
    if validation.returncode != 0:
        raise AssertionError("evidence-B overlay failed coordination validation\n"
                             + validation.stdout + validation.stderr)
    if (target / "coordination/BOARD.md").read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during evidence-B validation")

    for link in re.findall(r"\]\(([^)#\s]+)", STATUS):
        if link.startswith(("http://", "https://")):
            continue
        resolved = (target / "support" / link).resolve()
        try:
            resolved.relative_to(target)
        except ValueError:
            errors.append(f"current-status.md: escaping link {link!r}")
            continue
        if not resolved.exists():
            errors.append(f"current-status.md: dangling link {link!r}")
    if errors:
        raise AssertionError("\n".join(errors))

    if args.native_python:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime" / "Output")
        env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime" / "model_cache")
        for layer, count in {"core-unit": 42, "contract": 30, "state-integrity": 3}.items():
            native = subprocess.run(
                [args.native_python, "run_tests.py", "--layer", layer,
                 "--pattern", "test*.py", "--verbosity", "1"],
                cwd=target, env=env, text=True, capture_output=True, check=False,
            )
            combined = native.stdout + "\n" + native.stderr
            counts = [int(v) for v in re.findall(r"Ran (\d+) tests?", combined)]
            if native.returncode != 0 or counts != [count]:
                raise AssertionError(f"native layer {layer} failed: exit={native.returncode}")
            print(f"NATIVE PASSED: {layer} {count}/{count}, exit 0")

if OUT.resolve().parent != (WIKI / "doc/support-transfer/rendered").resolve():
    raise AssertionError("unsafe output path")
if OUT.exists():
    shutil.rmtree(OUT)
for rel, text in outputs.items():
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

actual_paths = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual_paths != set(outputs):
    raise AssertionError(f"inventory mismatch: {sorted(actual_paths)}")

for rel in sorted(outputs):
    print("rendered", rel)
print("APPEND-ONLY PASSED: published log prefix preserved; exactly two events appended")
print("TRUTH GUARDS PASSED: no synchronization overclaim; precondition stated explicitly")
print("OWNERSHIP PASSED: AGENTS.md untouched")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"CONTENT_A={CONTENT_A}")
