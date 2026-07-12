"""C5.2 aggregate-runner contract tests.

The runner must execute layered checks (L0-L5), exit non-zero on failure while
naming the failing layer, and never let a SKIPPED layer count as passed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
RUNNER = WORKSPACE / "scripts" / "run_validation.py"

sys.path.insert(0, str(WORKSPACE / "scripts"))

import run_validation  # noqa: E402


def _step(code: str) -> list[str]:
    return [sys.executable, "-c", code]


def test_all_layers_pass():
    layers = [
        run_validation.Layer("L0 demo", [run_validation.Step("ok", _step("pass"))]),
        run_validation.Layer("L1 demo", [run_validation.Step("ok", _step("pass"))]),
    ]
    results = run_validation.run_layers(layers)
    assert run_validation.overall_exit(results) == 0
    assert all(r.state == "PASS" for r in results)


def test_failure_is_nonzero_and_names_the_layer(capsys):
    layers = [
        run_validation.Layer("L0 demo", [run_validation.Step("ok", _step("pass"))]),
        run_validation.Layer("L3 integration demo",
                             [run_validation.Step("boom", _step("raise SystemExit(2)"))]),
    ]
    results = run_validation.run_layers(layers)
    code = run_validation.overall_exit(results)
    run_validation.report(results)
    out = capsys.readouterr().out
    assert code == 1
    assert "FAIL" in out and "L3 integration demo" in out


def test_skipped_is_not_pass_and_fails_overall(capsys):
    layers = [
        run_validation.Layer(
            "L5 handoff demo",
            [run_validation.Step("missing", None, skip_reason="record not configured")],
        ),
    ]
    results = run_validation.run_layers(layers)
    code = run_validation.overall_exit(results)
    run_validation.report(results)
    out = capsys.readouterr().out
    assert results[0].state == "SKIPPED"
    assert code == 3, "a skipped layer must not yield exit 0 (SKIPPED != PASS)"
    assert "SKIPPED" in out and "record not configured" in out


def test_real_runner_lists_all_six_layers():
    """--list must show the real L0-L5 wiring without executing anything."""
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--list"], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    for token in ("L0", "L1", "L2", "L3", "L4", "L5"):
        assert token in proc.stdout, f"layer {token} missing from --list output"


def test_output_is_cp1252_portable():
    """C5.3: console output must survive CP1252 terminals (ASCII only)."""
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--list"], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60,
    )
    proc.stdout.encode("cp1252")  # raises UnicodeEncodeError on violation
