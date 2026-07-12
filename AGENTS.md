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
- Claude-owned index names currently include `PKE_SA_NQA1_Enconet_docs`,
  `PKE_SA_NQA1_Enconet_controlled`, `PKE_SA_NQA1_global_docs`, and
  `Enconet-0a063bd7`; Codex may inspect their recorded state but must not refresh them.
- Send cross-agent notes, questions, review requests, blockers, and acknowledgements through
  `Enconet/coordination/messages/` using immutable `CX_` messages. Never rewrite a message.
- Keep the active message directory limited to unresolved communication. Once resolution is
  confirmed, create an immutable resolution manifest and move Codex-owned `CX_` messages to
  `Enconet/coordination/archive/`. Claude Code archives its own `CC_` records.
- Use `scripts/agent_coord.py` for claims, messages, releases, status generation, and
  coordination validation. The accepted message types include `claim` and `status` in addition
  to the original ADR-0017 types, as codified by `Enconet/coordination/TEAM_PROTOCOL.md`.

## Git workflow

- This is a single-developer repository. Prefer frequent, small commits pushed directly to the
  active working branch, currently `main`.
- Use pull requests only when the project owner explicitly requests one or an external constraint
  requires one. Do not introduce default PR ceremony, review-gate branches, or long-lived feature
  branches; cross-agent review occurs through immutable coordination messages and pushed commits.

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
   When the owner asks to "check messages", automatically inspect, independently review, validate,
   and acknowledge actionable Codex-addressed messages in the same turn unless the owner explicitly
   requests a read-only listing or the review is blocked. Never acknowledge acceptance without evidence.
   Complete the ADR-0018 lifecycle in the same turn: archive resolved and confirmed Codex-owned
   `CX_` records with an immutable resolution manifest, then regenerate and validate the board.
4. Check the actual tree and Git identity before trusting paths or status copied from another machine.
5. Use jdocmunch for indexed documentation and jcodemunch for indexed code; refresh only Codex-owned indexes after edits.
6. Run `python scripts/check_guidance_drift.py` after guidance or paired-skill edits and
   `python scripts/check_skill_structure.py` before adding or moving skills.
7. Keep changes scoped and add tests in proportion to audit, data-integrity, and cross-project risk.
8. Before session close, use the user-global `handoff` skill and record failed or unavailable checks explicitly.
9. Publish session handoffs through `python scripts/make_handoff.py`; validate existing records
   with `python scripts/make_handoff.py --validate <record>`. Never label a check `passed`
   without its command and integer exit code.

## Current environment

- Git is established at the `03_PKE_SA_NQA1` workspace root on `main`; verify current HEAD,
  upstream, and worktree state at session start rather than relying on a copied snapshot.
- The active shared Miniconda interpreter has the Enconet runtime/test dependencies installed
  (`pytest`, `pandas`, and `openpyxl`, verified by C5.3 on 2026-07-11). A dedicated project virtual
  environment remains an owner decision, and future sessions must still treat failed imports as failures.
- Planned files and directories are not evidence of implemented capability.
