# ADR-0001 — One git repository rooted at `03_PKE_SA_NQA1`

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-11 |
| Decided by | Human (project owner) |
| Scope | Workspace |
| Register | D-1 (`docs/CX_CC_RECONCILIATION.md` §6; `docs/CC_ALIGNMENT_PLAN.md` §5) |

## Context

The relocated checkout has no `.git` anywhere under `03_PKE_SA_NQA1`; the GitHub backup
(`github.com/nekiee13/CC_LLM_Wiki_PKE_SA_Enconet`) is not verifiably connected to this
tree. Options considered: repository per project entry (Enconet only), one repository at
`03_PKE_SA_NQA1`, or one repository over all of `LLM_Wiki`.

## Decision

One git repository rooted at `03_PKE_SA_NQA1`, covering Enconet, Ekonerg, TEKOL, and the
shared workspace assets (CLAUDE.md/AGENTS.md, shared skills, global `doc/`, workspace
scripts/tests).

## Consequences

- G0 recovery (CC_ALIGNMENT_PLAN Task C0.1) targets this root: reconcile against the
  GitHub backup file-by-file; no local file silently discarded.
- Other `LLM_Wiki` sections (01_, 02_, 04_) keep their own version-control arrangements.
- Root `.gitignore`, commit-tag vocabulary, and this ADR store are versioned by this repo.
