# CX_ADR-0015 — Codex `/handoff` skill is installed user-globally

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Codex user environment (all Codex projects) + workspace |
| Register | post-preparation decision; amends master plan Task 0.7 (amendment A6) |

## Context

The Codex handoff skill was stored at
`03_PKE_SA_NQA1/.agents/skills/handoff/SKILL.md`. That repository-local location limited
discovery to this workspace, while the owner requires the same `/handoff` workflow in all
Codex projects.

## Decision

Move the complete Codex skill to the user-global location
`C:\Users\PC\.agents\skills\handoff\SKILL.md`. Remove the workspace copy. Keep
workspace and project `.agents/skills/` directories available for skills whose ownership is
limited to those scopes.

This decision changes Codex infrastructure only. Codex must not modify `CLAUDE.md`,
`.claude/`, or user-global Claude Code infrastructure. Any Claude-side synchronization is
owned and performed by Claude Code.

## Consequences

- `/handoff` is discoverable in Codex projects regardless of their repository root.
- The global skill is user-environment state and is not versioned by this repository; its
  installation and validation state must be recorded in project handoffs when relevant.
- Project guidance and controlled plans reference `~/.agents/skills/handoff/`, while archived
  plans and immutable handoffs retain historical paths.
- A new Codex session may be required for skill discovery after installation.
- Cross-agent contract checks must report Claude synchronization as pending until Claude Code
  verifies its own infrastructure; Codex must not perform that synchronization.
