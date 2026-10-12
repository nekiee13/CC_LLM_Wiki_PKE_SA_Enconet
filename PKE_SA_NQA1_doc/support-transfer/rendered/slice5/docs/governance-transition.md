# Governance Transition

Last reviewed: 2026-04-11

## Current Governance Mode

- Workflow mode: trunk-only on `main`
- Active runtime scope: `oc-fin-opencode`
- Paused runtime scope: `oc-fin`

## Operating Rules

1. Develop directly on `main` unless an explicit exception is approved.
2. Keep runtime and docs aligned in the same change set when interfaces/workflows change.
3. Treat `docs/README.md` as the authoritative docs entrypoint.

## Sync Procedure

Daily sync commands:

```bash
git fetch origin --prune
git rev-parse HEAD
git rev-parse origin/main
git pull --ff-only origin main
git push origin main
```

## Divergence Recovery

Do not discard local commits or working-tree changes as routine synchronization. Stop writes and
capture evidence first:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git log --oneline --decorate --graph -n 20
```

Identify the exact commits and paths at risk; inspect active claims/messages; confirm the intended
recovery point and whether uncommitted work, a patch, branch, worktree, or backup must be preserved.
Prefer non-destructive recovery such as a fast-forward, preserving work on a named branch, or a
reviewed `git revert` of identified commits.

Any destructive discard requires explicit owner approval naming the exact target, recovery point,
preservation/backup evidence, validation commands, and stop conditions. This runbook does not
authorize `git reset --hard`, `git clean`, force-push, recursive deletion, or history rewriting.
After an approved recovery, rerun status, relevant native checks, and support validation; record the
literal commands, integer exit codes, and resulting Git identity.

## Documentation Governance

- FIN runtime docs owner: FIN maintainers (`docs/fin/*`)
- OC docs owner: OC maintainers (`docs/oc/*`)
- Integration pilot owner: pilot maintainers (`docs/integration-pilot/*`)
- Refactor invariants owner: core maintainers (`docs/refactor/*`)

File-level freshness status is tracked in `docs/documentation_freshness_ledger.md`.
