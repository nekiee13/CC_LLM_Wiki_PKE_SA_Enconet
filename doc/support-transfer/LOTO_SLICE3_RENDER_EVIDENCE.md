---
record_type: exact_render_evidence
target: CC_Loto
slice: 3
recorded_at_utc: 2026-07-19T22:06:40Z
target_parent: 4ce96acb3a47d6239dd85abbedaa6d5bd5b7a38a
render_timestamp: 2026-07-19T22:05:00Z
---

# CC_Loto Slice 3 exact-render evidence

## Control

- Target branch: `main`.
- Local HEAD and `origin/main`: `4ce96acb3a47d6239dd85abbedaa6d5bd5b7a38a`.
- Divergence: `0 0`; porcelain: empty.
- Renderer: [`rendered/render_loto_slice3.py`](rendered/render_loto_slice3.py), SHA-256
  `3D40E25C68DB90212D0AEB28E7D4E3546B0299E26F520B9EE2CB40D239ED7041`.
- Exact byte authority: [`rendered/loto-slice3/`](rendered/loto-slice3/).
- Scope: seven creates plus one generated `coordination/BOARD.md` modification.
- The seven create paths are absent. The only collision is the expected existing board.
- CC_Loto remained read-only during preparation.

## Deterministic render and lifecycle probe

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python doc\support-transfer\rendered\render_loto_slice3.py --timestamp 2026-07-19T22:05:00Z
```

Exit code `0`; a second fixed-timestamp run produced zero SHA-256 differences. The renderer overlays
the candidate on a disposable copy of the published Slice 2 support/coordination tree, regenerates
the board through the installed target tool, and requires 0 errors and 0 warnings.

The disposable first-publication probe then:

1. validates and writes one immutable handoff record;
2. atomically replaces the bootstrap `HANDOFF.md` pointer;
3. appends one canonical pipe-delimited `handoff-published` event;
4. proves the pointer change makes `BOARD.md` stale and validation non-zero;
5. regenerates the board with the installed tool and returns validation to zero.

## Exact proposed bytes

| Operation | Target path | SHA-256 |
|---|---|---|
| create | `HANDOFF.md` | `EBE7F3B48A28B02F8B3B32D586144D4B1EDF43EBC85D0303FCC0AB90ADBC0A43` |
| modify generated | `coordination/BOARD.md` | `A541294B50A11AE56E48DA5735C3BAF67D76264B4CA72BAD8A0F287F37E0A349` |
| create | `support/handoffs/README.md` | `7361E41C6CAF5C3498404064F8D0CC30873182D86762E941E6DFE39243EFDDDC` |
| create | `support/schemas/handoff.schema.json` | `EC50DA1A7EACA3FE30C19054883DEC032255585908EADB3D12864FB710E621E1` |
| create | `support/templates/continuity-checklist.template.md` | `0752B1B93494C5D87DB7095092D3C65B876B2FE79F3BF14625B47A0E733F16E2` |
| create | `support/templates/handoff-pointer.template.md` | `B34705ACD74EF5231FF1B4CEC0931485BC1580D9EDBA3AB1E5B2A227D5491905` |
| create | `support/templates/handoff-record.template.md` | `0F2CD0A817E275012B924AB0CD24A641B20F6D500AEA5316AC5D355BFC748EE3` |
| create | `tools/support/make_handoff.py` | `357ECF76E407BA9A3027E007DB872C6505521DEB5DF7FAA7B11D366AE745F655` |

The board uses explicit LF bytes: 0 CR and 18 LF. Any path-set or byte change invalidates this
evidence and requires a new render and review.

## Bootstrap truth and target adaptations

- `HANDOFF.md` says no immutable record is published, contains no fabricated record ID or dangling
  record link, and points operators to current status, coordination, claims, and Git state.
- The generated board reports `Record: none published (bootstrap state)`, archive count zero, and
  the reviewed timestamp. Creating `HANDOFF.md` without this board modification would be stale and
  is prohibited.
- The publisher is installed at Loto-native `tools/support/make_handoff.py`, imports the sibling
  `_support_shared`, and has no FIN, Wiki, or private-path runtime reference.
- Its append-only event matches CC_Loto's pipe-delimited support log contract. The accepted schema
  and semantic checks are unchanged; SHA-1 and SHA-256 Git object formats remain supported.
- Continuity renders `CC_Loto`; the pointer template retains exactly its intentional handoff
  placeholder allowlist. No product dependency, code, data, output, workflow, guidance, index, tag,
  or release is in scope.

## Target-adapted publisher suite

The accepted staged publisher tests were run against the rendered Loto module through a disposable
alias harness: 33 passed, exit `0`, outside the sandbox. The first in-sandbox attempt exited `1`:
31 tests errored on Windows pytest temp ACL setup/cleanup and two non-temp tests passed. That attempt
is excluded from pass evidence. The failed harness was removed after the outside-sandbox rerun.
