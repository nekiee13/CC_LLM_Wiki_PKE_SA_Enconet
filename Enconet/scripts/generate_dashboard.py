#!/usr/bin/env python3
"""Render and publish a self-contained EPIC12 dashboard from validated data."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

import yaml

import db_util
import evidence_access_policy
import validate_evidence_bundle
from build_dashboard_data import validate_data
from build_evaluation_package import validate_source
from finding_workflow import APPROVALS
from generate_report import require_report_gates

ENCONET = Path(__file__).resolve().parents[1]
TEMPLATE = ENCONET / "templates" / "dashboard-template.html"
EVIDENCE_BUDGETS = ENCONET / "schemas" / "evidence_access_budgets.yml"
OUTPUTS = ENCONET / "outputs"
WIKI = ENCONET / "wiki" / "dashboards"

UI = {
    "en": {"title":"Appendix B Evaluation Dashboard","kicker":"Offline audit dashboard","score":"Weighted score","applicable":"Applicable criteria","classification":"Classification","summary":"Executive summary","summary_text":"The package contains {count} applicable criteria with a weighted score of {score}.","distribution":"Classification distribution","filter":"Rating","search":"Search","sort":"Reverse order","expand":"Expand all","collapse":"Collapse all","print":"Print","criteria":"Criterion cards","matrix":"Evaluation matrix","actions":"Priority actions","details":"Show / hide details","affirmative":"Affirmative","contrary":"Contrary","judgement":"Judgement","none":"none","na":"n/a","all":"All ratings","id":"Criterion","name":"Name","rating":"Rating","criterion_score":"Score","evidence":"Evidence","none_actions":"No approved priority actions are present."},
    "sl": {"title":"Nadzorna plošča vrednotenja Dodatka B","kicker":"Nadzorna plošča za delo brez povezave","score":"Utežena ocena","applicable":"Veljavna merila","classification":"Razvrstitev","summary":"Povzetek","summary_text":"Paket vsebuje {count} veljavnih meril z uteženo oceno {score}.","distribution":"Porazdelitev razvrstitev","filter":"Ocena","search":"Iskanje","sort":"Obrni vrstni red","expand":"Razširi vse","collapse":"Strni vse","print":"Natisni","criteria":"Kartice meril","matrix":"Matrika vrednotenja","actions":"Prednostni ukrepi","details":"Prikaži / skrij podrobnosti","affirmative":"Pritrdilno","contrary":"Nasprotno","judgement":"Presoja","none":"brez","na":"ni relevantno","all":"Vse ocene","id":"Merilo","name":"Ime","rating":"Ocena","criterion_score":"Točke","evidence":"Dokazi","none_actions":"Odobrenih prednostnih ukrepov ni."},
    "hr": {"title":"Nadzorna ploča ocjene Dodatka B","kicker":"Izvanmrežna nadzorna ploča","score":"Ponderirana ocjena","applicable":"Primjenjivi kriteriji","classification":"Klasifikacija","summary":"Sažetak","summary_text":"Paket sadrži {count} primjenjivih kriterija s ponderiranom ocjenom {score}.","distribution":"Raspodjela klasifikacija","filter":"Ocjena","search":"Pretraži","sort":"Obrni redoslijed","expand":"Proširi sve","collapse":"Sažmi sve","print":"Ispiši","criteria":"Kartice kriterija","matrix":"Matrica ocjene","actions":"Prioritetne radnje","details":"Prikaži / sakrij pojedinosti","affirmative":"Potvrdno","contrary":"Suprotno","judgement":"Prosudba","none":"nema","na":"nije primjenjivo","all":"Sve ocjene","id":"Kriterij","name":"Naziv","rating":"Ocjena","criterion_score":"Bodovi","evidence":"Dokazi","none_actions":"Nema odobrenih prioritetnih radnji."},
}

EVIDENCE_UI = {
    "en": {"evidence_title": "Source evidence", "evidence_close": "Close evidence",
           "evidence_context": "Requested report record",
           "evidence_statement": "Statement", "evidence_document": "Source document",
           "evidence_traceability": "Traceability", "evidence_quotes": "Exact quotes",
           "evidence_chunk": "Source chapter", "evidence_unavailable": "Evidence unavailable",
           "previous_chunk": "Previous chapter", "next_chunk": "Next chapter",
           "confidence": "Confidence", "highlight_exact": "Exact match",
           "highlight_normalized": "Normalized match", "highlight_ambiguous": "Repeated match",
           "highlight_not_found": "Quote not found in this chapter",
           "highlight_outside_chunk": "Quote belongs to another chapter",
           "highlight_warning": "{count} quote highlight warning(s); quote records remain visible.",
           "evidence_actions": "Evidence record", "copy_citation": "Copy traceable citation",
           "print_evidence": "Print evidence", "citation_label": "Traceable citation",
           "copy_success": "Citation copied",
           "copy_fallback": "Copying was denied; the citation is selected below"},
    "sl": {"evidence_title": "Izvorni dokaz", "evidence_close": "Zapri dokaz",
           "evidence_context": "Zahtevani zapis poročila",
           "evidence_statement": "Trditev", "evidence_document": "Izvorni dokument",
           "evidence_traceability": "Sledljivost", "evidence_quotes": "Natančni navedki",
           "evidence_chunk": "Izvorno poglavje", "evidence_unavailable": "Dokaz ni na voljo",
           "previous_chunk": "Prejšnje poglavje", "next_chunk": "Naslednje poglavje",
           "confidence": "Zanesljivost", "highlight_exact": "Natančno ujemanje",
           "highlight_normalized": "Normalizirano ujemanje", "highlight_ambiguous": "Ponovljeno ujemanje",
           "highlight_not_found": "Navedka ni v tem poglavju",
           "highlight_outside_chunk": "Navedek pripada drugemu poglavju",
           "highlight_warning": "Opozorila pri označevanju navedkov: {count}; zapisi navedkov ostanejo vidni.",
           "evidence_actions": "Dokazni zapis", "copy_citation": "Kopiraj sledljiv navedek",
           "print_evidence": "Natisni dokaz", "citation_label": "Sledljiv navedek",
           "copy_success": "Navedek je kopiran",
           "copy_fallback": "Kopiranje ni dovoljeno; navedek je označen spodaj"},
    "hr": {"evidence_title": "Izvorni dokaz", "evidence_close": "Zatvori dokaz",
           "evidence_context": "Traženi zapis izvješća",
           "evidence_statement": "Tvrdnja", "evidence_document": "Izvorni dokument",
           "evidence_traceability": "Sljedivost", "evidence_quotes": "Točni citati",
           "evidence_chunk": "Izvorno poglavlje", "evidence_unavailable": "Dokaz nije dostupan",
           "previous_chunk": "Prethodno poglavlje", "next_chunk": "Sljedeće poglavlje",
           "confidence": "Pouzdanost", "highlight_exact": "Točno podudaranje",
           "highlight_normalized": "Normalizirano podudaranje", "highlight_ambiguous": "Ponovljeno podudaranje",
           "highlight_not_found": "Citat nije pronađen u ovom poglavlju",
           "highlight_outside_chunk": "Citat pripada drugom poglavlju",
           "highlight_warning": "Upozorenja pri označavanju citata: {count}; zapisi citata ostaju vidljivi.",
           "evidence_actions": "Zapis dokaza", "copy_citation": "Kopiraj sljedivi citat",
           "print_evidence": "Ispiši dokaz", "citation_label": "Sljedivi citat",
           "copy_success": "Citat je kopiran",
           "copy_fallback": "Kopiranje nije dopušteno; citat je označen ispod"},
}
for _language, _labels in EVIDENCE_UI.items():
    UI[_language].update(_labels)


def _script_json(value: object) -> str:
    serialized = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                  .replace("&", "\\u0026").replace("<", "\\u003c")
                  .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    return re.sub(
        "[\x7f-\x9f\u202a-\u202e\u2066-\u2069]",
        lambda match: f"\\u{ord(match.group()):04x}",
        serialized,
    )


def _bundle_hash(bundle: dict) -> str:
    return hashlib.sha256(validate_evidence_bundle.canonical_bytes(bundle)).hexdigest()


def _validate_bundle_for_dashboard(bundle: dict, data: dict) -> None:
    metadata = bundle.get("metadata", {})
    for field in ("run_id", "supplier", "deliverable_language"):
        if metadata.get(field) != data.get(field):
            raise ValueError(f"evidence bundle/dashboard mismatch: {field}")
    errors = validate_evidence_bundle.validate(bundle)
    if errors:
        raise ValueError("invalid evidence bundle: " + "; ".join(errors))
    budgets = yaml.safe_load(EVIDENCE_BUDGETS.read_text(encoding="utf-8"))
    bundle_bytes = len(validate_evidence_bundle.canonical_bytes(bundle))
    size_limit = budgets["size_bytes"]["bundle"]
    if bundle_bytes > size_limit:
        raise ValueError(f"bundle size budget exceeded: {bundle_bytes} > {size_limit}")
    for name, limit in budgets["projection_counts"].items():
        count = len(bundle[name])
        if count > limit:
            raise ValueError(f"{name} projection budget exceeded: {count} > {limit}")


def render(
    data: dict, template: Path = TEMPLATE, *, evidence_bundle: dict | None = None
) -> str:
    errors = validate_data(data)
    if errors:
        raise ValueError("invalid dashboard data: " + "; ".join(errors))
    language = data["deliverable_language"]
    if language not in UI:
        raise ValueError("unsupported deliverable_language")
    source = template.read_text(encoding="utf-8")
    markers = (
        "__DASHBOARD_DATA__", "__DASHBOARD_UI__", "__EVIDENCE_BUNDLE__",
        "__EVIDENCE_BUNDLE_SHA256__",
    )
    if any(source.count(marker) != 1 for marker in markers):
        raise ValueError("dashboard template injection markers are invalid")
    if evidence_bundle is not None:
        _validate_bundle_for_dashboard(evidence_bundle, data)
        evidence_hash = _bundle_hash(evidence_bundle)
    else:
        evidence_hash = ""
    return (source.replace("__DASHBOARD_DATA__", _script_json(data))
            .replace("__DASHBOARD_UI__", _script_json(UI[language]))
            .replace("__EVIDENCE_BUNDLE__", _script_json(evidence_bundle))
            .replace("__EVIDENCE_BUNDLE_SHA256__", evidence_hash).rstrip() + "\n")


def default_outputs(data: dict) -> tuple[Path, Path]:
    supplier = re.sub(r"[^a-z0-9_-]+", "-", data.get("supplier", "supplier").casefold()).strip("-")
    filename = f"{supplier}_appendix_b_dashboard.html"
    return OUTPUTS / filename, WIKI / filename


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
    parser.add_argument("dashboard_data", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--wiki-output", type=Path)
    parser.add_argument("--evidence-bundle", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    args = parser.parse_args(argv)
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"))
        data = json.loads(args.dashboard_data.read_text(encoding="utf-8"))
        bundle = (
            json.loads(args.evidence_bundle.read_text(encoding="utf-8"))
            if args.evidence_bundle else None
        )
        if bundle is not None:
            package_hash = hashlib.sha256(args.package.read_bytes()).hexdigest()
            if package_hash != bundle.get("lineage", {}).get("package", {}).get("sha256"):
                raise ValueError("package bytes do not match evidence bundle lineage")
        source_errors = validate_source(package, args.db, args.approvals)
        if source_errors:
            raise ValueError(source_errors[0])
        require_report_gates(package)
        content = render(data, evidence_bundle=bundle)
        from validate_dashboard import validate  # local import avoids CLI import cycle
        errors = validate(package, data, content, evidence_bundle=bundle)
        if errors:
            raise ValueError(errors[0])
        if bundle is not None:
            if args.output is None:
                raise ValueError("--output is required with --evidence-bundle")
            if args.wiki_output is not None:
                raise ValueError("--wiki-output is forbidden for evidence-access candidates")
            output = args.output.resolve()
            evidence_access_policy.require_output_target(output)
            expected = evidence_access_policy.candidate_path(
                bundle["metadata"]["run_id"], output.name
            ).resolve()
            if output != expected:
                raise evidence_access_policy.PolicyError(
                    f"candidate output must be directly under the selected run directory: {expected}"
                )
            _atomic_write_text(output, content)
            print(f"generate_dashboard: PASS - {output} - evidence bundle embedded")
        else:
            default_output, default_wiki = default_outputs(data)
            output, wiki_output = args.output or default_output, args.wiki_output or default_wiki
            for path in (output, wiki_output):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
            print(f"generate_dashboard: PASS - {output} ; {wiki_output}")
        return 0
    except Exception as exc:  # noqa: BLE001 - publication boundary fails closed
        print(f"generate_dashboard: FAIL - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
