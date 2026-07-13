# Indexing — profiles, mandatory options, caveats

- **Scope:** documentation/code index profiles used in this workspace, the options
  that are mandatory on every refresh, and known tool caveats. Task C6.2 will extend
  this with the full jmunch profile table; entries below are the profiles verified in
  use as of 2026-07-11.
- **Owner:** repository code/docs indexes are shared-neutral under ADR-0019; agent-specific
  guidance indexes remain separately owned under ADR-0016.
- **Update trigger:** a profile is created, re-rooted, renamed, or a new caveat is
  observed.

## Shared-neutral repository profiles

Plan profile names (ALIGNMENT_PLAN C6.2) map to these actual index names:

| Plan name | Tool | Index name | Root | Mandatory options (every refresh) |
|---|---|---|---|---|
| `enconet-docs` | jdocmunch | `local/PKE_SA_NQA1_Enconet_docs` | `Enconet/` | `extra_ignore_patterns: ["raw/**", "incoming/**", "derived/**", "db/**", "sieving/DATA/**", "coordination/archive/**", "coordination/claims/**", "coordination/BOARD.md", "AGENTS.md", "CLAUDE.md", "**/AGENTS.md", "**/CLAUDE.md", "**/CC_*", ".claude/**", ".agents/**", "**/settings.local.json"]`; pass an explicit filtered tracked-file list to defeat dot-directory force-discovery |
| — (controlled view) | jdocmunch | `local/PKE_SA_NQA1_Enconet_controlled` | `Enconet/` | docs patterns **plus** `["docs/context/**", "docs/_archive/**", "coordination/archive/**"]` |
| `nqa1-global-docs` | jdocmunch | `local/PKE_SA_NQA1_global_docs` | `03_PKE_SA_NQA1/doc/` | none (directory holds only workspace docs) — created 2026-07-12 (C6.2) |
| `enconet-code` | jcodemunch | `local/Enconet-0a063bd7` | `Enconet/` | `extra_ignore: ["raw/**", "incoming/**", "derived/**", "db/**", "sieving/DATA/**", "coordination/**", "wiki/**", ".claude/**", ".agents/**", "**/settings.local.json"]`; `.gitignore` honored |

Refresh discipline: exactly one writer holds an active `INDEX-REFRESH` claim; either
agent may query or verify. Refresh after batch documentation changes and before `/handoff`;
full refresh (documented root + full ignore list) rather than bare incremental after
any structural change; SHA-certification requires a clean worktree (refresh after
commit); run `verify_index` after each full refresh and record the certified
`repo@sha` in the next handoff. Last recorded certification: all three doc profiles
clean (0 drift / 0 missing / 0 errors) at `81adeea`, 2026-07-14.

## Agent-owned guidance indexes

`Codex_global_guidance` and `PKE_SA_NQA1_codex_guidance` remain Codex-owned because
their corpus is Codex guidance. Equivalent Claude-specific guidance scope remains
Claude-owned. Do not create a second repository code/docs index merely for agent naming.

## Caveats (observed, dated)

- **Wrong-root incremental refresh silently re-roots a profile** — an incremental
  jdocmunch refresh without the documented root + ignore patterns re-rooted the docs
  profile and pulled `sieving/DATA` JSON into it (observed live 2026-07-11). Rule:
  always pass the documented root **and** the full ignore-pattern list; the patterns
  are not persisted between refreshes.
- **Dead-code output is heuristic** — `find_dead_code` false-positives on `__init__`
  re-exports; confirm with `find_importers`/grep before deletion
  (`Enconet/docs/CX_CC_RECONCILIATION.md` §2.2.2).
- **Counts are not acceptance criteria** — index section counts change as corpora
  grow (reconciliation §2.3.5); test properties (zero drift, `verify_index` clean),
  not fixed counts.
- **`verify_index` skips `#0` root sections** — every document-root pseudo-section
  reports `empty_byte_range` and is counted as skipped (observed 2026-07-12); this is
  a structural artifact, not corruption. Clean = 0 drift / 0 missing / 0 errors.
- **Orphan analysis is section-granular** — `get_orphan_sections` flags interior
  sections of documents that are themselves fully navigable, and immutable records
  (handoffs, messages) that are linked by pointer/manifest rather than prose (waived
  2026-07-12 per the C6.1 rule: the orphan gate applies at document level to
  controlled docs; archived history is cataloged but exempt).
- **BOARD.md pointer links must be re-rooted** — `BOARD.md` lives in
  `coordination/`, so project-relative `handoffs/...` links must be rewritten to
  `../handoffs/...` (fixed in `agent_coord.py`, 2026-07-12; found by
  `get_broken_links`).
- **jcodemunch language discovery expanded beyond Python** — index version 17
  discovered JSON and YAML in addition to Python (observed 2026-07-14), so relying
  on the former Python-only default admitted `sieving/DATA` and one `.claude` file.
  Rule: every code refresh must pass the full explicit exclusion list in the
  `enconet-code` profile above. The installed CLI also lacks the former
  `verify-index` subcommand; verify source root/loadability/counts and the certified
  Git SHA through `resolve_repo`, `list_repos`, and `get_repo_outline`.
- **jdocmunch may force-discover agent guidance despite directory ignores** — a
  full walk with `.agents/**` still admitted `.agents/skills/README.md`, and the
  former profile did not exclude root `CLAUDE.md` (observed 2026-07-14). Shared
  repository doc refreshes must exclude both agents' root/directory guidance and
  pass an explicit filtered tracked-file list; do not rely on ignore patterns alone.
