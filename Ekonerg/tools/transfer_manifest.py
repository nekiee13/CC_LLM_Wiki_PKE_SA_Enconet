"""EK-0.2: inventory pinned Git blobs, never copy or execute source tools.

Generate review artifacts only in Ekonerg/docs/transfer. The manifest is a
proposal, not an executable allowlist or approval. Adapt/recreate entries require
separate reviewed work; the future EK-1.1 copier must not treat them as copy.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

BASELINE = "9f20430c95334daa4c3cedb7ee71b002bd3be739"
WORKSPACE = Path(__file__).resolve().parents[2]
OUTPUT = WORKSPACE / "Ekonerg" / "docs" / "transfer"
POLICY = "ek-0.2-conservative-v1"


@dataclass(frozen=True)
class Blob:
    mode: str
    oid: str
    data: bytes


def read_snapshot(root: Path, revision: str) -> tuple[str, dict[str, Blob]]:
    """Read the tree and exact blobs, never worktree contents or Git filters."""
    def git(*args, input=None):
        return subprocess.check_output(["git", "-C", str(root), *args], input=input)

    commit = git("rev-parse", "--verify", revision + "^{commit}").decode().strip()
    entries = []
    for raw in git("ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
        if not raw:
            continue
        metadata, filename = raw.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        if kind != "blob":
            raise ValueError("Unsupported non-blob tree entry: " + filename.decode())
        entries.append((filename.decode("utf-8"), mode, oid))
    oids = sorted({oid for _, _, oid in entries})
    stream = git("cat-file", "--batch", input=("\n".join(oids) + "\n").encode())
    blobs, offset = {}, 0
    for expected in oids:
        end = stream.index(b"\n", offset)
        oid, kind, size = stream[offset:end].decode().split()
        if oid != expected or kind != "blob":
            raise ValueError("Unexpected Git batch response")
        start, length = end + 1, int(size)
        data = stream[start:start + length]
        if len(data) != length or stream[start + length:start + length + 1] != b"\n":
            raise ValueError("Truncated Git blob")
        blobs[oid] = data
        offset = start + length + 1
    if offset != len(stream):
        raise ValueError("Unexpected trailing Git output")
    return commit, {name: Blob(mode, oid, blobs[oid]) for name, mode, oid in entries}


RUN_CONTRACTS = {
    "evidence_access_operations.yml", "evidence_access_promotion.yml",
    "evidence_access_release_candidate.yml", "evidence_access_review_protocol.yml",
    "evidence_access_uat.yml", "sieving_data_migration_manifest.yml",
}
SUPPORT_NOTES = {
    "agent_coord.py": "Repoint ROOT/COORD/HANDOFF_POINTER and derived directories to Ekonerg; test nested and sibling isolation.",
    "run_validation.py": "Repoint WORKSPACE/ENCONET/SIEVING, every subprocess/cwd, schemas, local tests and fresh DATA manifests; phase-aware empty setup.",
    "make_handoff.py": "Adapt WORKSPACE/DEFAULT_PROJECT/SCHEMA_PATH/default project-id; discover actual Git root separately; local publication only.",
    "check_guidance_drift.py": "Use local doc/GUIDANCE_PAIRS.json; no Enconet or global guidance dependency; preserve agent ownership.",
    "check_skill_structure.py": "Distinguish project and workspace scopes; default local checks without scanning sibling project data; explicit scope tests.",
}


def disposition(path: str, blob: Blob) -> tuple[str, str | None, str, str]:
    """Explicit conservative category policy; full per-file inventory is frozen."""
    name = PurePosixPath(path).name
    local = "Ekonerg/" + (path[len("Enconet/"):] if path.startswith("Enconet/") else path)
    if blob.mode not in {"100644", "100755"}:
        return "exclude", None, "unsupported-entry", "Never transfer links or special entries."
    if name == "CLAUDE.md" or ".claude" in PurePosixPath(path).parts or name.startswith("CC_"):
        return "exclude", None, "claude-owned", "Claude creates its own Ekonerg setup; never copy or modify Claude-owned records."
    if path == "handoff_schema.yml":
        return "copy", local, "handoff-schema", "Generic handoff record schema; no audit-run state."
    if path.startswith("scripts/"):
        return "adapt", local, "support-tool", SUPPORT_NOTES.get(name, "Local support regression tests; replace workspace/sibling fixtures and paths without weakening checks.")
    if path == "doc/GUIDANCE_PAIRS.json":
        return "recreate", local, "guidance-pairs", "New local pair map; Claude owns its side; no inherited synchronization claims."
    if path in {".gitignore", ".gitattributes"}:
        return "adapt", local, "repository-policy", "Scope ignore and line-ending rules to Ekonerg; preserve source-data and runtime exclusions."
    if path in {"AGENTS.md", "README.md"}:
        return "exclude", None, "workspace-guidance", "Workspace guidance remains inherited; do not duplicate it as project guidance."
    if not path.startswith("Enconet/"):
        return "exclude", None, "other-workspace-material", "Other project support-transfer examples and historical engineering records are not the active audit framework."
    rel = path[len("Enconet/"):]
    if rel in {"HANDOFF.md"}:
        return "exclude", None, "old-handoff", "Keep new Ekonerg handoffs; never replace them with Enconet history."
    if rel == "coordination/TEAM_PROTOCOL.md":
        return "adapt", local, "coordination-contract", "Keep neutral protocol and lifecycle rules; use local tooling and paths."
    if rel == "coordination/BOARD.md":
        return "recreate", local, "fresh-board", "Generate from fresh local claims/messages; no inherited history."
    if rel.startswith(("raw/", "derived/", "outputs/", "handoffs/", "coordination/", "sieving/runs/")):
        return "exclude", None, "audit-history", "Old sources, derived evidence, outputs, runs, and coordination history must not transfer."
    if rel.startswith("sieving/tools/_archive/"):
        if name == "README.md":
            return "recreate", local, "quarantine-notice", "Fresh notice that retired repair tools are deliberately absent; never restore them to satisfy legacy tests."
        return "exclude", None, "retired-repair", "Quarantined legacy repair tools are not runtime support; never run or reactivate them."
    if rel.startswith("decisions/"):
        if name == "README.md":
            return "recreate", local, "decision-register", "Fresh Ekonerg decision register with reusable policy references, never old audit approvals."
        return "exclude", None, "historical-decision", "Retain origin reference in the review guide; restate reusable rules in new Ekonerg guidance."
    if rel.startswith("wiki/"):
        if rel in {"wiki/index.md", "wiki/log.md", "wiki/current-status.md"} or name == ".gitkeep":
            return "recreate", local, "fresh-wiki", "Fresh setup pages and empty required directories; no old projections or status."
        return "exclude", None, "audit-projection", "Findings, gates, actions, matrices and dashboards belong to the old audit."
    if rel.startswith("manifests/"):
        if name.endswith(".csv") or name == "README.md":
            return "recreate", local, "fresh-ledger", "Keep field contracts only; CSV headers with zero old rows and fresh operating guidance."
        return "exclude", None, "old-batch", "No old source batch identifiers, document lists or intake decisions."
    if rel == "project-state.yml":
        return "recreate", local, "fresh-state", "Ekonerg, Croatian, setup phase, all G1-G7 pending; no old decision references."
    if rel in {"sieving/DATA_MANIFEST.json", "sieving/prompts/CHANGELOG.md"}:
        return "recreate", local, "fresh-sieving-record", "Empty corpus checksum record or fresh prompt history; keep no old filenames, hashes or decisions."
    if rel.startswith("schemas/") and name in RUN_CONTRACTS:
        return "recreate", local, "run-bound-contract", "Fresh unapproved contract/template; no inherited run/source/crumb IDs, hashes, counts or approvals."
    if rel.startswith(("tests/fixtures/", "sieving/tests/fixtures/", "sieving/prompts/fixtures/")):
        return "recreate", local, "synthetic-fixture", "Invent source-free fixtures and regenerate expected output through reviewed tests, not copied evidence."
    if rel.startswith("benchmarks/") and name not in {"validate_benchmarks.py", "BENCHMARK_POLICY.md", ".gitkeep"}:
        return "recreate", local, "synthetic-benchmark", "Rebuild isolated synthetic fixtures; keep scoring and rendering classes distinct and preserve independent expected-value review."
    if rel.startswith("docs/"):
        if any(part in {"reviews", "acceptance", "releases", "context", "_archive"} for part in PurePosixPath(rel).parts):
            return "exclude", None, "old-review-or-context", "Old review/UAT/release records and context do not authorize Ekonerg."
        return "adapt", local, "operating-guide", "Retain reusable workflow only; remove company examples, source excerpts, completed claims and old approval links."
    if rel == "MASTER_DEVELOPMENT_PLAN.md":
        return "recreate", "Ekonerg/docs/FRAMEWORK_REQUIREMENTS.md", "requirements-map", "Extract reusable acceptance rules only; this is not an inherited completed plan or approval."
    if rel.startswith(".agents/") or rel == "AGENTS.md":
        return "adapt", local, "codex-guidance", "Local Codex guidance only; sanitize examples and historical run lessons, preserve gates; Claude synchronization remains pending."
    if name == ".gitkeep":
        return "recreate", local, "empty-directory", "Create an empty structural placeholder only, not other folder contents."
    if rel.startswith(("scripts/", "sieving/src/", "sieving/tests/", "tests/", "sieving/tools/")) or name.endswith(".py"):
        return "adapt", local, "audit-code", "Retain tool behavior; review roots, default supplier/IDs, embedded fixtures, imports and subprocess targets before local use."
    if rel.startswith(("schemas/", "templates/", "sieving/prompts/")) or rel == "db/schema.sql":
        return "adapt", local, "framework-contract", "Keep reusable taxonomy/schema/rendering behavior; strip run-bound values and test against fresh state and synthetic data."
    if rel.startswith("sieving/") or rel in {"environment.yml", "Sieving_method_specification_Guide.md", "benchmarks/BENCHMARK_POLICY.md"}:
        return "adapt", local, "framework-support", "Local operating/dependency/provenance contract; preserve origin, remove old audit details, verify shared runtime separately."
    return "exclude", None, "unselected", "Not an approved runtime input; adding it requires manifest revision and review."


def content_flags(data: bytes) -> list[str]:
    text = data.decode("utf-8-sig", errors="replace")
    patterns = {
        "company-name": r"(?i)enconet|tekol",
        "run-or-document-id": r"\b(?:RUN-\d{8}|DOC-\d{4}|CRUMB-|SRC-\d{8})",
        "approval-or-promotion": r"(?i)\b(?:approved|promoted|decision_reference|approval_ref)\b",
        "sha256-literal": r"\b[0-9a-f]{64}\b",
        "windows-absolute-path": r"[A-Za-z]:[\\/]",
        "parent-path": r"\.\.[\\/]",
        "source-quote-field": r"(?i)evidence_quotes|citation_text|expected_crumbs",
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text)]


def build_manifest(blobs: dict[str, Blob], revision: str) -> dict:
    rows = []
    for path, blob in sorted(blobs.items()):
        treatment, destination, category, purpose = disposition(path, blob)
        title = PurePosixPath(path).name.replace("_", " ").replace("-", " ")
        if treatment != "exclude" and path.endswith(".py"):
            tree = ast.parse(blob.data.decode("utf-8-sig"), filename=path)
            docstring = ast.get_docstring(tree)
            if docstring:
                title = docstring.splitlines()[0][:240]
        rows.append({"source": path, "destination": destination, "mode": blob.mode,
                     "git_blob": blob.oid, "sha256": hashlib.sha256(blob.data).hexdigest(),
                     "bytes": len(blob.data), "treatment": treatment, "category": category,
                     "purpose": title,
                     "purpose_and_required_work": purpose,
                     "content_flags": content_flags(blob.data) if treatment != "exclude" else []})
    return {"schema_version": 1, "policy": POLICY, "source_commit": revision,
            "status": "proposed-awaiting-Claude-review", "inventory_only": True,
            "scope": "every tracked entry in the pinned workspace; no untracked or ignored input",
            "files": rows}


def validate_manifest(manifest: dict, blobs: dict[str, Blob], revision: str) -> list[str]:
    """Reject omissions, additions, edits and unsafe mappings, not just bad hashes."""
    errors = []
    expected = build_manifest(blobs, revision)
    if not isinstance(manifest, dict):
        return ["Manifest must be an object"]
    if set(manifest) != set(expected):
        errors.append("Unexpected or missing top-level fields")
    for key in expected.keys() - {"files"}:
        if manifest.get(key) != expected[key]:
            errors.append("Metadata mismatch: " + key)
    rows = manifest.get("files")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        return errors + ["files must be a list of objects"]
    paths = [row.get("source") for row in rows]
    if any(not isinstance(path, str) for path in paths):
        return errors + ["Every source must be a string"]
    if len(paths) != len(set(paths)):
        errors.append("Duplicate source entries")
    if set(paths) != set(blobs):
        errors.append("Inventory differs from pinned tree: missing or foreign source entries")
    destinations = []
    expected_by_path = {row["source"]: row for row in expected["files"]}
    for row in rows:
        if row != expected_by_path.get(row["source"]):
            errors.append("Changed source/hash/disposition: " + row["source"])
        dest = row.get("destination")
        if dest is not None:
            if not isinstance(dest, str):
                errors.append("Invalid destination type")
                continue
            parts = PurePosixPath(dest).parts
            if not dest.startswith("Ekonerg/") or ".." in parts or "\\" in dest or ":" in dest:
                errors.append("Unsafe destination: " + dest)
            destinations.append(dest.casefold())
    if len(destinations) != len(set(destinations)):
        errors.append("Case-insensitive destination collision")
    if rows != expected["files"] and not errors:
        errors.append("Noncanonical row order")
    return errors


def dependency_scan(blobs: dict[str, Blob], manifest: dict) -> dict:
    """Navigation evidence, not a proof of dynamic dependency closure."""
    by_name = defaultdict(list)
    modules = defaultdict(list)
    for path in blobs:
        by_name[PurePosixPath(path).name].append(path)
        if path.endswith(".py"):
            modules[PurePosixPath(path).stem].append(path)
    entries = []
    for row in manifest["files"]:
        path = row["source"]
        if row["treatment"] == "exclude":
            continue
        data = blobs[path].data
        try:
            source = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            entries.append({"source": path, "binary": True, "requires_manual_review": True})
            continue
        imports, local_imports, external, constants = [], {}, [], []
        if path.endswith(".py"):
            tree = ast.parse(source, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
            for module in sorted(set(imports)):
                matches = modules.get(module.split(".")[-1], [])
                if matches:
                    local_imports[module] = matches
                elif module.split(".")[0] not in sys.stdlib_module_names:
                    external.append(module)
            for node in tree.body:
                if isinstance(node, (ast.Assign, ast.AnnAssign)):
                    snippet = ast.get_source_segment(source, node) or ""
                    if any(token in snippet for token in ("Path(", "ROOT", "WORKSPACE", "ENCONET", "SCHEMA", "TEMPLATE", "MANIFEST")):
                        constants.append({"line": node.lineno, "assignment": snippet})
        # Exact known filenames referenced anywhere in selected text; ambiguous
        # names intentionally retain every candidate for reviewer inspection.
        names = set(re.findall(r"[A-Za-z_][A-Za-z0-9_.-]*\.(?:py|md|yml|yaml|json|sql|html|csv|txt|xlsx)", source))
        references = {name: by_name[name] for name in sorted(names) if name in by_name}
        entries.append({"source": path, "imports": sorted(set(imports)),
                        "local_import_candidates": local_imports,
                        "nonstdlib_or_unresolved_imports": external,
                        "known_file_reference_candidates": references,
                        "root_assignments": constants, "content_flags": row["content_flags"]})
    return {"source_commit": manifest["source_commit"], "policy": POLICY,
            "limitations": "Static imports, top-level root expressions and known filenames only. Dynamic paths, dataflow and transitive third-party dependencies need task tests and manual review.",
            "files": entries}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "verify"])
    args = parser.parse_args()
    try:
        revision, blobs = read_snapshot(WORKSPACE, BASELINE)
        manifest = build_manifest(blobs, revision)
        scan = dependency_scan(blobs, manifest)
        artifacts = {"transfer-manifest.json": manifest, "dependency-scan.json": scan}
        if args.command == "build":
            OUTPUT.mkdir(parents=True, exist_ok=True)
            for name, data in artifacts.items():
                # Generated metadata only: never write to a manifest destination.
                (OUTPUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
        else:
            actual = json.loads((OUTPUT / "transfer-manifest.json").read_text(encoding="utf-8"))
            errors = validate_manifest(actual, blobs, revision)
            if json.loads((OUTPUT / "dependency-scan.json").read_text(encoding="utf-8")) != scan:
                errors.append("Dependency scan differs from committed inputs")
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
        print(json.dumps({"command": args.command, "source_commit": revision,
                          "files": len(manifest["files"]),
                          "treatments": dict(Counter(row["treatment"] for row in manifest["files"])),
                          "dependency_scan_files": len(scan["files"]),
                          "framework_files_copied": 0}, indent=2))
        return 0
    except (OSError, ValueError, SyntaxError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
