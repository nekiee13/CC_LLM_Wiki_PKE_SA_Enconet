from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[2]


def run(root: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    return subprocess.run([sys.executable, "-B", str(root / "scripts" / script), *args], cwd=root,
                          env=env, text=True, capture_output=True, check=False)


def copy_project(root: Path) -> None:
    for folder in ("scripts", "db", "schemas", "sieving"):
        shutil.copytree(PROJECT / folder, root / folder, dirs_exist_ok=True)
    (root / "raw").mkdir()
    (root / "manifests").mkdir()


def add_evaluations(root: Path) -> None:
    raw = root / "raw" / "appendix-b.txt"
    raw.write_text("# Appendix B\n\nOrganization requirement.\n", encoding="utf-8")
    digest = hashlib.sha256(raw.read_bytes()).hexdigest()
    db = root / "db" / "nqa_audit.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,language,document_side,sha256) VALUES (?,?,?,?,?,?,?)",
                     ("DOC-0002", "appendix-b.txt", "Appendix B", "Regulator", "en", "RULE", digest))
        conn.execute("INSERT INTO approved_sources VALUES (?,?,?,?,?,?,?)",
                     ("SYNTH-RULE", "GOVERNING", "test-edition", digest, "G1-SYNTH", "owner", "2026-10-02"))
        conn.commit()
    (root / "schemas" / "scoring_model.yml").write_text(
        "model_version: synthetic-1\ncalibration_status: approved\napproval_ref: G3-RUN-20261002-01\n"
        "rating_weights:\n  fully: 1.0\n  substantially: 0.75\n  partially: 0.5\n  minimally: 0.25\n  unmet: 0.0\n  undetermined: 0.0\n  na: null\n"
        "classification_thresholds:\n  - {min_score: 90.0, class: fully}\n  - {min_score: 0.0, class: unmet}\n", encoding="utf-8")
    approvals = root / "manifests" / "approvals.csv"
    with approvals.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["object_id", "decision", "date", "reviewer", "notes"])
        for gate in ("G2", "G3", "G4"):
            writer.writerow([f"{gate}-RUN-20261002-01", "approved", "2026-10-02", "owner", "synthetic-1" if gate == "G3" else "synthetic"])
    helper = root / "evaluation_helper.py"
    helper.write_text(
        "from pathlib import Path\n"
        "import sqlite3\n"
        "from evaluation_engine import write_rulings, write_evaluation\n"
        "root=Path(__file__).resolve().parent; db=root/'db'/'nqa_audit.sqlite'\n"
        "with sqlite3.connect(db) as c: criteria=[r[0] for r in c.execute('SELECT criterion_id FROM criteria ORDER BY criterion_id')]\n"
        "rulings=[{'criterion_id':cid,'applicable':cid=='APP_B_I','justification':'synthetic scope','scope_source_doc_id':'DOC-0002'} for cid in criteria]\n"
        "write_rulings(db,run_id='RUN-20261002-01',supplier='Synthetic',language='en',rulings=rulings,apply=True)\n"
        "for cid in criteria:\n"
        "    record={'criterion_id':cid,'classification':'fully' if cid=='APP_B_I' else 'na','judge_ruling':'synthetic','rationale':'synthetic chain'}\n"
        "    write_evaluation(db,run_id='RUN-20261002-01',record=record,evidence_ids=['CRUMB-DOC-0001-APP_B_I-0001'] if cid=='APP_B_I' else [],apply=True)\n",
        encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "scripts")
    result = subprocess.run([sys.executable, "-B", str(helper)], cwd=root, env=env, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr


def test_full_synthetic_chain_uses_only_a_temporary_project(tmp_path: Path):
    root = tmp_path / "Ekonerg synthetic Č audit"
    root.mkdir()
    copy_project(root)
    db = root / "db" / "nqa_audit.sqlite"
    assert run(root, "init_db.py", "--db", str(db)).returncode == 0
    assert run(root, "seed_criteria.py", "--db", str(db)).returncode == 0
    raw = root / "raw" / "procedure.txt"
    raw.write_text("# Procedure\n\nSynthetic control.\n\n## Review\n\nThe supplier performs design review.\n", encoding="utf-8")
    digest = hashlib.sha256(raw.read_bytes()).hexdigest()
    (root / "manifests" / "raw_sources.csv").write_text(
        "doc_id,filename,title,supplier,doc_date,language,side_hint,sha256,promoted_utc,source_url,notes\n"
        f"DOC-0001,procedure.txt,Procedure,Synthetic,2026-10-02,en,DOCUMENT,{digest},2026-10-02T00:00:00Z,n-a,synthetic\n", encoding="utf-8")
    with sqlite3.connect(db) as conn:
        conn.execute("INSERT INTO documents(doc_id,filename,title,supplier,doc_date,language,document_side,sha256) VALUES (?,?,?,?,?,?,?,?)",
                     ("DOC-0001", "procedure.txt", "Procedure", "Synthetic", "2026-10-02", "en", "DOCUMENT", digest))
        conn.commit()
    raw.chmod(0o444)
    assert run(root, "extract_text.py", "DOC-0001", "--db", str(db), "--apply").returncode == 0
    assert run(root, "chunk_document.py", "DOC-0001", "--db", str(db), "--apply").returncode == 0
    prompts = root / "sieving" / "prompts"
    (prompts / "active.yml").write_text("schema_version: '1.0'\nactive:\n  DOCUMENT: synthetic_document_v1\n", encoding="utf-8")
    (prompts / "synthetic_document_v1.md").write_text("Synthetic prompt.\n", encoding="utf-8")
    assert run(root, "sieve_run.py", "--db", str(db), "--run-id", "RUN-20261002-01", "--doc-id", "DOC-0001", "--prompt-version", "synthetic_document_v1", "--document-side", "DOCUMENT").returncode == 0
    crumb = root / "sieving" / "synthetic.json"
    crumb.write_text(json.dumps({"document": {"doc_id": "DOC-0001", "name": "procedure.txt", "date": "n-a", "document_side": "DOCUMENT", "authority_references": []}, "items": [{"item_id": "synthetic-1", "criterion_id": "APP_B_I", "criterion_name": "Organization", "statement": "The supplier performs design review.", "item_type": "control", "entities": {}, "sources": [{"source_locator": "Review [line 5]"}], "evidence_quotes": [{"quote_original": "The supplier performs design review.", "quote_language": "en"}]}]}), encoding="utf-8")
    assert run(root, "import_crumbs.py", str(crumb), "--db", str(db), "--run-id", "RUN-20261002-01").returncode == 0
    assert run(root, "link_crumbs.py", "--db", str(db), "--run-id", "RUN-20261002-01", "--apply").returncode == 0
    add_evaluations(root)
    output = root / "outputs"; output.mkdir()
    package, report, data, dashboard = (output / name for name in ("package.json", "report.md", "dashboard.json", "dashboard.html"))
    commands = [
        ("build_evaluation_package.py", "--db", str(db), "--run-id", "RUN-20261002-01", "--approvals", str(root / "manifests" / "approvals.csv"), "--output", str(package)),
        ("generate_report.py", str(package), "--output", str(report)),
        ("build_dashboard_data.py", str(package), "--generated-date", "2026-10-02T00:00:00Z", "--dash-id", "DASH-20261002-0001", "--output", str(data)),
        ("generate_dashboard.py", str(data), "--output", str(dashboard)),
        ("validate_report.py", str(package), str(report)),
        ("validate_dashboard.py", str(package), str(data), str(dashboard)),
    ]
    results = [run(root, script, *args) for script, *args in commands]
    assert all(result.returncode == 0 for result in results), [result.stderr for result in results]
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT count(*) FROM document_chunks").fetchone()[0] == 2
        assert conn.execute("SELECT count(*) FROM crumbs").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM crumb_chunk_links").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM criterion_evaluations").fetchone()[0] == 18
