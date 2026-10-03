# APP_B DOCUMENT sieving prompt — candidate v1

Format target: local `schemas/app_b_json_schema.yml` version 1.1.
This is a candidate template, not an active prompt. Use it only after the
owner-approved intake and run context identify the company document.

Turn one approved company document into JSON with top-level `document` and
`items`. Preserve each quote exactly as it appears in that source. Keep
its chapter, heading, or section locator. Use the local Appendix B criterion
ID/name pairs. Do not create normative authority or RULE-only fields on
the DOCUMENT side. Do not invent a quote, source, or approval. Preserve the
chapter path used by the local chunk store; page numbers are not document
identifiers.

Run context placeholder:

```yaml
DOCUMENT_SIDE: "DOCUMENT"
SOURCE_RULES: null
AUTHORITY_REFERENCES: []
```
