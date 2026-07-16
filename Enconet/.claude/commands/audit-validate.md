---
description: Run the phase-aware validation spine.
---

# /audit-validate — validation

**Purpose:** Run the phase-aware validation spine.
**Script(s):** `scripts/run_all_validations.py`
**Preconditions (exact allowed phases):** setup, registered, chunked, sieved, evidence_reviewed, evaluated, findings_drafted, findings_approved, report_ready, dashboard_ready, closed, failed
**Outputs:** aggregate PASS or FAIL; manifests/validation_runs.csv unless --no-record

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-validate -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
