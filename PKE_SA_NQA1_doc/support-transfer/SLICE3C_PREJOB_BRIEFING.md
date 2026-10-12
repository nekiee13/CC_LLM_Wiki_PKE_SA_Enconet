---
record_type: support_transfer_prejob_briefing
slice: 3c
version: 1
recorded_at_utc: 2026-07-18T13:52:30Z
authorized_by: M2_APPROVAL.md and M2_AMENDMENT_1.md
implementer: codex
reviewer: claude-code
target_parent: ea41c2a6ddb9906ede272a9003ddddf212c5b80a
status: pre-write-review-required
---

# Slice-3c pre-job briefing — CC_FIN index closure

## Authority, roles, and boundary

The owner confirmed Codex as implementer and Claude Code as independent reviewer.
Slice 3c is exactly **1 create + 1 modification**:

1. create `support/README.md` from the accepted support-index template and complete
   CC_FIN rendering profile;
2. modify `docs/README.md` by adding exactly this one line after the existing
   governance-transition entry:
   `- [Support system](../support/README.md) — repo-local governance, coordination, and handoff core`

No other path enters content commit A. The clean pre-slice parent is published Slice 3
`ea41c2a6ddb9906ede272a9003ddddf212c5b80a`. Recovery is a reviewed revert of
Slice 3c's named commits to that parent, never reset or broad cleanup.

## Exact byte authority and rendering facts

`rendered/slice3c/` contains the two final target files. `render_slice3c.py` reads the
reviewed parent `docs/README.md` blob, proves the diff is one added line and no deletion,
renders every support-index placeholder, checks links/sensitivity/workspace references,
and validates a disposable Slice-2 + Slice-3 + Slice-3c overlay.

The support index explicitly links and labels the complete accepted FIN list:

- enhanced implementation plan;
- project documentation index;
- architecture/current-state `docs/project/AS-IS.md`;
- documentation freshness ledger;
- integration-pilot feature ADR register;
- the pull-request template, M5 exception issue form, and all three existing workflows;
- `pyproject.toml`, runtime requirements, and test requirements;
- release/package state: release adapter inventory-only; remote tag inventory is empty;
  no repository release record is present; tag/release creation remains out of scope.

The live `git ls-remote --tags origin` check returned exit 0 with zero tag refs. The
GitHub CLI is unavailable, and an unauthenticated releases API request against this
repository returned 404, so that API was **not** reported as passed. “No release
record” is the repository/tag-inventory statement authorized by amendment 1; it does
not claim visibility into private draft releases.

## Why BOARD is outside the slice

The installed `agent_coord.render_board` reads only coordination claims, active/archive
message records, and root `HANDOFF.md`. Neither `support/README.md` nor
`docs/README.md` is an input. A disposable overlay using the published Slice-2 and
Slice-3 bytes ran the installed validator without `--write-board`: exit 0, 0 errors,
0 warnings, and `coordination/BOARD.md` was byte-identical before/after. Therefore
Slice 3c needs no BOARD regeneration and no scope amendment.

## Reproduction and preflight

Run from the Wiki root with a writable temporary directory:

`$env:PYTHONDONTWRITEBYTECODE='1'; python doc/support-transfer/rendered/render_slice3c.py`

Expected exit 0: exact two-file inventory; docs diff one added line; target validator
0/0; BOARD byte-identical; link, placeholder, sensitivity, and forbidden-reference
checks passed. A second run must reproduce both files byte-for-byte.

Immediately before target write:

1. require live remote, `origin/main`, and local HEAD all equal
   `ea41c2a6ddb9906ede272a9003ddddf212c5b80a`, divergence `0 0`, empty porcelain;
2. require `support/README.md` absent and the target `docs/README.md` blob equal the
   reviewed parent blob;
3. rerun the renderer twice and require 2/2 SHA-256 identity and unchanged BOARD;
4. stop on upstream drift, path collision, unexpected docs diff, broken link,
   placeholder, sensitive content, runtime artifact, or scope expansion.

## Two-commit target protocol

1. **Content commit A**: copy `support/README.md` and replace `docs/README.md` from the
   exact rendered tree; stage exactly those two paths; compare both staged blobs to the
   reviewed source; commit only on 2/2 byte identity.
2. At clean A run exactly
   `$env:PYTHONDONTWRITEBYTECODE='1'; python scripts/agent_coord.py .`; require exit 0,
   0 errors/0 warnings, and the same BOARD blob as A's parent.
3. At clean A run exactly
   `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --continue-on-collection-errors -q --tb=no --junitxml="$env:TEMP\fin_slice3c_A.xml"`.
   Expected exit 1 only for the normative baseline: 54/54 tuples, 0 new, 0 gone,
   0 mutated (343 tests: 276 passed, 51 failed, 3 collection errors, 13 skipped).
4. **Evidence commit B** modifies only `support/log.md` and
   `support/current-status.md`, recording A's full SHA/committer UTC, both literal
   commands and integer exits, target 0/0, native tuple evidence, and reviewer gate.
5. At clean B rerun the target command and native command with
   `fin_slice3c_B.xml`; require target 0/0, the same 54 tuples, and A-to-B tuple
   identity. Confirm BOARD still equals the parent blob.
6. Confirm A is exactly the two reviewed blobs, `B^ == A`, and `A..B` changes exactly
   the two evidence files. Submit to Claude; no CC_FIN push before independent review.

Any scope, byte, link, validation, baseline, BOARD, authority-label, or reviewer defect
is a stop. Literal failed commands and integer exits are reported; expected native red
is never relabeled as a pass.
