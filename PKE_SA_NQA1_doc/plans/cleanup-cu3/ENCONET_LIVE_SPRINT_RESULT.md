# Enconet live cleanup: CU-3.3

The live layout is migrated. This is not final approval of the updated reusable
release. Claude's post-execution review remains pending.

## Work applied

- Moved 17,752 files under the exact recorded map. Kept all file bytes and
  identities. Kept the original Git blobs for 463 tracked files.
- Moved the two named Claude ADRs under the owner's narrow exception.
  Both hashes match their originals. No other Claude-owned file changed.
- Archived 10 empty old directory trees by native rename. Their directory
  identities, owners and permissions were preserved. Nothing was deleted.
- Installed 45 runtime/config files from Enconet's own script overlay, plus
  the existing neutral coordinator and benchmark components named in it.
- Added the existing handoff publisher as a local copy, with its unchanged
  neutral schema. Routed `audit-close` to that copy. The two-file handoff
  compatibility patch has its own exact plan and journal within CU-3.3.
- Updated Codex guidance and current result links. Claude guidance and skills
  remain unchanged; their synchronization is explicitly pending.
- Kept the frozen portable package together under output history, so its
  relative paths and pinned member hashes still validate. It is not the
  active dashboard entrypoint.

## Open the results

- Light: `Enconet/outputs/RUN-20261008-17/dashboard_light.html`
- Dark: `Enconet/outputs/RUN-20261008-17/dashboard_dark.html`
- Report: `Enconet/outputs/RUN-20261008-17/report.md`

Both dashboards remain self-contained and unchanged. The new report copy only
updates 382 artifact links. Its original remains under `revisions/relocated-originals`.

## Verification

| Check | Result |
| --- | --- |
| Exact-map isolated audit rehearsal | Exit 0; all 19 phase checks passed |
| Live `Enconet/scripts/run_all_validations.py --no-record` | Exit 0; all 19 checks passed |
| Focused cleanup regression | Exit 0; 25 passed, no skips |
| Handoff publisher regression | Exit 0; 12 passed, no skips |
| Publication-manifest reader regression | Exit 0; 7 passed, no skips |
| Frozen publication relocation verification | Exit 0; all 12 artifacts match the unchanged manifest |
| Live reset preview | Exit 0; preview only, no reset applied |
| Local `audit-close` publication and handoff validation | Exit 0; record in coordination/handoffs; old handoff home absent |
| Local coordination validation | Exit 0; 0 errors, 0 warnings; one deferred review request, no active claims |
| `scripts/check_guidance_drift.py` | Exit 0; 0 errors; pending Claude synchronization documented |
| Protected-file comparison | Exit 0; all 486 hashes unchanged |
| File-move workflow retry | Exit 0; 17,752 moved; 463 tracked moves; complete journal |
| Empty-tree archival | Exit 0; all 10 trees moved |
| Runtime installation | Exit 0; 45 files installed |
| Local handoff compatibility installation | Exit 0; 2 files installed |
| Full 467-test historical release regression | Not run in this cleanup turn; fixture path compatibility still needs checking before the updated reusable release |

The database SHA256 remains
`f17c977f8c5ffec13a279bdb909dd17f38e056e5183812a92ae5810b03251ed1`.
Conformance stays **80.6% (1450/1800)**. Incoming, raw sources, evidence,
approvals, audit phase and gates are unchanged. The owner's edited evidence-access
plan moved to `Enconet/docs/plans/` with its working bytes preserved and its edit
still unstaged. Other existing owner edits were preserved too.

## Exceptions and remaining work

Git staging first stopped on 75 line-ending-only changes. Each moved working
file still matched its original hash. Both Git versions were compared, the
original blobs were restored, and the archive attribute policy was corrected.
The retry passed. The proof is retained in the packet; no working file was rewritten.

Three Claude-owned archived plans remain at their original paths. Historical
test-folder remnants outside the ten archived homes still need the existing
final-cleanup disposition. No permission or ACL bypass was used.

The ADR resolution manifest uses the owner's session date in its ID. Its
`created_at_utc` value was a date placeholder, not a measured clock reading;
use commit `a35bfa1` for creation timing. The manifest is immutable and was not
rewritten. Its recorded pre-move hash remains correct.

Continue the original cleanup plan: finish the historical regression/path checks,
then CU-4 reusable release and known-vendor alignment. Do not add new plan slices.

## Evidence and recovery

- Exact plans, authorizations, test XML and hash comparisons:
  `PKE_SA_NQA1_doc/plans/cleanup-cu3/enconet-authorized-sprint-20261013/`.
- File, directory, runtime and handoff journals, plus original runtime files:
  `Enconet/work/migrations/cleanup-cu3-live-20261013/`.
- Original audit documents remain in their original `incoming/` and `raw/` homes.
