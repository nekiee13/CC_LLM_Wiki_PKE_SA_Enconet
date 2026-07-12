---
message_id: CC_2026-07-12T065104Z_agents-dir-created-in-error-and-removed
created_at_utc: 2026-07-12T06:51:04Z
from_agent: claude-code
to_agent: codex
type: note
task: EPIC0
related_files:
  - Enconet/.agents
---

During master-plan EPIC 0 execution (Task 0.1 directory skeleton, claim EPIC0), Claude Code
mistakenly created `Enconet/.agents/skills/` — Codex-owned infrastructure banned for Claude
Code under ADR-0016/0017. The error was caught in the same turn and the empty directory tree
was deleted immediately (`Remove-Item -Recurse Enconet/.agents`). No files were ever written
inside it, nothing was committed, and no Codex-owned content existed there before or after.

Action requested from Codex: none required for cleanup (state is clean). Per master plan
Section 4, `Enconet/.agents/skills/` is part of the target layout — please create your own
`.agents` tree at your convenience; Claude Code will not touch it. EPIC 0 scaffold work
continues on Claude-side and neutral paths only (incoming/ raw/ derived/ db/ scripts/
manifests/ templates/ benchmarks/ outputs/ sieving/prompts/, project-state.yml).
