---
record_type: slice_prejob_briefing
slice: 2
target: CC_FIN
version: 2
recorded_at_utc: 2026-07-18T12:39:25Z
supersedes: version 1 (pre-commit staging exposed platform-default BOARD newline
  translation; v2 requires explicit LF bytes so reviewed source and staged blob match)
authorized_by: M2_APPROVAL.md plus M2_AMENDMENT_1.md
implementer: codex
reviewer: claude-code
roles_assigned_by: human owner, in-session, 2026-07-18
---

# Slice-2 pre-job briefing v2 — CC_FIN coordination core

This briefing is the only current slice-2 scope. It opens review of the corrected
rendered candidate only. No CC_FIN write, commit, or
push occurs until Claude Code accepts this briefing and the exact rendered tree.

## Roles and gate

Implementer: **codex**. Reviewer: **claude-code**. The owner confirmed these roles
for slice 2 in-session. Independent review is required before the content commit and
again before push.

## Exact content scope — 14 creates, no modification

Content commit A copies the byte authority in `rendered/slice2/` exactly:

1. `coordination/TEAM_PROTOCOL.md`
2. `coordination/BOARD.md`
3. `coordination/schemas/message.schema.json`
4. `coordination/schemas/claim.schema.json`
5. `coordination/schemas/resolution-manifest.schema.json`
6. `coordination/templates/message.template.md`
7. `coordination/templates/claim.template.yml`
8. `coordination/templates/resolution-manifest.template.md`
9. `coordination/templates/guidance-semantics.template.md`
10. `coordination/messages/README.md`
11. `coordination/archive/README.md`
12. `coordination/claims/README.md`
13. `scripts/agent_coord.py`
14. `scripts/_support_shared.py`

No agent-owned guidance, handoff file, support index, test module, workflow, or other
path is in slice 2. The guidance-semantics file is itself a template: its exact
contract-approved placeholders are intentional and are not claims that either
agent-owned guidance payload already exists or is synchronized.

## Target adaptations visible in the rendered tree

The accepted staged sources are adapted only where target installation requires it:

- `agent_coord.py` imports sibling `_support_shared`, not staged `_shared`;
- tracked queue `README.md` placeholders are ignored as records, and the archive
  placeholder is excluded from the generated record count;
- the target CLI accepts `--timestamp` with `--write-board` for exact BOARD byte
  reproduction and writes explicit LF bytes on every platform; normal generation
  still uses current UTC;
- target-local module names and runtime documentation replace staged/Wiki wording;
- before slice 3, BOARD truthfully says `HANDOFF.md missing`. Adding `HANDOFF.md`
  makes BOARD stale and validation non-zero until regeneration.

The last point does not expand slice 2. Slice 3's pre-job briefing must explicitly
include the required generated BOARD refresh in its exact evidence diff. If its
authorized exact scope cannot accommodate that generated modification, execution
stops for an owner-reviewed amendment rather than leaving a stale board.

## Preflight immediately before CC_FIN content commit A

1. `HEAD` and live `origin/main` both equal published slice-1 B
   `879bcb507e461282c68cb20beab77c0def9019a4`; porcelain is empty; divergence is
   `0 0`.
2. All 14 creation paths above are absent.
3. The Wiki source commit containing this briefing, `SLICE2_RENDER_EVIDENCE.md`, the
   renderer, and the rendered tree is pushed and accepted by Claude Code.
4. Re-run the fixed-timestamp renderer and confirm 14/14 SHA-256-identical files.

Any mismatch is a stop condition.

## Two-commit evidence protocol

1. **Content commit A**: copy the 14-file rendered tree byte-for-byte; stage only the
   14 paths; compare every staged blob to the reviewed source; commit. BOARD initially
   has no active records, archive count 0, and `HANDOFF.md missing`.
2. **Coordination validation at clean A**: run exactly from the CC_FIN root:
   `$env:PYTHONDONTWRITEBYTECODE='1'; python scripts/agent_coord.py .`
   Expected result: exit 0, `validate: 0 error(s), 0 warning(s)`, no tracked or
   untracked runtime artifact.
3. **Native validation at clean A**: run exactly:
   `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --continue-on-collection-errors -q --tb=no --junitxml="$env:TEMP\fin_slice2_A.xml"`
   The report is outside the repository. Expected result is exit 1 with all 54
   normative baseline tuples unchanged: 0 new, 0 gone, 0 mutated. `pytest.ini` sets
   `testpaths = tests`; the new `scripts/` files are outside discovery, but the native
   comparison remains mandatory and is evidence rather than an assumption.
4. **Evidence commit B**: append `support-committed-local` and `support-validated`
   events for subject `SLICE-2` to `support/log.md`, and refresh
   `support/current-status.md`. The committed-local timestamp is A's committer time
   converted to UTC; the validated event names A's full SHA, both literal A commands,
   integer exit codes, target-validator result, and 54-tuple result. B changes exactly
   those two existing support files.
5. **Final validation at clean B**: re-run the exact coordination command and the
   identical native command with only the report name changed to
   `fin_slice2_B.xml`; confirm the same target-validator result and the same 54 tuples.
   Also confirm 14-file inventory, sensitivity/placeholder/link checks, A-byte
   identity, recorded A equals `B^`, and `A..B` contains exactly the two evidence
   paths. These B-tree results are reviewer evidence and create no third target commit.

## Publication and recovery

The slice consists of A and B. Both remain local until Claude Code independently
reproduces the evidence and explicitly authorizes their exact push. Rollback, only on
reviewer/owner direction, is `git revert` B followed by A. Never reset toward the old
M1 anchor; that would destroy the accepted slice-1 history.

## Stop conditions

Stop on preflight drift; any path outside the 14 creates in A or the two evidence
modifications in B; any byte mismatch; non-zero coordination validation; any new,
gone, or mutated baseline tuple; sensitive content; unresolved non-template
placeholder; dangling/escaping link; runtime artifact; stale BOARD; or reviewer
finding. Report the exact failed command and integer exit code. No push occurs on a
stop.
