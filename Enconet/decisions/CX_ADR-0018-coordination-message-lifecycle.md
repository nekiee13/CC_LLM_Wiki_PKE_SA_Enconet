# ADR-0018 - Coordination message lifecycle: active, resolved, archived

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Workspace coordination protocol (both agents) |
| Register | Extends ADR-0017; no frozen-plan amendment |
| Authored by | Codex (`CX_` prefix) |

## Context

ADR-0017 defines immutable inter-agent messages but does not define when resolved
communication leaves the active directory. Keeping solved conversations beside open
questions and blockers makes session startup noisy and can cause agents to repeat closed
work. Deleting or rewriting messages would destroy evidence.

The owner requires solved and mutually confirmed messages to be recorded as solved and
moved to a coordination archive, leaving only active communication in
`coordination/messages/`.

## Decision

The following lifecycle is part of the inter-agent coordination protocol:

1. `coordination/messages/` is the **active queue**. A message remains active while it
   requires an answer, acknowledgement, decision, review, action, or blocker resolution.
2. A message is **resolved** only when its requested outcome is explicit and supported by
   a reply, referenced artifact/validation, or direct owner decision.
3. A message is **confirmed** when the addressed agent acknowledges the resolution or the
   owner declares it closed. Silence is not confirmation.
4. Before archival, the responsible agent creates an immutable, author-prefixed resolution
   manifest in `coordination/archive/`. The manifest identifies each message, its outcome,
   and confirmation evidence.
5. Each agent moves only its own prefixed records (`CX_` by Codex, `CC_` by Claude Code).
   Moving the other agent's record is prohibited by ADR-0016.
6. Archived messages retain their original filename and content. They are never rewritten
   or deleted. After Git recovery, archival uses a history-preserving move.
7. A blocker cannot be archived merely because it was acknowledged. Its underlying
   condition must be resolved or explicitly accepted/deferred by the owner.
8. Closure and acknowledgement messages may be archived after all referenced requests are
   closed and both agents have recorded acceptance where required.
9. Cross-references must resolve to the active or archive location. Archive manifests are
   immutable evidence and remain in `coordination/archive/`.
10. Pre-C0.1 archive moves are allowed only by explicit owner instruction and are recorded
    as bootstrap operations because Git history is unavailable.

## Validation Contract

When C2.4 implements `agent_coord.py`, its validation/status behavior must:

- list active messages separately from archived records;
- reject an archived message without a resolution manifest and confirmation evidence;
- reject deletion, content mutation, duplicate message IDs, or filename changes during
  archival;
- flag resolved-and-confirmed messages left in the active queue;
- flag unresolved messages placed in the archive;
- require blocker disposition (`resolved`, `owner-accepted`, or `deferred-until`) before
  archival;
- preserve per-agent ownership during archive operations.

## Consequences

- Session startup reads only `coordination/messages/` for active communication; archives
  are consulted for history or evidence.
- Resolution logging uses immutable per-operation manifests instead of one shared mutable
  log, avoiding concurrent append conflicts and preserving agent authorship.
- Both agents update only their own guidance to reference ADR-0018. The future neutral
  `TEAM_PROTOCOL.md` must incorporate this lifecycle when C2.4 executes.
- ADR-0017 and the frozen plans remain unchanged.
