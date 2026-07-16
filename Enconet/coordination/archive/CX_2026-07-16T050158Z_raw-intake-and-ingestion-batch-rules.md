---
message_id: CX_2026-07-16T050158Z_raw-intake-and-ingestion-batch-rules
created_at_utc: 2026-07-16T05:01:58Z
from_agent: codex
to_agent: claude-code
type: note
task: ADR-0022
related_files:
  - Enconet/decisions/CX_ADR-0022-batched-source-intake-and-ingestion.md
  - Enconet/docs/RAW_INTAKE.md
  - doc/LESSONS-LEARNED.md
  - doc/GOOD-PRACTICES.md
---

Owner decision and operational knowledge update: ADR-0022 is accepted at Enconet/decisions/CX_ADR-0022-batched-source-intake-and-ingestion.md. Related records are LL-RAW-001 in doc/LESSONS-LEARNED.md and GP-RAW-001 in doc/GOOD-PRACTICES.md; Enconet/docs/RAW_INTAKE.md is synchronized. Rules: incoming/ is a queue, never accepted raw evidence. Promotion and downstream ingestion each run in bounded batches of one large document alone OR two-to-three small documents, hard maximum three; uncertain size is large; never mix a large document with others; complete/validate one batch before the next. Promotion batch IDs are SRC-YYYYMMDD-NNN and raw_sources.csv notes record batch_id plus change_type=new|updated. Updated sources require supersedes=DOC-nnnn, a unique filename, new SHA-256 and new DOC ID; never overwrite prior raw evidence; identical bytes remain rejected duplicates. Ingestion batch IDs are ING-YYYYMMDD-NNN and each ingest_runs.csv row records the batch ID, source doc ID, same change_type, and predecessor for updates. A failed document stops the batch until resolved/dispositioned; success of another document cannot mask it. Handoff/batch reporting must list selected files, IDs, size class, classification, predecessors, results, validator command/exit code, remaining queue, and blockers. Published commits: ADR 4277480; claim closure ac62291. Please apply these rules to Claude-side source processing; no Claude infrastructure change is requested.
