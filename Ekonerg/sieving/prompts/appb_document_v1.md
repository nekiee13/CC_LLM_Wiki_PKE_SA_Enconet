# APP_B DOCUMENT sieving prompt — candidate v1

Format target: local `schemas/app_b_json_schema.yml` version 1.1.
This is the owner-authorized active template for controlled tests. Use it only
after the owner-approved intake and run context identify the company document.

Turn one approved company document into JSON with top-level `document` and
`items`. Preserve each quote exactly as it appears in that source. Keep
its chapter, heading, or section locator. Use the local Appendix B criterion
ID/name pairs. Do not create normative authority or RULE-only fields on
the DOCUMENT side. Do not invent a quote, source, or approval. Preserve the
chapter path used by the local chunk store; page numbers are not document
identifiers.

Recall-first collection rule: collect every plausible Ekonerg control, process
step, role, record, or related statement that may connect to an Appendix B
criterion. Include borderline or indirect wording instead of silently dropping
it. Keep the original quote and chapter/heading path exact. When the mapping is
uncertain, use the closest supported criterion and say `candidate; verify
criterion mapping` in the plain `statement`; never present that candidate as a
proven control. Never invent a quote, source fact, or regulatory conclusion.
Broad collection is preferred; later review may reject or downgrade a
candidate. This is fuzzy interpretation for recall, not permission to alter
source text.

Vendor evidence depth rule: a high-level reference to a regulation, standard,
or QMS process is a lead, not objective proof that the control works. Look in
the vendor document for deeper evidence such as named roles, approval or review
steps, controlled records, registers, forms, reports, outputs, acceptance
criteria, training records, revision history, or examples of implementation.
Collect those details as separate source-supported crumbs when they can be
linked to an Appendix B criterion. If only the high-level reference is present,
keep it as a candidate and state that objective evidence was not shown; do not
silently treat the reference as full alignment.

Run context placeholder:

```yaml
DOCUMENT_SIDE: "DOCUMENT"
SOURCE_RULES: null
AUTHORITY_REFERENCES: []
```
