# Ekonerg audit framework: detailed work summary

Date: 7 October 2026. Prepared by Codex for the owner.

## 1. What the framework now does

The framework reads a supplier's quality management documents, gathers traceable
evidence, compares that evidence with the audit requirements, and presents the
results. It is a documentation audit and a guide for the later on-site audit.
It does not claim that a written procedure proves that work was performed.

The common audit question is whether the supplier's QA system meets **10 CFR 50
Appendix B**, using **ASME NQA-1** to interpret the duties. Each supplier has its
own scope, sources, editions, evidence, decisions, ratings, and results.

The owner clarified that the tool must evaluate the documentation and show the
result. It must not withhold the score until a person fills in a judgment form.
The owner also permitted the recorded results to be treated as official audit
results without a further human-rating step. This does not replace a real audit
of implementation, nor does it transfer approvals to another company.

## 2. Current Ekonerg result

| Measure | Current result |
|---|---:|
| Active vendor crumbs | 475 |
| Links from criteria to score-supporting vendor crumbs | 379 |
| Exact active quote-to-chapter link rows | 558 |
| Registered raw sources with verified hashes | 32 |
| Appendix B criteria evaluated | 18 |
| Total criterion points | 1400 / 1800 |
| Overall conformance | 77.8% |
| Fully matched | 3: IV, V, XVI |
| Substantially matched | 14 |
| Partially matched | 1: IX |

These counts measure different things. One crumb can have more than one quote
or chapter link. Some collected crumbs are not used to support a score. Keyword
search leads are not included as accepted crumbs simply because a word matched.

Run: `RUN-20261003-32`. Latest all-criterion review:
`ALL18-REVIEW-20261007-01`. These are Ekonerg results, not a reusable vendor target.

Current light dashboard:
[EKONERG_DASHBOARD.html](../out/2026-10-07/all18-review/EKONERG_DASHBOARD.html).
Owner-accepted dark copy:
[EKONERG_DASHBOARD_DARK.html](../out/2026-10-07/dark-dashboard/grid/EKONERG_DASHBOARD_DARK.html).

## 3. Sieving: from a narrow search to a broad evidence search

### The original problem

The early vendor evidence count was too low. A key cause was the poorly covered
or incomplete management manual. The owner pointed to concrete chapters and
appendices that contained useful controls for identification, special processes,
test control, handling, and inspection/test status.

The owner then supplied a fuller manual. The framework preserved the old source
and registered the replacement as a new source. The complete manual is
`DOC-0032`; it supersedes the incomplete `DOC-0031` intake. The approved new
manual generation is `RUN-20261006-77`. Old source history was not erased.

### What changed

The DOCUMENT method now uses two passes through every chapter:

1. Find direct controls: who does what, what must be checked, who approves it,
   what is accepted, and which records must be kept.
2. Ask which quality goal the text supports. Compare its meaning with the
   intent cards for all 18 Appendix B criteria.

The method uses broad keywords and semantic judgment. There is no fixed crumb
quota and no rule to stop after a few strong examples. A passage can support
more than one criterion when it contains separate control ideas.

The active DOCUMENT prompt is `appb_document_v3_context_anchors`. Its companion
concept cards explain each criterion in plain language. The keyword sweep
preserves a coverage record, source offsets, exact passages, and unmatched text.
Unmatched text still needs reading: no keyword match does not mean no evidence.

### What “fuzzy logic” means here

The search can recognize a control even when the document uses different words
from the regulation. For example, a review-and-release rule may support status
control even if it never says “Criterion XIV.”

This is high-recall semantic matching. It is **not** a formal fuzzy analytical
hierarchy process (FAHP). The owner deferred FAHP. No FAHP weights or new rating
categories were introduced.

### Safeguards kept

Concrete controls, indirect support, and candidate leads remain distinct.
A high-level reference to a standard is a useful lead, not proof that every
detail is implemented. More crumbs alone do not mean a higher score.

Quotes must remain exact. Sources and chapter locations must support the claim.
Fuzzy meaning does not permit fuzzy quotations, invented controls, guessed
context, or copied evidence from regulatory documents.

