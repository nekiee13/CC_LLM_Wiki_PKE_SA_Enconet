---
record_type: exact_render_evidence
target: CC_Loto
slice: 3c
recorded_at_utc: 2026-07-19T23:13:35Z
target_parent: 7100469757128defd3c437d6f9554744e57a6fa1
render_timestamp: 2026-07-19T23:12:00Z
---

# CC_Loto Slice 3c exact-render evidence

## Control

- Target branch: `main`.
- Local HEAD and `origin/main`: `7100469757128defd3c437d6f9554744e57a6fa1`.
- Divergence: `0 0`; porcelain: empty.
- Renderer: [`rendered/render_loto_slice3c.py`](rendered/render_loto_slice3c.py), SHA-256
  `CCFE7B4CBD0139666062E830D6D74B8BFB79164CFBA4177668168070D8DFC7C7`.
- Exact byte authority: [`rendered/loto-slice3c/`](rendered/loto-slice3c/).
- Scope: create `support/README.md`; modify root `README.md` by one added line, zero deletions.
- CC_Loto remained read-only throughout preparation.

## Deterministic renderer

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$lotoTestPython = Join-Path $env:TEMP 'cc-loto-support-venv\Scripts\python.exe'
python doc\support-transfer\rendered\render_loto_slice3c.py `
  --timestamp 2026-07-19T23:12:00Z --native-python $lotoTestPython
```

Exit `0`. A second fixed-timestamp render reproduced 2/2 SHA-256 values. It copied the published
target to a short `%TEMP%\l3c-*` root, overlaid both candidates, ran the installed coordination
validator, asserted board identity, checked local links/placeholders/sensitivity, and ran native
layers. The real target remained unchanged.

## Exact proposed bytes

| Operation | Target path | SHA-256 | Git object |
|---|---|---|---|
| modify, one line | `README.md` | `2986366D27FF0C4F2B225EED28FBB9E00A14879D8D38F9A6ECAD4A2AA1D282E3` | `e40f8bfe56910ecf7d76e1b048bacb659718b411` |
| create | `support/README.md` | `F12E5A6FDCA48D6C3B2E54C2A640B089E0BA1B9BD5BAC3F66652D69749756A44` | `2ffc90e87eec8bcc32c86b1a496185e6126448cc` |

The parent root README SHA-256 is
`4F1A33B8297E8DBF795F9479AE7389DA212019A91EE2DA510544E9C7F2A9D79F` and Git object is
`a79799c3ca4893ff269762089243afa13043fd21`. `git diff --no-index --numstat` returned `1 0`.
Any path, byte, parent, or line-count change invalidates this evidence.

## Target-specific content truth

- The index links only installed support-core paths plus existing Loto product, architecture,
  current-state, progress, roadmap, CI, and packaging authorities.
- It labels the enhanced plan as owner-designated while preserving its `Proposed` header and says
  explicitly that prior TDD progress does not prove enhanced-plan completion.
- Documentation/code indexes remain deferred; no external index/corpus operation is represented.
- Existing CI is integrate-existing-CI-only; no hosted mutation is represented.
- The release adapter is inventory-only. The tag statement is backed by
  `git ls-remote --tags origin`, exit `0`, empty output. GitHub releases are explicitly unavailable
  because `gh` is not installed; no release-count claim is made.
- Native paths and commands use `run_tests.py` and Loto's `tools/` convention. There is no FIN,
  Wiki, private-path, product-data, or unresolved-placeholder content.

The root README addition points to the new index without rewriting product documentation or
creating a nonexistent `docs/README.md`.
