"""Render the M2-amendment-1 slice-1 tree into doc/support-transfer/rendered/slice1/.

Fail-closed: unresolved placeholders, sensitive patterns, Wiki references, or
unresolvable relative Markdown links abort before any file is written.

Byte authority: the COMMITTED rendered tree is commit A's byte authority. A fresh
run stamps a fresh UTC time into the two timestamped records unless the reviewed
timestamp is supplied for exact byte reproduction:

    python render_slice1.py --timestamp 2026-07-18T05:42:39Z
"""
import argparse
import re, sys, shutil
from pathlib import Path
from datetime import datetime, timezone

WIKI = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WIKI / 'doc/support-transfer/staged'))
from _shared import scan_sensitive

TPL = WIKI / 'doc/support-transfer/templates'
OUT = WIKI / 'doc/support-transfer/rendered/slice1'
_args = argparse.ArgumentParser(description=__doc__)
_args.add_argument('--timestamp', help='fixed UTC render timestamp '
                   '(YYYY-MM-DDTHH:MM:SSZ) for exact byte reproduction')
_ns = _args.parse_args()
if _ns.timestamp:
    datetime.strptime(_ns.timestamp, '%Y-%m-%dT%H:%M:%SZ')
NOW = _ns.timestamp or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
BASE = '238c207c73970f3d3c6dc00c2db5932ebeca7be4'

PROFILE = """# CC_FIN support profile (target-local controlled authority)

## Control

- Repository: `https://github.com/nekiee13/CC_FIN` (`main`)
- Record class: Controlled (see [RECORD-KEEPING.md](RECORD-KEEPING.md))
- Provenance (history, not a runtime reference): profile v1.0 approved by the human
  project owner on 2026-07-16 at transfer gate M1; target-local installation authorized
  by the owner's transfer gate M2 decision and its amendment 1 on 2026-07-18.
- This file is the target-local support authority for ownership, enabled modules,
  validation composition, sensitivity, scale, and recovery. It never replaces product
  requirements: where scopes conflict, product authority outranks support workflow.

## Identity, roles, and authority

The human owner approves gates, authority changes, destructive recovery,
hosted-governance changes, and release decisions. Codex owns `AGENTS.md`, `.agents/`,
and `CX_` records. Claude owns `CLAUDE.md`, `.claude/`, and `CC_` records. Neutral
coordination, support schemas, decision registers, logs, handoffs, and generated
board/status views are shared by contract. An agent may inspect but not edit the other
agent's infrastructure.

Existing feature ADRs, project documentation, GitHub workflows/templates, the
documentation freshness ledger, and the enhanced product Master Plan remain
authoritative in their existing scopes; support records link to them and do not copy or
renumber them.

## Enabled modules

| Module | State | Rationale |
|---|---|---|
| Governance/records/ADR/handoff/validation/recovery core | Enabled | Required portable contract |
| Dual-agent ownership and immutable messaging | Enabled | Both agents are active writers |
| Multi-writer claims and generated board | Enabled | Prevent overlapping edits |
| Lightweight human milestone gates | Enabled | Owner control without a product state machine |
| Documentation and code indexes | Enabled only after committed-state preflight | Navigation support at repository scale |
| Hosted-governance adapter | Integrate existing files; any mutation separately approved | Existing GitHub controls must not be shadowed |
| Release adapter | Inventory only | No tags or releases requested |
| Repo-local workflow skills | Disabled initially | No proven repeated target-specific workflow yet |
| Formal workflow state machine | Disabled | Product work does not require a phase engine |

## Native validation contract

Support checks add a fast layer and compose with, never replace, native checks:

1. support schema, reference, ownership, message, claim, board, and handoff validators;
2. focused `python -m pytest` tests for changed support integration;
3. relevant existing unit/integration tests;
4. broader `python -m pytest` when proportional to risk;
5. targeted Ruff checks where already applicable;
6. CPI tests only when CPI prerequisites exist and the change touches CPI behavior;
7. existing CI as hosted evidence after push.

Skipped, unavailable, blocked, and not-run checks are never reported as passed. Support
validators must not trigger forecasting, model generation, dashboard rendering, or
expensive data pipelines.

## Product preservation

The three chart-generation paths, including the A-F standalone Cockpit/dashboard,
remain product capabilities. Support work does not change their status, wiring, data,
or acceptance; pipeline work recorded as seeded/pending remains a product-plan concern.

## Sensitivity and indexing

Secrets stay outside Git; records may name environment-variable contracts but never
values. Tracked datasets, spreadsheets, output snapshots, model fixtures, vendor trees,
archives, generated output, caches, debug material, and machine-private paths are
excluded from support records and indexes; a committed path may be cited with a
checksum when necessary. Index profiles include committed source, tests, and
authoritative documentation only; an index refresh requires one explicit claim and
committed-state verification.

## Scale assumptions

One human owner, two agents, low concurrent write volume, on the order of a thousand
tracked files, moderate support-record growth, Git retention, and support validation
measured in seconds. No database, service, queue, or runtime dependency enters the
product.

## Git and hosted workflow

Work stays on `main` in small reversible commits. Publication is sequential and
reviewed before push. No force push, history rewrite, broad reset, branch-protection
mutation, tag, or release is authorized. Hosted branch protection remains `unknown`
until independently verified. The known workflow branch-filter mismatch is handled
only through its separately approved isolated change. One narrow exception exists as
history: the owner's transfer-gate amendment authorized a single reset of one rejected,
never-pushed local commit to its recorded parent; that authorization was one-time and
never extends to routine recovery or to any pushed commit.

## Product-work boundary

Product issues, backlog, and progress stay in the product Master Plan and GitHub
issue governance; support records link to them and never form a competing backlog.
Release creation remains out of scope for support work.

## Recovery

Before each publication slice, capture HEAD, upstream, clean status, and the allowed
path list. Abort on drift, ownership conflict, unexpected generated files, secret or
data exposure, failing support checks, or changed product behavior. Revert only
identified support commits after owner approval; never use `reset --hard` as routine
recovery and never remove unrelated work. Re-run preflight and native focused checks
after any rollback.
"""

