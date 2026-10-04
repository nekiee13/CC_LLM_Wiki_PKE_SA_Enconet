# MIN-3.1 evidence-matrix refresh

**Status:** Draft, non-scoring; owner G2 and G3 records remain in force

## What and why

This refresh connects the current imported crumbs to all 18 Appendix B
criteria. It is a map for the reviewer. It is not a compliance score and does
not create findings.

## Current snapshot

- Run: `RUN-20261003-32`
- Criteria: 18/18 present
- Applicability: 12 applicable, 6 conditional, 0 final N/A
- Evidence rows: 189 document crumbs and 54 rule crumbs
- Anchored document crumbs: 11
- Findings: 0
- Actions: 0

The low anchor count means most older crumbs still have no typed context. This
does not erase their exact quotes, but it limits traceability until the affected
documents are resieved with the active v3 context-anchor prompt.

## Gate status

Formal evaluation is not run by this task. The six conditional criteria still
need owner confirmation before they can receive a scored rating. Policy text is
not treated as proof that staff used a control. Candidate leads remain leads.

## Artifacts

- Matrix: `out/2026-10-04/MIN-3.1-evidence-matrix.md`
- Machine-readable matrix: `out/2026-10-04/MIN-3.1-evidence-matrix.json`
- Source command: `python Ekonerg/scripts/build_matrix.py --db db/nqa_audit.sqlite --run-id RUN-20261003-32 --json out/2026-10-04/MIN-3.1-evidence-matrix.json --markdown out/2026-10-04/MIN-3.1-evidence-matrix.md`

## Next gate

Owner must confirm whether the six conditional controls are demonstrated by
Ekonerg work samples before formal evaluation can proceed. No rating or audit
conclusion is claimed here.
