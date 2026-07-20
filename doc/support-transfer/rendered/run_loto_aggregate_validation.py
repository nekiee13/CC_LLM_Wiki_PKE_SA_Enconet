"""Reproduce the read-only CC_Loto milestone aggregate validation.

This evidence harness writes only to an OS temporary directory.  It never
updates the target worktree, its validation history, or its Git metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_TIP = "d5dc65e568ee73d82389e6e1d3fdf24122661adf"
EXPECTED_LAYER_COUNTS = {
    "core-unit": 42,
    "contract": 30,
    "state-integrity": 3,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run(command: list[str], root: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    print(f"$ {' '.join(command)}")
    print(f"exit={result.returncode}")
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.stderr.strip():
        print(result.stderr.rstrip())
    return result


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--native-python", type=Path, required=True)
    parser.add_argument("--expected-tip", default=EXPECTED_TIP)
    args = parser.parse_args()

    root = args.root.resolve()
    native_python = args.native_python.resolve()
    support_python = Path(sys.executable).resolve()
    require(root.is_dir(), f"target root absent: {root}")
    require(native_python.is_file(), f"native interpreter absent: {native_python}")

    before_status = git(root, "status", "--porcelain")
    before_board = digest(root / "coordination" / "BOARD.md")
    head = git(root, "rev-parse", "HEAD")
    upstream = git(root, "rev-parse", "origin/main")
    divergence = git(root, "rev-list", "--left-right", "--count", "origin/main...HEAD")
    require(head == args.expected_tip, f"HEAD drift: {head}")
    require(upstream == args.expected_tip, f"origin/main drift: {upstream}")
    require(divergence.split() == ["0", "0"], f"divergence: {divergence}")
    require(not before_status, f"dirty target before validation: {before_status}")

    base_env = os.environ.copy()
    base_env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="loto-aggregate-") as temp_name:
        temp_root = Path(temp_name)
        base_env["DYNAMIX_OUTPUT_DIR"] = str(temp_root / "Output")
        base_env["DYNAMIX_MODEL_CACHE_DIR"] = str(temp_root / "model_cache")

        aggregate = run(
            [str(support_python), "tools/validate_support.py", "--root", str(root),
             "--native-python", str(native_python), "--no-record"],
            root,
            base_env,
        )
        require(aggregate.returncode == 0, "installed aggregate did not pass")
        for expected in (
            "coordination: passed (errors=0; warnings=0)",
            "handoff: not-configured",
            "support-schemas: passed (parsed=1)",
            "native-contract-support: passed",
            "native-optional: not-run",
            "hosted-ci: not-run",
        ):
            require(expected in aggregate.stdout, f"aggregate output missing: {expected}")

        coordination = run(
            [str(support_python), "tools/support/agent_coord.py", "."], root, base_env
        )
        require(coordination.returncode == 0, "direct coordination validation failed")
        require("0 error(s), 0 warning(s)" in coordination.stdout,
                "direct coordination result is not 0/0")

        missing_native = run(
            [str(support_python), "tools/validate_support.py", "--root", str(root),
             "--native-python", str(temp_root / "absent-python.exe"), "--no-record"],
            root,
            base_env,
        )
        require(missing_native.returncode == 1, "missing-native probe did not fail closed")
        require("native-contract-support: unavailable" in missing_native.stdout,
                "missing-native probe did not report unavailable")

        wrong_operator = run(
            [str(native_python), "tools/validate_support.py", "--root", str(root),
             "--native-python", str(native_python), "--no-record"],
            root,
            base_env,
        )
        require(wrong_operator.returncode == 1, "wrong-operator probe did not fail closed")
        require("coordination: unavailable" in wrong_operator.stdout,
                "wrong-operator probe did not report unavailable")

        for layer, count in EXPECTED_LAYER_COUNTS.items():
            layer_result = run(
                [str(native_python), "run_tests.py", "--layer", layer, "--verbosity", "1"],
                root,
                base_env,
            )
            combined = layer_result.stdout + layer_result.stderr
            require(layer_result.returncode == 0, f"native layer failed: {layer}")
            require(f"Ran {count} tests" in combined, f"unexpected count for {layer}")

    after_status = git(root, "status", "--porcelain")
    after_board = digest(root / "coordination" / "BOARD.md")
    require(not after_status, f"dirty target after validation: {after_status}")
    require(after_board == before_board, "coordination/BOARD.md changed")
    require(git(root, "rev-parse", "HEAD") == args.expected_tip, "HEAD changed")

    print("SUMMARY")
    print(f"target_tip={args.expected_tip}")
    print("divergence=0/0")
    print("aggregate=passed")
    print("coordination=passed errors=0 warnings=0")
    print("fail_closed_probes=2/2")
    print("native_layers=42/42,30/30,3/3")
    print("excluded_layers=optimization-core,integration,webapp,optional,hosted-ci:not-run")
    print(f"board_sha256={before_board}")
    print("target_write=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
