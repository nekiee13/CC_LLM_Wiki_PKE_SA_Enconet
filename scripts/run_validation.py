"""Aggregate layered validation runner (ALIGNMENT_PLAN C5.2).

Layers L0-L5: syntax -> structure/paths/authority -> unit -> integration ->
golden regression -> state/handoff recovery. Exit codes: 0 all layers passed,
1 at least one layer FAILED (named in the report), 3 no failures but at least
one layer SKIPPED (SKIPPED is never PASS). Paths resolve from this script's
location, never the CWD. Stdlib only; output is ASCII (CP1252-portable).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
ENCONET = WORKSPACE / "Enconet"
SIEVING = ENCONET / "sieving"
STEP_TIMEOUT_S = 900


@dataclass
class Step:
    name: str
    command: list[str] | None  # None means the step cannot run
    cwd: Path = WORKSPACE
    skip_reason: str = ""


@dataclass
class Layer:
    name: str
    steps: list[Step]


@dataclass
class Result:
    layer: str
    state: str  # PASS | FAIL | SKIPPED
    details: list[str] = field(default_factory=list)


def _run_step(step: Step) -> tuple[str, str]:
    if step.command is None:
        return "SKIPPED", f"{step.name}: {step.skip_reason or 'not configured'}"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", COLUMNS="200")
    try:
        proc = subprocess.run(
            step.command, cwd=step.cwd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=STEP_TIMEOUT_S, env=env,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return "FAIL", f"{step.name}: could not execute ({exc})"
    if proc.returncode:
        tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-8:])
        return "FAIL", f"{step.name}: exit {proc.returncode}\n{tail}"
    return "PASS", f"{step.name}: exit 0"


def run_layers(layers: list[Layer]) -> list[Result]:
    results = []
    for layer in layers:
        states, details = [], []
        for step in layer.steps:
            state, detail = _run_step(step)
            states.append(state)
            details.append(detail)
        if "FAIL" in states:
            layer_state = "FAIL"
        elif "SKIPPED" in states:
            layer_state = "SKIPPED"
        else:
            layer_state = "PASS"
        results.append(Result(layer.name, layer_state, details))
    return results


def overall_exit(results: list[Result]) -> int:
    if any(r.state == "FAIL" for r in results):
        return 1
    if any(r.state == "SKIPPED" for r in results):
        return 3
    return 0


def report(results: list[Result]) -> None:
    print("aggregate validation report (C5.2)")
    print("=" * 60)
    for r in results:
        print(f"[{r.state}] {r.layer}")
        for detail in r.details:
            for line in detail.splitlines():
                print(f"    {line}")
    failed = [r.layer for r in results if r.state == "FAIL"]
    skipped = [r.layer for r in results if r.state == "SKIPPED"]
    print("=" * 60)
    if failed:
        print(f"FAILED layer(s): {', '.join(failed)}")
    if skipped:
        print(f"SKIPPED layer(s): {', '.join(skipped)} -- SKIPPED is not PASS")
    if not failed and not skipped:
        print("all layers passed")


def _pointer_record() -> Path | None:
    pointer = ENCONET / "HANDOFF.md"
    if not pointer.is_file():
        return None
    match = re.search(r"\((handoffs/[^)]+\.md)\)", pointer.read_text(encoding="utf-8"))
    if not match:
        return None
    record = ENCONET / match.group(1)
    return record if record.is_file() else None


def build_layers() -> list[Layer]:
    py = sys.executable
    json_files = [
        WORKSPACE / "handoff_schema.yml",
        WORKSPACE / "doc" / "GUIDANCE_PAIRS.json",
        ENCONET / "schemas" / "sieving_contract.yml",
        ENCONET / "schemas" / "sieving_data_migration_manifest.yml",
        SIEVING / "DATA_MANIFEST.json",
    ]
    parse_code = (
        "import json,sys\n"
        "for p in sys.argv[1:]:\n"
        "    json.load(open(p, encoding='utf-8'))\n"
    )
    record = _pointer_record()
    if record:
        l5_validate = Step(
            "validate pointed-to handoff record",
            [py, str(WORKSPACE / "scripts" / "make_handoff.py"), "--validate", str(record)],
        )
    else:
        l5_validate = Step(
            "validate pointed-to handoff record", None,
            skip_reason="HANDOFF.md missing or does not resolve to an immutable record",
        )
    return [
        Layer("L0 syntax", [
            Step("compile workspace scripts", [py, "-m", "compileall", "-q", str(WORKSPACE / "scripts")]),
            Step("compile sieving sources", [py, "-m", "compileall", "-q", str(SIEVING / "src"), str(SIEVING / "cli.py")]),
            Step("parse machine-readable manifests", [py, "-c", parse_code, *map(str, json_files)]),
        ]),
        Layer("L1 structure, paths, authority", [
            Step("guidance-pair drift", [py, str(WORKSPACE / "scripts" / "check_guidance_drift.py")]),
            Step("skill structure", [py, str(WORKSPACE / "scripts" / "check_skill_structure.py")]),
            Step("coordination protocol", [py, str(WORKSPACE / "scripts" / "agent_coord.py"), "validate"]),
        ]),
        Layer("L2 unit (workspace scripts)", [
            Step("workspace script tests", [py, "-m", "pytest", "scripts/tests", "-q", "-p", "no:cacheprovider"]),
        ]),
        Layer("L3 integration (project)", [
            Step("schema contract validator", [py, str(ENCONET / "scripts" / "validate_schemas.py")]),
            Step("schema and ingestion pipeline tests", [py, "-m", "pytest",
                 "tests/test_validate_schemas.py", "tests/test_db_backbone.py", "tests/test_raw_intake.py",
                 "tests/test_chunk_pipeline.py",
                 "-q", "-p", "no:cacheprovider"], cwd=ENCONET),
            Step("sieving test suite", [py, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=SIEVING),
            Step("installation verification", [py, "verify_install.py"], cwd=SIEVING),
            Step("DATA checksum manifest", [py, str(SIEVING / "tools" / "verify_data_manifest.py")]),
        ]),
        Layer("L4 golden regression (contract vs corpus)", [
            Step("contract drift tests", [py, "-m", "pytest", "tests/test_contract_drift.py", "-q", "-p", "no:cacheprovider"], cwd=SIEVING),
        ]),
        Layer("L5 state and handoff recovery", [
            l5_validate,
            Step("handoff staleness", [py, str(WORKSPACE / "scripts" / "make_handoff.py"), "--check-staleness"]),
        ]),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print layer wiring without executing")
    args = parser.parse_args()
    layers = build_layers()
    if args.list:
        for layer in layers:
            print(layer.name)
            for step in layer.steps:
                target = " ".join(step.command) if step.command else f"(skipped: {step.skip_reason})"
                print(f"    {step.name}: {target}")
        return 0
    results = run_layers(layers)
    report(results)
    return overall_exit(results)


if __name__ == "__main__":
    raise SystemExit(main())
