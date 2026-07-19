---
record_type: local_ab_implementation_evidence
target: CC_Loto
slice: 2
recorded_at_utc: 2026-07-19T21:42:42Z
wiki_packet_commit: 5408dd6a592680b9963f2377262e9ff1999889e4
target_parent: 496800dcf499f5bde21e52e1ea6abe917ca22e4f
content_commit_a: 12ef3b784496764b5534879e7819f19ff2a4616c
evidence_commit_b: 4ce96acb3a47d6239dd85abbedaa6d5bd5b7a38a
publication_state: local_unpushed
---

# CC_Loto Slice 2 local A/B implementation evidence

## Gate and chain

- The independently accepted Wiki packet is committed and pushed at
  `5408dd6a592680b9963f2377262e9ff1999889e4`; Wiki HEAD and `origin/main` matched with divergence
  `0 0` before target implementation.
- CC_Loto preflight passed at published Slice 1 tip
  `496800dcf499f5bde21e52e1ea6abe917ca22e4f`: branch `main`, HEAD equals `origin/main`, divergence
  `0 0`, empty porcelain, all 14 creation paths absent.
- Local chain is exactly `496800dc -> 12ef3b7 (A) -> 4ce96ac (B)`.
- CC_Loto is clean and two commits ahead of `origin/main` (`2 0`). Nothing was pushed.

## Content commit A

Commit `12ef3b784496764b5534879e7819f19ff2a4616c` (`support: add coordination core`) has parent
`496800dcf499f5bde21e52e1ea6abe917ca22e4f` and adds exactly the 14 independently reviewed paths
from [`rendered/loto-slice2/`](rendered/loto-slice2/): 12 under `coordination/` and two under
`tools/support/`.

- Corrected pre-stage filesystem inventory: 14 files under exactly the two allowed untracked roots.
- Staged path count: 14.
- Reviewed source to target bytes: 0 mismatches.
- Raw target file to staged Git blob: 0 mismatches.
- Reviewed source Git object to committed A object: 0 mismatches.
- `git diff --cached --check`: exit `0` before commit.
- Worktree after commit: clean.

At clean A, the installed support command `python tools/support/agent_coord.py .` used the separate
support-operator interpreter with PyYAML `6.0.3` and jsonschema `4.26.0`; exit `0`, 0 errors, 0
warnings. CC_Loto product requirements were not edited and the product environment is not claimed
support-capable.

With output/model-cache paths redirected outside the repository, the native target runner produced:

| A layer | Tests | Exit | Result |
|---|---:|---:|---|
| `core-unit` | 42 | 0 | passed |
| `contract` | 25 | 0 | passed |
| `state-integrity` | 3 | 0 | passed |
| Total | 70 | 0 | passed |

## Evidence commit B

Commit `4ce96acb3a47d6239dd85abbedaa6d5bd5b7a38a` (`support: record Slice 2 validation evidence`) has
parent A and changes exactly:

- `support/current-status.md` — SHA-256
  `9941E7CD0021476402FCFC5320A3EBA27E4E13359B711A07CA4DED7AAF261DBF`
- `support/log.md` — SHA-256
  `5B7BB4E70ABCC335D9171D99BCA6FE86EB66E294427871C27C62336DA197FD8A`

The reviewed B byte authority is [`rendered/loto-slice2-evidence-b/`](rendered/loto-slice2-evidence-b/).
The log is append-only relative to published Slice 1 and adds exactly two Slice 2 events. It records
A's full SHA and parent, Wiki packet commit, path/identity evidence, actual commands and integer
exits, actual support-library versions, the product-environment non-claim, and the stopped initial
scope guard. Current status truthfully reports local/unpushed A/B, empty target-local queues, the
missing handoff pointer, remaining slices, the independent committed-object review gate, and M4 as
closed.

At clean B:

- `B^ == A`; `A^ == 496800dc`.
- A path count is 14; B path count is 2.
- A reviewed-source/committed-object mismatches remain 0.
- Installed coordination validation exits `0` with 0 errors and 0 warnings.
- Target is clean; divergence is `2 0`.
- Native final-tree layers again pass 42/42, 25/25, and 3/3 (70/70), all exit `0`.

## Truthful stopped and invalid attempts

These results are excluded from pass evidence but retained for review:

1. One combined read-only preflight command exited `1` because its PowerShell guard compared the
   divergence output to a single-quoted literal tab. Its printed evidence already showed the correct
   `0 0`, exact target SHAs, 14 candidates, and zero collisions; a corrected split-field guard then
   exited `0` before any target write.
2. The first target copy guard stopped before staging because `git status --porcelain` summarized 14
   files as two untracked directories. It left only the intended `coordination/` and `tools/support/`
   roots. The corrected guard counted 14 filesystem files, then the staged identity gate passed.
3. One post-A comparison converted `git show` bytes through PowerShell text lines and reported 14
   mismatches; that method is invalid evidence. The replacement compared reviewed-source Git object
   IDs directly to `A:path` object IDs and returned 0 mismatches.

## Reviewer handoff and recovery

Claude must independently inspect A/B identities, paths, bytes, installed validation, native results,
evidence truth, and clean `2 0` state. No push is authorized by this record. On explicit acceptance,
Codex may push exactly A followed by B as one normal fast-forward and report live remote state.
Recovery, only on reviewer/owner direction, is a new revert of B followed by A; reset, force push,
and unrelated cleanup are prohibited. M4 remains closed.
