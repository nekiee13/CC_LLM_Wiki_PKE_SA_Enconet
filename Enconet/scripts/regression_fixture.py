"""Build a verified disposable historical test workspace, never a live restore."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import zipfile
from project_layout import LEGACY, V4, guard

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "tests/fixtures/history/enconet-pre-reset-20261007.zip"
ARCHIVE_SHA256 = "38018c13eb9c17172c7c3486b4041dbb54e27618f78cfb9989ebb56cbfcfaedf"
HISTORICAL_NAMES = {"test_browser_harness.py", "test_epic7_requirements.py", "test_epic8_evaluation.py", "test_epic13_validation.py",
    "test_portable_report_links.py", "test_quote_highlighting.py", "test_report_link_validator.py",
    "test_review_catalog.py", "test_review_package_portability.py", "test_review_workspace.py"}

def historical_test(name: str) -> bool:
    return name.startswith("test_evidence") or name in HISTORICAL_NAMES

def copyable(relative: Path) -> bool:
    forbidden = {".git", ".agents", ".claude", "coordination", "__pycache__", ".test-tmp",
                 "_archive", "context", "history", ".obsidian"}
    if relative.parts[:2] == ("sieving", "tools"):
        forbidden.remove("_archive")  # AST/inventory tests read quarantined tools; never execute them.
    return (not set(relative.parts) & forbidden and relative.name not in {"AGENTS.md", "CLAUDE.md"}
            and not relative.name.startswith("CC_") and relative.suffix not in {".pyc", ".pyo"})

def validate_archive(archive: Path = ARCHIVE, expected_sha: str = ARCHIVE_SHA256) -> dict:
    if hashlib.sha256(archive.read_bytes()).hexdigest() != expected_sha:
        raise ValueError("historical archive checksum mismatch")
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        if len(set(names)) != len(names):
            raise ValueError("duplicate archive entry")
        for name in names:
            parts = PurePosixPath(name).parts
            if (not parts or name.startswith(("/", "\\")) or ".." in parts or ":" in name or "\\" in name
                    or any(p in {".claude", ".agents", "coordination"} for p in parts)
                    or parts[-1] in {"AGENTS.md", "CLAUDE.md"} or parts[-1].startswith(("CC_", "CX_"))):
                raise ValueError(f"unsafe archive entry: {name}")
        bad = z.testzip()
        if bad:
            raise ValueError(f"archive CRC mismatch: {bad}")
        plan = json.loads(z.read("reset-plan.json"))
        rows = plan["candidates"]
        expected_names = {r["relative_path"] for r in rows}
        if set(names) != expected_names | {"reset-plan.json"}:
            raise ValueError("archive/manifest entries differ")
        for row in rows:
            payload = z.read(row["relative_path"])
            if len(payload) != row["size"] or hashlib.sha256(payload).hexdigest() != row["sha256"]:
                raise ValueError(f"archive entry checksum mismatch: {row['relative_path']}")
        return plan

def source_homes(source: Path) -> dict:
    """Select explicit source homes; the disposable fixture stays historical."""
    config = source / "project-layout.json"
    if not config.exists():
        return LEGACY  # Pre-layout historical test sources only.
    data = json.loads(config.read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or set(data) != {"schema_version", "layout"}
            or type(data["schema_version"]) is not int or data["schema_version"] != 1
            or data["layout"] not in ("legacy", "v4")):
        raise ValueError("invalid fixture source layout")
    return V4 if data["layout"] == "v4" else LEGACY


def scratch_home(source: Path = ROOT) -> Path:
    return source / (".tmp" if source_homes(source) == V4 else ".test-tmp")


def require_target(target: Path, source: Path = ROOT) -> Path:
    target, source = target.resolve(), source.resolve()
    scratch = scratch_home(source)
    if target == source or target == scratch or not target.is_relative_to(scratch):
        raise ValueError("historical fixture requires an isolated local scratch target")
    if source == ROOT:
        guard(target)
    if target.exists():
        raise ValueError("historical target already exists; never overlay or retry into it")
    return target

def build(target: Path, source: Path = ROOT, archive: Path = ARCHIVE) -> dict:
    target = require_target(target, source)
    plan = validate_archive(archive)
    target.mkdir(parents=True)
    # Code/contracts come from the current release; only evidence/results come
    # from the hash-locked historical fixture. No sibling project is used.
    homes = source_homes(source)
    roots = [(name, name) for name in ("scripts", "schemas", "templates", "tests", "docs",
             "sieving/src", "sieving/tests", "sieving/prompts", "sieving/tools")]
    roots += [(homes[name], name) for name in ("decisions", "benchmarks")]
    if homes == V4:
        roots.append((homes["reviews"], "docs/reviews"))
    for source_home, destination_home in roots:
        directory = source / source_home
        for current, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if copyable(Path(current).relative_to(source) / d)
                       and not d.startswith(("epic13-", ".pytest", "pytest-cache"))]
            for name in files:
                original = Path(current) / name
                relative = original.relative_to(source)
                if not copyable(relative):
                    continue
                destination = target / destination_home / original.relative_to(directory)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(original, destination)
    if homes == V4:
        # Historical tests reference pre-cleanup plan names. Copy only allowed
        # current contracts into their disposable historical paths, never live.
        for original in (source / homes["plans"]).glob("*.md"):
            if copyable(original.relative_to(source)):
                shutil.copyfile(original, target / "docs" / original.name)
    (target / "project-layout.json").write_text(
        '{"schema_version":1,"layout":"legacy"}\n', encoding="utf-8")
    for name in ("cli.py", "requirements.txt", "verify_install.py", "README.md", "QUICKSTART.md", "PROJECT_INFO.md", "PROVENANCE.md", "DATA_MANIFEST.json", "SIEVING_PLAYBOOK.md"):
        original = source / "sieving" / name
        if original.is_file():
            shutil.copyfile(original, target / "sieving" / name)
    (target / "db").mkdir(exist_ok=True)
    shutil.copyfile(source / "db/schema.sql", target / "db/schema.sql")
    for name in ("index.md", "log.md", "current-status.md"):
        (target / "wiki").mkdir(exist_ok=True)
        shutil.copyfile(source / "wiki" / name, target / "wiki" / name)
    for name in ("criteria", "evidence", "findings", "actions", "gates", "dashboards"):
        (target / "wiki" / name).mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for row in plan["candidates"]:
            relative = Path(row["relative_path"])
            if relative.parts[:2] == ("db", "backups"):
                continue
            destination = (target / relative).resolve()
            if not destination.is_relative_to(target):
                raise ValueError("archive target escaped isolated workspace")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(z.read(row["relative_path"]))
            if relative.parts[0] == "raw":
                destination.chmod(stat.S_IREAD)
    return {"fixture_sha256": ARCHIVE_SHA256, "manifest_entries": len(plan["candidates"]),
            "target": str(target), "historical_only": True}
