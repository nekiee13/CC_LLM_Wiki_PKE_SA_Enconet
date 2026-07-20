"""Run the CC_Loto scoped rollback proof in a disposable clone."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_TIP = "d5dc65e568ee73d82389e6e1d3fdf24122661adf"
LAYER_COUNTS = {"core-unit": 42, "contract": 30, "state-integrity": 3}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def invoke(
    command: list[str], root: Path, env: dict[str, str], *, show_output: bool = True
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, cwd=root, env=env, text=True, capture_output=True, check=False
    )
    print(f"$ {' '.join(command)}")
    print(f"exit={result.returncode}")
    if show_output and result.stdout.strip():
        print(result.stdout.rstrip())
    if show_output and result.stderr.strip():
        print(result.stderr.rstrip())
    return result


def git(root: Path, env: dict[str, str], *args: str) -> str:
    result = invoke(["git", *args], root, env, show_output=False)
    require(result.returncode == 0, result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def tracked_hashes(root: Path, env: dict[str, str]) -> dict[str, str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, env=env, capture_output=True, check=False
    )
    require(result.returncode == 0, "git ls-files failed")
    paths = [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]
    return {path: sha256((root / path).read_bytes()) for path in paths}


def commit(root: Path, env: dict[str, str], message: str, timestamp: str) -> str:
    commit_env = env.copy()
    commit_env.update(
        {
            "GIT_AUTHOR_NAME": "Rollback Rehearsal",
            "GIT_AUTHOR_EMAIL": "rollback-rehearsal@example.invalid",
            "GIT_COMMITTER_NAME": "Rollback Rehearsal",
            "GIT_COMMITTER_EMAIL": "rollback-rehearsal@example.invalid",
            "GIT_AUTHOR_DATE": timestamp,
            "GIT_COMMITTER_DATE": timestamp,
        }
    )
    git(root, commit_env, "commit", "-m", message)
    return git(root, env, "rev-parse", "HEAD")


def revert(root: Path, env: dict[str, str], target: str, timestamp: str) -> str:
    revert_env = env.copy()
    revert_env.update(
        {
            "GIT_AUTHOR_NAME": "Rollback Rehearsal",
            "GIT_AUTHOR_EMAIL": "rollback-rehearsal@example.invalid",
            "GIT_AUTHOR_DATE": timestamp,
            "GIT_COMMITTER_NAME": "Rollback Rehearsal",
            "GIT_COMMITTER_EMAIL": "rollback-rehearsal@example.invalid",
            "GIT_COMMITTER_DATE": timestamp,
        }
    )
    git(root, revert_env, "revert", "--no-edit", target)
    return git(root, env, "rev-parse", "HEAD")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--native-python", type=Path, required=True)
    parser.add_argument("--expected-tip", default=EXPECTED_TIP)
    args = parser.parse_args()

    source = args.source.resolve()
    native_python = args.native_python.resolve()
    support_python = Path(sys.executable).resolve()
    require(source.is_dir(), f"source absent: {source}")
    require(native_python.is_file(), f"native interpreter absent: {native_python}")

    source_env = os.environ.copy()
    source_env["PYTHONDONTWRITEBYTECODE"] = "1"
    source_head = git(source, source_env, "-c", f"safe.directory={source.as_posix()}",
                      "rev-parse", "HEAD")
    source_status = git(source, source_env, "-c", f"safe.directory={source.as_posix()}",
                        "status", "--porcelain")
    require(source_head == args.expected_tip, f"source HEAD drift: {source_head}")
    require(not source_status, f"source worktree dirty: {source_status}")

    with tempfile.TemporaryDirectory(prefix="loto-rollback-") as temp_name:
        temp_root = Path(temp_name)
        clone = temp_root / "CC_Loto-rehearsal"
        clone_result = invoke(
            ["git", "clone", "--quiet", "--no-hardlinks", str(source), str(clone)],
            temp_root,
            source_env,
        )
        require(clone_result.returncode == 0, "disposable clone failed")
        require(git(clone, source_env, "rev-parse", "HEAD") == args.expected_tip,
                "clone tip mismatch")
        baseline_tree = git(clone, source_env, "rev-parse", "HEAD^{tree}")
        baseline_hashes = tracked_hashes(clone, source_env)
        board_before = sha256((clone / "coordination" / "BOARD.md").read_bytes())

        probe = clone / "support" / "rollback-rehearsal-probe.md"
        probe.write_text("# Disposable rollback probe\n\nphase: skeleton\n", encoding="utf-8")
        git(clone, source_env, "add", "support/rollback-rehearsal-probe.md")
        slice_one = commit(clone, source_env, "rehearsal: publish support skeleton",
                           "2026-07-20T03:00:00Z")

        concurrent = clone / "owner-concurrent.txt"
        concurrent_bytes = b"unrelated owner work must survive rollback\n"
        concurrent.write_bytes(concurrent_bytes)
        concurrent_hash = sha256(concurrent_bytes)
        git(clone, source_env, "add", "owner-concurrent.txt")
        concurrent_commit = commit(clone, source_env, "owner: concurrent unrelated work",
                                   "2026-07-20T03:01:00Z")

        probe.write_text(
            "# Disposable rollback probe\n\nphase: coordination\n", encoding="utf-8"
        )
        result_path = clone / "support" / "rollback-rehearsal-result.md"
        result_path.write_text("# Disposable result\n\nstate: pending\n", encoding="utf-8")
        git(clone, source_env, "add", "support/rollback-rehearsal-probe.md",
            "support/rollback-rehearsal-result.md")
        slice_two = commit(clone, source_env, "rehearsal: publish coordination evidence",
                           "2026-07-20T03:02:00Z")

        validation_env = source_env.copy()
        validation_env["DYNAMIX_OUTPUT_DIR"] = str(temp_root / "Output")
        validation_env["DYNAMIX_MODEL_CACHE_DIR"] = str(temp_root / "model_cache")
        injected_failure = invoke(
            [str(support_python), "tools/validate_support.py", "--root", str(clone),
             "--native-python", str(temp_root / "missing-python.exe"), "--no-record"],
            clone,
            validation_env,
        )
        require(injected_failure.returncode == 1, "injected failure did not fail closed")
        require("native-contract-support: unavailable" in injected_failure.stdout,
                "injected failure did not report unavailable")
        require(not git(clone, source_env, "status", "--porcelain"),
                "failure probe dirtied the clone")

        revert_two = revert(clone, source_env, slice_two, "2026-07-20T03:03:00Z")
        revert_one = revert(clone, source_env, slice_one, "2026-07-20T03:04:00Z")

        require(not probe.exists() and not result_path.exists(),
                "slice paths survived scoped rollback")
        require(concurrent.read_bytes() == concurrent_bytes, "concurrent bytes changed")
        require(sha256(concurrent.read_bytes()) == concurrent_hash,
                "concurrent hash changed")
        after_hashes = {path: sha256((clone / path).read_bytes()) for path in baseline_hashes}
        require(after_hashes == baseline_hashes, "pre-existing tracked bytes changed")
        require(sha256((clone / "coordination" / "BOARD.md").read_bytes()) == board_before,
                "BOARD bytes changed")
        remaining = git(clone, source_env, "diff", "--name-only",
                        f"{args.expected_tip}..HEAD").splitlines()
        require(remaining == ["owner-concurrent.txt"], f"unexpected remaining paths: {remaining}")
        require(not git(clone, source_env, "status", "--porcelain"),
                "recovered clone is dirty")

        aggregate = invoke(
            [str(support_python), "tools/validate_support.py", "--root", str(clone),
             "--native-python", str(native_python), "--no-record"],
            clone,
            validation_env,
        )
        require(aggregate.returncode == 0, "post-recovery aggregate failed")
        for expected in (
            "coordination: passed (errors=0; warnings=0)",
            "handoff: not-configured",
            "support-schemas: passed (parsed=1)",
            "native-contract-support: passed",
        ):
            require(expected in aggregate.stdout, f"aggregate missing: {expected}")

        coordination = invoke(
            [str(support_python), "tools/support/agent_coord.py", "."],
            clone,
            validation_env,
        )
        require(coordination.returncode == 0, "post-recovery coordination failed")
        require("0 error(s), 0 warning(s)" in coordination.stdout,
                "post-recovery coordination is not 0/0")

        for layer, count in LAYER_COUNTS.items():
            result = invoke(
                [str(native_python), "run_tests.py", "--layer", layer, "--verbosity", "1"],
                clone,
                validation_env,
                show_output=False,
            )
            combined = result.stdout + result.stderr
            require(result.returncode == 0, f"post-recovery layer failed: {layer}")
            require(f"Ran {count} tests" in combined, f"count mismatch: {layer}")
            print(f"{layer}: passed ({count}/{count})")

        require(not git(clone, source_env, "status", "--porcelain"),
                "post-validation clone is dirty")
        history = git(clone, source_env, "rev-list", "HEAD").splitlines()
        for named in (slice_one, concurrent_commit, slice_two, revert_two, revert_one):
            require(named in history, f"history lost commit: {named}")

        print("SUMMARY")
        print(f"source_tip={args.expected_tip}")
        print(f"baseline_tree={baseline_tree}")
        print(f"baseline_tracked_files={len(baseline_hashes)}")
        print(f"slice_commit_1={slice_one}")
        print(f"concurrent_commit={concurrent_commit}")
        print(f"slice_commit_2={slice_two}")
        print(f"revert_commit_2={revert_two}")
        print(f"revert_commit_1={revert_one}")
        print(f"concurrent_sha256={concurrent_hash}")
        print(f"board_sha256={board_before}")
        print("remaining_diff=owner-concurrent.txt")
        print("post_recovery_aggregate=passed")
        print("post_recovery_coordination=passed errors=0 warnings=0")
        print("post_recovery_native=42/42,30/30,3/3")
        print("source_write=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
