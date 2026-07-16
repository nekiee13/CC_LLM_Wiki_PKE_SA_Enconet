# Support-transfer intentional difference register v1.0

Common semantics are fixed: authority is explicit, evidence is immutable where required, current
status is replaceable, validation is truthful, handoffs are clone-complete, messages are owned and
immutable, and recovery is scoped. The differences below adapt implementation without weakening
those semantics.

| ID | Difference | Rationale | Owner | Verification | Reconsider when |
|---|---|---|---|---|---|
| D-01 | FIN publishes first; Loto waits for M4 | Sequential pilot limits two-repo blast radius | Owner | Gate and claim checks | FIN pilot accepted or transfer strategy changes |
| D-02 | FIN uses pytest/Ruff/CPI applicability; Loto uses `run_tests.py` layers | Preserve native validation contracts | Project maintainer | Command exit codes and CI | Native test architecture changes |
| D-03 | FIN index module enabled; Loto deferred | FIN is much larger and has vendor/data exclusions | Index owner | Profile validation and committed-state refresh claim | Loto navigation cost or corpus grows materially |
| D-04 | FIN integrates existing freshness ledger and feature ADRs; Loto integrates U7 | Existing governance differs | Documentation owner | Support index reference audit | Product documentation governance changes |
| D-05 | FIN has Codex guidance to correct; Loto has Claude guidance to correct | Infrastructure ownership boundary | Respective agent | Guidance drift and ownership checks | Counterpart guidance is introduced or ownership changes |
| D-06 | FIN may correct one CI branch filter after separate approval; Loto has no planned workflow edit | Only FIN has proven `master`/`main` mismatch | Owner + workflow owner | Diff review and hosted run | M1 defers correction or workflow changes upstream |
| D-07 | FIN support tests may use pytest discovery; Loto tests must live in an existing `run_tests.py` layer | Avoid undiscovered tests and new runner dependency | Test owner | Collection/listing evidence | Loto adopts a different runner |
| D-08 | FIN has explicit Cockpit A-F non-regression note; Loto has no equivalent | Preserve user-confirmed FIN product capability | Product owner | Product-plan link and focused regression selection | FIN cockpit architecture changes |
| D-09 | FIN tracked datasets/vendor corpus and Loto `DATA.csv` have target-specific exclusions | Different product-data layouts | Data owner | Index/exclusion audit | Product data governance changes |
| D-10 | Both omit Wiki sieve, ingestion, raw-source, phase engine, golden-loop, and audit adapters | They are Wiki-domain behavior, not portable support core | Owner | Planned-path manifest contains none | A target proves an equivalent need |
| D-11 | Both initially omit repo-local skills and formal state machines | Simplicity and no demonstrated workflow frequency | Owner | Module table and path audit | Repetition/error data justifies a module |
| D-12 | Release adapters inventory only; package versions remain untouched | Transfer is not a product release | Product owner | No tags/releases/version diffs | Owner initiates release work |

## Common non-negotiable checks

- No target wording may redefine `passed`, `skipped`, `blocked`, or `unavailable`.
- Neither target may treat a current-status view as immutable evidence or an event log as editable.
- Agent ownership cannot be bypassed for convenience.
- Product plans, requirements, data, and product-state records are linked, not copied.
- A disabled module is a deliberate omission, not an incomplete core requirement.
