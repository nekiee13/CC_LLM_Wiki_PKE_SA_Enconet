"""Preview/apply a hash-pinned first release; never replace an existing file.

This deliberately does not weaken the normal reviewed replacement publisher.
A run-specific owner exception must explicitly authorize deferred review and
pin the complete plan. The result manifest is the release commit marker.
Readers must not treat a partial set as released without that marker. Individual
files are installed atomically, with handled-failure rollback. A process/power
failure can leave files without a marker: fail closed and investigate, never
silently overwrite or automatically delete them on retry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime, timezone

import audit_state

ROOT = Path(__file__).resolve().parents[1]


class ReleaseError(ValueError):
    """The approved first-release contract cannot be safely applied."""


def fingerprint(contract):
    return hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def safe(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ReleaseError("invalid relative path")
    path = (root / value).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ReleaseError("path escapes project root")
    return path


def checked_plan(contract, root):
    if set(contract) != {"schema_version", "run_id", "review_status", "owner_exception",
                         "gate_approvals", "artifacts", "result_manifest"}:
        raise ReleaseError("invalid release contract fields")
    if contract["schema_version"] != 1 or contract["review_status"] != "deferred":
        raise ReleaseError("requires an explicit deferred-review first-release contract")
    run = contract["run_id"]
    if not isinstance(run, str) or not re.fullmatch(r"RUN-[A-Za-z0-9-]+", run):
        raise ReleaseError("invalid run identity")
    if contract["gate_approvals"] != [f"G5-{run}", f"G6-{run}"]:
        raise ReleaseError("gate identities must match the release run")
    approvals = root / "manifests/approvals.csv"
    for ref in contract["gate_approvals"] + [contract["owner_exception"]]:
        try:
            row = audit_state.approval_for(ref, approvals)
        except (OSError, audit_state.StateError) as exc:
            raise ReleaseError(str(exc)) from exc
        if row["decision"] != "approved" or row["reviewer"] != "project-owner":
            raise ReleaseError("release requires signed project-owner approval")
    if (not contract["owner_exception"].startswith("PUBLICATION-") or
            f"contract_sha256={fingerprint(contract)}" not in row.get("notes", "") or
            "review deferred" not in row.get("notes", "")):
        raise ReleaseError("owner exception must pin this exact plan and permit review deferred")
    result = safe(root, contract["result_manifest"])
    if not result.is_relative_to(root / "manifests"):
        raise ReleaseError("result must be in project manifests")
    if result.exists():
        raise ReleaseError("release result already exists")
    rows, destinations = [], set()
    if not isinstance(contract["artifacts"], list) or not contract["artifacts"]:
        raise ReleaseError("empty release")
    for row in contract["artifacts"]:
        if set(row) != {"source", "destination", "sha256"}:
            raise ReleaseError("invalid artifact row")
        source, destination = safe(root, row["source"]), safe(root, row["destination"])
        if not (destination.is_relative_to(root / "outputs") or
                destination.is_relative_to(root / "wiki/dashboards")):
            raise ReleaseError("artifact destination outside output/dashboard roots")
        if destination in destinations or destination.exists():
            raise ReleaseError("duplicate or existing destination")
        destinations.add(destination)
        digest = row["sha256"]
        if (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or
                not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != digest):
            raise ReleaseError("source hash mismatch")
        rows.append((source, destination, digest))
    if result in destinations:
        raise ReleaseError("result collides with artifact")
    return rows, result


def publish(contract_path, *, root=ROOT, execute=False, validator=None, link=os.link):
    root = Path(root).resolve()
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    rows, result_path = checked_plan(contract, root)
    if not execute:
        return {"preview": True, "contract_sha256": fingerprint(contract),
                "artifacts": contract["artifacts"]}
    if validator is None:
        raise ReleaseError("execute requires a post-publication validator")
    installed = []
    # Staging resides on the destination volume so hard links are atomic and
    # no-clobber on Windows and POSIX. Never use os.replace on release targets.
    with tempfile.TemporaryDirectory(prefix="release-stage-", dir=root) as temporary:
        staging = Path(temporary)
        staged = []
        for index, (source, destination, digest) in enumerate(rows):
            path = staging / str(index)
            path.write_bytes(source.read_bytes())
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ReleaseError("candidate changed while staging")
            staged.append((path, destination, digest))
        checked_plan(contract, root)  # recheck gates, hashes and absent targets
        try:
            for path, destination, digest in staged:
                destination.parent.mkdir(parents=True, exist_ok=True)
                link(path, destination)
                installed.append((destination, digest))
            validator()
            for destination, digest in installed:
                if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
                    raise ReleaseError("published bytes changed during validation")
            result = {"schema_version": 1, "run_id": contract["run_id"],
                      "published_at": datetime.now(timezone.utc).isoformat(),
                      "review_status": "deferred", "owner_exception": contract["owner_exception"],
                      "contract_sha256": fingerprint(contract), "artifacts": contract["artifacts"]}
            marker = staging / "result.json"
            marker.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            result_path.parent.mkdir(parents=True, exist_ok=True)
            os.link(marker, result_path)  # marker last, also refuses overwrites
            return result
        except Exception as exc:
            recovery = []
            for destination, digest in reversed(installed):
                try:
                    if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
                        recovery.append(str(destination))
                    else:
                        destination.unlink()  # only exact files created by this transaction
                except OSError:
                    recovery.append(str(destination))
            suffix = f"; manual recovery needed: {recovery}" if recovery else ""
            raise ReleaseError(f"publication failed and rolled back: {exc}{suffix}") from exc


def validate_live(root):
    """Run the complete dashboard-ready spine against staged final files."""
    import subprocess
    import yaml
    import validate_report_links
    state = yaml.safe_load((root / "project-state.yml").read_text(encoding="utf-8"))
    supplier = re.sub(r"[^a-z0-9_-]+", "-", state["supplier"].casefold()).strip("-")
    package = root / f"outputs/{supplier}_appendix_b_evaluation_package.json"
    report = root / f"outputs/{supplier}_appendix_b_evaluation_report.md"
    viewer = root / f"outputs/{supplier}_appendix_b_dashboard.html"
    errors = validate_report_links.validate_paths(report, viewer, package, project_root=root)
    if errors:
        raise ReleaseError("; ".join(errors))
    # Validate all future-phase checks without prematurely changing live state.
    if state["phase"] != "findings_approved":
        raise ReleaseError("first publication requires findings_approved phase")
    state["phase"] = "dashboard_ready"
    with tempfile.TemporaryDirectory(prefix="release-check-", dir=root) as folder:
        projected = Path(folder) / "state.yml"
        projected.write_text(yaml.safe_dump(state), encoding="utf-8")
        completed = subprocess.run([sys.executable, str(root / "scripts/run_all_validations.py"),
                                    "--state", str(projected), "--benchmarks", "--no-record"],
                                   cwd=root, check=False)
        if completed.returncode:
            raise ReleaseError(f"complete projected aggregate exited {completed.returncode}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        result = publish(args.contract, execute=args.execute, validator=lambda: validate_live(ROOT))
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as exc:
        print(f"publish_audit_release: FAIL - {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
