# EK-6.3 G2 — Owner applicability approval applied

**Decision date:** 2026-10-03  
**Decision reference:** `G2-RUN-20261003-32`  
**Owner:** Owner  
**Run:** `RUN-20261003-32`

## Result

The owner approved the EK-6.3 preliminary screen:

- 12 criteria are applicable.
- 6 criteria are conditional: VIII, IX, XI, XII, XIII, and XIV.
- 0 criteria are final `NOT_APPLICABLE`.

The database stores all 18 criteria as `applicable=1` because the six
conditional controls remain inside the audit scope. Their written
justifications preserve the conditional decision and require work-sample
confirmation before any later N/A decision.

## Applied records

- Approval ledger: `manifests/approvals.csv`.
- Normalized approved rulings: `out/2026-10-03/EK-6.3-G2/applicability_g2_approved.json`.
- Run-scoped matrix: `out/2026-10-03/EK-6.3-G2/evidence_matrix_g2_applied.md`.
- Database rows: 18 applicability records for `RUN-20261003-32`.

## Validation

- Applicability preview: passed with 18 rulings.
- Applicability apply: passed with 18 rulings.
- Ekonerg script tests: `58 passed`.
- Formal criterion evaluations and scoring are still pending G3 approval and
  human evidence judgments.

## Conditional-evaluation guard

The six conditional criteria are now stored with an explicit
`applicability_state=conditional` value. This keeps them in scope without
letting the scoring engine treat them as confirmed applicable controls.

- A criterion in the conditional state cannot receive a scored rating until
  an owner confirmation reference is recorded.
- `scripts/confirm_applicability.py` records that confirmation and the owner
  approval reference before evaluation can proceed.
- Legacy rows are upgraded from their owner-approved conditional justification
  text without changing source evidence.
- The matrix and validation tools show the conditional state and preserve the
  confirmation reference.

The six rows for `RUN-20261003-32` were migrated successfully and have no
confirmation reference yet. Therefore G3 scoring remains blocked by design.
