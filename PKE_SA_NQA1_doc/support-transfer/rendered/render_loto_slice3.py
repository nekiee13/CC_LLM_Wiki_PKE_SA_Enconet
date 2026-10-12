"""Render and validate the CC_Loto Slice 3 handoff core.

The output is written only after a disposable overlay of the published Slice 2
tree validates. It contains seven creates plus the required generated BOARD.md
modification. No CC_Loto file is written by this renderer.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
TEMPLATES = WIKI / "doc/support-transfer/templates/handoff"
STAGED = WIKI / "doc/support-transfer/staged"
OUT = WIKI / "doc/support-transfer/rendered/loto-slice3"
LOTO = Path("C:/xPY/xPrj/CC_Loto")

sys.path.insert(0, str(STAGED))
from _shared import scan_sensitive  # noqa: E402


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--timestamp", help="fixed UTC BOARD/bootstrap timestamp")
args = parser.parse_args()
if args.timestamp:
    datetime.strptime(args.timestamp, "%Y-%m-%dT%H:%M:%SZ")
NOW = args.timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected one replacement site, found {count}")
    return text.replace(old, new)


publisher = (STAGED / "handoff_publisher.py").read_text(encoding="utf-8")
publisher = re.sub(
    r'\A""".*?"""',
    '"""CC_Loto target-local deterministic handoff publisher.\n\n'
    'Publishes an immutable validated record before atomically replacing HANDOFF.md,\n'
    'then appends a canonical event to support/log.md. Install and import this module\n'
    'from tools/support; all paths resolve beneath the explicit target root. Runtime\n'
    'dependencies are PyYAML and jsonschema in the support-operator environment.\n'
    '"""',
    publisher,
    count=1,
    flags=re.DOTALL,
)
publisher = replace_once(
    publisher,
    "from _shared import scan_sensitive, split_frontmatter",
    "from _support_shared import scan_sensitive, split_frontmatter",
    "installed shared-helper import",
)
publisher = replace_once(
    publisher,
    "# observation about a SHA-1-only pattern is addressed here for the staged\n"
    "# artifact; both targets are SHA-1 today so this has no live effect.",
    "# observation about a SHA-1-only pattern is addressed by this target-local\n"
    "# implementation; SHA-1 and SHA-256 repository formats are both accepted.",
    "target-local SHA format comment",
)
publisher = replace_once(
    publisher,
    '        fh.write(f"{stamp} publish {record.record_id} {record.source_agent} {record.status}\\n")',
    '        fh.write(\n'
    '            f"handoff-published | {stamp} | {record.record_id} | "\n'
    '            f"Immutable handoff published; status {record.status}; "\n'
    '            f"HANDOFF.md updated | {record.source_agent}\\n"\n'
    '        )',
    "target event-log format",
)

pointer = (
    "# Current handoff\n\n"
    "- Record: none published (bootstrap state)\n"
    f"- Bootstrap recorded at UTC: `{NOW}`\n"
    "- Status: `not-configured`\n\n"
    "No immutable handoff record has been published yet. Before continuing work, "
    "inspect the current support status, coordination board, messages, claims, and "
    "Git state. Publish the first validated immutable record with "
    "`tools/support/make_handoff.py`; publication atomically replaces this pointer.\n"
)

handoff_readme = (
    "# Immutable handoff records\n\n"
    "Tracked bootstrap placeholder for validated immutable handoff records created by "
    "`tools/support/make_handoff.py`. No record exists at installation time; `HANDOFF.md` "
    "states that bootstrap condition explicitly and is replaced by the first successful "
    "publication. Never edit a published record in place.\n"
)

continuity = (TEMPLATES / "continuity-checklist.template.md").read_text(encoding="utf-8")
continuity = continuity.replace("{{PROJECT_NAME}}", "CC_Loto")

outputs = {
    "support/schemas/handoff.schema.json": (TEMPLATES / "handoff.schema.json").read_text(encoding="utf-8"),
    "support/templates/handoff-record.template.md": (TEMPLATES / "handoff-record.template.md").read_text(encoding="utf-8"),
    "support/templates/handoff-pointer.template.md": (TEMPLATES / "handoff-pointer.template.md").read_text(encoding="utf-8"),
    "support/templates/continuity-checklist.template.md": continuity,
    "support/handoffs/README.md": handoff_readme,
    "tools/support/make_handoff.py": publisher,
    "HANDOFF.md": pointer,
}

