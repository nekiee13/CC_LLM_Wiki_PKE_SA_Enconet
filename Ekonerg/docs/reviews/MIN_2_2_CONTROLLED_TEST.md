# MIN-2.2 controlled sieving test

## Result

The first controlled test passed for one RULE source and one Ekonerg QMS
procedure. The full 31-document intake was not processed.

| Run | Source | Prompt | Crumbs | Quote links | Golden score |
|---|---|---|---:|---:|---|
| `RUN-20261003-01` | `DOC-0002` — 10 CFR 50 Appendix B | `appb_rule_v1` | 6 | 6/6 (100%) | 6 found, 0 missed, 0 spurious |
| `RUN-20261003-02` | `DOC-0027` — PQ09.2 audits | `appb_document_v1` | 8 | 8/8 (100%) | 8 found, 0 missed, 0 spurious |

Both runs are local generation 1 records. Their run rows, crumbs, and chapter
links are stored in the local ignored database at `db/nqa_audit.sqlite`.

## What this test proves

- The active prompts can create local runs for both sides.
- The owner-approved Appendix B source is registered as a governing source.
- Strict crumb validation accepts the local English RULE output and Croatian
  DOCUMENT output.
- Every test quote links to a same-document chapter/section location.
- The objective-evidence calibration captures more than a high-level QMS
  reference: it includes reports, approvals, response deadlines, follow-up,
  and record retention.

## What this test does not prove

- It does not prove Ekonerg performs these controls in practice.
- It does not complete the audit or create findings.
- It does not validate all 31 documents.
- It does not approve the older manual or corrective-action golden drafts.

## Evidence files

- RULE metrics: [`out/2026-10-03/metrics.json`](../../out/2026-10-03/metrics.json)
- RULE score: [`out/2026-10-03/RUN-20261003-01/score.json`](../../out/2026-10-03/RUN-20261003-01/score.json)
- DOCUMENT metrics: [`out/2026-10-03/RUN-20261003-02/metrics.json`](../../out/2026-10-03/RUN-20261003-02/metrics.json)
- DOCUMENT score: [`out/2026-10-03/RUN-20261003-02/score.json`](../../out/2026-10-03/RUN-20261003-02/score.json)

The next step is human review of this controlled output, followed by bounded
document batches. Do not treat the scores as audit conclusions.
