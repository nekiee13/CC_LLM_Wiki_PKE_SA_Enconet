---
description: Generate the report from the canonical package and approvals.
---

# /audit-report — report

**Purpose:** Generate the report from the canonical package and approvals.
**Script(s):** `scripts/generate_report.py`
**Preconditions (exact allowed phases):** findings_approved
**Outputs:** controlled evaluation report

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-report -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
