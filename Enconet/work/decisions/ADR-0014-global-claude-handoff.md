# ADR-0014 — Claude Code `/handoff` skill is installed user-globally

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | User environment (all Claude Code projects) + workspace |
| Register | post-preparation decision; amends master plan Task 0.7 (amendment A5) |

## Context

The Claude Code handoff skill lived at `03_PKE_SA_NQA1/.claude/skills/handoff/SKILL.md`
as a thin pointer to the Codex contract. Claude Code discovers project skills from the
session's working directory, so the skill was invisible to sessions started elsewhere —
and the owner wants `/handoff` usable in **all** Claude projects (Travel Guide,
02_PKE_Procedure_revision, future work), not only this workspace.

## Decision

The Claude Code skill moves to the user-global location
`C:\Users\PC\.claude\skills\handoff\SKILL.md`. The workspace copy is removed. The global
version is self-contained (no relative pointer) but implements the **same record
contract** as the workspace Codex skill (`.agents/skills/handoff/SKILL.md`), with
`source_agent: claude-code`.

## Consequences

- `/handoff` is available in every Claude Code session regardless of starting directory.
- The Codex counterpart stays at workspace level (Codex discovery convention unchanged).
- Contract changes must update **both** files (global Claude + workspace Codex); the
  planned drift validator (ALIGNMENT_PLAN C2.1) must include the user-global path.
- Other projects using the skill get degraded-but-honest records (`nogit`, `partial`,
  `log_update: not-configured`) wherever the record infrastructure doesn't exist.
- No project may define its own conflicting `handoff` skill; a project-level override
  requires a superseding ADR.
