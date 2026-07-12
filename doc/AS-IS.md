# AS-IS — Verified current state

- **Scope:** verified facts about the repository, environment, and implemented
  capability. Every claim here carries a file, command, or test reference
  (ALIGNMENT_PLAN C2.2 acceptance); anything unverified belongs in `AFI.md` or the
  plans, not here.
- **Owner:** shared — the agent whose action changes the baseline updates this file
  in the same change.
- **Update trigger:** any change to repository identity, environment, dependency
  state, or implemented capability.

Created 2026-07-11T20:54Z by Claude Code during Task C0.1; extended by C2.2.

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

## Environment (C5.3, 2026-07-11)

- Default interpreter: `C:\xAppz\miniconda\python.exe`, Python 3.13.9 (shared
  miniconda base env — no project venv; open owner decision, see `AFI.md`).
- Installed 2026-07-11: pytest 9.1.1, pandas 3.0.3, openpyxl 3.1.5, numpy 2.5.1
  (verify on other machines: `python -m pytest --version`).
- Mandatory suite from `Enconet/sieving` (2026-07-12): `python -m pytest -q
  -p no:cacheprovider` → **48 passed**, 72% measured coverage, exit 0;
  `python verify_install.py` (PYTHONUTF8=1) → all checks passed, exit 0.
- Workspace script suite (2026-07-12): `python -m pytest scripts/tests -q` →
  **21 passed**, exit 0. Aggregate runner: `python scripts/run_validation.py` (C5.2).
- Corpus integrity: `Enconet/sieving/tools/verify_data_manifest.py` →
  OK, 68 files match `DATA_MANIFEST.json` (2026-07-12).
- `gh` CLI is not installed (checked 2026-07-11).

## Implemented capability (verified)

- Sieving subsystem: `Enconet/sieving/src/json_extractor`
  (validate/flatten/query/export), tests in `Enconet/sieving/tests` (the 48 passing
  tests above). Fail-closed filtering + CLI exit 2 (C4.1); blocking ERROR-validation
  export gate with recorded override reason (C4.2); hazardous tools quarantined in
  `sieving/tools/_archive/`, non-mutating `verify_install.py` (C4.3); single-owner
  contract `Enconet/schemas/sieving_contract.yml` loaded at runtime, drift-tested
  against the 68-file corpus (C4.4, ADR-0003); docs advertise CLI only with
  docs-vs-reality smoke tests (C4.5, ADR-0007). Known gaps: `AFI.md`.
- Handoff infrastructure: `handoff_schema.yml` + `scripts/make_handoff.py`
  (render/validate/atomic publish/staleness; C3) — integrated in both agents'
  session protocols.
- Coordination tooling: `scripts/agent_coord.py` (C2.4; `validate` clean 2026-07-12).
- Guidance drift validator: `scripts/check_guidance_drift.py` +
  `doc/GUIDANCE_PAIRS.json` (C2.1; 0 errors, 38 anchors, 2026-07-12).
- Skill-structure validator: `scripts/check_skill_structure.py` (C2.3; 0 errors).
- Aggregate layered validation runner: `scripts/run_validation.py` (C5.2; L0–L5,
  SKIPPED ≠ PASS).
- Record taxonomy instantiated: `Enconet/wiki/` log/status/index (C5.1); navigation
  READMEs interlinked (C6.1); index profiles + caveats in `doc/INDEXING.md` (C6.2).
- ALIGNMENT_PLAN waves G0–G5 are implemented (2026-07-12); the master plan's
  database/report/dashboard EPICs (2+) remain **planned, not implemented**; planned
  files are not evidence of implemented capability.

## Known caveats

- Global `user.name`/`user.email` are unset; identity is repo-local only
  (`git config user.name` at root).
- Line-ending policy is set by root `.gitattributes` (`* text=auto`, LF in repository).
