---
record_type: design_checkpoint
scope: T4-T5
recorded_at_utc: 2026-07-17T00:34:05Z
status: partial
completed_criteria: T5.1
target_mutation: none
publication_gate: M2
---

# T4/T5 design checkpoint — T5.1 complete only

## Accepted design evidence

The owner accepted T45-F1, T45-F2, and the independent review's planning-versus-publication
boundary. The corrected package machine-enforces:

- no fabricated HEAD for absent/unknown Git state;
- full current/stale Git HEAD evidence for the present SHA-1 targets;
- objective condition/date and owner for every `deferred-until` disposition;
- rejection of deferral-only fields on other dispositions;
- literal validation outcomes, record-before-pointer atomicity, and explicit interruption states.

T5.1's four target-handoff-profile criteria are complete because they are definitional and backed by
the reviewed contract/schema. The SHA-1 40-hex pattern is an accepted non-blocking observation for
the current targets; future SHA-256 adoption is its reconsideration trigger.

## Explicitly pending

- T4.1 artifact/validator, T4.3, and T5.2 await executable staged artifacts plus positive and
  fault-injection tests in disposable roots.
- T4.2 and target-installed T4.1/T5.3 await gated T7/T8 publication and integration.
- Claude alone authors CC_FIN's Claude-owned payload when authorized; Codex alone authors CC_Loto's
  Codex-owned payload when authorized.
- No wholesale T4/T5 completion is represented.

## Evidence

- corrections: `1e4b6bb`;
- Codex review lifecycle: `09fcf2b`;
- owner/Claude manifest:
  `Enconet/coordination/archive/CC_2026-07-17T003333Z_resolved-t4-t5-design-review-manifest.md`;
- review disposition: `T4_T5_REVIEW_DISPOSITION.md`;
- independent result: four schemas valid and 22/22 reviewed cases behaved as specified;
- targets remained clean at FIN `238c207c73970f3d3c6dc00c2db5932ebeca7be4` and Loto
  `b469afc6f7e5593c60d0e5bdcfc7dead4a6bc481`.

## Authorization boundary

This checkpoint authorizes planning/staged work only. M2 still blocks every FIN write, and M3
blocks Loto publication.
