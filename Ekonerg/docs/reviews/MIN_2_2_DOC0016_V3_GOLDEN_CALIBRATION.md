# MIN-2.2 DOC-0016 v3 golden calibration

**Status:** Pending owner golden-fixture approval and Claude review

## What changed

The owner selected PIVOT-4 Option A. The source-context-anchor extension is
therefore versioned as `appb_document_v3_context_anchors`. The earlier v2
approval remains tied to the exact v2 prompt text.

The v2 DOC-0016 candidate `RUN-20261004-44` was rejected under
`PIVOT-4-OPTION-A-20261004-OWNER`. No approved v2 result was changed. A new
candidate was then created as `RUN-20261004-49`.

## Calibration result

| Check | Result |
|---|---:|
| Candidate run | `RUN-20261004-49` |
| Prompt | `appb_document_v3_context_anchors` |
| Crumbs | 12 |
| Exact quote links | 12/12 (100%) |
| Golden found | 12 |
| Golden missed | 0 |
| Golden spurious | 0 |
| Promotion ready | No — fixture has no owner approval yet |

The fixture contains the same 12 reviewed DOC-0016 control ideas plus the
source-stated context fields. It does not turn candidate leads into positive
audit conclusions. Anchors remain source-supported only and are never guessed.

## Owner gate

Please review and approve the fixture if correct. Suggested approval reference:
`GOLDEN-DOC0016-V3-20261004-OWNER`.

Approval is a separate gate from the earlier Option A decision. Until it is
recorded, v3 remains a candidate and is not active.

## Artifacts

- Prompt: `sieving/prompts/appb_document_v3_context_anchors.md`
- Candidate input: `sieving/DATA/production/2026-10-04/q09_doc0016_v3_calibration.json`
- Run metrics: `sieving/runs/RUN-20261004-49/metrics.json`
- Golden fixture: `benchmarks/sieving_golden/manifest_document_doc0016_v3.yml`
- Golden score: `docs/reviews/MIN_2_2_DOC0016_V3_GOLDEN_SCORE_DRAFT.json`
