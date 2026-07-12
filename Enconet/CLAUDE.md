# Enconet Claude Code Guidance

This file extends `../CLAUDE.md` and applies within Enconet.

## Read first

1. `MASTER_DEVELOPMENT_PLAN.md` (v1.4 canonical)
2. `docs/ALIGNMENT_PLAN.md` (canonical — waves G0–G5, acceptance criteria)
3. `decisions/README.md` (ADR register, all preparation decisions ADR-0001…0013)
4. `docs/CX_CC_RECONCILIATION.md` (the CX/CC merge agreement)

Treat `docs/context/` and `docs/_archive/` (superseded plan variants, critiques, session
exports) as historical/source input, not a current implementation contract.

## Current implementation and guardrails

- Working code is under `sieving/src/json_extractor`; tests are under `sieving/tests`.
- Do not run `sieving/tools/fix_files.py` or `fix_structure.py`; their root assumptions are unsafe.
- Do not export after a filter or validation error unless an explicit development override is
  approved and recorded. Fail-closed behavior is implemented (C4.1/C4.2): filter errors block
  export unconditionally; ERROR-severity validation blocks export unless an override reason is
  recorded. Do not weaken these gates.
- The standalone Streamlit GUI was retired by human decision on 2026-07-04. Remove stale GUI
  instructions; do not reintroduce it without a superseding ADR.
- Resolve active paths from project/package roots or explicit configuration, never legacy paths.

## Verification

From `Enconet/sieving`, after dependencies are installed:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -q -p no:cacheprovider
$env:PYTHONUTF8='1'
python verify_install.py
```

Use the `/handoff` skill (user-global, `~/.claude/skills/handoff/`; ADR-0014) to close,
pause, or transfer a session. Use `../scripts/make_handoff.py` to render, validate, and
atomically publish the handoff record and pointer (C3); the skill remains the
evidence-collection and status contract. Record dependency, encoding, Git, test, and
index failures explicitly.

