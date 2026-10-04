# MIN-1.1 — Minimum local runtime sprint

**Status:** Codex implementation complete; Claude review pending

## Scope

This sprint covered one task only: prove fresh local database creation and
repeatable Appendix B criterion seeding in disposable synthetic projects. It did
not process another Ekonerg document and did not change the real audit database.

## TDD result

The first synthetic run exposed a test-fixture defect. The bootstrap test copied
`init_db.py` but omitted its required local `db_util.py`, so the copied runtime
could not start. The smallest fix was to include `db_util.py` in the copied
bootstrap files. No production source or audit data was changed.

Changed file:

`scripts/tests/test_db_bootstrap.py`

## Acceptance evidence

The corrected synthetic checks ran in disposable projects and exited `0`.
They covered:

- company name with spaces: `Audit Beta with spaces`;
- company name with a Croatian character: `Ekonerg ogled Čakovec`;
- runs with and without a fake `Enconet` sibling;
- fresh database integrity and required tables;
- exactly 18 Appendix B criteria;
- repeat seed preserving the first database byte-for-byte;
- refusal of changed taxonomy;
- refusal of foreign database paths and unsafe reset attempts;
- neutral ID patterns without inherited company names;
- unchanged fake-sibling marker bytes and timestamps.

Recorded command outcome:

```text
MIN-1.1 manual synthetic checks: PASS
manual_exit_code=0
```

The normal pytest invocation was also attempted, but its `tmp_path` cleanup was
blocked by the machine's protected Windows temporary-directory permissions. That
environment failure is recorded, not reported as a test pass. The direct calls to
the same test functions above completed successfully with exit code 0.

## Boundary

This closes only MIN-1.1. The synthetic end-to-end rehearsal (MIN-1.2) remains a
separate task. No real Ekonerg score, finding, or conclusion was produced.

