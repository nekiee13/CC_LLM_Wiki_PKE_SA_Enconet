# MIN-2.2 prompt evaluation packet

## Purpose

This packet lets the owner and reviewer inspect the two prompt candidates before
real Ekonerg sieving starts. Both prompts are now active by explicit owner
instruction. Claude review and golden calibration approval are still pending.

## Candidate files

| Side | Candidate | File | Status |
|---|---|---|---|
| RULE | `appb_rule_v1` | [`sieving/prompts/appb_rule_v1.md`](../../sieving/prompts/appb_rule_v1.md) | Active; owner-authorized |
| DOCUMENT | `appb_document_v1` | [`sieving/prompts/appb_document_v1.md`](../../sieving/prompts/appb_document_v1.md) | Active; owner-authorized |

The candidate and active mappings are visible in
[`sieving/prompts/active.yml`](../../sieving/prompts/active.yml). Activation
records owner authorization; it does not equal Claude review or golden approval.

## What the owner should check

### RULE prompt

- Does it preserve every regulatory quote exactly?
- Does each item include a locator and original-language quote?
- Does it keep 10 CFR Appendix B as the governing rule?
- Does it use ASME NQA-1 only as the approved interpretation role?
- Does it avoid inventing an edition, date, applicability decision, or text?

### DOCUMENT prompt

- Does it extract Ekonerg controls without calling them regulatory rules?
- Does every quote point to a chapter, heading, section, or other usable locator?
- Does it keep the company document separate from governing authority?
- Does it avoid treating a policy statement as proof that staff used the control?
- Does it preserve missing images or missing chapters/sections as evidence limits?

## Decision record

Choose one decision for each candidate:

1. **Approve** — record the approval reference and activate the version in
   `active.yml`.
2. **Revise** — describe the required change; keep `active: {}`.
3. **Reject** — record the reason; keep `active: {}`.

Activation is now recorded as owner authorization. It does not equal Claude
review or golden approval. Run a small reviewed test set before processing all
31 documents.

## Storage contract

The database preserves chapter structure, not page IDs:

- `document_chunks.heading_path` is the canonical chapter/heading path.
- `crumb_sources.source_heading_path` carries that path into evidence records.
- `source_locator` identifies the chapter or section text used by a crumb.

Page numbers may appear as optional source metadata, but they are never the
document key and must not replace the chapter path.

## Golden calibration, in simple terms

Golden calibration is a small answer key. We choose a few source passages and
write down the crumbs that a good sieve should return. The tool compares a test
run with that key. A match means the shape and wording are close; it does not
prove that the whole audit is correct.

The owner also set a recall-first rule for sieving: keep plausible and
borderline crumbs when the source supports them. Preserve the exact quote and
chapter path, and mark an uncertain criterion mapping as a candidate for later
review. This widens collection without inventing facts or calling a candidate
an audit conclusion.

Fresh Ekonerg draft keys are available for review:

- [`manifest_rule.yml`](../../benchmarks/sieving_golden/manifest_rule.yml) —
  two Appendix B rule crumbs.
- [`manifest_document.yml`](../../benchmarks/sieving_golden/manifest_document.yml)
  — two Ekonerg manual crumbs.
- [`manifest_document_corrective.yml`](../../benchmarks/sieving_golden/manifest_document_corrective.yml)
  — one corrective-action procedure crumb.

All three are marked `pending_human_approval`. They contain Ekonerg source
quotes only; no Enconet answer key or approval was copied.

## Current gate

- Incoming source set: G1 approved, 31 files.
- Extraction and chunking: complete, 411 validated chunks.
- Local sieving stages: complete; `sieve_generation.py` is now copied into
  Ekonerg and guarded by a regression test. The harness no longer reports a
  missing local stage.
- Real crumbs: none created yet.
- Active prompts: `appb_rule_v1` and `appb_document_v1`, activated by explicit
  owner instruction on 2026-10-03.
- Golden drafts: prepared, but not approved.
- Next required step: run a small controlled test set; do not process all 31
  documents until the test output and golden drafts are reviewed.

## Readiness check (2026-10-03)

- `python -m pytest Ekonerg/scripts/tests -q` — PASS, 57 tests.
- `python -B Ekonerg/scripts/validate_sieving_harness.py --allow-pending-claude`
  — should pass with a pending-golden note after activation.
- Golden calibration remains pending human approval. No real sieve run was
  started; activation only unlocked controlled test runs.
