"""Render and validate the Claude-owned CC_Loto minimal guidance alignment.

Scope is one modification: append a single support-workflow section to
`CLAUDE.md`. The candidate is a pure append to the reviewed parent blob, so
every pre-existing byte is preserved by construction. The check-state
vocabulary is pinned to the installed schema by reference rather than
transcribed, so the defect corrected in Codex step 1 cannot propagate here.
No CC_Loto file is written by this renderer.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/loto-claude-alignment"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
PARENT = "a4ccbe144a2027745e74215e2136dbe6fe610497"
PARENT_CLAUDE_OBJECT = "3edd87504e76a97d8ba46ecf40e81b8ad894299f"
PARENT_AGENTS_OBJECT = "42571a2c5f67b5a11759f38d7d65f50f156087c3"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


SECTION = """
## Support system and coordination

This repository carries a support workflow alongside its product code. The summary below is
deliberately short; the controlling detail lives in [support/README.md](support/README.md),
[support/PROFILE.md](support/PROFILE.md),
[coordination/TEAM_PROTOCOL.md](coordination/TEAM_PROTOCOL.md), and the installed tools under
`tools/support/`. Where this summary and those authorities disagree, the authorities win.

- **Ownership.** Claude Code owns `CLAUDE.md`, `.claude/`, and `CC_` coordination records. Codex
  owns `AGENTS.md`, `.agents/`, and `CX_` records. Read the other agent's files for context, but
  never edit, move, delete, archive, or re-index them; request changes through a coordination
  message. Coordination records without an agent prefix, schemas, templates, validators, the
  generated board, support records, and handoffs are shared-neutral: claim them before editing and
  take independent review.

- **Session start.** For support-oriented work read, in order: this file; `support/README.md` and
  `support/PROFILE.md`; `HANDOFF.md` and its immutable record when one is published;
  `support/current-status.md` and append-only `support/log.md`; `coordination/BOARD.md`, unresolved
  `coordination/messages/`, and active `coordination/claims/`; then live Git state - branch, HEAD,
  upstream, divergence, worktree, and any unfinished risky artifact. Verify that state against the
  records rather than trusting the records.

- **Coordination lifecycle.** Messages are immutable: correct or answer with a new `reply_to`
  record, never by rewriting a sent one. Claims reserve anticipated paths and must not overlap.
  Archive a message only once it is resolved **and** the counterpart has confirmed - silence is not
  confirmation - moving only `CC_` records under an immutable resolution manifest. Use
  `python tools/support/agent_coord.py .` to validate, and regenerate the board through the tool
  rather than hand-editing `coordination/BOARD.md`, which is generated state and never authority.
  When asked to check messages, inspect and independently verify actionable Claude-addressed
  messages in the same turn; never acknowledge acceptance without evidence.

- **Validation truth.** Run the support aggregate as
  `python tools/validate_support.py --root . --native-python <target-interpreter>` and native layers
  as `python run_tests.py --layer <layer>`. The support tools require PyYAML and jsonschema from a
  separate support-operator environment; the product requirements environment does not provide them
  and must not be changed to provide them. Report every check with its literal state from the
  vocabulary defined in [support/schemas/handoff.schema.json](support/schemas/handoff.schema.json) -
  that schema and `tools/validate_support.py` are the authority, not any prose copy of the list.
  `blocked` is a handoff/blocker state, never a check result. An applicable check that could not run
  fails closed; never relabel a skipped, unavailable, not-run, or excluded check as passed, and
  never let a zero exit code stand in for a check that did not execute.

- **Safe recovery.** Capture parent, upstream, divergence, clean state, and allowed paths before any
  reviewed change. Recovery is a new `git revert` of the named commits after reviewer or owner
  direction; reset, force push, history rewriting, and broad cleanup are prohibited. Preserve
  unrelated and concurrent work, then re-run the support and applicable native checks and record
  literal commands and exit codes. A revert that conflicts with later work on the same append-only
  records requires owner-directed resolution.

