"""Render and dry-run the owner-approved CC_Loto AGENTS.md correction."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path


PARENT = "d5dc65e568ee73d82389e6e1d3fdf24122661adf"
PARENT_AGENTS_OBJECT = "34b7eb93095022bea137e2a0c2313f356bfa0f28"
PARENT_CLAUDE_OBJECT = "3edd87504e76a97d8ba46ecf40e81b8ad894299f"
OLD = (
    "Missing optional dependencies must remain fail-soft where the product contract says so. Report each\n"
    "check literally as passed, failed, skipped, unavailable, blocked, unknown, or not run; never relabel\n"
    "a missing, timed-out, or excluded check as passed. Redirect output and model-cache paths outside the\n"
)
NEW = (
    "Missing optional dependencies must remain fail-soft where the product contract says so. Report each\n"
    "check literally as passed, failed, skipped, not-run, unknown, not-configured, or unavailable;\n"
    "`blocked` is a handoff/blocker state, never a check result. Never relabel a missing, timed-out, or\n"
    "excluded check as passed. Redirect output and model-cache paths outside the\n"
)
PRESERVED_BLOCKER_WARNING = (
    "Never report a validation as passed when it was skipped, blocked, unavailable, or not run."
)
LAYER_COUNTS = {"core-unit": 42, "contract": 30, "state-integrity": 3}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run(command: list[str], root: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=root, env=env, text=True, capture_output=True, check=False
    )


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def render(root: Path) -> bytes:
    require(git(root, "rev-parse", "HEAD") == PARENT, "target HEAD drift")
    require(git(root, "rev-parse", f"{PARENT}:AGENTS.md") == PARENT_AGENTS_OBJECT,
            "parent AGENTS.md object drift")
    require(git(root, "rev-parse", f"{PARENT}:CLAUDE.md") == PARENT_CLAUDE_OBJECT,
            "parent CLAUDE.md object drift")
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", "-C", str(root),
         "show", f"{PARENT}:AGENTS.md"],
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, "cannot read parent AGENTS.md blob")
    source = result.stdout.decode("utf-8")
    require(source.count(OLD) == 1, "exact defective enumeration not found once")
    require(source.count(PRESERVED_BLOCKER_WARNING) == 1,
            "preserved blocker warning not found once")
    candidate = source.replace(OLD, NEW, 1)
    require(candidate.count(PRESERVED_BLOCKER_WARNING) == 1,
            "line-129 blocker warning changed")
    require("check literally as passed, failed, skipped, not-run, unknown, not-configured, or unavailable;" in candidate,
            "canonical enumeration absent")
    require("`blocked` is a handoff/blocker state, never a check result." in candidate,
            "blocked-state boundary absent")
    require("check literally as passed, failed, skipped, unavailable, blocked" not in candidate,
            "defective enumeration survived")
    return candidate.encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--native-python", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    candidate = render(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(candidate)
    object_result = subprocess.run(
        ["git", "hash-object", "--stdin"], input=candidate, capture_output=True, check=False
    )
    require(object_result.returncode == 0, "cannot calculate candidate Git object")
    candidate_object = object_result.stdout.decode("ascii").strip()
    candidate_sha = hashlib.sha256(candidate).hexdigest().upper()

    print(f"candidate_sha256={candidate_sha}")
    print(f"candidate_object={candidate_object}")
    print(f"candidate_bytes={len(candidate)}")

    if args.native_python is None:
        return 0
    native_python = args.native_python.resolve()
    require(native_python.is_file(), "native interpreter absent")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="loto-guidance-correction-") as temp_name:
        temp_root = Path(temp_name)
        overlay = temp_root / "CC_Loto-overlay"
        clone_result = run(
            ["git", "clone", "--quiet", "--no-hardlinks", str(root), str(overlay)],
            temp_root,
            env,
        )
        require(clone_result.returncode == 0, "overlay clone failed")
        require(git(overlay, "checkout", "--quiet", PARENT) == "", "overlay checkout failed")
        board_before = hashlib.sha256((overlay / "coordination" / "BOARD.md").read_bytes()).hexdigest()
        claude_before = git(overlay, "hash-object", "CLAUDE.md")
        (overlay / "AGENTS.md").write_bytes(candidate)
        require(git(overlay, "diff", "--name-only") == "AGENTS.md", "overlay path scope changed")
        require(git(overlay, "hash-object", "CLAUDE.md") == claude_before == PARENT_CLAUDE_OBJECT,
                "CLAUDE.md changed")
        env["DYNAMIX_OUTPUT_DIR"] = str(temp_root / "Output")
        env["DYNAMIX_MODEL_CACHE_DIR"] = str(temp_root / "model_cache")

        aggregate = run(
            [sys.executable, "tools/validate_support.py", "--root", str(overlay),
             "--native-python", str(native_python), "--no-record"], overlay, env
        )
        require(aggregate.returncode == 0, "overlay aggregate failed")
        require("coordination: passed (errors=0; warnings=0)" in aggregate.stdout,
                "overlay coordination not 0/0")
        require("native-contract-support: passed" in aggregate.stdout,
                "focused support contract failed")
        for layer, count in LAYER_COUNTS.items():
            result = run(
                [str(native_python), "run_tests.py", "--layer", layer, "--verbosity", "1"],
                overlay,
                env,
            )
            require(result.returncode == 0, f"native layer failed: {layer}")
            require(f"Ran {count} tests" in result.stdout + result.stderr,
                    f"native count mismatch: {layer}")
        require(hashlib.sha256((overlay / "coordination" / "BOARD.md").read_bytes()).hexdigest()
                == board_before, "BOARD changed")
        overlay_status = git(overlay, "status", "--porcelain")
        print(f"overlay_porcelain={overlay_status!r}")
        require(overlay_status == "M AGENTS.md",
                f"unexpected overlay artifact: {overlay_status!r}")
        numstat = git(overlay, "diff", "--numstat", "--", "AGENTS.md")
        print(f"overlay_numstat={numstat}")
        print("overlay_aggregate=passed")
        print("overlay_native=42/42,30/30,3/3")
        print("overlay_board=byte-identical")
        print("overlay_paths=AGENTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
