# Enconet Claude Code Guidance

This file extends `../CLAUDE.md` and applies within Enconet.

## Read first

1. `MASTER_DEVELOPMENT_PLAN.md` (v1.4 canonical)
2. `docs/ALIGNMENT_PLAN.md` (canonical — waves G0–G5, acceptance criteria)
3. `decisions/README.md` (ADR register, all preparation decisions ADR-0001…0013)
4. `docs/CX_CC_RECONCILIATION.md` (the CX/CC merge agreement)

Treat `docs/context/` and `docs/_archive/` (superseded plan variants, critiques, session
exports) as historical/source input, not a current implementation contract.

## Current implementation and guardrails

- Working code is under `sieving/src/json_extractor`; tests are under `sieving/tests`.
- Do not run `sieving/tools/fix_files.py` or `fix_structure.py`; their root assumptions are unsafe.
- Do not export after a filter or validation error unless an explicit development override is
  approved and recorded. Fail-closed behavior is implemented (C4.1/C4.2): filter errors block
  export unconditionally; ERROR-severity validation blocks export unless an override reason is
  recorded. Do not weaken these gates.
- The standalone Streamlit GUI was retired by human decision on 2026-07-04. Remove stale GUI
  instructions; do not reintroduce it without a superseding ADR.
- Resolve active paths from project/package roots or explicit configuration, never legacy paths.
- Follow [`docs/RAW_INTAKE.md`](docs/RAW_INTAKE.md) for source intake. It uses one
  controlled doorway: place a reviewed file directly in `incoming/`,
  then run `scripts/promote_source.py` with its registry metadata. Promotion moves it to
  `raw/`, applies a platform read-only mode (Windows read-only attribute / POSIX write bits),
  and registers identical provenance in SQLite and `manifests/raw_sources.csv`. Never edit
  `raw/` files in place; replace them only through a separately reviewed, newly named source.

## Sieving workflows (EPIC18)

- Read `sieving/SIEVING_PLAYBOOK.md` before every sieving run, crumb-quality review, or
  prompt change — it is the mandatory entry point for all sieving work.
- Read `.claude/skills/sieving-run/SKILL.md` before an initial or repeat sieve execution.
- Read `.claude/skills/crumb-quality/SKILL.md` before judging extracted crumb quality.
- Read `.claude/skills/sieving-tuning/SKILL.md` before changing a prompt or deciding a
  candidate generation.
- A prompt promotion or rejection is incomplete until its reusable lesson is deposited
  in the matching skill and linked from `sieving/prompts/CHANGELOG.md`.
- Generations are immutable: new RUN-id per attempt, candidates stay inactive until the
  recorded human decision, downstream stages read `active_crumbs` only.

## Token-efficiency application in this pipeline

Applies the workspace-root permanent token-efficiency goal to Enconet's audit pipeline. Raw
intake and promotion reads stay full and mandatory — extraction accuracy depends on complete
source text, and this section does not relax that.

- For later audit stages (linking, evaluation, report, dashboard), retrieve canonical
  criterion-scoped evidence from SQLite and `active_crumbs` using stable crumb, quote, chunk, and
  provenance references rather than re-reading whole incoming documents or chunk dumps. Escalate
  from compact metadata to exact evidence, adjacent chunks, and finally the full controlled source
  whenever ambiguity, conflict, missing context, broken traceability, or reviewer need requires it.
- Query growing manifests (`manifests/*.csv`) and append-only records (`wiki/log.md`,
  `wiki/evidence/matrix.*`) by stable run/source identifier or the relevant tail/section during
  routine work; read the complete file only at `/audit-close`, `/handoff`, or whenever the full
  history is what the decision actually needs.
- Keep deterministic pipeline work — chunking, quote linking, schema checks, scoring, package
  construction, and report/dashboard rendering — in scripts. Reserve LLM context for semantic
  judgment, exception review, and synthesis that actually requires it.
- For repeat sieving or revised candidate generations, review the generation diff and changed
  crumbs first, proven unchanged by stable identifiers and hashes; fall back to a full comparison
  whenever hashes, lineage, or diff completeness cannot be proven. Full baseline review remains
  required at the applicable approval gate.
- Targeted checks never replace `/audit-validate`, the aggregate suite, or a required gate
  packet; run those in full at the required boundary regardless of what ran during iteration.

