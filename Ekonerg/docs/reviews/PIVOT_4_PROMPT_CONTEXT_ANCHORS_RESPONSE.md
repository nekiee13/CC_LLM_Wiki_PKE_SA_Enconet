# PIVOT-4 response: prompt context anchors

## What was checked

Claude's review in `CC_2026-10-04T172044Z_prompt-context-anchors-changes-requested`
identified two separate controls:

1. The active prompt registry must show its owner-authorization provenance.
2. A prompt change after the DOC-0016 golden approval must not silently reuse
   that approval.

## Fix completed: registry provenance

`Ekonerg/sieving/prompts/active.yml` now again contains the existing provenance
comments. They state the owner activation date, the calibration status, and the
candidate prompts. The active slots remain unchanged:

- RULE: `appb_rule_v1`
- DOCUMENT: `appb_document_v2_concept_recall`

Focused check:

```text
python -m pytest Ekonerg/sieving/tests/test_prompt_registry.py -q
exit 0
5 passed in 0.26s
```

This closes only the registry regression. No prompt or run data was changed.

## Decision still required: additive DOCUMENT prompt change

`appb_document_v2_concept_recall.md` contains the later evidence-context-anchor
addition. The DOC-0016 golden fixture and RUN-20261003-40 were approved before
that addition. Therefore the existing approval is not silently extended.

The next action needs an explicit owner decision choosing one of these paths:

- create a new prompt version, calibrate it with a fresh golden fixture, and
  obtain owner approval; or
- approve the additive change as requiring no recalibration, with that decision
  recorded in the controlled approvals record.

Until that decision is recorded, no new promotion is claimed. The prompt still
states that anchors must come from the source and must never be guessed, and it
keeps `candidate_lead` separate from objective evidence.
