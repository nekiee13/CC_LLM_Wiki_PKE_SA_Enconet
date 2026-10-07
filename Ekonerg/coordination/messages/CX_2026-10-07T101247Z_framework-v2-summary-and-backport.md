---
message_id: CX_2026-10-07T101247Z_framework-v2-summary-and-backport
created_at_utc: 2026-10-07T10:12:47Z
from_agent: codex
to_agent: claude-code
type: review_request
task: FRAMEWORK-REUSE-20261007
related_files:
  - Ekonerg/docs/EKONERG_IMPROVEMENTS_SUMMARY_20261007.md
  - audit_template/framework_release.py
  - audit_template/prepare_vendor.py
  - audit_template/framework/v2/manifest.json
  - Enconet/docs/FRAMEWORK_UPGRADE_20261007.md
---

# Framework reuse rollout — 7 October 2026

Owner request: summarize Ekonerg, upgrade Enconet, and prepare IBE, TEKOL,
IGH, IMK, KCPG, and MOR. Codex implements; Claude reviews later.

## Epic A — Record what improved

What & why: keep the lessons in one place so the next audit does not repeat
the same search, scoring, GUI, or transfer mistakes.

### A1 — Detailed summary: done

What & why: explain the seven improvements, their limits, and the evidence.

- [x] [Detailed summary](../../Ekonerg/docs/EKONERG_IMPROVEMENTS_SUMMARY_20261007.md) written.
- [x] Vendor crumbs distinguished from rule crumbs, search leads, and score links.
- [x] FAHP marked deferred; semantic recall is not described as formal FAHP.
- [x] Part 21, real-audit verification, and unrun checks remain visible.

## Epic B — Backport useful methods to Enconet

What & why: add the newer tools while keeping the closed audit intact.
An upgrade is not a reset or an automatic new audit.

### B1 — Additive tool upgrade: done

What & why: copy portable features from one pinned package, not by ad hoc edits
to each company. The installer creates missing files only.

- [x] Fourteen upgrade files installed locally; journal kept in
  `Enconet/.bootstrap/framework-v2/`.
- [x] Full keyword sweep, concept cards, v3 candidate prompt and context contract installed.
- [x] Safe reset v2 installed; **not applied to the live audit**.
- [x] Neutral light renderer, dark overlay, CSS and decorative scripts installed.
- [x] Retry with a second run ID created zero files and preserved all 14 matches.
- [x] Enconet DB remains `73eaa3a46215c08ad4d0539a297ba0acc33024ea21e7fa1fbdec0f1a3d623b3d`.
- [x] Existing source, result, model, applicability, approval and active prompt bytes preserved.

### B2 — Separate Enconet dashboard candidates: done

What & why: use Enconet's own result in the new presentation. Never show Ekonerg
facts under an Enconet title or overwrite the approved report/dashboard.

- [x] [Light candidate](../../Enconet/out/2026-10-07/framework-v2/ENCONET_DASHBOARD_LIGHT.html).
- [x] [Dark candidate](../../Enconet/out/2026-10-07/framework-v2/ENCONET_DASHBOARD_DARK.html).
- [x] Existing run reproduced: 87.5%, 234 vendor crumbs, 18 criteria.
- [x] Per-criterion summaries, score evidence, exact quotes and chapter access.
- [x] Forty-two live-browser checks passed, including controls, mobile and print styles.
- [x] Original controlled dashboard stays in `Enconet/outputs/` unchanged.

These are presentation candidates, not new criterion judgments or a new issued
audit. The English presentation labels do not replace Enconet's controlled
Croatian report. This renderer has not replaced the existing phase dispatcher.

### B3 — Do not reopen a closed audit: preserved

What & why: updating software must not change what the previous audit concluded.

- [x] No Enconet re-sieving, source-edition replacement, prompt activation, rating
  write, generation promotion, gate change, or reset performed.
- [x] Frozen Enconet master/alignment plans unchanged.
- [ ] For a future re-audit, calibrate/activate the new prompt on Enconet sources
  and check optional context-field runtime compatibility before import.

The last item is a new audit's intake work, not an implied approval inherited
from Ekonerg. Installing a prompt and contract does not migrate evidence tables.

## Epic C — Prepare one clean start for six vendors

What & why: reuse code and methods, not a company's documents, decisions, or scores.

### C1 — Versioned clean package: prepared and tested

What & why: join the existing pinned components with current portable methods.
Use one file manifest and one setup command instead of many transfer slices.

- [x] `audit_template/framework/v2/`: 123 company-neutral files.
- [x] `audit_template/framework/upgrade-v2/`: 14 additive upgrade files.
- [x] Files and source component manifests are hash-checked.
- [x] Local runtime has no sibling-project imports or data dependency.
- [x] Clean package has empty approvals and no active prompt.
- [x] No raw sources, DB, audit outputs, company fixtures, or Claude-owned files copied.
- [x] Initializer seeds only the 18 common taxonomy names, not requirements,
  source editions, applicability, evidence, approvals, or results.
- [x] Fresh intake is preview-first and keeps incoming documents intact.
- [x] Original data, missing dependency, and reset-coverage defects caught by tests.

The framework can build evidence and outputs once the new company's controlled
inputs and decisions exist. Tests prove mechanics; they do not certify a new
supplier's documentation or replace local golden calibration.

### C2 — Six vendor previews: prepared, not deployed

What & why: show the exact copy plan without altering new or existing company trees.

