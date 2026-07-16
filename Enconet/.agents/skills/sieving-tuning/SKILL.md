---
name: sieving-tuning
description: Interpret sieve metrics, generation diffs, and golden-set scores to decide whether to promote, reject, retain, or roll back a prompt generation. Use for every prompt change and every candidate-generation decision.
---

# Sieving Tuning

1. Read `sieving/SIEVING_PLAYBOOK.md`, candidate metrics, and the active-run diff.
2. Investigate zero-crumb criteria, completeness regressions, quote-verification gaps,
   rejected/failed counts, and every changed sample. More crumbs alone is not improvement.
3. Score the exact prompt version against the human-approved golden set. Draft results are
   diagnostic only and cannot support promotion.
4. Promote only when the score is promotion-ready, changes preserve source fidelity,
   exceptions are resolved, and a human approval row exists.
5. Reject regressions; retain the active generation when evidence is inconclusive. Roll back only
   before downstream evaluation and record why.
6. Update prompt CHANGELOG with score and decision, then deposit the reusable lesson in
   `$sieving-run`, `$crumb-quality`, or this skill.

Never delete a generation, overwrite prompt history, equate volume with accuracy, or manufacture
golden approval.
