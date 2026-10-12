# PIVOT-3 context-runtime dry run

All three requested checks passed without changing the live database.

## 1. Migration idempotence

The live database was copied to a disposable project-local file. The context
migration was run twice on that copy.

- Schema hash before: `844345a0a2fa007b628f84be8627a95b3deb5d7a94cb531386a0bfee2399b195`
- Schema hash after first run: same
- Schema hash after second run: same
- Table count: 23 in every snapshot
- Row counts: identical in every snapshot
- Result: **PASS**

## 2. Importer anchor refusal

The importer was given an item with `evidence_type: objective_record` and no
source context anchor. It refused the item with:

```text
items[0].evidence_type requires at least one source context anchor
```

Result: **PASS**. An evidence type is accepted only when at least one of the
five source anchors is present.

## 3. Matrix read-only check

The diagnostic matrix for evaluation run `RUN-20261003-32` was built twice
from the live database without writing matrix files.

- Criteria: 18
- Active sieve runs visible: 31
- Evidence types: `untyped: 189`
- Unanchored document evidence: 189
- Matrix hash before and after: `0bc2c7e12206908f221cf6ca51e54ca692193799d056287e9eae6aac5149332a`
- Result: **PASS**; hash unchanged

The untyped and unanchored values are reported as-is. No historical crumb or
context row was rewritten.

Machine-readable evidence: `PIVOT_3_CONTEXT_RUNTIME_DRY_RUN.json`.

## Post-promotion matrix reconciliation

The earlier dry run intentionally recorded the pre-promotion state. After the
owner-approved v3 DOC-0016 generation became active, a fresh read-only matrix
shows the expected current state: 189 DOCUMENT crumbs, 55 RULE crumbs, and 12
anchored DOCUMENT crumbs. The v3 matrix is
`out/2026-10-04/MIN-3.1-evidence-matrix-v3.md`. No historical crumb or context
row was rewritten; the change is the approved active-generation selection.
