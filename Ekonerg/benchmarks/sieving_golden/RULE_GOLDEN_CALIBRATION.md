# Ekonerg RULE golden calibration

## Status

**Draft — pending human approval**

- Source: `DOC-0002` — `10CFR_Part 50_-_Appendix_B.md`
- Side: `RULE`
- Prompt: `appb_rule_v1`
- Approval reference: none yet
- YAML manifest: [`manifest_rule.yml`](manifest_rule.yml)

This is a small answer key for testing the RULE sieve. It tells us which
regulatory crumbs a good run should find. It does not approve the source, prove
audit compliance, or replace human review.

The sieve uses a recall-first rule. It should keep plausible, source-supported
crumbs, including borderline ones, while preserving exact quotes and chapter
locators. Uncertain mappings remain candidates for review.

## Expected crumbs

### GOLDEN-RULE-001 — Organization

- Criterion: `APP_B_I`
- Locator: `I. Organization`
- Expected statement: The applicant shall be responsible for the establishment
  and execution of the quality assurance program.
- Exact source quote:

  > The applicant shall be responsible for the establishment and execution of the quality assurance  
  > program.

### GOLDEN-RULE-002 — Document Control

- Criterion: `APP_B_VI`
- Locator: `VI. Document Control`
- Expected statement: Measures shall be established to control the issuance of
  documents.
- Exact source quote:

  > Measures shall be established to control the issuance of documents, such as instructions, procedures, and drawings, including changes thereto, which prescribe all activities affecting quality.

### GOLDEN-RULE-003 — Quality Assurance Program

- Criterion: `APP_B_II`
- Locator: `II. Quality Assurance Program`
- Expected statement: The applicant shall establish a quality assurance
  program which complies with the requirements of this appendix.
- Exact source quote:

  > The applicant shall establish at the earliest practicable time, consistent with the schedule for accomplishing the activities, a quality assurance program which complies with the  requirements of this appendix.

### GOLDEN-RULE-004 — Design Control

- Criterion: `APP_B_III`
- Locator: `III. Design Control`
- Expected statement: Measures shall be established to assure that applicable
  regulatory requirements and the design basis are correctly translated into
  design documents.
- Exact source quote:

  > Measures shall be established to assure that applicable regulatory requirements and the design basis

### GOLDEN-RULE-005 — Control of Purchased Material, Equipment, and Services

- Criterion: `APP_B_VII`
- Locator: `VII. Control of Purchased Material, Equipment, and Services`
- Expected statement: Measures shall be established to assure that purchased
  material, equipment, and services conform to the procurement documents.
- Exact source quote:

  > Measures shall be established to assure that purchased material, equipment, and services, whether purchased directly or through contractors and subcontractors, conform to the procurement documents.

### GOLDEN-RULE-006 — Quality Assurance Records

- Criterion: `APP_B_XVII`
- Locator: `XVII. Quality Assurance Records`
- Expected statement: Sufficient records shall be maintained to furnish evidence
  of activities affecting quality.
- Exact source quote:

  > Sufficient records shall be maintained to furnish evidence of activities affecting quality.

## Calibration result

The expected set contains six crumbs across six Appendix B criteria.

The draft self-score is:

| Measure | Result |
|---|---:|
| Found | 6 |
| Missed | 0 |
| Spurious | 0 |
| Human approval | Pending |
| Promotion ready | No |

The score is only a structural check. Human approval is still required before
this set can be used as a promotion gate.
