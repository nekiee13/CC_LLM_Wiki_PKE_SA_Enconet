# Workspace documentation — `03_PKE_SA_NQA1/doc/`

- **Scope:** index of the workspace-level (cross-project) engineering documentation.
  Project-specific docs live inside each project (e.g. `Enconet/docs/`).
- **Owner:** shared — either agent (Codex, Claude Code) updates it under the
  coordination protocol (`Enconet/coordination/TEAM_PROTOCOL.md`); the human owner
  approves substantive policy content.
- **Update trigger:** whenever a file is added to or removed from `doc/`.

Created by Task C2.2 (`Enconet/docs/ALIGNMENT_PLAN.md`, wave G1, ADR-0005).
Navigation: workspace overview at [`../README.md`](../README.md); project docs at
[`../Enconet/docs/README.md`](../Enconet/docs/README.md) and
[`../Enconet/wiki/index.md`](../Enconet/wiki/index.md) (C6.1).

## Contents

| File | Purpose |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Global architecture: design principles, data spine, target layout |
| [FUNCTIONAL-ANALYSIS.md](FUNCTIONAL-ANALYSIS.md) | Mission, deliverables, roles, gates — what the system does and for whom |
| [AS-IS.md](AS-IS.md) | Verified current state: repository, environment, implementation inventory |
| [AFI.md](AFI.md) | Areas for improvement: known limitations and unremediated findings |
| [GOOD-PRACTICES.md](GOOD-PRACTICES.md) | Patterns proven in this workspace, with their evidence |
| [LESSONS-LEARNED.md](LESSONS-LEARNED.md) | Defects and traps already paid for; do not repeat them |
| [RECORD-KEEPING.md](RECORD-KEEPING.md) | Which records exist, where, and their immutability/lifecycle rules |
| [SKILLS.md](SKILLS.md) | Skill inventory and placement rules for both agents |
| [INDEXING.md](INDEXING.md) | Documentation/code index profiles, mandatory options, caveats |
| [GIT_CONVENTIONS.md](GIT_CONVENTIONS.md) | Commit tags, ignore policy, line endings, identity (Task C0.2) |
| [GUIDANCE_PAIRS.json](GUIDANCE_PAIRS.json) | Guidance-pair drift manifest consumed by `scripts/check_guidance_drift.py` (Task C2.1) |
| [Support_system.md](Support_system.md) | Owner-accepted portable software-development support framework: core, modules, principles, and conformance profile |
| [SUPPORT_SYSTEM_TRANSFER_MASTER_PLAN.md](SUPPORT_SYSTEM_TRANSFER_MASTER_PLAN.md) | Controlled GitHub-Issues-style Master Plan for transferring the support system to CC_FIN and CC_Loto; implementation awaits review and owner activation |
| [Support_system_transfer_draft.md](Support_system_transfer_draft.md) | Historical reviewed planning draft; superseded only when the final Master Plan is accepted and activated |

## Authority

Workspace guidance (`../CLAUDE.md`, `../AGENTS.md`) and controlled project documents
outrank these files where they conflict. `AS-IS.md` records only verified facts;
plans and intentions belong to `Enconet/MASTER_DEVELOPMENT_PLAN.md` and
`Enconet/docs/ALIGNMENT_PLAN.md`.
