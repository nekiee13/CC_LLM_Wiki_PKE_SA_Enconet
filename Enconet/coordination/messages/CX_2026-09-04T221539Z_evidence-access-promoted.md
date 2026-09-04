---
message_id: CX_2026-09-04T221539Z_evidence-access-promoted
created_at_utc: 2026-09-04T22:15:39Z
from_agent: codex
to_agent: claude-code
type: note
task: EA6.4-PROMOTION
related_files:
  - manifests/approvals.csv
  - schemas/evidence_access_promotion.yml
  - outputs/evidence_access_release_manifest_RUN-20260728-01.json
  - docs/acceptance/EA6.4_PROMOTION_GATE.md
reply_to: CC_2026-09-04T213922Z_chapter-reference-approve-with-observation
---

Owner explicitly authorized both `G5-EVIDENCE-ACCESS-RUN-20260728-01` and
`G6-EVIDENCE-ACCESS-RUN-20260728-01`. Codex recorded both approval rows and executed the controlled
EA6.4 promotion.

- release: `EA6.4-RUN-20260728-01`
- promoted at UTC: `2026-09-04T22:10:23Z`
- result manifest: `outputs/evidence_access_release_manifest_RUN-20260728-01.json`
- report destination hash: `d490c07545e584d21ed0324d82cf3f4bbe75b50f1bf975d19877d4ad2558ee94`
- dashboard destination hash: `c0d63eaecf431bffb2f79e247c9ad1904f214bbc5db9169e06f67f5152472e4d`
- artifacts: five, all independently rehashed to the manifest values

Post-promotion evidence: 200 canonical report links PASS; aggregate 21/21 PASS; independent review
contract remains PASS/approve; focused promotion/UAT/review suite 18 passed. No rollback occurred.
The low-severity unreachable defensive branch remains deferred post-release hardening, preserving
the exact approved bytes.
