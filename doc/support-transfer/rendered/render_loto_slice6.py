"""Render and validate the CC_Loto Slice 6 validators/tests candidate.

The candidate adds one target-native support aggregate and two focused unittest
modules in the existing contract layer. No CC_Loto file is written.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


WIKI = Path(__file__).resolve().parents[3]
OUT = WIKI / "doc/support-transfer/rendered/loto-slice6"
LOTO = Path("C:/xPY/xPrj/CC_Loto")
PARENT = "f549b40665c2321ff46168d43c67b2f2f9422bd5"

sys.path.insert(0, str(WIKI / "doc/support-transfer/staged"))
from _shared import scan_sensitive  # noqa: E402


AGGREGATE = r'''"""Deterministic CC_Loto support validation aggregate.

Run support checks in the support-operator environment and compose them with
the existing layered unittest runner. The runner is read-only; ``--no-record``
explicitly guarantees that no validation history is written.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

STATES = {"passed", "failed", "skipped", "not-run", "unknown",
          "not-configured", "unavailable"}
FAILURE_STATES = {"failed", "unknown", "unavailable"}


@dataclass(frozen=True)
class CheckResult:
    name: str
    state: str
    detail: str

    def __post_init__(self) -> None:
        if self.state not in STATES:
            raise ValueError(f"invalid check state: {self.state}")


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _run(command: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(command, cwd=root, env=env, text=True,
                          capture_output=True, check=False)


def _command_result(name: str, command: list[str], root: Path,
                    runner: Callable = _run) -> CheckResult:
    try:
        result = runner(command, root)
    except FileNotFoundError as exc:
        return CheckResult(name, "unavailable", str(exc))
    state = "passed" if result.returncode == 0 else "failed"
    detail = f"exit={result.returncode}; command={' '.join(command)}"
    return CheckResult(name, state, detail)


def check_coordination(root: Path) -> CheckResult:
    try:
        support_tools = root / "tools" / "support"
        sys.path.insert(0, str(support_tools))
        module = _load("cc_loto_agent_coord", support_tools / "agent_coord.py")
        result = module.validate(root)
    except (OSError, ImportError, ModuleNotFoundError) as exc:
        return CheckResult("coordination", "unavailable", str(exc))
    return CheckResult("coordination", "passed" if result.ok else "failed",
                       f"errors={len(result.errors)}; warnings={len(result.warnings)}")


def check_handoff(root: Path) -> CheckResult:
    pointer = root / "HANDOFF.md"
    if not pointer.is_file():
        return CheckResult("handoff", "not-configured", "HANDOFF.md is absent")
    text = pointer.read_text(encoding="utf-8")
    if "Record: none published (bootstrap state)" in text:
        return CheckResult("handoff", "not-configured", "bootstrap pointer; no record published")
    match = re.search(r"support/handoffs/[0-9A-Za-z_.-]+\.md", text)
    if not match:
        return CheckResult("handoff", "failed", "pointer does not name an immutable record")
    record_path = root / match.group(0)
    if not record_path.is_file():
        return CheckResult("handoff", "failed", f"missing record: {match.group(0)}")
    try:
        support_tools = root / "tools" / "support"
        sys.path.insert(0, str(support_tools))
        module = _load("cc_loto_make_handoff", support_tools / "make_handoff.py")
        errors = module.validate_record(module.parse_record(record_path.read_text(encoding="utf-8")))
    except (OSError, ValueError, ImportError, ModuleNotFoundError) as exc:
        return CheckResult("handoff", "failed", str(exc))
    return CheckResult("handoff", "failed" if errors else "passed",
                       f"validation_errors={len(errors)}")


def check_support_schemas(root: Path) -> CheckResult:
    schemas = sorted((root / "support" / "schemas").glob("*.json"))
    if not schemas:
        return CheckResult("support-schemas", "not-configured", "no support schemas")
    try:
        for path in schemas:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError(f"{path.name} is not a JSON object")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return CheckResult("support-schemas", "failed", str(exc))
    return CheckResult("support-schemas", "passed", f"parsed={len(schemas)}")


def run_checks(root: Path, *, native_python: str | None = None,
               runner: Callable | None = None) -> list[CheckResult]:
    runner = _run if runner is None else runner
    python = native_python or sys.executable
    results = [check_coordination(root), check_handoff(root), check_support_schemas(root)]
    results.append(_command_result(
        "native-contract-support",
        [python, "run_tests.py", "--layer", "contract", "--pattern",
         "test_support_*.py", "--verbosity", "1"], root, runner,
    ))
    results.append(CheckResult(
        "native-optional", "not-run", "optional layer is not requested by the fast support aggregate"
    ))
    results.append(CheckResult(
        "hosted-ci", "not-run", "hosted workflow is not executed by a local aggregate"
    ))
    return results


def exit_code(results: list[CheckResult]) -> int:
    return 1 if any(item.state in FAILURE_STATES for item in results) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--native-python",
                        help="interpreter used only to invoke the existing target-native runner")
    parser.add_argument("--no-record", action="store_true",
                        help="write no validation-run record (the current runner is read-only)")
    args = parser.parse_args(argv)
    results = run_checks(args.root.resolve(), native_python=args.native_python)
    for item in results:
        print(f"{item.name}: {item.state} ({item.detail})")
    return exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main())
