# MIN-2.2: v3 scope-two golden drafts

## What this records

The owner approved the larger corrected candidate scope (option 2). This note
records the next safe step: making reviewable golden drafts from those candidates.

This is **not** a promotion. The active database generations and dashboard stay
unchanged until the review and approval gates below are complete.

## Candidate inputs

| Document | Candidate file | Items | SHA-256 |
|---|---|---:|---|
| DOC-0016 | `sieving/candidates/repairs-20261005/DOC-0016.json` | 28 | `937c86a47601d9886df970901ed0681dd0d1fa7c9eebf48d783e6aaa904a03b7` |
| DOC-0021 | `sieving/candidates/repairs-20261005/DOC-0021.json` | 21 | `9f8ba03c524b3c145b86ea9df4acd6e94a9d69c1842b9dc87bcac4f142c5a7ba` |

Both files use prompt version `appb_document_v3_context_anchors` and pass
`validate_app_b_json.py --strict`.

## Controlled comparison

Each corrected candidate was compared with its same-document v3 candidate:

- DOC-0016: 28 items before and after; one quote-only correction at
  `Q09-DOC0016-007` (`provjera` → `provjere`) with its locator retained.
- DOC-0021: 21 items before and after; one quote-only correction at
  `Q12-DOC0021-006`, using the exact clause 3.3.5 text and locator.

No item was added or removed by this correction step.

## Pending golden drafts

- `benchmarks/sieving_golden/manifest_document_doc0016_v3_scope2_draft_20261006.yml`
- `benchmarks/sieving_golden/manifest_document_doc0021_v3_scope2_draft_20261006.yml`

The drafts are marked `pending_human_approval` and contain no approval
reference. They are review fixtures, not evidence of approval.

Draft-only scoring was run with `--allow-draft`:

- DOC-0016: 28 found, 0 missed, 0 spurious; `promotion_ready=false` because
  the fixture is not approved.
- DOC-0021: 21 found, 0 missed, 0 spurious; `promotion_ready=false` for the
  same reason.

Score files:

- `out/2026-10-06/doc0016-scope2-draft-score.json`
- `out/2026-10-06/doc0021-scope2-draft-score.json`

## Required next gates

1. Claude or the owner reviews every changed quote and the full candidate diff.
2. The owner records a separate golden-calibration approval for each document,
   or rejects the draft with a reason.
3. `score_sieving.py` is run against the approved fixture and candidate, and the
   score shows no missed or spurious items.
4. A separate owner decision promotes a specific database generation. Promotion
   must still pass downstream-evidence and immutability checks.

Until all four gates pass, the broader scope is only a reviewed candidate.
