# All-files keyword sweep and replacement manual

Date: 2026-10-06. Implementer: Codex. Claude review: pending.

## Scope and result

The owner supplied a replacement manual and requested a full keyword sweep of
all files. The sweep reads all 31 registered Markdown files in `incoming`:
24 vendor QMS files and 7 regulatory/reference files. It checks all 18 Appendix B
concepts. It does not stop at four hits, skip a criterion with old crumbs, or
drop short or long quotes. It does not copy old crumbs into the new results.

The published bundle is
[full-keyword-sweep-verified](../../out/2026-10-06/full-keyword-sweep-verified/README.md).
The full quoted manual leads are in
[DOC-0031](../../out/2026-10-06/full-keyword-sweep-verified/review/DOC-0031.md).
Every document has a quoted Markdown file, JSON with exact offsets, a full source
snapshot, and a coverage ledger. The ledger includes blocks with no keyword hit.

This completes the **keyword pass**, not the full two-pass semantic re-sieve
required by `appb_document_v3_context_anchors`. The new method has its own name,
`full_keyword_sweep_v1`; it does not claim to have run that LLM prompt.

Hits are evidence leads, not approved findings. A source paragraph can support
more than one criterion. Count its text once and count its criterion links
separately. Table headings, definitions, cross-references, and environmental or
safety passages can be leads without being objective nuclear QA controls.
Keyword absence is not proof of missing evidence. The unmatched blocks still
need semantic review, as do the matched passages.

### Verified counts

| Source set | Files | Passage locations | Distinct quote texts per document | Criterion links |
|---|---:|---:|---:|---:|
| Vendor QMS | 24 | 2,892 | 2,669 | 6,890 |
| Regulatory/reference | 7 | 2,992 | 2,959 | 6,757 |
| Manual only, included in vendor total | 1 | 1,359 | 1,250 | 2,931 |

The vendor total includes the manual; do not add it again. Distinct text counts
are summed per source document, not globally across different documents. They
are not counts of approved crumbs. There are also 438 unmatched vendor content
blocks, including 187 in the manual, retained for semantic review. The active
database still has 214 vendor crumbs. No new sweep leads have been imported.

Final manifest SHA-256:
`68214ed980ca3e22c339c0d7efa80a54072770dcb3c0b3da9b0ac15ea932f2df`.

## Replacement source

Only DOC-0031 changed in `incoming`. Its full revision 5 file has 227,530 bytes
and 3,180 lines. The previously registered copy has 14,550 bytes and 318 lines.

| Copy | SHA-256 |
|---|---|
| Replacement, snapshotted in this bundle | `9492b447c386d174ca6fd7a473999a4999899523ae21570a81626ffadfdeae87` |
| Old registered raw copy, retained | `cd2e60b5b67229ac02dbd92d6637780d1e12b0491b11a54d37bc78fdd6d635a0` |

The source-availability blocker is resolved by the owner's replacement and this
inspection. The old source, chapter rows, active runs, candidate runs, evidence
links, and scores have not been overwritten. New quotes must not be attached to
old DOC-0031 database chapters. The replacement still needs revision-aware
intake before new crumbs can be imported with correct chapter links.

## What the owner's five examples now show

These are Codex's source-based interpretations of selected passages. They do not
change a criterion score. Source line numbers below point to the full snapshot,
not to pages. The chapter is the main locator.

| Criterion | Source location | What it says and what remains to check |
|---|---|---|
| VIII: identification | 8.5.3, line 1142; 8.5.5, lines 1154–1166; Dodatak 1, point 8, line 1825 | The manual says projects, studies, and related records stay traceable through work-order numbers and document IDs. It also lists identification as part of product protection. Nuclear status marking is to be defined in a specific document as needed. There is evidence here; actual project markings need their own support. |
| IX: special processes | Chapter 3 definitions; 8.5.2, lines 1136–1138; Prilog 5, lines 1656–1677; Dodatak 1, point 9, line 1829 | The manual defines qualified procedures and calls for validation/control if special processes are used. Prilog 5 lists visual, penetrant, magnetic-particle, and ultrasonic procedures. A procedure title is a useful lead, but not its full method or a qualification record. |
| XI: testing | 9.1.4, line 1257; Dodatak 1, point 11, line 1837; Prilog 5, line 1686; Dodatak 1 / Prilog 1 notes, lines 1887 onward | The manual says it does not test its own services/products. It also says testing for a customer needs a program, procedures, requirements, acceptance criteria, conditions, and evaluation of results. Keep both parts of that statement. Software checks and the ROS-02 reference are further leads. No standalone ROS-02 source is in the 31-file intake. |
| XIII: handling, storage, shipping | 8.5.5, lines 1154–1166; Dodatak 1, point 13, line 1845 | Measures include handling, storage, cleaning, packaging, protection, and transport. The text calls for special marking, checks, tools, and trained handlers where conditions require them. This is substantive documented control, not an empty heading. |
| XIV: status | Dodatak 1, point 14, line 1849; 9.1.4, lines 1245–1247 | Nuclear inspection/test/operating status marking is to be set out in a specific document when needed. Release records must identify who authorized delivery. The conditional plan for marking must not be presented as proof that every status-control document already exists. |

