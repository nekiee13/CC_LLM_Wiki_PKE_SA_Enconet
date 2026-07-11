# Indexing — profiles, mandatory options, caveats

- **Scope:** documentation/code index profiles used in this workspace, the options
  that are mandatory on every refresh, and known tool caveats. Task C6.2 will extend
  this with the full jmunch profile table; entries below are the profiles verified in
  use as of 2026-07-11.
- **Owner:** each agent documents and maintains only its own tool indexes (ADR-0016);
  this file lists both for navigation.
- **Update trigger:** a profile is created, re-rooted, renamed, or a new caveat is
  observed.

## Claude-owned jdocmunch profiles (maintained by Claude Code)

| Profile | Root | Mandatory `extra_ignore_patterns` (every refresh) |
|---|---|---|
| `local/PKE_SA_NQA1_Enconet_docs` | `Enconet/` | `["sieving/DATA/**", ".claude/**", "**/settings.local.json"]` |
| `local/PKE_SA_NQA1_Enconet_controlled` | `Enconet/` | docs patterns **plus** `["docs/context/**", "docs/_archive/**", "coordination/archive/**"]` |

Refresh discipline: refresh after batch documentation changes and before `/handoff`;
SHA-certification requires a clean worktree (refresh after commit); run `verify_index`
after each full refresh. Last certified state is recorded in each handoff.

## Codex-owned indexes (named for navigation only — never touched by Claude Code)

`Codex_global_guidance`, `PKE_SA_NQA1_codex_guidance`, `PKE_SA_NQA1_agent_guidance`
(ADR-0016). Their roots and refresh rules are Codex-documented.

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

## Planned (Task C6.2, not yet implemented)

Profiles `enconet-code` (jcodemunch, `Enconet/`, Python only) and `nqa1-global-docs`
(jdocmunch over `03_PKE_SA_NQA1/doc/` — becomes possible now that C2.2 created this
directory's content), with stable names, excludes, and full-vs-incremental rules.
