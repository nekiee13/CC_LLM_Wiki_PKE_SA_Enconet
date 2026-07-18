# Slice-1 rendered-tree evidence (M2 amendment 1, AM1-F1)

Rendered 2026-07-18 into `doc/support-transfer/rendered/slice1/` — the exact byte
content proposed for the amended slice-1 content commit A in CC_FIN. Eight files, no
`support/README.md`, no `docs/README.md` modification, no
`support/decisions/adr.template.md` (AM1-F4: the ADR design template stays Wiki-side;
T3's asset map instantiates it only as `support/decisions/ADR-SUP-NNNN-slug.md` files).

## Render protocol (fail-closed)

- **passed** — render + first-pass checks: command=
  `python doc/support-transfer/rendered/render_slice1.py` (renderer retained in-repo
  alongside its output; the committed rendered tree plus the independent read-back
  below are the reproducible authority); exit_code=0. The renderer aborts before writing any file
  on: unresolved `{{...}}` placeholder, sensitive-content pattern
  (staged `_shared.scan_sensitive`), forbidden reference tokens (`LLM_Wiki`, `03_PKE`,
  `Enconet`, `xPY`), or a relative Markdown link that resolves neither inside the slice
  tree nor to an existing CC_FIN path. A deliberately broken probe (leftover
  `{{TARGET_DECISION_AUTHORITIES}}`) aborted with exit 1 before the fix, demonstrating
  the fail-closed behavior.
- **passed** — disposable-root read-back verification: the rendered tree was copied to
  a fresh temporary root and independently re-verified from disk (8/8 files; no
  placeholder, no sensitive pattern, no forbidden token including absolute-path forms,
  no link escaping the root, no dangling link); exit_code=0; the disposable root was
  removed afterward.

## AM1-RR corrections (re-rendered and re-verified)

- **RR1**: `support/PROFILE.md` now carries the active M1 `Git and hosted workflow`
  rules (main-only, small reversible commits, sequential review-before-push, no force
  push/history rewrite/broad reset/branch-protection mutation/tag/release, hosted
  protection `unknown` until verified, workflow mismatch only via its separate
  approval) and the product-work boundary (product issues stay in the product
  plan/GitHub; release creation out of scope), with the amendment's one-time reset
  exception stated narrowly as history.
- **RR2**: the rendered `support/log.md` carries only a truthful `support-prepared`
  event; the `support-committed-local` event is appended by evidence commit B with
  commit A's committer time (deterministic rule in the briefing), and
  `support/current-status.md` no longer claims commit A exists.
- **RR3**: every rendered command reference uses the accepted baseline flags with
  reporting-only additions; `-W ignore` is removed everywhere.
- **passed** — post-correction disposable-root re-verification (8/8 files; adds probes
  for the backdated event type, `-W ignore`, and the RR1 rule set via
  whitespace-tolerant matching); exit_code=0.

## AM1-RR5/RR6 corrections and byte authority

- **RR5**: the rendered status and briefing v5 now carry one literal PowerShell
  command as the exact entry point (environment-assignment form; fixed report names
  `fin_slice1_A.xml`/`fin_slice1_B.xml` under `$env:TEMP`; `-q`, `--tb=no`,
  `--junitxml` fixed; no `-W` or other behavior change). No meta-placeholder remains
  in any rendered command.
- **RR6**: the prepared event states exactly the facts available at its timestamp
  ("rendered and disposable read-back verified"); the stale `support-committed-local`
  statement below was corrected.
- **Byte authority**: the committed rendered tree — not a fresh renderer run — is
  commit A's byte authority (briefing v5's byte-for-byte rule). The retained renderer
  additionally accepts `--timestamp <reviewed UTC>` for exact byte reproduction; this
  was mechanically demonstrated (fresh render stamped, then re-run with `--timestamp`
  produced all 8 files SHA-256-identical, exit 0). A fresh run without `--timestamp`
  intentionally stamps a new UTC into the two timestamped records.
- **passed** — post-RR5/RR6 disposable-root re-verification (8/8; probes added for
  meta-placeholders, the literal command appearing exactly twice in the status, the B
  report name, and prepared-event wording); exit_code=0.

## Content decisions visible in the rendered tree

- `support/PROFILE.md` (new, Controlled): clone-complete target-local profile authority
  — identity/ownership, enabled/disabled modules, native-validation composition,
  product preservation, sensitivity/indexing, scale assumptions, recovery rules. M1/M2
  provenance is cited as history with no workspace path (AM1-F2 of the S1 review:
  `SUPPORT_PROFILE_PATH` now renders to the target-local path `support/PROFILE.md`).
- `support/RECORD-KEEPING.md`: published path/class map gains a
  `support/PROFILE.md | Controlled` row and labels the `support/README.md` row as
  arriving with the index-closure slice.
- `support/current-status.md`: names the exact like-for-like pytest command as the
  next-action entry point; the validation summary states the expected literal outcome
  as **pending** and explains the two-commit evidence protocol — no validation result
  is authored before it exists (AM1-F2/S1-F3).
- `support/log.md`: the initial (and only) rendered event is `support-prepared`,
  stating the render + disposable read-back facts available at its timestamp; the
  `support-committed-local` and `support-validated` events are appended by evidence
  commit B with their actual UTC times under the briefing's deterministic rule
  (AM1-RR2/RR6 — nothing is backdated, and independent reviewer verification is never
  claimed at the render timestamp).
- `support/decisions/README.md`: existing FIN decision authorities listed with
  architecture/AS-IS included; no renumbering.

## Slice 3c

Slice 3c (`support/README.md` + the `docs/README.md` link line) is **not rendered
here**; per AM1-F1 it is rendered and evidenced at its own pre-job briefing, after
slices 2 and 3 exist.