Versioned prompts, golden fixtures, inactive candidate generations, metrics,
diffs, and recorded promotion/rejection decisions remain part of the method.
The approved calibration examples helped prevent both missed evidence and
overclaiming. Document batching is a quality aid, not a rigid quota: the owner
left sizing to Codex, with roughly 30–50 pages as a useful working target.

## 4. Evidence and chapter traceability

The owner confirmed that documents are stored and reviewed by **chapter**, not
by page-ID records. The evidence chain is now visible to the dashboard user:

`criterion rating → supporting crumb → exact quote → source chapter → registered source`

Clicking a crumb opens its quote and chapter text inside the offline dashboard.
The display keeps the source filename, chapter heading, chunk ID, quote ID, and
locator visible. This lets the auditor check a claim without guessing which
document section it came from.

Strict quote repairs addressed non-verbatim text and wrong or weak links. Raw
source hashes remained unchanged. One owner-approved quote-only migration
changed active quote records in place; its before/after database hashes and
provenance were recorded as an explicit exception to generation immutability.
It is not permission for future silent edits.

Two flawed inactive candidates were rejected and retained for history. Fresh
exact-quote candidates were imported, reviewed, approved, and promoted instead.
This fixed the evidence without using known defective generations.

## 5. Regulatory baseline and scope

The supplied regulatory sources include Appendix B and the fuller ASME NQA-1
material. Their presence widened the available interpretive baseline; it did
not make every part of NQA-1 mandatory.

The owner's scope decisions for Ekonerg were:

- Ekonerg is the only audited supplier. Other firms are checked only through
  Ekonerg's controls over quality-affecting supplier work.
- Activities are deduced from the vendor documents, including design,
  engineering services, and consultancy. Vague scope must be flagged.
- NQA-1 Part 1 is mandatory within the selected audit basis. Part 2 is not
  automatically mandatory; not all NQA-1 provisions have the same status.
- Applicability must be explained. Ekonerg's approved matrix includes all
  18 Appendix B criteria.
- Part 21 is applicable, with particular importance for nonconformances,
  corrective action, and the reporting route.

Part 21 remains separate from the Appendix B score. A full rating for XVI is
not a finding of full Part 21 compliance. The customer-notification text does
not, by itself, prove the complete applicable reporting route. That is still
an explicit real-audit verification point.

Historic Ekonerg audit reports were read as comparison aids. They helped locate
referenced procedures and explain possible gaps in the supplied manual. They
were **not** treated as current Ekonerg QMS evidence or added to the active set.

## 6. Evaluation and scoring

The framework returned to the existing Enconet five-level method:

| Rating | Level | Criterion score |
|---|---:|---:|
| Fully matched | 5/5 | 100 |
| Substantially matched | 4/5 | 75 |
| Partially matched | 3/5 | 50 |
| Minimally matched | 2/5 | 25 |
| Unmet | 1/5 | 0 |

The overall result is the mean over applicable criteria, rounded using the
local scoring contract. Approved not-applicable criteria remain visible but
are excluded from the denominator. The scale was not replaced by new classes.

The owner found the earlier scoring too harsh for a documentation screen. The
reassessment therefore distinguished two questions: does the written system
cover the duty, and has implementation been proved through work records?
Missing work samples alone no longer cap an otherwise complete written
control below full. Real gaps in the written system still lower the rating.

Each criterion has a short explanation, affirmative evidence, contrary points,
a ruling, linked score support, and verification actions. Regulatory crumbs
describe the comparison baseline; vendor crumbs support vendor ratings.

The percentage is an ordinal summary of criterion judgments. It is not a
measured percentage of every NQA-1 clause and is not proof of legal compliance.

## 7. Dashboard: useful results instead of an intake workflow

The first dark dashboard changed too much. It showed gates, queues, and a
judgment-entry form instead of the requested conformance presentation. The
owner rejected that direction and asked for the TEKOL light example's layout,
populated with **Ekonerg** data. TEKOL example values were not production results.

The light dashboard now presents summary metrics, executive summary,
classification distribution, filters, search, sorting, 18 criterion cards,
the evidence matrix, gaps, and auditor actions. The radar chart was discarded
as requested. The empty-matrix defect was fixed without removing its behavior.

