"""Render and validate the CC_FIN target-local baseline-fingerprint migration."""

from __future__ import annotations

import hashlib
import io
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/baseline-fingerprint"
FIN = Path("C:/xPY/xPrj/CC_FIN")
PARENT = "1d61534b81771ae2cd0b8ca5ffa1dd9911712439"
SOURCE = WIKI / "doc/support-transfer/M2_BASELINE_FAILURE_SET.md"
PATHS = (
    "support/BASELINE-FINGERPRINT.md",
    "support/README.md",
    "support/RECORD-KEEPING.md",
)

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


def git_blob(path: str) -> str:
    completed = subprocess.run(
        [
            "git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN),
            "show", f"{PARENT}:{path}",
        ],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"cannot read reviewed parent blob {PARENT}:{path}: "
            + completed.stderr.decode("utf-8", errors="replace")
        )
    return completed.stdout.decode("utf-8")


source = SOURCE.read_text(encoding="utf-8")
contract_at = source.index("## Comparison contract (M2-RR1)")
body = source[contract_at:]
body = body.replace("## Comparison contract (M2-RR1)", "## Comparison contract", 1)
body = body.replace(
    "## Mechanical demonstration of the documented rule (M2-RR3)",
    "## Mechanical demonstration of the documented rule",
    1,
)

baseline = f"""---
record_type: normative_test_baseline_fingerprint
record_id: FIN-BASELINE-238C207
record_class: immutable
version: 1
baseline_commit: 238c207c73970f3d3c6dc00c2db5932ebeca7be4
prepared_from_parent: {PARENT}
---

# CC_FIN normative test baseline fingerprint

This target-local record is the normative non-green test fingerprint captured at CC_FIN
commit `238c207c73970f3d3c6dc00c2db5932ebeca7be4` on 2026-07-18 with Python 3.13.9
(miniconda) and pytest 9.1.1. The like-for-like command was
`PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider
--continue-on-collection-errors`; its JUnit report was written outside the repository.

Totals: **343 tests — 276 passed, 51 failed, 3 collection errors, 13 skipped.**
Classes: 24 `import-unavailable:torch` (21 failures plus 3 collection errors), 11
`import-unavailable:matplotlib`, and 19 `assertion` outcomes.

This record is immutable. A reviewed successor must preserve this record and explain any
intentional baseline change. It is support evidence, not permission to weaken product tests,
install dependencies, change product behavior, or relabel an expected red native run as passed.

{body}"""

readme = git_blob("support/README.md")
readme_anchor = "- [Append-only event log](log.md)\n"
readme_line = "- [Normative test baseline fingerprint](BASELINE-FINGERPRINT.md)\n"
if readme.count(readme_anchor) != 1 or readme_line in readme:
    raise AssertionError("support README insertion anchor drifted or link already exists")
readme_candidate = readme.replace(readme_anchor, readme_anchor + readme_line, 1)

recordkeeping = git_blob("support/RECORD-KEEPING.md")
class_anchor = "| `support/log.md` | Append-only |\n"
class_line = "| `support/BASELINE-FINGERPRINT.md` | Immutable; supersede with a new reviewed record |\n"
if recordkeeping.count(class_anchor) != 1 or class_line in recordkeeping:
    raise AssertionError("record-class insertion anchor drifted or path already exists")
recordkeeping_candidate = recordkeeping.replace(class_anchor, class_anchor + class_line, 1)

candidates = {
    PATHS[0]: baseline,
    PATHS[1]: readme_candidate,
    PATHS[2]: recordkeeping_candidate,
}

rows = re.findall(r"^\| `([^`]+)` \| (failure|error) \| ([^|]+) \| `([^`]+)` \|$", baseline, re.MULTILINE)
if len(rows) != 54:
    raise AssertionError(f"expected 54 normative tuples, found {len(rows)}")
classes = [row[2].strip() for row in rows]
if classes.count("import-unavailable:torch") != 24:
    raise AssertionError("torch tuple count is not 24")
if classes.count("import-unavailable:matplotlib") != 11:
    raise AssertionError("matplotlib tuple count is not 11")
if classes.count("assertion") != 19:
    raise AssertionError("assertion tuple count is not 19")
if len({tuple(row) for row in rows}) != 54 or len({row[0] for row in rows}) != 54:
    raise AssertionError("normative tuple or node IDs are not unique")

errors: list[str] = []
for path, content in candidates.items():
    hits = scan_sensitive(content)
    if hits:
        errors.append(f"{path}: sensitive patterns {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "C:/xPY", "C:\\xPY"):
        if token in content:
            errors.append(f"{path}: forbidden workspace reference {token!r}")
if errors:
    raise AssertionError("\n".join(errors))

archive = subprocess.run(
    [
        "git", "-c", "safe.directory=C:/xPY/xPrj/CC_FIN", "-C", str(FIN),
        "archive", "--format=tar", PARENT,
    ],
    capture_output=True,
    check=False,
)
if archive.returncode != 0:
    raise AssertionError(
        "cannot archive reviewed parent: "
        + archive.stderr.decode("utf-8", errors="replace")
    )

overlay = WIKI / "doc/support-transfer/rendered/.baseline-fingerprint-overlay"
if overlay.exists():
    shutil.rmtree(overlay)
overlay.mkdir(parents=True)
try:
    target = overlay
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as tar:
        tar.extractall(target, filter="data")
    board_path = target / "coordination/BOARD.md"
    board_before = board_path.read_bytes()
    for relative, content in candidates.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    completed = subprocess.run(
        [sys.executable, str(target / "scripts/agent_coord.py"), str(target)],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "baseline-fingerprint overlay failed target coordination validation\n"
            + completed.stdout + completed.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during overlay validation")
    if not (target / "support/BASELINE-FINGERPRINT.md").is_file():
        raise AssertionError("README baseline link target is absent")
finally:
    shutil.rmtree(overlay)

if OUT.exists():
    shutil.rmtree(OUT)
for relative, content in candidates.items():
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != set(PATHS):
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")

for relative in PATHS:
    digest = hashlib.sha256((OUT / relative).read_bytes()).hexdigest().upper()
    print(f"SHA256 {relative} {digest}")
print("INVENTORY PASSED: one immutable record plus two navigation/classification integrations")
print("TUPLE CONTRACT PASSED: 54 unique nodes; 24 torch / 11 matplotlib / 19 assertion")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"TARGET_PARENT={PARENT}")
