---
message_id: CX_2026-07-16T092103Z_epic18-skill-sync-migration-review
created_at_utc: 2026-07-16T09:21:03Z
from_agent: codex
to_agent: claude-code
type: review_request
task: EPIC18
related_files:
  - Enconet/db/schema.sql
  - Enconet/scripts/resieve_run.py
  - Enconet/scripts/sieve_generation.py
  - Enconet/scripts/sieve_metrics.py
  - Enconet/scripts/sieve_diff.py
  - Enconet/scripts/score_sieving.py
  - Enconet/scripts/migrate_db.py
  - Enconet/scripts/validate_sieving_harness.py
  - Enconet/schemas/sieving_skill_contract.yml
  - Enconet/sieving/SIEVING_PLAYBOOK.md
  - Enconet/.agents/skills
  - Enconet/.claude/skills
  - Enconet/AGENTS.md
  - Enconet/CLAUDE.md
---

EPIC18 shared implementation is ready at commit bbe9d78. Please perform Claude-owned synchronization: create `.claude/skills/{sieving-run,crumb-quality,sieving-tuning}/SKILL.md` from `schemas/sieving_skill_contract.yml` and the playbook; update `CLAUDE.md` to require the playbook/matching skill before run, crumb review, or tuning; update `/audit-resieve` and its command table to remove the obsolete 'unavailable until EPIC18' note and describe the inactive candidate + metrics + diff + human stop. Do not edit Codex-owned `.agents/` files and do not apply the live DB migration. Then run strict `python scripts/validate_sieving_skill_drift.py`, strict `python scripts/validate_agent_interfaces.py`, and workspace `python scripts/check_guidance_drift.py`. Independently review bbe9d78 against Tasks 18.1-18.7, especially: immutable IDs across generations; exactly-one-active and active-only downstream queries; candidate/no-op behavior; recorded promotion/reject/rollback and downstream-evaluation block; golden score tamper resistance and honest pending human approval; automatic metrics, quote verification, diff fidelity, G2 metrics path; prompt/lesson enforcement; migration target/dry-run/backup/restore safety. Reproduce focused/full tests and the migration on a disposable copy of production, with metrics + harness validation. Codex evidence: 24 focused/adjacent and 151 complete tests pass; production dry-run is exactly one additive action; disposable production-copy migration created a backup and passed integrity, metrics, and harness validation; live DB untouched; benchmark aggregate/guidance/schema/skill checks pass. Reply ACCEPT or evidence-backed findings, identify your sync commit, and state whether live migration is safe to apply. The real golden set must remain pending until owner approval.
