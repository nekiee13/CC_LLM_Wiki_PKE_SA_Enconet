# Document chunking procedure

EPIC 4 operates only on registered documents whose extracted UTF-8 text exists at
`derived/DOC-nnnn.txt`.

Run `python scripts/chunk_document.py DOC-nnnn`. For Markdown sources, ATX level-1
and level-2 headings (`#` and `##`) start chunks and take precedence over numeric
lines so numbered lists are not mistaken for chapters. Markdown heading paths retain
the heading text and source line number, for example
`Manual [line 1] > Scope [line 8]`, so repeated titles remain distinct and auditable.
Level-3 and deeper Markdown headings remain inside their level-2 parent.

When no Markdown level-1/2 headings exist, lines beginning with a numeric level-1
heading (`1.`) or level-2 heading (`1.1`) start chunks. Level-3 and deeper numeric
headings remain inside their level-2 parent. The stored numeric heading path is `1`
or `1 > 1.1`; chunk offsets always refer to the complete derived text.

If no supported level-1/2 heading exists, the entire non-empty document becomes one
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
