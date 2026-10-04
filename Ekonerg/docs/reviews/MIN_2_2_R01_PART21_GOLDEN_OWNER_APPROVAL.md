# R-01 Part 21 golden-fixture owner approval

**Status:** approved by owner on 2026-10-05; generation promoted

**Approval reference:** `GOLDEN-DOC0001-PART21-20261005-OWNER`

## Approval scope

This decision approves or rejects the calibration answer key for the corrected
Part 21 sieving generation. It does not decide Part 21 applicability, Ekonerg
conformity, audit findings, or the final audit score.

## Evidence reviewed

- Fixture: `benchmarks/sieving_golden/manifest_rule_doc0001_part21_v1.yml`
- Candidate: `RUN-20261003-24`
- Source: `raw/10CFR_Part_21.md`
- Technical review: Claude approved the fixture scope and exact quotes.
- Draft score: `found=8`, `missed=0`, `spurious=0`.
- Exact source quotes: `13/13`.

## Owner decision

```text
Decision:        [x] APPROVE   [ ] APPROVE WITH CHANGES   [ ] REJECT

Owner:           Owner
Decision date:   2026-10-05
Decision ref:    GOLDEN-DOC0001-PART21-20261005-OWNER

Items to change or reject: none

Owner comments: Approved calibration scope only. Applicability and conformity
remain separate decisions.
```

## After approval

Codex recorded the fixture approval, changed the manifest status to `approved`,
reran the strict score, and promoted `RUN-20261003-24` using the separate
owner-approved generation decision. Golden approval and generation promotion
do not decide applicability or conformity.
