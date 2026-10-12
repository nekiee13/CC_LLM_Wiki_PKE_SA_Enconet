---
record_type: exact_render_evidence
target: CC_Loto
slice: 6
recorded_at_utc: 2026-07-20T01:34:11Z
target_parent: f549b40665c2321ff46168d43c67b2f2f9422bd5
---

# CC_Loto Slice 6 validators/tests — exact-render evidence

## Control

- Target branch: `main`; reviewed parent: `f549b40665c2321ff46168d43c67b2f2f9422bd5`.
- Renderer: [`rendered/render_loto_slice6.py`](rendered/render_loto_slice6.py), SHA-256
  `E72AFD96E3E15AFBBF129202823CB2A40137049918EE001913CBA869258277D8`.
- Exact byte authority: [`rendered/loto-slice6/`](rendered/loto-slice6/).
- Scope: exactly three new shared-neutral target-native paths; all absent at the parent.
- Author/implementer: Codex; independent reviewer: Claude Code.
- CC_Loto remained read-only throughout packet preparation.

## Exact proposed bytes

| Operation | Target path | SHA-256 | Git object |
|---|---|---|---|
| create | `tools/validate_support.py` | `681C3277CD813ED3608930D1D241DEB74085339A8C356D73E7BAB11EE5C4F07A` | `40b44057048fb3083213f040bc5d769e399a42a3` |
| create | `tests/contract/test_support_coordination.py` | `128DEFAC009234085C4D004607A8F9271CCC9EFCBC62CCFCF193B5AB92A19B72` | `75bf30a8a1cbc857bda86bd0ac85111857e38f8f` |
| create | `tests/contract/test_support_handoff.py` | `FCA588D212EDB02789B050C560A0B2783FBFEB7164EC826B36355BDBDEB008F6` | `0fc854e085f19a0d2367bd5290d7e8e4b398bc98` |

The renderer writes explicit LF bytes. Two complete invocations produced the same three SHA-256
values and objects.

## Contract implemented

- Uses Loto-native `tools/` placement and existing layered `unittest` runner.
- Separates the support-operator interpreter from the explicit target-native interpreter.
- Runs only the focused existing-layer pattern in the fast aggregate; no second test framework.
- Enforces exactly `passed`, `failed`, `skipped`, `not-run`, `unknown`, `not-configured`, and
  `unavailable`; applicable `failed`, `unknown`, and `unavailable` states make the aggregate
  nonzero, while deliberate `not-run`, `skipped`, and `not-configured` states do not.
- Accepts explicit `--no-record`; the current implementation is read-only.
- Reports bootstrap handoff `not-configured`, optional layer `not-run`, and hosted CI `not-run`
  rather than implying passes.
- Skips the tracked-digest invariant outside Git and rejects an enclosing Git root before
  `git ls-files`, so a source export neither errors nor receives false confidence.

## Preserved boundaries

The renderer rejects pytest references, unresolved placeholders, sensitive patterns, foreign
workspace/project tokens, `blocked` as a check state, target drift, dirty status, or an already
existing target path. It performs no target write, dependency change, workflow mutation, hosted
action, index refresh, tag, release, product/data/model run, aggregate acceptance, rollback claim,
or M4 transition.
