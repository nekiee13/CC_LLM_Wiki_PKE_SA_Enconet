# Functional analysis — what the system does and for whom

- **Scope:** functional view of the audit evidence compiler: mission, users,
  deliverables, human gates. Condensed from `Enconet/MASTER_DEVELOPMENT_PLAN.md`
  §1 and §5 (canonical); this file adds no requirements of its own.
- **Owner:** shared (either agent under the coordination protocol).
- **Update trigger:** an approved master-plan revision changing mission, roles,
  gates, or deliverables.

## Mission (master plan §1)

Ingest raw supplier QA documentation, convert it into traceable evidence, evaluate it
criterion-by-criterion against 10 CFR 50 Appendix B (as interpreted by ASME NQA-1), and
generate two consistent, validated deliverables: an **Evaluation Report** and a
**standalone HTML Dashboard**. The etalon (Appendix B) is always registered as a raw
source; its 18 criteria are ruled applicable/not-applicable per supplier before scoring.

The end state is a **validated audit evidence compiler**: raw documents in,
evidence-bounded deliverables out, machine validation at every joint — because an audit
conclusion is only defensible when every score, gap, and recommendation traces to
objective evidence in the supplier's own documents.

## Users and roles (master plan §5)

| Role | Responsibility |
|---|---|
| Human (auditor/owner) | Supplies raw documents, decides every gate, approves findings, owns final deliverables |
| Codex / Claude Code (executors) | Build the system, run pipelines, draft evaluations/findings, generate deliverables; never advance a phase on their own |

## Human gates (master plan §5)

G1 Registry → G2 Evidence → G3 Evaluation → G4 Findings → G5 Report → G6 Dashboard →
G7 Closeout. Each gate is recorded as a decision row in `manifests/approvals.csv` plus a
gate packet; agents stop at gates.

## Definition of Done (master plan §1/§7)

- Full data spine implemented and validated; all validators PASS via one aggregate runner.
- Both reference benchmarks reproduce (scoring fixture; dashboard rendering fixture).
- Report and Dashboard generate from the **same** evaluation data package; score
  divergence anywhere fails validation.
- All human gates decided and recorded; first production supplier run (Enconet corpus)
  executable end-to-end.

## Current functional coverage

As of 2026-07-11 only the sieving subsystem baseline exists
(`Enconet/sieving/src/json_extractor` — validate/flatten/query/export; see
`AS-IS.md` for the verified inventory and `AFI.md` for its known gaps). All other
spine stages are planned (EPICs 0–18); planned files are not evidence of implemented
capability.
