#!/usr/bin/env python3
"""Read-only structure and gate check; PASS is not audit approval."""
import argparse
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import yaml

import db_util
from evaluation_engine import _approval, _approved_model, _connect, _id, _raw_document, ROOT, POSITIVE, score_rating
from project_paths import configure_standard_streams, local_path


def validate(db: Path, run_id: str) -> list[str]:
    _id(run_id, "run_id")
    errors: list[str] = []
    try:
        g2 = _approval(f"G2-{run_id}")
    except ValueError as exc:
        errors.append(str(exc))
        g2 = None
    try:
        scoring = _approved_model(run_id)
    except ValueError as exc:
        errors.append(str(exc))
        scoring = None
    with closing(_connect(db, write=False)) as conn:
        criteria = {r[0] for r in conn.execute("SELECT criterion_id FROM criteria")}
        taxonomy = yaml.safe_load(local_path(ROOT / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))
        canonical = {row["criterion_id"] for row in taxonomy["criteria"]}
        if len(criteria) != 18 or criteria != canonical:
            errors.append("local criteria incomplete")
        run = conn.execute("SELECT scoring_model_version FROM evaluation_runs WHERE run_id=?", (run_id,)).fetchone()
        if run is None:
            errors.append("evaluation run missing")
        elif scoring is not None and run["scoring_model_version"] != scoring["model_version"]:
            errors.append("run scoring model differs from G3 approval")
        rulings = {r["criterion_id"]: r for r in conn.execute(
            "SELECT * FROM criterion_applicability WHERE evaluation_run_id=?", (run_id,))}
        evaluations = {r["criterion_id"]: r for r in conn.execute(
            "SELECT * FROM criterion_evaluations WHERE evaluation_run_id=?", (run_id,))}
        if set(rulings) != criteria:
            errors.append("applicability matrix incomplete")
        if set(evaluations) != criteria:
            errors.append("evaluation records incomplete")
        for cid, ruling in rulings.items():
            try:
                _raw_document(conn, ruling["scope_source_doc_id"])
            except ValueError as exc:
                errors.append(f"{cid}: {exc}")
            if ruling["decision_ref"] != f"G2-{run_id}":
                errors.append(f"G2 decision reference differs: {cid}")
            if g2 is not None and (ruling["approved_by"] != g2["reviewer"] or
                                   ruling["approved_date"] != g2["date"]):
                errors.append(f"G2 signer or date differs: {cid}")
        for cid, evaluation in evaluations.items():
            links = conn.execute("SELECT c.criterion_id,c.document_side,r.is_active FROM evaluation_evidence x "
                                 "JOIN crumbs c ON c.item_id=x.item_id JOIN sieve_runs r ON r.run_id=c.sieve_run_id "
                                 "WHERE x.evaluation_id=?", (evaluation["evaluation_id"],)).fetchall()
            if any(link["criterion_id"] != cid or not link["is_active"] for link in links):
                errors.append(f"inactive or wrong-criterion evidence: {cid}")
            has_document = any(link["document_side"] == "DOCUMENT" and link["is_active"] for link in links)
            if evaluation["rating"] in POSITIVE and not has_document:
                errors.append(f"positive classification without active DOCUMENT evidence: {cid}")
            if evaluation["evidence_supported"] != int(has_document):
                errors.append(f"evidence-supported flag mismatch: {cid}")
            if cid in rulings and (bool(rulings[cid]["applicable"]) == (evaluation["rating"] == "na")):
                errors.append(f"rating conflicts with applicability: {cid}")
            if scoring is not None and evaluation["score"] != score_rating(evaluation["rating"], scoring_model=scoring):
                errors.append(f"score mismatch: {cid}")
        for row in conn.execute("PRAGMA foreign_key_check"):
            errors.append(f"foreign key violation: {tuple(row)}")
    return errors


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=db_util.DEFAULT_DB)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--no-record", action="store_true", help="compatibility: this validator is always read-only")
    args = parser.parse_args()
    try:
        errors = validate(args.db, args.run_id)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"validate_evaluation: FAIL - {error}", file=sys.stderr)
    if errors:
        return 1
    print("validate_evaluation: PASS - 18/18 structurally valid; not audit approval")
    return 0


if __name__ == "__main__":
    from project_paths import configure_standard_streams
    configure_standard_streams()
    raise SystemExit(main())
