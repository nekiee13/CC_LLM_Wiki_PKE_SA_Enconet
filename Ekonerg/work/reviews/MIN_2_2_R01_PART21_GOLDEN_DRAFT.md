# R-01 Part 21 golden fixture draft

**Status:** approved by owner; generation promoted

## Purpose

This draft turns the Claude-reviewed corrected Part 21 generation into a
repeatable calibration check. It is not an applicability decision and it is
not an audit conclusion.

## Fixture

- Manifest: `benchmarks/sieving_golden/manifest_rule_doc0001_part21_v1.yml`
- Candidate: `RUN-20261003-24`
- Source: `raw/10CFR_Part_21.md`
- Prompt: `appb_rule_v1`
- Expected crumbs: 8
- Expected evidence quotes: 13
- Approval reference: `GOLDEN-DOC0001-PART21-20261005-OWNER`

All 13 expected quotes were copied from the corrected candidate and checked by
Claude as exact substrings of the raw Part 21 source. The owner approved this
calibration set. It remains separate from Part 21 applicability and Ekonerg
conformity decisions.

## Required next step

The fixture approval is recorded in `manifests/approvals.csv`. The strict
score passed and the controlled generation command promoted
`RUN-20261003-24` over `RUN-20261003-23` under
`R01-PART21-GEN2-PROMOTE-20261005-OWNER`. Applicability and conformity remain
separate.

## Promotion evidence

- Strict score: `found=8`, `missed=0`, `spurious=0`, `promotion_ready=true`.
- Database SHA-256: `6cffba9bdbc2330b6ee915ba847fd86981d7a3957dc50d69e26bd7d37d5d818c`.
- Score SHA-256: `493e535cad9ba47f8f8fe90cd0b1278d76c69ade94b4255b9222bb8483131880`.
- Candidate metrics SHA-256: `297bec77924925d2bc8ed797a75a44cc74cac8255c2510662c1ef8f5f378d842`.

The aggregate remains blocked only by historical traceability records; no
audit score or conformity conclusion has been produced.
