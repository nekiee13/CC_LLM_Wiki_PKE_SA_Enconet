"""Render and validate the CC_Loto guidance-correction evidence-B candidate.

Scope is two modifications of existing support records: append exactly two
events to `support/log.md` and replace `support/current-status.md`. The log is
derived from the reviewed commit-A blob so the published prefix is preserved by
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
OUT = WIKI / "doc/support-transfer/rendered/loto-cc-guidance-evidence-b"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
CONTENT_A = "416691248cb4f69586ddd483a942c56e5be60cf6"
PARENT = "fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e"
CLAUDE_OBJECT = "3edd87504e76a97d8ba46ecf40e81b8ad894299f"
AGENTS_OBJECT = "34b7eb93095022bea137e2a0c2313f356bfa0f28"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


EVENTS = (
    "support-committed-local | 2026-07-20T00:55:07Z | LOTO-CC-GUIDANCE | Content commit A "
    f"`{CONTENT_A}` was created locally on published Slice 5 parent `{PARENT}` from Wiki packet "
    "commit `5a50210af395d34341ef55022f57541e8b56c3f1`; A modifies exactly root `CLAUDE.md` at the "
    f"independently reviewed Git object `{CLAUDE_OBJECT}`, with 3 additions and 2 deletions "
    "confined to the opening paragraph and no other line changed; the staged object was compared "
    "to the reviewed authority before commit and matched; Codex-owned `AGENTS.md` remains "
    f"unchanged at `{AGENTS_OBJECT}`; nothing pushed | claude-code\n"
    "support-validated | 2026-07-20T00:56:12Z | LOTO-CC-GUIDANCE-A | Using the separate "
    "support-operator interpreter with PyYAML 6.0.3 and jsonschema 4.26.0, `python "
    "tools/support/agent_coord.py .` exited 0 with 0 errors and 0 warnings and "
    "`coordination/BOARD.md` remained byte-identical. With `$env:PYTHONDONTWRITEBYTECODE='1'` and "
    "output/model-cache directories redirected outside the repository, `run_tests.py --layer "
    "core-unit`, `--layer contract`, and `--layer state-integrity` (pattern `test*.py`, verbosity "
    "1) exited 0, 0, and 0 with 42/42, 25/25, and 3/3 passing (70/70 total); the worktree stayed "
    "clean. The corrected sentence replaces a false no-packaging/no-requirements claim with the "
    "verified setuptools `dynamix-lottery` / Python `>=3.11` / `requirements.txt` and "
    "`requirements.lock` facts, each asserted against the reviewed parent blobs before rendering. "
    "This correction does NOT synchronize the guidance pair: `AGENTS.md` carries support "
    "read-order, ownership, validation-truth, recovery, and gate anchors that `CLAUDE.md` does "
    "not, and closing that asymmetry remains a separate owner-scoped slice | claude-code\n"
)

STATUS = """# CC_Loto current support status

- Observed at UTC: `2026-07-20T00:56:12Z`
- HEAD: `this status is recorded by evidence commit B, whose parent is guidance-correction content \
commit A 416691248cb4f69586ddd483a942c56e5be60cf6`
- Upstream relation: `the two local guidance-correction commits remain unpushed; origin/main \
remains at published Slice 5 tip fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e`
- Worktree: `clean required at evidence commit B before final-tree validation and reviewer handoff`
- Support milestone: `M3 authorized Loto publication; Slices 1, 2, 3, 3c, and 5 are published and \
closed; this Claude-owned guidance correction awaits committed-object review; M4 remains closed`
- Product plan reference: `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`

## Active work

- Content commit A modifies exactly root [CLAUDE.md](../CLAUDE.md), replacing a stale sentence that
  claimed `sys.path` bootstrapping and no packaging or requirements file. The replacement states the
  verified facts: the project is packaged with setuptools as `dynamix-lottery`, targets Python
  `>=3.11`, is normally used as an editable install, and takes `requirements.txt` and
  `requirements.lock` as dependency authorities.
- The stale sentence also contradicted the same file's own later sections, which already described
  an installable package and prohibited reintroducing per-file `sys.path.insert` bootstrapping. The
  correction removes that internal contradiction and preserves those sections unchanged.
- Roles were reversed for this slice: Claude Code authored the Claude-owned change and Codex was the
  independent reviewer. Codex accepted the pre-write packet with no findings and did not edit any
  Claude-owned file.
- This status and the appended events form evidence commit B. Neither A nor B is pushed until Codex
  independently reviews the committed objects and explicitly authorizes the push.
- Validators/tests, aggregate validation, rollback evidence, and the M4 decision remain later
  separately gated work.

## Messages, claims, and blockers

The installed target-local coordination queue remains empty; cross-agent review is conducted through
the Wiki workspace neutral channel. Push is blocked pending Codex's independent review of local A
and B.

## Guidance pair state

The two agent guidance files are **not** synchronized, and this correction does not make them so.
Codex-owned `AGENTS.md` carries support read-order, ownership, literal validation-state, recovery,
and owner-gate anchors; Claude-owned `CLAUDE.md` remains a product-development guidance file that
carries none of them. Whether `CLAUDE.md` should carry support workflow at all is an owner-scoped
decision and belongs to a separate briefed and reviewed slice. No record may report the pair as
synchronized until that work exists and both agents confirm their own side.

## Validation state

