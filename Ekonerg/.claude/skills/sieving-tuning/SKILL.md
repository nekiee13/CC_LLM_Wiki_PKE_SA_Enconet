---
name: sieving-tuning
description: Compare local sieve generations, prompt metrics, and a human-approved golden set before a prompt decision. Use for candidate promotion, rejection, retention, or rollback.
---

# Sieving tuning

Read `sieving/SIEVING_PLAYBOOK.md`, the candidate metrics, the active-run diff,
and the local golden-set status. Check zero-crumb criteria, quote links,
rejected or failed items, and changed samples. More crumbs alone do not
prove better quality.

Score the exact prompt version only against a human-approved golden set.
A pending or draft set is diagnostic, not promotion-ready. Promotion also
needs source fidelity, resolved exceptions, and a recorded human approval.
If evidence is unclear, retain the active generation. Reject regressions;
roll back only within the allowed local workflow and record the reason.

Do not delete a generation or rewrite prompt history. Record the decision
and score in the local prompt CHANGELOG, then deposit a reusable lesson in the
`sieving-run`, `crumb-quality`, or this skill. Never invent an approval.
