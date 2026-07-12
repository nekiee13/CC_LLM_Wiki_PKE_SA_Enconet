# Enconet project-local Codex skills

This directory is reserved for Codex-owned skills whose scope is limited to the
Enconet project, per ADR-0016 and `doc/SKILLS.md`.

Each installed skill must use the layout:

```text
.agents/skills/<skill-name>/SKILL.md
```

No project-local skills are installed yet. Cross-project skills such as
`handoff` remain user-global under `$HOME/.agents/skills/` and must not be
duplicated here.

Claude Code must not modify this directory. Its corresponding infrastructure is
owned separately under `.claude/`.