- **Owner gates.** Milestone gates are the owner's decision and are never inferred from completed
  work, elapsed time, or independent review. Publishing files is not milestone acceptance, and a
  passing support aggregate is evidence about the support system, not about the product test suite.
  Do not describe the two agent guidance files as synchronized unless both sides are published and
  each agent has confirmed its own side at the live tip.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native-python", help="target-requirements interpreter for native layers")
    return parser.parse_args()


def git_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "-C", str(LOTO),
         "show", f"{PARENT}:{path}"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"cannot read parent blob {PARENT}:{path}: "
            + result.stderr.decode("utf-8", errors="replace")
        )
    return result.stdout


def git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "-C", str(LOTO), *args],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


args = parse_args()

# 1. Frozen preconditions.
if git_text("rev-parse", "HEAD") != PARENT:
    raise AssertionError("target HEAD drifted from the reviewed parent")
if git_text("rev-parse", f"{PARENT}:CLAUDE.md") != PARENT_CLAUDE_OBJECT:
    raise AssertionError("parent CLAUDE.md object drifted")
if git_text("rev-parse", f"{PARENT}:AGENTS.md") != PARENT_AGENTS_OBJECT:
    raise AssertionError("parent AGENTS.md object drifted; step 1 must be published and closed")

# 2. Pin the check vocabulary to executable authority rather than transcribing it.
schema = json.loads(git_blob("support/schemas/handoff.schema.json").decode("utf-8"))
# checks[] items are a $ref into $defs; resolve it rather than assuming an inline shape.
checks_items = schema["properties"]["checks"]["items"]
ref = checks_items.get("$ref")
if ref != "#/$defs/check":
    raise AssertionError(f"unexpected checks item shape: {checks_items}")
states = set(schema["$defs"]["check"]["properties"]["state"]["enum"])
expected_states = {"passed", "failed", "skipped", "not-run", "unknown",
                   "not-configured", "unavailable"}
if states != expected_states:
    raise AssertionError(f"installed schema check vocabulary changed: {sorted(states)}")
if "blocked" in states:
    raise AssertionError("schema now admits blocked as a check state; re-review required")

# 3. Derive the candidate as a pure append to the reviewed parent blob.
parent_text = git_blob("CLAUDE.md").decode("utf-8")
if "\r" in parent_text:
    raise AssertionError("parent CLAUDE.md blob is not LF-normalized")
if not parent_text.endswith("\n"):
    raise AssertionError("parent CLAUDE.md does not end with a newline")
if "## Support system and coordination" in parent_text:
    raise AssertionError("support section already present at the reviewed parent")
candidate = parent_text + SECTION

errors: list[str] = []
if not candidate.startswith(parent_text):
    errors.append("candidate is not a pure append to the parent blob")
if candidate[len(parent_text):] != SECTION:
    errors.append("appended bytes differ from the reviewed section")

# 4. The section must reference the authority, never restate a rival enumeration.
if "support/schemas/handoff.schema.json" not in SECTION:
    errors.append("section does not reference the schema as vocabulary authority")
if "`blocked` is a handoff/blocker state, never a check result." not in SECTION:
    errors.append("section omits the blocked-state boundary")
for defective in (
    "passed, failed, skipped, unavailable, blocked",
    "skipped, unavailable, blocked, unknown",
):
    if defective in SECTION:
        errors.append(f"section transcribes a defective enumeration: {defective!r}")
# No literal state list at all: the schema is the single source.
listed = [state for state in sorted(expected_states) if f"`{state}`" in SECTION]
if listed:
    errors.append(f"section enumerates check states instead of referencing the schema: {listed}")

# 5. The section must not claim synchronization, and must say the opposite.
for overclaim in ("pair is synchronized", "guidance is synchronized", "now synchronized",
                  "files are synchronized"):
    if overclaim in candidate:
        errors.append(f"unauthorized synchronization claim: {overclaim!r}")
if "synchronized unless both sides are published" not in SECTION:
    errors.append("section omits the synchronization precondition")

