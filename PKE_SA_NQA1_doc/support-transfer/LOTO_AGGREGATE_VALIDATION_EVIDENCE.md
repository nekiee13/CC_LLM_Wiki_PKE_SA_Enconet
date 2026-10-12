---
record_type: aggregate_validation_evidence
target: CC_Loto
target_tip: d5dc65e568ee73d82389e6e1d3fdf24122661adf
recorded_at_utc: 2026-07-20T02:16:58Z
executed_by: codex
review_state: awaiting_claude
target_write: none
---

# CC_Loto milestone aggregate validation evidence

## Outcome

The installed CC_Loto aggregate passed at the exact published Slice 6 tip. Both unavailable-operator
probes failed closed, direct coordination validation returned 0 errors/0 warnings, and the
proportional native layers passed 42/42, 30/30, and 3/3. The target stayed clean and byte-identical at
its generated BOARD. Live `origin/main` returned the same tip and no tag ref. This evidence is not yet
independent review and does not open M4.

## Identity and immutability

| Fact | Observed |
|---|---|
| Local HEAD | `d5dc65e568ee73d82389e6e1d3fdf24122661adf` |
| Fetched `origin/main` | same |
| Live `refs/heads/main` | same |
| Divergence | `0 0` |
| Live tag refs | zero |
| Porcelain before/after | empty / empty |
| BOARD SHA-256 before/after | `A541294B50A11AE56E48DA5735C3BAF67D76264B4CA72BAD8A0F287F37E0A349` / same |
| Target writes | none |

## Successful execution

The exact two-command block is in
[`LOTO_AGGREGATE_VALIDATION_BRIEFING.md`](LOTO_AGGREGATE_VALIDATION_BRIEFING.md). The harness exited
`0` and asserted every result rather than merely printing it.

| Invocation/result | Exit | Evidence |
|---|---:|---|
| Installed aggregate `--no-record` with explicit native Python | 0 | coordination passed 0/0; handoff not-configured; schemas passed parsed=1; focused support contract passed; optional and hosted not-run |
| Direct `tools/support/agent_coord.py .` | 0 | `validate: 0 error(s), 0 warning(s)` |
| Missing `--native-python` executable | 1 | `native-contract-support: unavailable` |
| Target Python used as support operator | 1 | `coordination: unavailable (No module named 'jsonschema')` |
| `run_tests.py --layer core-unit --verbosity 1` | 0 | `Ran 42 tests`, `OK` |
| `run_tests.py --layer contract --verbosity 1` | 0 | `Ran 30 tests`, `OK` |
| `run_tests.py --layer state-integrity --verbosity 1` | 0 | `Ran 3 tests`, `OK` |
| Live branch/tag query | 0 | one branch ref at the frozen tip; zero tag refs |

The aggregate's focused contract invocation is the installed command
`run_tests.py --layer contract --pattern test_support_*.py --verbosity 1`; its published tests report
5/5. The full contract layer reports 30/30 because it includes the existing contract tests as well.

## Applicability truth

Optimization-core, integration, webapp, optional, and hosted CI were not run. The approved support
profile forbids executing product/model/optimizer/webapp/external flows unless a changed integration
requires them; this read-only support verification changes no integration. Their state is therefore
`not-run`, not `passed` or `skipped`.

## Attempt accounting

The first sandboxed invocation reached and passed the aggregate, direct coordination check, and both
fail-closed probes, then failed core-unit because the child target interpreter was denied permission
to create the designated OS-temporary output directory. Cleanup of that denied directory and Git's
remote transport were denied by the same sandbox boundary. This was an execution-environment failure,
not counted as a product pass. The identical read-only harness was rerun with access to its designated
temporary directory and completed successfully with the results above. No command was silently
omitted and no target write occurred in either attempt.

## Remaining gates

Claude's independent reproduction/acceptance is still required. Scoped rollback proof remains a
separate gated task, guidance alignment remains an owner decision, and the owner-gated M4 packet and
decision remain closed.
