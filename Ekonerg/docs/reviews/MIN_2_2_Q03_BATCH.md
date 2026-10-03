# MIN-2.2 Q-03 bounded batch

## Result

Q-03 processed three related Ekonerg procedures: document control,
nonconformance control, and corrective action. The batch stayed within the
planned small-document group. It produced 19 active-generation crumbs across
the three documents. Quotes in the two completed runs all linked to the local
chapter store.

| Document | Run | Active status | Crumbs | Quote links | Main criteria |
|---|---|---|---:|---:|---|
| DOC-0014 | `RUN-20261003-03` | active | 6 | 7/7 (100%) | VI, XVII, XVIII |
| DOC-0029 | `RUN-20261003-04` | active | 7 | 10/10 (100%) | XV, XVI, XVII |
| DOC-0030 | `RUN-20261003-05` | active, link review incomplete | 6 | 6/8 (75%) | I, VII, XVI, XVII |

DOC-0030 had two quotes that crossed an embedded page-image marker. The first
active import therefore retained the crumbs but could not link those two
quotes. A corrected generation, `RUN-20261003-06`, was created as an inactive
candidate. It has 9/9 links (100%) and is awaiting a recorded generation
decision; it has not replaced the active generation.

## What this shows

- Strict DOCUMENT validation accepts all 19 Q-03 active crumbs.
- Objective evidence was collected as separate controls, roles, actions, and
  records rather than treating a high-level procedure reference as proof.
- Chapter and heading locators remain the evidence addresses.
- Part 21 wording in DOC-0029 was retained as a candidate scope/evidence lead;
  this batch does not decide regulatory applicability or audit compliance.

## Limits and next action

- These are source statements, not proof that Ekonerg performed the controls.
- No Appendix B evaluation, finding, or conclusion was made.
- DOC-0030 generation 2 needs an owner/reviewer decision before promotion or
  rejection. Do not use it as active audit evidence until that decision is
  recorded.
- Continue with the next bounded batch only after this generation decision is
  recorded or the active-generation limitation is explicitly accepted.

## Evidence files

- [DOC-0014 metrics](../../out/2026-10-03/Q03-RUN-20261003-03/metrics.json)
- [DOC-0029 metrics](../../out/2026-10-03/Q03-RUN-20261003-04/metrics.json)
- [DOC-0030 candidate metrics](../../out/2026-10-03/Q03-RUN-20261003-06/metrics.json)
- Candidate diff and detailed run artifacts remain in the local ignored
  `sieving/runs/RUN-20261003-06/` directory.
