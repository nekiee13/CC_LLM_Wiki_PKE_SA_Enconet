# Fast audit plan: check record

Date: 2026-10-01. Author: Codex. Reviewer: Claude, pending.

This record covers the [fast audit plan](../EKONERG_FAST_AUDIT_PLAN.md).
It checks the plan, not an audit result or the runtime tools.

## What changed

The new plan has four epics and ten tasks. Each has a What & Why note and
acceptance criteria. Codex carries out the work; Claude reviews it. Owner
gates remain explicit. Setup has a total limit of 60 minutes of active work.
The first target is a source register and a cited working audit section.

The old plan now points to this new work order. Its full framework scope and
unfinished EK-1.2 work remain visible. No task was marked approved by this edit.
No live source was moved, altered, ingested, or graded. The folder inspection
read file names and sizes only. No audit source was added to Git.

## Input facts

The incoming folder contains 31 Markdown files and 1,851,547 bytes.
By file name, seven are rule or standard files and 24 are QMS files.
The QMS group has 23 procedures and one manual. These are file-list facts;
source identity and completeness still need the checks in EF-1.1.

The earlier source identity note is cited as prior evidence. This turn did
not recheck the text or hashes of those sources. The new plan carries forward
its open edition and snapshot-date checks without choosing missing facts.

## Readability result

Flesch-Kincaid grade: **5.779348462210077**, below the required limit of 9.
Counts: 3,308 words, 331 sentences, and 4,898 syllables.
The exact machine result is in [the JSON record](EK_FAST_PLAN_READABILITY.json).

The existing checker and its existing environment were reused. No package
was installed or changed. Versions: Python 3.13.9, textstat 0.7.13,
NLTK 3.10.3, and Pyphen 0.18.1. The dictionary hash is in the JSON record.

Policy: all-plan-prose-v1. It includes narrative text, What & Why notes,
work steps, and acceptance criteria. It excludes headings, tables, code,
inline code such as paths, rules, and field labels. There are 96 excluded
items. Link labels remain in the prose. Use the checker's `--details` flag
to inspect the full measured prose and each exclusion.

This is an aggregate English prose grade. It does not prove that every
sentence is easy for every reader. The plan also explains key terms such
as QA, QMS, hashes, Markdown, CSV, and TDD in plain words.

## Commands and results

Commands run from the workspace root. Exit codes below are observed integers.

| Check | Command | Exit | Result |
|---|---|---:|---|
| Initial measurement with default Python | `python -B Ekonerg/tools/measure_plan_readability.py Ekonerg/docs/EKONERG_FAST_AUDIT_PLAN.md --limit 9` | 1 | Failed: NLTK is absent from the default interpreter. |
| Measurement with the existing review environment | `Ekonerg/tools/.venv/Scripts/python.exe -B Ekonerg/tools/measure_plan_readability.py Ekonerg/docs/EKONERG_FAST_AUDIT_PLAN.md --limit 9` | 0 | Grade 5.779348462210077; pass. |
| Existing checker tests | `Ekonerg/tools/.venv/Scripts/python.exe -B -m unittest discover -s Ekonerg/tools/tests -p test_measure_plan_readability.py -q` | 0 | Eight tests passed. |
| Structure | PowerShell check below | 0 | Four epics, ten tasks, fourteen notes, fourteen acceptance blocks; no incomplete sections. |
| Whitespace | `git diff --check` | 0 | No errors. Git reported its existing line-ending conversion warnings. |

The default-Python failure is retained. Success came from the already
configured review environment, not from a change to the audit environment.

Exact structure check:

```powershell
$plan = Get-Content -LiteralPath Ekonerg/docs/EKONERG_FAST_AUDIT_PLAN.md -Encoding UTF8 -Raw
$epics = @([regex]::Matches($plan, '(?m)^## Epic EF-\d+:'))
$tasks = @([regex]::Matches($plan, '(?m)^### Task EF-\d+\.\d+:'))
$notes = @([regex]::Matches($plan, '(?m)^\*\*What & Why:\*\*'))
$accept = @([regex]::Matches($plan, '(?m)^\*\*Acceptance criteria:\*\*'))
$sections = @([regex]::Matches($plan, '(?ms)^#{2,3} (?:Epic|Task) EF-[^\r\n]+\r?\n(?:(?!^#{2,3} ).)*'))
$bad = @($sections | Where-Object {
    $_.Value -notmatch '\*\*What & Why:\*\*' -or
    $_.Value -notmatch '\*\*Acceptance criteria:\*\*' -or
    $_.Value -notmatch '(?m)^- \[ \] '
})
[pscustomobject]@{
    Epics = $epics.Count
    Tasks = $tasks.Count
    WhatWhy = $notes.Count
    AcceptanceBlocks = $accept.Count
    IncompleteSections = $bad.Count
} | ConvertTo-Json
if ($epics.Count -ne 4 -or $tasks.Count -ne 10 -or
    $notes.Count -ne 14 -or $accept.Count -ne 14 -or $bad.Count -ne 0) {
    exit 1
}
```

## Scope of verification

No runtime code changed, so the runtime suites were not rerun. Their prior
results are not presented as validation of this document workflow.
No source-reading pilot or end-to-end audit run occurred in this plan task.

The documentation and code index lists were checked. No Ekonerg index is
configured. Shared Enconet indexes still name commit 62a0251; they were not
used as current evidence or refreshed. Exact live plan files were read.

Claude review remains pending. The input-file count is not proof of complete
evidence. New audit outputs will state their source coverage and review status.
