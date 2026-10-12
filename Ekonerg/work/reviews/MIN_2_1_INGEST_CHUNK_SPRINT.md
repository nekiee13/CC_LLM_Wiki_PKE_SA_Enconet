# MIN-2.1 — Ekonerg intake, extraction, and chunk verification

**Status:** Codex implementation complete; Claude review pending

## Scope

This sprint covered one batch only: verify the approved 31-file Ekonerg source
set, its local registered copies, extracted text, and chunks. It did not create
new document slices and did not change source files.

## Validation commands

```text
python scripts/validate_raw_sources.py --db db/nqa_audit.sqlite
exit code: 0

python scripts/validate_chunks.py --db db/nqa_audit.sqlite --no-record
exit code: 0
```

Both checks passed.

## Intake evidence

| Check | Result |
|---|---:|
| Files in `incoming/` | 31 |
| Manifest rows | 31 |
| Registered database documents | 31 |
| Local raw copies | 31 |
| Validated document chunks | 411 |
| Incoming → manifest hashes | exact match |
| Manifest → database hashes | exact match |
| Raw copies → manifest hashes | exact match |
| Missing registered files | 0 |
| Extra registered files | 0 |

The validation path uses the approved manifest and local project database. No
file outside the approved source set was added as owner evidence. Incoming files
remain the owner-controlled source drop.

## Boundary

This closes MIN-2.1. The next planned task is MIN-2.2: sieve, validate, and
import the real Ekonerg crumbs as one bounded batch. Applicability and scoring
remain separate gates.

