"""Package the tested v4 candidate as a fresh immutable clean release.

No live supplier reads, audit data, approval inheritance or release overwrite.
The owner deferred Claude review; that status is recorded, not called approval.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import tempfile

from bootstrap_sieving import _check_existing_chain
from check_candidate_paths_v4 import scan
import prepare_framework_candidate_v4 as candidate

WORKSPACE = Path(__file__).resolve().parents[1]
METHOD = """# Company-neutral framework v4 — usage

This release supplies tools, not an approved audit. Each supplier has its own
local scripts. No sibling company's documents or decisions are used at runtime.

## Folder homes

Keep owner inputs in incoming, registered sources in raw, and the database in db.
Working files live in work: derived, manifests, benchmarks, decisions, reviews,
validation, bootstrap and migrations. Put plans in docs/plans and session notes
in coordination/handoffs. project-layout.json explicitly selects v4.

Results use outputs/RUN-YYYYMMDD-N. dashboard_light.html and dashboard_dark.html
are separate self-contained files. Open either one directly; no theme chooser
or server is needed. Internal review packages belong in work/reviews.

## Start a new audit

1. Read the local AGENTS.md, project-state.yml and sieving/SIEVING_PLAYBOOK.md.
2. Put this supplier's documents and proposed regulatory sources in incoming.
3. Agree source editions, scope, language and applicability with the owner.
4. Initialize a fresh database with python scripts/init_db.py, then follow the
   documented intake, chapter, calibration, sieving and approval commands.
5. Use python scripts/audit_command.py audit-status to check the current stage.
   Do not skip a gate or copy another supplier's approval.

No database, sources, crumbs, scores, active prompt or golden fixture is installed.
Claude setup and review remain pending; Codex must not edit Claude infrastructure.
Old method documents are retained for history; this is the current layout guide.

## Reset and repeat

Reset is preview-first. Review its exact targets and arrange the local backup
decision before apply. It preserves incoming and framework/history records.
A backup waiver from another supplier never transfers. Never reset to upgrade
the framework or to make a test pass.
"""


def build(destination):
    destination = Path(destination).absolute()
    _check_existing_chain(destination)
    if destination.exists():
        raise FileExistsError("release destination must be fresh")
    scratch = WORKSPACE / ".tmp"
    _check_existing_chain(scratch)
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="release-v4-", dir=scratch) as folder:
        stage = Path(folder) / "candidate"
        record = candidate.build(stage)
        paths = scan(stage)
        if not paths["passed"]:
            raise ValueError("candidate has unresolved direct-path findings")
        payload = candidate.verify_payload(record, stage)
    for name in list(payload):
        if name.startswith(("incoming/", "raw/", "outputs/", "sieving/DATA/", ".claude/")):
            if not name.endswith("/.gitkeep"):
                raise ValueError("company evidence or infrastructure in release: " + name)
            del payload[name]
    payload["docs/FRAMEWORK_METHOD_V4.md"] = METHOD.encode("utf-8")
    attrs = payload[".gitattributes"].decode("utf-8")
    attrs = attrs.replace("manifests/*.csv", "work/manifests/*.csv")
    attrs = attrs.replace(".bootstrap/**/*.jsonl", "work/bootstrap/**/*.jsonl")
    attrs = attrs.replace("benchmarks/sieving_golden/", "work/benchmarks/sieving_golden/")
    attrs = attrs.replace("\nderived/**", "\nwork/derived/**")
    attrs += ("\n# Current v4 framework and exact retained migration bytes\n"
              "docs/** text eol=lf\nwiki/*.md text eol=lf\nAGENTS.md text eol=lf\n"
              "framework-company.json text eol=lf\nproject-state.yml text eol=lf\n"
              "project-layout.json text eol=lf\nwork/migrations/** -text\n")
    payload[".gitattributes"] = attrs.encode("utf-8")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WORKSPACE,
                          capture_output=True, text=True, check=True).stdout.strip()
    sources = [Path(__file__).resolve(), Path(candidate.__file__).resolve()]
    sources += [Path(__file__).parent / name for name in (
        "bootstrap_sieving.py", "framework_release.py", "prepare_vendor.py",
        "upgrade_vendor_v4.py", "check_candidate_paths_v4.py")]
    sources += sorted(candidate.RUNTIME.glob("*"))
    manifest = {
        "template_version": "4.0.0", "scope": "clean-audit-framework",
        "status": "tested-framework-not-company-approved", "review_status": "deferred",
        "source_head": head, "baseline_manifest_sha256": candidate.PIN,
        "provenance": [{"source": path.relative_to(WORKSPACE).as_posix(),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                       for path in sources if path.is_file()],
        "files": [{"path": name, "bytes": len(body),
                   "sha256": hashlib.sha256(body).hexdigest()}
                  for name, body in sorted(payload.items())]}
    destination.mkdir(parents=True, exist_ok=False)
    for name, body in payload.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(body)
    with (destination / "manifest.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.destination)
    print(json.dumps({"version": manifest["template_version"], "files": len(manifest["files"]),
                      "review_status": manifest["review_status"]}))


if __name__ == "__main__":
    main()
