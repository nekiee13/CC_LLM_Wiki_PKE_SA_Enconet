# Skills — inventory and placement rules

- **Scope:** inventory of agent skills relevant to this workspace and the placement
  rules for adding new ones. Placement authority: workspace `CLAUDE.md`/`AGENTS.md`
  and ADR-0014; placement is machine-checked by `scripts/check_skill_structure.py`
  (Task C2.3).
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

Structure rules (enforced by `python scripts/check_skill_structure.py`, exit 1 on
violation; tests: `scripts/tests/test_skill_structure.py`, C2.3):

- A skill name must not appear at two nesting scopes of the same agent
  (user-global / workspace / project) — that is conflicting ownership. The same
  name in two *different projects* does not conflict.
- A paired skill (same name on both agents) must live at the **same scope** on
  both sides, as `/handoff` does (user-global, ADR-0014).
- Every skill directory must contain `SKILL.md`.
- The planned sieving skills (master plan Task 18.7) are **Enconet-level**:
  `Enconet/.claude/skills/` and `Enconet/.agents/skills/`, never workspace or
  user-global (ALIGNMENT_PLAN C2.3).

## Inventory (verified 2026-07-11)

| Skill | Sides | Location(s) | Status |
|---|---|---|---|
| `/handoff` | both (paired, ADR-0014) | `~/.claude/skills/handoff/SKILL.md`; `~/.agents/skills/handoff/SKILL.md` | Installed user-globally on both sides; contract drift-checked (pair `handoff-skill` in `GUIDANCE_PAIRS.json`) |

No workspace-shared or project-level skills exist yet on either side
(`check_skill_structure.py --list`, 2026-07-11: 2 locations, 0 errors; workspace
skill dirs exist but are empty on both sides; no project-level skill dirs). The
planned sieving skill set (master plan Task 18.7) is not implemented — planned
files are not evidence of implemented capability.
