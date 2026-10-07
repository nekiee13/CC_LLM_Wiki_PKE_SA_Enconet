# Enconet source-set review - G1

## Intake completed

All **33 audit sources** are now registered: 26 Enconet documents and seven
regulatory documents. Each incoming original is unchanged. Registry, database,
raw-file hashes and write locks validate. Three non-source files stay excluded.

The first source was registered earlier. This task registered the remaining 32
in 17 bounded batches, validating every batch before starting the next.

- [Inventory](../out/2026-10-07/fresh-intake/incoming-inventory.json)
- [Original copy plan](../out/2026-10-07/fresh-intake/remaining-source-plan.json)
- [First attempt receipt](../out/2026-10-07/fresh-intake/source-registration-receipt.jsonl)
- [Resume plan](../out/2026-10-07/fresh-intake/remaining-source-plan-resume.json)
- [Resume receipt](../out/2026-10-07/fresh-intake/source-registration-receipt-resume.jsonl)
- Registry: `manifests/raw_sources.csv`, DOC-0001 through DOC-0033.

## One important edition question

The supplied ASME preface identifies **NQA-1:2015**. Enconet's Nuclear QA Plan,
section 1.1, instead cites **NQA-1:1994 with 1995 addenda, and the 2008 edition**.

This does not prove a failed QA system. It means the audit must state which
edition it uses. A supplier's declared edition and the owner's audit target
are not always the same. We must not silently replace one with the other.

Proposed target for owner approval: use the supplied NQA-1:2015 text to
interpret Appendix B, and flag the older references for real-audit verification.
If the audit must test the older contractual editions instead, the owner needs
to provide those editions and select them explicitly.

## Proposed audit fence

From Nuclear QA Plan section 1.2: maintenance and equipment-condition programs;
training and qualification; periodic safety reviews; nuclear safety analyses;
modification preparation and documentation; QA/QC services; independent technical
document review and verification; emergency preparedness; radioactive-waste
management and decommissioning; evaluation of safety-important projects;
equipment qualification; and control and maintenance of the MECL database.
The section states that the services cover all nuclear-facility lifecycle phases.

Enconet is the only supplier under evaluation. Check its control of subcontractor
work affecting quality, not those companies as separate audit targets. Individual
contracts may add duties; those are not inferred from an unavailable contract.

## Requested owner decision

Please confirm or amend this compact proposed basis:

1. Accept the 33 registered supplied sources for this fresh audit (G1).
2. Appendix B is the common governing baseline. Use supplied NQA-1:2015 Part 1
   to interpret it. Keep Parts 2-4 available as supporting text, not automatically
   mandatory. Keep Part 21 duties explicit and separate from the 18-criterion score.
3. Use the Enconet-only boundary and documented activities above. Detailed
   criterion applicability is assessed at its own gate, not approved by G1.
4. Produce explanations and reports in Croatian, with original quotes preserved.

These are proposals, not recorded approvals. No gate has advanced, no prompt
has been activated, and no new score has been written.

## Checks and exception record

- `python -m pytest audit_template/tests/test_source_batch_runner.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/enconet-source-batches-20261007-c`: exit 0, two tests passed (including Croatian filename and changed-source refusal).
- `python Enconet/scripts/validate_raw_sources.py`: exit 0, all 33 raw records valid.
- `python Enconet/scripts/run_all_validations.py --no-record`: exit 0; setup structure passed; later-phase checks skipped.
- Independent incoming hash check: 36 of 36 unchanged; DB chapter and crumb counts remain zero.

A fixture first exposed a legacy project-root alias; the import now uses the
local path helper. The first live attempt then stopped at SRC-20261007-003 on
Windows console encoding, before copying that source. SRC-002 was validated.
The runner now sets UTF-8 for child processes; its Unicode test passes. The
failed receipt is preserved and the verified remaining plan resumed successfully.

Next after approval: advance G1 through the state tool, ingest by chapter,
prepare local v3 golden calibration, then sieve and evaluate vendor evidence.
