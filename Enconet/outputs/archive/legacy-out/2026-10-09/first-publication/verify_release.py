"""Retain exact release hashes, source integrity and full final validation logs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
release = json.loads((ROOT / "manifests/release_RUN-20261008-17.json").read_text())
for row in release["artifacts"]:
    source, target = ROOT / row["source"], ROOT / row["destination"]
    assert hashlib.sha256(target.read_bytes()).hexdigest() == row["sha256"], target
    assert source.read_bytes() == target.read_bytes(), target
regression = json.loads((OUT / "regression/summary.json").read_text())
checked = 0
for relative, digest in regression["live_before"].items():
    if relative.startswith(("incoming/", "raw/", "derived/", "db/", ".claude/", "CLAUDE.md", "coordination/")):
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
        checked += 1
command = [sys.executable, str(ROOT / "scripts/run_all_validations.py"), "--benchmarks", "--no-record"]
result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
(OUT / "final-aggregate.log").write_text(result.stdout + result.stderr, encoding="utf-8", newline="\n")
record = {"command": command, "exit_code": result.returncode,
          "published_artifacts": len(release["artifacts"]), "protected_files_unchanged": checked,
          "passed": result.returncode == 0}
(OUT / "verification.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(record))
print(result.stdout.strip().splitlines()[-1])
raise SystemExit(result.returncode)
