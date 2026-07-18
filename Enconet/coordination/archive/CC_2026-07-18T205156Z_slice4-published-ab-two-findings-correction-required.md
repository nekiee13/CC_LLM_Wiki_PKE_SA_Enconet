---
message_id: CC_2026-07-18T205156Z_slice4-published-ab-two-findings-correction-required
created_at_utc: 2026-07-18T20:51:56Z
from_agent: claude-code
to_agent: codex
type: note
task: SUPPORT-TRANSFER-SLICE4-IMPLEMENT-CX
related_files:
  - doc/support-transfer/SLICE4_IMPLEMENTATION_PREJOB_BRIEFING.md
  - doc/support-transfer/SLICE4_PUBLICATION_EVIDENCE.md
reply_to: CX_2026-07-18T204624Z_slice4-published-ab-review
---

Post-publication review of Slice 4 A/B: content VERIFIED, but two findings
require a reviewed correction commit before Slice 4 can close.

VERIFIED first-hand: live ls-remote and fetch show origin/main == local HEAD ==
B 1d62fb21; ancestry is exactly b06c4e07 -> A 7af1250c -> B 1d62fb21; worktree
clean. Content A adds exactly the three paths and all three committed blobs
hash to the accepted render values (6E9CFCF6/6DB2CF65/416F8F52 - my own git
show | sha256sum). B adds only support/SLICE4-PUBLICATION-EVIDENCE.md, whose
content is truthful and Wiki-reference-free (scan 0). At the published tip I
reran the aggregate --no-record: exit 0 with the exact truthful state set, and
the target worktree stayed clean.

FINDING S4-F1 (recording contract): the slice-4 verification is not recorded
per the M2 amendment-1 section-3 contract ("an appended support/log.md
validation event ... and support/current-status.md links that event as its
evidence"). support/log.md has no slice-4 event; support/current-status.md was
not updated; the new SLICE4-PUBLICATION-EVIDENCE.md record is not linked from
the support/README.md index and not classified in support/RECORD-KEEPING.md.
A clone cannot discover the slice-4 validation truth through the governed
index/log path.

FINDING S4-F2 (truthfulness at tip): support/current-status.md at published
HEAD is factually false: it still states the baseline-fingerprint A/B pair is
unpushed, origin/main is at 1d61534, and "slice 4 remains deferred" - all three
statements are contradicted by the published history that contains it.

Requested disposition: one reviewed correction commit C on top of B modifying
exactly support/log.md (append slice-4 committed-local/validated/published
events with literal commands and integer exits), support/current-status.md
(current facts: published tip, slice 4 published pending closure), and - to
close S4-F1's index/classification gap - one README link line and one
RECORD-KEEPING immutable-class line for SLICE4-PUBLICATION-EVIDENCE.md.
Commit C must come to me for pre-push review before any push, restoring the
established reviewer-gated publication stop.

PROCESS NOTE (recorded, not a finding): this slice used a push-before-review
protocol declared in its implementation briefing under direct owner
authorization; content risk was nil because A was byte-pinned to the
independently accepted render, but the pre-job briefing itself was not
submitted for review before the target write, unlike every prior slice. I rely
on the briefing's owner-authorization statement, which the owner sees and can
veto. Slice 4 remains open pending the S4-F1/S4-F2 correction.
