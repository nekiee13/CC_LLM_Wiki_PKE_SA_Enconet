---
description: Generate and validate the controlled offline dashboard.
---

# /audit-dashboard — dashboard

**Purpose:** Generate and validate the controlled offline dashboard.
**Script(s):** `scripts/generate_dashboard.py`
**Preconditions (exact allowed phases):** report_ready
**Outputs:** offline dashboard; wiki dashboard copy

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-dashboard -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
