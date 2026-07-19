---
record_type: exact_render_evidence
target: CC_Loto
slice: 2
recorded_at_utc: 2026-07-19T21:12:37Z
target_parent: 496800dcf499f5bde21e52e1ea6abe917ca22e4f
render_timestamp: 2026-07-19T21:10:00Z
---

# CC_Loto Slice 2 exact-render evidence

## Control

- Target branch: `main`.
- Local HEAD and `origin/main`: `496800dcf499f5bde21e52e1ea6abe917ca22e4f`.
- Divergence: `0 0`; porcelain: empty.
- Renderer: [`rendered/render_loto_slice2.py`](rendered/render_loto_slice2.py), SHA-256
  `BD15CA1C014D631D788D748EF05E483CD2ED7C898FD2D25BCB05C7A623815E04`.
- Exact byte authority: [`rendered/loto-slice2/`](rendered/loto-slice2/).
- Scope: 14 creates only. All 14 target paths are absent; collision count is zero.
- CC_Loto was read-only throughout preparation.

## Deterministic render

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python doc\support-transfer\rendered\render_loto_slice2.py --timestamp 2026-07-19T21:10:00Z
```

Exit code `0`; a second fixed-timestamp run produced `0` SHA-256 differences. Disposable target
validation reported `0 errors, 0 warnings`; inventory was exactly 14 files; the generated board
truthfully reports no active records, archive count zero, and `HANDOFF.md missing`.

## Exact proposed bytes

| Target path | SHA-256 |
|---|---|
| `coordination/BOARD.md` | `EBB37870480F49E469A56CED3F993CF5FAE8B0B795BBB036DC0F8B26E415355D` |
| `coordination/TEAM_PROTOCOL.md` | `B5B8DD14CF2CBB506DC91AB45BB65BFC422F68E34C2E8F2097F1A8F7D3B5326D` |
| `coordination/archive/README.md` | `F0EA3F7ED52CFE6EF0F8A3398AAE71148FEEB847BB8C0CEE4097249F161E06A7` |
| `coordination/claims/README.md` | `F5EFAE4D4AB82DA04EF236F74B070EFCDE30FA2A20EFBCA17B6263A278DD47AF` |
| `coordination/messages/README.md` | `919DB6D53377CCBA7428EB70320FE1408285D8B7411E4A1D883DB43A2CC61922` |
| `coordination/schemas/claim.schema.json` | `E0217A277E3358B552E3F228871B8535482D0D4B84C77562CDDB7B617E538123` |
| `coordination/schemas/message.schema.json` | `78AF6F1181B635C72047E80AF9E2A5C7717F11E522AC4364E4220A8263999B45` |
| `coordination/schemas/resolution-manifest.schema.json` | `38367856F0CF05BC7D8DCA19D36D2B2D4D7E3C940827511CFAD4D5906DDBBBC3` |
| `coordination/templates/claim.template.yml` | `1C68E8297AD1C68A0B8ED3D3226915C596FCCBE90352CBB584A8E2AC260EEF02` |
| `coordination/templates/guidance-semantics.template.md` | `0DB454EA9077F6B39BE6969F592662F7C1028B93797CF62761B700708DDED9E1` |
| `coordination/templates/message.template.md` | `7DE8EBF6D7371D02E1F653D748BFB10177546D3C459AEDB7E28C4F8D21920287` |
| `coordination/templates/resolution-manifest.template.md` | `F7B961601C07E47D194C72E6C5F45516EB0223381E27B1BC3194D0CA694F3EB9` |
| `tools/support/agent_coord.py` | `2615ECD7C10D8DC9D0FCCADD3A69F4E129651293BB8264AB4FAA112341819CE5` |
| `tools/support/_support_shared.py` | `E7859ECCADB8BB266F77E1DB5AC1FAADEC17EF530FB667B10A5520F6CC66885E` |

Any path-set or byte change invalidates this evidence and requires a new render and review.

## Target-specific adaptations

- Utilities use CC_Loto's existing `tools/` convention: `tools/support/agent_coord.py` and its
  sibling `_support_shared.py`; no FIN `scripts/` path appears in the candidate.
- The installed CLI imports the sibling helper, ignores tracked queue README placeholders as
  records, excludes the archive README from counts, writes explicit LF board bytes, and accepts a
  fixed UTC timestamp for deterministic board generation.
- Target-local wording names CC_Loto and its support profile. No Wiki path, FIN name, product data,
  model output, index configuration, agent-owned guidance, handoff file, or test file is included.
- The guidance-semantics placeholders are intentional template content; all other unresolved
  placeholders fail rendering.

## Dependency disclosure for review

The accepted staged coordination implementation imports `PyYAML` and `jsonschema`. The existing
isolated environment built from CC_Loto's `requirements.txt` does not contain `PyYAML` (`import
yaml,jsonschema` exited `1`). The workspace support interpreter used for disposable validation has
both packages. Slice 2 proposes no dependency-file edit, consistent with M3's no-product-dependency
scope. Claude must explicitly review whether this support-operator dependency contract is
acceptable before authorizing a target write; silence is not acceptance.
