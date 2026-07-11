# AS-IS — Repository state

Created 2026-07-11T20:54Z by Claude Code during Task C0.1. Update whenever the
repository baseline changes.

## Repository identity (C0.1, ADR-0001)

| Field | Value |
|---|---|
| Root | `C:\xPY\xPrj\LLM_Wiki\03_PKE_SA_NQA1` (one repo over Enconet, Ekonerg, TEKOL, shared assets) |
| Remote `origin` | `https://github.com/nekiee13/CC_LLM_Wiki_PKE_SA_Enconet.git` |
| Branch | `main` (tracks `origin/main`) |
| Baseline HEAD | `b4289daf03e43d14e41246664ec059ce973d8fa3` |
| Commit identity | repo-local `nekiee13 <nekiee13@gmail.com>` |
| Git version | 2.51.2.windows.1 |

## C0.1 resolution (owner-directed, 2026-07-11)

- Owner assigned C0.1 to Claude Code, then ruled the prior GitHub content
  **irrelevant**: the local tree is the new canonical baseline; the remote was
  authorized to be erased and replaced.
- Consequently no local-vs-remote file classification was performed — every local
  file is keep-local by owner decision. Prior remote HEAD `dd5736c88ac812ed577f53a9a2a82c58bb4d4f01`
  (branch `main`) is preserved here for provenance; it is no longer reachable from
  the new history after the forced update.
- Baseline commit contains 103 files. Excluded by bootstrap `.gitignore` (root):
  `*/sieving/DATA/` (68 files, ~0.96 MB, per ADR-0002) and Python caches (3 `.pyc`).
  Ignore policy refinement and the DATA checksum manifest were completed by Task C0.2
  (2026-07-11): root `.gitignore` finalized, `.gitattributes` line-ending policy added,
  `Enconet/sieving/DATA_MANIFEST.json` (68 files, SHA-256) tracked and verified by
  `Enconet/sieving/tools/verify_data_manifest.py`. Commit tags: `doc/GIT_CONVENTIONS.md`.
  External DATA backup designation remains the open owner action.

## Authentication

- GitHub auth uses Git Credential Manager with `credential.gitHubAuthModes = device`
  (browser device flow at https://github.com/login/device); the previous stored token
  was removed on owner instruction 2026-07-11. Stored account: `nekiee13`.
- `gh` CLI is not installed.

## Known caveats

- Global `user.name`/`user.email` are unset; identity is repo-local only.
- Line-ending policy is set by root `.gitattributes` (`* text=auto`, LF in repository).
- Runtime dependencies `pytest`, `pandas`, `openpyxl` remain absent (C5.3).
