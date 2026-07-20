---
record_type: exact_render_evidence
target: CC_Loto
slice: 6
recorded_at_utc: 2026-07-20T01:21:41Z
target_parent: f549b40665c2321ff46168d43c67b2f2f9422bd5
---

# CC_Loto Slice 6 validators/tests — exact-render evidence

## Control

- Target branch: `main`; reviewed parent: `f549b40665c2321ff46168d43c67b2f2f9422bd5`.
- Renderer: [`rendered/render_loto_slice6.py`](rendered/render_loto_slice6.py), SHA-256
  `35C971966D72EFF007E7199BADCE8EE4650077D3C914C28313E724C8D0CAB507`.
- Exact byte authority: [`rendered/loto-slice6/`](rendered/loto-slice6/).
- Scope: exactly three new shared-neutral target-native paths; all absent at the parent.
- Author/implementer: Codex; independent reviewer: Claude Code.
- CC_Loto remained read-only throughout packet preparation.

## Exact proposed bytes

| Operation | Target path | SHA-256 | Git object |
|---|---|---|---|
| create | `tools/validate_support.py` | `00C4CA3B0C428259881E0345833863825D5732F1513326A47B1C62B840C1CA25` | `60523c65a08b4b4ace453ada2effc4f4a8fafc69` |
| create | `tests/contract/test_support_coordination.py` | `5D4BD6F6518897759CDD4237FC2630A0A15BD5894D5F87BBFD9CA1AC1F8623FF` | `541b1d32928e2f46c41b5d08309ebe8a72b814c7` |
| create | `tests/contract/test_support_handoff.py` | `53E5BC1E6673EBD9612FEDF9B8824D07825E9A5E7F088D3AF265AC5DF9308F56` | `18151907ce8a8c81df05029c6bd3944fd72dd480` |

The renderer writes explicit LF bytes. Two complete invocations produced the same three SHA-256
values and objects.

## Contract implemented

- Uses Loto-native `tools/` placement and existing layered `unittest` runner.
- Separates the support-operator interpreter from the explicit target-native interpreter.
- Runs only the focused existing-layer pattern in the fast aggregate; no second test framework.
- Enforces exactly `passed`, `failed`, `skipped`, `not-run`, `unknown`, `not-configured`, and
  `unavailable`; only `failed` makes the aggregate nonzero.
- Accepts explicit `--no-record`; the current implementation is read-only.
- Reports bootstrap handoff `not-configured`, optional layer `not-run`, and hosted CI `not-run`
  rather than implying passes.

## Preserved boundaries

The renderer rejects pytest references, unresolved placeholders, sensitive patterns, foreign
workspace/project tokens, `blocked` as a check state, target drift, dirty status, or an already
existing target path. It performs no target write, dependency change, workflow mutation, hosted
action, index refresh, tag, release, product/data/model run, aggregate acceptance, rollback claim,
or M4 transition.
