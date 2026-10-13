# ADR-0019 — Shared neutral MCP repository indexes

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-13 |
| Decided by | Human (project owner) |
| Scope | Workspace MCP code and documentation indexes (both agents) |
| Register | Supersedes only the repository-index ownership clauses of ADR-0016; extends ADR-0017 coordination controls |
| Authored by | Codex (`CX_` prefix) |

## Context

Claude Code and Codex work on the same repository and query the same local
jcodemunch/jdocmunch backend. Maintaining agent-specific copies of an identical
repository corpus would duplicate indexing work, storage, refresh time, context, and
staleness management without improving retrieval.

Live capability review on 2026-07-13 established that code indexing is already shared
in practice: exactly one Enconet code index exists. Documentation duplication is limited
to profiles whose corpus scope genuinely differs, especially agent-specific guidance.

## Decision

Repository-scoped MCP indexes are shared neutral infrastructure:

| Corpus | Tool | Canonical index |
|---|---|---|
| Enconet code | jcodemunch | `local/Enconet-0a063bd7` |
| Enconet full documentation | jdocmunch | `local/PKE_SA_NQA1_Enconet_docs` |
| Enconet controlled documentation | jdocmunch | `local/PKE_SA_NQA1_Enconet_controlled` |
| Workspace engineering documentation | jdocmunch | `local/PKE_SA_NQA1_global_docs` |

Either agent may query and verify these indexes. Refreshes follow these controls:

1. Exactly one agent refreshes a shared index at a time under an active
   `INDEX-REFRESH` coordination claim.
2. Shared indexes are refreshed only from committed repository state. The indexed Git
   HEAD and verification result are recorded in status or handoff evidence.
3. `doc/INDEXING.md` is the neutral binding refresh specification. Every refresh passes
   the documented source root and complete exclusion set; tool defaults or a bare
   incremental refresh are not an adequate profile specification.
4. Enconet documentation profiles exclude at least `raw/**`, `incoming/**`,
   `derived/**`, `db/**`, `sieving/DATA/**`, and agent-local settings/infrastructure as
   specified by the profile. Controlled-view exclusions remain additional.
5. A refresh is complete only after the applicable index verification reports no drift,
   missing documents, or errors. Structural tool caveats remain documented explicitly.
6. Separate agent-owned indexes are allowed only when corpus scope or tool configuration
   genuinely differs. Codex guidance indexes (`Codex_global_guidance`,
   `PKE_SA_NQA1_codex_guidance`) remain Codex-owned; equivalent Claude guidance scope,
   if indexed, remains Claude-owned.
7. No duplicate repository code index is created merely to provide an agent-specific
   name. The existing generated Enconet code identity is retained.

## Consequences

- The repository-index ownership rows in ADR-0016 are superseded by this decision;
  ADR-0016 continues to govern `AGENTS.md`, `CLAUDE.md`, agent directories, global
  configuration, guidance-only indexes, and `CX_`/`CC_` record ownership.
- Shared index refreshes become coordinated writes under ADR-0017 rather than unilateral
  agent-owned maintenance. Queries remain concurrent and read-only.
- `doc/INDEXING.md` and each agent's own guidance must be updated to distinguish shared
  repository indexes from agent-owned guidance indexes. Each agent edits only its own
  infrastructure under ADR-0016.
- Existing canonical repository indexes are promoted in place; no retirement or rebuild
  is required solely for naming.
- The first shared refresh occurs only after the raw-source disposition and related code
  changes are committed, using the expanded exclusions and a recorded verification.
