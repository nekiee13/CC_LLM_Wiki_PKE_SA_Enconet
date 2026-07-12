# APP_B RULE sieving prompt — v1

Targets `schemas/app_b_json_schema.yml` schema version 1.1 and ADR-0020.

Transform one normative source document into JSON with top-level `document` and `items`.
Preserve every quote verbatim. Use canonical Appendix B criterion ID/name pairs. Each
item must include all source locators and evidence quotes.

Run context placeholder:

```yaml
DOCUMENT_SIDE: "RULE"
AUTHORITY_REFERENCES: <non-empty list supplied by guarded run context>
```

Each authority reference contains `authority_role`, `source_code`, `source_locator`,
`applicability`, and (for Part 21) `applicability_basis`. Appendix B and Part 21 are
GOVERNING; ASME NQA-1 is INTERPRETIVE. Never classify NQA-1 as governing regulation.
