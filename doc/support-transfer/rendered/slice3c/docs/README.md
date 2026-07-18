# Repository Documentation Index

Last reviewed: 2026-06-16
Source commit: `030bcd5`

This index is the primary entry point for all documentation in this repository.

## Documentation Sets

| Set | Path | Purpose | Status |
|---|---|---|---|
| Project documents | `docs/project/` | Whole-repo README, Architecture & Functional analysis, SRS, Manual, AS-IS | Current |
| FIN runtime | `docs/fin/` | Forecasting and scenario engine architecture, contracts, and SwS | Current |
| Operational runbooks | `docs/*.md` (root) | Follow-up ML operations, ANN operator flow, governance notes | Current |
| ANN training upgrade | `docs/ann_training/` | SGN+Magnitude ANN upgrade plan (epics A–E, OI-1…OI-7) | **COMPLETE 2026-06-16** |
| LSTM calibration | `docs/lstm_calibration/` | LSTM point-forecast calibration backtest plan (3 epics) | Complete |
| OpenCode (OC) | `docs/oc/` | OC-specific architecture, entities, diagrams, and SwS | Current |
| Integration pilot evidence | `docs/integration-pilot/` | Time-bounded pilot execution evidence and ADRs | Historical evidence |
| Refactor governance | `docs/refactor/` | Phase-1 invariants and architectural decisions | Current |

## Start Here

- Whole-repo project document set (README, Architecture & Functional analysis, SRS, Manual, AS-IS): `docs/project/README.md`
- FIN runtime docs: `docs/fin/README.md`
- ANN training upgrade (plan + AS-IS, all epics/OIs complete): `docs/ann_training/00_ann_training_upgrade_plan.md`
- OC docs: `docs/oc/README.md`
- Integration pilot status and usage: `docs/integration-pilot/README.md`
- Phase-1 invariants: `docs/refactor/phase1_rules.md`
- Governance transition and trunk operations: `docs/governance-transition.md`
- [Support system](../support/README.md) — repo-local governance, coordination, and handoff core

## Freshness and Ownership

- Full file-level inventory and actions: `docs/documentation_freshness_ledger.md`
- Generated OC artifacts are snapshots and must be refreshed via OC docs build flow.
- Integration pilot files remain retained as evidence and should not be treated as default runtime instructions unless explicitly marked current.
- Link integrity (verified 2026-06-26, commit `e8b9461`): all 17 relative links across the `docs/project/` set resolve, and the two cross-file section anchors (`Architectural_and_functional_analysis.md#42-forecasting-core-srcmodels`, `Manual.md#6-git--sync-trunk-only-workflow`) match GitHub's heading-slug algorithm; confirmed against GitHub's GFM render.

## Maintenance Policy

- Review cadence: at least once per sprint, or immediately after contract/entrypoint changes.
- Required metadata updates on meaningful doc changes:
  - `Last reviewed`
  - source commit/hash reference where applicable
  - status classification (`Current`, `Historical evidence`, `Generated snapshot`)
- PR checklist requirement: update docs whenever interfaces, schemas, runbooks, or operator workflows change.

- Canonical FIN runtime open/close runbook: `docs/opencode-runtime-safe-open-close.md`
