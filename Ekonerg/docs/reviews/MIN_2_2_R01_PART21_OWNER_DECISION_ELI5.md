# R-01 Part 21 owner decision — ELI5

## What is the owner deciding?

The owner is choosing whether the corrected evidence set for `RUN-20261003-24`
is ready for the audit team to use.

Think of it like checking a box of labeled evidence cards:

- Are the 8 crumbs sensible?
- Do the quotes really come from the Part 21 source?
- Is anything important missing or wrong?

The owner is **not** deciding whether Ekonerg passes the audit. This decision
only selects the evidence version that may be used later.

## The three choices

### APPROVE

The evidence set is good enough to use. Codex can promote
`RUN-20261003-24` as the accepted Part 21 generation.

### APPROVE WITH CHANGES

The evidence is mostly good, but the owner lists exact changes. Codex keeps the
candidate inactive, makes a corrected generation, and asks for confirmation
again.

### REJECT

The evidence set should not be used. Codex keeps it inactive and records why it
was rejected. The older generation remains available for traceability.

## Current candidate

- Run: `RUN-20261003-24`
- Crumbs: 8
- Exact quote links: 13/13 (100%)
- Rejected items: 0
- Failed items: 0

## Owner response

```text
Decision:        [ ] APPROVE   [ ] APPROVE WITH CHANGES   [ ] REJECT

Owner:           ______________________________________
Decision date:   ______________________________________
Decision ref:    ______________________________________

Comments:
_______________________________________________________
_______________________________________________________
```

The completed decision is recorded in `manifests/approvals.csv`. It does not
create an audit conclusion or a compliance score.
