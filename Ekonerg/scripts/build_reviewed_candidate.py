"""Build an exact-quote candidate from explicit semantic-review annotations.

This is an assembler, not an LLM or a keyword-to-finding converter. A reviewer
authors the section notes, criterion mappings and statements. This command only
checks their source ranges, records provenance and prepares a READ-ONLY intake
preview. It has no database import, source overwrite or promotion capability.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sqlite3

import yaml

ROOT = Path(__file__).resolve().parents[1]
STRENGTHS = {"objective_control", "supporting_control", "candidate_lead"}
TYPES = {"control", "reference", "definition", "role_responsibility", "finding", "record", "status_statement"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def local(path, root):
    root = root.resolve()
    result = (path if path.is_absolute() else root / path).resolve()
    if not result.is_relative_to(root):
        raise ValueError("path must remain within the selected project")
    return result


def prepare(raw, config, entries, criteria):
    if sha(raw) != config["source_sha256"]:
        raise ValueError("review source hash changed")
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    section_at = {}
    cursor = 1
    for section in config["sections"]:
        if section["start"] != cursor or not cursor <= section["end"] <= len(lines):
            raise ValueError("section review has a gap, overlap or invalid range")
        if any(not section[key].strip() for key in ("chapter", "pass1", "pass2")):
            raise ValueError("both semantic pass notes are required for every section")
        for number in range(cursor, section["end"] + 1):
            section_at[number] = section
        cursor = section["end"] + 1
    if cursor != len(lines) + 1:
        raise ValueError("section review does not reach the last source line")
    for key, value in config.get("context", {}).items():
        if key not in {"project_ref", "contract_ref", "supplier_ref", "source_revision", "evidence_date"} or not value or value not in text:
            raise ValueError("context must be allowed and present verbatim in source")
    items, locations, fingerprints, used = [], [], set(), {}
    metrics = Counter()
    for number, entry in enumerate(entries, 1):
        start, end = int(entry["start"]), int(entry["end"])
        if not 1 <= start <= end <= len(lines):
            raise ValueError(f"invalid quote line range at entry {number}")
        criterion = "APP_B_" + entry["criterion"]
        strength, statement, item_type = entry["strength"], entry["statement"].strip(), entry["type"]
        if criterion not in criteria or strength not in STRENGTHS or item_type not in TYPES:
            raise ValueError(f"invalid criterion/strength/type at entry {number}")
        if entry["pass"] not in {"1", "2"} or not statement:
            raise ValueError("review pass and authored statement are required")
        section = section_at[start]
        if section is not section_at[end]:
            raise ValueError("quote crosses reviewed section boundaries; split its source ranges")
        quote = "".join(lines[start - 1:end]).rstrip("\r\n")
        if not quote.strip():
            raise ValueError("quote is blank")
        fingerprint = (criterion, quote, statement)
        if fingerprint in fingerprints:
            raise ValueError("duplicate evidence and control meaning; merge explicitly")
        fingerprints.add(fingerprint)
        # Explicit section review is the parent authority. A nearest printed
        # heading only adds detail; malformed Markdown cannot change its parent.
        headings = [line.strip().lstrip("# ").strip("*") for line in lines[section["start"] - 1:start]
                    if re.match(r"^#{1,6}\s", line)]
        detail = f" / {headings[-1]}" if headings else ""
        locator = f"{section['chapter']}{detail} [lines {start}-{end}; source {config['source_sha256'][:12]}]"
        item_id = f"{config['prefix']}-{number:04d}"
        if not re.fullmatch(r"[A-Za-z0-9_-]+", item_id):
            raise ValueError("unsafe item prefix")
        if strength == "candidate_lead":
            statement += " Objective evidence not shown by this reference/lead."
        item = {"item_id": item_id, "criterion_id": criterion, "criterion_name": criteria[criterion],
                "statement": f"{strength}: {statement}", "item_type": item_type,
                "evidence_type": "candidate_lead" if strength == "candidate_lead" else "policy_or_procedure",
                "entities": {}, "sources": [{"source_locator": locator}],
                "evidence_quotes": [{"quote_original": quote, "quote_language": config["language"], "source_locator": locator}]}
        if config.get("context"):
            item["context"] = config["context"].copy()
        items.append(item)
        a, b = offsets[start - 1], offsets[start - 1] + len(quote)
        if text[a:b] != quote:
            raise ValueError("non-exact source quote")
        locations.append({"item_id": item_id, "line_start": start, "line_end": end,
                          "char_start": a, "char_end": b, "quote_original": quote,
                          "source_locator": locator, "semantic_pass": int(entry["pass"])})
        for line_number in range(start, end + 1):
            used.setdefault(line_number, []).append(item_id)
        metrics["direct_items" if entry["pass"] == "1" else "concept_items"] += 1
        metrics[strength] += 1
    if not items:
        raise ValueError("no reviewed evidence annotations")
    payload = {"prompt_version": config["prompt_version"], "source_sha256": config["source_sha256"],
               "document": {"doc_id": config["doc_id"], "name": config["name"], "date": config["date"],
                            "document_side": "DOCUMENT", "authority_references": []}, "items": items}
    provenance = {"source_sha256": sha(raw), "registered_source_sha256": config["registered_sha256"],
                  "source_revision_registered": False, "import_ready": False, "database_modified": False,
                  "review_scope": config.get("review_scope", "Explicit source-based semantic annotations"),
                  "line_count": len(lines), "sections": config["sections"], "quote_locations": locations,
                  "line_coverage": [{"line": n, "section": section_at[n]["chapter"], "items": used.get(n, []),
                      "disposition": "quoted" if n in used else "reviewed_context_or_no_separate_control"}
                      for n in range(1, len(lines) + 1)],
                  "merged_source_passages": config.get("merged_source_passages", []),
                  "metrics": {**dict(metrics), "items": len(items),
                              "merged_source_passages": len(config.get("merged_source_passages", [])),
                              "rejected_invalid_items": 0,
                              "distinct_quote_ranges": len({(q["char_start"], q["char_end"]) for q in locations}),
                              "per_criterion": dict(Counter(i["criterion_id"] for i in items))}}
    return payload, provenance


def intake_preview(root, config, payload):
    """Inspect exact live identity and dependencies; never create or migrate DB."""
    database = local(Path("db/nqa_audit.sqlite"), root)
    before = sha(database.read_bytes())
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        document = conn.execute("SELECT * FROM documents WHERE doc_id=?", (config["doc_id"],)).fetchone()
        if not document or document["sha256"] != config["registered_sha256"]:
            raise ValueError("registered predecessor differs from the reviewed baseline")
        runs = [dict(r) for r in conn.execute("SELECT run_id,status,is_active,prompt_version,generation FROM sieve_runs WHERE doc_id=? ORDER BY generation", (config["doc_id"],))]
        chunks = [dict(r) for r in conn.execute("SELECT chunk_id,heading_path,char_start,char_end,source_sha256 FROM document_chunks WHERE doc_id=?", (config["doc_id"],))]
        active = [r["run_id"] for r in runs if r["is_active"]]
        old = [dict(r) for r in conn.execute("SELECT c.item_id,c.criterion_id,c.statement,q.quote_original FROM crumbs c JOIN sieve_runs r ON r.run_id=c.sieve_run_id LEFT JOIN crumb_quotes q ON q.item_id=c.item_id WHERE r.doc_id=? AND r.is_active=1", (config["doc_id"],))]
        old_count = len({r["item_id"] for r in old})
        max_id = max(int(r[0].split("-")[1]) for r in conn.execute("SELECT doc_id FROM documents"))
    if before != sha(database.read_bytes()):
        raise ValueError("database changed during intake preview")
    raw_path = local(Path("raw") / document["filename"], root)
    if sha(raw_path.read_bytes()) != config["registered_sha256"]:
        raise ValueError("old raw hash differs from registered identity")
    new_text = local(Path(config["source"]), root).read_bytes().decode("utf-8")
    return {"mode": "preview_only", "live_writes": 0, "database_sha256": before,
            "logical_document": config["doc_id"], "registered_filename": document["filename"],
            "old_sha256": config["registered_sha256"], "replacement_sha256": config["source_sha256"],
            "replacement_kind": config.get("replacement_kind", "unspecified_requires_review"),
            "source_context": config.get("context", {}),
            "old_active_runs": active, "existing_runs": runs, "existing_chunks": chunks,
            "old_active_crumbs": old_count, "prepared_items": len(payload["items"]),
            "old_quote_rows_still_verbatim_in_replacement": sum(bool(r["quote_original"]) and r["quote_original"] in new_text for r in old),
            "old_quote_rows": len(old), "old_criterion_counts": dict(Counter({cid: len({r["item_id"] for r in old if r["criterion_id"] == cid}) for cid in {r["criterion_id"] for r in old}})),
            "next_unreserved_document_id": f"DOC-{max_id + 1:04d}",
            "blockers_to_live_import": ["Replacement hash differs from documents/raw registry; source identity needs tested revision-aware intake.",
                "Existing candidate generations require recorded disposition before the normal re-sieve importer can create another.",
                "Do not link new quotes to predecessor chapters, rewrite old crumbs, or count old/new manual evidence twice."],
            "proposed_write_strategy_for_review": [
                "Retain the old registered source, document identity, chunks, runs and evidence links unchanged.",
                "Register the complete extraction under a fresh source identity with an explicit predecessor relation; the next ID above is NOT reserved.",
                "Create chapter records for the new source and import this reviewed candidate against that identity, not the old DOC identity.",
                "Use one tested current-source selection for active auditing so the old and new manual are not both counted.",
                "Switch active evidence only through recorded generation/source decisions and refresh evaluation links/scores; retain historical generations."],
            "recovery_strategy_for_review": config.get("recovery_strategy", "Not decided; no live writes are permitted by this preview.")}


def build(root, review, output):
    root = Path(root).resolve()
    review = local(Path(review), root)
    output = local(Path(output), root)
    if not output.is_relative_to(root / "sieving/candidates") or output == root / "sieving/candidates" or output.exists():
        raise ValueError("output must be a new directory under project sieving/candidates")
    config_path = review / "review.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    with (review / "annotations.tsv").open(encoding="utf-8", newline="") as stream:
        entries = list(csv.DictReader(stream, delimiter="\t"))
    raw = local(Path(config["source"]), root).read_bytes()
    taxonomy = yaml.safe_load((root / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))
    criteria = {r["criterion_id"]: r["criterion_name"] for r in taxonomy["criteria"]}
    payload, provenance = prepare(raw, config, entries, criteria)
    preview = intake_preview(root, config, payload)
    provenance["annotations_sha256"] = sha((review / "annotations.tsv").read_bytes())
    provenance["review_sha256"] = sha(config_path.read_bytes())
    provenance["assembler_sha256"] = sha(Path(__file__).read_bytes())
    prompt = root / "sieving/prompts" / (config["prompt_version"] + ".md")
    provenance["prompt_sha256"] = sha(prompt.read_bytes())
    provenance["concepts_sha256"] = sha((root / "sieving/prompts/appb_concepts.yml").read_bytes())
    output.mkdir(parents=True, exist_ok=False)
    results = {"candidate.json": payload, "provenance.json": provenance, "intake-preview.json": preview}
    for name, value in results.items():
        (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = [f"# {config['name']} — reviewed evidence candidate", "", "Status: source-based semantic review by Codex; not imported or promoted. Claude review pending.", "",
          "Objective control means concrete wording in a procedure, not proof that a project performed it. References and conditional statements retain their limits.", "",
          f"Source SHA-256: `{config['source_sha256']}`. Old source and active database evidence remain unchanged.", "",
          f"Items: {len(payload['items'])}. Direct-pass items: {provenance['metrics']['direct_items']}. Concept-pass items: {provenance['metrics']['concept_items']}.", "",
          "| Criterion | Items |", "|---|---:|"]
    for cid in criteria:
        md.append(f"| {cid}: {criteria[cid]} | {provenance['metrics']['per_criterion'].get(cid, 0)} |")
    for item in payload["items"]:
        md += ["", f"## {item['item_id']} — {item['criterion_id']}: {item['criterion_name']}", "", item["statement"], "",
               item["sources"][0]["source_locator"], "", *["> " + s for s in item["evidence_quotes"][0]["quote_original"].splitlines()]]
    (output / "candidate.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    manifest = {"source_sha256": config["source_sha256"], "artifacts": {p.name: sha(p.read_bytes()) for p in output.iterdir() if p.is_file()}}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return provenance["metrics"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=ROOT)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.project, args.review, args.output), indent=2))


if __name__ == "__main__":
    main()
