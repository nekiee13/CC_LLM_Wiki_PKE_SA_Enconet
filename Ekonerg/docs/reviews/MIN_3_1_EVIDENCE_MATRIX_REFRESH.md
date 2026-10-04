# MIN-3.1 evidence-matrix refresh

**Status:** Draft, non-scoring; owner G2 and G3 records remain in force

## What and why

This refresh connects the current imported crumbs to all 18 Appendix B
criteria. It is a map for the reviewer. It is not a compliance score and does
not create findings.

## Current snapshot

- Run: `RUN-20261003-32`
- Criteria: 18/18 present
- Applicability: 18 applicable, 0 conditional, 0 final N/A
- Evidence rows: 189 document crumbs and 55 RULE crumbs
- Anchored document crumbs: 12
- Findings: 0
- Actions: 0

The low anchor count means most older crumbs still have no typed context. This
does not erase their exact quotes, but it limits traceability until the affected
documents are resieved with the active v3 context-anchor prompt.

## Gate status

Formal evaluation is not run by this task. The owner confirmed the six historic
scope criteria under `G2-HISTORIC-SIX-20261004-OWNER`, so applicability no
longer blocks scoring. Evidence quality still does: policy text is not treated
as proof that staff used a control, and candidate leads remain leads.

## Artifacts

- Matrix: `out/2026-10-04/MIN-3.1-evidence-matrix-v3.md`
- Machine-readable matrix: `out/2026-10-04/MIN-3.1-evidence-matrix-v3.json`
- Source command: `python Ekonerg/scripts/build_matrix.py --db db/nqa_audit.sqlite --run-id RUN-20261003-32 --json out/2026-10-04/MIN-3.1-evidence-matrix-v3.json --markdown out/2026-10-04/MIN-3.1-evidence-matrix-v3.md`

## Next gate

Formal evaluation may now proceed, but no rating or audit conclusion is claimed
by this matrix refresh.
