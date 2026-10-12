# Ekonerg documentation audit — 6 October 2026

**Result: 66.7% — partially matched.**

The approved five-point model gives **1,200 / 1,800 points**. All 18 criteria
are evaluated: 12 substantial and 6 partial. None is withheld or marked unmet.
These are official documentation-audit results under the owner's instruction.
They identify where a later field audit should look more closely; they do not
claim that the controls were observed working on a job.

[Open the results dashboard](EKONERG_DASHBOARD.html).
[Read the evidence-count matrix](evidence-matrix.md).
[Read all 18 assessment explanations](../../../docs/reviews/MANUAL_REFRESH_ASSESSMENT_20261006.json).

## What changed

The full manual now has 279 active crumbs in RUN-20261006-77, replacing the
incomplete copy's 18. Total active vendor evidence is **475 crumbs**. There are
379 links from vendor controls to criterion scores. The manual's 68 candidate
leads remain visible in the evidence pool but do not support scores. Counts
are not a scoring formula.

| Criterion | Previous points | Current points | Level |
|---|---:|---:|---|
| I Organization | 75 | 75 | 4/5 — substantial |
| II QA program | 75 | 75 | 4/5 — substantial |
| III Design control | 75 | 75 | 4/5 — substantial |
| IV Procurement documents | 50 | 75 | 4/5 — substantial |
| V Instructions and procedures | 75 | 75 | 4/5 — substantial |
| VI Document control | 100 | 75 | 4/5 — substantial |
| VII Purchased items and services | 75 | 75 | 4/5 — substantial |
| VIII Identification | 0 | 50 | 3/5 — partial |
| IX Special processes | 0 | 50 | 3/5 — partial |
| X Inspection | 75 | 75 | 4/5 — substantial |
| XI Test control | 0 | 50 | 3/5 — partial |
| XII Measuring/test equipment | 50 | 50 | 3/5 — partial |
| XIII Handling/storage/shipping | 0 | 75 | 4/5 — substantial |
| XIV Inspection/test/operating status | 0 | 50 | 3/5 — partial |
| XV Nonconforming items | 50 | 50 | 3/5 — partial |
| XVI Corrective action | 75 | 75 | 4/5 — substantial |
| XVII QA records | 100 | 75 | 4/5 — substantial |
| XVIII Audits | 75 | 75 | 4/5 — substantial |

The prior score was 52.8%. Five former zero scores came from missed source
content. The full manual supplies real controls for them. It also exposes
inconsistent procedure references, so document and record control are no
longer full matches. Procurement-document coverage is more complete.

## Main follow-up areas

- **VIII:** obtain the nuclear item-identification plan and applicable marking,
  storage-identity and limited-life controls.
- **IX:** examine the actual special-process methods and qualification rules.
  Do not infer their contents from RVT/RPT/RMT/RUT titles. Clarify whether
  coatings, concrete, mixtures or other special work is in Ekonerg's contract.
- **XI:** examine customer test prerequisites, acceptance rules and records,
  plus the actual software-verification method. Resolve the ROS-02/ROS-03 link.
- **XII:** confirm equipment-to-use traceability and review of prior results
  when equipment is out of calibration. The allowed commercial-device
  exception is not itself a failure.
- **XIV:** obtain the nuclear status-marking rules, including marking authority,
  prevention of bypass and operating-status controls where applicable.
- **XV:** confirm technical justification and design treatment for repair or
  use-as-is dispositions, evaluator competence and required as-built updates.

## Validation and history

The approved source switch and all 18 assessments were applied in one
transaction. Old raw text, chapters, crumbs and generations remain unchanged.
The prior assessments and their exact links are kept in database history and
[before.json](transition/before.json). The [receipt](transition/completed.json)
records database hashes. A repeat apply returned `already_applied`.

The 68-test regression command passed before and after activation. One
sandboxed repeat failed at temporary-folder setup; its approved rerun passed.
The eight phase-applicable aggregate checks passed. Evaluation validation was
run separately and passed for all 18 rows. Inactive score links: 0. Foreign-key
errors: 0. Candidate leads linked as score support: 0.

The empty matrix defect was reproduced by a failing test: radar removal also
removed the cards/matrix startup call. That call is preserved now. Structural
dashboard tests pass. Browser interaction checks did **not** complete: Chrome
and Edge relaunched without returning DOM output, and a removed temporary
profile caused a warning. The two test processes were closed; the failed helper
was removed. The failed check records are retained. Mobile interaction and
print/PDF output are not claimed as browser-verified.

All 31 sources have had the keyword sweep. Only the manual has completed the
new full semantic review. The other 23 vendor documents retain their earlier
reviewed generations and are next. The separate dark-mode trial was not started.
Claude review is pending; no further owner decision is needed for this switch.
