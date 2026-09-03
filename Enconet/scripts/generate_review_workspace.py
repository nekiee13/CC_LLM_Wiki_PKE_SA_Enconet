#!/usr/bin/env python3
"""Render a self-contained offline run-selection workspace from a validated catalog."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

import validate_review_catalog


ENCONET = Path(__file__).resolve().parents[1]
TEMPLATE = ENCONET / "templates" / "review-workspace-template.html"
CATALOG = ENCONET / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"
OUTPUT = CATALOG.with_name("review_workspace.html")
KINDS = ("viewer", "report", "bundle", "package")
LABELS = {"viewer": "Open Evidence Explorer", "report": "Open report", "bundle": "Evidence bundle", "package": "Evaluation package"}


def _script_json(value: object) -> str:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            .replace("&", "\\u0026").replace("<", "\\u003c")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def _artifact_state(artifact: dict, output_path: Path, project_root: Path) -> dict:
    root = project_root.resolve()
    target = (root / Path(artifact["path"])).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return {**artifact, "available": False, "reason": "path outside project"}
    if not target.is_file():
        return {**artifact, "available": False, "reason": "file missing"}
    try:
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
    except OSError:
        return {**artifact, "available": False, "reason": "file unreadable"}
    if actual != artifact["sha256"]:
        return {**artifact, "available": False, "reason": "hash mismatch"}
    relative = os.path.relpath(target, output_path.resolve().parent).replace("\\", "/")
    href = "/".join(quote(part, safe="._-") for part in relative.split("/"))
    return {**artifact, "available": True, "href": href}


def _view_model(catalog: dict, output_path: Path, project_root: Path) -> dict:
    rows = []
    for row in catalog["runs"]:
        artifacts = {
            kind: _artifact_state(row["artifacts"][kind], output_path, project_root)
            for kind in KINDS
        }
        rows.append({**row, "artifacts": artifacts,
                     "available": all(item["available"] for item in artifacts.values())})
    return {"schema_version": "1.0", "runs": rows}


def _card(row: dict, *, initially_open: bool) -> str:
    escape = html.escape
    run_id = escape(row["run_id"])
    detail_id = f"run-details-{run_id}"
    availability = "available" if row["available"] else "unavailable"
    search = escape(" ".join(str(row[key]) for key in (
        "supplier", "framework", "run_id", "language", "status"
    )).casefold(), quote=True)
    items = []
    hashes = []
    for kind in KINDS:
        artifact = row["artifacts"][kind]
        hashes.append(
            f"<li><strong>{escape(kind)}</strong>: <code>{escape(artifact['sha256'])}</code></li>"
        )
        if artifact["available"]:
            items.append(
                f'<li><a data-artifact="{kind}" href="{escape(artifact["href"], quote=True)}">'
                f'{escape(LABELS[kind])}</a></li>'
            )
        else:
            items.append(
                f'<li class="unavailable">{escape(LABELS[kind])}: '
                f'Unavailable: {escape(artifact["reason"])}</li>'
            )
    hidden = "" if initially_open else " hidden"
    expanded = "true" if initially_open else "false"
    return (
        f'<article class="run-card" data-run-id="{run_id}" data-status="{escape(row["status"])}" '
        f'data-availability="{availability}" data-search="{search}">'
        f'<button type="button" class="run-select" aria-expanded="{expanded}" aria-controls="{detail_id}">'
        f'<span class="run-title">{escape(row["supplier"])} · {escape(row["framework"])} · {run_id}</span>'
        f'<span class="status status-{escape(row["status"])}">{escape(row["status"])}</span></button>'
        f'<div class="run-details" id="{detail_id}"{hidden}>'
        f'<p>Language: <strong>{escape(row["language"])}</strong> · Generated: '
        f'<time>{escape(row["generated_at_utc"])}</time></p>'
        f'<ul class="artifact-list">{"".join(items)}</ul>'
        f'<details class="hashes"><summary>Artifact hashes</summary><ul>{"".join(hashes)}</ul></details>'
        f'</div></article>'
    )


def render(
    catalog: dict,
    *,
    output_path: Path,
    project_root: Path = ENCONET,
    template: Path = TEMPLATE,
    validate_catalog: bool = True,
) -> str:
    if validate_catalog:
        errors = validate_review_catalog.validate(catalog)
        if errors:
            raise ValueError("invalid review catalog: " + errors[0])
    model = _view_model(catalog, output_path, project_root)
    cards = "".join(
        _card(row, initially_open=len(model["runs"]) == 1) for row in model["runs"]
    ) or '<p class="empty">No registered review runs are available.</p>'
    source = template.read_text(encoding="utf-8")
    for marker in ("__RUN_CARDS__", "__REVIEW_CATALOG__"):
        if source.count(marker) != 1:
            raise ValueError(f"review workspace template marker invalid: {marker}")
    return (source.replace("__RUN_CARDS__", cards)
            .replace("__REVIEW_CATALOG__", _script_json(model)).rstrip() + "\n")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", prefix=f".{path.name}.",
            suffix=".tmp", dir=path.parent, delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--project-root", type=Path, default=ENCONET)
    args = parser.parse_args(argv)
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        content = render(catalog, output_path=args.output, project_root=args.project_root)
        from validate_review_workspace import validate
        errors = validate(catalog, content)
        if errors:
            raise ValueError(errors[0])
        _atomic_write(args.output, content)
        print(f"generate_review_workspace: PASS - {len(catalog['runs'])} run(s) - {args.output}")
        return 0
    except Exception as exc:  # noqa: BLE001 - controlled generation boundary
        print(f"generate_review_workspace: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
