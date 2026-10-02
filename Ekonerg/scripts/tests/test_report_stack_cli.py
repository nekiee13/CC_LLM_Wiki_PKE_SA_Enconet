from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parent / "audit_template" / "tests"))
from test_report_stack import _fixture  # shared synthetic-only fixture


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / script), *args],
        cwd=ROOT.parent,
        text=True,
        capture_output=True,
        check=False,
    )


def test_copied_runtime_cli_chain(tmp_path: Path):
    db, approvals, run_id = _fixture(tmp_path)
    output = tmp_path / "outputs"
    package = output / "package.json"
    report = output / "report.md"
    data = output / "dashboard.json"
    dashboard = output / "dashboard.html"
    commands = [
        ("build_evaluation_package.py", "--db", str(db), "--run-id", run_id, "--approvals", str(approvals), "--output", str(package)),
        ("generate_report.py", str(package), "--output", str(report)),
        ("build_dashboard_data.py", str(package), "--generated-date", "2026-10-02T00:00:00Z", "--dash-id", "DASH-20261002-0001", "--output", str(data)),
        ("generate_dashboard.py", str(data), "--output", str(dashboard)),
        ("validate_report.py", str(package), str(report)),
        ("validate_dashboard.py", str(package), str(data), str(dashboard)),
    ]
    results = [_run(*command) for command in commands]
    assert all(result.returncode == 0 for result in results), [result.stderr for result in results]
    assert all(path.is_file() for path in (package, report, data, dashboard))
    assert "Četa  Audit" in dashboard.read_text(encoding="utf-8")
