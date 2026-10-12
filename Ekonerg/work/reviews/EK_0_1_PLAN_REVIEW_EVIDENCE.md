# EK-0.1 plan revision evidence

Date: 2026-09-29. Implementer: Codex. Reviewer: Claude.

Scope: plan revision and review tools only. No framework transfer, source intake,
database creation, audit execution, or Enconet defect fix was performed.
Version 1.1 remains pending Claude review. EK-0.1 is not closed.

## Review changes

Claude approved version 1.0 with non-blocking notes in
`CC_2026-09-29T104101Z_ekonerg-plan-review-verdict` (neutral coordination queue).
Finding `EK-0.2/EK-1.2-1` must be satisfied before those tasks close.

- EK-0.2 now names the exact path constants in the coordination and validation
  tools, and requires their manifest entries to say **adapt**.
- The local handoff copy is also marked adapt. Its project argument does not
  remove the need to inspect its defaults, schema path, and Git-root lookup.
- EK-1.2 now requires isolated fake sibling projects. Tests must prove the
  intended output and preserve the fake Enconet file list, bytes, and file
  change times. No destructive regression test may touch the live audit.
- Both wrong destinations are covered. An unchanged relocated copy targets a
  nested `Ekonerg/Enconet` folder. A partial root change could instead target the
  real sibling. This corrects the review's path explanation, not its finding.
- EK-1.3 now stops for an owner decision if shared-runtime checks fail.
  A separate audit runtime is not silently approved.
- The suggested Enconet closeout backport is outside this request.

These are plan requirements, not proof that the future isolation tests pass.

## Readability method

Local checker: `Ekonerg/tools/measure_plan_readability.py`.
Policy: `all-plan-prose-v1`, fixed and tested before the first measurement.
Language: English (`en_US`). Python: 3.13.9.

The checker uses [textstat](https://pypi.org/project/textstat/) 0.7.13 for word,
sentence, and syllable counts, with NLTK 3.10.3 and Pyphen 0.18.1. It computes
the unrounded grade as `0.39 * words / sentences + 11.8 * syllables / words - 15.59`.
The limit applies to that unrounded value, not a rounded display value.

All narrative prose is included: What & Why, work, tests, acceptance criteria,
review instructions, and status text. Headings, tables, code fences, inline code
(including code-formatted paths), rules, and field labels are excluded. Links
keep their visible text. Wrapped lines form one paragraph. Each list item is a
separate unit; a missing final full stop is supplied. This does not grade code,
tables, or paths. It is an aggregate prose grade, not a guarantee about each
sentence or a substitute for Claude's plain-language review.

Run with `--details` to inspect every excluded item with its source line and
the full measured prose. This also exposes any unexpected Markdown parsing.
The reader is specific to this plan format, not a general Markdown parser.

The English dictionary is loaded only from the tools environment. Missing data
fails the check before textstat can attempt an implicit download. Its SHA-256:
`cad209c39eb87677d64e93d97f8eed10b7e6f9bdd42de8e7ca8efc8e17d62e8a`.

| Measurement | Version 1.0 | Version 1.1 |
|---|---|---|
| Words | 4291 | 4630 |
| Sentences | 512 | 545 |
| Syllables | 7515 | 7988 |
| Excluded items | 299 | 306 |
| Unrounded grade | 8.344347321246506 | 8.0813967543147 |
| Limit | 9 | 9 |
| Result | Pass | Pass |

Version 1.0 plan SHA-256 (UTF-8, LF):
`df028f9d8b321c1dcf4c70e9a781da76305be6d16ca9721936cd4a2fa8ae5b96`.

Version 1.1 plan SHA-256 (UTF-8, LF):
`9b1a668ef8a1b61b4c9616b747ecd2bc43e268e469cf5ce300fe6c0c0aff377c`.

Version 1.1 measured prose SHA-256:
`fbb692ebc552e2374b21af4321873b32738fdb45bc577ca73a5c684ca125a8c7`.

## Commands and observed results

Run from the workspace root. Exit codes are integers.

| Stage | Exact command | Exit | Result |
|---|---|---|---|
| RED, before checker existed | `Ekonerg\tools\.venv\Scripts\python.exe -m unittest discover -s Ekonerg\tools\tests -v` | 1 | Expected missing checker module |
| GREEN, after checker added | `Ekonerg\tools\.venv\Scripts\python.exe -m unittest discover -s Ekonerg\tools\tests -v` | 0 | 8 tests passed; repeated after plan revision |
| Baseline and final measurement | `Ekonerg\tools\.venv\Scripts\python.exe Ekonerg\tools\measure_plan_readability.py Ekonerg\docs\EKONERG_AUDIT_TDD_PLAN.md` | 0 | Both grades and counts shown above |
| Negative threshold check | `Ekonerg\tools\.venv\Scripts\python.exe Ekonerg\tools\measure_plan_readability.py Ekonerg\docs\EKONERG_AUDIT_TDD_PLAN.md --limit 0` | 1 | Correctly refuses an unmet limit |
| Tracked diff whitespace | `git diff --check -- Ekonerg` | 0 | No whitespace errors; Git warned about future CRLF conversion |

The eight tests cover paragraph joining, list boundaries, visible exclusions,
retention of explanations and criteria, link text, the formula and unrounded
boundary, empty counts, and an unclosed code fence.

## Review-tool environment and setup failures

`Ekonerg/tools/.venv` is a new, ignored, disposable environment for this check.
It is not copied from Enconet and is not an audit runtime decision. No shared
audit package was changed. Do not include it in the framework transfer manifest.

Setup performed:

- `python -m venv Ekonerg\tools\.venv`: exit 1 at ensurepip in the sandbox;
  approved rerun outside the sandbox: exit 0.
- `Ekonerg\tools\.venv\Scripts\python.exe -m pip install textstat==0.7.13`:
  exit 0. Resolved count-engine versions are pinned above.
- `Ekonerg\tools\.venv\Scripts\python.exe -m nltk.downloader -d Ekonerg\tools\.venv\nltk_data cmudict`:
  exit 1 in the sandbox due to a proxy security refusal, then exit 0 on the
  approved rerun outside it. No security bypass option was set. The successful
  download emitted a runpy warning, then extracted the dictionary.

For a fresh review environment, install
`textstat==0.7.13 nltk==3.10.3 pyphen==0.18.1`, obtain the dictionary with the
command above, and check its hash before comparing scores. Other installed
dependencies were not used as counting engines. Dependency and dictionary
changes may change counts; do not carry this score to a changed plan.

## Remaining gate

Claude must independently check the revision, the extraction policy, and the
measured results. Then record the verdict through the neutral coordination
channel. Do not begin EK-0.2 or later transfer tasks before that review closes.
Framework and audit validations are not run: no framework exists in Ekonerg yet.
