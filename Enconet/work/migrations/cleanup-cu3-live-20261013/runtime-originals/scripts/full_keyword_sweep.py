"""Read-only, high-recall intake sweep. Never imports, scores, or promotes leads.

Writes a fresh, reproducible bundle under the selected project's out directory.
Sources, the registry, and all existing database generations remain unchanged.
Character offsets refer to the UTF-8 decoded snapshot, including original CR/LF.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import sqlite3
from pathlib import Path
import re
import unicodedata

PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_RULES = PROJECT / "sieving/prompts/full_keyword_sweep_v1.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold().replace("đ", "d"))
                   if not unicodedata.combining(c))


def load_rules(path):
    rules = json.loads(Path(path).read_text(encoding="utf-8"))
    expected = {"APP_B_" + n for n in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
                                      "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII")}
    if set(rules["criteria"]) != expected:
        raise ValueError("Rules must cover exactly all 18 criteria")
    for entry in rules["criteria"].values():
        if not entry["terms"]:
            raise ValueError("Every criterion needs search terms")
        for term in entry["terms"]:
            re.compile(r"\b(?:" + term + ")")
    return rules


def heading(line):
    clean = line.strip().lstrip("\ufeff")
    markdown = re.match(r"^(#{1,6})\s+(.+?)\s*#*$", clean)
    title = (markdown[2] if markdown else clean).strip("* ")
    appendix = re.match(r"^(DODATAK|PRILOG|APPENDIX|ANNEX)\s+\d+\s*[:.\-]?", title, re.I)
    # A plain appendix title inside a contents list or a paragraph's reference
    # list is not an appendix boundary. Converted diagram captions may carry
    # their image on the same line instead of Markdown heading markup.
    if appendix and (markdown or clean.startswith("**") or "![](" in clean):
        return (-1 if appendix[1].upper() == "DODATAK" else 0), title
    if markdown:
        # Converted PDFs often use #, ##, #### inconsistently. The printed
        # clause number, not its font/Markdown size, determines chapter depth.
        number = re.match(r"^(\d+(?:\.\d+)*)(?:\.?\s)", title)
        return (len(number[1].split(".")) if number else len(markdown[1])), title
    return None


def blocks(source):
    """Partition every character; retain headings, empty lines and non-matches."""
    lines = source.splitlines(keepends=True)
    offset, index, stack = 0, 0, []
    while index < len(lines):
        line = lines[index]
        start, first = offset, index + 1
        found = heading(line)
        kind = "content"
        if found:
            level, title = found
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            kind = "heading"
        elif not line.strip():
            kind = "blank"
        elif re.fullmatch(r"\s*!\[[^\]]*\]\([^\n]+\)\s*", line):
            kind = "image_reference_only"
        elif re.fullmatch(r"[\s|:\-]+", line) and "-" in line:
            kind = "table_separator_or_rule"
        elif "|" in line and not line.strip().strip("| \t\r\n"):
            kind = "empty_table_row"
        offset += len(line)
        index += 1
        # Tables and list entries are individual units; ordinary paragraphs keep
        # all continuation lines. No maximum length, and no clipping of the quote.
        if kind == "content" and not re.match(r"\s*(?:\||[-*+]\s|\d+[.)]\s)", line):
            while index < len(lines):
                nxt = lines[index]
                if not nxt.strip() or heading(nxt) or re.match(r"\s*(?:\||[-*+]\s|\d+[.)]\s|!\[)", nxt):
                    break
                offset += len(nxt)
                index += 1
        yield {"char_start": start, "char_end": offset, "line_start": first, "line_end": index,
               "chapter_path": " / ".join(t for _, t in stack) or "Front matter",
               "nearest_heading": stack[-1][1] if stack else "", "kind": kind}


def scan(source, rules):
    compiled = {cid: [(term, re.compile(r"\b(?:" + term + ")")) for term in entry["terms"]]
                for cid, entry in rules["criteria"].items()}
    passages, coverage = [], []
    for number, block in enumerate(blocks(source), 1):
        raw = source[block["char_start"]:block["char_end"]]
        quote = raw.rstrip("\r\n")
        body, context = normalize(quote), normalize(block["nearest_heading"])
        matches = {}
        if block["kind"] == "content":
            for cid, terms in compiled.items():
                direct = [term for term, pattern in terms if pattern.search(body)]
                indirect = [term for term, pattern in terms if pattern.search(context)]
                if direct or indirect:
                    matches[cid] = {"quote_terms": direct, "heading_terms": indirect}
        bid = f"B{number:05d}"
        coverage.append({**block, "block_id": bid,
                         "disposition": "candidate_lead" if matches else
                         "no_keyword_match" if block["kind"] == "content" else block["kind"]})
        if matches:
            passages.append({"passage_id": bid, "chapter_path": block["chapter_path"],
                             "line_start": block["line_start"], "line_end": block["line_end"],
                             "char_start": block["char_start"],
                             "char_end": block["char_start"] + len(quote),
                             "quote_original": quote, "matches": matches,
                             "evidence_type": "candidate_lead", "semantic_review": "pending"})
    return {"passages": passages, "coverage": coverage}


def verify_scan(source, result, rules):
    previous = 0
    for block in result["coverage"]:
        if block["char_start"] != previous or block["char_end"] <= previous:
            raise ValueError("Coverage has a gap or overlap")
        previous = block["char_end"]
    if previous != len(source):
        raise ValueError("Source coverage incomplete")
    for passage in result["passages"]:
        if source[passage["char_start"]:passage["char_end"]] != passage["quote_original"]:
            raise ValueError("Non-exact quote or offset")
    if scan(source, rules) != {key: result[key] for key in ("passages", "coverage")}:
        raise ValueError("Sweep does not reproduce from source and rules")


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def file_inventory(root, folders):
    return {str(p.relative_to(root)): digest(p.read_bytes())
            for folder in folders for p in sorted((root / folder).rglob("*")) if p.is_file()}


def safe_file(path, root):
    if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
        raise ValueError(f"Source escapes project or is linked: {path}")


def load_exclusions(path, root):
    if path is None:
        return {}
    path = Path(path)
    safe_file(path, root)
    data = json.loads(path.read_text(encoding='utf-8'))
    exclusions = {}
    for row in data['files']:
        name = row['filename']
        if Path(name).name != name or name in exclusions or not row.get('reason'):
            raise ValueError('Invalid or duplicate exclusion')
        candidate = root / 'incoming' / name
        safe_file(candidate, root)
        if not candidate.is_file() or digest(candidate.read_bytes()) != row['sha256']:
            raise ValueError('Excluded incoming file changed: ' + name)
        exclusions[name] = row
    return exclusions


def prepare(root, rules, exclusions=None):
    exclusions = exclusions or {}
    registry = root / "manifests/raw_sources.csv"
    safe_file(registry, root)
    with registry.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    names = [row["filename"] for row in rows]
    if len(set(names)) != len(names) or len({r["doc_id"] for r in rows}) != len(rows):
        raise ValueError("Duplicate registry filename or ID")
    # A fuller owner extraction is registered separately so historical raw
    # evidence stays intact. Scan its original incoming filename exactly once.
    database = root / 'db/nqa_audit.sqlite'
    incoming_names = {r['doc_id']:r['filename'] for r in rows}
    retired = set()
    if database.is_file():
        with database.open('rb') as stream:
            is_sqlite = stream.read(16) == b'SQLite format 3\x00'
        if is_sqlite:
            conn = sqlite3.connect(database.resolve().as_uri()+'?mode=ro',uri=True)
            try:
                exists = conn.execute("SELECT 1 FROM sqlite_master WHERE name='source_revision_intakes' AND type='table'").fetchone()
                revisions = conn.execute('SELECT old_doc_id,new_doc_id,source_sha256 FROM source_revision_intakes').fetchall() if exists else []
            finally:
                conn.close()
            by_id = {r['doc_id']:r for r in rows}
            if len({r[0] for r in revisions}) != len(revisions):
                raise ValueError('Ambiguous replacement sources; select one intake before sweeping')
            pending = list(revisions)
            while pending:
                progressed = False
                for old_id,new_id,digest_value in list(pending):
                    if old_id not in by_id or new_id not in by_id or by_id[new_id]['sha256'] != digest_value:
                        raise ValueError('Source-revision registry mismatch')
                    if any(r[1] == old_id for r in pending):
                        continue
                    incoming_names[new_id] = incoming_names[old_id]
                    retired.add(old_id)
                    pending.remove((old_id,new_id,digest_value))
                    progressed = True
                if not progressed:
                    raise ValueError('Cyclic source-revision history')
    rows = [r for r in rows if r['doc_id'] not in retired]
    names = [incoming_names[r['doc_id']] for r in rows]
    if set(exclusions) & set(names):
        raise ValueError('A registered source cannot be excluded from the sweep')
    if len(set(names)) != len(names):
        raise ValueError('Ambiguous incoming source mapping')
    incoming = sorted(p for p in (root / "incoming").rglob("*")
                      if p.is_file() and p.name != '.gitkeep'
                      and p.relative_to(root / 'incoming').as_posix() not in exclusions)
    actual = {p.relative_to(root / "incoming").as_posix() for p in incoming}
    if actual != set(names):
        raise ValueError(f"Missing or unregistered incoming files: {sorted(actual ^ set(names))}")
    prepared = []
    for row in rows:
        name, doc_id, side = row["filename"], row["doc_id"], row["side_hint"]
        if not re.fullmatch(r"DOC-\d+", doc_id) or side not in ("DOCUMENT", "RULE"):
            raise ValueError("Invalid registered ID or side")
        incoming_name = incoming_names[doc_id]
        path, old_path = root / "incoming" / incoming_name, root / "raw" / name
        safe_file(path, root)
        safe_file(old_path, root)
        if path.suffix.lower() != ".md":
            raise ValueError(f"Unsupported source format: {name}")
        raw = path.read_bytes()
        old = old_path.read_bytes()
        if digest(old) != row["sha256"].lower():
            raise ValueError(f"Registered raw source hash mismatch: {doc_id}")
        source = raw.decode("utf-8")
        result = scan(source, rules)
        verify_scan(source, result, rules)
        prepared.append((raw, {"schema": "full_keyword_sweep_leads/1", "method": rules["version"],
            "doc_id": doc_id, "filename": incoming_name, "document_side": side,
            "source_sha256": digest(raw), "registered_source_sha256": row["sha256"],
            "source_changed": digest(raw) != row["sha256"].lower(),
            "source_bytes": len(raw), "source_characters": len(source),
            "source_lines": len(source.splitlines()), **result}))
    return prepared


def render_document(doc, rules):
    output = [f"# {doc['doc_id']} — {doc['filename']}", "",
        "These are exact source passages found by a broad keyword sweep. They are NOT approved findings.", "",
        "Each passage is printed once, even when it has links to more than one criterion.", "",
        f"Side: {doc['document_side']}. Source SHA-256: `{doc['source_sha256']}`.", "",
        "[Full source snapshot](../sources/" + doc["doc_id"] + ".md)", ""]
    for p in doc["passages"]:
        output += [f"## {doc['doc_id']}-{p['passage_id']}", "",
            f"Chapter: {p['chapter_path']} · lines {p['line_start']}–{p['line_end']}", "",
            "Criteria: " + "; ".join(cid + " — " + rules["criteria"][cid]["name"] for cid in p["matches"]), "",
            *["> " + line for line in p["quote_original"].splitlines()], ""]
    return "\n".join(output)


def summarize(doc):
    per = Counter(cid for passage in doc["passages"] for cid in passage["matches"])
    return {key: doc[key] for key in ("doc_id", "filename", "document_side", "source_sha256",
            "registered_source_sha256", "source_changed", "source_bytes", "source_lines")} | {
            "passages": len(doc["passages"]), "unique_quote_texts": len({p["quote_original"] for p in doc["passages"]}),
            "criterion_links": sum(per.values()), "per_criterion": dict(per),
            "coverage_blocks": len(doc["coverage"]),
            "unmatched_content_blocks": sum(b["disposition"] == "no_keyword_match" for b in doc["coverage"])}


def build(root, output, rules_path, exclusions_path=None):
    root, output = Path(root).resolve(), Path(output).resolve()
    if not output.is_relative_to(root / "out") or output == root / "out" or output.exists():
        raise ValueError("Output must be a NEW directory below this project's out directory")
    rules = load_rules(rules_path)
    protected = file_inventory(root, ("incoming", "raw", "sieving/DATA", "db"))
    registry_hash = digest((root / "manifests/raw_sources.csv").read_bytes())
    exclusions = load_exclusions(exclusions_path, root)
    prepared = prepare(root, rules, exclusions)
    output.mkdir(parents=True, exist_ok=False)
    for folder in ("documents", "sources", "review"):
        (output / folder).mkdir()
    (output / "rules.json").write_bytes(Path(rules_path).read_bytes())
    (output / "scanner.py").write_bytes(Path(__file__).read_bytes())
    write_json(output / 'exclusions.json', {'files': list(exclusions.values())})
    summaries = []
    for raw, doc in prepared:
        did = doc["doc_id"]
        (output / "sources" / (did + ".md")).write_bytes(raw)
        write_json(output / "documents" / (did + ".json"), doc)
        (output / "review" / (did + ".md")).write_text(render_document(doc, rules), encoding="utf-8")
        summaries.append(summarize(doc))
    totals = {side: {key: sum(row[key] for row in summaries if row["document_side"] == side)
                      for key in ("passages", "unique_quote_texts", "criterion_links", "unmatched_content_blocks")}
              | {"documents": sum(row["document_side"] == side for row in summaries)} for side in ("DOCUMENT", "RULE")}
    report = ["# Full keyword sweep — results", "", "This is a recall pass, not a new audit score.", "",
              "No old crumbs were carried forward. No count or quote-length limits were used. All 18 criteria were searched.", "",
              "Keyword/heading matches are unreviewed leads. Read unmatched blocks too: absence of a keyword is not absence of evidence.", "",
              "Regulatory/reference passages are separate from vendor evidence. This scan does not change applicability or make optional NQA-1 parts mandatory.", "",
              "New source revisions are snapshotted here; they are NOT linked to old database chapters. All existing sources and database generations stay unchanged.", "",
              "| Side | Files | Passage occurrences | Distinct quote texts (per document) | Criterion links | Unmatched blocks |",
              "|---|---:|---:|---:|---:|---:|"]
    for side, counts in totals.items():
        report.append(f"| {side} | {counts['documents']} | {counts['passages']} | {counts['unique_quote_texts']} | {counts['criterion_links']} | {counts['unmatched_content_blocks']} |")
    report += ["", "## Documents", "", "| Document | Side | Passages | Links | Changed source |",
               "|---|---|---:|---:|---|"]
    for row in summaries:
        did = row["doc_id"]
        report.append(f"| [{did}: {row['filename']}](review/{did}.md) | {row['document_side']} | {row['passages']} | {row['criterion_links']} | {row['source_changed']} |")
    (output / "README.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    if protected != file_inventory(root, ("incoming", "raw", "sieving/DATA", "db")) or registry_hash != digest((root / "manifests/raw_sources.csv").read_bytes()):
        raise ValueError("Inputs changed during sweep; bundle NOT complete")
    manifest = {"schema": "full_keyword_sweep_manifest/1", "method": rules["version"],
                "complete_keyword_pass": True, "semantic_review_complete": False,
                "database_imported": False, "source_registry_modified": False,
                "source_and_database_unchanged": True, "registry_sha256": registry_hash,
                "protected_files": protected, "documents": summaries, "totals": totals,
                "incoming_exclusions": list(exclusions.values()),
                "artifacts": {p.relative_to(output).as_posix(): digest(p.read_bytes())
                              for p in sorted(output.rglob("*")) if p.is_file()}}
    write_json(output / "manifest.json", manifest)
    verify_bundle(output)
    return manifest


def verify_bundle(output):
    output = Path(output).resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()} - {"manifest.json"}
    if actual != set(manifest["artifacts"]):
        raise ValueError("Missing or extra artifacts")
    for name, expected in manifest["artifacts"].items():
        path = output / name
        safe_file(path, output)
        if digest(path.read_bytes()) != expected:
            raise ValueError(f"Artifact hash mismatch: {name}")
    rules = load_rules(output / "rules.json")
    for summary in manifest["documents"]:
        did = summary["doc_id"]
        if not re.fullmatch(r"DOC-\d+", did):
            raise ValueError("Invalid document ID")
        doc = json.loads((output / "documents" / (did + ".json")).read_text(encoding="utf-8"))
        raw = (output / "sources" / (did + ".md")).read_bytes()
        if digest(raw) != doc["source_sha256"] or summary != summarize(doc):
            raise ValueError(f"Source or summary mismatch: {did}")
        verify_scan(raw.decode("utf-8"), doc, rules)
    return {"documents": len(manifest["documents"]), "totals": manifest["totals"], "exact_quotes": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--verify", type=Path)
    parser.add_argument('--exclusions', type=Path, help='Local explicit filename/hash/reason list for non-source incoming files')
    args = parser.parse_args()
    if args.verify:
        result = verify_bundle(args.verify)
    elif args.output:
        result = build(args.project, args.output, args.rules, args.exclusions)["totals"]
    else:
        parser.error("Use --output NEW_DIRECTORY or --verify EXISTING_BUNDLE")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
