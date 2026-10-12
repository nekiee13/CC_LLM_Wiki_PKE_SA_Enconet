---
record_type: verification_briefing
target: CC_Loto
gate_dependency: M4
target_tip: d5dc65e568ee73d82389e6e1d3fdf24122661adf
prepared_by: codex
independent_reviewer: claude-code
state: awaiting_independent_review
---

# CC_Loto milestone aggregate validation briefing

## Decision boundary

This packet asks Claude Code to reproduce and review the read-only Loto aggregate evidence at the
published Slice 6 tip. Acceptance establishes only the independently reviewed aggregate prerequisite
for a future M4 packet. It does not authorize a target write, rollback action, guidance alignment,
M4 packet approval, tag, release, hosted mutation, or index refresh. M4 remains closed.

## Frozen authority and preconditions

- Target: `C:\xPY\xPrj\CC_Loto` / `nekiee13/CC_Loto`.
- Required live, fetched, and local `main`: `d5dc65e568ee73d82389e6e1d3fdf24122661adf`.
- Required divergence: `0 behind / 0 ahead`; required porcelain: empty.
- Required live tags: zero.
- Installed aggregate: `tools/validate_support.py`, invoked by the support-operator Python with the
  target-requirements Python passed explicitly through `--native-python`.
- Harness: [`rendered/run_loto_aggregate_validation.py`](rendered/run_loto_aggregate_validation.py),
  SHA-256 `6BDB9BDDFB6D3BDBCE8AD12F870F3AF1B12A446FC9FE6A34787D1542042A1113`.

Abort review on tip/divergence/cleanliness drift, a different harness hash, an unexpected tracked
write, a changed BOARD digest, an aggregate/native failure, a count mismatch, or a fail-open probe.

## Exact reproduction

From the Wiki root, with the existing target-requirements interpreter:

```powershell
$native = Join-Path $env:TEMP 'cc-loto-support-venv\Scripts\python.exe'
python doc\support-transfer\rendered\run_loto_aggregate_validation.py `
  --root C:\xPY\xPrj\CC_Loto --native-python $native
git -c safe.directory=C:/xPY/xPrj/CC_Loto -C C:\xPY\xPrj\CC_Loto `
  ls-remote origin refs/heads/main refs/tags/*
```

The harness itself checks local/fetched identity, divergence, clean status before and after,
BOARD byte identity, installed aggregate output, direct coordination validation, both fail-closed
operator probes, and the proportional native layers. Its only writes are isolated product output
and cache paths beneath an OS temporary directory, removed on successful completion.

## Expected evidence

| Check | Required literal result |
|---|---|
| Installed aggregate | exit `0` |
| Coordination | `passed`, 0 errors, 0 warnings |
| Handoff | `not-configured` (bootstrap pointer) |
| Support schemas | `passed`, parsed=1 |
| Focused native support contract | `passed`, 5/5 through installed aggregate |
| Missing native executable | `unavailable`, aggregate exit `1` |
| Product interpreter as support operator | coordination `unavailable`, aggregate exit `1` |
| Native core-unit | 42/42, exit `0` |
| Native contract | 30/30, exit `0` |
| Native state-integrity | 3/3, exit `0` |
| BOARD | SHA-256 unchanged: `A541294B50A11AE56E48DA5735C3BAF67D76264B4CA72BAD8A0F287F37E0A349` |
| Target after run | same HEAD, divergence 0/0, empty porcelain |

Per the accepted Loto profile, optimization-core, integration, webapp, optional, and hosted CI are
not applicable to this support-only aggregate verification and are `not-run`, never `passed`.

## Reviewer response requested

Claude should independently verify the frozen live tip and zero tags, rerun the harness, confirm its
scope is read-only and target-native, and accept or reject the evidence with exact findings. The next
separate candidate after acceptance is scoped rollback evidence; no rollback rehearsal starts from
this request.
