# ADR-0005 — Both Claude Code and Codex are maintained, with drift validation

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Workspace |
| Register | D-5 |

## Context

Two agents work this project: Claude Code (discovers `CLAUDE.md`, `.claude/skills/`) and
Codex (discovers `AGENTS.md`, `.agents/skills/`). The alternative was standardizing on one
agent for simpler governance.

## Decision

Maintain **both** agent surfaces permanently. Owner's rationale, recorded verbatim in
substance:

1. This is an extremely important project to the owner; two heads are better than one.
   The owner's capacity for explaining and specifying is limited — all available help is
   wanted, and cross-review between agents has already caught real errors in both
   directions (see `docs/CX_CC_RECONCILIATION.md`).
2. Session limits are harsh; running both agents keeps progress moving as fast as
   possible. The `/handoff` skill was anticipated precisely to make agent-to-agent and
   session-to-session transfer safe.

## Consequences

- `CLAUDE.md`/`AGENTS.md` pairs and skill pairs must stay semantically aligned; a drift
  validator compares them and flags divergence (tool-specific differences are documented,
  not silently tolerated).
- Shared skills carry **one** record contract; per-agent files may only adapt discovery
  and set `source_agent` (pattern already in place for `/handoff`).
- Every session (either agent) ends with `/handoff`; the next session (either agent)
  starts from `HANDOFF.md` and verifies it against reality.