ownership = (
    "Codex owns `AGENTS.md`, `.agents/`, and `CX_` records. Claude owns `CLAUDE.md`,\n"
    "`.claude/`, and `CC_` records. Neutral coordination, support schemas, decision\n"
    "registers, logs, handoffs, and generated board/status views are shared by contract;\n"
    "an agent may inspect but not edit the other agent's infrastructure. The human owner\n"
    "decides gates, authority changes, destructive recovery, hosted-governance changes,\n"
    "and releases.")

authorities = (
    "- Enhanced product Master Plan: `docs/project/CC_FIN_project_upgrade_plan_enhanced.md`\n"
    "- Architecture / AS-IS: `docs/project/AS-IS.md`\n"
    "- Feature/integration ADRs: `docs/integration-pilot/adr/` (existing IDs, paths, and scopes retained)\n"
    "- Documentation index and freshness ledger: `docs/README.md`, `docs/documentation_freshness_ledger.md`\n"
    "- GitHub workflows, templates, and issue governance: `.github/`")

# One literal, executable PowerShell command (AM1-RR5). The A and B runs differ
# only in the fixed report filename; reporting-only flags, no -W or other
# behavior change.
PYTEST_CMD_A = ("$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest "
                "-p no:cacheprovider --continue-on-collection-errors -q --tb=no "
                '--junitxml="$env:TEMP' + chr(0x5c) + 'fin_slice1_A.xml"')
PYTEST_CMD_B = PYTEST_CMD_A.replace('fin_slice1_A.xml', 'fin_slice1_B.xml')

values = {
    'PROJECT_NAME': 'CC_FIN',
    'PRODUCT_PLAN_PATH': 'docs/project/CC_FIN_project_upgrade_plan_enhanced.md',
    'SUPPORT_PROFILE_PATH': 'support/PROFILE.md',
    'UTC_TIMESTAMP': NOW,
    'GIT_HEAD': BASE + ' (pre-slice parent; this file first lands in slice-1 content commit A)',
    'UPSTREAM_RELATION': 'synchronized 0 0 with origin/main at observation',
    'WORKTREE_STATE': 'clean at observation, before the slice-1 commits',
    'SUPPORT_MILESTONE': ('transfer gate M2 approved with amendment 1 (slices 1-3, 3c, 5, 6 '
        'authorized; slice 4 deferred); slice-1 content rendered and reviewed, commits A and B pending'),
    'ACTIVE_WORK_SUMMARY': ('- Slice 1 (8 neutral support records): content commit A, the '
        'like-for-like validation run, and evidence commit B follow the two-commit protocol; '
        'push blocked until reviewer acceptance.\n'
        '- Slices 2 (coordination core), 3 (handoff core), and 3c (index closure) authorized and pending.'),
    'COORDINATION_SUMMARY': ('The coordination core (protocol, queues, claims, generated board) '
        'arrives with slice 2; no target-local messages, claims, or blockers exist yet.'),
    'VALIDATION_SUMMARY': ('Pending for this slice: after content commit A, the like-for-like '
        'native run executes exactly this PowerShell command from the repository root: `'
        + PYTEST_CMD_A + '`. Expected literal outcome is exit code 1 with the identical '
        'recorded failing/erroring tuple set (54 nodes, 0 new / 0 gone / 0 mutated). The '
        'result is recorded as a support-validated event in [log.md](log.md) by evidence '
        'commit B, which touches only log.md and this file (neither is collected by the '
        'native suite: pytest testpaths=tests). The final-tree check re-runs the identical '
        'command at clean HEAD B with the report name fin_slice1_B.xml. No validation claim '
        'is authored before the run exists.'),
    'NEXT_ACTION_OWNER': 'claude-code (implementer this slice)',
    'NEXT_ACTION_PREREQUISITES': 'content commit A exists; worktree clean',
    'NEXT_ACTION': ('Run the like-for-like native suite (entry point, one literal PowerShell '
        'command from the repository root: `' + PYTEST_CMD_A + '`), compare tuples against '
        'the recorded baseline set, then write evidence commit B appending the '
        'support-committed-local and support-validated events to log.md and refreshing this '
        'status; then hand to reviewer codex'),
    'NEXT_ACTION_STOP_CONDITION': ('Any new, disappeared, or mutated tuple; any porcelain entry '
        'outside log.md and current-status.md at commit B; reviewer findings'),
    'STATUS_EVIDENCE_LINKS': ('- Slice-1 events (support-prepared now; support-committed-local '
        'and support-validated appended by evidence commit B) in [log.md](log.md)\n'
        '- Record classes in [RECORD-KEEPING.md](RECORD-KEEPING.md)\n'
        '- Sensitivity/module/recovery authority in [PROFILE.md](PROFILE.md)'),
}

