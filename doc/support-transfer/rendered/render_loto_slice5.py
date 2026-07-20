"""Render and validate the Codex-owned CC_Loto Slice-5 guidance candidate."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/loto-slice5"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
PARENT = "85f97d0a75a996e83691d2b103d9724cb3136653"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


GUIDANCE = """# CC_Loto Codex Guidance

## Scope and authority

These instructions govern Codex work in this repository. The human owner controls milestone
decisions, authority changes, destructive recovery, hosted settings, tags, releases, and product
scope. The owner-designated product authority is `docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md`; the root
`README.md`, architecture/current-state documents, `PROGRESS.md`, `ROADMAP.md`, CI, and the native
test runner retain their distinct scopes. Support records link those authorities and do not replace
or silently reinterpret them.

The enhanced plan retains its `Proposed` document header. Earlier TDD-plan progress does not prove
completion of the enhanced plan. Always inspect current Git and product evidence instead of relying
on copied status text.

## Ownership boundary

- Codex owns `AGENTS.md`, `.agents/`, Codex configuration/indexes, and `CX_` coordination records.
- Claude Code owns `CLAUDE.md`, `.claude/`, Claude configuration/indexes, and `CC_` coordination
  records. Codex may read them for shared context but must not edit, move, delete, archive, or
  re-index them.
- `coordination/`, shared support records, schemas, templates, validators, and handoffs are neutral
  by contract. Use immutable messages and claims; never rewrite a sent message.
- Repo-local workflow skills are disabled initially. Do not create `.agents/` content unless a
  later owner-approved, separately reviewed slice enables it.
- When Codex changes its own side of a dual-agent contract, record Claude synchronization as
  pending; never claim both sides are synchronized without Claude's confirmation.

## Session start and coordination

For support-oriented work, read in order:

1. this `AGENTS.md` and any nearer nested Codex guidance;
2. `support/README.md` and `support/PROFILE.md`;
3. `HANDOFF.md` and its immutable record when one is published;
4. `support/current-status.md` and the append-only `support/log.md`;
5. `coordination/BOARD.md`, unresolved `coordination/messages/`, and active
   `coordination/claims/`;
6. live Git branch, HEAD/upstream/divergence, worktree state, and unfinished risky artifacts.

Use `python tools/support/agent_coord.py .` for read-only coordination validation. Use the installed
tool's claim, message, release, and status operations rather than hand-editing generated
`coordination/BOARD.md`. Keep only unresolved communication active. Once resolution is confirmed,
create an immutable resolution manifest and archive only Codex-owned `CX_` records; ask Claude Code
to archive its own `CC_` records.

When the owner asks to check messages, inspect and independently verify actionable Codex-addressed
messages in the same turn. Never acknowledge acceptance without evidence. Preserve the complete
immutable message lifecycle and regenerate/validate the board after coordination state changes.

## Repository and product boundaries

- Project: DynaMix Lottery Forecasting System, an installable Python package with `dynamix` under
  `src/` and `opt` at repository root. Root entrypoint files are thin shims.
- Packaging authority: `pyproject.toml` defines setuptools package `dynamix-lottery` version
  `0.1.0`, Python `>=3.11`, mixed discovery under `src` and `.`, and optional dependency groups.
  Runtime/locked dependency authorities are `requirements.txt` and `requirements.lock`.
- `DATA.csv` is tracked product input. Do not expose its content in support records or indexes;
  cite only path and SHA-256 when identity evidence is explicitly required.
- Do not modify controlled product data, model/output artifacts, StatGrid, plots, caches, generated
  results, dependencies, hosted configuration, product plans, or architecture scope unless the
  owner explicitly places that change in the task.
- Documentation/code indexes remain deferred. Do not create or refresh an external index/corpus
  without a later owner-approved claim and exact exclusion review.

## Native commands and validation truth

Install the package from repository authority when setup is required:

```bash
python -m pip install -e .
```

Use the repository's layered `unittest` runner, not pytest:

```bash
python run_tests.py
python run_tests.py --layer core-unit --pattern test*.py --verbosity 1
python run_tests.py --layer contract --pattern test*.py --verbosity 1
python run_tests.py --layer state-integrity --pattern test*.py --verbosity 1
python run_tests.py --include-optional
```

The optional layer and heavy model families are not required unless the task makes them applicable.
Missing optional dependencies must remain fail-soft where the product contract says so. Report each
check literally as passed, failed, skipped, unavailable, blocked, unknown, or not run; never relabel
a missing, timed-out, or excluded check as passed. Redirect output and model-cache paths outside the
repository for support-only validation when practical.

