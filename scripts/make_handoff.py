"""Validate and atomically publish project handoffs (ALIGNMENT_PLAN C3).

The schema file is JSON-compatible YAML so the helper remains stdlib-only.
Paths resolve from this script, never the caller's CWD.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
DEFAULT_PROJECT = WORKSPACE / "Enconet"
SCHEMA_PATH = WORKSPACE / "handoff_schema.yml"
HEADINGS = [
    "Objective and Phase", "Completed Work", "Decisions", "Validation Evidence",
    "Repository and Index State", "Blockers and Risks",
    "Uncommitted or Generated Artifacts", "Exact Next Action", "Follow-up Queue",
]


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def run(command: list[str], cwd: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8",
                           errors="replace", capture_output=True, timeout=20)
        return p.returncode, (p.stdout or p.stderr).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, str(exc)


def git_facts(project: Path) -> dict:
    rc, root = run(["git", "rev-parse", "--show-toplevel"], project)
    if rc:
        return {"available": False, "head": "unavailable", "short": "nogit",
                "warning": "WARNING: Git metadata unavailable; record is not SHA-certified."}
    root_path = Path(root)
    _, head = run(["git", "rev-parse", "HEAD"], root_path)
    _, branch = run(["git", "branch", "--show-current"], root_path)
    _, status = run(["git", "status", "--short"], root_path)
    _, upstream = run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], root_path)
    _, remote = run(["git", "remote", "get-url", "origin"], root_path)
    return {"available": True, "root": root, "head": head, "short": head[:7],
            "branch": branch or "detached", "detached": not bool(branch),
            "dirty": bool(status), "status": status or "clean",
            "upstream": upstream or "not-configured", "remote": remote or "not-configured"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        raise ValueError("missing frontmatter block")
    data = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, text[m.end():]


def validate_text(text: str, path: Path | None = None,
                  schema_path: Path = SCHEMA_PATH) -> list[str]:
    errors = []
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fm, body = parse_frontmatter(text)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]
    for key in schema["required_frontmatter"]:
        if not fm.get(key):
            errors.append(f"missing frontmatter field: {key}")
    if fm.get("record_type") != schema["record_type"]:
        errors.append("record_type must be handoff")
    if fm.get("schema_version") != str(schema["schema_version"]):
        errors.append("unsupported schema_version")
    if fm.get("status") not in schema["status_values"]:
        errors.append("invalid overall status")
    try:
        created = datetime.strptime(fm.get("created_at_utc", ""), "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        errors.append("created_at_utc must be UTC ISO-8601")
        created = None
    positions = []
    for heading in schema["required_headings"]:
        matches = list(re.finditer(rf"(?m)^## {re.escape(heading)}\s*$", body))
        if len(matches) != 1:
            errors.append(f"heading must occur exactly once: {heading}")
        else:
            positions.append(matches[0].start())
    if positions != sorted(positions):
        errors.append("required headings are out of order")
    try:
        checks = json.loads(fm.get("validation_checks_json", "[]"))
        if not isinstance(checks, list):
            raise ValueError
        for i, check in enumerate(checks):
            state = check.get("state")
            if state not in schema["check_state_values"]:
                errors.append(f"check {i}: invalid state")
            if state == "passed" and (not check.get("command") or
                                       not isinstance(check.get("exit_code"), int)):
                errors.append(f"check {i}: passed requires command and integer exit_code")
    except (json.JSONDecodeError, ValueError, AttributeError):
        errors.append("validation_checks_json must be a JSON array of objects")
    if path and created:
        suffix = "nogit" if fm.get("git_head") == "unavailable" else fm.get("git_head", "")[:7]
        expected = created.strftime("%Y-%m-%dT%H%M%SZ") + f"-{suffix}.md"
        if path.name != expected:
            errors.append(f"filename does not match record identity: expected {expected}")
    return errors


def read_optional(path: Path, label: str) -> str:
    if not path.is_file():
        return f"- {label}: not-configured (`{path.name}` missing)."
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return f"- {label}: configured; tail: " + " / ".join(lines[-3:])


def unique_timestamp(directory: Path, stamp: datetime, suffix: str) -> datetime:
    while (directory / f"{stamp.strftime('%Y-%m-%dT%H%M%SZ')}-{suffix}.md").exists():
        stamp += timedelta(seconds=1)
    return stamp


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def render(args, project: Path, facts: dict, created: datetime, checks: list[dict]) -> str:
    check_json = json.dumps(checks, ensure_ascii=False, separators=(",", ":"))
    git_lines = ([f"- Git root: `{facts['root']}`; branch: `{facts['branch']}`; HEAD: `{facts['head']}`.",
                  f"- Upstream: `{facts['upstream']}`; remote: `{facts['remote']}`; worktree: {'dirty' if facts['dirty'] else 'clean'}."]
                 if facts["available"] else [f"- {facts['warning']}"])
    validation = [f"- **{c.get('state', 'unknown')}** — {c.get('name', 'unnamed')}: "
                  f"command={c.get('command', 'not-run')!r}; exit_code={c.get('exit_code', 'not-run')}; "
                  f"{c.get('summary', '')}" for c in checks] or ["- No validation checks supplied (`unknown`)."]
    sections = {
        "Objective and Phase": args.objective,
        "Completed Work": "\n".join(f"- {x}" for x in args.completed) or "- None recorded.",
        "Decisions": "\n".join(f"- {x}" for x in args.decision) or "- None recorded.",
        "Validation Evidence": "\n".join(validation),
        "Repository and Index State": "\n".join(git_lines + [
            read_optional(project / "current-status.md", "current status"),
            read_optional(project / "project-state.yml", "project state"),
            f"- Index metadata: {args.index_state}. Stale when its recorded HEAD differs from `{facts['head']}`.",
        ]),
        "Blockers and Risks": "\n".join(f"- {x}" for x in args.blocker) or "- None recorded.",
        "Uncommitted or Generated Artifacts": ("- Worktree changes were present at collection time." if facts.get("dirty") else "- None detected by Git."),
        "Exact Next Action": args.next_action,
        "Follow-up Queue": "\n".join(f"{i}. {x}" for i, x in enumerate(args.follow_up, 1)) or "1. None recorded.",
    }
    fm = ["---", "record_type: handoff", "schema_version: 1",
          f"project: {args.project_id}", f"created_at_utc: {created.strftime('%Y-%m-%dT%H:%M:%SZ')}",
          f"status: {args.status}", f"git_head: {facts['head']}",
          f"source_agent: {args.source_agent}", f"validation_checks_json: {check_json}", "---", "",
          f"# Handoff — {created.strftime('%Y-%m-%dT%H:%M:%SZ')}", ""]
    body = []
    for heading in HEADINGS:
        body += [f"## {heading}", "", sections[heading], ""]
    if not (project / "wiki" / "log.md").is_file():
        body += ["`log_update: not-configured` (no `wiki/log.md` exists).", ""]
    return "\n".join(fm + body)


def publish(args) -> Path:
    project = Path(args.project_root).resolve()
    facts = git_facts(project)
    checks = [parse_check(value) for value in args.check]
    handoffs = project / "handoffs"
    created = unique_timestamp(handoffs, now_utc(), facts["short"])
    record = handoffs / f"{created.strftime('%Y-%m-%dT%H%M%SZ')}-{facts['short']}.md"
    text = render(args, project, facts, created, checks)
    errors = validate_text(text, record)
    if errors:
        raise ValueError("; ".join(errors))
    atomic_write(record, text)
    rel = record.relative_to(project).as_posix()
    pointer = (f"# HANDOFF (pointer)\n\n**Authoritative record:** [`{rel}`]({rel})\n\n"
               f"**Status:** {args.status} · **Git:** `{facts['short']}` · "
               f"**Agent:** {args.source_agent} · **Created:** {created.strftime('%Y-%m-%dT%H:%M:%SZ')}\n\n"
               f"**Exact next action:** {args.next_action}\n")
    atomic_write(project / "HANDOFF.md", pointer)
    log = project / "wiki" / "log.md"
    if log.is_file():
        with log.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(f"\n- handoff-created | {created.strftime('%Y-%m-%dT%H:%M:%SZ')} | {rel} | {args.status} | {facts['head']}\n")
    return record


def parse_check(value: str) -> dict:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        parts = value.split("|", 4)
        if len(parts) != 5:
            raise ValueError("--check must be JSON or state|name|command|exit_code|summary")
        state, name, command, exit_code, summary = parts
        return {"state": state, "name": name, "command": command or None,
                "exit_code": int(exit_code) if exit_code else None, "summary": summary}


def check_staleness(project: Path) -> int:
    pointer = project / "HANDOFF.md"
    if not pointer.is_file():
        print("WARN: HANDOFF.md is missing")
        return 0
    match = re.search(r"\((handoffs/[^)]+\.md)\)", pointer.read_text(encoding="utf-8"))
    if not match or not (project / match.group(1)).is_file():
        print("WARN: HANDOFF.md does not resolve to an immutable record")
        return 0
    record = project / match.group(1)
    fm, _ = parse_frontmatter(record.read_text(encoding="utf-8"))
    current = git_facts(project)["head"]
    if fm.get("git_head") != current:
        print(f"WARN: handoff is stale (recorded {fm.get('git_head')}, current {current})")
        return 0
    print("handoff staleness: current")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--validate", metavar="RECORD")
    p.add_argument("--check-staleness", action="store_true")
    p.add_argument("--project-root", default=str(DEFAULT_PROJECT))
    p.add_argument("--project-id", default="PKE_SA_NQA1/Enconet")
    p.add_argument("--source-agent", choices=["codex", "claude-code"], default="codex")
    p.add_argument("--status", choices=["complete", "partial", "blocked"], default="partial")
    p.add_argument("--objective", default="Continuation state collected by make_handoff.py.")
    p.add_argument("--completed", action="append", default=[])
    p.add_argument("--decision", action="append", default=[])
    p.add_argument("--check", action="append", default=[], help="JSON or state|name|command|exit_code|summary")
    p.add_argument("--index-state", default="unknown (no machine-readable jmunch metadata supplied)")
    p.add_argument("--blocker", action="append", default=[])
    p.add_argument("--next-action", default="Review this handoff and choose the next task.")
    p.add_argument("--follow-up", action="append", default=[])
    return p


def main() -> int:
    args = parser().parse_args()
    if args.check_staleness:
        return check_staleness(Path(args.project_root).resolve())
    if args.validate:
        path = Path(args.validate)
        errors = validate_text(path.read_text(encoding="utf-8"), path)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"handoff validation: {len(errors)} error(s)")
        return 1 if errors else 0
    try:
        path = publish(args)
        print(f"Published {path}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
