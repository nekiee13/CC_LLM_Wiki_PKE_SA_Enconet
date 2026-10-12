"""Render the reviewed CC_FIN ADR-SUP-0001 alignment-activation records.

This renderer writes only a Wiki-side byte authority. It never writes CC_FIN.
The target change is four shared-neutral records: ADR, register, current status,
and one append-only event. AGENTS.md and CLAUDE.md are immutable preconditions.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
FIN = Path("C:/xPY/xPrj/CC_FIN")
OUT = WIKI / "doc/support-transfer/rendered/fin-guidance-alignment-activation"
PARENT = "41e8dccf8262ca06da24eed66d3ec4ee03e94bd2"
AGENTS_OBJECT = "4cca3734d8c789038b1142a64be2eec2c5edbccc"
CLAUDE_OBJECT = "ecaf1abf5e7a7771d72166f17e4bd9c86c92831c"
CONFIRMED_AT = "2026-07-20T21:53:15Z"
CODEX_CONFIRMATION = (
    "CX_2026-07-20T214930Z_fin-claude-guidance-live-closure-and-codex-anchor-confirmation"
)
CLAUDE_CONFIRMATION = (
    "CC_2026-07-20T215315Z_fin-claude-guidance-closed-and-claude-anchor-confirmation"
)


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN), *args],
        capture_output=True,
        check=False,
    )


def git_text(*args: str) -> str:
    result = git(*args)
    if result.returncode != 0:
        raise AssertionError(result.stderr.decode("utf-8", "replace").strip() or "git failed")
    return result.stdout.decode("utf-8").strip()


def blob(path: str) -> bytes:
    result = git("show", f"{PARENT}:{path}")
    if result.returncode != 0:
        raise AssertionError(f"cannot read {PARENT}:{path}")
    return result.stdout


def confirmation_path(message_id: str) -> Path:
    for folder in (WIKI / "Enconet/coordination/messages", WIKI / "Enconet/coordination/archive"):
        candidate = folder / f"{message_id}.md"
        if candidate.is_file():
            return candidate
    raise AssertionError(f"confirmation record is missing: {message_id}")


if git_text("rev-parse", "HEAD") != PARENT:
    raise AssertionError("target HEAD drifted from the reviewed parent")
if git_text("rev-parse", "origin/main") != PARENT:
    raise AssertionError("target origin/main drifted from the reviewed parent")
if git_text("status", "--porcelain"):
    raise AssertionError("target worktree is not clean")
if git_text("rev-parse", f"{PARENT}:AGENTS.md") != AGENTS_OBJECT:
    raise AssertionError("live AGENTS.md object changed")
if git_text("rev-parse", f"{PARENT}:CLAUDE.md") != CLAUDE_OBJECT:
    raise AssertionError("live CLAUDE.md object changed")

codex_confirmation = confirmation_path(CODEX_CONFIRMATION).read_text(encoding="utf-8")
claude_confirmation = confirmation_path(CLAUDE_CONFIRMATION).read_text(encoding="utf-8")
if "five target-native meanings" not in codex_confirmation:
    raise AssertionError("Codex own-side confirmation is incomplete")
if "All five meanings" not in claude_confirmation:
    raise AssertionError("Claude own-side confirmation is incomplete")
if "NOT declaring the pair aligned" not in claude_confirmation:
    raise AssertionError("Claude confirmation does not preserve the shared-record gate")

adr_path = "support/decisions/ADR-SUP-0001-minimal-guidance-alignment.md"
register_path = "support/decisions/README.md"
status_path = "support/current-status.md"
log_path = "support/log.md"

adr = blob(adr_path).decode("utf-8")
old_frontmatter = "implementation_state: pending\n"
new_frontmatter = (
    "implementation_state: complete\n"
    f"implementation_completed_at_utc: {CONFIRMED_AT}\n"
    f"implementation_tip: {PARENT}\n"
)
if adr.count(old_frontmatter) != 1:
    raise AssertionError("ADR implementation-state anchor changed")
adr = adr.replace(old_frontmatter, new_frontmatter, 1)

old_boundary = "- Decision state is **Accepted**; implementation state is **Pending**."
new_boundary = "- Decision state is **Accepted**; implementation state is **Complete**."
if adr.count(old_boundary) != 1:
    raise AssertionError("ADR implementation-boundary anchor changed")
adr = adr.replace(old_boundary, new_boundary, 1)

completion = f"""## Implementation completion