The support operator requires PyYAML and jsonschema. The separately accepted support environment
may run `tools/support/agent_coord.py`; this does not imply that the product-requirements
environment contains those packages, and support publication must not silently add them to product
dependencies.

## Git workflow and safe recovery

This is a single-owner repository. Prefer small direct commits on `main`; use a pull request only
when the owner requests one or an external constraint requires it. Cross-agent review occurs through
immutable coordination messages and committed evidence. Before every reviewed slice, capture the
exact parent, upstream, divergence, clean state, allowed paths, and rollback scope.

Do not discard local commits or working-tree changes as routine synchronization. On divergence or
recovery work, stop writes and first capture:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git log --oneline --decorate --graph -n 20
```

Identify the exact commits and paths at risk, active claims/messages, intended recovery point, and
preservation evidence. Prefer fast-forward synchronization, preserving work on a named branch, or a
reviewed `git revert` of identified commits. Destructive discard, force push, recursive deletion,
history rewriting, or broad cleanup requires explicit owner approval naming the target, recovery
point, backup/preservation evidence, validation commands, and stop conditions. After approved
recovery, rerun Git, support, and applicable native checks and record literal commands and exits.

## Working rules

- Inspect actual files and Git state before trusting paths or status copied from another machine.
- Keep changes minimal and preserve unrelated work in a dirty tree. Stop if an overlapping change
  cannot be safely separated.
- Use target-native `tools/` placement and `run_tests.py` semantics; do not import FIN paths,
  pytest assumptions, Wiki runtime dependencies, or machine-private paths.
- Treat `docs/context/`, historical exports, examples, stale AS-IS snapshots, and proposed plans as
  non-authoritative unless a current controlled document promotes a requirement from them.
- Never report a validation as passed when it was skipped, blocked, unavailable, or not run.
- Before publishing support changes, require exact committed-object review and clean live-tip
  closure. Recovery is revert-only unless the owner explicitly approves another named operation.
- M4 cannot be inferred from completed slices. Aggregate validation, rollback evidence,
  independent review, and the owner's explicit decision remain separate gates.

## Completion checklist

Before handing off a change:

1. verify exact Git identity, path scope, and worktree state;
2. run coordination validation and the proportional native layers;
3. confirm no product-data/output/cache or cross-agent-owned path entered the change;
4. record literal commands, integer exits, unavailable checks, blockers, and recovery scope;
5. update only the appropriate replaceable/append-only support records;
6. use `python tools/support/make_handoff.py` when publishing an operational handoff, and verify the
   resulting pointer, immutable record, event, and generated board lifecycle;
7. keep owner gates and later slices closed unless their explicit evidence and decisions exist.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", required=True, help="reviewed UTC ISO-8601 timestamp")
    parser.add_argument(
        "--native-python",
        help="optional target-requirements interpreter for disposable native validation",
    )
    return parser.parse_args()


def checked_timestamp(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise AssertionError("--timestamp must be UTC")
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")


args = parse_args()
render_timestamp = checked_timestamp(args.timestamp)

completed = subprocess.run(
    [
        "git",
        "-c",
        "safe.directory=C:/xPY/xPrj/CC_Loto",
        "-C",
        str(LOTO),
        "cat-file",
        "-e",
        f"{PARENT}^{{commit}}",
    ],
    check=False,
)
if completed.returncode != 0:
    raise AssertionError("reviewed parent commit is unavailable")


def git_blob(path: str) -> bytes:
    result = subprocess.run(
        [
            "git",
            "-c",
            "safe.directory=C:/xPY/xPrj/CC_Loto",
            "-C",
            str(LOTO),
            "show",
            f"{PARENT}:{path}",
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"cannot read reviewed parent blob {PARENT}:{path}: "
            + result.stderr.decode("utf-8", errors="replace")
        )
    return result.stdout


pyproject = tomllib.loads(git_blob("pyproject.toml").decode("utf-8"))
if pyproject.get("build-system", {}).get("build-backend") != "setuptools.build_meta":
    raise AssertionError("reviewed parent setuptools backend drifted")
project = pyproject.get("project", {})
if (
    project.get("name") != "dynamix-lottery"
    or project.get("version") != "0.1.0"
    or project.get("requires-python") != ">=3.11"
):
    raise AssertionError("reviewed parent packaging identity drifted")
where = pyproject.get("tool", {}).get("setuptools", {}).get("packages", {}).get("find", {}).get("where")
if where != ["src", "."]:
    raise AssertionError("reviewed parent mixed package-discovery fact drifted")

runner = git_blob("run_tests.py").decode("utf-8")
for required in ("unittest", '"core-unit"', '"contract"', '"state-integrity"', '"optional"'):
    if required not in runner:
        raise AssertionError(f"reviewed parent native runner missing {required!r}")

profile = git_blob("support/PROFILE.md").decode("utf-8")
for required in (
    "Documentation/code indexes | Deferred",
    "Repo-local workflow skills | Disabled initially",
    "Release adapter | Inventory only",
):
    if required not in profile:
        raise AssertionError(f"reviewed support profile missing state {required!r}")

parent_agents = subprocess.run(
    [
        "git",
        "-c",
        "safe.directory=C:/xPY/xPrj/CC_Loto",
        "-C",
        str(LOTO),
        "cat-file",
        "-e",
        f"{PARENT}:AGENTS.md",
    ],
    capture_output=True,
    check=False,
)
if parent_agents.returncode == 0:
    raise AssertionError("AGENTS.md already exists at the reviewed parent")

errors: list[str] = []
if re.search(r"\{\{[A-Z_]+\}\}", GUIDANCE):
    errors.append("AGENTS.md: unresolved placeholder")
hits = scan_sensitive(GUIDANCE)
if hits:
    errors.append(f"AGENTS.md: sensitive patterns {hits}")
for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_FIN", "C:/xPY", "C:\\xPY"):
    if token in GUIDANCE:
        errors.append(f"AGENTS.md: forbidden foreign/workspace reference {token!r}")
for prohibited in (
    "python -m pytest",
    "git reset --hard",
    "python scripts/agent_coord.py",
    "no packaging or `requirements.txt`",
):
    if prohibited in GUIDANCE:
        errors.append(f"AGENTS.md: prohibited or stale guidance {prohibited!r}")
for required in (
    "support/README.md",
    "HANDOFF.md",
    "support/current-status.md",
    "support/log.md",
    "coordination/BOARD.md",
    "coordination/messages/",
    "coordination/claims/",
    "python tools/support/agent_coord.py .",
    "python run_tests.py",
    "reviewed `git revert`",
    "explicit owner approval",
    "passed, failed, skipped, unavailable, blocked, unknown, or not run",
    "M4 cannot be inferred",
):
    if required not in GUIDANCE:
        errors.append(f"AGENTS.md: semantic anchor missing {required!r}")
if errors:
    raise AssertionError("\n".join(errors))

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="l5-", dir=temp_root) as tmp:
    target = Path(tmp) / "repo"
    shutil.copytree(
        LOTO,
        target,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"),
    )
    (target / "AGENTS.md").write_text(GUIDANCE, encoding="utf-8", newline="\n")

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
            "Slice-5 overlay failed target coordination validation\n"
            + validation.stdout
            + validation.stderr
        )
    if board_path.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during Slice-5 validation")

    for rel in (
        "support/README.md",
        "support/PROFILE.md",
        "HANDOFF.md",
        "support/current-status.md",
        "support/log.md",
        "coordination/BOARD.md",
        "coordination/TEAM_PROTOCOL.md",
        "tools/support/agent_coord.py",
        "tools/support/make_handoff.py",
        "docs/CC_Loto_ENHANCED_UPGRADE_PLAN.md",
        "requirements.txt",
        "requirements.lock",
    ):
        if not (target / rel).is_file():
            raise AssertionError(f"guidance target missing in overlay: {rel}")

    if args.native_python:
        native_env = os.environ.copy()
        native_env["PYTHONDONTWRITEBYTECODE"] = "1"
        native_env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime" / "Output")
        native_env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime" / "ModelCache")
        expected = {"core-unit": 42, "contract": 25, "state-integrity": 3}
        for layer, expected_count in expected.items():
            native = subprocess.run(
                [
                    args.native_python,
                    "run_tests.py",
                    "--layer",
                    layer,
                    "--pattern",
                    "test*.py",
                    "--verbosity",
                    "1",
                ],
                cwd=target,
                env=native_env,
                text=True,
                capture_output=True,
                check=False,
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
expected_parent = (WIKI / "doc/support-transfer/rendered").resolve()
if out_resolved.parent != expected_parent:
    raise AssertionError(f"unsafe output path: {out_resolved}")
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
(OUT / "AGENTS.md").write_text(GUIDANCE, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != {"AGENTS.md"}:
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")

print("rendered AGENTS.md")
print("INVENTORY PASSED: exactly one Codex-owned create")
print("TARGET FACTS PASSED: setuptools dynamix-lottery 0.1.0, Python >=3.11, native unittest layers")
print("SEMANTIC ANCHORS PASSED: read-order, ownership, validation, recovery, gates")
print("TARGET VALIDATION PASSED: 0 errors, 0 warnings; BOARD byte-identical")
print(f"RENDER_TIMESTAMP={render_timestamp}")
print(f"TARGET_PARENT={PARENT}")
