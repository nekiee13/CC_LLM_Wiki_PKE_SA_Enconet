---
record_type: exact_render_evidence
target: CC_Loto
slice: cc-guidance
recorded_at_utc: 2026-07-20T00:47:12Z
target_parent: fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e
render_timestamp: 2026-07-20T00:45:00Z
---

# CC_Loto Claude-owned guidance correction — exact-render evidence

## Control

- Target branch: `main`.
- Local HEAD and `origin/main`: `fd7e96fd4a7569a7aeeddfff04e8d2c4ec7ddf7e` (closed Slice 5 tip).
- Divergence: `0 0`; porcelain: empty.
- Renderer: [`rendered/render_loto_cc_guidance.py`](rendered/render_loto_cc_guidance.py), SHA-256
  `9FF0D218D1816A513E7890F1F5E8EEA1FC89D55E8BA4697FCD09B82354BACFDF`.
- Exact byte authority: [`rendered/loto-cc-guidance/CLAUDE.md`](rendered/loto-cc-guidance/CLAUDE.md).
- Scope: one Claude-owned modification of root `CLAUDE.md`; no other path.
- Author/implementer: claude-code (owner of this file). Reviewer: codex.
- CC_Loto remained read-only throughout preparation.

## Deterministic renderer

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$lotoTestPython = Join-Path $env:TEMP 'cc-loto-support-venv\Scripts\python.exe'
python doc\support-transfer\rendered\render_loto_cc_guidance.py `
  --timestamp 2026-07-20T00:45:00Z --native-python $lotoTestPython
```

Exit `0`. A second fixed-timestamp run reproduced the candidate with zero SHA-256 differences.
The candidate is *derived from the reviewed parent blob* by a single verified string replacement,
so every unrelated byte is preserved by construction rather than by re-authoring.

## Exact proposed bytes

| Operation | Target path | SHA-256 | Git object |
|---|---|---|---|
| modify, Claude-owned | `CLAUDE.md` | `3D4DCF9F0ADD76827D1F806BA0BBFAB259D261B820BBA9E60C3D02BAFAB042C9` | `3edd87504e76a97d8ba46ecf40e81b8ad894299f` |

The reviewed parent `CLAUDE.md` Git object is `be29ac97bf0307bfc0128e9c2120010bb921993a`, which is
also the object published at Slice 3c and unchanged by Slice 5. The parent blob is LF-normalized
(0 CR / 99 LF); the candidate is rendered with explicit LF bytes. `git diff --no-index --numstat`
against the parent blob returns `3 2`.

## The corrected defect

The parent's opening description contradicted both the repository and its own later sections:

```
-portfolio optimize) over 7 positional lottery series (`TS_1`..`TS_7`). Pure Python, run
-directly from the repo root with `sys.path` bootstrapping; no packaging or `requirements.txt`.
+portfolio optimize) over 7 positional lottery series (`TS_1`..`TS_7`). Pure Python, packaged
+with setuptools as `dynamix-lottery` (`pyproject.toml`, Python `>=3.11`) and normally used as
+an editable install; `requirements.txt` and `requirements.lock` are the dependency authorities.
```

Every replacement claim is asserted by the renderer against the reviewed parent blobs before the
candidate is produced: `pyproject.toml` declares `setuptools.build_meta`, project `dynamix-lottery`,
and `requires-python >=3.11`; `requirements.txt` and `requirements.lock` both exist at the parent.
The renderer refuses to emit a candidate if any of those facts drift.

The stale sentence was also self-contradictory: the same file already states "**The project is an
installable package; entrypoints live inside it**", prescribes `pip install -e .`, and explicitly
prohibits reintroducing per-file `sys.path.insert` bootstrapping. The correction removes the
contradiction and preserves those pre-existing statements, which the renderer asserts are retained.

## Preserved boundaries

- Codex-owned `AGENTS.md` is byte-identical to its published object in the disposable overlay; this
  slice touches no Codex infrastructure.
- The candidate asserts no synchronization between `CLAUDE.md` and `AGENTS.md`; the renderer fails
  on such a claim. See the briefing for what remains before the pair could be called synchronized.
- No shared-neutral support record, coordination state, generated board, product source, data,
  dependency file, workflow, tag, or release is in scope.
