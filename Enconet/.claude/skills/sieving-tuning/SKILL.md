---
name: sieving-tuning
description: Interpret sieve metrics, generation diffs, and golden-set scores to decide whether to promote, reject, retain, or roll back a prompt generation. Use for every prompt change and every candidate-generation decision.
---

# Sieving Tuning

1. Read `sieving/SIEVING_PLAYBOOK.md`, the candidate's metrics report, and its diff
   against the previous active generation.
2. Investigate zero-crumb criteria, completeness regressions, quote-verification gaps,
   rejected/failed counts, and every changed sample. More crumbs alone is never
   improvement.
3. Score the exact prompt version against the human-approved golden calibration set.
   Draft golden results are diagnostic only and can never support promotion.
4. Promote only when the golden score is promotion-ready, the changes preserve source
   fidelity, exceptions are resolved, and a recorded human approval row exists — a
   promotion without human approval is invalid.
5. Reject regressions; retain the existing active generation when evidence is
   inconclusive. Roll back only before downstream evaluation evidence exists, and record
   why.
6. Update `sieving/prompts/CHANGELOG.md` with the score and decision, then deposit the
   reusable lesson in `sieving-run`, `crumb-quality`, or this skill.

Never delete a generation, overwrite prompt history, equate volume with accuracy, or
manufacture golden approval.
