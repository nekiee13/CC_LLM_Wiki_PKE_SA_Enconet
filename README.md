# PKE SA NQA1 — supplier-audit workspace

Workspace root for the NQA-1 supplier-audit projects (ADR-0001). Three project
entries: **Enconet** (active), **Ekonerg** and **TEKOL** (not yet started). Two agents
(Codex, Claude Code) work this repository under a shared coordination protocol.

Created by Task C6.1 (`Enconet/docs/ALIGNMENT_PLAN.md`, wave G5).

## Start here

| Entry point | What it is |
|---|---|
| [`Enconet/HANDOFF.md`](Enconet/HANDOFF.md) | Pointer to the latest immutable session handoff — read first |
| [`Enconet/wiki/index.md`](Enconet/wiki/index.md) | Enconet navigation: status, log, authoritative documents |
| [`Enconet/wiki/current-status.md`](Enconet/wiki/current-status.md) | Current phase and open items |
| [`doc/README.md`](doc/README.md) | Workspace-level engineering documentation index |
| [`Enconet/coordination/TEAM_PROTOCOL.md`](Enconet/coordination/TEAM_PROTOCOL.md) | Dual-agent coordination protocol (ADR-0017/0018) |

## Authoritative project documents (Enconet)

- [`Enconet/MASTER_DEVELOPMENT_PLAN.md`](Enconet/MASTER_DEVELOPMENT_PLAN.md) — canonical master plan (v1.4)
- [`Enconet/docs/ALIGNMENT_PLAN.md`](Enconet/docs/ALIGNMENT_PLAN.md) — alignment plan, waves G0–G5
- [`Enconet/decisions/README.md`](Enconet/decisions/README.md) — ADR register
- [`Enconet/docs/README.md`](Enconet/docs/README.md) — project documentation catalog
- [`Enconet/Sieving_method_specification_Guide.md`](Enconet/Sieving_method_specification_Guide.md) — sieving specification
- [`Enconet/schemas/`](Enconet/schemas/) — single-owner sieving contract (ADR-0003)

## Agent guidance

Tool-specific, semantically aligned pairs (drift-checked by
`scripts/check_guidance_drift.py`): `CLAUDE.md`/`AGENTS.md` at the workspace root and
in `Enconet/`. Each agent reads its own chain; neither edits the other's
infrastructure (ADR-0016).

## Working rules in force

- `Enconet/sieving/DATA/` is never tracked; its checksum manifest is (ADR-0002).
- Validation: `python scripts/run_validation.py` (aggregate layers L0–L5, C5.2).
- Handoffs: `python scripts/make_handoff.py` (C3); session end requires one.
