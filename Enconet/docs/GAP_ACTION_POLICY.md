# Gap-to-action policy

| Field | Value |
|---|---|
| Scope | EPIC9 automatic actions for `missing-evidence` gaps |
| Owner | Enconet controlled data contract |
| Update trigger | Gap vocabulary or automatic action rule changes |

Every `missing-evidence` gap receives an open action in the same database transaction.
An explicitly supplied action type must be `verification` or `document_request`.
Otherwise the deterministic default is:

- `document_request` when `missing_evidence_ref` contains the word `document`
  case-insensitively;
- `verification` for every other missing-evidence reference.

This heuristic selects the follow-up workflow only. It does not classify evidence,
create a finding, or replace human audit judgment. Action IDs use the maximum existing
numeric `ACT-` suffix plus one so deletion cannot cause reuse or collision.
