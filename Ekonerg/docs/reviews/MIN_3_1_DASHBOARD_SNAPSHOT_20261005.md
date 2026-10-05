# MIN-3.1 UMBRA evidence dashboard snapshot

Status: generated evidence view; no conformity result is asserted.

The offline dashboard is [EKONERG_UMBRA_DASHBOARD_2026-10-05.html](../../out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.html). Its machine-readable data is [EKONERG_UMBRA_DASHBOARD_2026-10-05.json](../../out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.json).

## What the snapshot shows

- 24 of 24 supplied vendor QMS files read; 31 registered files in total.
- 189 active vendor crumbs and 55 active regulatory-rule crumbs.
- 321 active quote records: 320 exact links and 2 normalized links.
- 13 of 18 Appendix B criteria have at least one vendor crumb; 5 have no direct vendor crumb.
- G1, G2, and G3 are approved. G4–G7 remain pending.
- 0 of 18 criterion judgments are recorded. The score and final classification are therefore **Withheld**.

## Provenance

The generator reads `db/nqa_audit.sqlite`, `out/2026-10-05/MIN-3.1-evidence-matrix-v4.json`, and `project-state.yml`. The QMS batch table is reconciled to `docs/reviews/EF_2_2_EVIDENCE_REVIEW.md` (B01–B10, 24 vendor files).

Command used:

```text
python Ekonerg/scripts/build_evidence_dashboard.py --generated-date 2026-10-05 --json-output Ekonerg/out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.json --html-output Ekonerg/out/2026-10-05/EKONERG_UMBRA_DASHBOARD_2026-10-05.html
```

Targeted dashboard tests: `2 passed` (`python -m pytest Ekonerg/scripts/tests/test_evidence_dashboard.py -q`).
