# Manifests — control ledgers (EPIC 0, Task 0.4)

Human-scannable CSV ledgers of the audit trail. Headers are fixed here before any data
flows; scripts append rows, never rewrite history. Canonical header documentation —
`MASTER_DEVELOPMENT_PLAN.md` Task 0.4 and project guidance reference this file.

## raw_sources.csv

One row per document promoted into `raw/` (Task 3.1/3.2). Values must match the
`documents` DB table exactly.

| column | meaning |
|---|---|
| doc_id | `DOC-nnnn` per `schemas/id_patterns.yml` |
| filename | filename as stored in `raw/` |
| title | human title |
| supplier | supplier key (e.g. `enconet`); `etalon` sources use the supplier they are registered for |
| doc_date | document date (ISO `YYYY-MM-DD`) or `n-a` |
| language | `sl` / `en` / `hr` (`schemas/vocabularies.yml`) |
| side_hint | expected `RULE` / `DOCUMENT` side |
| sha256 | SHA-256 of the promoted file (immutability anchor) |
| promoted_utc | promotion timestamp, UTC ISO-8601 |
| source_url | public source URL (etalon) or `n-a` |
| notes | free text |

## ingest_runs.csv

One row per pipeline run (chunking or sieving).

| column | meaning |
|---|---|
| run_id | `RUN-YYYYMMDD-nn` per ID grammar |
| run_type | `chunk` / `sieve` |
| doc_id | document processed |
| prompt_version | sieving prompt version, `n-a` for chunk runs |
| document_side | `RULE` / `DOCUMENT`, `n-a` for chunk runs |
| started_utc / finished_utc | UTC ISO-8601 timestamps |
| result | `ok` / `failed` / `aborted` |
| notes | free text |

## validation_runs.csv

One row per validator invocation (every EPIC 13 validator appends here).

| column | meaning |
|---|---|
| run_utc | UTC ISO-8601 timestamp |
| validator | script name (e.g. `validate_traceability.py`) |
| phase | `project-state.yml` phase at run time |
| result | `PASS` / `FAIL` / `SKIPPED(phase)` |
| exit_code | integer exit code |
| details | one-line summary (counts, first failure) |

## approvals.csv

One row per human gate/approval decision (header fixed by Task 0.4).

| column | meaning |
|---|---|
| object_id | gate (`G1`…`G7`), finding, ruling set, fixture, or prompt version ID |
| decision | `approved` / `rejected` / `deferred` |
| date | decision date (ISO `YYYY-MM-DD`) |
| reviewer | human reviewer name |
| notes | rationale / conditions |

## link_exceptions.csv

Human-approved quote↔chunk mismatch exceptions (Task 6.2). Unapproved exceptions count
as broken links in validation.

| column | meaning |
|---|---|
| crumb_id | `CRUMB-…` ID |
| quote_id | `QUOTE-…` ID |
| reason | why the quote is not literally in the chunk (table extraction, OCR variance, …) |
| approved_by | human approver |
| date | approval date (ISO `YYYY-MM-DD`) |
