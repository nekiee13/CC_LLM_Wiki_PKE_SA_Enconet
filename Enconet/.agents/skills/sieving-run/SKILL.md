---
name: sieving-run
description: Operate controlled RULE or DOCUMENT sieving generations, including run context, prompt selection, strict import, quote linking, metrics, and failure handling. Use before starting an initial sieve run or re-sieving any Enconet document.
---

# Sieving Run

1. Read `sieving/SIEVING_PLAYBOOK.md` and `Sieving_method_specification_Guide.md`.
2. Confirm the controlled document, side, active prompt in `sieving/prompts/active.yml`, and
   authority references. RULE requires valid authority objects; DOCUMENT forbids them.
3. Use a new RUN-id. Never reuse a completed run or edit prior crumbs.
4. Validate generated JSON strictly before import. A filter or validation error blocks import.
5. Run the canonical `audit-sieve` or `audit-resieve` dispatcher. For re-sieving, keep the
   candidate inactive until metrics, diff, golden score, and human decision are complete.
6. Link quotes and inspect exception candidates. Never treat an unlinked quote as verified.
7. Confirm per-RUN metrics exist. Record failures and rejected item counts truthfully.
8. Stop before promotion; use `$sieving-tuning` for the decision loop.

On failure, preserve run and source evidence, report failed/not-run checks, and do not fall back
to unfiltered output. Deposit new operating lessons here when prompt decisions expose reusable
run-discipline rules.