At live tip `{PARENT}`, both agent-owned guidance files are published and each owner independently
confirmed its own file against the live Git object:

- Codex confirmed `AGENTS.md` object `{AGENTS_OBJECT}` and all five target-native meanings in
  `{CODEX_CONFIRMATION}`.
- Claude Code confirmed `CLAUDE.md` object `{CLAUDE_OBJECT}` and all five target-native meanings in
  `{CLAUDE_CONFIRMATION}`.

Those two confirmations satisfy the decision's bilateral precondition. The guidance pair is
minimally aligned in shared meaning at the implementation tip; agent-specific wording and product
guidance remain intentionally distinct. This completion establishes guidance semantics only. It is
not evidence that the product test suite is green, and it does not fix or close the separate
`scripts/validate_support.py` fail-open defect for applicable `unknown` or `unavailable` results.

"""
evidence_anchor = "## Evidence\n"
if adr.count(evidence_anchor) != 1:
    raise AssertionError("ADR evidence anchor changed")
adr = adr.replace(evidence_anchor, completion + evidence_anchor, 1)

register = blob(register_path).decode("utf-8")
old_row = (
    "| ADR-SUP-0001 | Minimal dual-agent guidance alignment | Accepted | Pending | — | "
    "[Decision](ADR-SUP-0001-minimal-guidance-alignment.md) |"
)
new_row = (
    "| ADR-SUP-0001 | Minimal dual-agent guidance alignment | Accepted | Complete | — | "
    "[Decision](ADR-SUP-0001-minimal-guidance-alignment.md) |"
)
if register.count(old_row) != 1:
    raise AssertionError("decision-register row changed")
register = register.replace(old_row, new_row, 1)

parent_log = blob(log_path).decode("utf-8")
if not parent_log.endswith("\n"):
    raise AssertionError("parent log lacks final newline")
event = (
    f"support-alignment-confirmed | {CONFIRMED_AT} | ADR-SUP-0001 | At live tip `{PARENT}`, "
    f"Codex confirmed live AGENTS.md object `{AGENTS_OBJECT}` and Claude Code confirmed live "
    f"CLAUDE.md object `{CLAUDE_OBJECT}`; each confirmation independently verified all five "
    "target-native guidance meanings and neither agent-owned record declared alignment; this "
    "shared-neutral activation records implementation complete while preserving the separate "
    "validate_support.py fail-open owner item and making no product-suite health claim | codex\n"
)
log = parent_log + event

status = f"""# CC_FIN current support status

- Observed at UTC: `{CONFIRMED_AT}`
- HEAD: `this status is recorded by the ADR-SUP-0001 activation commit whose reviewed parent is {PARENT}`
- Upstream relation: `read live Git state; this record does not substitute for HEAD/origin/divergence checks`
- Worktree: `clean required before and after the reviewed activation commit`
- Support milestone: `ADR-SUP-0001 decision accepted and implementation complete: both live guidance files carry the five target-native shared meanings and both owners independently confirmed their own side`
- Product plan reference: `docs/project/CC_FIN_project_upgrade_plan_enhanced.md`

## Completed guidance alignment

- Codex-owned `AGENTS.md` is live at object `{AGENTS_OBJECT}` and Codex confirmed its support read
  order, ownership, literal validation truth, scoped recovery, and non-inferable owner gates in
  `{CODEX_CONFIRMATION}`.
- Claude-owned `CLAUDE.md` is live at object `{CLAUDE_OBJECT}` and Claude Code confirmed the same
  five meanings on its side in `{CLAUDE_CONFIRMATION}`.
