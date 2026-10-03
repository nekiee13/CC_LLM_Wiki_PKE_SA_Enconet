# APP_B DOCUMENT sieving prompt — concept-recall candidate v2

Format target: local `schemas/app_b_json_schema.yml` version 1.1. Use the
registered company document and preserve every quote exactly as written. Keep
the chapter, heading, or section locator. Never invent a quote, fact, source,
approval, or audit conclusion.

## Main goal

Collect possible evidence with high recall. A crumb is a traceable clue, not a
compliance decision. A weak but source-supported clue is better than silently
discarding it.

## Two passes over every chapter or chunk

### Pass 1 — Direct controls

Collect clear statements about a role, process step, approval, review,
verification, record, acceptance rule, training activity, or implementation
example. Create a separate item for each distinct control idea.

### Pass 2 — Quality-goal concept sweep

Use `sieving/prompts/appb_concepts.yml`. For every chapter or chunk, ask:

1. What quality goal does this text support?
2. Which Appendix B intent card is a plausible match?
3. Is the match direct, supporting, or only a lead?
4. Can the exact source text and chapter locator support a separate crumb?

Keep every plausible match that has an exact source quote. Do not stop after
the strongest examples. Do not use a fixed maximum number of crumbs. One
source passage may support more than one criterion when the passage contains
different control ideas; make separate crumbs and explain the mapping.

## Strength labels

Put one of these labels at the start of `statement`:

- `objective_control:` — the text gives a concrete control detail;
- `supporting_control:` — the text gives useful indirect control detail;
- `candidate_lead:` — the relationship is plausible but needs later checking.

For an uncertain mapping, add `candidate; verify criterion mapping`. For a
high-level reference without deeper proof, keep the reference as a
`candidate_lead` and say `objective evidence not shown`. Never turn a lead into
a positive audit conclusion.

## Output rules

- Use the canonical Appendix B criterion ID and name.
- Preserve exact quotes and chapter locators.
- Keep DOCUMENT items free of RULE-only authority fields.
- Keep duplicate statements only when their quotes or control meaning differ.
- Reject only items that lack a source quote, locator, or usable criterion link.
- Record the number of direct items, concept-sweep items, merged duplicates,
  and rejected items in the run metrics.

Run context placeholder:

```yaml
DOCUMENT_SIDE: "DOCUMENT"
SOURCE_RULES: null
AUTHORITY_REFERENCES: []
CONCEPT_CARDS: "sieving/prompts/appb_concepts.yml"
RECALL_PASS_COUNT: 2
```
