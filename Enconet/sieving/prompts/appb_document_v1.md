# APP_B DOCUMENT sieving prompt — v1

Targets `schemas/app_b_json_schema.yml` schema version 1.1 and ADR-0020.

Transform one Enconet evidence document into JSON with top-level `document` and
`items`. Preserve every quote verbatim and retain every source locator. Use canonical
Appendix B criterion ID/name pairs; do not create normative authority objects.

Run context placeholder:

```yaml
DOCUMENT_SIDE: "DOCUMENT"
SOURCE_RULES: null
AUTHORITY_REFERENCES: []
```