At content commit A `416691248cb4f69586ddd483a942c56e5be60cf6`, the separate support-operator
interpreter provided PyYAML `6.0.3` and jsonschema `4.26.0`; `python tools/support/agent_coord.py .`
exited `0` with 0 errors and 0 warnings, and `coordination/BOARD.md` remained byte-identical.
CC_Loto product requirements were not changed and its product environment is not claimed
support-capable.

With output and model-cache directories redirected outside the repository, target-native commands
`python run_tests.py --layer core-unit --pattern test*.py --verbosity 1`, `python run_tests.py
--layer contract --pattern test*.py --verbosity 1`, and `python run_tests.py --layer
state-integrity --pattern test*.py --verbosity 1` exited `0`, `0`, and `0`: 42, 25, and 3 tests
passed (70/70). Optional, optimizer, integration, and webapp layers were not made applicable by a
documentation-only change and were **not run**; that is a not-run state, not a pass. The committed
`CLAUDE.md` object matches the reviewed authority, and `AGENTS.md` is unchanged.

## Exact next action

- Owner: `codex (independent reviewer), then claude-code (implementer)`
- Prerequisites: evidence commit B exists; worktree is clean; `B^ == A`; A changes exactly one path
  and B exactly two; committed objects match their reviewed authorities
- Action: independently review local commits A and B, then authorize or reject one fast-forward push
  containing exactly A followed by B
- Stop condition: any amended/rebased commit, unexpected path, byte mismatch, stale board,
  coordination error, native-layer regression, target drift, synchronization overclaim, or reviewer
  finding

## Evidence

- Slice preparation, local commit, review, and validation events in [log.md](log.md)
- Handoff state in [HANDOFF.md](../HANDOFF.md)
- Record classes in [RECORD-KEEPING.md](RECORD-KEEPING.md)
- Sensitivity, native-runner, module, and recovery authority in [PROFILE.md](PROFILE.md)
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--native-python",
        help="optional target-requirements interpreter for disposable native validation",
    )
    return parser.parse_args()


def git_blob(ref: str, path: str) -> bytes:
    result = subprocess.run(
        [
            "git",
            "-c",
            "safe.directory=C:/xPY/xPrj/CC_Loto",
            "-C",
            str(LOTO),
            "show",
            f"{ref}:{path}",
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"cannot read blob {ref}:{path}: " + result.stderr.decode("utf-8", errors="replace")
        )
    return result.stdout


args = parse_args()

# Commit A must be exactly what was reviewed before evidence about it is written.
for path, expected in (("CLAUDE.md", CLAUDE_OBJECT), ("AGENTS.md", AGENTS_OBJECT)):
    actual = subprocess.run(
        [
            "git",
            "-c",
            "safe.directory=C:/xPY/xPrj/CC_Loto",
            "-C",
            str(LOTO),
            "rev-parse",
            f"{CONTENT_A}:{path}",
        ],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    if actual != expected:
        raise AssertionError(f"commit A {path} object {actual} != reviewed {expected}")

parent_log = git_blob(CONTENT_A, "support/log.md").decode("utf-8")
if "\r" in parent_log:
    raise AssertionError("parent log blob is not LF-normalized; re-review required")
if not parent_log.endswith("\n"):
    raise AssertionError("parent log does not end with a newline; append would corrupt the record")
log = parent_log + EVENTS

# Append-only, proven rather than asserted.
if not log.startswith(parent_log):
    raise AssertionError("log candidate does not preserve the published prefix")
added_lines = log.splitlines()[len(parent_log.splitlines()) :]
if len(added_lines) != 2:
    raise AssertionError(f"expected exactly two appended events, got {len(added_lines)}")
for line in added_lines:
    if line.count(" | ") < 4 or not line.endswith(" | claude-code"):
        raise AssertionError(f"appended event does not match the pipe-delimited contract: {line!r}")

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
            errors.append(f"{rel}: forbidden foreign/workspace reference {token!r}")
    # Truthfulness guards specific to this slice.
    for overclaim in ("pair is synchronized", "guidance is synchronized", "now synchronized"):
        if overclaim in text:
            errors.append(f"{rel}: unauthorized synchronization claim {overclaim!r}")
if "**not** synchronized" not in STATUS:
    errors.append("current-status.md: required non-synchronization statement missing")
if errors:
    raise AssertionError("\n".join(errors))

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="lccb-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        LOTO,
        target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"),
    )
    for rel, text in outputs.items():
        (target / rel).write_text(text, encoding="utf-8", newline="\n")

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
            "evidence-B overlay failed target coordination validation\n"
            + validation.stdout
            + validation.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during evidence-B validation")

    link_re = re.compile(r"\]\(([^)#\s]+)")
    for link in link_re.findall(STATUS):
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
        native_env = os.environ.copy()
        native_env["PYTHONDONTWRITEBYTECODE"] = "1"
        native_env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime" / "Output")
        native_env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime" / "ModelCache")
        for layer, expected_count in {"core-unit": 42, "contract": 25, "state-integrity": 3}.items():
            native = subprocess.run(
                [args.native_python, "run_tests.py", "--layer", layer,
                 "--pattern", "test*.py", "--verbosity", "1"],
                cwd=target, env=native_env, text=True, capture_output=True, check=False,
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
if out_resolved.parent != (WIKI / "doc/support-transfer/rendered").resolve():
    raise AssertionError(f"unsafe output path: {out_resolved}")
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
print("TRUTH GUARDS PASSED: no synchronization overclaim; non-synchronization stated explicitly")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"CONTENT_A={CONTENT_A}")
