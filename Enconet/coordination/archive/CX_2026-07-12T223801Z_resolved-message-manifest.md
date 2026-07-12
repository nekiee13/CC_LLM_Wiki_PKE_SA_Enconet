---
record_type: coordination_resolution_manifest
created_at_utc: 2026-07-12T22:38:01Z
resolved_by: codex
authority: ADR-0018
status: complete
---

# Resolved-message archive manifest (Codex-owned raw-intake and index records)

The Codex-owned records below received explicit Claude Code confirmation and are moved
intact under their original filenames. The Claude-owned confirmation remains untouched
for Claude Code to archive.

| Archived message | Resolution | Confirmation evidence |
|---|---|---|
| `CX_2026-07-12T220232Z_ack-raw-files-bypassed-intake-doorway.md` | The acknowledged raw-intake blocker was resolved by the owner-directed controlled promotion and independently validated | `CC_2026-07-12T223453Z_blocker-closed-adr19-guidance-updated.md` |
| `CX_2026-07-12T221623Z_raw-corpus-promotion-complete.md` | The 20-file RULE corpus promotion, extraction, registry, and validation were independently confirmed at `73f7b2a` | `CC_2026-07-12T223453Z_blocker-closed-adr19-guidance-updated.md` |
| `CX_2026-07-12T221828Z_shared-mcp-index-decision-recorded.md` | Claude-owned guidance was updated to implement the ADR-0019 shared-neutral index contract and its drift check passed | `CC_2026-07-12T223453Z_blocker-closed-adr19-guidance-updated.md` |
| `CX_2026-07-12T222950Z_shared-indexes-refreshed-73f7b2a.md` | The shared-index refresh at clean committed HEAD `73f7b2a` was noted with clean verification | `CC_2026-07-12T223453Z_blocker-closed-adr19-guidance-updated.md` |

The remaining open item is the NQA-1 `source_rules` vocabulary decision before EPIC5;
it is not a request carried by any archived message above.
