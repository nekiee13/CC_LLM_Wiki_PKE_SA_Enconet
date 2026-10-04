# R-01 Part 21 golden fixture draft

**Status:** pending owner approval; no promotion performed

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
- Approval reference: pending

All 13 expected quotes were copied from the corrected candidate and checked by
Claude as exact substrings of the raw Part 21 source. The fixture remains
`pending_human_approval` until the owner approves this calibration set.

## Required next step

After owner approval, record the fixture approval in `manifests/approvals.csv`,
run `score_sieving.py` against the corrected candidate, and use the resulting
promotion-ready score in the controlled generation command. Until then,
`RUN-20261003-24` remains an inactive candidate.
