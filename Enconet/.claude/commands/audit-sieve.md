---
description: Start the first authority-aware sieve generation for a chunked source.
---

# /audit-sieve — initial sieving

**Purpose:** Start the first authority-aware sieve generation for a chunked source.
**Script(s):** `scripts/sieve_run.py`
**Preconditions (exact allowed phases):** chunked
**Outputs:** sieve_runs row; guarded sieve-run workspace

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-sieve -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
