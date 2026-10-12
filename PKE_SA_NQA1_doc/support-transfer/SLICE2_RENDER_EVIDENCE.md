# Slice-2 rendered-tree evidence

The exact candidate for CC_FIN content commit A is
`doc/support-transfer/rendered/slice2/`: 14 files rendered at
`2026-07-18T11:54:00Z`. The committed rendered tree, not a fresh run, is byte
authority. Exact reproduction uses:

`python doc/support-transfer/rendered/render_slice2.py --timestamp 2026-07-18T11:54:00Z`

## Inventory and target state

- **passed** — inventory is exactly the 14 create paths in
  `M2_DRY_RUN_MANIFEST.md`; no extra file or cache is present; exit 0.
- **passed** — all 14 target paths are absent in clean CC_FIN at published slice-1
  HEAD `879bcb507e461282c68cb20beab77c0def9019a4`; present count 0.
- **passed** — CC_FIN `pytest.ini` has `testpaths = tests`; `scripts/` is outside
  normal discovery. This is a scope fact only, not a substitute for the required
  native A/B runs.

## Fail-closed render and byte reproduction

- The renderer builds into a disposable target root, runs the rendered target
  validator there, verifies the exact inventory and initial BOARD state, and only then
  replaces `rendered/slice2/`.
- Unknown/unresolved placeholders fail. The only retained `{{...}}` values are the
  exact T4 allowlist inside `guidance-semantics.template.md`; they are intentional
  template fields. `TEAM_PROTOCOL.md` has no unresolved placeholder.
- Sensitive-pattern, forbidden-workspace-reference, inventory, validator, and
  relative-link defects fail before publication. The scanner source necessarily
  contains its own sensitive regex signatures; the renderer excludes exactly the
  declared `SENSITIVE_PATTERNS` table from self-scan while scanning the remainder of
  `_support_shared.py` and every other output.
- **passed** — first fixed-timestamp render: target validation 0 errors, 0 warnings;
  exact 14 files; initial archive count 0; `HANDOFF.md missing`; renderer exit 0.
- **passed** — fixed-timestamp rerun: 14 files before, 14 after, SHA-256 difference
  count 0; renderer exit 0.

## Target adaptations

1. **Sibling import** — staged `from _shared ...` becomes target-local
   `from _support_shared ...`; the rendered CLI executed successfully, proving import
   resolution with installed target names.
2. **Tracked placeholders** — `messages/README.md` and `archive/README.md` are skipped
   by Markdown record loading; archive count excludes its README. `claims/README.md`
   is Markdown and claim loading remains YAML-only. Initial validation with all three
   placeholders returned 0 errors, 0 warnings and BOARD archive count 0.
3. **Deterministic BOARD** — `write_board` and the target CLI accept a reviewed UTC
   timestamp and `write_board` uses explicit LF newlines, preventing Windows CRLF
   translation from changing the reviewed/staged blob. Omitting the timestamp retains
   normal current-UTC behavior. The generated header names
   `agent_coord.render_board`, matching the installed module.
4. **Pre-slice-3 pointer state** — absence is represented, not hidden. Disposable
   probe results: initial validation exit 0; copying a HANDOFF pointer without BOARD
   regeneration produced the expected stale-board error and exit 1; regeneration
   with a fixed timestamp returned exit 0 and BOARD named the pointer.
5. **Target-local documentation** — staged/Wiki installation prose is replaced by
   clone-complete target runtime documentation; no runtime Wiki path or import remains.

## Target-adapted fault-injection suite

The accepted 33-test coordination module was loaded from the rendered
`scripts/agent_coord.py` (with the rendered sibling helper), not from the staged
validator:

- first attempt: unavailable before test bodies ran — pytest's default temporary root
  was access-denied by the Windows environment; 33 setup errors, exit 1;
- rerun with an explicit disposable base: 30 passed, 3 failed, exit 1. The three
  overlap fixtures hard-code claim expiry `2026-07-18T01:00:00Z`, which preceded the
  actual run; the validator correctly treated those claims as inactive;
- controlled-time rerun with validator time frozen inside the unchanged fixtures'
  validity window: **33 passed**, exit 0.

The controlled clock changes no target file or validator source. It demonstrates the
intended active-claim overlap behavior while preserving the production rule that
expired claims do not retain exclusivity. The first harness import also created two
local `__pycache__` files before bytecode suppression was applied; the final inventory
audit caught them, and a fixed-timestamp regeneration removed them. Final state is
exactly 14 files and zero cache directories. All disposable roots were removed.

## Pre-commit staging stop and LF correction

After Claude accepted briefing v1, Codex copied the 14 candidate files into clean
CC_FIN and staged exactly those 14 paths. The mandatory staged-blob comparison stopped
before commit A: 13 blobs matched, while `coordination/BOARD.md` differed. The source
BOARD had Windows CRLF bytes because target `Path.write_text` used platform-default
newline translation; Git correctly normalized the staged blob to LF. No commit was
created. Codex unstaged and removed only the 14 uncommitted slice-2 files, restoring
CC_FIN clean at `879bcb507e461282c68cb20beab77c0def9019a4`, divergence `0 0`.

Briefing v2 and the corrected target writer now pass `newline="\n"` explicitly.
Post-correction evidence:

- fixed-timestamp render: exit 0, 14 exact files, target validation 0 errors/warnings;
- BOARD raw-byte audit: 0 CR bytes, 18 LF bytes;
- simulated CC_FIN Git filtering for every reviewed path: 14 raw blobs compared,
  mismatch count 0;
- target-adapted controlled-time suite: 33 passed, exit 0;
- CC_FIN remains clean/synchronized and all 14 paths are absent.

This changes the rendered target script by the explicit LF argument. BOARD's logical
content and timestamp are unchanged, but its working-tree byte production is now
platform-stable. Independent rereview is required before another target copy.

## Initial BOARD state

The reviewed BOARD is generated evidence with:

- active claims: none;
- active messages: none;
- pointer: `HANDOFF.md missing`;
- archive: 0 records;
- generation timestamp: `2026-07-18T11:54:00Z`.

Slice 3 must regenerate BOARD when it creates HANDOFF.md. Because the accepted dry-run
manifest labels slice 3 create-only, its own pre-job briefing must make the generated
BOARD evidence modification explicit or stop for an owner-reviewed scope amendment.

## Checks intentionally pending until target commits

No CC_FIN file was changed while producing this evidence. Content-A blob comparison,
target validation at A/B, native pytest A/B, exact 54-tuple comparisons, evidence
commit B, final identity, and pre-push review remain pending and must not be reported
as passed before their commands exist.
