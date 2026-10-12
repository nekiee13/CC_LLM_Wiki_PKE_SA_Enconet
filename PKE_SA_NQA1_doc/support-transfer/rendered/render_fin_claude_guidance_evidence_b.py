"""Render and validate the CC_FIN CLAUDE.md evidence-B candidate.

Two modifications of existing support records: append exactly two events to
`support/log.md` and replace `support/current-status.md`. The log is derived
from the committed A blob so the published prefix is preserved by construction.
No CC_FIN file is written by this renderer.
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
OUT = WIKI / "doc/support-transfer/rendered/fin-claude-guidance-evidence-b"
FIN = Path("C:/xPY/xPrj/CC_FIN")
CONTENT_A = "16b8d80eea93231e984a30c61c2fa5c836e80710"
PARENT = "9308e25bbd1177ba69b8075210e1c5e079213fc5"
CLAUDE_OBJECT = "ecaf1abf5e7a7771d72166f17e4bd9c86c92831c"
AGENTS_OBJECT = "4cca3734d8c789038b1142a64be2eec2c5edbccc"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


EVENTS = (
    "support-committed-local | 2026-07-20T21:33:47Z | FIN-CLAUDE-GUIDANCE | Content commit A "
    f"`{CONTENT_A}` was created locally on the published AGENTS-completion parent `{PARENT}` from "
    "Wiki packet commit `35a0a7b0d330bbdce2835b40f960cc47f4c4aa28`; A creates exactly root "
    f"`CLAUDE.md` at the independently reviewed Git object `{CLAUDE_OBJECT}`, 73 additions and 0 "
    "deletions; the staged object was compared to the reviewed authority before commit and matched; "
    f"Codex-owned `AGENTS.md` remains unchanged at `{AGENTS_OBJECT}`; nothing pushed | claude-code\n"
    "support-validated | 2026-07-20T21:34:25Z | FIN-CLAUDE-GUIDANCE-A | At clean A, `python "
    "scripts/agent_coord.py .` exited 0 with 0 errors and 0 warnings and `coordination/BOARD.md` "
    "stayed byte-identical; `python scripts/validate_support.py --no-record` exited 0 with literal "
    "states coordination passed, handoff not-configured, support-schemas passed, native-pytest "
    "passed, optional-cpi not-configured, targeted-ruff not-configured, and hosted-ci not-run - no "
    "unrun or unconfigured layer is represented as passed. The new `CLAUDE.md` pins the check-state "
    "vocabulary to `support/schemas/handoff.schema.json` by reference and states truthfully that "
    "`scripts/validate_support.py` treats only `failed` as failing, so an applicable check it could "
    "not run still exits 0; that aggregate defect is separate owner-facing scope and is not fixed "
    "here. Publication does not establish bilateral guidance alignment | claude-code\n"
)

STATUS = """# CC_FIN current support status

- Observed at UTC: `2026-07-20T21:34:25Z`
- HEAD: `this status is recorded by evidence commit B, whose parent is Claude guidance content \
commit A 16b8d80eea93231e984a30c61c2fa5c836e80710`
- Upstream relation: `the two local guidance commits remain unpushed; origin/main remains at the \
published AGENTS-completion tip 9308e25bbd1177ba69b8075210e1c5e079213fc5`
- Worktree: `clean required at evidence commit B before committed-object review`
- Support milestone: `ADR-SUP-0001 minimal guidance alignment accepted/pending; the Codex-owned \
AGENTS.md completion is published and closed; the Claude-owned CLAUDE.md create awaits \
committed-object review; the pair is not yet aligned`
- Product plan reference: `docs/project/CC_FIN_project_upgrade_plan_enhanced.md`

## Active work

- Content commit A creates root [CLAUDE.md](../CLAUDE.md): 73 additions, 0 deletions, a genuine
  create with no pre-existing byte affected. It exposes the five shared meanings CC_FIN's installed
  `coordination/templates/guidance-semantics.template.md` requires - ownership, support read order,
  coordination lifecycle, validation truth, safe recovery, and non-inferable owner gates - plus a
  short product-orientation section that links existing authorities rather than restating them.
- The check-state vocabulary is referenced from
  [support/schemas/handoff.schema.json](schemas/handoff.schema.json) rather than transcribed.
