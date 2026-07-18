# CC_FIN support profile (target-local controlled authority)

## Control

- Repository: `https://github.com/nekiee13/CC_FIN` (`main`)
- Record class: Controlled (see [RECORD-KEEPING.md](RECORD-KEEPING.md))
- Provenance (history, not a runtime reference): profile v1.0 approved by the human
  project owner on 2026-07-16 at transfer gate M1; target-local installation authorized
  by the owner's transfer gate M2 decision and its amendment 1 on 2026-07-18.
- This file is the target-local support authority for ownership, enabled modules,
  validation composition, sensitivity, scale, and recovery. It never replaces product
  requirements: where scopes conflict, product authority outranks support workflow.

## Identity, roles, and authority

The human owner approves gates, authority changes, destructive recovery,
hosted-governance changes, and release decisions. Codex owns `AGENTS.md`, `.agents/`,
and `CX_` records. Claude owns `CLAUDE.md`, `.claude/`, and `CC_` records. Neutral
coordination, support schemas, decision registers, logs, handoffs, and generated
board/status views are shared by contract. An agent may inspect but not edit the other
agent's infrastructure.

Existing feature ADRs, project documentation, GitHub workflows/templates, the
documentation freshness ledger, and the enhanced product Master Plan remain
authoritative in their existing scopes; support records link to them and do not copy or
renumber them.

## Enabled modules

| Module | State | Rationale |
|---|---|---|
| Governance/records/ADR/handoff/validation/recovery core | Enabled | Required portable contract |
| Dual-agent ownership and immutable messaging | Enabled | Both agents are active writers |
| Multi-writer claims and generated board | Enabled | Prevent overlapping edits |
| Lightweight human milestone gates | Enabled | Owner control without a product state machine |
| Documentation and code indexes | Enabled only after committed-state preflight | Navigation support at repository scale |
| Hosted-governance adapter | Integrate existing files; any mutation separately approved | Existing GitHub controls must not be shadowed |
| Release adapter | Inventory only | No tags or releases requested |
| Repo-local workflow skills | Disabled initially | No proven repeated target-specific workflow yet |
| Formal workflow state machine | Disabled | Product work does not require a phase engine |

## Native validation contract

Support checks add a fast layer and compose with, never replace, native checks:

1. support schema, reference, ownership, message, claim, board, and handoff validators;
2. focused `python -m pytest` tests for changed support integration;
3. relevant existing unit/integration tests;
4. broader `python -m pytest` when proportional to risk;
5. targeted Ruff checks where already applicable;
6. CPI tests only when CPI prerequisites exist and the change touches CPI behavior;
7. existing CI as hosted evidence after push.

Skipped, unavailable, blocked, and not-run checks are never reported as passed. Support
validators must not trigger forecasting, model generation, dashboard rendering, or
expensive data pipelines.

## Product preservation

The three chart-generation paths, including the A-F standalone Cockpit/dashboard,
remain product capabilities. Support work does not change their status, wiring, data,
or acceptance; pipeline work recorded as seeded/pending remains a product-plan concern.

## Sensitivity and indexing

Secrets stay outside Git; records may name environment-variable contracts but never
values. Tracked datasets, spreadsheets, output snapshots, model fixtures, vendor trees,
archives, generated output, caches, debug material, and machine-private paths are
excluded from support records and indexes; a committed path may be cited with a
checksum when necessary. Index profiles include committed source, tests, and
authoritative documentation only; an index refresh requires one explicit claim and
committed-state verification.

## Scale assumptions

One human owner, two agents, low concurrent write volume, on the order of a thousand
tracked files, moderate support-record growth, Git retention, and support validation
measured in seconds. No database, service, queue, or runtime dependency enters the
product.

## Recovery

Before each publication slice, capture HEAD, upstream, clean status, and the allowed
path list. Abort on drift, ownership conflict, unexpected generated files, secret or
data exposure, failing support checks, or changed product behavior. Revert only
identified support commits after owner approval; never use `reset --hard` as routine
recovery and never remove unrelated work. Re-run preflight and native focused checks
after any rollback.
