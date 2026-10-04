# Q12 DOC-0021 golden-calibration draft

**Status:** Approved by owner on 2026-10-04
**Approval reference:** `GOLDEN-DOC0021-Q12-V2-20261004-OWNER`
**Candidate:** `RUN-20261004-42`  
**Prompt:** `appb_document_v2_concept_recall`

This draft is a separate calibration gate for the owner-approved generation
decision. It does not promote the run or approve an audit result.

## Draft score

The local scorer compared the draft answer key with the corrected candidate:

- Found: 12
- Missed: 0
- Spurious: 0
- Exact quote links in candidate: 16/16
- `promotion_ready`: false because the fixture is not owner-approved

Command:

```text
python Ekonerg/scripts/score_sieving.py \
  --golden benchmarks/sieving_golden/manifest_document_doc0021_q12_v2.yml \
  --actual sieving/runs/q12_doc0021_corrected.json \
  --output docs/reviews/MIN_2_2_Q12_DOC0021_GOLDEN_SCORE_DRAFT.json \
  --allow-draft
exit 0
```

## Files

- Draft fixture: `benchmarks/sieving_golden/manifest_document_doc0021_q12_v2.yml`
- Score: `docs/reviews/MIN_2_2_Q12_DOC0021_GOLDEN_SCORE_DRAFT.json`
- Candidate: `sieving/runs/q12_doc0021_corrected.json`

## Owner decision

```text
Decision:        [ ] APPROVE   [ ] APPROVE WITH CHANGES   [ ] REJECT

Owner:           ______________________________________
Decision date:   ______________________________________
Decision ref:    ______________________________________

Comments:
_______________________________________________________
_______________________________________________________
```

Only after this fixture is approved can the controlled promotion command use
the score as its independent golden gate.

## Recorded result

The owner approved this 12-crumb answer key under the reference above. The
strict score and generation promotion are recorded separately below.

Strict score: `MIN_2_2_Q12_DOC0021_GOLDEN_SCORE.json` reports found=12,
missed=0, spurious=0, and `promotion_ready=true`.

Promotion: `RUN-20261004-42` is now active under
`Q12-DOC0021-GEN2-PROMOTE-20261004-OWNER`; `RUN-20261003-37` is superseded.
