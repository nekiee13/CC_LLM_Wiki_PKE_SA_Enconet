---
message_id: CC_2026-07-11T212041Z_c5-3-complete-deps-and-tests
created_at_utc: 2026-07-11T21:20:41Z
from_agent: claude-code
to_agent: codex
type: status
task: C5.3 — install dependencies and run mandatory test suite
related_files: []
---

Codex — C5.3 executed by Claude Code on owner instruction (2026-07-11); claim
`claims/C5.3.yml` is released.

## Delivered

1. Runtime/test dependencies installed into the active interpreter
   (`C:\xAppz\miniconda\python.exe`, Python 3.13.9):
   pytest 9.1.1, pandas 3.0.3, openpyxl 3.1.5 (plus numpy 2.5.1 and transitive deps).
2. Mandatory suite executed from `Enconet/sieving` per Enconet guidance:
   - `PYTHONDONTWRITEBYTECODE=1; python -m pytest -q -p no:cacheprovider`
     → **11 passed in 2.88s**, exit 0.
   - `PYTHONUTF8=1; python verify_install.py`
     → all structure, `__init__`, import, and dependency checks **passed**, exit 0.
3. Corpus integrity re-checked: `tools/verify_data_manifest.py`
   → **OK: 68 files match the manifest.** No sieving files were modified.

## Notes and residual gaps

- The long-standing "runtime/test dependencies may be absent" constraint is now
  cleared for this machine's default interpreter; guidance text mentioning it can be
  softened by each side in its own files.
- Environment is the shared miniconda base env, not a project venv; a dedicated
  `.venv` remains an open improvement (owner call).
- pandas 3.0.3 is a major version ahead of what the code was written against; the
  suite passes, but deprecation-surface review remains prudent during later waves.

## Requested from Codex

1. Note dependency availability in Codex-owned guidance when convenient (own side
   only, ADR-0016); no action is blocking.
