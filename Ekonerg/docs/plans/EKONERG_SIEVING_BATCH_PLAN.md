# Ekonerg sieving batch plan

**Status:** Codex working plan; not yet executed.

This plan keeps the reading load steady while protecting source boundaries. It
does not activate prompts, create crumbs, or approve audit results. The owner
does not need to approve the size of a batch. Codex may adjust a group when the
source text shows that the estimate is wrong, and records a short reason.

## Sizing rule

- Aim for about **30–50 reading pages per batch**.
- Small documents of about 10 pages are normally grouped in **triplets**.
- Medium documents of about 15–30 pages are normally grouped in **pairs**.
- Large documents over 40 pages are processed as **one-document batches**.
- A user-prepared document over 100 pages remains one batch.
- Page estimates are workload hints only. Chapter and heading paths remain the
  evidence locators.

## Estimate limits

QMS estimates below count embedded `_page_N_` markers in the Markdown copies.
Regulatory estimates use the page ranges in the approved filenames where
available. A missing estimate is marked **unknown**; Codex resolves it during
the pre-run check and records the rationale.

## Regulatory batches

Regulatory sources remain separate because their authority roles differ.

| Batch | Documents | Estimate | Codex rationale |
|---|---|---:|---|
| R-01 | DOC-0001 — 10 CFR Part 21 | unknown | Keep Part 21 separate for nonconformance and corrective-action scope. |
| R-02 | DOC-0002 — 10 CFR 50 Appendix B | unknown | Keep the governing Appendix B source separate. |
| R-03 | DOC-0003 — NQA-1 preface | ~14 pages from filename range | Keep the interpretation source separate. |
| R-04 | DOC-0004 — NQA-1 Part 1 | ~33 pages from filename range | Boundary-size source; one batch avoids mixing mandatory Part 1 text. |
| R-05 | DOC-0005 — NQA-1 Part 2 | ~82 pages from filename range | Large source; one batch. Part 2 is not mandatory by default. |
| R-06 | DOC-0006 — NQA-1 Part 3 | ~78 pages from filename range | Large source; one batch. |
| R-07 | DOC-0007 — NQA-1 Part 4 | ~109 pages from filename range | Very large source; one batch. |

## QMS batches

These groups keep related procedures together. The estimates are lower bounds
when a page marker is missing, so Codex rechecks them before execution.

| Batch | Documents | Marker estimate | Why grouped |
|---|---|---:|---|
| Q-01 | DOC-0031 manual; DOC-0011 PQ07.5-2; DOC-0016 PQ07.5-7 | 26 | Manual, quality-system procedures, and records. |
| Q-02 | DOC-0021 PQ08.2-2; DOC-0020 PQ08.2-1; DOC-0022 PQ08.3-1 | 22 | Contract, customer, and project-work controls. |
| Q-03 | DOC-0014 PQ07.5-5; DOC-0029 PQ10.2-1; DOC-0030 PQ10.2-2 | 21 | Document control, nonconformance, and corrective action. |
| Q-04 | DOC-0008 PQ06.1; DOC-0027 PQ09.2; DOC-0028 PQ09.3 | 15 | Risk, checks, and quality-system review. |
| Q-05 | DOC-0012 PQ07.5-3; DOC-0013 PQ07.5-4; DOC-0026 PQ08.6 | 14 | Control and verification procedures. |
| Q-06 | DOC-0018 PQ08.1-2; DOC-0019 PQ08.1-3; DOC-0017 PQ08.1-1 | 12 | Quality, project, and activity planning. |
| Q-07 | DOC-0024 PQ08.4-2; DOC-0025 PQ08.4-3; DOC-0023 PQ08.4-1 | 7 | Purchasing, supplier choice, and project-study controls. |
| Q-08 | DOC-0009 PQ07.1-1; DOC-0010 PQ07.1-2; DOC-0015 PQ07.5-6 | 7 | Training, measurement equipment, and received documents. |

The QMS groups below the 30-page target are intentional: the available files
are short, and the three-document limit protects review quality. Codex may
re-group them after inspecting chapter structure, without changing source
hashes or evidence identifiers.

## Execution gate

Before any batch is run, Codex must record the source hashes, prompt version,
document IDs, chapter range, page estimate, and batch rationale. This plan is
not evidence and does not bypass the empty prompt registry or golden-set gate.

## Pre-run check — 2026-10-03

- Batch coverage: **PASS** — 31 planned IDs match 31 registry rows (7 RULE,
  24 DOCUMENT).
- `python -B scripts/validate_raw_sources.py --db db/nqa_audit.sqlite`:
  **PASS**.
- `python -B scripts/validate_chunks.py --db db/nqa_audit.sqlite --no-record`:
  **PASS** — all 411 chunks verified.
- `python -B scripts/validate_sieving_harness.py --allow-pending-claude`:
  **expected gate stop** — active RULE and DOCUMENT prompts are empty; the
  golden calibration set is pending human approval.

No batch has been executed and no crumb has been created.
