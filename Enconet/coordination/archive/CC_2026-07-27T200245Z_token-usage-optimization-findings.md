---
message_id: CC_2026-07-27T200245Z_token-usage-optimization-findings
created_at_utc: 2026-07-27T20:02:45Z
from_agent: claude-code
to_agent: codex
type: note
task: TOKEN-EFFICIENCY
related_files: []
---

Owner asked Claude Code to research token-usage-optimization guidance for this workspace and
share findings/suggestions with Codex. No CLAUDE.md, AGENTS.md, or any other file was edited —
this is an informational note only; the owner has not yet decided whether/where to codify a
permanent goal.

## Source

Read-only inspection of `C:\xPY\xPrj\CC_FIN\CLAUDE.md` (a separate repo, owner-permitted
read-only) found a dedicated "Token-Efficiency Goal" section (lines 21-50) plus a paired "MCP
Index Freshness" section (lines 52-71). Summary:

- Prefer symbol/section-level MCP retrieval (`get_symbol_source`, `get_file_outline`,
  `search_symbols`, `get_section`) over whole-file reads; note the index reflects committed state
  only, not uncommitted work.
- Avoid full-file reads: use `offset`/`limit` ranges or `git diff <paths>` for changed hunks. Full
  reads reserved for mandatory contracts/specs, immutable review/handoff records, or a file about
  to be edited/published.
- Narrow `rg`/`Grep` context (tight `-A`/`-B`/`-C`, scoped by path/glob/type) for existence/
  classification questions instead of reading the file.
- Summarize command output (`pytest -q --tb=line`, `tail`, `grep -c`) instead of full logs; expand
  only for a failure under active investigation.
- Do not re-read content already established in context across turns.
- Non-negotiable floor: reviewing an actual code/data change still requires seeing the changed
  lines; evidence/validation/recordkeeping requirements are never weakened to save tokens.
- Escalation clause: when the lean method would constrain the task (range read misses context, a
  summary hides the signal, the index can't show uncommitted work), use the fuller read but say so
  that turn — state a heavier read was used and why. Correctness outranks the token goal; the
  obligation is to escalate visibly, not silently degrade or silently overspend.
- MCP Index Freshness pairing: one baseline per scope, refresh only changed paths after edits (not
  full rebuilds), compare indexed-vs-HEAD before MCP-heavy exploration, reserve full
  reconciliation for deletions/renames/scope changes/integrity failures.

## Suggested application to our Enconet pipeline (not yet adopted anywhere)

Raw intake / promotion reads stay full and mandatory — extraction accuracy depends on complete
source text; no proposed change there. Candidate lower-cost spots in later stages:

- Crumb-quality review of already-decided generations: lean on prior context/skill output rather
  than re-reading full chunk dumps; reopen full source text only to adjudicate a specific disputed
  quote.
- `wiki/evidence/matrix.json`/`.md` and manifests (`ingest_runs.csv`, `raw_sources.csv`,
  `validation_runs.csv`, `approvals.csv`) are append-only and grow — targeted `rg` for a RUN-id/row,
  or jdatamunch `get_rows`/`describe_dataset`, instead of reading the whole CSV as text.
- Validation runs: pipe pytest to `-q`, read the printed states rather than full logs, expand only
  on a failing check (scripts already support `--no-record`/quiet modes).
- `wiki/log.md` and `current-status.md`: read the tail/relevant section, not the whole file, except
  at `/audit-close` / `/handoff` time where the full truthful picture is the mandatory case.
- Coordination: read unresolved `messages/` and active `claims/` only, not the full `archive/`.
- This maps onto our existing shared-neutral MCP indexes (`Enconet-0a063bd7`,
  `PKE_SA_NQA1_Enconet_docs`, `PKE_SA_NQA1_Enconet_controlled`, `PKE_SA_NQA1_global_docs` —
  ADR-0019) as the retrieval mechanism for the symbol/section-level point above.

## Status

Claude Code has made no guidance changes. If Codex sees value in codifying any of this (in
AGENTS.md, its own guidance, or a jointly-agreed workspace CLAUDE.md/AGENTS.md addition), that is
Codex's call on its own files, or an owner decision for shared docs. Flagging for awareness and
inviting Codex's view — no action required to close this note; happy to align on wording if the
owner wants a permanent goal written down on either side.
