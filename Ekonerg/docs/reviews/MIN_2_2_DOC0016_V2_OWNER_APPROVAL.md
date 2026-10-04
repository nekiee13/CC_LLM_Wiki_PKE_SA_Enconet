# DOC-0016 Q09 v2 golden-fixture approval

**Status:** Approved by owner on 2026-10-04  
**Approval reference:** `GOLDEN-DOC0016-V2-20261004-OWNER`

## What the owner is approving

This sheet asks the owner to approve the answer key used to check the
corrected Q09 sieving run for `DOC-0016`.

It approves the expected crumbs and their exact source quotes. It does **not**
approve an audit conclusion, a conformity score, or the final Ekonerg audit
report.

## Files reviewed

- Golden fixture: `benchmarks/sieving_golden/manifest_document_doc0016_v2.yml`
- Source document: `raw/PQ07.5-7_r10_Kontrola_zapisa.md`
- Corrected candidate input: `sieving/runs/q09_doc0016_v2_corrected.json`
- Candidate run: `sieving/runs/RUN-20261003-40/`
- Technical review: `docs/reviews/MIN_2_2_DOC0016_V2_GOLDEN.md`

## Verification results

The candidate was checked against the golden fixture:

| Check | Result |
|---|---:|
| Expected crumbs | 12 |
| Found | 12 |
| Missed | 0 |
| Spurious | 0 |
| Exact quote links | 12/12 (100%) |
| Current promotion-ready state | No; owner approval is still missing |

The corrected quote for `Q09-DOC0016-007` uses `provjere`, matching the source.
Items `Q09-DOC0016-011` and `Q09-DOC0016-012` are marked `candidate_lead`.
They are leads for later checking, not proof that an audit control works.

## Scope of the 12 expected crumbs

The answer key covers these Appendix B areas:

- `APP_B_I` — Organization (2 crumbs)
- `APP_B_III` — Design Control (1 candidate lead)
- `APP_B_VI` — Document Control (1 crumb)
- `APP_B_X` — Inspection (1 supporting-control crumb)
- `APP_B_XVII` — Quality Assurance Records (6 crumbs)
- `APP_B_XVIII` — Audits (1 candidate lead)

The statements use the approved concept-recall labels:

- `objective_control`: direct evidence of a stated control;
- `supporting_control`: useful support for a control;
- `candidate_lead`: a lead that needs deeper evidence before any positive audit conclusion.

## Owner decision

Please select one decision and complete the record.

```text
Decision:        [ ] APPROVE   [ ] APPROVE WITH CHANGES   [ ] REJECT

Owner:           ______________________________________
Decision date:   ______________________________________
Decision ref:    ______________________________________

Items to change or reject (write “none” if not applicable):
_______________________________________________________
_______________________________________________________

Owner comments:
_______________________________________________________
_______________________________________________________
```

### Meaning of the choices

- **APPROVE:** all 12 expected crumbs and their scope are accepted.
- **APPROVE WITH CHANGES:** list the exact item IDs and required changes. The
  fixture stays pending until Codex updates it and the owner confirms the new
  version.
- **REJECT:** do not promote this candidate; explain what is wrong.

## What happens after approval

Codex will record the decision in `manifests/approvals.csv`, set the fixture's
`status` and `approval_ref`, and rerun the strict scorer. Promotion of
`RUN-20261003-40` still needs its own recorded generation decision; golden
approval alone does not activate a candidate generation.

## Recorded result

The decision is recorded in `manifests/approvals.csv`. The strict scorer now
reports 12 found, 0 missed, 0 spurious, and `promotion_ready=true`.
