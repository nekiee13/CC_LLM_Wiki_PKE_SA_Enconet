# Enconet Codex Guidance

## Scope

These instructions apply within `03_PKE_SA_NQA1/Enconet` and extend `../AGENTS.md`.

## Read first

1. `MASTER_DEVELOPMENT_PLAN.md` (v1.4 canonical) for the target plan.
2. `docs/ALIGNMENT_PLAN.md` (canonical) for waves G0–G5, migration order, and acceptance criteria.
3. `decisions/README.md` for the ADR register (current through ADR-0017).
4. `docs/CX_CC_RECONCILIATION.md` for the agreement that merged the CX/CC preparation.
5. `Sieving_method_specification_Guide.md` v1.3 for the current subsystem, checking claims
   against actual code and tests; C4.4 implemented the single-owner contract.

`docs/context/` and `docs/_archive/` contain source material, examples, superseded plan
variants, and historical session exports. They are history, not a current implementation
contract.

## Current implementation

- Working code is under `sieving/src/json_extractor` with CLI, query, flattening, and export adapters.
- Tests are under `sieving/tests`.
- Example RULE and DOCUMENT JSON data is under `sieving/DATA`.
- The upstream Streamlit GUI (`app.py`, `adapters/streamlit_app/`) was retired when the
  subsystem was vendored, by owner decision dated 2026-07-04. Do not advertise or restore it
  without a new owner decision; use the headless pipeline and generated review outputs.
- Database, complete wiki, report/dashboard generation, audit state machine, and aggregate validators
  remain planned unless executable evidence proves otherwise.

## Guardrails

- `MASTER_DEVELOPMENT_PLAN.md` and `docs/ALIGNMENT_PLAN.md` are frozen. Do not edit either
  unless the project owner explicitly reopens planning.
- Do not run `sieving/tools/fix_files.py` or `sieving/tools/fix_structure.py`; their current root
  assumptions are unsafe after relocation.
- Filtering fails closed and export is blocked after a filter error. Preserve that contract; the
  development-only unfiltered preview override must remain explicit, preview-only, and recorded.
- Resolve active paths from project/package roots or explicit configuration, never legacy absolute paths.
- Keep Appendix B taxonomy/schema changes synchronized across machine-readable contracts, prompts,
  runtime validation, query fields, and fixtures until one canonical owner is implemented.

## Verification

From `Enconet/sieving`, after installing the declared dependencies:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -q -p no:cacheprovider
$env:PYTHONUTF8='1'
python verify_install.py
```

Record dependency or encoding failures as failures, not as successful verification.

## Skills and session continuity

- User-global Codex skills: `$HOME/.agents/skills/`; `/handoff` is installed there.
- Workspace-shared Codex skills: `../.agents/skills/`.
- Enconet-only Codex skills: `.agents/skills/`.
- Use the user-global `handoff` skill when asked to close, pause, transfer, or summarize a working session.
- Use `../scripts/make_handoff.py` to render, validate, and atomically publish the handoff record
  and pointer; the skill remains the evidence-collection and status contract.
- Do not claim that `/handoff` is fully integrated with project state until the related master-plan
  acceptance criteria and validators are implemented.

## Team coordination

- Follow ADR-0016/0017/0018. Claude Code owns all Claude infrastructure and Claude-owned indexes;
  Codex may read but must not modify or re-index them.
- Session order: `HANDOFF.md`, then `coordination/BOARD.md`, unread messages addressed to
  Codex, and active claims when those records exist.
- Reply to Claude through a new immutable `coordination/messages/CX_*.md` record with
  `reply_to`; never edit a `CC_` message.
- When the owner asks to "check messages", treat actionable review requests as authorization to
  inspect, independently validate, and respond in the same turn. Only stop at reporting when the
  owner explicitly requests read-only inspection or evidence is insufficient for acknowledgement.
- After processing messages, archive every resolved and confirmed Codex-owned `CX_` record with
  an immutable ADR-0018 resolution manifest; leave Claude-owned `CC_` archival to Claude Code.
- Resolved and confirmed `CX_` messages belong in `coordination/archive/` with an immutable
  resolution manifest. Active `coordination/messages/` contains unresolved items only.
- Default to one active writer in the shared tree. Parallel work requires separate Git
  worktrees and non-overlapping claims after C0.1/C2.4 establishes those controls.
