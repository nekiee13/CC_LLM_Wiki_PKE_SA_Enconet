# Ekonerg audit framework: function and goal

## Goal

This is a repeatable pre-flight audit framework. Its question is:

> Does Ekonerg's own quality assurance system meet the requirements of 10 CFR
> 50 Appendix B, interpreted with ASME NQA-1?

The same framework will later be reused for IBE, IMK, TEKOL, IGH, and other
companies. Each company gets a separate intake, database, evidence set, score,
findings, and report.

This is the owner's core reuse rule: a new company should need a fresh source
intake and reviewed configuration, not another round of per-company code
patches.

The result is an evidence-based map of strong and weak areas. It helps the real
audit team choose where to seek objective operating evidence. It is not a
replacement for the real audit and it must not invent implementation records.

## What the framework does

1. **Ingests** the owner-approved regulatory and company QMS documents.
2. **Preserves chapters** and source locators while extracting evidence crumbs.
3. **Maps** vendor crumbs to the 18 Appendix B criteria.
4. **Evaluates** every criterion against the approved five-level model.
5. **Traces** each criterion result back to its exact crumb and source chapter.
6. **Reports** summaries, score details, evidence gaps, and auditor verification
   actions.

The sieve uses a broad, fuzzy reading rule. A high-level QMS reference is a
useful lead, but deeper vendor text and objective-evidence clues should also be
collected when they reasonably relate to the purpose of a requirement. The
sieve must not be so strict that useful clues disappear, and it must not invent
facts or quotes.

The dashboard is a presentation layer. The database, source snapshot, crumb
links, evaluation records, and approval records remain the controlled sources.

## Evidence boundary

The audit fence surrounds Ekonerg's QA system. Other companies are not audit
targets. Supplier controls are checked only when Ekonerg's documents say they
can affect quality.

The owner has identified Ekonerg's work as design, engineering services, and
consultancy. If a supplier activity boundary is vague, the framework records
that uncertainty for review instead of silently expanding the scope.

Policy text shows that a control is described. It does not prove that the
control operated. The framework therefore flags the need for implementation
records, samples, completed audits, certificates, operating examples, or other
objective evidence.

Part 21 is used mainly for nonconformances and corrective actions. ASME NQA-1
Part 1 is mandatory in the interpretation baseline; Part 2 is guidance unless
an approved scope decision makes a specific use applicable.

Appendix B applicability is reasoned criterion by criterion. A criterion is
not removed just because the current documents are thin; missing evidence is a
gap. A not-applicable result needs an explicit owner decision.

The source is stored and displayed by document chapter. Page identifiers are
not the traceability key. Each crumb must retain its document, chapter path,
quote, and link to the stored chapter text.

## Score meaning

The approved Ekonerg model is `1.0-ekonerg-20261004` under `G3-RUN-20261003-32`:

| Level | Weight | Meaning |
|---|---:|---|
| Fully | 1.00 | Strong support, subject to final human review |
| Substantially | 0.75 | Most control elements described or supported, with gaps |
| Partially | 0.50 | Some useful support, but material gaps remain |
| Minimally | 0.25 | Very limited support |
| Unmet | 0.00 | No sufficient support in the current evidence set |

The score is a navigation aid for audit focus. A human reviewer and the owner
must still control formal judgment, approval, and release.
