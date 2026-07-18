---
record_type: support_transfer_prejob_briefing
slice: 6
version: 1
recorded_at_utc: 2026-07-18T15:07:34Z
authorized_by: M1_APPROVAL.md item 8 and M2_APPROVAL.md
implementer: codex
reviewer: claude-code
target_parent: 9b79b5eff70bda8c04d8b4d3eb578b99a24fac25
status: pre-write-review-required
---

# Slice-6 pre-job briefing — CC_FIN main-branch workflow trigger

## Authority, roles, and exact boundary

The owner assigned Codex as implementer and Claude Code as independent reviewer. Slice 6
modifies exactly one existing CC_FIN file and one line:

```diff
 .github/workflows/followup-ml-gate.yml
-      - master
+      - main
```

No other target path or hosted-governance mutation is authorized. The reviewed clean parent
is published Slice 5 evidence commit `9b79b5eff70bda8c04d8b4d3eb578b99a24fac25`.
Rollback, if separately approved after a failure, is a reviewed revert of named Slice 6
commits to that parent, never reset, cleanup, or history rewriting.

## Exact rendered proposal

`rendered/slice6/` contains the final workflow blob. `render_slice6.py` reads the workflow
directly from the reviewed parent, preserves its committed CRLF convention, and stops unless
the branch block is unique and the only differing line is exactly `master` to `main` at the
known position. It also proves that the pull-request trigger, every existing job/step/command,
and the `${{ github.run_id }}` expression remain present.

The candidate SHA-256 reproduced identically on two consecutive renders:
`4CDB74F51D6690DB96B38A280F64AB3D92C802A37ED5BE57BD83F375E5771664`.
PyYAML is installed and loaded the candidate without a syntax error. `actionlint` is not
installed, so no actionlint result is claimed.

## BOARD non-impact

The workflow path is not an input to the generated coordination board. The renderer archives
the exact reviewed parent into a disposable tree, overlays the one candidate file, runs the
installed target validator without board generation, and compares raw BOARD bytes. Validation
returned exit 0 with 0 errors and 0 warnings and BOARD was byte-identical. Slice 6 therefore
has no BOARD modification and needs no scope amendment.

## Preflight and local validation contract

Immediately before target write, require the live remote, `origin/main`, and local HEAD all
equal the reviewed parent, divergence `0 0`, empty porcelain, unchanged parent workflow blob,
and a fresh deterministic render. Stop on drift, line-ending change, more than one diff line,
scope expansion, sensitive content, runtime artifact, or validation change.

At clean content A and clean evidence B, run and record separately:

1. `$env:PYTHONDONTWRITEBYTECODE='1'; python scripts/agent_coord.py .`
2. `python -m py_compile scripts/followup_ml.py scripts/followup_ml_scope_audit.py scripts/followup_ml_parity.py scripts/followup_ml_ci_parity_gate.py src/followup_ml/draft.py src/followup_ml/scope_audit.py`
3. `python -m pytest tests/test_followup_ml_parity_tool.py tests/test_followup_ml_policy.py tests/test_followup_ml_scope_audit.py -q`
4. `python scripts/followup_ml_ci_parity_gate.py --round-id 26-1-06 --round-id 26-1-09 --round-id 26-1-11`
5. `python -m pytest tests/test_infra.py::test_fetch_data_parses_comma_thousands_numeric_fields -q`
6. `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --continue-on-collection-errors -q --tb=no --junitxml="$env:TEMP\fin_slice6_A.xml"` at A, with `fin_slice6_B.xml` at B.

Commands 1–5 must exit 0. Command 6 is expected to exit 1 only for the normative 54-tuple
baseline: 54 expected/actual, 0 new, 0 gone, 0 mutated, and A-to-B identity. BOARD must remain
the same object as the parent.

## Two-commit target protocol

1. **Content commit A:** replace exactly the workflow file from the rendered tree; stage only
   that path; require the staged object to equal the reviewed rendered object and the cached
   diff to contain exactly one deletion/addition pair (`master`/`main`); commit locally.
2. Run the complete local validation contract at clean A.
3. **Evidence commit B:** modify only `support/log.md` and `support/current-status.md`, recording
   A's full SHA and committer UTC, literal commands and integer exits, exact focused results,
   target 0/0, BOARD identity, and native tuple evidence. Do not claim hosted success.
4. Run the complete local contract at clean B, require A-to-B tuple identity and exact A/B
   ancestry/scope, then submit both local commits for Claude's independent pre-push review.
5. Only after reviewer acceptance, push exactly A/B as a fast-forward. The main-push workflow
   becomes triggerable only at this point; a local render or commit is not hosted evidence.

## Hosted evidence after push

Existing CI is hosted evidence after push under the accepted FIN native-validation profile.
After publication, identify the `followup-ml-gate` run for commit B and wait for its terminal
state. Record the exact commit, workflow/run identity, URL when available, terminal state,
conclusion, and job/check results in immutable coordination evidence. Report `passed` only for
a terminal successful conclusion. If the run is absent, inaccessible, queued, or unavailable,
record that literal state and keep Slice 6 open; if it fails, record failure and stop for reviewed
disposition/recovery. No third target commit or corrective hosted mutation is implied.

Any byte, scope, authority, validation, baseline, BOARD, ownership, reviewer, remote, or hosted
evidence defect is a stop. Skipped, unavailable, pending, or failed checks are never relabeled
as passed.
