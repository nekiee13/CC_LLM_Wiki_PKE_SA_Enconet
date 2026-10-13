# CU-4.2: approved protected-fixture parent move

Status: **all named filesystem holds resolved; final plan sign-off still open**.
This is execution of the owner's specific "yes. proceed" move-only exception,
not a new task or a general relaxation of agent ownership.

## Completed move

From: `Enconet/.test-tmp`.

To: `Enconet/.tmp/cleanup-retained-20261014/protected-test-fixtures`.

The original parent is absent. All **15 recorded fixture trees**, **195 files**,
**6,538 real directory nodes** and **2,653 internal symbolic shortcuts** are
retained unchanged. Complete post-rename verification and no-op repeat apply
both pass. No file was deleted, rewritten or regenerated. No ACL, owner,
attribute or shortcut target was changed. Absolute shortcuts keep their old
target strings: they are historical, not runnable aliases in the retained home.
No shortcut was followed. Live undo was not run.

The generated `.claude` copies moved only as descendants of the one approved
parent. Actual workspace, supplier and user-global agent configuration was
not moved or edited. The ordinary ownership guard in cleanup_migration.py
is unchanged. The dedicated helper accepts only these two parent homes,
checks the exact fifteen children against the previously reviewed hold list,
and refuses changed authority, content/membership/identity/ACL drift, external
shortcuts, unknown reparse points, hard links, `.git`/`.agents` paths and
collisions. It performs whole-tree preflight before native rename and checks
every witness afterward. All operations are same-volume, reversible retention.

## Authority and evidence

- Specific owner record: `OWNER_PROTECTED_FIXTURE_MOVE_20261014.md`.
- Full no-follow witness: `protected-fixture-plan.json.zip`.
- Canonical plan SHA-256:
  `af9750046412367367571e76f495ab061f154e026801a6c435dadcafb93409a3`.
- The plan pins the actual authority's raw hash and the original hold-list
  raw hash. Native witnesses include each file's raw hash, identity, mtime,
  mode/attributes and ACL hash; directory identities/attributes/ACL hashes;
  shortcut identities/attributes and exact target strings.

`PYTHON` means `C:/xPY/vEnv/WikiEnconet/python.exe`. For the first command,
MODE was `preview`, `apply`, `verify`, then `apply` again. Every command
listed below exited **0**. Native filesystem/browser access was used where
required; no unavailable check is counted as a pass.

```text
PYTHON -B scripts/retain_protected_test_fixtures.py --root . --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/protected-fixture-plan.json.zip --authority PKE_SA_NQA1_doc/plans/cleanup-cu4/OWNER_PROTECTED_FIXTURE_MOVE_20261014.md --mode MODE
PYTHON -B -m pytest scripts/tests/test_retain_protected_test_fixtures.py scripts/tests/test_archive_pytest_scratch.py -q -p no:cacheprovider --basetemp .tmp/cu4-protected-move-tests-01 --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/protected-move-tests-01.xml
PYTHON -B -m pytest scripts/tests -q -p no:cacheprovider --basetemp .tmp/cu4-protected-move-full-01 --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/protected-move-full-01.xml
PYTHON -B Enconet/scripts/run_all_validations.py --no-record
PYTHON -B Ekonerg/scripts/run_all_validations.py --no-record
PYTHON -B scripts/check_guidance_drift.py
PYTHON -B scripts/check_skill_structure.py
```

Focused safety tests: **21 passed**. Complete workspace tooling: **140 passed**,
no skips. Includes native apply/retry/verify/undo on disposable fixtures,
failed-native-rename retry, exact scope, changed file/membership/authority,
external shortcuts, hard links and destination collisions. No failed run
occurred in this batch. Enconet aggregate: **19 passed**. Ekonerg aggregate:
**8 passed, 9 phase skips**, no phase advancement. Guidance: zero errors,
47 anchors/eight documented differences. Skill structure: zero errors,
32 locations. Earlier full audit regression and standalone PDF checks were
not rerun for this scratch-only operation.

Audit DB SHA-256 values still equal their pre-cleanup baselines:

- Enconet: `f17c977f8c5ffec13a279bdb909dd17f38e056e5183812a92ae5810b03251ed1`.
- Ekonerg: `161c56ff5d457348ec6809c5e6dcc41e2dd09854d4e71cde11d12a2064d387c0`.

## Remaining original-plan work

The Windows candidates hold, old-doc file/shell holds and all twenty named
scratch holds are now resolved through documented retention. Historical hold
lists and handoffs remain immutable; this result supersedes their pending
filesystem status, not their original evidence or decisions.

The latest retention batches still need Claude post-execution review. Final
current/historical path disposition and the single plan closure report remain
CU-4.2 work. Do not infer full cleanup closure from the absence of these holds.
Seven original owner edits remain unstaged. No audit source, evidence, score,
gate, prompt or dashboard changed. Shared index certification remains at its
prior committed snapshot, not current-tip freshness; no agent-owned index was
refreshed. No further owner decision is pending for the completed parent move.
