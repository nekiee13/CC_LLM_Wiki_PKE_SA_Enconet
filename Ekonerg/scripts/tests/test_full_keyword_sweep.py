"""Recall and source-integrity checks; these do not certify semantic relevance."""
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "full_keyword_sweep.py"
spec = importlib.util.spec_from_file_location("full_keyword_sweep", SCRIPT)
sweep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep)
RULES = SCRIPT.parents[1] / "sieving/prompts/full_keyword_sweep_v1.json"


def test_no_count_or_length_cap_and_cross_mapping():
    rules = sweep.load_rules(RULES)
    source = "# 8.5 Realizacija\n\n" + "\n\n".join(
        f"Sljedivost proizvoda i skladištenje za radni nalog {i}. " + "x" * 800
        for i in range(9)
    )
    result = sweep.scan(source, rules)
    assert len(result["passages"]) == 9
    assert all({"APP_B_VIII", "APP_B_XIII"} <= set(p["matches"]) for p in result["passages"])
    for p in result["passages"]:
        assert source[p["char_start"]:p["char_end"]] == p["quote_original"]


def test_appendix_heading_context_and_last_line():
    rules = sweep.load_rules(RULES)
    source = "# 8.5 Main\r\n\r\n**DODATAK 1:**\r\n\r\n# 9. Upravljanje specijalnim procesima\r\n\r\nOpisano u poglavlju 8.5.2.\r\n\r\n# 18. Provjere\r\n\r\nZavršni zapis o provjeri."
    result = sweep.scan(source, rules)
    p = result["passages"][0]
    assert "DODATAK 1" in p["chapter_path"]
    assert "APP_B_IX" in p["matches"]
    assert p["matches"]["APP_B_IX"]["heading_terms"]
    assert result["passages"][-1]["char_end"] == len(source)
    assert "APP_B_XVIII" in result["passages"][-1]["matches"]
    sweep.verify_scan(source, result, rules)


def test_tables_headings_and_blank_lines_accounted():
    source = "# Kvaliteta\n\n| Kod | Postupak |\n| --- | --- |\n| RUT-03 | Ultrazvučno ispitivanje zavarenih spojeva |\n\n![image](x.png)\n\nBez ključnih riječi.\n"
    result = sweep.scan(source, sweep.load_rules(RULES))
    assert any("RUT-03" in p["quote_original"] for p in result["passages"])
    assert any(b["disposition"] == "no_keyword_match" for b in result["coverage"])
    assert any(b["disposition"] == "image_reference_only" for b in result["coverage"])
    assert result["coverage"][-1]["char_end"] == len(source)


def test_inconsistent_markdown_levels_use_printed_chapter_numbers():
    source = "# 6. Planning\n\n## 8. Realization\n\n#### 8.4 Procurement\n\n#### 8.5 Realization\n\n# 8.5.5 Očuvanje proizvoda\n\nSkladištenje proizvoda.\n\n**DODATAK 1:**\n\n# 3. Projektiranje\n\n#### 8. Identifikacija\n\nSljedivost.\n\n**PRILOG 1: Dijagram toka**\n\nZapisi.\n"
    result = sweep.scan(source, sweep.load_rules(RULES))
    first = result["passages"][0]["chapter_path"]
    assert "6. Planning" not in first and "8.4" not in first
    assert first == "8. Realization / 8.5 Realization / 8.5.5 Očuvanje proizvoda"
    assert result["passages"][1]["chapter_path"] == "DODATAK 1: / 8. Identifikacija"
    assert result["passages"][2]["chapter_path"] == "DODATAK 1: / PRILOG 1: Dijagram toka"


def test_empty_table_row_is_not_a_crumb():
    result = sweep.scan("# Test Control\n\n|    |    |\n", sweep.load_rules(RULES))
    assert not result["passages"]
    assert result["coverage"][-1]["disposition"] == "empty_table_row"


