---
record_type: exact_render_evidence
target: CC_Loto
slice: claude-guidance-alignment
step: 2
recorded_at_utc: 2026-07-20T03:36:40Z
target_parent: a4ccbe144a2027745e74215e2136dbe6fe610497
authorized_by: LOTO_GUIDANCE_ALIGNMENT_APPROVAL.md item 2
implementer: claude-code
reviewer: codex
---

# CC_Loto Claude-owned minimal alignment — exact-render evidence

## Control

- Target branch: `main`; local HEAD and `origin/main` at published step-1 tip
  `a4ccbe144a2027745e74215e2136dbe6fe610497`; divergence `0 0`; porcelain empty; zero tags.
- Renderer: [`rendered/render_loto_claude_alignment.py`](rendered/render_loto_claude_alignment.py),
  SHA-256 `402689E8526240DB826F40CD62F7B0FE639A05FB98F7A18FE59B122FAAF86135`.
- Exact byte authority:
  [`rendered/loto-claude-alignment/CLAUDE.md`](rendered/loto-claude-alignment/CLAUDE.md).
- Scope: one Claude-owned modification of root `CLAUDE.md`; no other path.
- CC_Loto remained read-only throughout preparation.

## Deterministic renderer

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$lotoTestPython = Join-Path $env:TEMP 'cc-loto-support-venv\Scripts\python.exe'
python doc\support-transfer\rendered\render_loto_claude_alignment.py `
  --native-python $lotoTestPython
```

Exit `0`. A second run reproduced the candidate with zero SHA-256 differences.

## Exact proposed bytes

| Operation | Target path | SHA-256 | Git object |
|---|---|---|---|
| modify, Claude-owned | `CLAUDE.md` | `0DE42FEA59543B2961688ABEA0A0BE67FB7D34499613AC222E5ADEC11CD67A35` | `689a48b669c009baf79f1349e64f352532a5e444` |

Reviewed parent object is `3edd87504e76a97d8ba46ecf40e81b8ad894299f`. Against that blob,
`git diff --no-index --numstat` returns **55 additions and 0 deletions**: the change is a pure
append of one section, and the renderer proves that structurally by requiring
`candidate.startswith(parent_text)` and requiring the appended bytes to equal the reviewed section
exactly. Every pre-existing byte is therefore preserved by construction, not by inspection.

A measurement note, recorded because the first number I produced was wrong: an initial numstat run
compared against a PowerShell-redirected copy of the parent and reported `56 1`. The redirection
altered the file. Comparing against the actual Git blob returns `55 0`. The corrected figure is the
one above; the incorrect one is disclosed rather than dropped.

## Vocabulary pinned to executable authority

The section does **not** transcribe the check-state list. It points at
`support/schemas/handoff.schema.json` and `tools/validate_support.py` as the authority. The renderer
enforces this in both directions:

- it reads the schema blob at the reviewed parent, resolves the `#/$defs/check` reference, and
  requires the enum to equal exactly `passed, failed, skipped, not-run, unknown, not-configured,
  unavailable`, failing if the schema ever admits `blocked`;
- it requires the section to reference the schema path and to state that `blocked` is a
  handoff/blocker state and never a check result;
- it fails if the section contains any of the known defective enumerations, and it fails if the
  section enumerates the states at all, so no prose copy can drift from the schema.

This directly answers the step-1 defect: the wrong enumeration in `AGENTS.md` was a transcription
of a contract that already existed in machine-readable form. This candidate cannot repeat that,
because it has no enumeration to get wrong.

## Ownership and scope guarantees asserted by the renderer

- Codex-owned `AGENTS.md` is byte-identical to its published object in the disposable overlay, and
  the parent `AGENTS.md` object is required to equal `42571a2c...`, so this slice cannot run before
  step 1 is published.
- No synchronization claim may appear in the candidate; the section is required to state the
  opposite precondition.
- Pre-existing product anchors are required to survive: the installable-package rule, `pip install
  -e .`, the corrected packaging sentence, `INDEX_MODE = "event"`, leakage safety, `run_tests.py`,
  and the generated-`Output/` note.
- No `.claude/`, `.agents/`, coordination record, support record, product source, dependency,
  workflow, test, data/model/output, index, tag, or release path is in scope.
