# Controlled raw-source intake

This is the operating procedure for `MASTER_DEVELOPMENT_PLAN.md` EPIC 3. A source is
not accepted merely because it exists in the workspace: it must pass human review,
promotion, registration, extraction, and validation.

ADR-0022 governs batch size and lineage recording. Treat `incoming/` as a queue. Select
one large document, or two to three small documents, for a promotion batch; never
process more than three or mix a large document with another file. Add the required
`batch_id`, `change_type`, and (for updates) `supersedes` tags to `--notes`. Complete
and validate the selected batch before starting another. Downstream ingestion follows
the same one-large or two-to-three-small limit and records its own `ING-*` batch ID in
`manifests/ingest_runs.csv`.

1. Place the reviewed file directly in `incoming/`. Use a stable, unique filename.
2. Initialize the project database once with `python scripts/init_db.py` if needed.
3. Run `python scripts/promote_source.py <filename> --title <title> --supplier
   <supplier> --doc-date YYYY-MM-DD --language <sl|en|hr> --side <RULE|DOCUMENT>`.
   Optional provenance is supplied with `--source-url` and `--notes`.
4. Promotion moves the file to `raw/`, removes write permissions, computes SHA-256,
   allocates the next `DOC-nnnn`, and writes the same provenance to SQLite and
   `manifests/raw_sources.csv`. A duplicate filename or checksum fails closed.
5. Run `python scripts/extract_text.py DOC-nnnn`. Supported text-family inputs are
   UTF-8 TXT, Markdown, CSV, JSON, XML, and HTML. Other formats require an approved,
   explicitly recorded extractor; silent or lossy fallback is forbidden.
6. Run `python scripts/validate_raw_sources.py`. Any checksum mismatch, writable raw
   file, missing registered file, unregistered file, or DB/manifest divergence fails.

On POSIX, promotion clears user/group/other write bits. On Windows, Python maps the
same operation to the file's read-only mode. These controls prevent accidental edits;
the SHA-256 registry detects changes even if permissions are later bypassed. Never
edit or replace a file in `raw/` in place. A revised source enters through `incoming/`
under a new reviewed filename and receives its own document ID.
An updated document is therefore promoted as a new immutable source record with
`change_type=updated; supersedes=DOC-nnnn`; the predecessor remains unchanged.