- ADR-SUP-0001 records minimal semantic alignment, not byte identity. Agent-specific wording and
  product guidance remain intentionally distinct.

## Messages, claims, and blockers

The immutable cross-agent evidence is retained in the Wiki coordination archive. This activation
has its own exact render, pre-write review, committed-object review, publication check, and scoped
revert path. No agent-owned guidance file changes in the activation commit.

## Validation state

At published guidance tip `{PARENT}`, `python scripts/agent_coord.py .` exited `0` with 0 errors and
0 warnings and `python scripts/validate_support.py --no-record` exited `0` with literal states:
coordination passed, handoff not-configured, support-schemas passed, native-pytest passed,
optional-cpi not-configured, targeted-ruff not-configured, and hosted-ci not-run. The activation is
record-only and must repeat these proportional support checks; broader product layers are not run
and are not represented as passed.

## Separate owner-facing item

`scripts/validate_support.py` still treats only `failed` as failing while it can emit `unknown` or
`unavailable`, so an applicable check it could not execute may still leave aggregate exit code `0`.
The printed states remain authoritative. ADR-SUP-0001 completion does not fix or close this defect.

## Exact next action

- Owner: `codex (implementer), then claude-code (independent reviewer)`
- Action: apply the reviewed four-path activation authority, validate, commit locally, obtain
  committed-object review, push only on authorization, then verify the live tip
- Stop condition: any guidance-file change, log-prefix mutation, object mismatch, alignment claim
  without both confirmations, product-health overclaim, validation mutation, or reviewer finding

## Evidence

- Decision: [ADR-SUP-0001](decisions/ADR-SUP-0001-minimal-guidance-alignment.md)
- Decision register: [support decisions](decisions/README.md)
- Append-only events: [log.md](log.md)
- Guidance: [`../AGENTS.md`](../AGENTS.md), [`../CLAUDE.md`](../CLAUDE.md)
"""

outputs = {
    adr_path: adr,
    register_path: register,
    status_path: status,
    log_path: log,
}

if not log.startswith(parent_log) or len(log.splitlines()) != len(parent_log.splitlines()) + 1:
    raise AssertionError("log is not the exact parent plus one event")
if event.count("|") != 4:
    raise AssertionError("activation event breaks the pipe-delimited contract")
if "implementation_state: complete" not in adr or "implementation state is **Complete**" not in adr:
    raise AssertionError("ADR is not internally complete")
if "| Accepted | Complete |" not in register:
    raise AssertionError("register is not internally complete")
for text in outputs.values():
    if "product test suite is green" in text and "not evidence" not in text:
        raise AssertionError("product-health overclaim")
    if "fail-open defect" not in (adr + status + log):
        raise AssertionError("separate validator defect disclosure missing")
for foreign in ("CC_Loto", "tools/support/", "run_tests.py", "--native-python"):
    if any(foreign in text for text in outputs.values()):
        raise AssertionError(f"foreign target reference: {foreign}")

if OUT.resolve().parent != (WIKI / "doc/support-transfer/rendered").resolve():
    raise AssertionError("unsafe output path")
if OUT.exists():
    shutil.rmtree(OUT)
for rel, text in outputs.items():
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != set(outputs):
    raise AssertionError(f"output inventory mismatch: {sorted(actual)}")

for rel in sorted(outputs):
    data = (OUT / rel).read_bytes()
    blob_result = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True)
    print(f"{rel} sha256={hashlib.sha256(data).hexdigest().upper()} object={blob_result.stdout.decode().strip()} bytes={len(data)}")
print("INVENTORY PASSED: four shared-neutral records; no guidance file")
print("CONFIRMATIONS PASSED: both own-side records and live objects pinned")
print("APPEND-ONLY PASSED: log is exact parent plus one event")
print("TRUTH PASSED: product layers not claimed; fail-open defect remains separate")
print(f"TARGET_PARENT={PARENT}")
