# PKE SA NQA1 Claude Code Guidance

## Scope

These instructions apply to every project under `03_PKE_SA_NQA1`. Nested `CLAUDE.md` files may
add project-specific rules but must not weaken evidence, source-integrity, validation, or
recordkeeping requirements.

## Workspace model

- Treat `03_PKE_SA_NQA1` as the workspace root and Enconet, Ekonerg, and TEKOL as project entries.
- Put reusable Claude Code skills in `.claude/skills/<skill>/SKILL.md`.
- Put project-specific Claude Code skills in `<project>/.claude/skills/<skill>/SKILL.md`.
- Exception: `/handoff` is installed user-globally (`~/.claude/skills/handoff/`) so every
  Claude project can use it (ADR-0014). Its contract stays identical to the workspace
  Codex counterpart `.agents/skills/handoff/SKILL.md`; changes must update both.
- Keep Claude Code discovery files separate from Codex `AGENTS.md`/`.agents` files. Equivalent
  rules must stay semantically aligned; tool-specific differences must be documented.
- **Infrastructure ownership ban (ADR-0016/0017):** Claude Code must never create, edit,
  delete, move, or re-index Codex infrastructure — `AGENTS.md` files, `.agents/` trees,
  `~/.codex/`, `~/.agents/`, `CX_`-prefixed records, or Codex-owned indexes
  (`Codex_global_guidance`, `PKE_SA_NQA1_codex_guidance`, `PKE_SA_NQA1_agent_guidance`).
  The reciprocal ban (Codex ↔ Claude infrastructure and Claude-owned indexes
  `PKE_SA_NQA1_Enconet_docs`, `PKE_SA_NQA1_Enconet_controlled`, `Enconet-0a063bd7`) is
  stated in `AGENTS.md`. Each agent applies changes to its own files only.
- **Coordination protocol (ADR-0017, implemented after C0.1):** cross-agent requests
  travel through neutral, versioned `Enconet/coordination/` records — `TEAM_PROTOCOL.md`
  and `BOARD.md` (agent-neutral shared authorities), immutable author-prefixed
  `messages/`, and task `claims/`. Both agents may modify `coordination/` under the
  shared protocol. Claim a task before editing; do not edit files under another agent's
  active claim; record the other agent's synchronization as *pending* until it confirms
  its own side; agents work as a team, not competitors.
- **Message lifecycle (ADR-0018):** `coordination/messages/` holds only active
  communication. A message is archived to `coordination/archive/` only when resolved
  **and** confirmed (silence is not confirmation), via an immutable author-prefixed
  resolution manifest, moved intact with its original filename. Move only your own
  `CC_` records. Blockers need a disposition (`resolved` / `owner-accepted` /
  `deferred-until`), never archival-by-acknowledgement. Pre-C0.1 moves only on explicit
  owner instruction (bootstrap).
- Put workspace-wide engineering documentation in `doc/` and project details inside the project.

## Authority and safety

- Current controlled documents and approved decisions outrank historical exports and examples.
- Treat `docs/context/` as non-authoritative input unless a controlled document promotes content.
- Do not modify controlled evidence or `sieving/DATA` in place without approval, provenance, and
  a tested migration path.
- Do not run repair/migration scripts until target-root, dry-run, and backup behavior are reviewed.
- Never report skipped, blocked, or unrun validation as passed.

## Working protocol

1. Read this file and the nearest project `CLAUDE.md`.
2. Read the current handoff/status records when they exist.
3. Verify the actual tree and Git identity before trusting copied paths/status.
4. Use jdocmunch/jcodemunch indexes when available and refresh them after edits.
5. Keep changes scoped and test in proportion to audit/data-integrity risk.
6. Use the shared handoff skill before session close or transfer.

Current constraints: Git identity is not yet verified; runtime/test dependencies may be absent;
planned files are not evidence of implemented capability.
