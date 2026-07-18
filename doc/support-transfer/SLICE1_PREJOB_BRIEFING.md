---
record_type: slice_prejob_briefing
slice: 1
target: CC_FIN
version: 6
recorded_at_utc: 2026-07-18T06:03:49Z
supersedes: version 5 (accepted by Codex at `CX_2026-07-18T055651Z`; v6 changes ONLY
  the role assignment per the owner's in-session reassignment — protocol content is
  otherwise identical), and versions 1-4 as chained in v5; all retained in Git history
authorized_by: M2_APPROVAL.md plus M2_AMENDMENT_1.md
implementer: codex
reviewer: claude-code
roles_assigned_by: human owner, in-session, 2026-07-18 (session-limit role switch)
---

# Slice-1 pre-job briefing v6 — CC_FIN neutral support records

This version is the **only current scope**; versions 1-5 are superseded in full (v6 = v5 with roles reassigned by the owner; AM1-F3, AM1-RR2..RR9 history unchanged).

## Roles (owner-reassigned in-session, 2026-07-18)

Implementer: **codex**. Reviewer: **claude-code**. Independent review by the
non-implementing agent is required before push and before any acceptance statement.
The rejected commit `80f8730` was authored under the previous role assignment; the
exceptional replacement and the A/B protocol below are procedure-bound, not
person-bound, and are now executed by codex.

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
2. **Validation run against A's tree**: with porcelain clean at A, run exactly this
   one literal PowerShell command from the repository root (AM1-RR3/RR5 — accepted
   baseline behavior plus fixed reporting-only additions; no `-W` or other
   behavior-altering flag):
   `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --continue-on-collection-errors -q --tb=no --junitxml="$env:TEMP\fin_slice1_A.xml"`
   Record the integer exit code; compare tuples against `M2_BASELINE_FAILURE_SET.md`.
3. **Evidence commit B**: append two events to `support/log.md` under this
   deterministic rule (AM1-RR2): a `support-committed-local` event whose timestamp is
   **commit A's committer time converted to UTC** (from
   `git show -s --format=%cI <A>`; fixed statement text), and a `support-validated`
   event (authoring time) carrying the exact command, integer exit code, tuple result
   (expected 54/54, 0 new / 0 gone / 0 mutated), and **commit A's SHA** as the tested
   tree; refresh `support/current-status.md` (validation summary now literal, next
   action = reviewer). Commit B's diff must touch only these two files.
4. **Final-tree validation at B (AM1-RR4/RR5)**: with porcelain clean at B, re-run
   the identical command with only the fixed report name changed:
   `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --continue-on-collection-errors -q --tb=no --junitxml="$env:TEMP\fin_slice1_B.xml"`
   and confirm the identical tuple set at HEAD B, plus focused B-tree checks
   (sensitive scan, relative links, status/log consistency: the recorded A SHA equals
   `B^`). These results are review evidence the reviewer reproduces independently; no
   further evidence commit is written (the target-local event truthfully records A as
   the tested tree of its result).
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
