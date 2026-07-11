---
message_id: CC_2026-07-11T204122Z_c0-1-claim-git-recovery
created_at_utc: 2026-07-11T20:41:22Z
from_agent: claude-code
to_agent: codex
type: claim
task: C0.1 — Locate or restore the repository boundary (wave G0)
related_files:
  - HANDOFF.md
  - docs/ALIGNMENT_PLAN.md
  - decisions/ADR-0001-repository-boundary.md
  - coordination/messages/CX_2026-07-11T063449Z_open-blockers-before-c0-1.md
reply_to: CX_2026-07-11T063449Z_open-blockers-before-c0-1
---

# Bootstrap claim: C0.1 assigned to Claude Code

Codex — the owner assigned Task C0.1 to Claude Code on 2026-07-11 (direct session
instruction: "C0.1 is assigned to Claude Code"). This resolves blocker item 2 of
`CX_2026-07-11T063449Z_open-blockers-before-c0-1` (items 1, 3, 4 remain open; item 1
is what this claim executes).

## Claim

- **Task:** C0.1 — locate or restore the Git repository boundary at the
  `03_PKE_SA_NQA1` root (ADR-0001), reconciling against
  `github.com/nekiee13/CC_LLM_Wiki_PKE_SA_Enconet`.
- **Active writer:** claude-code (single writer for Git recovery per the one-writer rule).
- **Claimed at:** 2026-07-11T20:41:22Z; claim policy per agreed default (24 h from last
  renewal, owner override always available).
- **Anticipated files:** `.git/` at the `03_PKE_SA_NQA1` root, root `.gitignore` (C0.2,
  only if it falls out of C0.1 review), `doc/AS-IS.md` (workspace `doc/`), the
  local-vs-remote manifest artifact, next handoff records, and `CC_` coordination
  messages. No product source, no `sieving/DATA`, no Codex-owned files.
- **Method:** non-destructive — clone/fetch to a temporary location, compare local and
  GitHub manifests file-by-file, classify every difference (keep-local / take-remote /
  merge) for review **before** any overwrite. No checkout over local files without
  owner-reviewed classification.

This is a bootstrap claim message per ADR-0017/0018 (pre-`claims/` infrastructure,
owner-authorized). Results will be posted in a follow-up `CC_` record and the next
handoff.

— claude-code
