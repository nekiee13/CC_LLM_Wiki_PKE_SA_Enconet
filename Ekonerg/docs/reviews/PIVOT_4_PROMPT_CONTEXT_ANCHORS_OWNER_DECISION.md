# PIVOT-4 prompt-anchor provenance decision

**Status:** Pending owner decision

## Why a decision is needed

The active DOCUMENT prompt `appb_document_v2_concept_recall` was extended with
optional evidence types and source-supported context anchors after the DOC-0016
golden fixture and generation were approved. The extension is additive, but the
old approval refers to the earlier prompt text.

The anchor rule itself is safe: anchors must be stated by the source, are never
guessed, and `candidate_lead` remains separate from objective evidence. The
question is how to control the changed prompt version.

## Owner choices

Choose one:

### A — New prompt version (recommended)

Create a new DOCUMENT prompt version containing the anchor extension. Prepare a
fresh golden calibration, obtain owner approval, and use the new version only
after that gate passes. Existing DOC-0016 approval remains tied to v2.

### B — No recalibration

Record an explicit owner decision that the additive anchor extension does not
change the approved extraction behavior and needs no fresh calibration. Keep
the existing v2 name and approval reference.

## Decision record

```text
Decision:        [ ] A — NEW VERSION   [ ] B — NO RECALIBRATION   [ ] DEFER

Owner:           ______________________________________
Decision date:   ______________________________________
Decision ref:    ______________________________________

Comments:
_______________________________________________________
_______________________________________________________
```

Until this is recorded, no new prompt promotion or golden result is claimed.
