---
record_type: slice_prejob_briefing
slice: 1
target: CC_FIN
version: 3
recorded_at_utc: 2026-07-18T05:32:00Z
supersedes: version 2 (AM1-RR2/RR3/RR4 protocol corrections; retained in Git history)
  and version 1 (2026-07-18T04:56:00Z; scope conflicted with T3 publication rule 5,
  rejected by review finding S1-F1)
authorized_by: M2_APPROVAL.md plus M2_AMENDMENT_1.md
implementer: claude-code
reviewer: codex
roles_assigned_by: human owner, in-session, 2026-07-18
---

# Slice-1 pre-job briefing v3 — CC_FIN neutral support records

This version is the **only current scope**; versions 1 and 2 are superseded in full (AM1-F3, AM1-RR2/RR3/RR4).

## Roles

Implementer: claude-code. Reviewer: codex. Independent review is required before push
and before any acceptance statement.

## Exact scope — 8 creates, no modification

The slice content is byte-for-byte the reviewed rendered tree in
`doc/support-transfer/rendered/slice1/` (evidence: `SLICE1_RENDER_EVIDENCE.md`):

`support/PROFILE.md`, `support/current-status.md`, `support/log.md`,
`support/RECORD-KEEPING.md`, `support/decisions/README.md`, `support/AFI.md`,
`support/LESSONS-LEARNED.md`, `support/GOOD-PRACTICES.md`

Explicitly **not** in slice 1: `support/README.md` and the `docs/README.md` link
(slice 3c, after coordination and handoff cores); `support/decisions/adr.template.md`
(AM1-F4: not an authorized target path).

## Exceptional replacement of the rejected commit (one-time, this slice only)

The rejected, never-pushed local commit `80f87308545875aeeed0bd8d35f6c65ab8f5cb1e` is
removed before re-implementation:

- Preconditions (all verified immediately before the command): porcelain empty;
  `HEAD` equals `80f8730...`; exactly `1 0` against `origin/main` (never pushed).
- Command: `git reset --hard 238c207c73970f3d3c6dc00c2db5932ebeca7be4`
- Postchecks: `HEAD` equals the anchor `238c207...`; porcelain empty; `0 0` against
  `origin/main`.
- This is authorized once, for this rejected unpushed commit, by M2_AMENDMENT_1.md §5;
  it is never a routine recovery method and never permitted after a push.

## Preflight (after the replacement, before writing)

1. `HEAD` equals anchor `238c207c73970f3d3c6dc00c2db5932ebeca7be4`; porcelain empty;
   `0 0` against `origin/main`.
2. All 8 creation paths absent; no `support/` directory exists.
3. The rendered source tree's own evidence is current (`SLICE1_RENDER_EVIDENCE.md`).

## Two-commit evidence protocol (AM1-F2, corrected per AM1-RR2/RR3/RR4)

1. **Content commit A**: copy the rendered tree byte-for-byte; `git add support`;
   verify staged paths are exactly the 8 files; commit. `support/log.md` carries only
   the truthful `support-prepared` event (render/verification time);
   `support/current-status.md` states validation as **pending** with the exact command
   as entry point. No record claims commit A exists before it does.
2. **Validation run against A's tree**: with porcelain clean at A, run exactly the
   accepted baseline command `PYTHONDONTWRITEBYTECODE=1 python -m pytest
   -p no:cacheprovider --continue-on-collection-errors` from the repository root, with
   reporting-only additions permitted (`-q`, `--tb=no`,
   `--junitxml=<outside-repo>`) and **no `-W` or other behavior-altering flag**
   (AM1-RR3); record the integer exit code; compare tuples against
   `M2_BASELINE_FAILURE_SET.md`.
3. **Evidence commit B**: append two events to `support/log.md` under this
   deterministic rule (AM1-RR2): a `support-committed-local` event whose timestamp is
   **commit A's committer time converted to UTC** (from
   `git show -s --format=%cI <A>`; fixed statement text), and a `support-validated`
   event (authoring time) carrying the exact command, integer exit code, tuple result
   (expected 54/54, 0 new / 0 gone / 0 mutated), and **commit A's SHA** as the tested
   tree; refresh `support/current-status.md` (validation summary now literal, next
   action = reviewer). Commit B's diff must touch only these two files.
4. **Final-tree validation at B (AM1-RR4)**: with porcelain clean at B, re-run the
   same like-for-like command and confirm the identical tuple set at HEAD B, plus
   focused B-tree checks (sensitive scan, relative links, status/log consistency:
   the recorded A SHA equals `B^`). These results are review evidence the reviewer
   reproduces independently; no further evidence commit is written (the target-local
   event truthfully records A as the tested tree of its result).
5. **Final identity verification**: porcelain empty; `HEAD == B`; `B^ == A`;
   `git diff A..B --name-only` is exactly `support/current-status.md` and
   `support/log.md`.

## Slice identity and recovery

The slice comprises **commits A and B**. Rollback (only with reviewer/owner direction):
`git revert` B then A, restoring the parent recorded in the preflight; never
`reset --hard`, never after push. Push happens only after reviewer acceptance of both
commits.

## Stop conditions

Precondition or postcheck failure at the exceptional replacement; preflight drift;
any staged path outside the 8; byte difference from the reviewed rendered tree; any
new/disappeared/mutated tuple; commit B touching anything beyond the two evidence
files; reviewer findings. On stop: no push, report to reviewer and owner with the
exact failing check.
