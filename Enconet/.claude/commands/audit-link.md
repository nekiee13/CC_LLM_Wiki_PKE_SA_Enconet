---
description: Link imported crumb quotes to containing source chunks.
---

# /audit-link — traceability

**Purpose:** Link imported crumb quotes to containing source chunks.
**Script(s):** `scripts/link_crumbs.py`
**Preconditions (exact allowed phases):** sieved
**Outputs:** crumb quote to chunk links

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-link -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
