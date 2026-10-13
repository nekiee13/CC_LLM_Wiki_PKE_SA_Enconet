# CU-4.2: remaining non-protected retention

Status: **partial**. Owner's "proceed" continues the existing cleanup task.
No epic, task, audit gate, deletion or ownership override was added.

## Completed

- Old `doc/` is now absent. Its **102 empty directory nodes** were renamed
  together to `.tmp/cleanup-retained-20261014/old-doc-empty-shells`, preserving
  saved directory identities, attributes and ACLs. No shell was deleted.
- Four populated test trees and one compiled-cache tree are retained under
  `.tmp/cleanup-retained-20261014/audit_template/tests/`, with their original
  names. **99 files and 45 directory nodes** match their captured witnesses.
  File witnesses include raw SHA-256, identity, modification time, attributes
  and ACL hash. Apply, verify and repeat apply pass; no live undo was run.
- Both current audit database hashes remain exactly unchanged.

The four generated test runs were classified against their actual producers:
`audit_template/tests/test_bootstrap_sieving_analysis.py`,
`test_bootstrap_phase_validation.py`, and `test_bootstrap_source_validation.py`.
They create synthetic companies `Mali Audit` and `Čista Tvrtka` beneath tests.
These are not Enconet/Ekonerg evidence or active source databases. The fifth
tree contains 22 compiled Python test-cache files. Original data is retained,
not regenerated, modified, executed or deleted.

## Bound plans and validation

Authority: `OWNER_REMAINING_RETENTION_20261014.md`, raw-hash-pinned and stored
with a byte-preserving Git rule. Exact plans:

- `old-doc-empty-plan.json`: canonical SHA-256
  `ca537dbc302a870bd3837e38dc785f3df0d027a0db4669529e5f543220b3466e`.
- `populated-test-history-plan.json`: canonical SHA-256
  `2c5155317e76dfe87f0dffeb2bcaf4eb701f3885aff6cd5068e597598e90fc01`.
- Empty-doc events: `old-doc-empty-journal.jsonl`.

The five-path populated profile is separate from empty-tree profiles. It
refuses changed files, hard links, shortcuts, foreign destinations and any
agent-owned target. All rows are checked before the first rename. Native
retry and undo, changed-file batch rejection, wrong profile/scope/destination,
ownership and hard-link refusal were tested on disposable inputs.

`PYTHON` below is `C:/xPY/vEnv/WikiEnconet/python.exe`. For each move tool,
MODE was `preview`, `apply`, `verify`, then `apply` again. Every final command
exited **0**, using native access where identity/ACL/browser access requires it.

```text
PYTHON -B scripts/cleanup_residual_empty.py --root . --bundle old-doc --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/old-doc-empty-plan.json --mode MODE --authority PKE_SA_NQA1_doc/plans/cleanup-cu4/OWNER_REMAINING_RETENTION_20261014.md --journal PKE_SA_NQA1_doc/plans/cleanup-cu4/old-doc-empty-journal.jsonl
PYTHON -B scripts/archive_pytest_scratch.py --root . --bundle populated-test-history --plan PKE_SA_NQA1_doc/plans/cleanup-cu4/populated-test-history-plan.json --authority PKE_SA_NQA1_doc/plans/cleanup-cu4/OWNER_REMAINING_RETENTION_20261014.md --mode MODE
PYTHON -B -m pytest scripts/tests -q -p no:cacheprovider --basetemp .tmp/cu4-final-retention-full-01 --junitxml PKE_SA_NQA1_doc/plans/cleanup-cu4/final-retention-full-01.xml
PYTHON -B Enconet/scripts/run_all_validations.py --no-record
PYTHON -B Ekonerg/scripts/run_all_validations.py --no-record
PYTHON -B scripts/check_guidance_drift.py
PYTHON -B scripts/check_skill_structure.py
```

Complete workspace suite: **131 passed**, no skips. Enconet aggregate:
**19 passed**. Ekonerg: **8 passed, 9 phase skips**, no phase change. Guidance:
zero errors, 47 anchors/eight documented differences. Skill structure: zero
errors, 32 locations. The focused native suite passed 17 tests. Its first
run had 16 passes/one case-sensitive assertion failure: the existing safety
guard correctly rejected a hard link with lowercase wording. The assertion
was corrected; both failed and passed XMLs remain. Earlier audit-wide 480-test
regression and standalone PDF runs were not rerun for these scratch-only moves.

Baseline database hashes:

- Enconet: `f17c977f8c5ffec13a279bdb909dd17f38e056e5183812a92ae5810b03251ed1`.
- Ekonerg: `161c56ff5d457348ec6809c5e6dcc41e2dd09854d4e71cde11d12a2064d387c0`.

## Still open

The original 20 populated/protected scratch holds are reduced to **15**.
All are under `Enconet/.test-tmp/` and contain generated `.claude` fixtures.
Their exact names remain in `legacy-empty-archive-plan.json`; the five
audit_template rows in that historical preview are superseded by this result.
No protected fixture file or parent was moved or changed.

To retain the remaining parent as a whole, an explicit owner exception must
name the move from `Enconet/.test-tmp` (including its generated `.claude`
fixtures) to `Enconet/.tmp/cleanup-retained-20261014/protected-test-fixtures`.
No edits to actual or generated Claude configuration would be included.
Without that exception, leave the parent where it is. This is a safety
boundary, not another implementation slice.

Post-execution review of this batch and final current/historical path closure
remain in CU-4.2. Seven original owner edits remain unstaged and untouched.
Shared index certification remains at `e420149`, not current-tip freshness;
no agent-owned index was refreshed. Dashboard results, gates, incoming/raw,
crumbs and live databases are unchanged. No full cleanup closure is claimed.
