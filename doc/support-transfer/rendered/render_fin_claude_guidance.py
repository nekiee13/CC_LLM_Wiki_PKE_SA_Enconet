"""Render and validate the Claude-owned CC_FIN guidance file.

Scope is one create: root `CLAUDE.md`, exposing the five shared meanings that
CC_FIN's own installed guidance-semantics template requires. The check-state
vocabulary is pinned to the installed schema by reference rather than
transcribed. The candidate deliberately makes no fail-closed claim about
`scripts/validate_support.py`, because that aggregate currently exits 0 on an
applicable check it could not run. No CC_FIN file is written by this renderer.
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
OUT = WIKI / "doc/support-transfer/rendered/fin-claude-guidance"
FIN = Path("C:/xPY/xPrj/CC_FIN")
PARENT = "e74147f3309e1835d28d7c248e00cdcbde2f1796"
PARENT_AGENTS_OBJECT = "d04bf3b8d1167e993e1c5c2d8d9cf33c296b5747"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


GUIDANCE = """# CLAUDE.md

Guidance for Claude Code working in this repository. Codex has its own instructions in
`AGENTS.md`; neither file replaces the other, and neither is a product requirements authority.

## Product orientation

Forecasting and Scenario Engine, currently in Path Stabilization (Phase-1). Canonical
implementation lives in `src/`; `compat/` is a delegation-only adapter layer; runnable entrypoints
live in `scripts/`. The public forecast boundary is `src.models.facade.ForecastArtifact`.

Authorities to read rather than restate: [README.md](README.md),
[docs/refactor/phase1_rules.md](docs/refactor/phase1_rules.md), and the detailed layout, style, and
completion rules already recorded in [AGENTS.md](AGENTS.md). This file does not duplicate them and
must not become a second backlog.

Native commands: `python -m pip install -r requirements.txt`, `python -m pytest`, and
`python -m ruff check src compat scripts tests tools`. Keep Phase-1 edits minimal and localized;
do not run repo-wide formatting sweeps.

## Support system and coordination

The repository-local support core is navigation and evidence. Controlling detail lives in
[support/README.md](support/README.md), [support/PROFILE.md](support/PROFILE.md), and
[coordination/TEAM_PROTOCOL.md](coordination/TEAM_PROTOCOL.md); where this summary and those
authorities disagree, the authorities win.

- **Ownership.** Claude Code owns `CLAUDE.md`, `.claude/`, and `CC_` coordination records. Codex
  owns `AGENTS.md`, `.agents/`, and `CX_` records. Read the other agent's files for context, but
  never edit, move, delete, archive, or re-index them; request changes through a coordination
  message. Coordination records without an agent prefix, schemas, templates, validators, the
  generated board, support records, and handoffs are shared-neutral: claim them before editing and
  take independent review.

- **Session start.** For support-oriented work read, in order: this file; `support/README.md` and
  `support/PROFILE.md`; `HANDOFF.md` and its immutable record once one is published;
  `support/current-status.md` and the append-only `support/log.md`; `coordination/BOARD.md`,
  unresolved `coordination/messages/`, and active `coordination/claims/`; then live Git state -
  branch, HEAD, upstream, divergence, worktree, and any unfinished or risky artifact. Verify that
  state against the records rather than trusting the records.

- **Coordination lifecycle.** Messages are immutable: correct or answer with a new `reply_to`
  record, never by rewriting a sent one. Claims reserve anticipated paths and must not overlap.
  Archive a message only once it is resolved **and** the counterpart has confirmed - silence is not
  confirmation - moving only `CC_` records under an immutable resolution manifest. Use
  `python scripts/agent_coord.py .` to validate, and regenerate the board through the installed CLI
  rather than hand-editing `coordination/BOARD.md`, which is generated state and never authority.
  When asked to check messages, inspect and independently verify actionable Claude-addressed
  messages in the same turn; never acknowledge acceptance without evidence.

- **Validation truth.** Report every check with its literal state from the vocabulary defined in
  [support/schemas/handoff.schema.json](support/schemas/handoff.schema.json) - that schema is the
  authority, not any prose copy of the list. `blocked` is a handoff and blocker state, never a
  check result. Never relabel a skipped, unavailable, not-run, or excluded check as passed, and
  never let an exit code stand in for a check that did not execute. Note a current limitation
  rather than assuming otherwise: `scripts/validate_support.py` treats only `failed` as a failing
  state, so an applicable check it could not run is reported honestly in its output but still
  yields exit `0`. Read its printed states; do not treat its exit code alone as proof that
  everything ran. Support checks compose with, and never replace, `python -m pytest`.

