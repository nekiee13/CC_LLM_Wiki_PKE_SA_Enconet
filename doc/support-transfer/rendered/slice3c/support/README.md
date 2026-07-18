# CC_FIN support system

## Authority

- Product plan: `docs/project/CC_FIN_project_upgrade_plan_enhanced.md`
- Product documentation: `docs/README.md`
- Support profile: `support/PROFILE.md`
- Repository: `https://github.com/nekiee13/CC_FIN` (`main`)

This index links authorities; it does not copy product requirements, backlog, progress, or
decisions. Product authority outranks support workflow where scopes conflict.

## Ownership

The human project owner approves gates, authority changes, destructive recovery, hosted-governance changes, tags, releases, and publication. Codex owns `AGENTS.md`, `.agents/`, and `CX_` records. Claude Code owns `CLAUDE.md`, `.claude/`, and `CC_` records. Coordination, support records, handoffs, schemas, templates, validators, and generated views are shared-neutral by contract. Each agent may inspect but must not edit or archive the other agent's owned infrastructure.

## Current records

- [Record classes](RECORD-KEEPING.md)
- [Current status](current-status.md)
- [Append-only event log](log.md)
- [Support decisions](decisions/README.md)
- [Areas for improvement](AFI.md)
- [Lessons learned](LESSONS-LEARNED.md)
- [Good practices](GOOD-PRACTICES.md)
- [Current handoff](../HANDOFF.md)
- [Coordination board](../coordination/BOARD.md)

## Existing decision authorities

- Enhanced implementation plan: [CC_FIN project upgrade plan](../docs/project/CC_FIN_project_upgrade_plan_enhanced.md)
- Project documentation index: [project documents](../docs/project/README.md)
- Architecture and current-state authority: [AS-IS](../docs/project/AS-IS.md)
- Documentation freshness authority: [freshness ledger](../docs/documentation_freshness_ledger.md)
- Existing feature decisions: [integration-pilot ADR register](../docs/integration-pilot/adr/README.md)
- Hosted workflows and forms: [pull-request template](../.github/pull_request_template.md), [M5 expansion exception issue form](../.github/ISSUE_TEMPLATE/m5-expansion-exception.yml), [follow-up ML gate](../.github/workflows/followup-ml-gate.yml), [label bootstrap](../.github/workflows/followup-ml-label-bootstrap.yml), and [scope governance](../.github/workflows/followup-ml-scope-governance.yml)
- Packaging authorities: [pyproject.toml](../pyproject.toml), [runtime requirements](../requirements.txt), and [test requirements](../requirements.test.txt)
- Release/package status: release adapter is **inventory-only**; remote tag inventory is empty and no release record is present. Creating a tag or release is outside this transfer.

## Validation and exclusions

- Native validation entry point: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest; run Ruff only where already applicable and CPI only when its prerequisites exist and CPI behavior changes`
- Sensitive/product-data exclusions: secrets and private paths; datasets, spreadsheets, vendor/archive trees, generated outputs, caches, debug material, model artifacts, and prohibited product data per [PROFILE.md](PROFILE.md)

Skipped, unavailable, blocked, and not-run checks are never reported as passed.
