#!/usr/bin/env python3
"""Render a deterministic, gate-controlled EPIC11 evaluation report from one package."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import yaml
from pathlib import Path

import db_util
import citation_renderer
import evidence_access_policy
from build_evaluation_package import validate_package, validate_source
from finding_workflow import APPROVALS, render_template

PROJECT = Path(__file__).resolve().parents[1]
TEMPLATE = PROJECT / "templates" / "evaluation-report-template.md"
OUTPUTS = PROJECT / "outputs"

HEADINGS = {
    "en": ["Executive Summary", "Scope and Source Documents", "Method", "Coverage Summary",
           "Criterion-by-Criterion Evaluation", "Gap Analysis", "Priority Verification Actions",
           "Recommendations", "Consolidated Conformance Score", "Limitations", "Appendix: Evidence Matrix"],
    "sl": ["Povzetek", "Obseg in izvorni dokumenti", "Metoda", "Povzetek pokritosti",
           "Vrednotenje po merilih", "Analiza vrzeli", "Prednostni ukrepi preverjanja",
           "Priporočila", "Skupna ocena skladnosti", "Omejitve", "Priloga: matrika dokazov"],
    "hr": ["Sažetak", "Opseg i izvorni dokumenti", "Metoda", "Sažetak pokrivenosti",
           "Ocjenjivanje po kriterijima", "Analiza nedostataka", "Prioritetne radnje provjere",
           "Preporuke", "Ukupna ocjena sukladnosti", "Ograničenja", "Prilog: matrica dokaza"],
}

TEXT = {
    "en": {"title": "Appendix B Evaluation Report", "language": "Report language",
           "summary": "The package records {count} applicable criteria and a consolidated classification of **{classification}**.",
           "method": "Generated deterministically from evaluation package schema {schema}; findings and actions require manifest-backed approval.",
           "none_findings": "No approved findings are present.", "none_actions": "No approved priority actions are present.",
           "limitations": "Only evidence and human approvals contained in the package are represented; verbatim evidence remains unchanged."},
    "sl": {"title": "Poročilo o vrednotenju Dodatka B", "language": "Jezik poročila",
           "summary": "Paket vsebuje {count} veljavnih meril in skupno razvrstitev **{classification}**.",
           "method": "Poročilo je deterministično ustvarjeno iz paketa vrednotenja sheme {schema}; ugotovitve in ukrepi zahtevajo odobritev v manifestu.",
           "none_findings": "Odobrenih ugotovitev ni.", "none_actions": "Odobrenih prednostnih ukrepov ni.",
           "limitations": "Prikazani so samo dokazi in človeške odobritve iz paketa; dobesedni dokazi ostanejo nespremenjeni."},
    "hr": {"title": "Izvješće o ocjeni Dodatka B", "language": "Jezik izvješća",
           "summary": "Paket sadrži {count} primjenjivih kriterija i ukupnu klasifikaciju **{classification}**.",
           "method": "Izvješće je deterministički izrađeno iz paketa ocjene sheme {schema}; nalazi i radnje zahtijevaju odobrenje u manifestu.",
           "none_findings": "Nema odobrenih nalaza.", "none_actions": "Nema odobrenih prioritetnih radnji.",
           "limitations": "Prikazani su samo dokazi i ljudska odobrenja iz paketa; doslovni dokazi ostaju nepromijenjeni."},
}


def canonical_bytes(package: dict) -> bytes:
    return (json.dumps(package, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def approved_ids(package: dict) -> set[str]:
    return {row.get("object_id", "") for row in package.get("approvals", [])
            if row.get("decision", "").casefold() == "approved"
            and row.get("date") and row.get("reviewer")}


def require_report_gates(package: dict) -> None:
    run_id = package.get("run", {}).get("run_id", "")
    approved = approved_ids(package)
    missing = [gate for gate in ("G2", "G3", "G4") if f"{gate}-{run_id}" not in approved]
    if missing:
        raise ValueError(f"approved {'/'.join(missing)} report gate(s) missing for {run_id}")


def portable_viewer_path(report_output: Path, viewer_output: Path) -> str:
    """Return a relocation-safe viewer path for two sibling package artifacts."""
    report = report_output.resolve()
    viewer = viewer_output.resolve()
    if report.parent != viewer.parent:
        raise ValueError("report and evidence viewer must be sibling artifacts")
    return viewer.name


def _citation(row: dict, *, viewer_path: str | None = None) -> str:
    if row.get("evidence_item_id"):
        return citation_renderer.render(
            "crumb", row["evidence_item_id"], viewer_path=viewer_path
        )
    if row.get("gap_id"):
        return citation_renderer.render("gap", row["gap_id"], viewer_path=viewer_path)
    if row.get("finding_id"):
        return citation_renderer.render(
            "finding", row["finding_id"], viewer_path=viewer_path
        )
    return citation_renderer.render("source", "package", viewer_path=viewer_path)


def render(
    package: dict, template: Path = TEMPLATE, *, viewer_path: str | None = None,
    documentary: bool = False,
) -> str:
    errors = validate_package(package)
    if errors:
        raise ValueError("invalid evaluation package: " + "; ".join(errors))
    require_report_gates(package)
    run = package["run"]; language = run.get("deliverable_language")
    if language not in HEADINGS:
        raise ValueError("unsupported deliverable_language")
    headings, text = HEADINGS[language], TEXT[language]
    approvals = approved_ids(package)
    findings = sorted((row for row in package["findings"]
                       if row.get("status") == "approved" and row.get("finding_id") in approvals),
                      key=lambda row: row["finding_id"])
    actions = sorted((row for row in package["actions"]
                      if row.get("approval_status") == "approved"
                      and row.get("action_id") in approvals and row.get("priority")),
                     key=lambda row: row["action_id"])
    metrics = package["metrics"]
    metadata = {
        "schema_version": "1.0", "run_id": run["run_id"],
        "package_sha256": hashlib.sha256(canonical_bytes(package)).hexdigest(),
        "consolidated_score": metrics["consolidated_score"],
        "classification_counts": metrics["classification_counts"],
        "applicable_count": metrics["applicable_count"],
        "gap_ids": [row["gap_id"] for row in package["gaps"]],
        "approved_finding_ids": [row["finding_id"] for row in findings],
        "approved_action_ids": [row["action_id"] for row in actions],
        "language": language,
    }
    if documentary:
        metadata["report_variant"] = "documentary"
    applicability = {row["criterion_id"]: row for row in package["applicability"]}
    criterion_blocks = []
    evaluations = package["evaluations"]
    if documentary:
        taxonomy = yaml.safe_load((PROJECT / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))["criteria"]
        order = {item["criterion_id"]: index for index, item in enumerate(taxonomy)}
        evaluations = sorted(evaluations, key=lambda row: order[row["criterion_id"]])
    for row in evaluations:
        ruling = applicability.get(row["criterion_id"], {})
        evidence = " ".join(
            citation_renderer.render("crumb", item, viewer_path=viewer_path)
            for item in row.get("evidence_ids", [])
        ) or citation_renderer.render("source", "package", viewer_path=viewer_path)
        evaluation = citation_renderer.render(
            "evaluation", row["evaluation_id"], label=row["criterion_id"],
            viewer_path=viewer_path,
        )
        document = citation_renderer.render(
            "document", ruling.get("scope_source_doc_id", ""), viewer_path=viewer_path,
        )
        if documentary:
            if ruling.get("applicable") and not isinstance(row.get("score"), (int, float)):
                raise ValueError(f"documentary report requires a stored score: {row['criterion_id']}")
            labels = {
                "hr": ("Bodovi", "Rang", "Odobrena primjenjivost", "Izvorno obrazloženje opsega", "U prilog", "Ograničenje", "Zaključak", "Dokazi"),
                "sl": ("Točke", "Rang", "Odobrena uporabnost", "Izvirna utemeljitev obsega", "V prid", "Omejitev", "Sklep", "Dokazi"),
                "en": ("Points", "Rank", "Approved applicability", "Original scope justification", "Affirmative", "Limitation", "Judgment", "Evidence"),
            }[language]
            rank = {"fully": "5/5", "substantially": "4/5", "partially": "3/5",
                    "minimally": "2/5", "unmet": "1/5"}.get(row["classification"], "n-a")
            criterion_blocks.append(
                f"### {evaluation} — {row.get('criterion_name', '')}\n\n"
                f"- classification: `{row['classification']}`\n"
                f"- {labels[0]}: {row.get('score') if row.get('score') is not None else 'n-a'} / 100; {labels[1]}: {rank}\n"
                f"- {labels[2]}: `{'applicable' if ruling.get('applicable') else 'not-applicable'}`\n"
                f"- {labels[3]}: {ruling.get('justification', 'n-a')} {document}\n\n"
                f"**{labels[4]}:** {row.get('affirmative_summary', '')}\n\n"
                f"**{labels[5]}:** {row.get('contrary_summary', '')}\n\n"
                f"**{labels[6]}:** {row.get('judge_ruling', '')}\n\n"
                f"**{labels[7]}:** {evidence}"
            )
            continue
        criterion_blocks.append(
            f"### {evaluation} — {row.get('criterion_name', '')}\n\n"
            f"- classification: `{row['classification']}`\n"
            f"- applicability: `{'applicable' if ruling.get('applicable') else 'not-applicable'}`\n"
            f"- justification: {ruling.get('justification', 'n-a')} {document}\n"
            f"- rationale: {row.get('rationale', '')} {evidence}"
        )
    gap_lines = [
        f"- {citation_renderer.render('gap', row['gap_id'], viewer_path=viewer_path)} (gap context): "
        f"{row['description']} {_citation(row, viewer_path=viewer_path)}"
        for row in package["gaps"]
    ]
    action_lines = [
        f"- {citation_renderer.render('action', row['action_id'], viewer_path=viewer_path)}: "
        f"{row['description']} {_citation(row, viewer_path=viewer_path)}" for row in actions
    ]
    finding_lines = [
        f"- {citation_renderer.render('finding', row['finding_id'], viewer_path=viewer_path)}: "
        f"{row['title']} — {row['body']} {_citation(row, viewer_path=viewer_path)}"
        for row in findings
    ]
    if documentary:
        # A multiline finding must cite its gap/evidence on the primary line,
        # not only after the last paragraph; the validator enforces that defense.
        finding_lines = [
            f"- {citation_renderer.render('finding', row['finding_id'], viewer_path=viewer_path)}: "
            f"{row['title']} {_citation(row, viewer_path=viewer_path)}\n\n{row['body']}"
            for row in findings
        ]
    counts = ["| classification | count |", "|---|---:|"] + [
        f"| {name} | {count} |" for name, count in sorted(metrics["classification_counts"].items())
    ]
    appendix = ["| criterion | classification | evidence |", "|---|---|---|"] + [
        f"| {row['criterion_id']} | {row['classification']} | "
        f"{' '.join(citation_renderer.render('crumb', item, viewer_path=viewer_path) for item in row.get('evidence_ids', [])) or citation_renderer.render('source', 'package', viewer_path=viewer_path)} |"
        for row in evaluations
    ]
    values = {
        "report_metadata": json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        "report_title": f"{text['title']} — {run.get('supplier', '')}",
        "language_line": f"**{text['language']}:** `{language}`",
        "executive_summary": text["summary"].format(count=metrics["applicable_count"], classification=metrics["classification"]),
        "scope": f"- run_id: `{run['run_id']}`\n- supplier: `{run.get('supplier', '')}`\n- scoring_model_version: `{run.get('scoring_model_version', '')}`",
        "method": text["method"].format(schema=package["schema_version"]),
        "coverage": "\n".join(counts), "criteria": "\n\n".join(criterion_blocks),
        "gaps": "\n".join(gap_lines) or f"- none {citation_renderer.render('source', 'package', viewer_path=viewer_path)}",
        "actions": "\n".join(action_lines) or text["none_actions"],
        "recommendations": "\n".join(finding_lines) or text["none_findings"],
        "score": f"**{metrics['consolidated_score']} / 100** — **{metrics['applicable_count']}** applicable criteria (`{metrics['classification']}`).",
        "limitations": text["limitations"], "appendix": "\n".join(appendix),
    }
    if documentary:
        notice = {
            "hr": "Dokumentacijska pretprocjena dobavljačeva QA sustava prema 10 CFR 50 Appendix B, uz odabranu ASME NQA-1 interpretaciju. Part 21 je zaseban skup, izvan ovog zbroja. Ovo nije potvrda terenske provedbe. Izvorni kalkulacijski model/run stamp ostaje povijesna provenance; ne označava sadašnji status odobrenja. Izvorna radna rationale ostaje u paketu i zapisu ocjene, dok ovaj izvještaj prikazuje odobrene argumente i zaključak. Bodovi su pohranjeni rezultat; rang5/5 nije postotna formula.",
            "sl": "Dokumentacijska predpresoja dobaviteljevega QA sistema po 10 CFR 50 Appendix B z izbrano ASME NQA-1 razlago. Part 21 je ločen, zunaj te ocene. To ni potrditev izvajanja na terenu. Izvirni zapis modela ostane zgodovinska sled, ne trenutni status odobritve. Izvirna rationale ostane v paketu; prikazani so odobreni argumenti in sklep. Točke so shranjen rezultat; rang5/5 ni odstotna formula.",
            "en": "Documentary pre-flight evaluation of the supplier QA system against 10 CFR 50 Appendix B using the selected ASME NQA-1 interpretation. Part 21 is separate and excluded from this score. This does not certify field implementation. The original calculation model/run stamp is historical provenance, not current approval status. Original rationale remains in the package/evaluation record; this report displays approved arguments and judgment. Points are stored results; rank5/5 is not a percentage formula.",
        }[language]
        gate_rows = {r['object_id']: r for r in package['approvals'] if r.get('object_id') in {f'G{n}-{run["run_id"]}' for n in (2,3,4)}}
        lines = []
        for number in (2, 3, 4):
            gate = gate_rows[f"G{number}-{run['run_id']}"]
            lines.append(f"- G{number}: approved — `{gate['object_id']}`; {gate['date']}")
        values["executive_summary"] += f"\n\n**{metrics['consolidated_score']} / 100**, {metrics['applicable_count']} applicable criteria.\n\n" + "\n".join(lines)
        values["method"] += "\n\n" + notice
        values["limitations"] += "\n\n" + notice
    for index, key in enumerate(("executive_summary", "scope", "method", "coverage", "criteria", "gaps", "actions", "recommendations", "score", "limitations", "appendix")):
        values[f"heading_{key}"] = headings[index]
    return render_template(template, values).rstrip() + "\n"


def default_output(package: dict) -> Path:
    supplier = re.sub(r"[^a-z0-9_-]+", "-", package["run"].get("supplier", "supplier").casefold()).strip("-")
    return OUTPUTS / f"{supplier}_appendix_b_evaluation_report.md"


def _atomic_write_text(path: Path, content: str) -> None:
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
    parser.add_argument("package", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--viewer-output", type=Path,
        help="sibling evidence viewer for a portable candidate report",
    )
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    parser.add_argument("--documentary", action="store_true",
                        help="show approved documentary arguments and stored criterion scores; keep original provenance unchanged")
    args = parser.parse_args(argv)
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"))
        source_errors = validate_source(package, args.db, args.approvals)
        if source_errors:
            raise ValueError(source_errors[0])
        output = args.output or default_output(package)
        if args.viewer_output is not None:
            if args.output is None:
                raise ValueError("--output is required with --viewer-output")
            output = output.resolve()
            viewer_output = args.viewer_output.resolve()
            evidence_access_policy.require_output_target(output)
            expected = evidence_access_policy.candidate_path(
                package["run"]["run_id"], output.name
            ).resolve()
            if output != expected:
                raise evidence_access_policy.PolicyError(
                    f"candidate output must be directly under the selected run directory: {expected}"
                )
            viewer_path = portable_viewer_path(output, viewer_output)
            content = render(package, viewer_path=viewer_path, documentary=args.documentary)
            _atomic_write_text(output, content)
        else:
            evidence_access_policy.require_output_target(output)
            content = render(package, documentary=args.documentary)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content, encoding="utf-8", newline="\n")
        print(f"generate_report: PASS - {output}")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI fail-closed boundary
        print(f"generate_report: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
