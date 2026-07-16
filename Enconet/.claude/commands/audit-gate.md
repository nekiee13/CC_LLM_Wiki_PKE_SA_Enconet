---
description: Assemble the gate packet for the current phase and stop for the human.
---

# /audit-gate — human gate

**Purpose:** Assemble the gate packet for the current phase and stop for the human.
**Script(s):** `scripts/gate_packet.py`
**Preconditions (exact allowed phases):** setup, sieved, evidence_reviewed, findings_drafted, findings_approved, report_ready, dashboard_ready
**Outputs:** one immutable human gate packet; no automatic transition

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-gate -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
