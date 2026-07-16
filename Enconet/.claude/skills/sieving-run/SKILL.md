---
name: sieving-run
description: Operate controlled RULE or DOCUMENT sieving generations - run context, prompt selection, strict validation and import, quote linking, metrics, and failure handling. Use before starting an initial sieve run or re-sieving any Enconet document.
---

# Sieving Run

1. Read `sieving/SIEVING_PLAYBOOK.md` and `Sieving_method_specification_Guide.md` first.
2. Confirm the controlled document, its side, the active prompt in
   `sieving/prompts/active.yml`, and the authority references. RULE requires valid
   authority objects; DOCUMENT forbids them.
3. Use a new RUN-id for every attempt. Never reuse a completed run, and never edit or
   delete prior crumbs - generations are immutable.
4. Validate the generated JSON strictly (`--strict`) before import. A filter or
   validation error blocks import; never fall back to unfiltered output.
5. Route execution through the canonical `/audit-sieve` or `/audit-resieve` command.
   For re-sieving, the new generation is an inactive candidate: it stays inactive until
   metrics, diff, golden score, and the human decision are complete.
6. Link quotes and inspect exception candidates. Never treat an unlinked quote as verified.
7. Confirm the per-RUN metrics report exists. Record rejected and failed item counts
   truthfully.
8. Stop before promotion; the decision loop belongs to the `sieving-tuning` skill.

On failure, preserve the run and source evidence, report failed or not-run checks as
exactly that, and never export or continue from unfiltered data. Deposit new operating
lessons in this skill when prompt decisions expose reusable run-discipline rules.
