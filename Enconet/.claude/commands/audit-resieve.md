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

Arguments after `--` pass through unchanged to the wrapped stage script. The canonical
dispatcher `scripts/audit_command.py` reads
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; this adapter must never bypass, duplicate, or weaken that check, and no
command advances a human gate on its own.

The new generation is created as an **inactive candidate**: it never modifies or
deletes prior crumbs, the previous generation stays active, and the run automatically
produces a per-RUN metrics report and a diff against the previous active generation.
The command **stops before promotion** — promotion, rejection, or rollback is a
separate recorded human decision through `scripts/sieve_generation.py` (read the
`sieving-tuning` skill and `sieving/SIEVING_PLAYBOOK.md` first).
