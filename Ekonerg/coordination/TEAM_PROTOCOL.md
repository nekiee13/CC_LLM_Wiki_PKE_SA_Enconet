# TEAM PROTOCOL — inter-agent coordination

Agent-neutral shared authority (ADR-0017, ADR-0018; implemented by Task C2.4).
Binding on Codex and Claude Code. Exempt from the CC_/CX_ authorship-prefix rule,
as is `BOARD.md`. Changes to this file require owner approval or a superseding ADR.

## 1. Channel

The repository is the agents' communication channel:

```text
coordination/
├── TEAM_PROTOCOL.md      ← this file (protocol text; neutral authority)
├── BOARD.md              ← generated summary (scripts/agent_coord.py status --write);
│                            never hand-edited, never authoritative history
├── messages/             ← ACTIVE queue: immutable, author-prefixed
│                            CC_/CX_<UTC-timestamp>_<topic>.md
├── archive/              ← resolved+confirmed messages and immutable resolution
│                            manifests (ADR-0018)
└── claims/<task-id>.yml  ← task ownership records
```

## 2. Working rules (1–10)

1. **Session start reading order:** `HANDOFF.md` → `BOARD.md` → unread
   `coordination/messages/` → active `coordination/claims/`.
2. **Claim before editing.** A claim names the task, the owning agent, the anticipated
   files, and its expiry.
3. **No edits under another agent's active claim.**
4. **Substantial work ends** with a handoff record or a targeted message.
5. **Cross-review is the norm:** one agent's implementation is normally reviewed by the
   other.
6. **"Both agents synchronized"** may be recorded only after each agent confirms its own
   side; until then the other side is *pending*.
7. **Conflicting recommendations** are recorded with evidence and resolved by the human
   or an ADR — never by silent override.
8. **One active writer per shared tree** (default).
9. **Parallel work** requires separate Git worktrees and non-overlapping claims.
10. **Message immutability:** acknowledgement is a new message with `reply_to`; existing
    messages are never rewritten; blockers require acknowledgement.

## 3. Message schema (ADR-0017)

Filename: `<CC|CX>_<YYYY-MM-DDTHHMMSSZ>_<kebab-topic>.md`, frontmatter:

```yaml
message_id:        # equals the filename without .md
created_at_utc:    # ISO-8601
from_agent: codex|claude-code
to_agent: codex|claude-code|both
type: note|review_request|blocker|question|acknowledgement|claim|status
task:
related_files: []
reply_to:          # optional message_id
```

`claim` and `status` extend the original ADR-0017 type list; codified here by C2.4
(claims-in-message form were already in bootstrap use before `claims/` existed).

## 4. Claim schema and expiry

`claims/<task-id>.yml`:

```yaml
task: C0.2
agent: codex|claude-code
status: active|released
claimed_at_utc: ...
last_renewed_at_utc: ...
expires_at_utc: ...        # default: last_renewed_at_utc + 24 h
anticipated_files:
  - path/one
  - path/two
note: optional free text
released_at_utc: ...       # set on release
```

**Expiry default: 24 hours from `last_renewed_at_utc`.** Expiry never implies
completion — an expired claim only stops blocking other agents. The owner may override
any claim at any time.

## 5. Message lifecycle (ADR-0018)

1. `messages/` holds only **active** communication.
2. A message is **resolved** only when its requested outcome is explicit and evidenced.
3. It is **confirmed** when the addressed agent acknowledges resolution or the owner
   declares it closed. **Silence is not confirmation.**
4. Before archival the responsible agent writes an immutable author-prefixed resolution
   manifest in `archive/` identifying each message, its outcome, and confirmation
   evidence.
5. Each agent moves only its own prefixed records.
6. Archived messages keep their original filename and content forever; archival uses a
   history-preserving move (`git mv`).
7. A **blocker** archives only with a disposition: `resolved`, `owner-accepted`, or
   `deferred-until <condition/date>` — acknowledgement alone never closes it.
8. Closure/acknowledgement messages archive after all referenced requests are closed.
9. Cross-references must resolve to `messages/` or `archive/`.

## 6. Tooling

`scripts/agent_coord.py` (workspace root) is the protocol tool:
`status | claim | release | message | acknowledge | validate`. `validate` enforces the
schema, uniqueness, claim-overlap, blocker-acknowledgement, lifecycle, and BOARD
freshness rules; CI/gates treat a non-zero exit as failure. `BOARD.md` is regenerated
with `python scripts/agent_coord.py status --write`.
