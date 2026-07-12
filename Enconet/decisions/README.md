# Decision records (ADRs) — 03_PKE_SA_NQA1 / Enconet

One decision per file. Records are **immutable**: to change a decision, write a new ADR
that names the one it supersedes — never edit or delete an accepted record. Workspace-scoped
ADRs live here until the workspace `doc/` scaffold exists; they may then migrate as a
reviewed change.

Format per record: header table (status, date, decided-by, scope, register ref) →
Context → Decision → Consequences.

## Register

| ADR | Decision | Scope | Status |
|---|---|---|---|
| [ADR-0001](ADR-0001-repository-boundary.md) | One git repository rooted at `03_PKE_SA_NQA1` | Workspace | Accepted |
| [ADR-0002](ADR-0002-data-policy.md) | `sieving/DATA` kept out of git; checksum manifest tracked | Project | Accepted |
| [ADR-0003](ADR-0003-schema-owner.md) | Canonical schemas start in `Enconet/schemas/` | Project | Accepted |
| [ADR-0004](ADR-0004-context-archive.md) | Historical context moves to `docs/_archive/`, never deleted | Project | Accepted |
| [ADR-0005](ADR-0005-dual-agent-policy.md) | Both Claude Code and Codex maintained, with drift validation | Workspace | Accepted |
| [ADR-0006](ADR-0006-canonical-master-plan.md) | v1.3-CX becomes the canonical master plan | Project | Accepted |
| [ADR-0007](ADR-0007-gui-retirement.md) | No standalone sieving GUI (backfill of 2026-07-04 decision) | Project | Accepted (backfilled) |
| [ADR-0008](ADR-0008-output-naming.md) | Output naming `<supplier>_<framework>_<artifact>`; framework label `appendix_b` | Project | Accepted |
| [ADR-0009](ADR-0009-language-policy.md) | Languages sl/en/hr; no translation; verbatim quotes; per-run deliverable language | Project | Accepted |
| [ADR-0010](ADR-0010-db-engine.md) | SQLite is the committed database engine | Project | Accepted |
| [ADR-0011](ADR-0011-evidence-page-granularity.md) | 18 per-criterion evidence pages (not per-crumb) | Project | Accepted |
| [ADR-0012](ADR-0012-scope-determinability.md) | Undeterminable supplier scope = non-conformance, never silent N/A | Project | Accepted |
| [ADR-0013](ADR-0013-scoring-deferral.md) | Scoring calibration deliberately deferred to Gate G3 | Project | Accepted (deferral) |
| [ADR-0014](ADR-0014-global-claude-handoff.md) | Claude Code `/handoff` skill installed user-globally (`~/.claude/skills/`) | User env + workspace | Accepted |
| [ADR-0015](CX_ADR-0015-global-codex-handoff.md) | Codex `/handoff` skill installed user-globally (`~/.agents/skills/`) | User env + workspace | Accepted |
| [ADR-0016](CC_ADR-0016-dual-agent-infrastructure-ban.md) | Dual-agent infrastructure ownership ban (neither agent touches the other's files/indexes) | Workspace + user env | Accepted |
| [ADR-0017](CC_ADR-0017-interagent-coordination-protocol.md) | Inter-agent coordination protocol: `coordination/` (TEAM_PROTOCOL, BOARD, messages, claims); repo = channel; implementation after C0.1 | Workspace | Accepted (deferred impl.) |
| [ADR-0018](CX_ADR-0018-coordination-message-lifecycle.md) | Active messages contain unresolved work; confirmed resolutions are logged and archived intact | Workspace | Accepted |
| [ADR-0019](CX_ADR-0019-shared-mcp-indexes.md) | Repository code/docs MCP indexes are shared-neutral with single-writer refresh controls; distinct guidance corpora remain agent-owned | Workspace | Accepted |
| [ADR-0020](CX_ADR-0020-regulatory-authority-and-interpretive-standard.md) | Appendix B is the governing baseline, Part 21 is a mandatory nonconformance add-on, and NQA-1 is the interpretive/implementation standard | Project | Accepted |

All decided 2026-07-11 by the project owner (D-1…D-6 from `docs/CX_CC_RECONCILIATION.md` §6
and the six domain decisions from `MASTER_DEVELOPMENT_PLAN.md` §8), except ADR-0007 which
backfills the 2026-07-04 GUI decision.

ADR-0019 was decided 2026-07-13 by the project owner after joint Codex/Claude capability
review confirmed that Enconet code indexing is already shared in practice.

ADR-0020 was decided 2026-07-13 by the project owner to establish the authority model
required before EPIC5 schema and sieving implementation.
