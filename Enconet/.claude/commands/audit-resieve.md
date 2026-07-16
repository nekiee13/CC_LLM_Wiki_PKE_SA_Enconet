---
description: Start a measured new sieve generation without overwriting its predecessor.
---

# /audit-resieve — iterative sieving

**Purpose:** Start a measured new sieve generation without overwriting its predecessor.
**Script(s):** `scripts/resieve_run.py`
**Preconditions (exact allowed phases):** sieved
**Outputs:** new generation; quality metrics; generation diff

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-resieve -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.

This command is reserved and fails closed until EPIC18 provides its implementation; do not substitute another script.