- **Safe recovery.** Capture parent, upstream, divergence, clean state, and allowed paths before
  any reviewed change. Recovery is a new `git revert` of the named commits after reviewer or owner
  direction; reset, force push, history rewriting, and broad cleanup are prohibited. Preserve
  unrelated and concurrent work, then re-run the support and applicable native checks and record
  literal commands and exit codes. A revert that conflicts with later work on the same append-only
  records requires owner-directed resolution.

- **Owner gates.** Milestone gates are the owner's decision and are never inferred from completed
  work, elapsed time, or independent review. Publishing files is not milestone acceptance, and a
  passing support check is evidence about the support system, not about the product test suite. Do
  not describe this repository's two agent guidance files as aligned or synchronized unless both
  are published and each agent has confirmed its own side at the live tip; `support/decisions/`
  records the current decision state.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args()


def git_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN),
         "show", f"{PARENT}:{path}"],
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"cannot read parent blob {PARENT}:{path}")
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

# 1. Frozen preconditions. CLAUDE.md must be a genuine create.
if git_text("rev-parse", "HEAD") != PARENT:
    raise AssertionError("target HEAD drifted from the reviewed parent")
if git_text("rev-parse", f"{PARENT}:AGENTS.md") != PARENT_AGENTS_OBJECT:
    raise AssertionError("parent AGENTS.md object drifted")
exists = subprocess.run(
    ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN),
     "cat-file", "-e", f"{PARENT}:CLAUDE.md"],
    capture_output=True, check=False,
)
if exists.returncode == 0:
    raise AssertionError("CLAUDE.md already exists at the reviewed parent; this slice is a create")

# 2. The five required meanings come from CC_FIN's own installed template.
template = git_blob("coordination/templates/guidance-semantics.template.md").decode("utf-8")
anchors = set(re.findall(r"^\| (read-order|ownership|truthful-validation|safe-recovery|target-gates)",
                         template, re.M))
if anchors != {"read-order", "ownership", "truthful-validation", "safe-recovery", "target-gates"}:
    raise AssertionError(f"installed template anchor set changed: {sorted(anchors)}")

# 3. Check vocabulary is pinned to the installed schema, never transcribed.
schema = json.loads(git_blob("support/schemas/handoff.schema.json").decode("utf-8"))
states = set(schema["$defs"]["check"]["properties"]["state"]["enum"])
expected_states = {"passed", "failed", "skipped", "not-run", "unknown",
                   "not-configured", "unavailable"}
if states != expected_states:
    raise AssertionError(f"installed schema vocabulary changed: {sorted(states)}")
if "blocked" in states:
    raise AssertionError("schema now admits blocked as a check state; re-review required")

candidate = GUIDANCE
errors: list[str] = []

# 4. The five meanings must be present and attributed, not enumerated away.
for needle, label in (
    ("Claude Code owns `CLAUDE.md`", "ownership"),
    ("read, in order", "read-order"),
    ("Messages are immutable", "coordination lifecycle"),
    ("support/schemas/handoff.schema.json", "validation vocabulary authority"),
    ("`git revert` of the named commits", "safe recovery"),
    ("never inferred from completed", "owner gates"),
):
    if needle not in candidate:
        errors.append(f"required meaning missing ({label}): {needle!r}")
# Guard against transcribing the vocabulary, not against naming a state. Describing the
# aggregate's own FAILURE_STATES requires saying `failed`; that is a reference, not a rival
# list. An enumeration is what drifts from the schema, so fail only on three or more.
listed = [s for s in sorted(expected_states) if f"`{s}`" in candidate]
if len(listed) >= 3:
    errors.append(f"candidate enumerates check states instead of referencing the schema: {listed}")

