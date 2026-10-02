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

## Reuse axiom

A new company audit must start from a company-neutral framework, not a new round of
per-file code patches. Treat a company name, path, source edition, document ID, or
approval embedded in reusable code as a framework defect to fix at its source.

The shared audit question is whether each company's own QA system meets 10 CFR 50
Appendix B requirements, using ASME NQA-1 to interpret those requirements. This
applies to Enconet, Ekonerg, and planned IBE, IMK, TEKOL, and IGH audits. Appendix B
criteria are therefore a common framework baseline, not company evidence to strip
from a clean copy. Keep each company's source documents, approved editions, mappings,
evidence, findings, and conclusions separate. This mission does not itself select an
ASME NQA-1 edition or approve any source intake or audit result.

- Keep company choices in explicit, reviewed configuration and fresh intake records.
  Do not infer regulatory applicability, source editions, storage, or approval from
  another company's project.
- Scripts must be copied into each project, as the owner requires, but the copy must
  come from one versioned, tested template. Normal runtime commands must not import
  code or read data from a sibling company project.
- Make initialization deterministic and repeatable: preview the file plan, apply only
  to the chosen new project, record hashes and provenance, and support safe retry.
  A later company should need configuration, approved source intake, and validation,
  not edits to reusable scripts.
- Test the bootstrap and normal commands with at least two synthetic company names,
  including spaces and non-ASCII characters, both with and without a sibling project.
  Assert that no other company's files change. A failure calls for a reusable fix and
  a regression test, not a one-company workaround.
- Group related transfer changes into coherent tested batches. Keep audit evidence,
  human approval gates, and required validation; avoid per-file review and handoff
  ceremony when one task-level record gives the same traceability.

## Dual-agent coordination

- Follow ADR-0016 through ADR-0019: separate agent infrastructure, shared project
  coordination, active/archive message lifecycle, and shared neutral repository indexes.
- Codex owns `AGENTS.md`, `.agents/`, `~/.codex/`, `~/.agents/`, `CX_` records, and the
  `Codex_global_guidance` and `PKE_SA_NQA1_codex_guidance` indexes.
- Do not modify or re-index Claude-owned guidance, skills, `CC_` records, or guidance-only indexes.
- ADR-0019 makes `PKE_SA_NQA1_Enconet_docs`, `PKE_SA_NQA1_Enconet_controlled`,
  `PKE_SA_NQA1_global_docs`, and `Enconet-0a063bd7` shared-neutral repository indexes.
  Either agent may query them; refresh only from committed state under one active
  `INDEX-REFRESH` claim using the exact profiles in `doc/INDEXING.md`.
- Send cross-agent notes, questions, review requests, blockers, and acknowledgements through
  the active project's `coordination/messages/` using immutable `CX_` messages. For Ekonerg,
  use `Ekonerg/coordination/`; for Enconet, use `Enconet/coordination/`. Never rewrite a
  message.
- Keep the active message directory limited to unresolved communication. Once resolution is
  confirmed, create an immutable resolution manifest and move Codex-owned `CX_` messages to
  that project's `coordination/archive/`. Claude Code archives its own `CC_` records.
- Use the active project's local `scripts/agent_coord.py` for claims, messages, releases, status
  generation, and coordination validation. The accepted message types include `claim` and
  `status` in addition to the original ADR-0017 types, as codified by that project's local
  `coordination/TEAM_PROTOCOL.md`.

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

## Permanent token-efficiency goal

Optimize token consumption across all workspace projects without weakening processing quality,
evidence integrity, validation rigor, controlled-document requirements, or human approval gates.

- Check jdocmunch/jcodemunch index identity and freshness before broad exploration. Prefer indexed
  section and symbol retrieval when current; use stale indexes only as navigation aids and verify
  relied-on conclusions against the live tree.
- Prefer narrow `rg` patterns, explicit paths, bounded results, and the minimum context required for
  the decision. Retrieve stable identifiers, summaries, and exact sections or symbols before reading
  whole files.
- Read mandatory contracts, required controlled sources, high-risk review records, and any file
  whose complete context is necessary for correctness in full. Never silently truncate required
  evidence to satisfy a token target.
- Escalate retrieval according to evidence need: compact metadata, exact evidence, adjacent context,
  then the full source. Ambiguity, conflict, missing context, or reviewer need requires escalation.
- Keep deterministic parsing, linking, validation, scoring, and artifact generation in scripts.
  Reserve LLM context for semantic judgment, exception review, and synthesis that requires it.
- Summarize routine command output while retaining exact commands, integer exit codes, counts,
  warnings, failures, and artifact paths. Preserve and inspect full logs when diagnosis requires them.
- Use focused tests during iteration, then run every mandatory aggregate or gate validation at its
  required boundary. Targeted checks never replace required full validation.
- Treat indexes as commit-scoped evidence. Prefer changed-path refreshes and a verified clean-tip
  reconciliation; rebuild fully after unproven deletion/rename handling, scope or parser changes,
  integrity failures, or unreconcilable history.
- If an efficiency method would constrain safe or correct completion, use the broader method and
  state the concrete quality or evidence reason.

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
5. Use jdocmunch for indexed documentation and jcodemunch for indexed code; refresh shared
   repository indexes only under ADR-0019 controls, and agent-specific indexes only when Codex-owned.
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
