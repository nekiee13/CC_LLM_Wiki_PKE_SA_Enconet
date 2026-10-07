---
name: sieving-run
description: Guide a guarded RULE or DOCUMENT sieving run in the current audit project. Use before a new extraction or re-sieve; do not use it to approve sources or activate prompts.
---

# Sieving run

Read the local `sieving/SIEVING_PLAYBOOK.md`, source approval records, and
`sieving/prompts/active.yml` before any run. A candidate prompt file is not
active just because it exists. Stop if the source, edition, side, or prompt
decision is missing. Never borrow another company's source or script.

1. Confirm the reviewed document and its RULE or DOCUMENT side. RULE needs
   approved authority references; DOCUMENT must not gain normative authority.
2. Create a new RUN-id. Keep prior runs and crumbs unchanged.
3. Validate output strictly before `import_crumbs.py`. A filter or validation
   failure blocks import; unfiltered output is never a fallback.
4. Use the local stages to link quotes and record metrics. An unlinked quote
   is not verified evidence.
5. Keep a re-sieve candidate inactive until its diff, golden score, and human
   decision are recorded. Use `$sieving-tuning` for the promotion decision.

On failure, preserve the run and source evidence. Report failed and not-run
checks plainly. Deposit a reusable run-discipline lesson here only after a
reviewed prompt decision reveals one.
