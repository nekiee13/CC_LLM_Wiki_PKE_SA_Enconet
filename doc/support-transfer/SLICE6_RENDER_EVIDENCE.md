# Slice-6 rendered-tree evidence

The exact candidate for CC_FIN content commit A is
`rendered/slice6/.github/workflows/followup-ml-gate.yml`, based on published parent
`9b79b5eff70bda8c04d8b4d3eb578b99a24fac25`.

## Candidate checks

- **passed, exit 0** — renderer produced exactly the one authorized path.
- **passed** — diff is exactly one changed line: `      - master` to `      - main`.
- **passed** — committed-parent CRLF convention is preserved; no whole-file normalization.
- **passed** — pull-request trigger, jobs, steps, existing commands, and GitHub run-ID
  expression are unchanged.
- **passed, exit 0** — installed target coordination CLI validated a disposable exact-parent
  overlay with 0 errors and 0 warnings; BOARD bytes were identical before and after.
- **passed** — sensitive-pattern, forbidden-workspace-reference, required-command, and exact
  inventory assertions completed inside the renderer.
- **passed** — two consecutive renders produced the same SHA-256:
  `4CDB74F51D6690DB96B38A280F64AB3D92C802A37ED5BE57BD83F375E5771664`.
- **passed** — installed PyYAML loaded the candidate without a syntax error.
- **unavailable** — `actionlint` is not installed; no actionlint pass is claimed.
- **observed** — live target was clean and synchronized at the reviewed parent when preparation
  began.

## Hosted-evidence boundary

This candidate corrects the main-push branch filter, but preparation cannot prove a hosted run.
The workflow becomes triggerable on `main` only after the accepted commits are pushed. Hosted
evidence must name the resulting commit-specific terminal run and conclusion; absent, pending,
inaccessible, or failed evidence cannot close Slice 6.

## Pending target checks

No CC_FIN file changed while producing this evidence. Claude Code's pre-write review, immediate
live preflight, staged-object identity, local A/B commits, focused/target/native validation at
A and B, pre-push review, exact push, and post-push hosted evidence remain pending.
