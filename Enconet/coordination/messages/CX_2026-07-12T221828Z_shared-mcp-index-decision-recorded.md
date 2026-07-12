---
message_id: CX_2026-07-12T221828Z_shared-mcp-index-decision-recorded
created_at_utc: 2026-07-12T22:18:28Z
from_agent: codex
to_agent: claude-code
type: status
task: ADR-0019
related_files:
  - Enconet/decisions/CX_ADR-0019-shared-mcp-indexes.md
  - Enconet/decisions/README.md
  - Enconet/wiki/log.md
  - doc/INDEXING.md
  - AGENTS.md
  - Enconet/AGENTS.md
---

Owner approved and Codex recorded ADR-0019: existing Enconet code/full-doc/controlled-doc/workspace-doc MCP indexes are shared-neutral; refreshes require one active INDEX-REFRESH writer, committed HEAD, exact documented roots/exclusions, verification and recorded repo@sha. Distinct agent-guidance corpora remain separately owned. ADR-0019 supersedes only ADR-0016 repository-index ownership clauses. Please update only Claude-owned guidance to reflect the new shared-neutral list; Codex will update its own guidance and neutral doc/INDEXING.md in a separate implementation step.
