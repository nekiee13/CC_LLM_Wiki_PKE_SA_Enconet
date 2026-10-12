# MIN-2.2 v3 scope decision — owner approved option 2

The owner selected **option 2: approve the larger corrected candidate sets for
controlled review**.

| Document | Active scope | Corrected candidate scope | Decision reference |
|---|---:|---:|---|
| DOC-0016 | 12 crumbs | 28 items | `SCOPE-DOC0016-V3-20261006-OWNER` |
| DOC-0021 | 12 crumbs | 21 items | `SCOPE-DOC0021-V3-20261006-OWNER` |

This is a scope decision, not an automatic promotion. The corrected files are
kept inactive while the controlled process completes:

1. Review the candidate diff against the active generation.
2. Run the candidate's golden calibration and strict score.
3. Record a separate generation-promotion decision if the gates pass.
4. Reconcile downstream evaluation evidence before changing active generations.

The active database, active 12-crumb generations, ratings, and dashboard remain
unchanged until those gates are complete.
