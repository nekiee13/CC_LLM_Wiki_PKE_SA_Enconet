# Priručnik re-sieve: source check and recall defects

Date: 2026-10-06. Document: DOC-0031, `Priručnik_sustava_upravljanja_rev.5.md`.

Status: complete re-sieving is blocked by missing source text. The full supplied
318-line file has been read. This record is a source check, not a completed
re-sieve or approval of a new generation.

The owner requested a thorough re-sieve of the whole manual. Task 3 (Astra /
UMBRA dark-mode work) is paused until task 1 is finished. Task 2 (empty dashboard
matrix) remains requested; no dashboard code was changed in this source check.

## What is available

Both `incoming/` and `raw/` copies have 14,550 bytes, 318 lines, and this SHA-256:

`cd2e60b5b67229ac02dbd92d6637780d1e12b0491b11a54d37bc78fdd6d635a0`

This equals the registered DOC-0031 hash. The database has 17 chunks. Each chunk
matches its source character range; the chunks cover offsets 0 through 14,259.
Concatenating them exactly reconstructs the full text read from the raw file.
The missing material was therefore already absent from the supplied Markdown;
the current chunking did not discard it.

Lines 35–113 contain the contents list. The body starts at line 117 and ends in
Chapter 3 at the definition of quality assurance (lines 316–318). Chapters 4–10
and the attachments are not present as body text. The empty `Kvalifikacija
osoblja` heading is another sign of incomplete source extraction.

A filename search of the workspace found only the Ekonerg incoming/raw manual
copies plus a different Enconet manual. No complete Ekonerg manual or ROS-02 was
found under those names. No replacement source was registered or inferred.

## Owner's source map checked against this file

| Criterion | Requested passage | Available here |
|---|---|---|
| VIII | 8.5.5; Dodatak 1, point 8 | Only the 8.5 contents entry and Dodatak 1 title; detailed text absent. |
| IX | Chapter 3 | Definitions are present, including qualified procedures; usable supporting clues were missed. |
| IX | 8.5.2; Prilog 5; Dodatak 1, point 9 | Detailed text absent. Prilog 5 and Dodatak 1 are named only. |
| XI | 9.1.4; Dodatak 1, point 11; ROS-02 | Detailed text absent; no registered ROS-02 document found. |
| XIII | 8.5.5; Dodatak 1, point 13 | Detailed text absent. |
| XIV | Dodatak 1, point 14 | Detailed text absent. |

The owner's questions about coatings, concrete, epoxy/cement mixes, VT of
non-metal surfaces, and carbon laminates remain review questions. They are not
quotes or findings extracted from this incomplete manual. Procedure codes RUT,
RMT, and RPT do occur in `PQ07.5-4_r6_Radni_postupci.md`; that is a different
document and must keep its own source identity.

## A separate defect in the previous re-sieve

The active generation is `RUN-20261003-39`: 18 crumbs, prompt v2. The inactive
candidate is `RUN-20261005-76`: 32 crumbs, labelled prompt v3.

Inspection of `scripts/rerun_document_v3_candidates.py`, function `prepare`,
shows that it:

- copies existing items;
- searches only five criteria (VIII, IX, XI, XIII, XIV);
- skips a criterion if the old output already has a crumb for it;
- skips source lines shorter than 25 or longer than 700 characters;
- excludes a quote once used, even for another criterion;
- stops after four added items per criterion.

This is a limited keyword expansion. It does not implement the active v3
prompt's two semantic passes over every chapter and all 18 criterion concepts,
with no fixed crumb cap. The earlier description of this as a full v3 re-sieve
was too strong. Source incompleteness and limited extraction are separate
defects; both must be addressed.

## Examples missed in the available text

These are reviewable source passages, not new imported crumbs or conformance
decisions. Definitions support possible mappings but do not prove execution.

| Source | Exact quote | Meaning to examine |
|---|---|---|
| Chapter 3, Kvalificirani postupci | Postupci koji su dokazano provjereni za odgovarajuću namjenu uz poštivanje svih primjenjivih propisa, standarda i tehničkih specifikacija. | IX: a defined concept of qualified procedures; check the missing process-specific details. |
| Chapter 3, Kontrolni postupci | Pisani i odobreni postupci koji detaljno opisuju način provedbe kontrole neke aktivnosti koju izvodi treća osoba (organizacija). | V / VII / X: approved written control methods and checking of third-party work. |
| Chapter 3, Nabavna dokumentacija | Ugovorna dokumentacija, kojom se određuju zahtjevi kojima proizvod ili usluga moraju udovoljiti da bi se smatrali prihvatljivim od strane Naručitelja. | IV: procurement documents carry requirements for acceptance. |
| 1.1, laboratory list | - - Ispitni laboratorij | XI: an identified testing activity; method, limits, and results still need their own evidence. |

The prior payload also uses `document.date: 2019-01-30`, while this source's
cover states preparation on 17.04.2023 and review/approval on 24.04.2023. The
registered database date is unknown. A fresh payload must use supported date
context and must not copy the unsupported old payload date.

## Next action

Obtain the complete revision 5 Markdown or original PDF from the owner, including
the chapters and attachments listed above. Preserve the currently registered
source and record the complete copy's provenance. Then read every substantive
section twice under the existing v3 prompt, record chapter coverage, check every
quote against the source, and prepare a new reviewable candidate/diff. Do not
describe table-of-contents headings as the missing chapter bodies.

The existing active generation, candidate, evidence links, and ratings are
unchanged. The full re-sieve remains open; no dark-mode work has started.
