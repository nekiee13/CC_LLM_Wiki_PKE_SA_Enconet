#!/usr/bin/env python3
"""Validate every portable report citation against its matched offline viewer."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import evidence_navigation
import generate_report
import validate_evidence_bundle
import validate_report


PROJECT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[([^\]\r\n]+)\]\(([^)\r\n]+)\)")
TYPED_LABEL = re.compile(
    r"\[(?:crumb|document|evaluation|gap|finding|action|source):[^\]\r\n]+\]"
)
REPORT_META = re.compile(r"<!-- report-metadata: (\{.*?\}) -->")
RENDERED_COLLECTIONS = {
    "document": ("documents", "document_id"),
    "evaluation": ("evaluations", "evaluation_id"),
    "crumb": ("crumbs", "crumb_id"),
    "gap": ("gaps", "gap_id"),
    "finding": ("findings", "finding_id"),
    "action": ("actions", "action_id"),
}


@dataclass(frozen=True)
class EvidenceLink:
    """One source-located Markdown evidence link."""

    label: str
    href: str
    target: str
    entity_type: str
    entity_id: str
    line: int
    column: int


def _location(path: Path, text: str, offset: int) -> str:
    line = text.count("\n", 0, offset) + 1
    last_newline = text.rfind("\n", 0, offset)
    column = offset - last_newline
    return f"{path}:{line}:{column}"


def parse_evidence_links(
    report: str, report_path: Path
) -> tuple[list[EvidenceLink], list[str]]:
    """Parse evidence links and source-locate malformed citation markup."""
    links: list[EvidenceLink] = []
    errors: list[str] = []
    matches = list(LINK.finditer(report))
    href_spans = [(match.start(2), match.end(2)) for match in matches]
    link_spans = [(match.start(), match.end()) for match in matches]

    for occurrence in re.finditer(r"#evidence/", report):
        if not any(start <= occurrence.start() < end for start, end in href_spans):
            errors.append(
                f"{_location(report_path, report, occurrence.start())}: "
                "malformed evidence Markdown URL"
            )
    for occurrence in TYPED_LABEL.finditer(report):
        if not any(start <= occurrence.start() < end for start, end in link_spans):
            errors.append(
                f"{_location(report_path, report, occurrence.start())}: "
                "typed evidence label is not a Markdown link"
            )

    for match in matches:
        label, href = match.groups()
        if "#evidence/" not in href:
            continue
        location = _location(report_path, report, match.start(2))
        parsed_url = urlsplit(href)
        target = f"#{parsed_url.fragment}" if parsed_url.fragment else ""
        parsed_target = evidence_navigation.parse(target)
        if (
            parsed_url.scheme or parsed_url.netloc or parsed_url.query
            or not parsed_url.path or parsed_target is None
        ):
            errors.append(f"{location}: malformed evidence Markdown URL")
            continue
        entity_type, entity_id = parsed_target
        links.append(EvidenceLink(
            label=label, href=href, target=target, entity_type=entity_type,
            entity_id=entity_id, line=int(location.rsplit(":", 2)[1]),
            column=int(location.rsplit(":", 1)[1]),
        ))
    return links, errors


class _EvidenceScriptParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.capturing = False
        self.records: list[tuple[str, str, str]] = []
        self._script_id = ""
        self._hash = ""
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        script_id = attributes.get("id")
        if tag == "script" and script_id in {"dashboard-data", "evidence-bundle"}:
            self.capturing = True
            self._script_id = script_id
            self._hash = attributes.get("data-sha256") or ""
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self.capturing:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capturing:
            self.records.append((self._script_id, self._hash, "".join(self._parts)))
            self.capturing = False


def _extract_bundle(viewer: str, viewer_path: Path, errors: list[str]) -> dict | None:
    parser = _EvidenceScriptParser()
    try:
        parser.feed(viewer)
    except Exception as exc:  # noqa: BLE001 - malformed artifact boundary
        errors.append(f"{viewer_path}: malformed viewer HTML: {exc}")
        return None
    evidence_records = [record for record in parser.records if record[0] == "evidence-bundle"]
    if len(evidence_records) != 1:
        errors.append(
            f"{viewer_path}: expected exactly one embedded evidence bundle; "
            f"found {len(evidence_records)}"
        )
        return None
    _script_id, declared_hash, payload = evidence_records[0]
    try:
        bundle = json.loads(payload)
    except json.JSONDecodeError as exc:
        errors.append(f"{viewer_path}: embedded evidence bundle is invalid JSON: {exc.msg}")
        return None
    actual_hash = hashlib.sha256(
        validate_evidence_bundle.canonical_bytes(bundle)
    ).hexdigest()
    if declared_hash != actual_hash:
        errors.append(f"{viewer_path}: embedded evidence bundle hash mismatch")
    for error in validate_evidence_bundle.validate(bundle):
        errors.append(f"{viewer_path}: invalid evidence bundle: {error}")
    return bundle


def _extract_dashboard_data(
    viewer: str, viewer_path: Path, errors: list[str]
) -> dict | None:
    parser = _EvidenceScriptParser()
    parser.feed(viewer)
    records = [record for record in parser.records if record[0] == "dashboard-data"]
    if len(records) != 1:
        errors.append(
            f"{viewer_path}: expected exactly one dashboard metadata record; found {len(records)}"
        )
        return None
    try:
        return json.loads(records[0][2])
    except json.JSONDecodeError as exc:
        errors.append(f"{viewer_path}: dashboard metadata is invalid JSON: {exc.msg}")
        return None


def _metadata(report: str, report_path: Path, errors: list[str]) -> dict:
    matches = REPORT_META.findall(report)
    if len(matches) != 1:
        errors.append(
            f"{report_path}: expected exactly one report metadata record; found {len(matches)}"
        )
        return {}
    try:
        return json.loads(matches[0])
    except json.JSONDecodeError as exc:
        errors.append(f"{report_path}: report metadata is invalid JSON: {exc.msg}")
        return {}


def _target_index(bundle: dict, errors: list[str]) -> set[str]:
    targets = {"#evidence/source/package"}
    seen = {"#evidence/source/package"}
    for entity_type, (collection, _id_field) in RENDERED_COLLECTIONS.items():
        for row in bundle.get(collection, []):
            target = row.get("viewer_target")
            if isinstance(target, str):
                if target in seen:
                    errors.append(f"duplicate viewer target: {target}")
                seen.add(target)
                if evidence_navigation.parse(target) == (entity_type, row.get(_id_field)):
                    targets.add(target)
    return targets


def _lineage_errors(bundle: dict, project_root: Path) -> list[str]:
    errors: list[str] = []
    for name in sorted(bundle.get("lineage", {})):
        entry = bundle["lineage"].get(name, {})
        relative = entry.get("path")
        expected = entry.get("sha256")
        if not isinstance(relative, str):
            continue
        root = project_root.resolve()
        artifact = (root / Path(relative)).resolve()
        try:
            artifact.relative_to(root)
        except ValueError:
            errors.append(f"unsafe lineage artifact path: {name} ({relative})")
            continue
        if not artifact.is_file():
            errors.append(f"missing lineage artifact: {name} ({artifact})")
            continue
        try:
            actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
        except OSError as exc:
            errors.append(f"unreadable lineage artifact: {name} ({artifact}): {exc}")
            continue
        if actual != expected:
            errors.append(
                f"stale lineage artifact: {name} ({artifact}); "
                f"expected {expected}, got {actual}"
            )
    return errors


def validate(
    report: str,
    viewer: str,
    package: dict,
    *,
    report_path: Path,
    viewer_path: Path,
    package_path: Path,
    project_root: Path = PROJECT,
    verify_lineage: bool = True,
) -> list[str]:
    """Return deterministic publication-blocking errors for the artifact trio."""
    errors: list[str] = []
    for error in validate_report.validate(package, report):
        errors.append(f"{report_path}: {error}")
    report_metadata = _metadata(report, report_path, errors)
    bundle = _extract_bundle(viewer, viewer_path, errors)
    dashboard_data = _extract_dashboard_data(viewer, viewer_path, errors)
    links, link_errors = parse_evidence_links(report, report_path)
    errors.extend(link_errors)
    if bundle is None:
        return list(dict.fromkeys(errors))

    package_run = package.get("run", {})
    bundle_metadata = bundle.get("metadata", {})
    for field in ("run_id", "deliverable_language"):
        if report_metadata.get("run_id" if field == "run_id" else "language") != bundle_metadata.get(field):
            errors.append(f"report/viewer mismatch: {field}")
        if package_run.get(field) != bundle_metadata.get(field):
            errors.append(f"package/viewer mismatch: {field}")
        if dashboard_data is not None and dashboard_data.get(field) != bundle_metadata.get(field):
            errors.append(f"viewer metadata/bundle mismatch: {field}")
    if dashboard_data is not None and dashboard_data.get("supplier") != bundle_metadata.get("supplier"):
        errors.append("viewer metadata/bundle mismatch: supplier")
    if package_run.get("supplier") != bundle_metadata.get("supplier"):
        errors.append("package/viewer mismatch: supplier")

    package_hash = hashlib.sha256(package_path.read_bytes()).hexdigest()
    if bundle.get("lineage", {}).get("package", {}).get("sha256") != package_hash:
        errors.append("package/viewer mismatch: package lineage sha256")
    if verify_lineage:
        errors.extend(_lineage_errors(bundle, project_root))

    if report_path.resolve().parent != viewer_path.resolve().parent:
        errors.append("report and viewer are not sibling artifacts")
    expected_viewer_path = quote(viewer_path.name, safe="._-")
    known_targets = _target_index(bundle, errors)
    for link in links:
        location = f"{report_path}:{link.line}:{link.column}"
        parsed_url = urlsplit(link.href)
        if parsed_url.path != expected_viewer_path or unquote(parsed_url.path) != viewer_path.name:
            errors.append(
                f"{location}: evidence link does not target sibling viewer: {link.href}"
            )
        if link.target not in known_targets:
            errors.append(f"{location}: unknown evidence target: {link.target}")

    try:
        expected_report = generate_report.render(package, viewer_path=viewer_path.name)
        expected_links, expected_parse_errors = parse_evidence_links(
            expected_report, report_path
        )
        if expected_parse_errors:
            errors.append("internal error: deterministic report produced malformed evidence links")
        actual_counts = Counter(link.target for link in links)
        expected_counts = Counter(link.target for link in expected_links)
        for target in sorted(actual_counts.keys() | expected_counts.keys()):
            actual_count = actual_counts[target]
            expected_count = expected_counts[target]
            if actual_count > expected_count:
                occurrence = [link for link in links if link.target == target][expected_count]
                location = f"{report_path}:{occurrence.line}:{occurrence.column}"
                errors.append(
                    f"{location}: duplicate report citation: {target} "
                    f"(expected {expected_count}, got {actual_count})"
                )
            elif actual_count < expected_count:
                errors.append(
                    f"{report_path}: missing report citation: {target} "
                    f"(expected {expected_count}, got {actual_count})"
                )
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"cannot derive expected report citations: {exc}")
    return list(dict.fromkeys(errors))


def validate_paths(
    report_path: Path,
    viewer_path: Path,
    package_path: Path,
    *,
    project_root: Path = PROJECT,
    verify_lineage: bool = True,
) -> list[str]:
    """Read the artifact trio and return errors without raising at the CLI boundary."""
    for path, kind in (
        (report_path, "report"), (viewer_path, "viewer"), (package_path, "package")
    ):
        if not path.is_file():
            return [f"{path}: {kind} file is missing"]
    try:
        report = report_path.read_text(encoding="utf-8")
        viewer = viewer_path.read_text(encoding="utf-8")
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"artifact read failed: {exc}"]
    try:
        return validate(
            report, viewer, package, report_path=report_path, viewer_path=viewer_path,
            package_path=package_path, project_root=project_root,
            verify_lineage=verify_lineage,
        )
    except Exception as exc:  # noqa: BLE001 - CLI must fail closed on malformed artifacts
        return [f"artifact validation failed: {exc}"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("viewer", type=Path)
    parser.add_argument("package", type=Path)
    parser.add_argument("--project-root", type=Path, default=PROJECT)
    args = parser.parse_args(argv)
    errors = validate_paths(
        args.report, args.viewer, args.package, project_root=args.project_root
    )
    if errors:
        for error in errors:
            print(f"validate_report_links: FAIL - {error}", file=sys.stderr)
        return 1
    links, _malformed = parse_evidence_links(
        args.report.read_text(encoding="utf-8"), args.report
    )
    print(f"validate_report_links: PASS - {len(links)} evidence link(s)")
    return 0


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
