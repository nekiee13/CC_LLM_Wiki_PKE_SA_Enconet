# ADR-0017 — Inter-agent coordination protocol (repository as the channel)

| Field | Value |
|---|---|
| Status | Accepted (implementation deferred until after Task C0.1 restores Git) |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Workspace (both agents) |
| Register | Extends ADR-0005 (dual-agent) and ADR-0016 (infrastructure ban) |
| Authored by | Claude Code |

## Context

ADR-0016 separates agent infrastructure but provided no channel for cross-agent requests.
Agents cannot communicate in real time; without a versioned protocol they act as
competitors on shared files. Owner's directive: separate agent infrastructure, **shared
project coordination** — the repository is the communication channel; the agents work as
a team.

## Decision

Adopt the coordination structure under `Enconet/coordination/`:

```text
coordination/
├── TEAM_PROTOCOL.md      ← agent-neutral shared authority (protocol text)
├── BOARD.md              ← generated current summary; never authoritative history
├── messages/             ← immutable, author-prefixed: CX_/CC_<timestamp>_<topic>.md
└── claims/<task-id>.yml  ← who owns a task + anticipated files + expiry
```

**Ownership rules:** Codex owns `AGENTS.md`, `.agents/`, `~/.codex/`, `~/.agents/`;
Claude owns `CLAUDE.md`, `.claude/`, `~/.claude/`. Neither modifies the other's
infrastructure (this adds `~/.codex/` to the ADR-0016 listing). Both agents may modify
neutral `coordination/` records under the shared protocol. Semantic requirements live in
neutral contracts, not duplicated independently inside agent files. Each agent records
the other's synchronization as *pending* until that agent confirms its own side.

**Prefix exception (narrow):** `TEAM_PROTOCOL.md` and `BOARD.md` are agent-neutral shared
authorities — exempt from the CC_/CX_ authorship-prefix rule. Immutable messages keep
author prefixes.

**Message schema (immutable; acknowledgement = new message with `reply_to`):**

```yaml
message_id:
created_at_utc:
from_agent: codex|claude-code
to_agent: codex|claude-code|both
type: note|review_request|blocker|question|acknowledgement
task:
related_files: []
reply_to:
```

**Working rules (1–10):** session start reads HANDOFF.md → BOARD.md → unread messages →
active claims; claim before editing; claims list anticipated files and expire; no edits
under another agent's active claim; substantial work ends with handoff or message;
one agent's implementation is normally reviewed by the other; "both agents synchronized"
only after each confirms its own side; conflicting recommendations recorded with evidence
and resolved by the human or an ADR; default one active writer per shared tree; parallel
work requires separate Git worktrees + non-overlapping claims.

**Validation (future `agent_coord.py`):** `status | claim | release | message |
acknowledge | validate`; rejects malformed messages, duplicate IDs, overlapping active
claims, unacknowledged blockers, stale BOARD.md, unsupported synchronization claims.

## Consequences

- New alignment-plan task (C2.4) carries implementation; **no `coordination/` files are
  created before Task C0.1 restores the Git boundary** — the protocol's value depends on
  versioned history.
- Record-purpose separation is binding: HANDOFF = session snapshot; messages = targeted
  notes/requests/blockers; claims = task ownership; BOARD = generated summary;
  ADRs = durable decisions, not conversation.
- Both agents' guidance states the ban on its own side only (Claude: workspace + global
  `~/.claude/CLAUDE.md`; Codex: its own files). The drift validator (C2.1) verifies the
  two protocol statements stay semantically equivalent.
- First coordinated task remains Git recovery (C0.1).
