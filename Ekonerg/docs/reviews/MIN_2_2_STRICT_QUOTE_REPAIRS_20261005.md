# MIN-2.2 strict quote repairs — 2026-10-05

## Result

Three repair candidates were rebuilt from the registered Ekonerg raw sources.
All three pass strict JSON validation and have zero non-exact source quotes.

| Document | Problem | Repair |
|---|---|---|
| DOC-0011 | The stored chapter list was flattened and duplicated list numbers. | Replaced it with the exact source chapter block from `PQ07.5-2_r8_Postupci_sustava_kvalitete,_sustava_za.md`. |
| DOC-0016 | The quote said `provjera`, while the source says `provjere`. | Replaced the quote with the exact source sentence and retained the chapter locator. |
| DOC-0021 | The quote was not tied to the correct clause. | Replaced it with the complete source line and locator for clause `3.3.5.`. |

## Validation

- `validate_app_b_json.py --strict`: 3/3 passed.
- Independent raw-source substring check: DOC-0011 `0` non-exact, DOC-0016 `0`, DOC-0021 `0`.
- Candidate files: [`sieving/candidates/repairs-20261005`](../../sieving/candidates/repairs-20261005/).

The database was not changed and no candidate was promoted. Promotion remains a
separate controlled decision after review and golden-score checks.
