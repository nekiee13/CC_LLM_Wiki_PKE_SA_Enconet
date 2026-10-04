# G3 run-metadata reconciliation

**Status:** Applied under owner approval on 2026-10-04
**Approval reference:** `G3-METADATA-RECONCILE-20261004-OWNER`
**Target:** `RUN-20261003-32`  
**Original value:** `0.1-placeholder`
**Approved model:** `1.0-ekonerg-20261004`

## What and why

The G3 scoring model was approved, but this existing evaluation run still has
the old placeholder model name. The controlled tool changes only that one
metadata field. It does not write evaluations, scores, findings, or crumbs.

## Safety controls

- The run ID is fixed to `RUN-20261003-32`.
- The old value must be exactly `0.1-placeholder`.
- The new value must be exactly `1.0-ekonerg-20261004`.
- Default mode is read-only dry run.
- Apply mode requires a separate owner-approved decision reference.
- The update must affect exactly one row.
- Before and after canonical row hashes are recorded.

## Verification

Focused tests:

```text
python -m pytest Ekonerg/scripts/tests/test_reconcile_run_metadata.py -q
exit 0
3 passed in 0.33s
```

Real-database dry run:

```text
python Ekonerg/scripts/reconcile_run_metadata.py --db db/nqa_audit.sqlite \
  --evidence docs/reviews/MIN_3_1_G3_RUN_METADATA_DRY_RUN.json
exit 0
```

Evidence: `MIN_3_1_G3_RUN_METADATA_DRY_RUN.json`

- Before hash: `f9a88532058dff322ae3911879c8255893c2160f441bf8c0ea8ffdb777e75010`
- After hash: `f9a88532058dff322ae3911879c8255893c2160f441bf8c0ea8ffdb777e75010`
- Changed: `false`

The dry run confirms that no live row changed.

## Owner apply decision

```text
Decision:        [x] APPROVE APPLY   [ ] REJECT   [ ] DEFER

Owner:           Owner
Decision date:   2026-10-04
Decision ref:    G3-METADATA-RECONCILE-20261004-OWNER

Comments:
Change only the scoring-model version for RUN-20261003-32.
```

The apply command was run from the `Ekonerg` project root. It used the
recorded decision reference and wrote the immutable JSON evidence record:

```text
python scripts/reconcile_run_metadata.py --run-id RUN-20261003-32 --old-version 0.1-placeholder --new-version 1.0-ekonerg-20261004 --decision-ref G3-METADATA-RECONCILE-20261004-OWNER --evidence docs/reviews/MIN_3_1_G3_RUN_METADATA_APPLY.json --apply
```

No hand edit was permitted. The apply record is
`MIN_3_1_G3_RUN_METADATA_APPLY.json`.

## Recorded result

The owner approved the apply under the reference above. The controlled tool
updated exactly one field on `RUN-20261003-32`; no evaluation, score, finding,
crumb, or source row was written. The recorded before hash is
`f9a88532058dff322ae3911879c8255893c2160f441bf8c0ea8ffdb777e75010`; the
recorded after hash is
`385a7ff1bf9a7209a9a8374e3d674b87ccd681c7e954dbc044cc74ce54870f26`.
