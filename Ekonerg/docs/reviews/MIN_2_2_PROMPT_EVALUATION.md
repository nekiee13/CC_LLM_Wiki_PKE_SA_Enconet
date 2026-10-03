# MIN-2.2 prompt evaluation packet

## Purpose

This packet lets the owner and reviewer inspect the two prompt candidates before
any real Ekonerg sieving starts. Both prompts are inactive. They cannot create a
sieve run while `sieving/prompts/active.yml` has an empty `active` mapping.

## Candidate files

| Side | Candidate | File | Status |
|---|---|---|---|
| RULE | `appb_rule_v1` | [`sieving/prompts/appb_rule_v1.md`](../../sieving/prompts/appb_rule_v1.md) | Candidate only |
| DOCUMENT | `appb_document_v1` | [`sieving/prompts/appb_document_v1.md`](../../sieving/prompts/appb_document_v1.md) | Candidate only |

The candidate list is also visible in
[`sieving/prompts/active.yml`](../../sieving/prompts/active.yml). `active: {}`
is intentional and is not an approval.

## What the owner should check

### RULE prompt

- Does it preserve every regulatory quote exactly?
- Does each item include a locator and original-language quote?
- Does it keep 10 CFR Appendix B as the governing rule?
- Does it use ASME NQA-1 only as the approved interpretation role?
- Does it avoid inventing an edition, date, applicability decision, or text?

### DOCUMENT prompt

- Does it extract Ekonerg controls without calling them regulatory rules?
- Does every quote point to a heading, page, or other usable locator?
- Does it keep the company document separate from governing authority?
- Does it avoid treating a policy statement as proof that staff used the control?
- Does it preserve missing images or missing pages as evidence limits?

## Decision record

Choose one decision for each candidate:

1. **Approve** — record the approval reference and activate the version in
   `active.yml`.
2. **Revise** — describe the required change; keep `active: {}`.
3. **Reject** — record the reason; keep `active: {}`.

Activation is a separate step. A candidate file alone never authorizes real
sieving. After activation, run a small reviewed test set before processing all
31 documents.

## Current gate

- Incoming source set: G1 approved, 31 files.
- Extraction and chunking: complete, 411 validated chunks.
- Real crumbs: none created yet.
- Active prompt: none.
- Next required decision: owner/reviewer prompt approval and activation.