Closed cards show a concise criterion summary, rating, percentage/5-point
level, and short support count. Long crumb lists and document references stay
inside the expanded card. Each score connects to its supporting crumbs and
source chapters. Matrix columns can be sorted. Keyboard search shortcuts,
expand/collapse controls, mobile layouts, and print/PDF remain available.

The dark presentation is a **separate copy**. It preserves the light file,
audit values, main interaction script, and light print layout. The accepted
look uses UMBRA-inspired foundations, luminous teal/blue accents, gradients,
soft light sources, a faint grid, and a cursor-following spotlight.

The owner also requested gray crumb references, lighter document names on
separate lines, and the light-intensity effect on the actual score bar rather
than on a second decorative line. Bar width never animates, so its value stays
honest. Reduced-motion, touch, forced-color, and print rules limit decorative
effects. The design is UMBRA-inspired, not a claim of strict compliance with
every component of a draft design system.

## 8. Reset and repeat audits

Reset is an explicit owner-operated command. It previews targets before any
removal, verifies a saved plan and file fingerprints, and uses a separate
confirmation token. A backed-up apply is the normal path. The owner's earlier
Ekonerg no-local-backup decision is not inherited by another vendor.

The reset keeps incoming documents, framework code, schemas, prompts, review
and handoff history, and coordination records. It removes known generated
audit state so the company can be audited again with revised documents or a
new sieving method. Thus it implements “start the audit over,” not “delete the
framework and its history.”

During this reuse work, the v2 reset also gained coverage for dated `out/`
snapshots, old candidate files, and the raw-source registry. Its plan format
was bumped to v2. Reset was tested on fixtures; neither live audit was reset.

## 9. Reuse and guidance

The workspace guidance now makes reuse an axiom: a new supplier must begin
from a company-neutral framework, not a round of company-name code patches.
Scripts remain local copies, as the owner requested. Normal runtime must not
import another company's scripts or read its evidence.

Guidance also separates agent ownership, active/archive messages, claims,
source integrity, validation, handoffs, and index freshness. Codex updates
`AGENTS.md` and its skills; Claude owns `CLAUDE.md` and its skills. This summary
does not claim that every new reuse change has already been synchronized on
Claude's side. The new synchronization request is left in coordination.

The new v2 package joins 23 pinned framework components with the current
portable improvements. It has a manifest, source hashes, one preview/apply
command, conflict blocking, exclusive file creation, and a retry journal.
It excludes company documents, databases, results, approvals, and active
prompt history. Existing folders are not blindly cloned or renamed.

## 10. Verification: what is proved and what is not

Existing Ekonerg records contain the earlier full keyword, quote, source,
evaluation, and dashboard checks. The light dashboard also has a recorded
29-check live-browser run and an actual 43-page A4 PDF check. See
[live print review](reviews/DASHBOARD_LIVE_PRINT_20261007.md).

The latest dark refinements had focused presentation tests and owner visual
acceptance. That acceptance does not mean the complete light-dashboard
browser/PDF suite was repeated after every dark refinement. Physical-printer
output was not tested. Historical passes are not reported as new passes.

The new reuse tests cover neutral company names, spaces and non-ASCII paths,
with/without a sibling company, safe retries, conflict refusal, empty approvals,
local runtime help, reset coverage, and read-only reproduction of both audits.
Transfer evidence and remaining limits are recorded in
[the reuse rollout record](../../doc/framework-reuse/ROLLOUT_20261007.md).

The new release is not permission to ingest unapproved sources, activate a
prompt without local calibration, change applicability, or reuse another
supplier's findings. Formal lifecycle fields also must not be declared closed
simply because the owner accepted the dashboard as the tool's completed result.

## 11. Practical outcome

The owner now has a much stronger documentation audit: more source-supported
vendor evidence, clearer ratings, clickable chapters, useful verification
targets, and a dashboard that works in both light and dark presentations.

For the next supplier, the work should be configuration, fresh intake,
calibration, and audit processing—not another four-day code-copy repair cycle.
The reusable release and Enconet backport are the next step toward that goal.