'''


TEST_COORDINATION = r'''"""Focused unittest coverage for the support aggregate contract."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


aggregate = load("loto_support_test_aggregate", ROOT / "tools" / "validate_support.py")


class SupportCoordinationTests(unittest.TestCase):
    def test_native_command_uses_existing_contract_layer(self):
        calls = []

        def passing_runner(command, root):
            calls.append((command, root))
            return subprocess.CompletedProcess(command, 0, "", "")

        results = aggregate.run_checks(ROOT, native_python="native-python", runner=passing_runner)
        native = next(item for item in results if item.name == "native-contract-support")
        self.assertEqual(native.state, "passed")
        self.assertEqual(calls, [([
            "native-python", "run_tests.py", "--layer", "contract", "--pattern",
            "test_support_*.py", "--verbosity", "1"], ROOT)])

    def test_aggregate_failure_composition(self):
        def failing_runner(command, root):
            return subprocess.CompletedProcess(command, 7, "", "injected")

        results = aggregate.run_checks(ROOT, runner=failing_runner)
        native = next(item for item in results if item.name == "native-contract-support")
        self.assertEqual(native.state, "failed")
        self.assertEqual(aggregate.exit_code(results), 1)

    def test_result_state_exit_semantics(self):
        non_failure = ["passed", "skipped", "not-run", "not-configured"]
        results = [aggregate.CheckResult(str(index), state, "probe")
                   for index, state in enumerate(non_failure)]
        self.assertEqual(aggregate.exit_code(results), 0)
        for state in ("failed", "unknown", "unavailable"):
            with self.subTest(state=state):
                self.assertEqual(
                    aggregate.exit_code([aggregate.CheckResult("probe", state, "applicable")]), 1
                )


if __name__ == "__main__":
    unittest.main()
'''


TEST_HANDOFF = r'''"""Focused unittest coverage for handoff truth and read-only mode."""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load_aggregate():
    path = ROOT / "tools" / "validate_support.py"
    spec = importlib.util.spec_from_file_location("loto_support_test_handoff_aggregate", path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


aggregate = load_aggregate()


def tracked_digest(root: Path) -> str:
    inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=root,
                            text=True, capture_output=True, check=False)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        raise unittest.SkipTest("tracked-file invariant requires an exact Git worktree")
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root,
                         text=True, capture_output=True, check=True)
    if Path(top.stdout.strip()).resolve() != root.resolve():
        raise AssertionError("Git top-level does not equal the candidate repository root")
    names = subprocess.run(["git", "ls-files", "-z"], cwd=root, check=True,
                           capture_output=True).stdout.split(b"\0")
    digest = hashlib.sha256()
    for raw in sorted(item for item in names if item):
        relative = raw.decode("utf-8")
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update((root / relative).read_bytes())
    return digest.hexdigest()


class SupportHandoffTests(unittest.TestCase):
    def test_bootstrap_handoff_is_truthfully_not_configured(self):
        result = aggregate.check_handoff(ROOT)
        self.assertEqual(result.state, "not-configured")

    def test_no_record_mode_changes_no_tracked_file(self):
        passed = [aggregate.CheckResult("probe", "passed", "injected")]
        before = tracked_digest(ROOT)
        with mock.patch.object(aggregate, "run_checks", return_value=passed):
            self.assertEqual(aggregate.main(["--root", str(ROOT), "--no-record"]), 0)
        self.assertEqual(tracked_digest(ROOT), before)


if __name__ == "__main__":
    unittest.main()
'''


FILES = {
    "tools/validate_support.py": AGGREGATE,
    "tests/contract/test_support_coordination.py": TEST_COORDINATION,
    "tests/contract/test_support_handoff.py": TEST_HANDOFF,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-python", required=True)
    return parser.parse_args()


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}{result.stderr}"
        )
    return result


args = parse_args()
native_python = str(Path(args.native_python).resolve())

# Freeze parent and scope before rendering.
head = run([
    "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "rev-parse", "HEAD"
], cwd=LOTO).stdout.strip()
origin = run([
    "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "rev-parse", "origin/main"
], cwd=LOTO).stdout.strip()
if head != PARENT or origin != PARENT:
    raise AssertionError(f"target drift: HEAD={head} origin/main={origin} expected={PARENT}")
if run([
    "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "status", "--porcelain"
], cwd=LOTO).stdout:
    raise AssertionError("CC_Loto worktree is not clean")
for rel in FILES:
    exists = subprocess.run([
        "git", "-c", "safe.directory=C:/xPY/xPrj/CC_Loto", "cat-file", "-e", f"{PARENT}:{rel}"
    ], cwd=LOTO, capture_output=True, check=False)
    if exists.returncode == 0:
        raise AssertionError(f"candidate path already exists at reviewed parent: {rel}")

errors = []
for rel, content in FILES.items():
    if "\r" in content:
        errors.append(f"{rel}: CR character")
    if re.search(r"\{\{[A-Z_]+\}\}", content):
        errors.append(f"{rel}: unresolved placeholder")
    hits = scan_sensitive(content)
    if hits:
        errors.append(f"{rel}: sensitive patterns {hits}")
    for token in ("LLM_Wiki", "03_PKE", "Enconet", "CC_FIN", "C:/xPY", "C:\\xPY"):
        if token in content:
            errors.append(f"{rel}: forbidden foreign/workspace reference {token!r}")
if "pytest" in "\n".join(FILES.values()).lower():
    errors.append("candidate introduces a pytest reference")
if "blocked" in AGGREGATE:
    errors.append("aggregate uses blocked as a check state")
if errors:
    raise AssertionError("\n".join(errors))

temp_root = Path(os.environ.get("TEMP", tempfile.gettempdir()))
with tempfile.TemporaryDirectory(prefix="ls6-", dir=temp_root) as tmp:
    root = Path(tmp) / "repo"
    shutil.copytree(
        LOTO, root,
        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "Output", "ModelCache"),
    )
    for rel, content in FILES.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        py_compile.compile(str(path), doraise=True)

    # A source export without .git must skip only the tracked-digest assertion,
    # not error or search upward into an unrelated repository.
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["DYNAMIX_OUTPUT_DIR"] = str(Path(tmp) / "runtime" / "Output")
    env["DYNAMIX_MODEL_CACHE_DIR"] = str(Path(tmp) / "runtime" / "ModelCache")
    no_git = run([
        native_python, "run_tests.py", "--layer", "contract",
        "--pattern", "test_support_*.py", "--verbosity", "1",
    ], cwd=root, env=env)
    no_git_output = no_git.stdout + "\n" + no_git.stderr
    if [int(value) for value in re.findall(r"Ran (\d+) tests?", no_git_output)] != [5]:
        raise AssertionError("non-Git focused run did not discover five tests")
    if "skipped=1" not in no_git_output:
        raise AssertionError("non-Git focused run did not skip the tracked-digest assertion")
    print("NON-GIT EXPORT PASSED: 5 focused tests, tracked-digest assertion skipped=1")

    run(["git", "init"], cwd=root)
    run(["git", "config", "user.name", "Slice 6 Review"], cwd=root)
    run(["git", "config", "user.email", "slice6@example.invalid"], cwd=root)
    run(["git", "add", "."], cwd=root)
    run(["git", "commit", "-m", "fixture"], cwd=root)

    board = root / "coordination/BOARD.md"
    board_before = board.read_bytes()
    aggregate = run([
        sys.executable, "tools/validate_support.py", "--root", ".",
        "--native-python", native_python, "--no-record",
    ], cwd=root, env=env)
    if "coordination: passed (errors=0; warnings=0)" not in aggregate.stdout:
        raise AssertionError("aggregate did not report coordination passed 0/0")
    if "handoff: not-configured (bootstrap pointer; no record published)" not in aggregate.stdout:
        raise AssertionError("aggregate did not report bootstrap handoff truthfully")
    if "support-schemas: passed (parsed=1)" not in aggregate.stdout:
        raise AssertionError("aggregate did not parse the installed handoff schema")
    if "native-contract-support: passed" not in aggregate.stdout:
        raise AssertionError("aggregate did not pass focused native contract tests")
    if "native-optional: not-run" not in aggregate.stdout or "hosted-ci: not-run" not in aggregate.stdout:
        raise AssertionError("aggregate lost truthful not-run states")
    if board.read_bytes() != board_before:
        raise AssertionError("coordination/BOARD.md changed during aggregate validation")

    missing_native = subprocess.run([
        sys.executable, "tools/validate_support.py", "--root", ".",
        "--native-python", str(Path(tmp) / "missing-python.exe"), "--no-record",
    ], cwd=root, env=env, text=True, capture_output=True, check=False)
    if missing_native.returncode != 1 or "native-contract-support: unavailable" not in missing_native.stdout:
        raise AssertionError(
            "missing applicable native interpreter did not fail closed\n"
            + missing_native.stdout + missing_native.stderr
        )
    print("OPERATOR PROBE PASSED: missing native interpreter -> unavailable, exit 1")

    wrong_operator = subprocess.run([
        native_python, "tools/validate_support.py", "--root", ".",
        "--native-python", native_python, "--no-record",
    ], cwd=root, env=env, text=True, capture_output=True, check=False)
    if wrong_operator.returncode != 1 or "coordination: unavailable" not in wrong_operator.stdout:
        raise AssertionError(
            "product interpreter missing support dependencies did not fail closed\n"
            + wrong_operator.stdout + wrong_operator.stderr
        )
    print("OPERATOR PROBE PASSED: wrong support interpreter -> unavailable, exit 1")

    expected = {"core-unit": 42, "contract": 30, "state-integrity": 3}
    for layer, expected_count in expected.items():
        native = run([
            native_python, "run_tests.py", "--layer", layer,
            "--pattern", "test*.py", "--verbosity", "1",
        ], cwd=root, env=env)
        combined = native.stdout + "\n" + native.stderr
        counts = [int(value) for value in re.findall(r"Ran (\d+) tests?", combined)]
        if counts != [expected_count]:
            raise AssertionError(f"native {layer} count {counts} != {[expected_count]}")
        print(f"NATIVE PASSED: {layer} {expected_count}/{expected_count}, exit 0")

    spec = importlib.util.spec_from_file_location("loto_slice6_probe", root / "tools/validate_support.py")
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load aggregate for failure probe")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    for state in ("failed", "unknown", "unavailable"):
        if module.exit_code([module.CheckResult("injected", state, "proof")]) != 1:
            raise AssertionError(f"injected applicable {state} did not return aggregate exit 1")
    for state in ("passed", "skipped", "not-run", "not-configured"):
        if module.exit_code([module.CheckResult("injected", state, "proof")]) != 0:
            raise AssertionError(f"deliberate/non-failure {state} returned nonzero")
    print("FAIL-CLOSED PROBE PASSED: failed/unknown/unavailable -> 1; deliberate states -> 0")

    if run(["git", "status", "--porcelain"], cwd=root).stdout:
        raise AssertionError("disposable overlay changed tracked content")

out_resolved = OUT.resolve()
if out_resolved.parent != (WIKI / "doc/support-transfer/rendered").resolve():
    raise AssertionError(f"unsafe output path: {out_resolved}")
if OUT.exists():
    shutil.rmtree(OUT)
for rel, content in FILES.items():
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")

actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
if actual != set(FILES):
    raise AssertionError(f"inventory mismatch: {sorted(actual)}")
for rel in sorted(FILES):
    digest = hashlib.sha256((OUT / rel).read_bytes()).hexdigest().upper()
    print(f"RENDERED {rel} SHA256={digest}")
print("INVENTORY PASSED: exactly three new target-native validators/tests paths")
print("TARGET VALIDATION PASSED: coordination 0/0; BOARD byte-identical; overlay clean")
print(f"TARGET_PARENT={PARENT}")