def test_appendix_references_do_not_reparent_the_main_document():
    source = "# 1. Uvod\n\nDODATAK 3: Zahtjevi prema ISO 45001\n\n# 8.5.5 Očuvanje proizvoda\n\nSkladištenje.\n\n**DODATAK 1:**\n\nPRILOG 2: Usporedna tablica\n\n# 8. Identifikacija\n\nSljedivost.\n"
    result = sweep.scan(source, sweep.load_rules(RULES))
    storage = next(p for p in result["passages"] if p["quote_original"] == "Skladištenje.")
    assert "DODATAK" not in storage["chapter_path"]
    trace = next(p for p in result["passages"] if p["quote_original"] == "Sljedivost.")
    assert trace["chapter_path"] == "DODATAK 1: / 8. Identifikacija"


def test_every_criterion_has_bilingual_signals():
    rules = sweep.load_rules(RULES)
    assert len(rules["criteria"]) == 18
    for cid, entry in rules["criteria"].items():
        for example in entry["examples"]:
            result = sweep.scan(example, rules)
            assert cid in result["passages"][0]["matches"], (cid, example)


def test_detects_quote_offset_and_missing_passage_tamper():
    rules = sweep.load_rules(RULES)
    source = "# Test Control\n\nIspitivanje proizvoda.\n"
    result = sweep.scan(source, rules)
    result["passages"][0]["quote_original"] += "invented"
    with pytest.raises(ValueError):
        sweep.verify_scan(source, result, rules)
    result = sweep.scan(source, rules)
    result["passages"] = []
    with pytest.raises(ValueError):
        sweep.verify_scan(source, result, rules)


@pytest.mark.parametrize("name", ["Company A", "Čista tvrtka"])
@pytest.mark.parametrize("sibling", [False, True])
def test_bundle_neutral_readonly_and_retry(tmp_path, name, sibling):
    root = tmp_path / name
    (root / "incoming").mkdir(parents=True)
    (root / "raw").mkdir()
    (root / "manifests").mkdir()
    (root / "sieving/DATA").mkdir(parents=True)
    (root / "db").mkdir()
    (root / "db/nqa_audit.sqlite").write_bytes(b"untouched actual database")
    (root / "sieving/DATA/sieving.db").write_bytes(b"untouched database")
    old = b"# Old\n"
    new = "# Priručnik\n\nSljedivost i skladištenje.\n".encode()
    (root / "raw/manual.md").write_bytes(old)
    (root / "incoming/manual.md").write_bytes(new)
    (root / "manifests/raw_sources.csv").write_text(
        "doc_id,filename,side_hint,sha256\nDOC-0001,manual.md,DOCUMENT," + sweep.digest(old) + "\n", encoding="utf-8")
    if sibling:
        (tmp_path / "Other Company").mkdir()
        (tmp_path / "Other Company/source.md").write_bytes(b"untouched sibling")
    before = {str(p): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    output = root / "out/sweep"
    result = sweep.build(root, output, RULES)
    assert result["documents"][0]["source_changed"]
    assert "db/nqa_audit.sqlite" in {p.replace("\\", "/") for p in result["protected_files"]}
    assert result["totals"]["DOCUMENT"]["documents"] == 1
    assert all(Path(p).read_bytes() == data for p, data in before.items())
    assert sweep.verify_bundle(output)["documents"] == 1
    with pytest.raises(ValueError):
        sweep.build(root, output, RULES)
    with pytest.raises(ValueError):
        sweep.build(root, tmp_path / "outside", RULES)
    payload_path = output / "documents/DOC-0001.json"
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload["passages"][0]["quote_original"] = "false"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        sweep.verify_bundle(output)


def test_unknown_incoming_file_is_not_silently_skipped(tmp_path):
    root = tmp_path / "company"
    (root / "incoming").mkdir(parents=True)
    (root / "manifests").mkdir()
    (root / "incoming/extra.pdf").write_bytes(b"PDF")
    (root / "manifests/raw_sources.csv").write_text("doc_id,filename,side_hint,sha256\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unregistered|Unsupported"):
        sweep.build(root, root / "out/sweep", RULES)
    assert not (root / "out/sweep").exists()