- `CLAUDE.md` states the current `scripts/validate_support.py` limitation truthfully: it treats only
  `failed` as failing and can emit `unavailable`, so an applicable check it could not run still
  exits 0. The reader is told to read the printed states, not the exit code. This documentation
  slice does not fix that aggregate defect, which is separate owner-facing scope.
- Roles were reversed for this slice: Claude Code authored the Claude-owned file and Codex was the
  independent reviewer, accepting the reparented packet with no finding.
- This status and the appended events form evidence commit B. Neither A nor B is pushed until Codex
  independently reviews the committed objects and explicitly authorizes the push.

## Messages, claims, and blockers

Cross-agent review runs through the Wiki workspace neutral channel. Push is blocked pending Codex's
independent review of local A and B.

## Guidance pair state

The two agent guidance files are **not** aligned by this commit. AGENTS.md carries all five
target-native meanings and CLAUDE.md now exposes them on the Claude side, but publication is a
precondition, not the conclusion: each agent must independently confirm the live shared meanings at
the published tip before any record calls the pair aligned, and ADR-SUP-0001 stays Accepted /
Pending until then.

## Validation state

At content commit A `16b8d80eea93231e984a30c61c2fa5c836e80710`, `python scripts/agent_coord.py .`
exited `0` with 0 errors and 0 warnings and `coordination/BOARD.md` stayed byte-identical.
`python scripts/validate_support.py --no-record` exited `0` with literal states coordination passed,
handoff not-configured, support-schemas passed, native-pytest passed, optional-cpi not-configured,
targeted-ruff not-configured, and hosted-ci not-run. No unrun or unconfigured layer is represented
as passed. Product code, dependencies, tests, and native product runs are outside this
documentation-only create and were not exercised.

## Exact next action

- Owner: `codex (independent reviewer), then claude-code (implementer)`
- Prerequisites: evidence commit B exists; worktree is clean; `B^ == A`; A creates exactly one path
  and B modifies exactly two; committed objects match their reviewed authorities
- Action: independently review local commits A and B, then authorize or reject one fast-forward push
  of exactly A followed by B
- Stop condition: any amended/rebased commit, unexpected path, byte mismatch, stale board,
  coordination error, target drift, premature alignment claim, or reviewer finding

## Evidence

- Slice preparation, local commit, and validation events in [log.md](log.md)
- Handoff state in [HANDOFF.md](../HANDOFF.md)
- Record classes in [RECORD-KEEPING.md](RECORD-KEEPING.md)
- Sensitivity, native-runner, and recovery authority in [PROFILE.md](PROFILE.md)
"""


def parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description=__doc__).parse_args()


def git_blob(ref: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN), "show", f"{ref}:{path}"],
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"cannot read blob {ref}:{path}")
    return result.stdout


def git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN), *args],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr.strip() or "git failed")
    return result.stdout.strip()


parse_args()

# Commit A must be exactly what was reviewed before evidence about it is written.
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
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_Loto", "C:/xPY", "C:\\xPY"):
        if token in text:
            errors.append(f"{rel}: forbidden reference {token!r}")
    for overclaim in ("pair is aligned", "now aligned", "is synchronized", "pair is synchronized"):
        if overclaim in text:
            errors.append(f"{rel}: unauthorized alignment claim {overclaim!r}")
if "**not** aligned by this commit" not in STATUS:
    errors.append("current-status.md: required non-alignment statement missing")
if errors:
    raise AssertionError("\n".join(errors))

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="fcab-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        FIN, target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", ".pytest_cache",
                                      "Output", "ModelCache", ".venv"),
    )
    for rel, text in outputs.items():
        (target / rel).write_text(text, encoding="utf-8", newline="\n")

    if (target / "AGENTS.md").read_bytes() != (FIN / "AGENTS.md").read_bytes():
        raise AssertionError("Codex-owned AGENTS.md must remain untouched")
    if (target / "CLAUDE.md").read_bytes() != (FIN / "CLAUDE.md").read_bytes():
        raise AssertionError("CLAUDE.md content must remain the reviewed A bytes")

    board_before = (target / "coordination/BOARD.md").read_bytes()
    validation = subprocess.run(
        [sys.executable, str(target / "scripts/agent_coord.py"), str(target)],
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
print("TRUTH GUARDS PASSED: no alignment overclaim; non-alignment stated; aggregate limit disclosed")
print("OWNERSHIP PASSED: AGENTS.md and A's CLAUDE.md bytes untouched")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"CONTENT_A={CONTENT_A}")