def render(name: str) -> str:
    text = (TPL / f'{name}.template.md').read_text(encoding='utf-8')
    for k, v in values.items():
        text = text.replace('{{' + k + '}}', v)
    left = re.findall(r'\{\{[A-Z_]+\}\}', text)
    assert not left, f'{name}: unresolved placeholders {left}'
    return text

record_keeping = render('record-keeping')
# Target-local additions per AM1-F4: PROFILE.md row; no adr.template.md row exists in
# the template (and none is installed target-side).
record_keeping = record_keeping.replace(
    '| `support/README.md` | Controlled |',
    '| `support/README.md` (arrives with the index-closure slice) | Controlled |\n'
    '| `support/PROFILE.md` | Controlled |')

log_initial = render('event-log').rstrip('\n') + '\n' + (
    f'support-prepared | {NOW} | SLICE-1 | Eight neutral support records rendered and '
    'disposable read-back verified for slice-1 content commit A under owner-approved '
    'transfer gate M2 amendment 1; the commit-operation and validation events are '
    'appended by evidence commit B with their actual UTC times; implementer '
    'claude-code, reviewer codex | claude-code\n')

values['TARGET_DECISION_AUTHORITIES'] = authorities
adr_register = render('adr-register')

outputs = {
    'support/PROFILE.md': PROFILE,
    'support/current-status.md': render('current-status'),
    'support/log.md': log_initial,
    'support/RECORD-KEEPING.md': record_keeping,
    'support/decisions/README.md': adr_register,
    'support/AFI.md': render('afi-ledger'),
    'support/LESSONS-LEARNED.md': render('lessons-ledger'),
    'support/GOOD-PRACTICES.md': render('good-practices-ledger'),
}

FIN = Path(r'C:/xPY/xPrj/CC_FIN')
errors = []
for rel, text in outputs.items():
    hits = scan_sensitive(text)
    if hits:
        errors.append(f'{rel}: sensitive {hits}')
    for token in ('LLM_Wiki', '03_PKE', 'Enconet', 'xPY'):
        if token in text:
            errors.append(f'{rel}: forbidden reference {token!r}')
    # relative markdown links must resolve inside the slice tree or existing FIN paths
    for m in re.finditer(r'\]\(([^)#\s]+)\)', text):
        link = m.group(1)
        if link.startswith(('http://', 'https://')):
            continue
        src_dir = Path(rel).parent
        resolved = (src_dir / link).as_posix()
        parts = []
        for seg in resolved.split('/'):
            if seg == '..':
                parts.pop()
            elif seg != '.':
                parts.append(seg)
        norm = '/'.join(parts)
        if norm not in outputs and not (FIN / norm).exists():
            errors.append(f'{rel}: unresolved relative link {link!r} -> {norm}')
assert not errors, '\n'.join(errors)

if OUT.exists():
    shutil.rmtree(OUT)
for rel, text in outputs.items():
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')
    print('rendered', rel, f'({len(text.splitlines())} lines)')
print('ALL CHECKS PASSED: no sensitive patterns, no forbidden references, all relative links resolve')
