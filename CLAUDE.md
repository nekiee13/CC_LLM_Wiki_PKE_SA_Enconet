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
  Codex counterpart `~/.agents/skills/handoff/SKILL.md` (also user-global); changes must
  update both.
- Keep Claude Code discovery files separate from Codex `AGENTS.md`/`.agents` files. Equivalent
  rules must stay semantically aligned; tool-specific differences must be documented.
- **Infrastructure ownership ban (ADR-0016/0017):** Claude Code must never create, edit,
  delete, move, or re-index Codex infrastructure — `AGENTS.md` files, `.agents/` trees,
  `~/.codex/`, `~/.agents/`, `CX_`-prefixed records, or Codex-owned indexes
  (`Codex_global_guidance`, `PKE_SA_NQA1_codex_guidance`, `PKE_SA_NQA1_agent_guidance`).
  The reciprocal ban (Codex ↔ Claude infrastructure) is stated in `AGENTS.md`. Each
  agent applies changes to its own files only.
- **Shared-neutral repository indexes (ADR-0019, supersedes the ADR-0016
  repository-index ownership clauses only):** the Enconet code index
  (`Enconet-0a063bd7`), full docs (`PKE_SA_NQA1_Enconet_docs`), controlled docs
  (`PKE_SA_NQA1_Enconet_controlled`), and workspace docs (`PKE_SA_NQA1_global_docs`)
  MCP indexes are shared-neutral: either agent may query and verify them. Refreshes
  require an active `INDEX-REFRESH` coordination claim (single writer), a clean
  committed HEAD, the exact roots/exclusions documented in `doc/INDEXING.md`,
  post-refresh verification, and the certified `repo@sha` recorded in handoff/status.
  Distinct agent-guidance corpora remain separately owned.
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
2. Session-start reading order (ADR-0017, C2.4): `HANDOFF.md` → `coordination/BOARD.md`
   → unread `coordination/messages/` → active `coordination/claims/`. The neutral
   protocol authority is `Enconet/coordination/TEAM_PROTOCOL.md`; use
   `python scripts/agent_coord.py` (status | claim | release | message | acknowledge |
   validate) for coordination operations. When the owner asks to "check messages",
   inspect, independently review/validate, and respond to actionable Claude-addressed
   messages in the same turn, unless the owner explicitly requests a read-only listing
   or evidence is insufficient — never acknowledge acceptance without evidence. Complete
   the ADR-0018 lifecycle in the same turn: archive resolved-and-confirmed Claude-owned
   `CC_` records with an immutable resolution manifest, then regenerate and validate
   the board; leave `CX_` archival to Codex.
3. Verify the actual tree and Git identity before trusting copied paths/status.
4. Use jdocmunch/jcodemunch indexes when available and refresh them after edits.
5. Keep changes scoped and test in proportion to audit/data-integrity risk.
6. After editing any guidance or skill-pair file, run
   `python scripts/check_guidance_drift.py` (manifest: `doc/GUIDANCE_PAIRS.json`, C2.1);
   silent divergence between the CLAUDE.md/AGENTS.md pairs fails the check.
7. Session end: running the user-global `/handoff` skill is mandatory before session
   close or transfer; session start reads `HANDOFF.md` first (step 2), then verifies it
   against reality (step 3).
8. Publish session handoffs through `python scripts/make_handoff.py`
   (`--source-agent claude-code`); validate existing records with
   `python scripts/make_handoff.py --validate <record>` (schema:
   `handoff_schema.yml`, C3). Never label a check `passed` without its command
   and integer exit code.

Current constraints: runtime/test dependencies (`pytest`, `pandas`, `openpyxl`) are
installed in the default interpreter on this machine (C5.3, 2026-07-11) — verify with
`python -m pytest --version` on other machines; planned files are not evidence of
implemented capability. Repository facts (root,
remote, identity) live in `doc/AS-IS.md`.
