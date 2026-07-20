---
record_type: slice_prejob_briefing
slice: 6
target: CC_Loto
version: 1
recorded_at_utc: 2026-07-20T01:21:41Z
authorized_by: M3_APPROVAL.md items 5-8; T6_VALIDATION_RECOVERY_GATE_CONTRACT.md T6.1
implementer: codex
reviewer: claude-code
target_parent: f549b40665c2321ff46168d43c67b2f2f9422bd5
status: pre-write-review-required
---

# CC_Loto Slice 6 validators/tests — pre-job briefing v1

This packet opens independent pre-write review only. It authorizes no CC_Loto write, commit, push,
dependency/product change, hosted action, aggregate-acceptance claim, rollback claim, or M4 transition.
Codex is implementer and Claude Code is independent reviewer.

## Exact content scope

Content commit A would add exactly three shared-neutral, target-native files from
[`rendered/loto-slice6/`](rendered/loto-slice6/):

1. `tools/validate_support.py` — deterministic read-only support aggregate;
2. `tests/contract/test_support_coordination.py` — aggregate composition and truthful-state tests;
3. `tests/contract/test_support_handoff.py` — bootstrap-handoff and `--no-record` immutability tests.

All three paths are absent at the reviewed parent. No agent-owned guidance, coordination record,
support evidence record, product source, dependency file, workflow, data/model/output, tag, release,
or index is in A.

Exact review inputs:

- [`LOTO_SLICE6_RENDER_EVIDENCE.md`](LOTO_SLICE6_RENDER_EVIDENCE.md)
- [`LOTO_SLICE6_DRY_RUN_EVIDENCE.md`](LOTO_SLICE6_DRY_RUN_EVIDENCE.md)
- [`rendered/render_loto_slice6.py`](rendered/render_loto_slice6.py)
- [`rendered/loto-slice6/`](rendered/loto-slice6/)

## Target-native composition and interpreter boundary

The aggregate follows Loto's accepted D-13 convention (`tools/`, not FIN's `scripts/`) and invokes
the existing runner without reimplementing discovery:

```text
<native-python> run_tests.py --layer contract --pattern test_support_*.py --verbosity 1
```

The support aggregate itself runs in the separate support-operator environment that provides
PyYAML/jsonschema for the installed coordination and handoff modules. `--native-python` selects the
target-requirements interpreter only for `run_tests.py`. This preserves the already accepted
dependency boundary; no repository dependency or pytest assumption is introduced.

Literal aggregate states are limited to the T5 vocabulary. Only `failed` produces a nonzero result.
The current bootstrap handoff is `not-configured`; the installed schema and coordination checks are
`passed`; optional native and hosted CI are `not-run`. `blocked` is never a check result.

## Verified preflight

- Live, local, and fetched CC_Loto `main` equal
  `f549b40665c2321ff46168d43c67b2f2f9422bd5`; divergence `0 0`; porcelain empty.
- Two complete disposable renders reproduced all three SHA-256 values and Git objects.
- Each overlay ran the aggregate with `--no-record`, kept `coordination/BOARD.md` byte-identical,
  stayed clean, and proved an injected applicable failure returns `1`.
- Focused support discovery adds five contract tests. Proportional native layers passed at the
  candidate tree: core-unit 42/42, contract 30/30, state-integrity 3/3, all exit `0`.

## Preflight immediately before content commit A

1. Reverify `HEAD == origin/main == f549b40...`, divergence `0 0`, and empty porcelain.
2. Reverify the three target paths remain absent and the Wiki packet commit is on `origin/main`.
3. Rerun the renderer with the reviewed native interpreter; require the exact hashes/objects.
4. Require Claude's explicit acceptance of the exact three-path scope and interpreter boundary.

Any mismatch is a stop condition.

## Proposed two-commit protocol after acceptance

1. **Content commit A:** stage exactly the three reviewed new files and require each staged Git
   object to match the render authority before committing locally.
2. **Validation at clean A:** run the aggregate `--no-record`, installed coordination validation,
   the focused five-test contract pattern, the three proportional native layers (42/30/3), the
   injected-failure probe, board immutability, and clean-tree checks.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md` with A's full
   identity, literal commands/exits/states, explicit attempt accounting, and the still-closed
   aggregate/rollback/M4 gates.
4. **Validation at clean B:** repeat applicable checks and prove `B^ == A`, exact A/B path sets,
   committed objects, and clean `0/2` state.
5. Keep A and B local until Claude independently reviews the committed objects and explicitly
   authorizes their exact fast-forward push.

Recovery, only on reviewer/owner direction, is a new revert of B followed by A. Reset, force push,
broad cleanup, or restoration of unrelated paths is prohibited.

## Stop conditions

Stop on target drift; dirty status; an existing candidate path; byte/object mismatch; any fourth A
path or third B path; pytest/dependency/product/workflow/agent-owned change; false pass or aggregate
claim; tracked mutation under `--no-record`; stale board; failed focused/native check; sensitive or
foreign content; or reviewer finding. Loto aggregate validation, rollback evidence, the separate
owner decision about guidance alignment, and M4 remain closed.