# 6. Pre-existing product guidance must survive untouched.
for anchor in (
    "The project is an installable package; entrypoints live inside it.",
    "pip install -e .",
    "packaged\nwith setuptools as `dynamix-lottery`",
    "**`INDEX_MODE = \"event\"`**",
    "**Leakage safety**",
    "python run_tests.py",
    "`Output/` is generated and gitignored.",
):
    if anchor not in candidate:
        errors.append(f"pre-existing product anchor lost: {anchor!r}")

# 7. Hygiene.
if re.search(r"\{\{[A-Z_]+\}\}", candidate):
    errors.append("unresolved placeholder")
hits = scan_sensitive(candidate)
if hits:
    errors.append(f"sensitive patterns {hits}")
for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_FIN", "C:/xPY", "C:\\xPY"):
    if token in SECTION:
        errors.append(f"forbidden foreign/workspace reference {token!r}")
if errors:
    raise AssertionError("\n".join(errors))

# 8. Disposable overlay: one path, support state inert, links resolve, native layers pass.
temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="lca-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        LOTO, target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"),
    )
    (target / "CLAUDE.md").write_text(candidate, encoding="utf-8", newline="\n")

    if (target / "AGENTS.md").read_bytes() != git_blob("AGENTS.md"):
        raise AssertionError("Codex-owned AGENTS.md must remain untouched by this slice")

    board_before = (target / "coordination/BOARD.md").read_bytes()
    validation = subprocess.run(
        [sys.executable, str(target / "tools/support/agent_coord.py"), str(target)],
        text=True, capture_output=True, check=False,
    )
    if validation.returncode != 0:
        raise AssertionError(
            "alignment overlay failed coordination validation\n"
            + validation.stdout + validation.stderr
        )
    if (target / "coordination/BOARD.md").read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during alignment validation")

    for link in re.findall(r"\]\(([^)#\s]+)", SECTION):
        if link.startswith(("http://", "https://")):
            continue
        resolved = (target / link).resolve()
        try:
            resolved.relative_to(target)
        except ValueError:
            errors.append(f"escaping link {link!r}")
            continue
        if not resolved.exists():
            errors.append(f"dangling link {link!r}")
    if errors:
        raise AssertionError("\n".join(errors))

    if args.native_python:
        native_env = os.environ.copy()
        native_env["PYTHONDONTWRITEBYTECODE"] = "1"
        native_env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime" / "Output")
        native_env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime" / "model_cache")
        for layer, count in {"core-unit": 42, "contract": 30, "state-integrity": 3}.items():
            native = subprocess.run(
                [args.native_python, "run_tests.py", "--layer", layer,
                 "--pattern", "test*.py", "--verbosity", "1"],
                cwd=target, env=native_env, text=True, capture_output=True, check=False,
            )
            combined = native.stdout + "\n" + native.stderr
            counts = [int(value) for value in re.findall(r"Ran (\d+) tests?", combined)]
            if native.returncode != 0 or counts != [count]:
                raise AssertionError(
                    f"native layer {layer} failed: exit={native.returncode}, counts={counts}\n"
                    + combined
                )
            print(f"NATIVE PASSED: {layer} {count}/{count}, exit 0")

out_resolved = OUT.resolve()
if out_resolved.parent != (WIKI / "doc/support-transfer/rendered").resolve():
    raise AssertionError(f"unsafe output path: {out_resolved}")
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
(OUT / "CLAUDE.md").write_text(candidate, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != {"CLAUDE.md"}:
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")

added = len(SECTION.splitlines())
print("rendered CLAUDE.md")
print("INVENTORY PASSED: exactly one Claude-owned modification")
print(f"APPEND-ONLY PASSED: parent preserved byte-for-byte; {added} lines appended")
print("VOCABULARY PASSED: pinned to installed schema by reference; no prose enumeration")
print("OWNERSHIP PASSED: AGENTS.md untouched; no synchronization claim")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"TARGET_PARENT={PARENT}")
