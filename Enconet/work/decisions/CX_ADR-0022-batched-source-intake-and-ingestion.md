# ADR-0022 — Bounded source-intake and ingestion batches

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-16 |
| Decided by | Human (project owner) |
| Scope | Enconet source promotion and downstream ingestion |
| Register | Governs `incoming/`, `raw/`, `manifests/raw_sources.csv`, and `manifests/ingest_runs.csv` |
| Authored by | Codex (`CX_` prefix) |

## Context

The owner will place numerous reviewed candidate files in `incoming/`. Processing all
files as one bulk operation would make failures difficult to isolate, weaken review of
per-document metadata, and obscure which sources were newly introduced versus updated
versions of existing documents. Direct placement in `raw/` is already prohibited by
the controlled intake contract and recorded in `LL-RAW-001` and `GP-RAW-001`.

The project already has the necessary per-document audit records:
`manifests/raw_sources.csv` records every successful promotion into immutable `raw/`,
and `manifests/ingest_runs.csv` records downstream processing. This ADR adds bounded
batching and an explicit new/updated classification without weakening those individual
records or overwriting prior source generations.

## Decision

1. Files placed by the owner in `incoming/` form a queue, not an accepted corpus.
   Presence in `incoming/` does not authorize bulk promotion, downstream ingestion, or
   deletion. Each file still requires review and the metadata required by
   `docs/RAW_INTAKE.md`.
2. Source promotion into `raw/` is performed in bounded batches:
   - one large document is processed alone; or
   - two or three small documents are processed together;
   - three documents is the hard maximum; and
   - a large document is never mixed with another document in the same batch.
3. The operator classifies size before starting the batch using document length,
   format complexity, extraction risk, and expected review effort—not filename or file
   count alone. When uncertain, classify the document as large and process it alone.
4. Every promotion batch receives a stable identifier
   `SRC-YYYYMMDD-NNN`. Each file is promoted separately with
   `scripts/promote_source.py`; its `--notes` metadata must include exactly one of:
   - `batch_id=SRC-YYYYMMDD-NNN; change_type=new`; or
   - `batch_id=SRC-YYYYMMDD-NNN; change_type=updated; supersedes=DOC-nnnn`.
   Additional human notes may follow these machine-readable tags.
5. `change_type=new` means no earlier registered document represents the same logical
   source/version lineage. `change_type=updated` means the candidate is a later version
   or replacement of a registered source; it must identify its immediate predecessor
   by `supersedes=DOC-nnnn`. Classification is decided by comparing title/source
   identity, revision/date, and checksum against the current registry, not by filename
   similarity alone.
6. An updated document never overwrites, renames, edits, or reuses the predecessor in
   `raw/`. It enters through `incoming/` under a stable unique filename, receives a new
   SHA-256 and `DOC-nnnn`, and links back through the `supersedes` tag. Identical bytes
   are duplicates, not updates, and promotion must continue to reject them.
7. A promotion batch is complete only when every selected file has either:
   - a successful, individually recorded row in `manifests/raw_sources.csv` and the
     matching SQLite document record; or
   - a recorded batch failure/disposition explaining why it was not promoted.
   The operator then runs `scripts/validate_raw_sources.py`. A failed promotion or
   validation stops the batch and blocks the next batch until reconciled; files not
   selected remain untouched in `incoming/`.
8. Downstream ingestion is also processed in bounded batches: one large document, or
   two to three small documents, with three as the hard maximum. Each document retains
   its own run record in `manifests/ingest_runs.csv`; the `notes` field must include
   `batch_id=ING-YYYYMMDD-NNN`, the source `doc_id`, and the same
   `change_type=new|updated` classification. Updated-document runs also include
   `supersedes=DOC-nnnn`.
9. An ingestion batch starts only from successfully promoted and validated `DOC-nnnn`
   records. Each stage records its own result; one document's success never masks
   another's failure. A failed document stops progression of that batch until the
   failure is resolved or explicitly dispositioned. The next batch does not start
   while the current batch has an unresolved result.
10. Generated text, chunks, sieve runs, and later artifacts follow their existing
    immutable/generational rules. Re-ingesting an updated source creates new derived
    records and generations; it does not mutate evidence derived from the superseded
    raw document.
11. At each session handoff or batch boundary, report at minimum: batch ID, selected
    filenames, assigned document IDs, size class, new/updated classification,
    predecessor IDs for updates, promotion/ingestion results, validation command and
    exit code, remaining incoming queue, and any blocker. “Processed” means recorded
    success, never merely attempted or copied.

## Consequences

- Numerous incoming files can queue safely while work proceeds in reviewable units.
- Promotion and ingestion failures are isolated to at most one large or three small
  documents, reducing provenance and rollback risk.
- `raw_sources.csv` remains the authoritative per-document record of what entered
  `raw/`; `ingest_runs.csv` remains the per-document processing record.
- New and updated documents are explicitly distinguishable, and every update preserves
  its predecessor rather than rewriting controlled evidence.
- Batch tags currently live in the existing `notes` columns. A future schema migration
  may promote them to dedicated columns only under a reviewed, tested migration that
  preserves all historical tags and ADR-0022 semantics.
