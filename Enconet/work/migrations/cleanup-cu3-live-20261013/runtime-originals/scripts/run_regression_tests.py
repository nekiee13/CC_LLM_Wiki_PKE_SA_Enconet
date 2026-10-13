"""Run every Enconet regression test, isolating historical data dependencies.

No skips or changed assertions: current unit tests run in the live code tree;
historical characterization and DATA tests run against current code in a fresh
hash-verified historical workspace. The workspace is retained for diagnostics.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from regression_fixture import ROOT, build, historical_test

def protected_hashes() -> dict:
    roots = ("incoming", "raw", "derived", "db", "outputs", "manifests", ".claude")
    values = {}
    for root in roots:
        for path in (ROOT / root).rglob("*"):
            if path.is_file() and path.suffix not in {"-wal", "-shm"}:
                values[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    for path in [ROOT / "CLAUDE.md", *(ROOT / "coordination/messages").glob("CC_*.md"),
                 *(ROOT / "coordination/archive").glob("CC_*.md")]:
        if path.is_file():
            values[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return values

def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / "out"):
        p.error("test reports must be under this project's out directory")
    output.mkdir(parents=True, exist_ok=True)
    if any((output / name).exists() for name in ("current.xml", "historical.xml", "summary.json")):
        p.error("test report target already exists; use a new output directory")
    before = protected_hashes()
    parent = ROOT / ".test-tmp"
    parent.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="regression-isolated-", dir=parent))
    fixture = work / "Enconet-history"
    provenance = build(fixture)
    tests = sorted((ROOT / "tests").glob("test*.py"))
    current = [str(t) for t in tests if not historical_test(t.name)] + [str(ROOT / "scripts/tests")]
    history = [str(fixture / "tests" / t.name) for t in tests if historical_test(t.name)] + [str(fixture / "sieving/tests")]
    results = []
    for label, paths, cwd in (("current", current, ROOT), ("historical", history, fixture)):
        command = [sys.executable, "-m", "pytest", *paths, "-q", "-o", "addopts=", "-p", "no:cacheprovider",
                   "--basetemp", str(work / f"pytest-{label}"), "--junitxml", str(output / f"{label}.xml"), "--tb=short"]
        environment = dict(os.environ, NQA_TEST_DECISION_ROOT=str(ROOT), NQA_TEST_SKILL_ORIGIN=str(ROOT), PYTHONUTF8="1",
                           PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run(command, cwd=cwd, env=environment,
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
        (output / f"{label}.log").write_text(completed.stdout + completed.stderr, encoding="utf-8", newline="\n")
        suites = ET.parse(output / f"{label}.xml").getroot().findall("testsuite")
        counts = {k: sum(int(s.attrib[k]) for s in suites) for k in ("tests", "errors", "failures", "skipped")}
        results.append({"class": label, "command": command, "exit_code": completed.returncode, **counts})
        print(label, completed.returncode, counts, flush=True)
    after = protected_hashes()
    if before != after:
        raise RuntimeError("live audit files changed during tests")
    summary = {"fixture": provenance, "groups": results, "live_audit_unchanged": True,
               "selected_test_files": len(tests), "skipped_test_files": [], "live_before": before}
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    return int(any(r["exit_code"] != 0 for r in results))

if __name__ == "__main__":
    raise SystemExit(main())
