"""Preview/apply/retry/undo a clean v2/v3 scaffold upgrade to v4.

Only hash-verified framework files move. Owner inputs and Claude infrastructure
are never moved. Original bytes and empty native directory trees stay in local
work/migrations history. There is no reset, deletion or overwrite operation.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re

from bootstrap_sieving import _check_existing_chain, _BAD_NAMES, load_manifest
from framework_release import spec
from prepare_vendor import scaffold
from preview_vendor_upgrade import match

WORKSPACE = Path(__file__).resolve().parents[1]
LEGACY_HOMES = ("benchmarks", "derived", "manifests", "decisions", "backup",
                "handoffs", "out", ".bootstrap", "docs/reviews")


def digest(body):
    return hashlib.sha256(body).hexdigest()


def fingerprint(value):
    return digest(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8"))


def local_root(target):
    root = Path(target).absolute()
    if (".." in root.parts or root.parent != WORKSPACE.absolute()
            or root.name.startswith(".") or not root.is_dir()):
        raise ValueError("one existing local supplier folder required")
    _check_existing_chain(root)
    return root


def local(root, name):
    parts = PurePosixPath(name).parts
    if (not parts or PurePosixPath(name).is_absolute() or "\\" in name
            or any(p in {".", ".."} or ":" in p or p.rstrip(" .") != p
                   or p.upper().split(".")[0] in _BAD_NAMES for p in parts)):
        raise ValueError("unsafe upgrade path")
    if any(p.casefold() in {".git", ".claude"} for p in parts):
        raise ValueError("foreign infrastructure path")
    if parts[-1].casefold() == "claude.md" or parts[-1].casefold().startswith("cc_"):
        raise ValueError("Claude-owned record path")
    path = root.joinpath(*parts)
    _check_existing_chain(path)
    for parent in path.parents:
        if parent == root:
            break
        if parent.exists() and not parent.is_dir():
            raise ValueError("upgrade path parent is not a directory")
    if path.is_file() and path.stat().st_nlink != 1:
        raise ValueError("hard-linked upgrade file")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("foreign resolved upgrade path")
    return path


def snapshot(root):
    result = {}
    for folder, dirs, names in os.walk(root, followlinks=False):
        for name in dirs + names:
            _check_existing_chain(Path(folder) / name)
        for name in names:
            path = Path(folder) / name
            if path.stat().st_nlink != 1:
                raise ValueError("hard-linked supplier file")
            result[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return result


def payload(release, supplier):
    selected = spec(release=release)
    manifest = load_manifest(selected)
    data = {r["path"]: (selected.bundle / r["path"]).read_bytes() for r in manifest["files"]}
    data.update(scaffold(supplier, release=release))
    return data, digest((selected.bundle / "manifest.json").read_bytes())


def preview(target):
    root = local_root(target)
    config = json.loads(local(root, "framework-company.json").read_text(encoding="utf-8"))
    versions = {"2.0.0": "v2", "3.0.0": "v3"}
    old_release = versions.get(config.get("framework_version"))
    if old_release is None:
        raise ValueError("upgrade requires an unstarted v2/v3 scaffold")
    supplier = config["supplier"]
    old, old_pin = payload(old_release, supplier)
    new, new_pin = payload("v4", supplier)
    before = snapshot(root)
    blockers = []
    owned = {}
    for name, body in old.items():
        if name.startswith("incoming/"):
            continue
        path = local(root, name)
        raw = path.read_bytes() if path.is_file() else None
        matched = match(raw, body) if raw is not None else None
        if matched is None:
            blockers.append("missing or edited installed framework file: " + name)
        else:
            owned[name] = {"path": name, "sha256": digest(raw), "baseline_match": matched}
    for name, sha in before.items():
        if name in old or name.startswith("incoming/"):
            continue
        if name.startswith(".bootstrap/framework-" + old_release + "/") and name.endswith(".jsonl"):
            owned[name] = {"path": name, "sha256": sha, "baseline_match": "retained-install-journal"}
        else:
            blockers.append("unplanned content must be preserved: " + name)
    # Saved Git policy files must be inert. Otherwise their deeper directory
    # rules could normalize the originals despite the history's -text policy.
    for row in owned.values():
        row["archive_path"] = row["path"] + ".record" if Path(row["path"]).name == ".gitattributes" else row["path"]
    if len({r["archive_path"].casefold() for r in owned.values()}) != len(owned):
        blockers.append("original archive path collision")
    return {"schema": "clean-scaffold-v4-upgrade-1", "target": str(root), "supplier": supplier,
            "from_release": old_release, "to_release": "v4",
            "manifest_sha256": {"old": old_pin, "new": new_pin}, "before": before,
            "originals": [owned[name] for name in sorted(owned)],
            "install": [{"path": name, "sha256": digest(body)} for name, body in sorted(new.items())],
            "blockers": blockers}


def homes(root, plan, run_id):
    if plan.get("schema") != "clean-scaffold-v4-upgrade-1" or plan.get("blockers"):
        raise ValueError("blocked or invalid upgrade plan")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", run_id):
        raise ValueError("explicit safe run ID required")
    new, pin = payload("v4", plan["supplier"])
    expected = [{"path": name, "sha256": digest(body)} for name, body in sorted(new.items())]
    if pin != plan["manifest_sha256"]["new"] or expected != plan["install"]:
        raise ValueError("new release changed after preview")
    home = local(root, "work/migrations/framework-v4/" + run_id)
    return home, new


def append(journal, event):
    with journal.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def move(source, destination):
    # Native rename is no-clobber on Windows. POSIX uses an exclusive link for
    # files, never os.replace. Directory targets were checked absent beforehand.
    if destination.exists():
        raise ValueError("upgrade destination exists")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt" or source.is_dir():
        os.rename(source, destination)
    else:
        os.link(source, destination, follow_symlinks=False)
        os.unlink(source)


def header(journal, plan):
    events = [json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines()]
    if not events or events[0].get("plan_sha256") != fingerprint(plan):
        raise ValueError("upgrade journal differs from plan")
    return events


def check_partial(root, home, plan, new):
    """Check every target before any recovery move or copy, not one at a time."""
    originals = {}
    pending = set()
    for row in plan["originals"]:
        name = row["path"]
        source = local(root, name)
        saved = local(root, (home / "original" / row["archive_path"]).relative_to(root).as_posix())
        if saved.exists():
            if not saved.is_file() or digest(saved.read_bytes()) != row["sha256"]:
                raise ValueError("retained original changed: " + name)
        else:
            if not source.is_file() or digest(source.read_bytes()) != row["sha256"]:
                raise ValueError("original file changed: " + name)
            pending.add(name)
        originals[name] = row
    for name, body in new.items():
        path = local(root, name)
        if path.exists():
            expected = originals[name]["sha256"] if name in pending else digest(body)
            if not path.is_file() or digest(path.read_bytes()) != expected:
                raise ValueError("installed file changed: " + name)
    for name in originals.keys() - new.keys() - pending:
        if local(root, name).exists():
            raise ValueError("retired original path recreated: " + name)
    for name in LEGACY_HOMES:
        path = local(root, name)
        saved = local(root, (home / "empty-homes" / name).relative_to(root).as_posix())
        if path.exists():
            if not path.is_dir() or saved.exists():
                raise ValueError("legacy home changed or collided: " + name)
            for item in path.rglob("*"):
                _check_existing_chain(item)
                if item.is_file() and item.relative_to(root).as_posix() not in pending:
                    raise ValueError("unplanned file in legacy home: " + name)
    return pending


def apply(plan, run_id, *, authority):
    root = local_root(plan["target"])
    home, new = homes(root, plan, run_id)
    journal = local(root, (home / "journal.jsonl").relative_to(root).as_posix())
    if not isinstance(authority, str) or not authority.strip():
        raise ValueError("explicit owner authorization reference required")
    if journal.exists():
        events = header(journal, plan)
        if events[0]["authority"] != authority or any(e.get("event") == "undo-complete" for e in events):
            raise ValueError("authorization differs or run was undone")
    else:
        if preview(root) != plan:
            raise ValueError("supplier changed after preview")
        home.mkdir(parents=True, exist_ok=False)
        with journal.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps({"event": "begin", "plan_sha256": fingerprint(plan),
                                     "authority": authority, "plan": plan}, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        events = header(journal, plan)
    check_partial(root, home, plan, new)
    for row in plan["originals"]:
        source = local(root, row["path"])
        backup = local(root, (home / "original" / row["archive_path"]).relative_to(root).as_posix())
        if backup.exists():
            if digest(backup.read_bytes()) != row["sha256"]:
                raise ValueError("original backup changed")
            if source.is_file() and digest(source.read_bytes()) not in {row["sha256"], digest(new.get(row["path"], b""))}:
                raise ValueError("live file changed during upgrade")
            continue
        if not source.is_file() or digest(source.read_bytes()) != row["sha256"]:
            raise ValueError("original file changed before backup")
        move(source, backup)
        append(journal, {"event": "retained-original", "path": row["path"], "sha256": row["sha256"]})
    for name in LEGACY_HOMES:
        source = local(root, name)
        destination = local(root, (home / "empty-homes" / name).relative_to(root).as_posix())
        if source.exists():
            if destination.exists() or any(p.is_file() for p in source.rglob("*")):
                raise ValueError("legacy home is not empty or already archived: " + name)
            move(source, destination)
            append(journal, {"event": "retained-empty-home", "path": name})
    for name in sorted(new, key=lambda key: (key == "project-layout.json", key)):
        path, body = local(root, name), new[name]
        if path.exists():
            if not path.is_file() or digest(path.read_bytes()) != digest(body):
                raise ValueError("new target changed or collided: " + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(body)
                stream.flush()
                os.fsync(stream.fileno())
            append(journal, {"event": "installed", "path": name, "sha256": digest(body)})
    verify(plan, run_id)
    if events[-1].get("event") != "complete":
        append(journal, {"event": "complete", "installed_files": len(new)})
    return {"state": "complete", "target": str(root), "installed_files": len(new),
            "retained_originals": len(plan["originals"]), "journal": str(journal)}


def verify(plan, run_id):
    root = local_root(plan["target"])
    home, new = homes(root, plan, run_id)
    if check_partial(root, home, plan, new):
        raise ValueError("upgrade original backup is incomplete")
    for name, body in new.items():
        path = local(root, name)
        if not path.is_file() or digest(path.read_bytes()) != digest(body):
            raise ValueError("installed file changed: " + name)
    for row in plan["originals"]:
        backup = local(root, (home / "original" / row["archive_path"]).relative_to(root).as_posix())
        if not backup.is_file() or digest(backup.read_bytes()) != row["sha256"]:
            raise ValueError("retained original changed: " + row["path"])
    for name, sha in plan["before"].items():
        if name.startswith("incoming/") and digest(local(root, name).read_bytes()) != sha:
            raise ValueError("owner input changed")
    if any(local(root, name).exists() for name in LEGACY_HOMES):
        raise ValueError("legacy working home remains")
    return {"state": "verified", "installed_files": len(new), "retained_originals": len(plan["originals"])}


def undo(plan, run_id):
    root = local_root(plan["target"])
    home, new = homes(root, plan, run_id)
    journal = home / "journal.jsonl"
    events = header(journal, plan)
    if events[-1].get("event") == "undo-complete":
        return {"state": "undone"}
    pending = check_partial(root, home, plan, new)
    for name in reversed(sorted(new, key=lambda key: (key == "project-layout.json", key))):
        source = local(root, name)
        if not source.exists() or name in pending:
            continue
        destination = local(root, (home / "undone-new" / name).relative_to(root).as_posix())
        move(source, destination)
    for name in LEGACY_HOMES:
        saved = local(root, (home / "empty-homes" / name).relative_to(root).as_posix())
        if saved.exists():
            move(saved, local(root, name))
    for row in plan["originals"]:
        if row["path"] in pending:
            continue
        saved = local(root, (home / "original" / row["archive_path"]).relative_to(root).as_posix())
        move(saved, local(root, row["path"]))
    for name, sha in plan["before"].items():
        if digest(local(root, name).read_bytes()) != sha:
            raise ValueError("undo comparison failed")
    append(journal, {"event": "undo-complete"})
    return {"state": "undone"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--authority")
    parser.add_argument("--mode", choices=("preview", "apply", "verify", "undo"), default="preview")
    args = parser.parse_args()
    if args.mode == "preview":
        if args.target is None or args.output is None:
            parser.error("preview requires --target and a fresh --output")
        if args.output.absolute().is_relative_to(args.target.absolute()):
            parser.error("preview output must be outside supplier")
        result = preview(args.target)
        _check_existing_chain(args.output.absolute())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(json.dumps({"mode": "preview", "blockers": result["blockers"],
                          "originals": len(result["originals"]), "install": len(result["install"])}))
    else:
        if args.plan is None or args.run_id is None:
            parser.error("operation requires --plan and --run-id")
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        result = (apply(plan, args.run_id, authority=args.authority) if args.mode == "apply"
                  else verify(plan, args.run_id) if args.mode == "verify" else undo(plan, args.run_id))
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
