---
description: Show the authoritative audit and validation status without changing state.
---

# /audit-status — session/status

**Purpose:** Show the authoritative audit and validation status without changing state.
**Script(s):** `scripts/audit_command.py`, `scripts/audit_state.py`
**Preconditions (exact allowed phases):** setup, registered, chunked, sieved, evidence_reviewed, evaluated, findings_drafted, findings_approved, report_ready, dashboard_ready, closed, failed
**Outputs:** project phase; gate states; open action count; last validation result

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-status
```

No arguments are required. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
