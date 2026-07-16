# Good practices — patterns proven in this workspace

- **Scope:** working patterns that have already earned their keep here, each with the
  evidence that proved it. Add a pattern only after it has actually prevented or
  caught a problem in this workspace.
- **Authority:** ADR-0021 defines the proof threshold, stable identifiers for new
  entries, active/deprecated/superseded lifecycle, and links to lessons learned.
- **Owner:** shared (either agent under the coordination protocol).
- **Update trigger:** a pattern demonstrably works (or a listed one fails and must be
  demoted to `LESSONS-LEARNED.md`).

## Provenance + divergence log for vendored code

`Enconet/sieving/PROVENANCE.md` records the upstream repo, exact commit, vendor date,
the ownership decision, and a dated table of every local modification with rationale
and the recovery commit. This made the GUI-retirement decision (2026-07-04)
reconstructible months later and settled the CX/CC disagreement about it
(`Enconet/docs/CX_CC_RECONCILIATION.md` §2.2.1). Apply the same pattern to any future
vendored component.

## Code verification before structural claims

Never act on heuristic tool output alone. The dead-code report on
`sieving/src/json_extractor` was materially false-positive; jcodemunch
reference checks (`find_importers`, reference queries) proved
`flatten_multiple_files`, `export_dataframe`, `discover_json_files`, and `QueryEngine`
live through `__init__` re-exports (reconciliation §2.2.2). Rule: confirm with
reference/importer queries or grep before any deletion.

## Checksummed manifests for untracked evidence

`Enconet/sieving/DATA/` is never tracked (ADR-0002), but
`Enconet/sieving/DATA_MANIFEST.json` (SHA-256 per file) is, and
`Enconet/sieving/tools/verify_data_manifest.py` machine-verifies it
(last run 2026-07-11: OK, 68 files). Integrity without tracking.

## Anchor-based guidance drift validation

Equivalent rules in the CLAUDE.md/AGENTS.md pairs are enforced as regex anchors that
must match both sides (`doc/GUIDANCE_PAIRS.json` + `scripts/check_guidance_drift.py`,
Task C2.1); intentional tool-specific differences are declared, silent divergence
fails. First real run immediately surfaced three wording mismatches (line-wrap
artifacts) and existing Codex-side staleness.

## Repository as coordination channel

Cross-agent requests travel as immutable author-prefixed messages plus explicit task
claims (`Enconet/coordination/`, ADR-0017/0018, `scripts/agent_coord.py`). No shared
mutable state, no editing under another agent's claim, and archival only after
resolved-and-confirmed — silence is not confirmation.

## Failing test first, then the implementation

C5.2's runner contract tests were written and demonstrably failing before
`run_validation.py` existed (2026-07-12); C4.5's docs smoke test immediately caught
two stale documented commands the moment it ran. Rule (ALIGNMENT_PLAN C5.2): every
implementation task starts from a failing test or validator demonstrating the gap.

## Layered aggregate validation with SKIPPED ≠ PASS

`scripts/run_validation.py` runs L0–L5 (syntax → structure/authority → unit →
integration → golden regression → handoff recovery), exits non-zero naming the failed
layer, and treats any skipped layer as exit 3, never as success. Its first real run
caught a stale BOARD and a nonconforming handoff record (see `LESSONS-LEARNED.md`).
Report output is deterministic (no timings or absolute paths in the verdict lines).

## Evidence-or-it-didn't-happen reporting

Never report skipped, blocked, or unrun validation as passed (workspace guidance;
handoff skill: per-check states `passed|failed|not-run|unknown`). Handoffs and task
completion messages cite commands, exit codes, and counts.

## GP-RAW-001 — One controlled doorway from `incoming/` to immutable `raw/`

- **Status:** active
- **Date recorded:** 2026-07-16
- **Scope/area:** Enconet source intake, identity, and provenance
- **Proposition:** Populate `raw/` only through `scripts/promote_source.py`. Place one
  reviewed source with a stable, unique filename in `incoming/`; initialize the DB if
  necessary; promote it with title, supplier, document date, language, side, and any
  source URL/notes; then extract text by the allocated document ID and run the
  raw-source validator. Revised documents repeat the process under a new reviewed
  filename and receive a new document ID—nothing in `raw/` is edited in place.
- **Evidence:** The direct-to-`raw/` requirements-document incident demonstrated the
  violation this pattern prevents. EPIC3 tests prove promotion atomically moves the
  source, assigns `DOC-nnnn`, writes identical DB and CSV provenance, hashes and locks
  the file, rejects duplicate names/checksums, and makes unregistered raw files visible.
  `python Enconet/scripts/validate_raw_sources.py` returned exit code 0 on 2026-07-16
  for the reconciled controlled set.
- **Value:** Every downstream artifact can resolve a stable document ID to immutable
  source bytes and matching human-readable/machine-readable provenance. Bulk intake
  remains auditable because each source crosses the same reviewed, fail-closed gate.
- **Owner/next action:** All source-intake operators; use the documented command below
  per file and do not begin extraction, chunking, or sieving until validation passes:

  ```powershell
  # From Enconet/
  python scripts/promote_source.py <filename> --title <title> --supplier <supplier> --doc-date YYYY-MM-DD --language <sl|en|hr> --side <RULE|DOCUMENT>
  python scripts/extract_text.py DOC-nnnn
  python scripts/validate_raw_sources.py
  ```

- **Links:** ADR-0021; ADR-0022; `LL-RAW-001`; EPIC3 Tasks 3.1–3.4;
  `Enconet/docs/RAW_INTAKE.md`; `Enconet/tests/test_raw_intake.py`.
