# ADR-0016 — Dual-agent infrastructure ownership ban

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Workspace + user environment (both agents) |
| Register | Refines ADR-0005 (dual-agent policy) and the "both files" consequence of ADR-0014/0015 |
| Authored by | Claude Code (CC_ prefix per agent-authorship convention) |

## Context

Both agents work the same tree (ADR-0005). Without an ownership boundary, either agent can
edit, move, or re-index the other's discovery files and skills, producing silent conflicts
that the drift validator cannot attribute.

## Decision

Each agent is **banned from touching the other's infrastructure** (create / edit / delete /
move / re-index):

| Owner | Infrastructure |
|---|---|
| Codex only | `AGENTS.md` files, `.agents/` trees, `~/.agents/`, `CX_`-prefixed records, Codex-owned indexes: `Codex_global_guidance`, `PKE_SA_NQA1_codex_guidance`, `PKE_SA_NQA1_agent_guidance` (stale — Codex retires it) |
| Claude Code only | `CLAUDE.md` files, `.claude/` trees, `~/.claude/`, `CC_`-prefixed records, Claude-owned indexes: `PKE_SA_NQA1_Enconet_docs`, `PKE_SA_NQA1_Enconet_controlled`, `Enconet-0a063bd7` |

Shared project records (canonical plans, `decisions/`, `handoffs/`, wiki, manifests,
code) remain writable by both agents under the existing rules; agent-authored ADR files
carry the author prefix (`CC_`/`CX_`) while keeping sequential ADR numbers.

## Consequences

- The ADR-0014/0015 rule "contract changes must update both skill files" becomes: each
  agent updates **its own** file; the drift validator (ALIGNMENT_PLAN C2.1) verifies the
  two stay semantically equivalent and must cover both user-global paths.
- Cross-agent change requests travel via the human or a handoff note, never direct edits.
- Guidance edits: Claude states the ban in `CLAUDE.md`, Codex states it in `AGENTS.md`;
  neither edits the other's statement.
- Index refreshes: each agent refreshes only its own profiles; profile ownership is
  documented in `doc/INDEXING.md` when C6.2 lands.