allowed_pointer_placeholders = {
    "HANDOFF_RECORD_ID", "HANDOFF_RECORD_RELATIVE_PATH",
    "HANDOFF_PUBLISHED_AT_UTC", "HANDOFF_SOURCE_AGENT",
    "HANDOFF_STATUS", "HANDOFF_GIT_HEAD",
}
placeholder_re = re.compile(r"\{\{([A-Z_]+)\}\}")
errors: list[str] = []
for rel, content in outputs.items():
    found = set(placeholder_re.findall(content))
    if rel == "support/templates/handoff-pointer.template.md":
        if found != allowed_pointer_placeholders:
            errors.append(f"{rel}: intentional placeholder set mismatch: {sorted(found)}")
    elif found:
        errors.append(f"{rel}: unresolved placeholders {sorted(found)}")
    hits = scan_sensitive(content)
    if hits:
        errors.append(f"{rel}: sensitive patterns {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "xPY", "CC_FIN", "scripts/make_handoff.py"):
        if token in content:
            errors.append(f"{rel}: forbidden cross-target/workspace reference {token!r}")
if errors:
    raise AssertionError("\n".join(errors))

expected_paths = set(outputs) | {"coordination/BOARD.md"}
scratch_base = WIKI / ".tmp" / "loto-slice3-preflight"
scratch_base.mkdir(parents=True, exist_ok=True)
scratch = scratch_base / f"run-{uuid.uuid4().hex}"
target = scratch / "target"
probe = scratch / "probe"
scratch.mkdir()
try:
    for rel in ("support", "coordination"):
        shutil.copytree(LOTO / rel, target / rel)
    (target / "tools").mkdir(parents=True)
    shutil.copytree(LOTO / "tools/support", target / "tools/support")
    for rel, content in outputs.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    board_command = [
        sys.executable, str(target / "tools/support/agent_coord.py"), str(target),
        "--write-board", "--timestamp", NOW,
    ]
    completed = subprocess.run(board_command, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(
            "target validator failed after bootstrap BOARD regeneration\n"
            + completed.stdout + completed.stderr
        )
    board = (target / "coordination/BOARD.md").read_text(encoding="utf-8")
    for required in (
        "- Record: none published (bootstrap state)",
        "- Archive: 0 records in `coordination/archive/`",
        f"Generated: {NOW}",
    ):
        if required not in board:
            raise AssertionError(f"BOARD.md missing required Slice 3 state: {required}")

    shutil.copytree(target, probe)
    sys.path.insert(0, str(probe / "tools/support"))
    spec = importlib.util.spec_from_file_location(
        "loto_slice3_target_make_handoff", probe / "tools/support/make_handoff.py"
    )
    if spec is None or spec.loader is None:
        raise AssertionError("could not load rendered target publisher")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.HandoffRecord(
        record_id="2026-07-19T221000Z-abc1234",
        created_at_utc="2026-07-19T22:10:00Z",
        source_agent="codex",
        status="partial",
        objective="Prove the target-local first-publication lifecycle.",
        checks=[module.Check(name="probe", state="passed", command="probe", exit_code=0,
                             evidence="disposable publication probe passed")],
        git_state=module.GitState(state="absent"),
        next_action=module.NextAction(owner="codex", action="Continue reviewed transfer",
                                      stop_condition="Reviewer finding"),
        artifacts=["support/handoffs/README.md"],
    )
    result = module.publish(probe, record)
    if result.exit_code != 0 or "abc1234" not in result.pointer_path.read_text(encoding="utf-8"):
        raise AssertionError("target publisher did not replace the bootstrap pointer")
    if not result.log_path.read_text(encoding="utf-8").splitlines()[-1].startswith(
        "handoff-published | "
    ):
        raise AssertionError("target publisher did not append the canonical event shape")
    stale = subprocess.run(
        [sys.executable, str(probe / "tools/support/agent_coord.py"), str(probe)],
        text=True, capture_output=True, check=False,
    )
    if stale.returncode == 0 or "BOARD.md is stale" not in (stale.stdout + stale.stderr):
        raise AssertionError("pointer replacement did not fail closed on stale BOARD")
    refreshed = subprocess.run(
        [sys.executable, str(probe / "tools/support/agent_coord.py"), str(probe),
         "--write-board", "--timestamp", NOW],
        text=True, capture_output=True, check=False,
    )
    if refreshed.returncode != 0:
        raise AssertionError("publisher probe did not validate after BOARD regeneration")

    link_re = re.compile(r"\]\(([^)#\s]+)")
    for path in target.rglob("*.md"):
        for link in link_re.findall(path.read_text(encoding="utf-8")):
            if "{{" in link or link.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / link).resolve()
            try:
                resolved.relative_to(target)
            except ValueError:
                errors.append(f"{path.relative_to(target)}: escaping link {link!r}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(target)}: dangling link {link!r}")
    if errors:
        raise AssertionError("\n".join(errors))

    out_resolved = OUT.resolve()
    out_resolved.relative_to(WIKI.resolve())
    if OUT.exists():
        shutil.rmtree(OUT)
    for rel in sorted(expected_paths):
        destination = OUT / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target / rel, destination)
finally:
    shutil.rmtree(scratch, ignore_errors=True)

actual_paths = {
    path.relative_to(OUT).as_posix()
    for path in OUT.rglob("*")
    if path.is_file() and "__pycache__" not in path.parts
}
if actual_paths != expected_paths:
    raise AssertionError(f"inventory mismatch: {sorted(actual_paths)}")

for rel in sorted(expected_paths):
    print("rendered", rel)
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings")
print("PUBLISHER PROBE PASSED: first record -> pointer -> event; stale BOARD -> refreshed")
print("INVENTORY PASSED: 7 creates + 1 generated BOARD modification")
print(f"RENDER_TIMESTAMP={NOW}")
