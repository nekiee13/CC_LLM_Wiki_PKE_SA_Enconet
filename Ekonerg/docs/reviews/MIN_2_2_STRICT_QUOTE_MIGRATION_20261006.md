# MIN-2.2 strict quote migration — completed

The owner approved use of the corrected source copy. The controlled generation
promotion command was attempted for DOC-0019 and DOC-0011, but both candidates
were correctly refused because downstream evaluation evidence already points to
the active generations. No generation or crumb ID was replaced.

To apply the approved repair without breaking those downstream links, the
quote text was updated in place for the two affected active quote records:

| Document | Quote | Active run | Result |
|---|---|---|---|
| DOC-0019 | `QUOTE-DOC-0019-0004-01` | `RUN-20261003-14` | exact raw-source chapter text |
| DOC-0011 | `QUOTE-DOC-0011-0034-01` | `RUN-20261005-51` | exact raw-source chapter text |

The migration is quote-only. Criteria, crumb IDs, chapter links, evaluation
rows, ratings, and the dashboard score were not changed.

## Validation

- Dry-run listed exactly two owner-approved quote repairs.
- Apply completed through `scripts/apply_strict_quote_repairs.py`.
- Active-only traceability validation: **PASS**.
- Aggregate validation: **PASS** (with unrelated phase skips reported by the aggregate runner).

The machine record with quote-level hashes is
[`strict-quote-migration-20261006.json`](../../out/2026-10-05/traceability-repair/strict-quote-migration-20261006.json).
