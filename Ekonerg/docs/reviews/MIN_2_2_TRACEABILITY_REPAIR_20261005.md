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
3. Added `evidence_matching.py`. It handles Markdown/HTML presentation noise,
   duplicate list markers from extraction, and explicit ellipsis excerpts.
   It does not use a similarity score.
4. Added `seed_requirements.py`. It previews and idempotently seeds distinct
   requirement statements from active RULE crumbs. It does not write scores,
   evaluations, findings, or source documents.

## Checks

```text
python -m pytest Ekonerg/scripts/tests/test_evidence_matching.py Ekonerg/scripts/tests/test_seed_requirements.py -q
exit 0 — 7 passed

python -m pytest Ekonerg/scripts/tests -q
exit 0 — 83 passed

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

The harness failure is the Claude-owned `sieving-tuning` skill check. The
traceability validator still sees 14 unlinked quotes across all generations;
two are in active runs:

- `QUOTE-DOC-0030-0002-01`: source wording differs (`Uvjeti` versus `Uvjete`).
- `QUOTE-DOC-0011-0011-01`: source wording differs (`imaju` versus `imati`).

The remaining 12 unlinked quotes are in inactive candidate, rejected, or
superseded generations. No exception or score was created for any mismatch.

The post-repair generated-state hash is:

- `db/nqa_audit.sqlite`: `c54a479cb5dc0ef725b6521fa78ab39ea6a25eb118d5e7e8a5aead06c551e3b3`
- `sieving/runs/RUN-20261003-05/metrics.json`: `183652ebb4357d58b33e6f075f1365b38d3509c96f062fe2bab34e286ac21721`
- `sieving/runs/RUN-20261003-14/metrics.json`: `26bee574374154a80d146a360beec40504e6f7ed117166b99c03dc1047d95d78`
- `sieving/runs/RUN-20261003-23/metrics.json`: `ff7c163e49230b49fd0a8a50cc73c1bf2ae8d7cf8003cd9bef3bce279e7a9fee`

## Gate decision

MIN-2.2 remains open. Requirement coverage is now green. The remaining
traceability differences need source-review or an owner-approved disposition;
the missing Claude skill needs Claude-side action. No audit score, finding, or
conclusion is produced while the aggregate gate is red.
