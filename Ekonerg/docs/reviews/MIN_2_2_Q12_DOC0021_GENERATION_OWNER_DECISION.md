# Q12 DOC-0021 generation decision

**Status:** Approved by owner on 2026-10-04
**Approval reference:** `Q12-DOC0021-GEN2-PROMOTE-20261004-OWNER`
**Candidate:** `RUN-20261004-42` (generation 2)  
**Document:** `DOC-0021`  
**Prompt:** `appb_document_v2_concept_recall`

## What this decision means

This decision selects whether the corrected Q12 generation replaces the older
`RUN-20261003-37` generation. It does not approve an audit conclusion, a
conformance score, or the final audit report.

## Evidence checked

| Check | Result |
|---|---:|
| Crumbs | 12 |
| Exact quote links | 16/16 (100%) |
| Rejected items | 0 |
| Failed items | 0 |
| Required fields complete | 100% |
| Candidate state | Inactive |

Claude reviewed the candidate and approved it for promotion after the owner
records this generation decision. The review corrected the explanation of the
source wording: `Prijedlog teksta` is in clause 3.3.4 and `Konacnu verziju` is
in clause 3.3.5. The corrected candidate uses the exact clause 3.3.5 source
quote and does not attach the old text to the wrong clause.

## Owner decision

Select one option and complete the record:

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

After `APPROVE`, Codex will add the decision to `manifests/approvals.csv`, run
the controlled promotion command, and verify that the old generation is
superseded without changing source documents or unrelated runs.

## Recorded result

The owner approved the generation decision under the reference above. The
controlled promotion still requires a matching approved golden score; no
promotion is claimed until that independent gate is available.
