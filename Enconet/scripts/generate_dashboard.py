#!/usr/bin/env python3
"""Render and publish a self-contained EPIC12 dashboard from validated data."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import db_util
from build_dashboard_data import validate_data
from build_evaluation_package import validate_source
from finding_workflow import APPROVALS
from generate_report import require_report_gates

ENCONET = Path(__file__).resolve().parents[1]
TEMPLATE = ENCONET / "templates" / "dashboard-template.html"
OUTPUTS = ENCONET / "outputs"
WIKI = ENCONET / "wiki" / "dashboards"

UI = {
    "en": {"title":"Appendix B Evaluation Dashboard","kicker":"Offline audit dashboard","score":"Weighted score","applicable":"Applicable criteria","classification":"Classification","summary":"Executive summary","summary_text":"The package contains {count} applicable criteria with a weighted score of {score}.","distribution":"Classification distribution","filter":"Rating","search":"Search","sort":"Reverse order","expand":"Expand all","collapse":"Collapse all","print":"Print","criteria":"Criterion cards","matrix":"Evaluation matrix","actions":"Priority actions","details":"Show / hide details","affirmative":"Affirmative","contrary":"Contrary","judgement":"Judgement","none":"none","na":"n/a","all":"All ratings","id":"Criterion","name":"Name","rating":"Rating","criterion_score":"Score","evidence":"Evidence","none_actions":"No approved priority actions are present."},
    "sl": {"title":"Nadzorna plošča vrednotenja Dodatka B","kicker":"Nadzorna plošča za delo brez povezave","score":"Utežena ocena","applicable":"Veljavna merila","classification":"Razvrstitev","summary":"Povzetek","summary_text":"Paket vsebuje {count} veljavnih meril z uteženo oceno {score}.","distribution":"Porazdelitev razvrstitev","filter":"Ocena","search":"Iskanje","sort":"Obrni vrstni red","expand":"Razširi vse","collapse":"Strni vse","print":"Natisni","criteria":"Kartice meril","matrix":"Matrika vrednotenja","actions":"Prednostni ukrepi","details":"Prikaži / skrij podrobnosti","affirmative":"Pritrdilno","contrary":"Nasprotno","judgement":"Presoja","none":"brez","na":"ni relevantno","all":"Vse ocene","id":"Merilo","name":"Ime","rating":"Ocena","criterion_score":"Točke","evidence":"Dokazi","none_actions":"Odobrenih prednostnih ukrepov ni."},
    "hr": {"title":"Nadzorna ploča ocjene Dodatka B","kicker":"Izvanmrežna nadzorna ploča","score":"Ponderirana ocjena","applicable":"Primjenjivi kriteriji","classification":"Klasifikacija","summary":"Sažetak","summary_text":"Paket sadrži {count} primjenjivih kriterija s ponderiranom ocjenom {score}.","distribution":"Raspodjela klasifikacija","filter":"Ocjena","search":"Pretraži","sort":"Obrni redoslijed","expand":"Proširi sve","collapse":"Sažmi sve","print":"Ispiši","criteria":"Kartice kriterija","matrix":"Matrica ocjene","actions":"Prioritetne radnje","details":"Prikaži / sakrij pojedinosti","affirmative":"Potvrdno","contrary":"Suprotno","judgement":"Prosudba","none":"nema","na":"nije primjenjivo","all":"Sve ocjene","id":"Kriterij","name":"Naziv","rating":"Ocjena","criterion_score":"Bodovi","evidence":"Dokazi","none_actions":"Nema odobrenih prioritetnih radnji."},
}


def _script_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).replace("<", "\\u003c")


def render(data: dict, template: Path = TEMPLATE) -> str:
    errors = validate_data(data)
    if errors:
        raise ValueError("invalid dashboard data: " + "; ".join(errors))
    language = data["deliverable_language"]
    if language not in UI:
        raise ValueError("unsupported deliverable_language")
    source = template.read_text(encoding="utf-8")
    if source.count("__DASHBOARD_DATA__") != 1 or source.count("__DASHBOARD_UI__") != 1:
        raise ValueError("dashboard template injection markers are invalid")
    return (source.replace("__DASHBOARD_DATA__", _script_json(data))
            .replace("__DASHBOARD_UI__", _script_json(UI[language])).rstrip() + "\n")


def default_outputs(data: dict) -> tuple[Path, Path]:
    supplier = re.sub(r"[^a-z0-9_-]+", "-", data.get("supplier", "supplier").casefold()).strip("-")
    filename = f"{supplier}_appendix_b_dashboard.html"
    return OUTPUTS / filename, WIKI / filename


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("dashboard_data", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--wiki-output", type=Path)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--approvals", type=Path, default=APPROVALS)
    args = parser.parse_args()
    try:
        package = json.loads(args.package.read_text(encoding="utf-8"))
        data = json.loads(args.dashboard_data.read_text(encoding="utf-8"))
        source_errors = validate_source(package, args.db, args.approvals)
        if source_errors:
            raise ValueError(source_errors[0])
        require_report_gates(package)
        content = render(data)
        from validate_dashboard import validate  # local import avoids CLI import cycle
        errors = validate(package, data, content)
        if errors:
            raise ValueError(errors[0])
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
