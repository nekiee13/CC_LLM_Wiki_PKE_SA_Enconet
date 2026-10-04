# R-01 Part 21 golden-fixture owner approval

**Status:** pending owner decision

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
Decision:        [ ] APPROVE   [ ] APPROVE WITH CHANGES   [ ] REJECT

Owner:           ______________________________________
Decision date:   ______________________________________
Decision ref:    ______________________________________

Items to change or reject (write "none" if not applicable):
_______________________________________________________
_______________________________________________________

Owner comments:
_______________________________________________________
_______________________________________________________
```

## After approval

Codex will record the fixture approval, change the manifest status to
`approved`, rerun the strict score, and use that score in the controlled
promotion command. Golden approval alone does not decide applicability or
conformity.
