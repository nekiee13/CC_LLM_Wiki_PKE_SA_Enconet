#!/usr/bin/env python3
"""Validate EA6.2 documentation and rehearse a clean portable-package build."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

import build_review_package
import validate_evidence_access_candidate
import validate_evidence_access_uat
import validate_review_package


COMMAND_IDS = {
    "verify-environment", "validate-candidate", "validate-package", "validate-uat",
    "aggregate", "build-portable", "open-workspace", "hash-baseline",
}
TOPICS = {
    "operations": ["Conda environment", "Open and use", "Build", "Validate", "Transfer", "Recovery", "Failure guide"],
    "architecture": ["Data flow", "Trust boundaries", "Artifact model", "Extension points"],
    "upgrade": ["Current approved behavior", "Upgrade decision gate", "Compatibility contract", "Rollback plan"],
}


def load_contract(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("operations contract must be an object")
    return value


def _safe(root: Path, relative: object) -> Path | None:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        return None
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def _topic_errors(label: str, text: str) -> list[str]:
    return [f"{label} documentation missing topic: {topic}" for topic in TOPICS[label] if topic not in text]


def validate(
    contract_path: Path,
    operations_path: Path,
    architecture_path: Path,
    upgrade_path: Path,
    project_root: Path,
    *,
    rehearse: bool = True,
) -> tuple[list[str], dict]:
    errors: list[str] = []
    summary = {"commands": 0, "rehearsal_files": 0, "rehearsal_runs": 0}
    try:
        contract = load_contract(contract_path)
        texts = {
            "operations": operations_path.read_text(encoding="utf-8"),
            "architecture": architecture_path.read_text(encoding="utf-8"),
            "upgrade": upgrade_path.read_text(encoding="utf-8"),
        }
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [f"evidence-access documentation is unreadable: {exc}"], summary
    if set(contract) != {"schema_version", "python", "commands", "rehearsal"}:
        errors.append("operations contract fields mismatch")
    if contract.get("schema_version") != "1.0":
        errors.append("unsupported operations schema_version")
    if contract.get("python") != r"C:\xPY\vEnv\WikiEnconet\python.exe":
        errors.append("operations contract does not pin the approved Conda interpreter")
    commands = contract.get("commands")
    if not isinstance(commands, list):
        commands = []
        errors.append("operations commands must be an array")
    summary["commands"] = len(commands)
    ids = [row.get("id") for row in commands if isinstance(row, dict)]
    if set(ids) != COMMAND_IDS or len(ids) != len(COMMAND_IDS):
        errors.append("operations command identities mismatch")
    for index, row in enumerate(commands):
        if not isinstance(row, dict) or set(row) != {"id", "text"}:
            errors.append(f"operations command fields mismatch: commands[{index}]")
            continue
        marker = f"command:{row['id']}"
        if marker not in texts["operations"]:
            errors.append(f"missing documented command: {row['id']}")
        if not isinstance(row["text"], str) or row["text"] not in texts["operations"]:
            errors.append(f"documented command text drift: {row['id']}")
    for label, text in texts.items():
        errors.extend(_topic_errors(label, text))
    combined = "\n".join(texts.values()).lower()
    if "streamlit run" in combined:
        errors.append("documentation advertises the retired Streamlit interface")
    if "a web service is not required" not in texts["architecture"].lower():
        errors.append("architecture does not state the offline service boundary")

    candidate_contract = project_root / "schemas" / "evidence_access_release_candidate.yml"
    uat_contract = project_root / "schemas" / "evidence_access_uat.yml"
    uat_packet = project_root / "docs" / "acceptance" / "EA5.4_OWNER_UAT.md"
    candidate_errors, _ = validate_evidence_access_candidate.validate(candidate_contract, project_root)
    errors.extend(f"candidate check: {error}" for error in candidate_errors)
    uat_errors, _ = validate_evidence_access_uat.validate(uat_contract, uat_packet, project_root)
    errors.extend(f"UAT check: {error}" for error in uat_errors)

    rehearsal = contract.get("rehearsal")
    if not isinstance(rehearsal, dict) or set(rehearsal) != {
        "catalog", "source_root", "expected_manifest_sha256", "expected_files", "expected_runs"
    }:
        errors.append("operations rehearsal fields mismatch")
        rehearsal = {}
    if rehearse and not errors:
        catalog_path = _safe(project_root, rehearsal.get("catalog"))
        source_root = _safe(project_root, rehearsal.get("source_root"))
        if catalog_path is None or source_root is None:
            errors.append("unsafe documentation rehearsal path")
        else:
            temporary = Path(tempfile.mkdtemp(prefix="ea6-2-doc-rehearsal-"))
            destination = temporary / "portable-package-Č"
            try:
                catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
                manifest_path = build_review_package.build(catalog, source_root, destination)
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                summary["rehearsal_files"] = len(manifest.get("files", []))
                summary["rehearsal_runs"] = len(manifest.get("run_ids", []))
                digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
                if digest != rehearsal.get("expected_manifest_sha256"):
                    errors.append("clean rehearsal manifest hash mismatch")
                if summary["rehearsal_files"] != rehearsal.get("expected_files"):
                    errors.append("clean rehearsal file count mismatch")
                if summary["rehearsal_runs"] != rehearsal.get("expected_runs"):
                    errors.append("clean rehearsal run count mismatch")
                errors.extend(f"clean rehearsal: {error}" for error in validate_review_package.validate(destination))
            except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"clean documentation rehearsal failed: {exc}")
            finally:
                shutil.rmtree(temporary, ignore_errors=True)
    return list(dict.fromkeys(errors)), summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--operations", type=Path, required=True)
    parser.add_argument("--architecture", type=Path, required=True)
    parser.add_argument("--upgrade", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--no-rehearsal", action="store_true")
    args = parser.parse_args(argv)
    errors, summary = validate(
        args.contract, args.operations, args.architecture, args.upgrade, args.project_root,
        rehearse=not args.no_rehearsal,
    )
    if errors:
        for error in errors:
            print(f"validate_evidence_access_docs: FAIL - {error}", file=sys.stderr)
        return 1
    print(
        "validate_evidence_access_docs: PASS - "
        f"commands={summary['commands']} rehearsal_files={summary['rehearsal_files']} "
        f"rehearsal_runs={summary['rehearsal_runs']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
