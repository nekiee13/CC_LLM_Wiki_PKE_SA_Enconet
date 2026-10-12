# MIN-2.2 — Real-document sieving sprint blocker

**Status:** blocked; task not closed

## Scope

This was one aggregate validation task for the real Ekonerg RULE and DOCUMENT
sieving runs. No new per-document slice was opened after the gate failed.

## Checks run

```text
python scripts/run_all_validations.py --db db/nqa_audit.sqlite --no-record
exit code: 1

python scripts/validate_traceability.py --db db/nqa_audit.sqlite --no-record
exit code: 1

python scripts/validate_sieving_harness.py --db db/nqa_audit.sqlite --allow-pending-claude
exit code: 1
```

The source and chunk checks inside the aggregate run still passed:

- `validate_raw_sources.py`: exit 0;
- `validate_chunks.py --no-record`: exit 0.

## Stop-gate findings

1. Active runs contain 28 quote records without a chunk link: 15 on the active
   DOCUMENT side and 13 on the active RULE side. The active runs therefore do
   not yet satisfy full quote traceability.
2. The requirements validator reports criterion `APP_B_XVIII` without a
   requirement row.
3. The sieving harness reports the Claude-owned `sieving-tuning` skill missing.
   Claude is currently unavailable, so Codex does not modify Claude-owned
   infrastructure.
4. The golden calibration note remains pending human review. Candidate context
   runs are inactive and do not change the active audit evidence.

## Disposition

MIN-2.2 remains open. The correct next action is to resolve these three recorded
gate issues, then rerun the same aggregate validation. No audit score, finding,
or conclusion is produced while this gate is red.

