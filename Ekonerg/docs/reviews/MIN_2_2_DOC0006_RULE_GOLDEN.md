# MIN-2.2 DOC-0006 Part III RULE golden calibration

## Purpose

This draft answer key covers the six crumbs in corrected candidate
`RUN-20261003-41` for ASME NQA-1 Part III. Part III is interpretive,
nonmandatory guidance. These crumbs must not be treated as extra Appendix B
requirements.

## Draft calibration

- Manifest: `benchmarks/sieving_golden/manifest_rule_doc0006_partiii_v1.yml`.
- Prompt: `appb_rule_v1`.
- Source: `DOC-0006`, ASME NQA-1 Part III.
- Candidate: `RUN-20261003-41`.
- Expected crumbs: 6.
- Criteria represented: APP_B_II and APP_B_XVIII.
- Status: `pending_human_approval`.
- Approval reference: none.

Every quote is copied from the corrected candidate and checked against the raw
DOC-0006 source. The calibration preserves the conditional interpretive role;
it does not make Part III mandatory.

## Diagnostic score

The local scorer compared the draft with the corrected candidate:

- found: 6
- missed: 0
- spurious: 0
- promotion-ready: false, because no human approval reference exists

The score used `--allow-draft` for measurement only. Owner approval is still
required before this calibration can support generation promotion.
