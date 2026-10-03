---
message_id: CX_2026-10-03T104111Z_controlled-sieving-test-complete
created_at_utc: 2026-10-03T10:41:11Z
from_agent: codex
to_agent: claude-code
type: review_request
task: MIN-2.2
related_files:
  - Ekonerg/docs/reviews/MIN_2_2_CONTROLLED_TEST.md
  - Ekonerg/schemas/sieving_contract.yml
  - Ekonerg/schemas/vocabularies.yml
  - Ekonerg/sieving/prompts/active.yml
  - Ekonerg/out/2026-10-03/metrics.json
  - Ekonerg/out/2026-10-03/RUN-20261003-01/score.json
  - Ekonerg/out/2026-10-03/RUN-20261003-02/metrics.json
  - Ekonerg/out/2026-10-03/RUN-20261003-02/score.json
---

Controlled MIN-2.2 test is complete for one owner-approved governing source and one objective-evidence vendor document.

- RUN-20261003-01 (DOC-0002, RULE): 6 crumbs, 6/6 quote links, score found=6, missed=0, spurious=0, promotion_ready=true.
- RUN-20261003-02 (DOC-0027, DOCUMENT objective evidence): 8 crumbs, 8/8 quote links, score found=8, missed=0, spurious=0, promotion_ready=true.
- Full Ekonerg script+sieving tests: 143 passed and 11 subtests passed.
- The local contract now records owner-approved DOC-0002 as the governing canonical source. The approval record and source hash remain the authority; vocabulary values alone are not approval.

Please review the report and evidence. This proves the controlled path (import, strict validation, quote linking, metrics, and golden scoring), not a full 31-document audit or audit conclusion. Claude approval is still pending.
