# EK-1.2 candidate: local diagnostic evidence matrix

This slice copies one report script from a versioned, hash-locked template.
It reads the local database and lists the 18 Appendix B criteria with counts
for RULE and company-document evidence, gaps, findings, and actions. The output
is diagnostic. It does not decide applicability, approve evidence, or make an
audit finding.

The script refuses a missing database, an unknown evaluation run, a criterion
set that differs from the local taxonomy, and any database or output path
outside its own project. It opens SQLite read-only. It first-writes JSON and
Markdown files; a repeat with identical content preserves both files, while
a changed or incomplete pair is refused. No source document is required to
test the script.

If any evaluation run exists, the caller must name one run. This stops a
matrix from mixing counts from different audit runs. With no evaluation run,
an unscoped pre-execution matrix is still possible.

Tests use two fake companies, including spaces and a Croatian character, one
with a sibling project and one without. They check preview, apply, retry,
outside-path rejection, row counts, unchanged database bytes and timestamp,
and sibling isolation. The real Ekonerg database and source intake are still
absent. This candidate awaits Claude's technical review; EK-1.2 stays open.

The first preview/apply used `evidence-matrix-20261001-01`. A later RED test
found that an unscoped report could mix existing runs. Before commit, Codex
kept that first copied script as a hash-checked backup in `.bootstrap` and
applied the corrected template under `evidence-matrix-20261001-02`. Both
immutable journals remain. The active script now matches the corrected
template hash; a repeat preview preserves it.
