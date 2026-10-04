# MIN-2.2 sprint repair — traceability and requirement rows

**Date:** 2026-10-05
**Status:** partial; the gate remains open
**Scope:** one aggregate repair batch; no new document slice was opened.

## What changed

1. Preserved the pre-link metrics for runs `RUN-20261003-05`,
   `RUN-20261003-14`, and `RUN-20261003-23` under
   `out/2026-10-05/traceability-repair/prelink-metrics/`.
2. Used the existing `link_crumbs.py` preview and apply path. Exact or
   presentation-only matches added links; unmatched text was not forced.
3. Added `evidence_matching.py`. It handles Markdown/HTML presentation noise
   and duplicate list markers from extraction. It does not case-fold, apply
   Unicode normalization, use a similarity score, or accept ellipsis excerpts.
   A link is valid only when the quote is a source substring after that
   presentation-only cleanup.
4. Added `seed_requirements.py`. It previews and idempotently seeds distinct
   requirement statements from active RULE crumbs. It does not write scores,
   evaluations, findings, or source documents.

## Checks

```text
python -m pytest Ekonerg/scripts/tests/test_evidence_matching.py Ekonerg/scripts/tests/test_seed_requirements.py -q
exit 0 — 7 passed

python -m pytest Ekonerg/scripts/tests -q
exit 0 — 83 passed

python -m pytest Ekonerg/scripts/tests Ekonerg/sieving/tests -q
exit 0 — 176 passed, 11 subtests passed

python Ekonerg/scripts/seed_requirements.py --db db/nqa_audit.sqlite
exit 0 — preview: 18 criteria, 55 planned rows, 55 missing

python Ekonerg/scripts/seed_requirements.py --db db/nqa_audit.sqlite --apply
exit 0 — inserted 55 rows

python Ekonerg/scripts/validate_requirements.py --db db/nqa_audit.sqlite --no-record
exit 0 — 18 criteria covered
```

The aggregate validation is still red:

```text
python Ekonerg/scripts/run_all_validations.py --no-record
exit 1 — sieving_harness, traceability
```

Claude confirmed that the `sieving-tuning` skill counterpart is now present,
so the harness gate is cleared. With the stricter source-substring matcher,
the traceability validator now reports 16 unresolved quote records across all
generations. Four are in active runs:

- `QUOTE-DOC-0030-0002-01`: source wording differs (`Uvjeti` versus `Uvjete`).
- `QUOTE-DOC-0001-0004-01`: the stored quote is not a raw substring of its
  linked chunk.
- `QUOTE-DOC-0001-0006-01`: the stored quote is not a raw substring of its
  linked chunk.
- `QUOTE-DOC-0011-0011-01`: no raw source substring link exists (`imaju`
  versus `imati`).

The active-link reconciliation currently finds 318 link rows: 313 exact raw
substrings and 5 non-exact links. The four active quote records above include
two quotes without links. Claude's review identifies seven non-exact active
crumbs when counting the source-side quote set; this count difference is under
reconciliation and is not being hidden by matcher relaxation.

The corrected non-exact list is recorded by quote ID and full item ID:

- `QUOTE-DOC-0030-0002-01` — `CRUMB-DOC-0030-APP_B_XVI-0002`
- `QUOTE-DOC-0030-0003-01` — `CRUMB-DOC-0030-APP_B_XVI-0003`
- `QUOTE-DOC-0019-0004-01` — `CRUMB-DOC-0019-APP_B_III-0003`
- `QUOTE-DOC-0001-0004-01` — `CRUMB-DOC-0001-APP_B_XVI-0003`
- `QUOTE-DOC-0001-0006-01` — `CRUMB-DOC-0001-APP_B_IV-0001`
- `QUOTE-DOC-0011-0010-01` — `CRUMB-DOC-0011-APP_B_VI-0002`
- `QUOTE-DOC-0011-0011-01` — `CRUMB-DOC-0011-APP_B_VI-0003`

`CRUMB-DOC-0001-APP_B_XVI-0004` is not listed because its quote is an exact
match. `CRUMB-DOC-0001-APP_B_XVI-0003` contains one exact quote and one
non-exact quote; only `QUOTE-DOC-0001-0004-01` is listed above.

The owner decision `R01-PART21-GEN2-PROMOTE-20261005-OWNER` and the golden
fixture approval `GOLDEN-DOC0001-PART21-20261005-OWNER` are recorded in
`manifests/approvals.csv`. The strict score passed and the controlled command
promoted `RUN-20261003-24`; `RUN-20261003-23` is now superseded. No exception
or audit conformity score was created for any traceability mismatch.

The post-repair generated-state hash is:

- `db/nqa_audit.sqlite`: `c54a479cb5dc0ef725b6521fa78ab39ea6a25eb118d5e7e8a5aead06c551e3b3`
- `sieving/runs/RUN-20261003-05/metrics.json`: `183652ebb4357d58b33e6f075f1365b38d3509c96f062fe2bab34e286ac21721`
- `sieving/runs/RUN-20261003-14/metrics.json`: `26bee574374154a80d146a360beec40504e6f7ed117166b99c03dc1047d95d78`
- `sieving/runs/RUN-20261003-23/metrics.json`: `ff7c163e49230b49fd0a8a50cc73c1bf2ae8d7cf8003cd9bef3bce279e7a9fee`

## Live-run scope update (2026-10-05)

The aggregate validator now invokes `validate_traceability.py --active-only`.
This is an explicit scope rule for the live audit: only the active generation
for each document is checked. The validator's default remains strict
full-history mode, so rejected and superseded generations are still preserved
for historical repair.

The active-only check now has two unresolved quote records:

- `QUOTE-DOC-0030-0002-01` (`Uvjeti` versus source `Uvjete`)
- `QUOTE-DOC-0011-0011-01` (`imaju` versus source `imati`)

No fuzzy or similarity link was invented. The aggregate remains red until these
two active records receive corrected candidate evidence or an explicitly
approved exception.

## Gate decision

MIN-2.2 remains open. Requirement coverage is green, the harness passes, and
the Part 21 corrected generation is promoted. The remaining gate is unresolved
historical traceability differences. No audit score, finding, or conclusion is
produced while the aggregate gate is red.
