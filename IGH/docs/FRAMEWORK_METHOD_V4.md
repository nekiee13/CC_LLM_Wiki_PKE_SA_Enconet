# Company-neutral framework v4 — usage

This release supplies tools, not an approved audit. Each supplier has its own
local scripts. No sibling company's documents or decisions are used at runtime.

## Folder homes

Keep owner inputs in incoming, registered sources in raw, and the database in db.
Working files live in work: derived, manifests, benchmarks, decisions, reviews,
validation, bootstrap and migrations. Put plans in docs/plans and session notes
in coordination/handoffs. project-layout.json explicitly selects v4.

Results use outputs/RUN-YYYYMMDD-N. dashboard_light.html and dashboard_dark.html
are separate self-contained files. Open either one directly; no theme chooser
or server is needed. Internal review packages belong in work/reviews.

## Start a new audit

1. Read the local AGENTS.md, project-state.yml and sieving/SIEVING_PLAYBOOK.md.
2. Put this supplier's documents and proposed regulatory sources in incoming.
3. Agree source editions, scope, language and applicability with the owner.
4. Initialize a fresh database with python scripts/init_db.py, then follow the
   documented intake, chapter, calibration, sieving and approval commands.
5. Use python scripts/audit_command.py audit-status to check the current stage.
   Do not skip a gate or copy another supplier's approval.

No database, sources, crumbs, scores, active prompt or golden fixture is installed.
Claude setup and review remain pending; Codex must not edit Claude infrastructure.
Old method documents are retained for history; this is the current layout guide.

## Reset and repeat

Reset is preview-first. Review its exact targets and arrange the local backup
decision before apply. It preserves incoming and framework/history records.
A backup waiver from another supplier never transfers. Never reset to upgrade
the framework or to make a test pass.
