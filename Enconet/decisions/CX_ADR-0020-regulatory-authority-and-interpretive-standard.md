# ADR-0020 — Regulatory authority and NQA-1 interpretive role

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-07-13 |
| Decided by | Human (project owner) |
| Scope | Enconet evaluation framework and EPIC5 sieving/data contracts |
| Register | Extends ADR-0003; requires an EPIC5 contract revision before NQA-1 sieve runs |
| Authored by | Codex (`CX_` prefix) |

## Context

The evaluation framework determines whether Enconet's quality-assurance system meets
10 CFR 50 Appendix B, interpreted and implemented through ASME NQA-1. The current
`source_rules` vocabulary contains `10CFR50_APPB` and `10CFR21` as flat, mutually
selectable values. NQA-1 source documents are now in the controlled RULE-side corpus,
but adding `ASME_NQA1` as an equal value would erase the difference between mandatory
regulatory authority and an interpretive/implementation standard.

The source terminology also differs and must be preserved: NQA-1 organizes its
top-level QA provisions as requirements; Appendix B organizes its provisions as
criteria; Part 21 specifies requirements.

Part 21 is not optional guidance. It is a mandatory regulatory add-on for
nonconformance handling. For applicable nonconformances, Appendix B and Part 21 both
supply mandatory code requirements, and the Appendix B QA system is expected to
provide for fulfilment of the Part 21 obligations.

## Decision

1. The framework's primary evaluation question is whether Enconet's QA system meets
   the mandatory requirements of 10 CFR 50 Appendix B as interpreted and implemented
   through ASME NQA-1.
2. `10CFR50_APPB` is the mandatory governing baseline across the QA-system evaluation.
3. `10CFR21` is a mandatory additional governing source for nonconformance handling
   when its requirements apply. The model must permit Appendix B and Part 21 to govern
   the same evaluation unit; they are not mutually exclusive alternatives.
4. `ASME_NQA1` is an interpretive and implementation source. It must remain explicitly
   distinguishable from governing regulatory sources and must not be flattened into
   the existing `source_rules` list as a peer authority.
5. Enconet procedures, records, and other supplier materials are evaluated evidence;
   they are neither governing nor interpretive authority.
6. The canonical contract must represent, at minimum:
   - zero or more governing references on an evaluation unit, including source and
     locator;
   - an applicability condition or determination for conditionally applicable Part 21
     requirements;
   - zero or more NQA-1 interpretive references, including source and locator; and
   - traceable mappings from governing requirements through interpretive requirements
     to Enconet evidence and evaluation results.
7. Source-native terminology is retained in presentation and records: Appendix B
   **criteria**, NQA-1 **requirements**, and Part 21 **requirements**. A generic internal
   term such as `provision` may be used only where a source-neutral container is needed.
8. Before EPIC5 processes NQA-1 sources, its schema, prompts, validators, fixtures,
   runtime projections, and documentation must replace or refine the current singular
   flat `source_rules` assumption consistently. Exact field names and cardinalities are
   implementation details, but they must preserve this authority model.

## Consequences

- EPIC5 cannot be implemented correctly by merely adding `ASME_NQA1` to
  `vocabularies.source_rules`.
- The current single-source RULE contract is recognized as insufficient for the target
  evaluation framework and requires a controlled, tested schema evolution under
  ADR-0003.
- Nonconformance evaluation must support concurrent Appendix B and Part 21 governing
  references, including an explicit Part 21 applicability decision.
- NQA-1 requirements may elaborate how an Appendix B criterion is understood and
  implemented, but they do not replace the governing code citation.
- Findings and reports must retain a visible chain from regulatory basis, through
  NQA-1 interpretation, to Enconet evidence and the resulting determination.
- This ADR defines authority and relationships; it does not itself approve a particular
  crosswalk, Part 21 applicability result, or compliance conclusion.
