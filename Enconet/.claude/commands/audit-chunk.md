---
description: Split one registered document into reviewable chunks.
---

# /audit-chunk — chunking

**Purpose:** Split one registered document into reviewable chunks.
**Script(s):** `scripts/chunk_document.py`
**Preconditions (exact allowed phases):** registered
**Outputs:** document_chunks rows; derived/chunks artifact

Run from `Enconet/` exactly:

```bash
python scripts/audit_command.py audit-chunk -- $ARGUMENTS
```

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.
