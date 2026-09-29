# EK-1.1 validation evidence

Date: 2026-09-29. Codex implementation; Claude review pending.
Session starting HEAD: `6d6cab253b743f2d8c5e3ec85c1b5bc4e5e6ffe9`.

## Results

- Thirty focused copier safety tests passed.
- Full local tool suite: 56 passed, no skipped tests.
- Pinned manifest verification passed without changing the approved artifacts.
- Real CLI preview proposed only `Ekonerg/handoff_schema.yml`, 644 bytes.
- Existing Ekonerg files and their change times, plus directory membership,
  were unchanged by that preview. Runtime cache/environment folders were
  excluded from the snapshot; `-B` and the tool disable import-cache writes.
- Real CLI refused an unchanged copy request for the adapt-only support tool.
- Live apply and runtime framework checks are not-run. Nothing has been copied
  into the real framework, and no source document or database was created.

## Exact commands and exit codes

Run from the workspace root unless stated otherwise.

| Stage | Command | Exit | Evidence |
|---|---|---:|---|
| Initial RED | `python -B -m unittest discover -s Ekonerg\tools\tests -p test_safe_transfer.py -v` | 1 | Missing `safe_transfer` module before implementation |
| First GREEN | `python -B -m unittest discover -s Ekonerg\tools\tests -p test_safe_transfer.py -v` | 0 | 21 tests passed |
| Receipt-type RED | `python -B -m unittest discover -s Ekonerg\tools\tests -p test_safe_transfer.py -v` | 1 | 30 tests ran; malformed receipt identity type was not rejected |
| Receipt-type GREEN | `python -B -m unittest discover -s Ekonerg\tools\tests -p test_safe_transfer.py -v` | 0 | 30 tests passed after strict integer validation |
| Full local suite | `python -B -m unittest discover -s Ekonerg\tools\tests -v` | 0 | 56 passed: 30 copier, 18 manifest, 8 readability |
| Source integrity | `python -B Ekonerg\tools\transfer_manifest.py verify` | 0 | All 1,963 rows and scan match the approved source |
| Real preview | `python -B Ekonerg\tools\safe_transfer.py` | 0 | One create candidate; 225 adapt and 49 recreate pending; 1,688 excluded |
| Negative selection | `python -B Ekonerg\tools\safe_transfer.py --source scripts/agent_coord.py` | 1 | Correct refusal: source is not approved for unchanged copy |

Temporary-directory tests ran with approved execution outside the sandbox because
earlier workspace testing established its temporary Git permissions issue. All
apply operations in this task used fresh mock workspaces only. The Windows test
created a real junction from fake Ekonerg `docs/` to fake sibling Enconet, proved
apply refused it, then removed only that test junction. No test touched live data.

## Preview no-write check

This inline Python check was passed to `python -B -` through PowerShell stdin;
exit 0. It invokes the real CLI, not a mocked preview. Reviewers can run the
same code from the workspace root. It writes no evidence artifact.

```python
import json
import subprocess
from pathlib import Path

root = Path('Ekonerg')

def snapshot():
    found = {}
    for path in root.rglob('*'):
        if '.venv' in path.parts or '__pycache__' in path.parts:
            continue
        if path.is_file():
            found[str(path)] = (path.read_bytes(), path.stat().st_mtime_ns)
        elif path.is_dir():
            found[str(path)] = None
    return found

before = snapshot()
run = subprocess.run(
    ['python', '-B', 'Ekonerg/tools/safe_transfer.py'],
    capture_output=True, text=True, encoding='utf-8')
assert run.returncode == 0, run.stderr
report = json.loads(run.stdout)
assert snapshot() == before
assert len(report['copy']) == 1
assert report['copy'][0]['state'] == 'create'
assert not (root / 'handoff_schema.yml').exists()
print('PASS: read-only preview')
```

The preview identifies source commit
`9f20430c95334daa4c3cedb7ee71b002bd3be739` and manifest approval
`CC_2026-09-29T114644Z_ekonerg-transfer-manifest-approve`.
Approved manifest LF SHA-256:
`fd9d69ff5c7836c1696402aa7012177de3e625efd301274f8eeddedbaeafc3a4`.
Expected copied schema byte SHA-256:
`79908730a5519ae245eb0418641192fe9938582c37ac7f13d33e061efb7b358f`.

## Coverage and limits

Tests cover exact copying, no-overwrite conflicts before and after preview,
matching-file preservation, fake sibling bytes/change times, existing owner files,
wrong roots, traversal, actual junctions, mocked reparse points, hard links,
directories in place of files, manifest and plan tampering, changed source bytes,
copy-only selection, CLI approval hash and CRLF handling, explicit run IDs,
writer locks, journal corruption, resume, and read-only recovery diagnosis.

Interruption tests inject exceptions before or after durable receipts. They also
plant a partial file after an intent to prove it cannot be overwritten or claimed
as a removal candidate. They do not simulate power loss, a hostile concurrent
writer, or every filesystem crash behavior. The tool requires a single cooperative
writer, treats stale locks and torn journals as manual-review stops, and has no
automatic deletion or force-unlock command.

This is not EK-1.2 isolation evidence for copied support tools. It is evidence
for the copier itself. Adapt and recreate rows remain unimplemented. Live apply
must wait for Claude's review of target paths, preview, journal, and recovery.

No guidance, skills, shared environment, or indexes were modified. Shared indexes
remain at stale `62a0251`; current pinned Git objects and local files were used.
Unrelated Enconet and support-transfer changes, including Claude-owned unstaged
message deletions, were preserved.
