# Enconet keyword sweep and calibration preparation

## Sweep completed

The reproducible keyword/heading pass scanned all 33 registered sources, using
all 18 criterion search lists. Raw files, incoming originals, registry and live
database were unchanged. Explicit hash-pinned non-source exclusions keep
desktop.ini, .gitkeep and the owner's conversion note out of audit evidence.
Unknown incoming files still block the sweep; a registered source cannot be
hidden by an exclusion.

| Side | Documents | Passage leads | Distinct quote texts, counted per document | Possible criterion links | Unmatched content blocks |
|---|---:|---:|---:|---:|---:|
| Vendor | 26 | 4,183 | 4,047 | 8,566 | 2,025 |
| Regulatory/supporting | 7 | 2,992 | 2,959 | 6,757 | 837 |

These are **search leads, not accepted crumbs**. The database still contains
zero crumbs and no new evaluations or score. The semantic review is not complete.
No maximum number or quote-length cap was imposed. Unmatched blocks remain
visible and must also be read for their meaning. Repeated wording and multiple
criterion matches must not be counted as separate proof without review.

[Sweep review bundle](../out/2026-10-07/full-keyword-sweep/README.md)

The bundle includes exact source snapshots, passages, coverage dispositions,
rules, scanner, exclusions and artifact hashes. Verification reproduces the
scan and verifies every passage offset and exact quote.

## Golden calibration candidate

[Owner review: 20 vendor examples](../benchmarks/sieving_golden/20261007-v3-nuclear-plan/OWNER_REVIEW.md)

The Nuclear QA Plan examples cover all 18 criterion intents plus a vague
standard reference and a supplier claim that criterion XIII is outside its
current scope. The conditional storage policy and scope claim both remain
visible. Neither automatically makes XIII applicable or not applicable.

Concrete written controls, indirect supporting controls and candidate leads
are separated using the existing v3 prompt. These are extraction strength
labels, not new conformance ratings. Written detail is not an executed work
record. Every selected quote is exact in registered DOC-0001 and a same-document
database section.

The fixture remains pending owner approval. Strict core JSON validation passed.
The diagnostic same-author consistency check found 20 expected items, with zero
missed/spurious items, but `promotion_ready` is false. This is not an independent
prompt execution, a complete sieve of the manual, or a measured recall result
for the full source set.

## Remaining v3 compatibility check

Code inspection confirmed a real storage gap: the current Enconet importer
writes core crumb fields but does not persist optional `evidence_type` or
`context`. Strict core validation accepts those fields without proving storage.
The draft keeps source-supported revision context in JSON. No live import was
attempted, no context was silently dropped, and v3 has not been activated.

Next implementation step: verify lossless context storage on a synthetic
database, then use the owner's local golden decision and a measured candidate
test before activation. Do not copy Ekonerg's golden approval or upgrade live
evidence in place. Supporting ASME Parts 2-4 retain their previously recorded
conversion/long-section warnings; keyword coverage does not resolve them.

## Validation commands

- `python -m pytest audit_template/tests/test_sweep_exclusions.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/enconet-sweep-exclusions-20261007-a`: exit 0, three tests passed.
- `python Enconet/scripts/full_keyword_sweep.py --output Enconet/out/2026-10-07/full-keyword-sweep --exclusions Enconet/out/2026-10-07/fresh-intake/sweep-exclusions.json`: exit 0, all 33 sources scanned.
- `python Enconet/scripts/full_keyword_sweep.py --verify Enconet/out/2026-10-07/full-keyword-sweep`: exit 0, exact quotes and artifact hashes verified.
- `python Enconet/scripts/validate_app_b_json.py Enconet/benchmarks/sieving_golden/20261007-v3-nuclear-plan/candidate.json --strict`: exit 0.
- `python Enconet/scripts/score_sieving.py --golden Enconet/benchmarks/sieving_golden/20261007-v3-nuclear-plan/manifest.yml --actual Enconet/benchmarks/sieving_golden/20261007-v3-nuclear-plan/candidate.json --output Enconet/benchmarks/sieving_golden/20261007-v3-nuclear-plan/draft-self-check.json --allow-draft`: exit 0, diagnostic only and not promotion-ready.
- `python Enconet/scripts/run_all_validations.py --no-record`: exit 0, four applicable checks passed at chunked; downstream checks skipped.

An additional read-only check found all 20 calibration quotes in raw and
same-document sections. The sweep's 73 protected file hashes still match,
including all incoming files, registered raw files and live database.

The reusable updated scanner source is in
`audit_template/runtime_v2/full_keyword_sweep.py`. The immutable committed v2
package is unchanged; no other company runtime was patched during this task.
