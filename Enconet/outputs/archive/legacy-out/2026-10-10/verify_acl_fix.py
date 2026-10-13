"""Retain final ACL-repair validation without changing prior release records."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
release_path = ROOT / "manifests/release_RUN-20261008-17.json"
release = json.loads(release_path.read_text(encoding="utf-8"))
for row in release["artifacts"]:
    assert hashlib.sha256((ROOT / row["destination"]).read_bytes()).hexdigest() == row["sha256"]
before = json.loads((OUT / "release-acl-repair/before.json").read_text(encoding="utf-8"))
after = json.loads((OUT / "release-acl-repair/after.json").read_text(encoding="utf-8"))
assert len(before) == len(after) == 13
for old, new in zip(before, after):
    assert old["path"] == new["path"] and old["sha256"] == new["sha256"]
    assert old["inheritance_protected"] and not new["inheritance_protected"]
commands = [
    [sys.executable, str(ROOT / "scripts/run_all_validations.py"), "--benchmarks", "--no-record"],
    [sys.executable, str(ROOT / "out/2026-10-09/scoring-fixture-refresh/verify_metadata.py")],
]
checks = []
for index, command in enumerate(commands):
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (OUT / f"acl-check-{index}.log").write_text(result.stdout + result.stderr, encoding="utf-8", newline="\n")
    checks.append({"command": command, "exit_code": result.returncode})
record = {"files": 13, "all_bytes_unchanged": True, "checks": checks,
          "passed": all(c["exit_code"] == 0 for c in checks)}
(OUT / "acl-checks.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(record))
raise SystemExit(int(not record["passed"]))
