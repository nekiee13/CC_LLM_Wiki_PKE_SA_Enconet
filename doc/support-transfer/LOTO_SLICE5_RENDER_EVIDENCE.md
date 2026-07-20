---
record_type: exact_render_evidence
target: CC_Loto
slice: 5
recorded_at_utc: 2026-07-19T23:59:29Z
target_parent: 85f97d0a75a996e83691d2b103d9724cb3136653
render_timestamp: 2026-07-19T23:57:00Z
---

# CC_Loto Slice 5 exact-render evidence

## Control

- Target branch: `main`.
- Local HEAD and `origin/main`: `85f97d0a75a996e83691d2b103d9724cb3136653`.
- Divergence: `0 0`; porcelain: empty.
- Renderer: [`rendered/render_loto_slice5.py`](rendered/render_loto_slice5.py), SHA-256
  `4B4EA8A1686CADB24809BC892E411847D173C8B5486958F81FB58038F0B2BAF3`.
- Exact byte authority: [`rendered/loto-slice5/AGENTS.md`](rendered/loto-slice5/AGENTS.md).
- Scope: create one Codex-owned root `AGENTS.md`; no other path.
- CC_Loto remained read-only throughout preparation.

## Deterministic renderer

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$lotoTestPython = Join-Path $env:TEMP 'cc-loto-support-venv\Scripts\python.exe'
python doc\support-transfer\rendered\render_loto_slice5.py `
  --timestamp 2026-07-19T23:57:00Z --native-python $lotoTestPython
```

Exit `0`. A second fixed-timestamp run without the optional native argument reproduced 1/1
candidate SHA-256 values. The renderer copies the published target to `%TEMP%\l5-*`, creates only
`AGENTS.md`, validates installed coordination without generating the board, asserts board identity,
checks target paths/facts/semantic anchors, and optionally runs native layers. The real target is
unchanged.

## Exact proposed bytes

| Operation | Target path | SHA-256 | Git object |
|---|---|---|---|
| create, Codex-owned | `AGENTS.md` | `6DE5B8400BD8794DB32B32C38E4F61BC35C45A4FAB15DD9FE6CF7DA2C6DA29E8` | `34b7eb93095022bea137e2a0c2313f356bfa0f28` |

Any path, byte, or parent change invalidates this evidence.

## Pinned target facts and semantics

- `pyproject.toml`: setuptools backend; project `dynamix-lottery` 0.1.0; Python `>=3.11`; package
  discovery under `src` and `.`.
- `run_tests.py`: native `unittest` runner with `core-unit`, `contract`, `state-integrity`, and
  optional layers. The candidate contains no pytest command.
- Target support profile: documentation/code indexes deferred, repo-local workflow skills disabled
  initially, release adapter inventory-only.
- Installed support/navigation/tool paths required by the candidate all exist in the published
  parent, including Loto-native `tools/support/agent_coord.py` and `make_handoff.py`.
- Read-order, ownership, literal validation-state, evidence-first recovery, reviewed-revert, explicit
  destructive-approval, and owner-gate anchors are present.
- Forbidden stale/foreign/unsafe strings and sensitive patterns are absent. No Claude-owned path is
  rendered.

Read-only comparison found a stale opening packaging sentence in Claude-owned `CLAUDE.md`. It is
reported as synchronization pending, not edited or hidden by this candidate.
