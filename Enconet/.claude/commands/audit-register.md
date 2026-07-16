---
description: Promote one reviewed incoming source through the controlled registry doorway.
---

# /audit-register — source registration

**Purpose:** Promote one reviewed incoming source through the controlled registry doorway.
**Script(s):** `scripts/promote_source.py`
**Preconditions (exact allowed phases):** setup
**Outputs:** raw source; manifests/raw_sources.csv row; documents row

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-register -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
