# Skills — inventory and placement rules

- **Scope:** inventory of agent skills relevant to this workspace and the placement
  rules for adding new ones. Placement authority: workspace `CLAUDE.md`/`AGENTS.md`
  and ADR-0014; the duplicate-ownership structure test is planned (Task C2.3).
- **Owner:** shared inventory; each agent maintains only its own skill files
  (ADR-0016 — Claude Code never edits `.agents/` trees, Codex never edits `.claude/`).
- **Update trigger:** a skill is added, moved, retired, or its pair contract changes.

## Placement rules

| Skill scope | Claude Code location | Codex location |
|---|---|---|
| Cross-project (user-global) | `~/.claude/skills/<skill>/SKILL.md` | `~/.agents/skills/<skill>/SKILL.md` |
| Workspace-shared | `03_PKE_SA_NQA1/.claude/skills/` | `03_PKE_SA_NQA1/.agents/skills/` |
| Project-only (e.g. Enconet) | `<project>/.claude/skills/` | `<project>/.agents/skills/` |

Paired skills (same contract on both sides) are drift-checked via
`doc/GUIDANCE_PAIRS.json` + `scripts/check_guidance_drift.py`; changes must update
both sides (each agent edits its own).

## Inventory (verified 2026-07-11)

| Skill | Sides | Location(s) | Status |
|---|---|---|---|
| `/handoff` | both (paired, ADR-0014) | `~/.claude/skills/handoff/SKILL.md`; `~/.agents/skills/handoff/SKILL.md` | Installed user-globally on both sides; contract drift-checked (pair `handoff-skill` in `GUIDANCE_PAIRS.json`) |

No workspace-shared or project-level skills exist yet on either side. The planned
sieving skill set (master plan Task 18.7) and the duplicate-name structure test
(Task C2.3) are not implemented — planned files are not evidence of implemented
capability.
