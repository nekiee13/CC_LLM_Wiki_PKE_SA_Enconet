# Architecture — NQA Supplier Audit Wiki (workspace view)

- **Scope:** the global architecture shared by all supplier projects (Enconet first):
  design principles, the canonical data spine, and the target directory layout.
  Summary only — the canonical source is `Enconet/MASTER_DEVELOPMENT_PLAN.md` v1.4
  §2–§4; where this file and the plan diverge, the plan wins.
- **Owner:** shared (either agent under the coordination protocol); architectural
  changes require a plan revision or ADR, never an edit here alone.
- **Update trigger:** an approved master-plan revision or ADR that changes principles,
  spine, or layout.

## Design principles (master plan §2, condensed)

1. **Evidence-bounded evaluation** — positive classifications require at least one
   supporting objective crumb; reasoning never substitutes for evidence.
2. **One data spine, one truth** — Report and Dashboard read the same validated
   evaluation package; divergence is a validation failure.
3. **Contracts before code, code before outputs** — schemas first, generators last.
4. **KISS task sizing** — one artifact per task, one session per task.
5. **Raw is immutable** — `raw/` never changes after promotion; checksums prove it.
6. **Generated, never hand-edited** — Report/Dashboard are compiler outputs.
7. **Human gates own the state** — agents execute; the human approves phase advances.
8. **Heritage by copy, not by reference** — proven patterns are copied and adapted.
9. **Supplier-agnostic engine** — parameterized by `<supplier>`; Enconet is first.
10. **Trilingual policy, verbatim evidence** (ADR-0009) — SL/EN/HR only; quotes verbatim;
    no translation layer; deliverable language chosen per run.
11. **Applicability before evaluation** — the 18 Appendix B criteria are ruled
    applicable/not-applicable per supplier before any scoring.
12. **Sieving is the crown activity, built for iteration** — versioned prompts,
    generational runs, measured effectiveness, one-step rollback.

## The data spine (master plan §3, canonical chain)

```text
raw document → extracted text (derived/) → semantic chunk (DB) → APP_B crumb + quotes (DB)
→ chunk↔crumb link → requirement registry → applicability ruling → criterion evaluation
→ gaps/findings/actions → evaluation data package (outputs/*.json)
→ evaluation report (outputs/*.md) → dashboard data + HTML (outputs/*.html/.json)
```

Every fact travels this chain; traceability drift between stages is the main project
risk and is machine-validated at every joint.

## Layout (master plan §4, condensed)

- `03_PKE_SA_NQA1/` — workspace root: shared guidance pair (`CLAUDE.md`/`AGENTS.md`),
  `doc/` (this directory), `scripts/` (workspace validators, coordination tooling),
  per-tool skill trees.
- `Enconet/` — first project: plan, ADRs (`decisions/`), controlled docs (`docs/`),
  coordination records (`coordination/`), handoffs, and the sieving subsystem
  (`sieving/` — code `src/json_extractor`, tests, `DATA/` per ADR-0002,
  `PROVENANCE.md`). Future layers per plan: `db/`, `schemas/`, `raw/`, `derived/`,
  `outputs/`, `benchmarks/`.
- `Ekonerg/`, `TEKOL/` — future supplier project entries (currently placeholders).

## Dual-agent architecture (ADR-0016/0017/0018)

Separate agent infrastructure (each agent owns its own guidance/skill/index files),
shared project coordination through neutral versioned records in
`Enconet/coordination/`. Semantic equivalence of the guidance pairs is machine-checked
by `scripts/check_guidance_drift.py` against `doc/GUIDANCE_PAIRS.json`.
