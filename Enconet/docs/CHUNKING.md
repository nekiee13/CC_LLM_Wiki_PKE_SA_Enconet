# Document chunking procedure

EPIC 4 operates only on registered documents whose extracted UTF-8 text exists at
`derived/DOC-nnnn.txt`.

Run `python scripts/chunk_document.py DOC-nnnn`. Lines beginning with a numeric
level-1 heading (`1.`) or level-2 heading (`1.1`) start chunks. Level-3 and deeper
headings remain inside their level-2 parent. The stored heading path is `1` or
`1 > 1.1`; chunk offsets always refer to the complete derived text.

If no level-1/2 numeric heading exists, the entire non-empty document becomes one
`whole-document` chunk and the command emits a warning. This fallback preserves all
source text for later review instead of inventing semantic boundaries.

`--min-chars` and `--max-chars` configure quality bounds. Bound violations are
warnings, with oversized chunks explicitly marked for manual splitting. Empty
documents and duplicate heading paths are rejected. Re-running the command replaces
all chunks for that document in one SQLite transaction, so old and new generations
cannot mix.

Run `python scripts/validate_chunks.py` to re-check chunk IDs, document ownership,
source checksums, non-empty text, and exact offset slicing. The validator appends its
PASS or FAIL summary to `manifests/validation_runs.csv`.
