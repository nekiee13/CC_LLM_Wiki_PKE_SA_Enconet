"""Render and validate the CC_FIN slice-3c index-closure tree."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
TEMPLATE = WIKI / "doc/support-transfer/templates/support-index.template.md"
SLICE2 = WIKI / "doc/support-transfer/rendered/slice2"
SLICE3 = WIKI / "doc/support-transfer/rendered/slice3"
OUT = WIKI / "doc/support-transfer/rendered/slice3c"
FIN = Path("C:/xPY/xPrj/CC_FIN")
PARENT = "ea41c2a6ddb9906ede272a9003ddddf212c5b80a"
DOCS_LINK = (
    "- [Support system](../support/README.md) — repo-local governance, "
    "coordination, and handoff core"
)

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


ownership = (
    "The human project owner approves gates, authority changes, destructive recovery, "
    "hosted-governance changes, tags, releases, and publication. Codex owns `AGENTS.md`, "
    "`.agents/`, and `CX_` records. Claude Code owns `CLAUDE.md`, `.claude/`, and `CC_` "
    "records. Coordination, support records, handoffs, schemas, templates, validators, "
    "and generated views are shared-neutral by contract. Each agent may inspect but "
    "must not edit or archive the other agent's owned infrastructure."
)

authorities = """- Enhanced implementation plan: [CC_FIN project upgrade plan](../docs/project/CC_FIN_project_upgrade_plan_enhanced.md)
- Project documentation index: [project documents](../docs/project/README.md)
- Architecture and current-state authority: [AS-IS](../docs/project/AS-IS.md)
- Documentation freshness authority: [freshness ledger](../docs/documentation_freshness_ledger.md)
- Existing feature decisions: [integration-pilot ADR register](../docs/integration-pilot/adr/README.md)
- Hosted workflows and forms: [pull-request template](../.github/pull_request_template.md), [M5 expansion exception issue form](../.github/ISSUE_TEMPLATE/m5-expansion-exception.yml), [follow-up ML gate](../.github/workflows/followup-ml-gate.yml), [label bootstrap](../.github/workflows/followup-ml-label-bootstrap.yml), and [scope governance](../.github/workflows/followup-ml-scope-governance.yml)
- Packaging authorities: [pyproject.toml](../pyproject.toml), [runtime requirements](../requirements.txt), and [test requirements](../requirements.test.txt)
- Release/package status: release adapter is **inventory-only**; remote tag inventory is empty and no release record is present. Creating a tag or release is outside this transfer."""

values = {
    "PROJECT_NAME": "CC_FIN",
    "PRODUCT_PLAN_PATH": "docs/project/CC_FIN_project_upgrade_plan_enhanced.md",
    "PRODUCT_DOC_INDEX_PATH": "docs/README.md",
    "SUPPORT_PROFILE_PATH": "support/PROFILE.md",
    "REPOSITORY_URL": "https://github.com/nekiee13/CC_FIN",
    "DEFAULT_BRANCH": "main",
    "AGENT_OWNERSHIP_SUMMARY": ownership,
    "TARGET_DECISION_AUTHORITIES": authorities,
    "NATIVE_VALIDATION_COMMAND": (
        "$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest; run Ruff only where "
        "already applicable and CPI only when its prerequisites exist and CPI behavior changes"
    ),
    "DATA_EXCLUSION_SUMMARY": (
        "secrets and private paths; datasets, spreadsheets, vendor/archive trees, "
        "generated outputs, caches, debug material, model artifacts, and prohibited "
        "product data per [PROFILE.md](PROFILE.md)"
    ),
}

support_index = TEMPLATE.read_text(encoding="utf-8")
for key, value in values.items():
    token = "{{" + key + "}}"
    if support_index.count(token) != 1:
        raise AssertionError(f"support template token {token} not found exactly once")
    support_index = support_index.replace(token, value)

docs_readme = git_blob("docs/README.md")
if DOCS_LINK in docs_readme:
    raise AssertionError("docs/README.md already contains the authorized support link")
anchor = "- Governance transition and trunk operations: `docs/governance-transition.md`"
if docs_readme.count(anchor) != 1:
    raise AssertionError("docs/README.md insertion anchor not found exactly once")
docs_rendered = docs_readme.replace(anchor, anchor + "\n" + DOCS_LINK)

outputs = {
    "support/README.md": support_index,
    "docs/README.md": docs_rendered,
}

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
if errors:
    raise AssertionError("\n".join(errors))

# The existing-file diff is exactly the one approved added line.
before_lines = docs_readme.splitlines()
after_lines = docs_rendered.splitlines()
added = [line for line in after_lines if line not in before_lines]
if added != [DOCS_LINK] or len(after_lines) != len(before_lines) + 1:
    raise AssertionError(f"docs/README.md diff is not exactly the approved line: {added}")

with tempfile.TemporaryDirectory(prefix="slice3c-render-") as tmp:
    target = Path(tmp) / "target"
    shutil.copytree(SLICE2, target)
    for path in SLICE3.rglob("*"):
        if path.is_file():
            rel = path.relative_to(SLICE3)
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
            "two-path Slice-3c overlay changed BOARD inputs or failed validation\n"
            + completed.stdout
            + completed.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during Slice-3c validation")

    link_re = re.compile(r"\]\(([^)#\s]+)")
    for rel, text in outputs.items():
        path = target / rel
        for link in link_re.findall(text):
            if link.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / link).resolve()
            try:
                target_rel = resolved.relative_to(target)
            except ValueError:
                errors.append(f"{rel}: escaping link {link!r}")
                continue
            if not resolved.exists() and not (FIN / target_rel).exists():
                errors.append(f"{rel}: dangling link {link!r}")
    if errors:
        raise AssertionError("\n".join(errors))

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
print("INVENTORY PASSED: 1 create + 1 one-line modification")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print("LINK/PLACEHOLDER/SENSITIVITY CHECKS PASSED")
print(f"TARGET_PARENT={PARENT}")
