---
description: Record one human criterion judgment through the evidence gate.
---

# /audit-eval — evaluation

**Purpose:** Record one human criterion judgment through the evidence gate.
**Script(s):** `scripts/write_evaluation.py`
**Preconditions (exact allowed phases):** evidence_reviewed
**Outputs:** criterion evaluation and evidence links

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-eval -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