| Vendor | Preview | Sources and decisions |
|---|---|---|
| IBE | [Final preview](IBE-preview-final.json) | Pending owner |
| TEKOL | [Final preview](TEKOL-preview-final.json) | Pending owner; preserve existing tree |
| IGH | [Final preview](IGH-preview-final.json) | Pending owner |
| IMK | [Final preview](IMK-preview-final.json) | Pending owner |
| KCPG | [Final preview](KCPG-preview-final.json) | Pending owner |
| MOR | [Final preview](MOR-preview-final.json) | Pending owner |

- [x] 123 framework files plus six small company setup records planned per vendor.
- [x] Supplier identity explicit; all gates pending; no database copied or created.
- [x] Regulatory editions, scope, Part 21 applicability, language and backup waiver
  remain unset. No other company's approvals are inherited.
- [x] Conflicts refuse the copy. Existing `CLAUDE.md` remains untouched.
- [ ] Owner chooses whether to deploy folders now or keep only this prepared release.
- [ ] Owner chooses regulatory editions per vendor, or explicitly permits edition reuse.

### C3 — Start the next audit as one coherent intake batch

What & why: do the audit work next, rather than another per-file patch cycle.

- [ ] Apply the chosen vendor setup after the owner chooses deployment.
- [ ] Put its current documents and approved regulatory sources in `incoming/`.
- [ ] Record scope, edition roles, language, and applicability in that project.
- [ ] Run source registration, extraction/chaptering, recall sweep and calibrated sieving.
- [ ] Evaluate all applicable criteria using linked vendor evidence; generate report and dashboards.
- [ ] Keep real-audit verification actions visible; do not replace results with a rating form.

## Commands

From the workspace root, substitute the chosen vendor and a fresh run ID:

```powershell
python audit_template/prepare_vendor.py --target IBE --supplier IBE
# Only after deployment is chosen:
python audit_template/prepare_vendor.py --target IBE --supplier IBE --apply --run-id ibe-setup-20261007
python IBE/scripts/init_db.py
```

The first command is read-only. The second is additive and refuses differing
files. The third creates a local database with common taxonomy names only.
Do not apply reset during setup or upgrade. Reset plans and no-backup waivers
must be reviewed for the company being reset.

For Enconet's additive package:

```powershell
python audit_template/framework_release.py --target Enconet --upgrade
```

## Validation evidence

Commands ran on 7 October 2026. An environment failure is not a software pass.

| Check | Command | Exit / result |
|---|---|---|
| Initial TDD run | `python -m pytest audit_template/tests/test_framework_release_v2.py -q -p no:cacheprovider` | 1; eight expected missing-module failures before implementation |
| Reuse regression | `python -m pytest audit_template/tests/test_framework_release_v2.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/ekonerg-reuse-v2-20261007-e` | 0; 13 passed, including clean intake and two-name setup |
| Existing bootstrap regression | `python -m pytest audit_template/tests/test_bootstrap_sieving.py -q -p no:cacheprovider --basetemp C:/Users/PC/AppData/Local/Temp/ekonerg-reuse-bootstrap-20261007-a` | 0; three passed, two subtests passed |
| Enconet aggregate | `C:/xPY/vEnv/WikiEnconet/python.exe scripts/run_all_validations.py --no-record` from Enconet | 0; all 19 applicable checks passed after escalation |
| Ekonerg aggregate | `python Ekonerg/scripts/run_all_validations.py --no-record` | 0; eight passed, later-phase checks explicitly skipped |
| New candidate browser checks | `C:/xPY/vEnv/WikiEnconet/python.exe audit_template/verify_framework_dashboard.py --light Enconet/out/2026-10-07/framework-v2/ENCONET_DASHBOARD_LIGHT.html --dark Enconet/out/2026-10-07/framework-v2/ENCONET_DASHBOARD_DARK.html --browser-executable C:/xPY/vEnv/WikiEnconet/pw-browsers/chromium_headless_shell-1234/chrome-headless-shell-win64/chrome-headless-shell.exe --output doc/framework-reuse/browser-checks-20261007` | 0; 42 passed |
| Pre-existing Enconet byte check | `python audit_template/framework_preservation.py --verify doc/framework-reuse/baseline-Enconet-20261007.json` | 0; 1703 files unchanged at post-install boundary |
| Pre-existing Ekonerg byte check | `python audit_template/framework_preservation.py --verify doc/framework-reuse/baseline-Ekonerg-20261007.json` | 0; 1666 files unchanged at post-install boundary |

The first Enconet aggregate attempt failed on sandbox browser permissions; its
approved-runtime rerun passed. Synthetic initialization first failed to commit
the taxonomy inserts; that was fixed and regression-tested. No live DB was changed.

The new browser check verifies print behavior/styles, not a new complete PDF or
physical-printer run. Earlier Ekonerg PDF evidence is separate historical evidence.
Shared search indexes are stale against current HEAD; live files were used.

Guidance drift check: `python scripts/check_guidance_drift.py`, exit 0, no errors.
Skill structure check: `python scripts/check_skill_structure.py`, exit 1, because
the pre-existing Claude-owned global `synced` directory has no `SKILL.md`.
Codex did not change that directory; Claude must disposition it. This is not
reported as a passed check or silently repaired across the ownership boundary.

## Agent ownership and review

Codex's new tooling and records are ready for Claude review. Claude alone may
update its guidance/skills. No `CLAUDE.md`, `.claude/`, or `CC_` record was edited.
Claude synchronization is pending, not claimed complete. Review requests use
Ekonerg's neutral coordination channel.
