#!/usr/bin/env python3
"""Write the owner-requested, evidence-based evaluation for the current Ekonerg run.

The five-point scale follows the approved local model:
5 fully (100), 4 substantially (75), 3 partially (50), 2 minimally (25),
and 1 unmet (0).  The ordinal point is shown in the review artifact; the
canonical database score remains the Enconet 0/25/50/75/100 percentage.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from evaluation_engine import write_evaluation


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "db" / "nqa_audit.sqlite"
DEFAULT_OUTPUT = ROOT / "out" / "2026-10-05" / "EKONERG_EVALUATION_20261005.json"
RUN_ID = "RUN-20261003-32"

# This is the documented first-pass judgment from the active Ekonerg vendor
# snapshot.  It is intentionally explicit rather than inferred from crumb count
# alone: objective-control crumbs support a positive rating; a missing vendor
# crumb cannot support conformance.
RATINGS = {
    "APP_B_I": "substantially",
    "APP_B_II": "substantially",
    "APP_B_III": "substantially",
    "APP_B_IV": "partially",
    "APP_B_V": "substantially",
    "APP_B_VI": "fully",
    "APP_B_VII": "substantially",
    "APP_B_VIII": "unmet",
    "APP_B_IX": "unmet",
    "APP_B_X": "substantially",
    "APP_B_XI": "unmet",
    "APP_B_XII": "partially",
    "APP_B_XIII": "unmet",
    "APP_B_XIV": "unmet",
    "APP_B_XV": "partially",
    "APP_B_XVI": "substantially",
    "APP_B_XVII": "fully",
    "APP_B_XVIII": "substantially",
}

POINTS = {"fully": 5, "substantially": 4, "partially": 3, "minimally": 2, "unmet": 1}
DIMENSIONS = {"fully": 0.95, "substantially": 0.75, "partially": 0.50, "minimally": 0.25, "unmet": 0.0}

RATIONALES = {
    "APP_B_I": "Named Ekonerg roles, procedure ownership, management approval, training, equipment, and customer responsibility controls are present, but many are candidate leads rather than implementation records.",
    "APP_B_II": "The management manual and quality-plan controls directly describe the Appendix B program and its tailoring, but lower-level implementation records are not in the active set.",
    "APP_B_III": "Design planning, input review, verification, change control, and independent final review are stated in vendor procedures; project-level design records still need sampling.",
    "APP_B_IV": "Offer and contract review controls are present, with procurement-document content leads, but the active vendor set does not show complete regulatory and QA flow-down text.",
    "APP_B_V": "Ekonerg procedures define scope, sequence, work steps, personnel, equipment, acceptance criteria, and records; representative job instructions are not fully present.",
    "APP_B_VI": "Document content, review, approval, revision, distribution, controlled copies, and obsolete-document controls are directly supported by vendor objective-control crumbs.",
    "APP_B_VII": "Supplier selection, evaluation, acceptance, contract review, and corrective-action controls are described; supplier implementation records are not supplied.",
    "APP_B_VIII": "The criterion is in scope, but the active Ekonerg vendor snapshot contains no direct vendor crumb for material, part, or component identification control.",
    "APP_B_IX": "The criterion is in scope, but the active Ekonerg vendor snapshot contains no direct vendor crumb for special-process qualification or control.",
    "APP_B_X": "Independent verification, inspection scope, supplier surveillance, and management-input controls are present, but completed inspection records are not supplied.",
    "APP_B_XI": "The criterion is in scope, but the active Ekonerg vendor snapshot contains no direct vendor crumb for a controlled test program or test results.",
    "APP_B_XII": "The procedure covers serviceable equipment, calibration, adjustment, intervals, records, and status marking; calibration certificates and use records are absent.",
    "APP_B_XIII": "The criterion is in scope, but the active Ekonerg vendor snapshot contains no direct vendor crumb for handling, storage, preservation, or shipping controls.",
    "APP_B_XIV": "The criterion is in scope, but the active Ekonerg vendor snapshot contains no direct vendor crumb for inspection, test, or operating-status identification.",
    "APP_B_XV": "Nonconformance reporting, severity evaluation, segregation, disposition, and customer consent are described, but completed Part 21/nonconformance records are absent.",
    "APP_B_XVI": "Complaint, corrective-action, trend, closure, follow-up, and Part 21 escalation controls are directly described, but executed records are not supplied.",
    "APP_B_XVII": "Record identification, collection, storage, retention, disposal, archives, and objective-evidence definitions are directly supported; sampled records are not supplied.",
    "APP_B_XVIII": "Audit planning, objective-evidence comparison, reporting, approval, periodic review, and supplier monitoring are described, but completed audit files are absent.",
}


def build_records(db: Path) -> tuple[list[dict], dict[str, list[str]]]:
    connection = sqlite3.connect(str(db))
    connection.row_factory = sqlite3.Row
    try:
        crumbs: dict[str, list[str]] = {cid: [] for cid in RATINGS}
        for row in connection.execute(
            "SELECT item_id, criterion_id FROM active_crumbs "
            "WHERE document_side='DOCUMENT' ORDER BY criterion_id, item_id"
        ):
            if row["criterion_id"] in crumbs:
                crumbs[row["criterion_id"]].append(row["item_id"])
        records = []
        for cid, rating in RATINGS.items():
            record = {
                "criterion_id": cid,
                "classification": rating,
                "coverage": DIMENSIONS[rating],
                "completeness": DIMENSIONS[rating],
                "accuracy": DIMENSIONS[rating],
                "clarity": DIMENSIONS[rating],
                "alignment": DIMENSIONS[rating],
                "affirmative_summary": f"Active Ekonerg vendor evidence supports the {rating} classification under the Appendix B comparison.",
                "contrary_summary": "The rating is limited by missing implementation records, incomplete detail, or no direct vendor crumb as stated in the rationale.",
                "judge_ruling": f"{rating.title()} ({POINTS[rating]}/5) — Codex evidence evaluation under the owner's instruction to score every criterion.",
                "rationale": RATIONALES[cid],
            }
            records.append(record)
        return records, crumbs
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    records, evidence = build_records(args.db)
    results = []
    for record in records:
        result = write_evaluation(
            args.db,
            run_id=args.run_id,
            record=record,
            evidence_ids=evidence[record["criterion_id"]],
            apply=args.apply,
        )
        results.append({**result, "criterion_id": record["criterion_id"], "rating": record["classification"],
                        "points": POINTS[record["classification"]], "evidence_count": len(evidence[record["criterion_id"]])})
    payload = {"run_id": args.run_id, "scale": POINTS, "records": results}
    if args.apply:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"mode": "apply" if args.apply else "preview", "run_id": args.run_id,
                      "criteria": len(results), "output": str(args.output) if args.apply else None}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