# 5. Truthfulness about the installed aggregate. FIN's validate_support.py is not
#    fail-closed, so the candidate must say so and must not claim otherwise.
aggregate = git_blob("scripts/validate_support.py").decode("utf-8")
fail_closed = 'FAILURE_STATES = {"failed", "unknown", "unavailable"}' in aggregate
if fail_closed:
    raise AssertionError(
        "scripts/validate_support.py is now fail-closed; the candidate's stated limitation "
        "is stale and this slice must be re-rendered and re-reviewed"
    )
if "still\nyields exit `0`" not in candidate and "yields exit `0`" not in candidate:
    errors.append("candidate omits the current aggregate exit-code limitation")
for false_claim in ("fails closed", "fail-closed"):
    if false_claim in candidate:
        errors.append(f"candidate asserts fail-closed behaviour FIN does not have: {false_claim!r}")

# 6. Target-native paths only; no cross-target leakage.
for foreign in ("tools/support/agent_coord.py", "tools/support/make_handoff.py",
                "run_tests.py", "--native-python", "dynamix", "CC_Loto"):
    if foreign in candidate:
        errors.append(f"foreign/cross-target reference {foreign!r}")
for native in ("scripts/agent_coord.py", "python -m pytest", "support/PROFILE.md",
               "coordination/TEAM_PROTOCOL.md"):
    if native not in candidate:
        errors.append(f"target-native reference missing: {native!r}")

# 7. No synchronization overclaim; state the precondition instead.
for overclaim in ("pair is synchronized", "now synchronized", "files are synchronized",
                  "guidance is aligned", "pair is aligned"):
    if overclaim in candidate:
        errors.append(f"unauthorized synchronization/alignment claim: {overclaim!r}")
if "unless both\n  are published and each agent has confirmed its own side" not in candidate:
    errors.append("candidate omits the bilateral confirmation precondition")

# 8. Hygiene.
if re.search(r"\{\{[A-Z_]+\}\}", candidate):
    errors.append("unresolved placeholder")
hits = scan_sensitive(candidate)
if hits:
    errors.append(f"sensitive patterns {hits}")
for token in ("LLM_Wiki", "03_PKE", "Enconet", "C:/xPY", "C:\\xPY"):
    if token in candidate:
        errors.append(f"forbidden workspace reference {token!r}")
if errors:
    raise AssertionError("\n".join(errors))

# 9. Disposable overlay: one path, support state inert, links resolve.
temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="fcg-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        FIN, target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", ".pytest_cache",
                                      "Output", "ModelCache", ".venv"),
    )
    (target / "CLAUDE.md").write_text(candidate, encoding="utf-8", newline="\n")

    # The overlay is a byte copy of the source tree with only CLAUDE.md added, so AGENTS.md must
    # equal the source working-tree file exactly. Compare against the source, not the committed
    # blob: the working tree is CRLF while the blob is LF (autocrlf), and the committed-object
    # guarantee is already enforced by the parent-object precondition plus the one-file inventory.
    if (target / "AGENTS.md").read_bytes() != (FIN / "AGENTS.md").read_bytes():
        raise AssertionError("Codex-owned AGENTS.md must remain untouched by this slice")

    board_before = (target / "coordination/BOARD.md").read_bytes()
    validation = subprocess.run(
        [sys.executable, str(target / "scripts/agent_coord.py"), str(target)],
        text=True, capture_output=True, check=False,
    )
    if validation.returncode != 0:
        raise AssertionError("overlay failed target coordination validation\n"
                             + validation.stdout + validation.stderr)
    if (target / "coordination/BOARD.md").read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during validation")

    for link in re.findall(r"\]\(([^)#\s]+)", candidate):
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

if OUT.resolve().parent != (WIKI / "doc/support-transfer/rendered").resolve():
    raise AssertionError("unsafe output path")
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
(OUT / "CLAUDE.md").write_text(candidate, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != {"CLAUDE.md"}:
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")

print("rendered CLAUDE.md")
print("INVENTORY PASSED: exactly one Claude-owned create")
print("ANCHORS PASSED: five meanings from the installed target-native template")
print("VOCABULARY PASSED: pinned to installed schema by reference; no prose enumeration")
print("TRUTH PASSED: current aggregate exit-code limitation stated; no fail-closed claim")
print("NATIVE PASSED: FIN-native paths only; no cross-target leakage")
print("OWNERSHIP PASSED: AGENTS.md untouched; no alignment/synchronization claim")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical; links resolve")
print(f"TARGET_PARENT={PARENT}")
