# Enconet wiki index

Navigation entry point for the Enconet project (C5.1/C6.1). Workspace-wide
engineering documentation lives in [`../../doc/`](../../doc/README.md).

## Live state

- [Current status](current-status.md) — replaceable snapshot of phase and open items
- [Event log](log.md) — append-only project event log
- [`../HANDOFF.md`](../HANDOFF.md) — pointer to the latest immutable handoff in [`../handoffs/`](../handoffs/)
- [`../coordination/BOARD.md`](../coordination/BOARD.md) — generated coordination board (claims, messages)

## Authoritative documents

- [`../MASTER_DEVELOPMENT_PLAN.md`](../MASTER_DEVELOPMENT_PLAN.md) — canonical master plan (v1.4)
- [`../docs/ALIGNMENT_PLAN.md`](../docs/ALIGNMENT_PLAN.md) — canonical alignment plan (waves G0–G5)
- [`../decisions/README.md`](../decisions/README.md) — ADR register (ADR-0001…)
- [`../docs/CX_CC_RECONCILIATION.md`](../docs/CX_CC_RECONCILIATION.md) — CX/CC merge agreement
- [`../Sieving_method_specification_Guide.md`](../Sieving_method_specification_Guide.md) — sieving specification (v1.3)
- [`../schemas/`](../schemas/) — single-owner sieving contract + DATA migration manifest (ADR-0003)

## Implementation

- [`../sieving/README.md`](../sieving/README.md) — JSON extractor documentation (CLI only, ADR-0007)
- [`../sieving/QUICKSTART.md`](../sieving/QUICKSTART.md) — quick start
- [`../sieving/PROJECT_INFO.md`](../sieving/PROJECT_INFO.md) — design decisions record
- [`../sieving/PROVENANCE.md`](../sieving/PROVENANCE.md) — append-only provenance log

## Controlled intake

- [`../manifests/raw_sources.csv`](../manifests/raw_sources.csv) — immutable-source registry
- [`../manifests/batches/`](../manifests/batches/) — completed intake-batch records
- [`gates/G2-20260728-FULL-enconet.md`](gates/G2-20260728-FULL-enconet.md) —
  approved full-scope evidence and applicability review
- [`gates/G7-RUN-20260728-01-enconet.md`](gates/G7-RUN-20260728-01-enconet.md) —
  approved closeout decision for the completed evaluation

## Deliverables

- [`../outputs/enconet_appendix_b_evaluation_package.json`](../outputs/enconet_appendix_b_evaluation_package.json)
- [`../outputs/enconet_appendix_b_evaluation_report.md`](../outputs/enconet_appendix_b_evaluation_report.md)
- [`../outputs/enconet_appendix_b_dashboard.html`](../outputs/enconet_appendix_b_dashboard.html)
- [`../outputs/closeout_manifest_RUN-20260728-01.json`](../outputs/closeout_manifest_RUN-20260728-01.json)

## Coordination

- [`../coordination/TEAM_PROTOCOL.md`](../coordination/TEAM_PROTOCOL.md) — neutral protocol authority (ADR-0017/0018)
- [`../coordination/messages/`](../coordination/messages/) — active immutable messages
- [`../coordination/archive/`](../coordination/archive/) — resolved records + resolution manifests

## Historical (non-authoritative)

- [`../docs/context/`](../docs/context/) and [`../docs/_archive/`](../docs/_archive/) — preserved history (ADR-0004); never a contract
