# PKE SA NQA1 Codex Guidance

## Scope

These instructions apply to every project under `03_PKE_SA_NQA1`. A nested `AGENTS.md` may add
project-specific rules but must not weaken evidence, source-integrity, validation, or recordkeeping
requirements defined here.

## Workspace model

- Treat `03_PKE_SA_NQA1` as the workspace root and `Enconet`, `Ekonerg`, and `TEKOL` as project entries.
- Put user-global Codex skills in `$HOME/.agents/skills/<skill>/SKILL.md`.
- Put workspace-shared Codex skills in `.agents/skills/<skill>/SKILL.md`.
- Put project-specific Codex skills in `<project>/.agents/skills/<skill>/SKILL.md`.
- Keep Codex configuration (`AGENTS.md`, `.agents/`) separate from Claude Code configuration
  (`CLAUDE.md`, `.claude/`). Update only the Codex side and record Claude synchronization as
  pending; Claude Code owns changes to its infrastructure.
- Put workspace-wide engineering documentation in `doc/` and project details inside the project.

## Dual-agent coordination

- Follow ADR-0016 through ADR-0018: separate agent infrastructure, shared project
  coordination, and active/archive message lifecycle.
- Codex owns `AGENTS.md`, `.agents/`, `~/.codex/`, `~/.agents/`, `CX_` records, and the
  `Codex_global_guidance` and `PKE_SA_NQA1_codex_guidance` indexes.
- Do not modify or re-index Claude-owned guidance, skills, `CC_` records, or indexes.
- Send cross-agent notes, questions, review requests, blockers, and acknowledgements through
  `Enconet/coordination/messages/` using immutable `CX_` messages. Never rewrite a message.
- Keep the active message directory limited to unresolved communication. Once resolution is
  confirmed, create an immutable resolution manifest and move Codex-owned `CX_` messages to
  `Enconet/coordination/archive/`. Claude Code archives its own `CC_` records.
- Until C0.1 restores Git and C2.4 creates the complete channel, messages created by explicit
  owner instruction are bootstrap records; `BOARD.md`, claims, and tooling remain deferred.

## Authority and safety

- Current controlled documents and approved decisions outrank historical session exports and examples.
- Treat every `docs/context/` directory as non-authoritative input unless a current document explicitly
  promotes a requirement from it.
- Do not modify controlled source evidence or `sieving/DATA` in place without explicit approval,
  provenance capture, and a tested migration path.
- Do not run repair or migration scripts until their target-root calculation, dry-run behavior, and
  backup strategy have been reviewed.
- Never report a validation as passed when it was skipped, blocked, or not run.

## Working protocol

1. Read this file and the nearest project `AGENTS.md`.
2. Read the project's current status/handoff when those records exist.
3. Read `coordination/BOARD.md`, unread messages addressed to Codex, and active claims when present.
4. Check the actual tree and Git identity before trusting paths or status copied from another machine.
5. Use jdocmunch for indexed documentation and jcodemunch for indexed code; refresh only Codex-owned indexes after edits.
6. Keep changes scoped and add tests in proportion to audit, data-integrity, and cross-project risk.
7. Before session close, use the user-global `handoff` skill and record failed or unavailable checks explicitly.

## Current preparation constraints

- Git metadata has not yet been verified at this workspace root.
- The active Python environment may not contain Enconet runtime/test dependencies.
- Planned files and directories are not evidence of implemented capability.
