# Enconet project documentation — `Enconet/docs/`

Catalog of project-level documentation (Task C6.1). Navigation starts at
[`../wiki/index.md`](../wiki/index.md); workspace-level engineering documentation
lives in [`../../doc/`](../../doc/README.md).

## Controlled / current

| File | Status |
|---|---|
| [ALIGNMENT_PLAN.md](ALIGNMENT_PLAN.md) | **Canonical** alignment plan (waves G0–G5, acceptance criteria); frozen — reopening requires the owner |
| [CX_CC_RECONCILIATION.md](CX_CC_RECONCILIATION.md) | The CX/CC merge agreement behind the canonical plans |

The other authoritative project documents live one level up:
[`../MASTER_DEVELOPMENT_PLAN.md`](../MASTER_DEVELOPMENT_PLAN.md) (canonical, v1.4),
[`../decisions/README.md`](../decisions/README.md) (ADR register),
[`../Sieving_method_specification_Guide.md`](../Sieving_method_specification_Guide.md),
and [`../schemas/`](../schemas/) (ADR-0003 contract owner).

## Historical / non-authoritative (ADR-0004)

| Directory | Status |
|---|---|
| [`context/`](context/) | Source input preserved for provenance; never a contract |
| [`_archive/`](_archive/) | Superseded plan variants, critiques, session exports; cataloged, exempt from controlled-doc gates |

Nothing in `context/` or `_archive/` outranks a controlled document or an accepted
ADR. Promote content only through a controlled document plus, where policy changes,
an ADR.
