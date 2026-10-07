# Enconet full vendor sieving - first real batch

## Activation and first run

Owner decision **confirmed** is recorded as `PROMPT-ENCONET-DOC-V3-20261007`.
DOCUMENT v3 is active, with local calibration/approval references in active.yml.
RULE v1 and the prompt text are unchanged. The operating lesson is deposited
in Codex's sieving-run skill; Claude synchronization and review remain pending.

Source: DOC-0001, Nuclear QA Plan NP-SUK-001 rev. 8.
Real run: **RUN-20261007-01**.

This is full-source semantic review, not a live import of the 20 calibration
examples. All 269 content blocks were read for direct controls and quality
intent, including non-keyword content. Every content block has a recorded
selection or context-only disposition. Headings and formatting remain covered
by the whole-source sweep record. There was no crumb quota.

| Result | Count |
|---|---:|
| Live vendor crumbs | 193 |
| Direct written controls | 115 |
| Supporting controls | 44 |
| Candidate leads | 34 |
| Exact source-chapter quote links | 223 |
| Retained context rows | 193 |
| Applicability decisions or criterion ratings written | 0 |

[Actual collected crumbs and quotes](../sieving/runs/RUN-20261007-01/REVIEW.md)

More than one distinct control can share a paragraph. It is not separate proof
when scoring. Standard lists and the informative comparison table are grouped
leads, not automatic positive findings. The conditional XIII policy and claimed
scope exclusion remain visible; neither is an automatic N/A decision.

## Traceability and records

The exact-run linker uses the recorded chapter locator to resolve repeated
wording, refuses normalized-only quotes and preserves previous links. It does
not use the legacy global link-rebuild operation. Independent checks found all
223 quotes verbatim in same-document chapters, with EXACT link method.
All 36 incoming files are still unchanged; registered sources remain intact.

- `sieving/runs/RUN-20261007-01/generated.json`: extraction payload.
- `sieving/runs/RUN-20261007-01/semantic-review.json`: source review decisions.
- `sieving/runs/RUN-20261007-01/metrics.json` and `metrics.md`.
- `manifests/ingest_runs.csv`: initial_sieve batch ING-20261007-001.

## Validation

- `python -m pytest Enconet/tests/test_exact_run_linking.py Enconet/tests/test_v3_context_storage.py Enconet/tests/test_epic5_sieving.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/enconet-first-sieve-20261007-a`: exit 0, 16 passed.
- `python Enconet/scripts/validate_app_b_json.py Enconet/sieving/runs/RUN-20261007-01/generated.json --strict`: exit 0.
- `python scripts/link_exact_run.py --run-id RUN-20261007-01`, then with `--apply`, from Enconet: both exit 0, 223 exact links.
- `python scripts/validate_traceability.py --no-record`, from Enconet: exit 0.
- `python Enconet/scripts/run_all_validations.py --no-record`: exit 0; four checks passed at chunked, later-phase checks skipped. Traceability and strict JSON were therefore also checked directly.
- `python scripts/check_guidance_drift.py`: exit 0.
- `python Enconet/scripts/validate_sieving_skill_drift.py --allow-pending-claude`: exit 0; pending synchronization is not completion.
- `python scripts/check_skill_structure.py`: exit 1; existing Claude-global synced directory lacks SKILL.md, left untouched.

## Remaining work

**1 of 26 vendor documents is fully sieved; 25 remain.** Regulatory documents
are ingested but requirement extraction is not complete. Phase remains chunked
while processing continues; G2-G7 remain pending. No overall score exists yet.

Next: quality manual and remaining procedures in bounded batches with fresh
run IDs. No new prompt approval is needed to continue. Keep broad meaning-based
recall, exact quotes and chapter links. Evaluate applicability and scores after
the required evidence and regulatory mapping are ready.
