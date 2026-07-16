---
description: Validate, then publish an evidence-bearing session handoff without changing phase.
---

# /audit-close — session/closeout

**Purpose:** Validate, then publish an evidence-bearing session handoff without changing phase.
**Script(s):** `scripts/run_all_validations.py`, `../scripts/make_handoff.py`
**Preconditions (exact allowed phases):** setup, registered, chunked, sieved, evidence_reviewed, evaluated, findings_drafted, findings_approved, report_ready, dashboard_ready, closed, failed
**Outputs:** aggregate verdict; immutable handoff record; HANDOFF.md pointer

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-close -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
