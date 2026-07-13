# ADR-0002 — `sieving/DATA` is not tracked in git; checksums are

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Project (Enconet), pattern applies to future entries |
| Register | D-2 option (c) |

## Context

`Enconet/sieving/DATA` holds 68 supplier-derived crumb JSON files (~1.2 MB). Options:
(a) track in git, (b) Git LFS, (c) keep outside the repository and track only checksums.
The corpus derives from supplier-internal documentation; the owner chose not to place it
in the GitHub-backed repository.

## Decision

Option (c): the DATA corpus is **not** committed to git. A manifest with per-file SHA-256
checksums **is** committed and machine-verified.

## Consequences

- Root `.gitignore` excludes `Enconet/sieving/DATA/` (and future `<project>/sieving/DATA/`).
- A tracked manifest (filename, size, SHA-256, source note) is added; a validator confirms
  the on-disk corpus matches it and fails on missing/foreign/modified files.
- **Open action (risk):** until an external controlled backup location is designated by the
  owner, the corpus exists only on this machine — single-copy risk. The handoff record must
  flag this until resolved.
- Any sanitized in-repo fixture subset (for tests) requires a separate approval.

## Open-action resolution

On 2026-07-13, the project owner designated the removable USB volume `WIKI_BCKP`
(volume serial `DFF9-9A03`; mounted as `F:` at the time of backup) as the external
controlled backup location. The first immutable snapshot was written to
`PKE_SA_NQA1/Enconet/ADR-0002/2026-07-13T210221Z/` on that volume.

The snapshot contains `DATA/` and `DATA_MANIFEST.json`. Post-copy verification against
the manifest found 68 expected and 68 actual files, with zero missing, foreign, or
modified files. The copied manifest SHA-256 is
`8df578abf6603c898c025d5b1e3860878462c211df142714bf463d1a18de61fc`.
The single-copy risk is therefore resolved as of this snapshot; future corpus changes
still require a new verified snapshot.