## Audit commands (EPIC17)

Run `/audit-status` at session start. Each pipeline stage has exactly one Claude slash
command in `.claude/commands/`; every adapter invokes the canonical dispatcher
`python scripts/audit_command.py <name> -- $ARGUMENTS` (from `Enconet/`;
`audit-status` needs no arguments). The dispatcher derives its contract from
`schemas/audit_commands.yml` and refuses a phase mismatch before starting the stage
process; adapters must never bypass, duplicate, or weaken that check. No command
advances a human gate on its own. `/audit-gate` assembles the gate packet and stops
for the human.

| Command | Stage | Exact allowed phase(s) | Artifacts |
|---|---|---|---|
| `/audit-status` | session/status | `setup, registered, chunked, sieved, evidence_reviewed, evaluated, findings_drafted, findings_approved, report_ready, dashboard_ready, closed, failed` | project phase, gate states, open action count, last validation result |
| `/audit-register` | source registration | `setup` | raw source, manifests/raw_sources.csv row, documents row |
| `/audit-chunk` | chunking | `registered` | document_chunks rows, derived/chunks artifact |
| `/audit-sieve` | initial sieving | `chunked` | sieve_runs row, guarded sieve-run workspace |
| `/audit-resieve` | iterative sieving | `sieved` | inactive candidate generation, quality metrics, and diff against the previous active generation; stop before promotion |
| `/audit-link` | traceability | `sieved` | crumb quote to chunk links |
| `/audit-eval` | evaluation | `evidence_reviewed` | criterion evaluation and evidence links |
| `/audit-report` | report | `findings_approved` | controlled evaluation report |
| `/audit-dashboard` | dashboard | `report_ready` | offline dashboard, wiki dashboard copy |
| `/audit-validate` | validation | `setup, registered, chunked, sieved, evidence_reviewed, evaluated, findings_drafted, findings_approved, report_ready, dashboard_ready, closed, failed` | aggregate PASS or FAIL, manifests/validation_runs.csv unless --no-record |
| `/audit-gate` | human gate | `setup, sieved, evidence_reviewed, findings_drafted, findings_approved, report_ready, dashboard_ready` | one immutable human gate packet; no automatic transition |
| `/audit-close` | session/closeout | `setup, registered, chunked, sieved, evidence_reviewed, evaluated, findings_drafted, findings_approved, report_ready, dashboard_ready, closed, failed` | aggregate verdict, immutable handoff record, HANDOFF.md pointer |

At session end, collect truthful handoff content with the user-global `/handoff`
skill, then publish through `/audit-close`: it validates first (`--no-record`) and
routes publication through `../scripts/make_handoff.py`; validation failure prevents
publication.

## Verification

From `Enconet/sieving`, after dependencies are installed:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -q -p no:cacheprovider
$env:PYTHONUTF8='1'
python verify_install.py
```

Use the `/handoff` skill (user-global, `~/.claude/skills/handoff/`; ADR-0014) to close,
pause, or transfer a session. Use `../scripts/make_handoff.py` to render, validate, and
atomically publish the handoff record and pointer (C3); the skill remains the
evidence-collection and status contract. Record dependency, encoding, Git, test, and
index failures explicitly.

## Evidence Access interpreter (EVIDENCE-ACCESS-TDD)

Commands under `docs/EVIDENCE_ACCESS_TDD_PLAN.md` — anything touching
`evidence_resolver.py`, `generate_evidence_bundle.py`, `browser_harness.py`,
`generate_review_catalog.py`, `generate_review_workspace.py`, `build_review_package.py`,
or their tests/validators — must run from the pinned Conda interpreter
`C:\xPY\vEnv\WikiEnconet\python.exe` (ADR-0023/ADR-0024/ADR-0025), not the default
interpreter: `sieving/requirements.txt` now also pins Playwright for this feature, and
the default interpreter noted in the workspace-root `CLAUDE.md` (C5.3) does not have it
installed. The unqualified `python` above in `## Verification` and in
`.claude/commands/audit-*.md` is unaffected by this note and needs no change: neither
the sieving pytest suite nor the generic EPIC17 audit-pipeline dispatcher imports
Playwright or any other evidence-access-only dependency, and both were independently
reproduced passing from the default interpreter on 2026-09-04.

