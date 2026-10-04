"""Project-local, approval-gated evaluation operations; no audit decision is inferred."""
from __future__ import annotations

import csv
from contextlib import closing
from decimal import Decimal, ROUND_HALF_UP
import hashlib
from pathlib import Path
import sqlite3

import yaml

import db_util
from project_paths import local_path

ROOT = Path(__file__).resolve().parents[1]
APPROVALS = ROOT / "manifests/approvals.csv"
MODEL = ROOT / "schemas/scoring_model.yml"
RAW = ROOT / "raw"
RATINGS = {"fully", "substantially", "partially", "minimally", "unmet", "undetermined", "na"}
POSITIVE = {"fully", "substantially"}
CONDITIONAL_BLOCKED_RATINGS = RATINGS - {"undetermined"}
DIMENSIONS = ("coverage", "completeness", "accuracy", "clarity", "alignment")
SUMMARIES = ("affirmative_summary", "contrary_summary", "judge_ruling", "rationale")


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty text")
    return value.strip()


def _id(value: object, pattern: str) -> str:
    value = _text(value, pattern)
    if db_util.id_patterns()[pattern].fullmatch(value) is None:
        raise ValueError(f"invalid {pattern}: {value}")
    return value


def _connect(path: Path, *, write: bool) -> sqlite3.Connection:
    database = local_path(path)
    if not database.is_file():
        raise ValueError(f"local database is missing: {database}")
    conn = sqlite3.connect(database.as_uri() + ("?mode=rw" if write else "?mode=ro"), uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    if not write:
        conn.execute("PRAGMA query_only=ON")
    return conn


def _approval(object_id: str) -> dict[str, str]:
    path = local_path(APPROVALS)
    if not path.is_file():
        raise ValueError(f"approval missing: {object_id}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["object_id", "decision", "date", "reviewer", "notes"]:
            raise ValueError("approval ledger header is invalid")
        rows = [row for row in reader if row["object_id"] == object_id]
    if len(rows) != 1 or rows[0]["decision"] != "approved" or not rows[0]["date"] or not rows[0]["reviewer"]:
        raise ValueError(f"signed approval missing or ambiguous: {object_id}")
    return rows[0]


def model() -> dict:
    data = yaml.safe_load(local_path(MODEL).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("rating_weights"), dict):
        raise ValueError("scoring model is invalid")
    return data


def _approved_model(run_id: str) -> dict:
    data = model()
    ref = f"G3-{run_id}"
    version = _text(data.get("model_version"), "model_version")
    if data.get("calibration_status") != "approved" or data.get("approval_ref") != ref or "placeholder" in version.lower():
        raise ValueError("Gate G3 model calibration is not approved for this run")
    row = _approval(ref)
    if version not in row["notes"]:
        raise ValueError("Gate G3 approval does not name the model version")
    if set(data["rating_weights"]) != RATINGS or data["rating_weights"]["na"] is not None:
        raise ValueError("scoring model rating weights are invalid")
    for rating in RATINGS - {"na"}:
        value = data["rating_weights"][rating]
        if type(value) not in (int, float) or not 0 <= value <= 1:
            raise ValueError("scoring model rating weights are invalid")
    return data


def score_rating(rating: str, *, scoring_model: dict | None = None) -> float | None:
    if rating not in RATINGS:
        raise ValueError(f"invalid rating: {rating}")
    weights = (scoring_model or model())["rating_weights"]
    weight = weights[rating]
    return None if weight is None else float((Decimal(str(weight)) * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def _raw_document(conn: sqlite3.Connection, doc_id: str) -> None:
    doc = conn.execute("SELECT filename,sha256,document_side FROM documents WHERE doc_id=?", (doc_id,)).fetchone()
    if doc is None:
        raise ValueError(f"scope source is not a registered document: {doc_id}")
    if doc["document_side"] == "RULE" and conn.execute(
            "SELECT 1 FROM approved_sources WHERE source_sha256=? AND authority_role='GOVERNING'",
            (doc["sha256"],)).fetchone() is None:
        raise ValueError(f"scope RULE source lacks approved governing-source record: {doc_id}")
    if doc["document_side"] not in {"RULE", "DOCUMENT"}:
        raise ValueError(f"scope source has an invalid document side: {doc_id}")
    path = local_path(RAW / doc["filename"])
    if not path.is_relative_to(RAW) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != doc["sha256"]:
        raise ValueError(f"scope source raw bytes missing or changed: {doc_id}")


def _ensure_applicability_guard_schema(conn: sqlite3.Connection) -> None:
    """Upgrade older local databases before writing applicability decisions.

    The project database predates the explicit conditional state.  The upgrade
    is additive and derives the six already-approved conditional rows from
    their owner-approved justification text once, preserving all source data.
    """
    columns = {row[1] for row in conn.execute("PRAGMA table_info(criterion_applicability)")}
    if "applicability_state" not in columns:
        conn.execute(
            "ALTER TABLE criterion_applicability ADD COLUMN applicability_state TEXT NOT NULL DEFAULT 'applicable' "
            "CHECK (applicability_state IN ('applicable','conditional','not-applicable'))"
        )
    if "conditional_confirmation_ref" not in columns:
        conn.execute(
            "ALTER TABLE criterion_applicability ADD COLUMN conditional_confirmation_ref TEXT"
        )
    conn.execute(
        "UPDATE criterion_applicability SET applicability_state='conditional' "
        "WHERE applicable=1 AND lower(justification) LIKE '%conditional%' "
        "AND applicability_state='applicable' "
        "AND conditional_confirmation_ref IS NULL"
    )
    conn.execute(
        "UPDATE criterion_applicability SET applicability_state='not-applicable' "
        "WHERE applicable=0 AND applicability_state='applicable'"
    )


def _applicability_state(item: dict) -> tuple[str, str | None]:
    """Normalize a ruling while keeping legacy G2 JSON readable."""
    justification = item["justification"]
    state = item.get("applicability_state")
    if state is None:
        state = "conditional" if "conditional" in justification.casefold() else (
            "applicable" if item["applicable"] else "not-applicable"
        )
    if state not in {"applicable", "conditional", "not-applicable"}:
        raise ValueError("invalid applicability_state")
    if state == "not-applicable" and item["applicable"]:
        raise ValueError("not-applicable state requires applicable=false")
    if state in {"applicable", "conditional"} and not item["applicable"]:
        raise ValueError("applicable or conditional state requires applicable=true")
    confirmation = item.get("conditional_confirmation_ref")
    if confirmation is not None:
        confirmation = _text(confirmation, "conditional_confirmation_ref")
    if state == "conditional" and confirmation:
        raise ValueError("conditional ruling cannot carry a confirmation reference")
    return state, confirmation


def _check_conditional_evaluation(ruling: sqlite3.Row | dict, rating: str) -> None:
    """Reject scored classifications until a conditional scope is confirmed."""
    if (ruling["applicability_state"] == "conditional" and
            not ruling["conditional_confirmation_ref"] and
            rating in CONDITIONAL_BLOCKED_RATINGS):
        raise ValueError("conditional applicability requires confirmation before evaluation")


def confirm_applicability(db: Path, *, run_id: str, criterion_id: str,
                          confirmation_ref: str, apply: bool = False) -> dict:
    """Record an approved confirmation for one previously conditional criterion."""
    _id(run_id, "run_id")
    criterion_id = _text(criterion_id, "criterion_id")
    confirmation = _approval(_text(confirmation_ref, "confirmation_ref"))
    with closing(_connect(db, write=apply)) as conn:
        if apply:
            conn.execute("BEGIN IMMEDIATE")
            _ensure_applicability_guard_schema(conn)
        row = conn.execute(
            "SELECT applicability_state, conditional_confirmation_ref "
            "FROM criterion_applicability WHERE evaluation_run_id=? AND criterion_id=?",
            (run_id, criterion_id),
        ).fetchone()
        if row is None:
            raise ValueError("applicability ruling is missing")
        if row["applicability_state"] != "conditional":
            raise ValueError("only a conditional ruling can be confirmed")
        if conn.execute(
                "SELECT 1 FROM criterion_evaluations WHERE evaluation_run_id=? AND criterion_id=?",
                (run_id, criterion_id)).fetchone() is not None:
            raise ValueError("confirmation is refused after evaluation evidence exists")
        if apply:
            conn.execute(
                "UPDATE criterion_applicability SET applicability_state='applicable', "
                "conditional_confirmation_ref=?, approved_by=?, approved_date=? "
                "WHERE evaluation_run_id=? AND criterion_id=?",
                (confirmation_ref, confirmation["reviewer"], confirmation["date"],
                 run_id, criterion_id),
            )
            conn.commit()
    return {"mode": "apply" if apply else "preview", "run_id": run_id,
            "criterion_id": criterion_id, "confirmation_ref": confirmation_ref}


def write_rulings(db: Path, *, run_id: str, supplier: str, language: str,
                  rulings: object, apply: bool = False) -> dict:
    _id(run_id, "run_id")
    supplier = _text(supplier, "supplier")
    language = _text(language, "language")
    approval = _approval(f"G2-{run_id}")
    if not isinstance(rulings, list) or len(rulings) != 18:
        raise ValueError("exactly 18 applicability rulings required")
    normalized = []
    for item in rulings:
        allowed = {"criterion_id", "applicable", "justification", "scope_source_doc_id",
                   "applicability_state", "conditional_confirmation_ref"}
        if not isinstance(item, dict) or not set(item) <= allowed or not {
            "criterion_id", "applicable", "justification", "scope_source_doc_id"
        } <= set(item):
            raise ValueError("applicability ruling has missing or unknown fields")
        if type(item["applicable"]) is not bool:
            raise ValueError("applicable must be true or false")
        state, confirmation = _applicability_state(item)
        normalized.append({"criterion_id": _text(item["criterion_id"], "criterion_id"),
                           "applicable": int(item["applicable"]),
                           "applicability_state": state,
                           "conditional_confirmation_ref": confirmation,
                           "justification": _text(item["justification"], "justification"),
                           "scope_source_doc_id": _id(item["scope_source_doc_id"], "doc_id"),
                           "approved_by": approval["reviewer"], "approved_date": approval["date"],
                           "decision_ref": f"G2-{run_id}"})
    with closing(_connect(db, write=apply)) as conn:
        if apply:
            conn.execute("BEGIN IMMEDIATE")
            _ensure_applicability_guard_schema(conn)
        criteria = {row[0] for row in conn.execute("SELECT criterion_id FROM criteria")}
        taxonomy = yaml.safe_load(local_path(ROOT / "schemas/app_b_taxonomy.yml").read_text(encoding="utf-8"))
        canonical = {row["criterion_id"] for row in taxonomy["criteria"]}
        if len(criteria) != 18 or criteria != canonical or {row["criterion_id"] for row in normalized} != criteria or len({row["criterion_id"] for row in normalized}) != 18:
            raise ValueError("rulings must cover the 18 local criteria exactly once")
        for item in normalized:
            _raw_document(conn, item["scope_source_doc_id"])
        existing = conn.execute("SELECT * FROM evaluation_runs WHERE run_id=?", (run_id,)).fetchone()
        if existing is not None:
            rows = conn.execute("SELECT * FROM criterion_applicability WHERE evaluation_run_id=?", (run_id,)).fetchall()
            expected = {r["criterion_id"]: r for r in normalized}
            if existing["supplier"] != supplier or existing["deliverable_language"] != language or len(rows) != 18 or any(
                any(row[key] != expected[row["criterion_id"]][key] for key in expected[row["criterion_id"]]) for row in rows
            ):
                raise ValueError("existing applicability run differs; refusing rewrite")
            if apply:
                conn.commit()
            return {"mode": "preserve" if apply else "preview", "run_id": run_id, "rulings": 18}
        if apply:
            db_util.insert(conn, "evaluation_runs", {"run_id": run_id, "supplier": supplier,
                "deliverable_language": language, "scoring_model_version": model()["model_version"]})
            for item in normalized:
                db_util.insert(conn, "criterion_applicability", {"evaluation_run_id": run_id, **item})
            conn.commit()
        return {"mode": "apply" if apply else "preview", "run_id": run_id, "rulings": 18}


def write_evaluation(db: Path, *, run_id: str, record: object,
                     evidence_ids: list[str], apply: bool = False) -> dict:
    _id(run_id, "run_id")
    scoring = _approved_model(run_id)
    _approval(f"G2-{run_id}")
    if not isinstance(record, dict) or set(record) - ({"criterion_id", "classification"} | set(DIMENSIONS) | set(SUMMARIES)):
        raise ValueError("evaluation record has unknown fields")
    cid = _text(record.get("criterion_id"), "criterion_id")
    rating = record.get("classification")
    if rating not in RATINGS:
        raise ValueError("invalid classification")
    values = {}
    for name in DIMENSIONS:
        value = record.get(name, 0)
        if type(value) not in (int, float) or not 0 <= value <= 1:
            raise ValueError(f"{name} must be a number from 0 to 1")
        values[name] = value
    for name in SUMMARIES:
        value = record.get(name, "")
        if not isinstance(value, str):
            raise ValueError(f"{name} must be text")
        values[name] = value.strip()
    if not values["judge_ruling"] or not values["rationale"]:
        raise ValueError("human judge_ruling and rationale are required")
    if not isinstance(evidence_ids, list) or len(set(evidence_ids)) != len(evidence_ids):
        raise ValueError("evidence IDs must be unique")
    for item in evidence_ids:
        _id(item, "crumb_id")
    eid = _id(f"EVAL-{cid}", "evaluation_id")
    with closing(_connect(db, write=apply)) as conn:
        if apply:
            conn.execute("BEGIN IMMEDIATE")
        run = conn.execute("SELECT scoring_model_version FROM evaluation_runs WHERE run_id=?", (run_id,)).fetchone()
        if run is None or run["scoring_model_version"] != scoring["model_version"]:
            raise ValueError("evaluation run scoring model differs from approved G3 version")
        ruling = conn.execute("SELECT applicable, applicability_state, conditional_confirmation_ref "
                              "FROM criterion_applicability WHERE evaluation_run_id=? AND criterion_id=?",
                              (run_id, cid)).fetchone()
        if ruling is None:
            raise ValueError("approved applicability ruling missing")
        if (not ruling["applicable"] and rating != "na") or (ruling["applicable"] and rating == "na"):
            raise ValueError("classification conflicts with applicability ruling")
        _check_conditional_evaluation(ruling, rating)
        if rating == "na" and (evidence_ids or any(values[name] for name in DIMENSIONS)):
            raise ValueError("not-applicable record must not carry evidence or scored dimensions")
        document_count = 0
        for item in evidence_ids:
            crumb = conn.execute("SELECT criterion_id,document_side FROM active_crumbs WHERE item_id=?", (item,)).fetchone()
            if crumb is None or crumb["criterion_id"] != cid:
                raise ValueError(f"evidence crumb is missing, inactive, or wrong criterion: {item}")
            document_count += crumb["document_side"] == "DOCUMENT"
        if rating in POSITIVE and not document_count:
            raise ValueError("positive classification requires linked active DOCUMENT crumb")
        row = {"evaluation_id": eid, "evaluation_run_id": run_id, "criterion_id": cid,
               "rating": rating, "score": score_rating(rating, scoring_model=scoring),
               "evidence_supported": int(bool(document_count)), **values}
        existing = conn.execute("SELECT * FROM criterion_evaluations WHERE evaluation_id=?", (eid,)).fetchone()
        if existing is not None:
            links = {r[0] for r in conn.execute("SELECT item_id FROM evaluation_evidence WHERE evaluation_id=?", (eid,))}
            if any(existing[key] != value for key, value in row.items()) or links != set(evidence_ids):
                raise ValueError("existing evaluation differs; refusing rewrite")
            return {"mode": "preserve" if apply else "preview", "evaluation_id": eid, "rating": rating}
        if apply:
            db_util.insert(conn, "criterion_evaluations", row)
            for item in evidence_ids:
                db_util.insert(conn, "evaluation_evidence", {"evaluation_id": eid, "item_id": item})
            conn.commit()
        return {"mode": "apply" if apply else "preview", "evaluation_id": eid, "rating": rating}


def metrics(rows: list[dict], *, scoring_model: dict) -> dict:
    if len(rows) != 18 or any(row.get("rating") not in RATINGS for row in rows):
        raise ValueError("exactly 18 valid evaluation ratings required")
    applicable = [row for row in rows if row["rating"] != "na"]
    if not applicable:
        raise ValueError("no applicable criteria to score")
    weights = scoring_model["rating_weights"]
    raw = Decimal(100) * sum(Decimal(str(weights[row["rating"]])) for row in applicable) / len(applicable)
    consolidated = float(raw.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    thresholds = scoring_model["classification_thresholds"]
    if not isinstance(thresholds, list) or not thresholds:
        raise ValueError("classification thresholds missing")
    classification = next((row["class"] for row in thresholds if consolidated >= row["min_score"]), None)
    if classification is None:
        raise ValueError("classification thresholds do not cover score")
    return {"consolidated_score": consolidated, "classification": classification,
            "applicable_count": len(applicable),
            "classification_counts": {rating: sum(row["rating"] == rating for row in rows) for rating in sorted(RATINGS)}}
