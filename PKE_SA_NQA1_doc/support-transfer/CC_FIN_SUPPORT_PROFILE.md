# CC_FIN support profile v1.0

## Control

- Target: `C:\xPY\xPrj\CC_FIN` / `nekiee13/CC_FIN`
- Accepted planning baseline candidate: `238c207c73970f3d3c6dc00c2db5932ebeca7be4`
- Profile state: candidate for owner gate M1; not published to the target
- Product authority: owner-designated enhanced implementation Master Plan
- Support authority: this profile only after M1 approval; it never replaces product requirements

## Identity, roles, and authority

The human owner approves gates, authority changes, destructive recovery, hosted-governance
changes, and release decisions. Codex owns `AGENTS.md`, `.agents/`, and `CX_` records. Claude
owns `CLAUDE.md`, `.claude/`, and `CC_` records. Neutral coordination, support schemas,
decision registers, logs, handoffs, and generated board/status views are shared by contract.
An agent may inspect but not edit the other agent's infrastructure.

Existing feature ADRs, project documentation, GitHub workflows/templates, freshness ledger, and
the enhanced product plan remain authoritative in their existing scopes. The support index links
to them and does not copy or renumber them. The `Proposed` header on the owner-designated plan is
an M1 disposition item; support work will not silently edit it.

## Core records and planned paths

The common repo-local core will use:

- `support/README.md` for authority and navigation;
- `support/current-status.md` as the replaceable current-state view;
- `support/log.md` as append-only event history;
- `support/decisions/README.md` plus immutable ADR files;
- `support/AFI.md`, `support/LESSONS-LEARNED.md`, and `support/GOOD-PRACTICES.md`;
- `support/handoffs/`, schemas, and templates for clone-complete session continuity;
- `coordination/messages/`, `coordination/archive/`, `coordination/claims/`, and generated
  `coordination/BOARD.md`;
- root `HANDOFF.md` as a pointer to the current validated handoff.

Product issues stay in the product Master Plan or GitHub Issues. Support records link to product
issues and do not create a competing backlog.

## Enabled modules

| Module | State at initial publication | Rationale |
|---|---|---|
| Mandatory governance/records/ADR/handoff/validation/recovery core | Enabled | Required portable contract |
| Dual-agent ownership and immutable messaging | Enabled | Both agents are active writers |
| Multi-writer claims and generated board | Enabled | Prevent overlapping edits |
| Lightweight human milestone gates | Enabled | Preserve owner control without product state-machine duplication |
| Documentation and code indexes | Enabled after committed-state preflight | Repository scale justifies navigation support |
| Hosted-governance adapter | Integrate existing files; mutation separately approved | Existing GitHub controls must not be shadowed |
| Release adapter | Inventory only | No tags and no transfer release requested |
| Repo-local workflow skills | Disabled initially | No proven repeated target-specific workflow yet |
| Formal workflow state machine | Disabled | Product work does not require Wiki's phase engine |

## Git and hosted workflow

Work remains on `main` with small, reversible commits. Preflight requires clean status and exact
baseline. Publication is sequential and reviewed before push. No force push, history rewrite,
broad reset, branch-protection mutation, tag, or release is authorized. Hosted protection remains
`unknown` until verified. The workflow branch mismatch (`master` versus `main`) is a separate M1
decision and, if approved, a separately reviewed change.

## Native validation contract

Support checks add a fast layer and compose with, rather than replace, native checks:

1. support schema, reference, ownership, message, claim, board, and handoff validators;
2. focused `python -m pytest` tests for changed support integration;
3. relevant existing unit/integration tests;
4. broader `python -m pytest` when proportional to risk;
5. targeted Ruff checks where already applicable;
6. CPI tests only when CPI prerequisites exist and the change touches CPI behavior;
7. existing CI as hosted evidence after push.

Skipped optional checks are reported as skipped or unavailable, never passed. Support validators
must not trigger forecasting, model generation, dashboard rendering, or expensive data pipelines.

## Product preservation

The three chart-generation paths, including the A-F standalone Cockpit/dashboard, remain product
capabilities. The support transfer does not change their status, wiring, data, or acceptance.
Dashboard pipeline work recorded as seeded/pending remains a product-plan concern.

## Sensitivity and indexing

Secrets stay outside Git; records may name environment-variable contracts but never values.
Tracked datasets, spreadsheets, output snapshots, model fixtures, vendor trees, archives,
generated output, caches, debug material, and machine-private paths are excluded from support
indexes and copied evidence. A record may cite a committed path and checksum when necessary.
Initial index profiles include committed source, tests, and authoritative documentation only.
Index refresh requires one explicit claim and committed-state verification.

## Scale and performance

The profile assumes one human owner, two agents, low concurrent write volume, approximately 1,052
tracked files, moderate support-record growth, Git retention, and fast support validation measured
in seconds. It introduces no database, service, queue, or runtime dependency into the product.

## Recovery and release

Before each publication slice, capture HEAD, upstream, clean status, and the allowed path list.
Abort on drift, ownership conflict, unexpected generated files, secret/data exposure, failing
support checks, or changed product behavior. Revert only identified support commits after owner
approval; never use `reset --hard` as routine recovery and never remove unrelated work. Re-run
preflight and native focused checks after rollback. Release creation remains out of scope.

## M1 acceptance conditions

- The owner accepts this version and exact baseline SHA.
- FIN remains the first and only active publication pilot.
- The profile's data/index exclusions and disabled modules are accepted.
- Guidance and CI collision dispositions are explicit.
- Publication uses the path-level manifest and stops before any unapproved target mutation.
