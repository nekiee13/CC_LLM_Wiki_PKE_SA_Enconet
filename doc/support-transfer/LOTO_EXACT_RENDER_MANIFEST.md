# CC_Loto Slice 1 exact-render manifest

## Control

- Prepared at UTC: `2026-07-18T22:18:54Z`
- Target baseline: `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`
- Target branch: `main`
- Target upstream: local HEAD equals `origin/main`; worktree porcelain is empty
- Render timestamp embedded in the proposed records: `2026-07-18T21:47:53Z`
- Renderer: [`rendered/render_loto.py`](rendered/render_loto.py)
- Exact output root: [`rendered/loto/`](rendered/loto/)
- Scope: Slice 1 preparation only; this manifest authorizes no CC_Loto write

## Deterministic render

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python doc\support-transfer\rendered\render_loto.py --timestamp 2026-07-18T21:47:53Z
```

Exit code: `0`. The renderer reported exactly eight files, no sensitive/workspace/private-path
hits, no unresolved placeholders, and no unresolved local links.

## Exact proposed bytes

| Target path | SHA-256 |
|---|---|
| `support/AFI.md` | `77CB3FEEBAA52F5ACCC4A3CFBA5798A614CCBB7CC48CC1711ED275B09E96C25C` |
| `support/current-status.md` | `B5960B6EA759556AC259F6AABAFD899BBC86145F774EBA755B742AB29D562658` |
| `support/decisions/README.md` | `7EDFDD5A51DA91D13A24BC926B9A4FEFA6F0208E2CB65A7A0A07A213556911DB` |
| `support/GOOD-PRACTICES.md` | `D10CA351A09F0AA4FE03CDE8668F87A9FCE073C77E727C2F1C88A168745B23FE` |
| `support/LESSONS-LEARNED.md` | `941A9F4BB3012D9640AB861D5F8415133ACEF4775ACC12F2E9EF0DD52FEB53D3` |
| `support/log.md` | `A12FA55F590B88AA087A930E654865BC90F0D497E240C95E1FAB5C3811D8602D` |
| `support/PROFILE.md` | `814DD9924718DEAF85808E473C0B2E0C59E3CF6C4C7EBD4D49351951930A1559` |
| `support/RECORD-KEEPING.md` | `E520502F19B2C987D7EE05A33DD6F4499F0E330E34413740ACB134F7ACD046DF` |

Any path-set or byte change invalidates this manifest and requires a new render and review.

## Publication boundary

After independent acceptance, content commit A may create only these eight exact blobs. Evidence
commit B may change only `support/log.md` and `support/current-status.md` to record the actual
post-A validation and committed identities. Both commits require pre-push review. Recovery is a
new revert of the named Slice 1 commits; reset, force-push, and unrelated cleanup are excluded.
