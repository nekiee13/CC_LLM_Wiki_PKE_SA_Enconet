# Enconet quality manual - full v3 sieving

Source: DOC-0003, PK-SUK-001 rev. 9. Run: RUN-20261007-02.

The whole manual was reviewed in direct-control and quality-intent passes,
including its annexes, appointment records and blocks without keyword hits.
All 725 content blocks have a review disposition. No count ceiling was imposed.
Heading text in the coverage note is compact navigation; full source text and
the registered database chapters remain intact.

## Result

| Measure | This run | Live audit total |
|---|---:|---:|
| Vendor crumbs | 399 | 592 |
| Exact source-chapter quote links | 641 | 864 |
| Vendor documents fully sieved | 1 | 2 of 26 |

This run contains 233 direct written controls, 108 supporting controls and 58
candidate leads. Those are the existing v3 extraction labels, not new ratings.
One control may need both an introductory clause and its list entry; quote
count is therefore not independent proof or a basis for raising the score.

[Read the actual collected crumbs and quotes](../sieving/runs/RUN-20261007-02/REVIEW.md)

## Important source clues retained

- Explicit document approval, revision, distribution and obsolete-copy controls.
- Project inputs, control points, verification, validation and change reviews.
- Supplier selection, annual re-evaluation, receipt checks and outsourcing controls.
- Product identity, protection, process validation and quality-record requirements.
- Named QA and management-representative appointments, not just generic roles.
- An urgent-release exception: retain it for checking limits in nuclear work.
- Annex A's IX/XIII scope exclusion, alongside the actual conditional controls.
  Its first sentence says X, while its later list says IX; the ambiguity is a
  lead, not a resolved applicability ruling.
- Referenced procedure/revision clues, including PP-74-01 and differences in
  the listed PP-42-02/PP-62-01 revisions. References do not replace detailed evidence.

No conformance rating or applicability decision was written. The reference
comparison table is retained as a lead and not used as an automatic mapping.

## Integrity and validation

- `python Enconet/scripts/validate_app_b_json.py Enconet/sieving/runs/RUN-20261007-02/generated.json --strict`: exit 0.
- Canonical `audit-sieve`, strict import, exact-run link preview/apply and run
  metrics: each exit 0; 399 imported and 641 linked exactly.
- `python scripts/validate_traceability.py --no-record`, from Enconet: exit 0.
- `python Enconet/scripts/run_all_validations.py --no-record`: exit 0; four checks
  passed at chunked; downstream checks skipped, so strict JSON and traceability
  were also checked directly.
- Independent check: all 864 live links are EXACT, same-document and verbatim
  in their chapter. All 36 incoming files match their reset-time hashes.
- Nuclear QA Plan run's crumb, quote, link and context data hashes matched
  before and after the second import. No earlier evidence was rewritten.

Run JSON, semantic decisions and per-run metrics are in
`sieving/runs/RUN-20261007-02/`. The ingestion ledger records the new batch.
The source and prompt were unchanged. No new framework feature was added here.

## Next

**24 vendor documents remain.** Continue the document-control, quality-record
and training procedures as the next bounded batch. Keep all prior generations
and exact links. No further prompt approval is needed. Regulatory requirement
extraction and later applicability/evaluation gates remain unfinished.
