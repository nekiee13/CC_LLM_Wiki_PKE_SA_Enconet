# APP_B RULE sieving prompt — candidate v1

Format target: local `schemas/app_b_json_schema.yml` version 1.1.
This is the owner-authorized active template for controlled tests. Use it only
after the owner-approved source intake and run context identify the normative source,
edition, authority role, and applicability.

Turn one approved normative source into JSON with top-level `document` and
`items`. Preserve every quote exactly as it appears in that source. Each
item needs its chapter or section locator and original-language evidence quote. Use
the local Appendix B criterion ID/name pairs. Do not invent source text,
an edition, or an applicability decision.

Run context placeholder:

```yaml
DOCUMENT_SIDE: "RULE"
AUTHORITY_REFERENCES: <non-empty list from approved run context>
```

Recall-first collection rule: collect every plausible Appendix B crumb that is
supported by the source, including borderline or indirect wording. Do not
discard a crumb only because the wording is not a neat mathematical match.
Keep the original quote and chapter/section locator exact. When the mapping is
uncertain, use the closest supported criterion and say `candidate; verify
criterion mapping` in the plain `statement`; never turn uncertainty into a
confirmed audit conclusion. Never invent a quote, source fact, edition, or
applicability decision. Broad collection is preferred; later review may reject
or downgrade a candidate.

Each authority reference carries `authority_role`, `source_code`,
`source_locator`, and `applicability`; Part 21 also needs
`applicability_basis` when that source is approved for the run. Use the
role supplied by the approved context. Never turn an interpretive source
into a governing regulation.
