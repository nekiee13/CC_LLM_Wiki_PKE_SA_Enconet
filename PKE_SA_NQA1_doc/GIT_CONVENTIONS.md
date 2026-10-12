# Git conventions — 03_PKE_SA_NQA1

Agent-neutral workspace guidance (Task C0.2). Applies to every commit in this
repository by either agent (Codex, Claude Code) or the owner.

## Commit tag vocabulary (ALIGNMENT_PLAN C0.2)

Prefix commit subjects with one or more of:

`[align] [scaffold] [docs] [schema] [ingest] [eval] [report] [dashboard] [gate] [fix] [test] [handoff]`

- `[align]` — plan/ADR/coordination alignment work
- `[scaffold]` — project skeleton, manifests, state files, git hygiene (master plan EPIC 0; e.g. `[scaffold] 0.4: seed manifest CSVs`)
- `[docs]` — documentation content
- `[schema]` — data or record schema changes
- `[ingest]` — ingestion/sieving pipeline
- `[eval]` — evaluation method or runs
- `[report]` / `[dashboard]` — output surfaces
- `[gate]` — validation gates and blocking checks
- `[fix]` — defect fixes
- `[test]` — test-only changes
- `[handoff]` — handoff records and pointers

Task IDs (e.g. `C0.2`) belong in the subject when the commit executes a planned task.

## Ignore policy (root `.gitignore`)

- `*/sieving/DATA/` is never tracked (ADR-0002); its SHA-256 manifest
  (`Enconet/sieving/DATA_MANIFEST.json`) **is** tracked and machine-verified by
  `Enconet/sieving/tools/verify_data_manifest.py`.
- Caches, virtualenvs, DB journals, `.obsidian/workspace*`, and agent-local settings
  (`.claude/settings.local.json`) stay untracked.

## Line-ending policy (root `.gitattributes`)

`* text=auto`: text files are stored with LF in the repository; working-tree endings
follow each machine's git configuration. Binary evidence formats are exempt.

## Identity

Commits use the owner's identity `nekiee13 <nekiee13@gmail.com>` (repo-local config).
Agent authorship is recorded via `Co-Authored-By` trailers.
