# G3 vendor-crumb evaluation approval

## What this gate controls

This gate approves the scoring method used to judge Ekonerg's vendor-document
evidence against Appendix B.

It does **not** approve a final audit score or say that Ekonerg passes. It only
approves the ruler that will be used for the later judgments.

## Vendor evidence used

- Vendor documents with active runs: 24
- Active vendor crumbs: 189
- Evidence matrix: `out/2026-10-04/vendor_evidence_matrix.md`
- Evaluation run: `RUN-20261003-32`
- Applicability: 12 applicable and 6 conditional criteria, already approved at G2

## Proposed scoring model

Model file: `schemas/scoring_model.yml`

| Rating | Weight |
|---|---:|
| Fully | 1.00 |
| Substantially | 0.75 |
| Partially | 0.50 |
| Minimally | 0.25 |
| Unmet | 0.00 |
| Undetermined | 0.00 until evidence is sufficient |
| Not applicable | excluded only after an approved applicability decision |

The consolidated score is calculated as:

```text
100 × sum of criterion weights ÷ number of applicable criteria
```

The result is rounded to one decimal place. Conditional criteria cannot receive
a scored rating until their applicability is confirmed.

## Owner decision

```text
Decision:        [ ] APPROVE   [ ] APPROVE WITH CHANGES   [ ] REJECT

Owner:           ______________________________________
Decision date:   ______________________________________
Decision ref:    G3-RUN-20261003-32

Required changes or comments:
_______________________________________________________
_______________________________________________________
```

### Meaning of the choices

- **APPROVE:** Codex may record criterion judgments using this model.
- **APPROVE WITH CHANGES:** Codex updates the model and waits for confirmation.
- **REJECT:** scoring remains blocked; no final conformance score is produced.

## Important boundary

Vendor crumbs are evidence leads. A policy sentence alone is not proof that a
control was used. Each judgment must consider objective records, approvals,
roles, outputs, revision history, or other implementation evidence. Missing
proof must remain `undetermined`, partially supported, or an open gap; it must
not be silently treated as a pass.