### Exact example: special processes

8.5.2, line 1138:

> Ukoliko bi se koristili neki drugi procesi pružanja usluga/isporuke proizvoda EKONERG-a kod kojih se eventualni nedostaci mogu uočiti tek nakon korištenja usluge/proizvoda, EKONERG će primijeniti mjere za validaciju i nadzor takvih procesa kao "specijalnih procesa".

### Exact example: test control

9.1.4, line 1257:

> EKONERG ne obavlja testiranja svojih usluga/proizvoda. Kada se obavljaju ispitivanja (testiranja) za Naručitelja uspostavit će se program ispitivanja (testiranja), kao i postupci koji će sadržavati zahtjeve ispitivanja, kriterije prihvatljivosti te uvjete ispitivanja. Postupcima će se također definirati dokumentiranje i evaluacija rezultata ispitivanja.

### Exact example: preservation

8.5.5, line 1166:

> Naglašena pažnja posvećuje se proizvodima za koje je naveden način čuvanja (čistoća, pakiranje, tlak, temperatura, vlaga, ...). Takvi proizvodi se posebno označavaju, provode se povremene kontrole ispunjavanje navedenih zahtjeva i za to se koriste posebni alati i posebna oprema za rukovanje. Ako postoje posebni zahtjevi za očuvanje proizvoda/opreme oni se definiraju Planom kvalitete za radni nalog/projekt, uključujući i iskustvo i osposobljenost rukovalaca za specifičnu opremu.

The owner's questions about coatings, concrete, epoxy/cement, non-metal visual
testing, and carbon laminates remain scope/evidence questions. We have not
turned those questions into source statements or assumed these activities are
performed by Ekonerg.

## Why this differs from the earlier output

Two problems reduced recall: the old supplied manual ended in Chapter 3, and
`rerun_document_v3_candidates.py` searched only five criteria with a four-hit cap
for criteria that had no old crumb. That legacy helper is not used for this run.
Do not use it as a full semantic v3 runner.

The new sweep uses Croatian and English word stems, synonyms, procedure codes,
and the nearest chapter heading. It includes tables and appendices. It preserves
each exact quote and its source hash. Printed clause numbers control the chapter
hierarchy because the converted Markdown uses inconsistent heading levels.
Plain appendix references do not become parent chapters.

The preliminary bundles `full-keyword-sweep-v1` and `full-keyword-sweep` were
inspection runs. They are superseded because their chapter-parent parsing was
not reliable. Retain them only as work history; use `full-keyword-sweep-verified`.

## Remaining work — one coherent continuation

Finish the existing re-sieve task, not a new series of scope expansions:

1. Record the replacement as a new source revision, with new chapter identities,
   while preserving old evidence and generations.
2. Complete the semantic passes over matched and unmatched source blocks. Merge
   duplicate evidence, preserve conditional wording, follow cited documents
   where present, and prepare exact-quote candidate payloads and generation diffs.
3. Use the existing import/promotion controls. Update the evidence matrix and
   recompute the established five-point scores from accepted evidence. The owner
   already authorized documentation-based official results without a judgment
   entry form; do not invent another human-rating gate.

Task 2, the empty evidence matrix, remains open. Task 3, the UMBRA/Astra design
trial, remains paused until the manual re-sieve is finished. No GUI was changed.

## Validation and boundaries

- TDD red: `python -m pytest Ekonerg/scripts/tests/test_full_keyword_sweep.py -q -p no:cacheprovider`
  exited 1 before the scanner existed. Final rerun exited 0: 13 tests passed.
  One intermediate sandbox run had 7 passes and 5 temporary-directory permission
  errors. The rerun outside that restriction passed; no failure was hidden.
- `python Ekonerg/scripts/full_keyword_sweep.py --output Ekonerg/out/2026-10-06/full-keyword-sweep-verified`
  exited 0. It checked every quote against its exact character range, accounted
  for every source character, and reproduced the matches from saved rules.
- `python Ekonerg/scripts/run_all_validations.py --no-record` exited 0:
  8 phase-applicable checks passed. Evaluation, report, dashboard, and related
  later-phase checks were skipped by the current `evidence_reviewed` phase.
  This result does not certify an updated dashboard or new audit score.
- A read-only source check confirmed all three quotations printed in this note
  are exact. Chapter parents for the owner's cited passages were inspected in
  the final bundle.
- The live database hash before and after the verified sweep is
  `2aba6d844bb609da85eef77aac2b5155d2bc5ccee02a5059af70c50f5e5b231f`.
  The bundle records before/after checks for `db`, `incoming`, `raw`, and
  `sieving/DATA`, plus the source registry. It does not write to any of them.
- The final bundle is reproducible with its saved `scanner.py` and `rules.json`.
  Its verification command is `python Ekonerg/scripts/full_keyword_sweep.py --verify Ekonerg/out/2026-10-06/full-keyword-sweep-verified`.

No company name, document ID, or approval is embedded in the sweep algorithm.
Tests cover two synthetic company names (including spaces and Croatian letters),
with and without a sibling tree. No sibling files change. The scanner is local
to this project and does not read another company's runtime or evidence.
