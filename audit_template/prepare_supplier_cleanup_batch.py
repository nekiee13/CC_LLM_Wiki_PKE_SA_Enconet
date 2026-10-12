"""Prepare a fresh supplier file-map proposal; no migration or authorization."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import zipfile

from prepare_framework_candidate_v4 import MOVED

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / 'scripts'))
import cleanup_migration as migration


def relocation_aliases(rows, supplier):
    """Resolve both original references and paths already routed by the runtime."""
    prefix = supplier + '/'
    aliases = {}
    for row in rows:
        if not row['source'].startswith(prefix) or not row['destination'].startswith(prefix):
            raise ValueError('foreign supplier relocation')
        old = row['source'][len(prefix):]
        new = row['destination'][len(prefix):]
        parts = old.split('/')
        candidates = [old]
        if parts[0] in MOVED:
            candidates.append('/'.join((MOVED[parts[0]], *parts[1:])))
        for name in candidates:
            if name in aliases and aliases[name] != new:
                raise ValueError('ambiguous relocated logical path')
            aliases[name] = new
    return {'schema_version': 1, 'paths': aliases}


def markdown_references(data, filenames):
    text = data.decode('utf-8')
    count = 0
    def replace(match):
        nonlocal count
        name = match.group(2)
        if name not in filenames:
            return match.group(0)
        count += 1
        return match.group(1) + filenames[name] + (match.group(3) or '') + ')'
    result = re.sub(r'(\]\()([^()?#\s]+)([?#][^)]*)?\)', replace, text)
    return result.encode('utf-8'), count


def prepare(supplier, destination):
    project = WORKSPACE / supplier
    if supplier in {'', '.', '..'} or Path(supplier).name != supplier or project.resolve().parent != WORKSPACE:
        raise ValueError('one local supplier folder required')
    destination = Path(destination).absolute()
    if destination.exists() or not destination.resolve().is_relative_to(WORKSPACE / 'PKE_SA_NQA1_doc/plans/cleanup-cu3'):
        raise ValueError('fresh cleanup packet directory required')
    previous = migration.load(WORKSPACE / 'PKE_SA_NQA1_doc/plans/cleanup-cu1/compiled-map/file-moves-final.zip')
    sources = {row['source']: dict(row) for row in previous['files'] if row['source'].startswith(supplier + '/')}
    # These homes have one explicit role. New records are proposed, not approved.
    for area, target in [('handoffs', 'coordination/handoffs'), ('.bootstrap', 'work/bootstrap'), ('backup', 'work/backup')]:
        folder = project / area
        if not folder.exists():
            continue
        for path in folder.rglob('*'):
            if not path.is_file():
                continue
            source = path.relative_to(WORKSPACE).as_posix()
            if source not in sources:
                sources[source] = {'source': source, 'destination': supplier + '/' + target + '/' + path.relative_to(folder).as_posix(),
                    'owner': 'claude-code' if path.name.startswith('CC_') or path.name == 'CLAUDE.md' else 'shared-or-owner',
                    'hold': None, 'basis': 'fresh explicit-home record; pending exact batch review',
                    'approval': 'pending', 'retention': 'keep exact bytes'}
    rows, held, changes = [], [], []
    dirty_result = subprocess.run(['git', 'diff', '--name-only', '-z'], cwd=WORKSPACE, capture_output=True, check=True)
    dirty = set(dirty_result.stdout.decode('utf-8').split('\0'))
    preserve = []
    for row in sources.values():
        try:
            source = migration.safe(WORKSPACE, row['source'])
            target = migration.safe(WORKSPACE, row['destination'])
            if not source.is_file() or target.exists():
                raise ValueError('missing source or existing destination')
            if row['owner'] not in {'codex', 'shared-or-owner'}:
                raise ValueError('Claude-owned record')
            digest = migration.digest(source)
            if row.get('sha256') and row['sha256'] != digest:
                changes.append({'source': row['source'], 'old_sha256': row['sha256'], 'current_sha256': digest})
            if row['source'] in dirty:
                preserve.append(row['source'])
            elif row.get('hold'):
                raise ValueError(row['hold'])
            row.update(sha256=digest, bytes=source.stat().st_size, hold=None, approval='pending-exact-batch-review')
            rows.append(row)
        except (ValueError, OSError) as error:
            held.append({'source': row['source'], 'reason': str(error)})
    plan = {'schema': 'cleanup-file-map-1', 'status': 'proposal-not-authorized', 'files': rows, 'collisions': []}
    adaptations = []
    for row in rows:
        if row['destination'].endswith('/report.md'):
            canonical = row['destination']
            parent = Path(canonical).parent.as_posix()
            names = {Path(other['source']).name: Path(other['destination']).name for other in rows
                     if Path(other['destination']).parent.as_posix() == parent}
            original = (WORKSPACE / row['source']).read_bytes()
            result, count = markdown_references(original, names)
            if count:
                retained = parent + '/revisions/relocated-originals/' + Path(row['source']).name
                row['destination'] = retained
                adaptations.append({'source': row['source'], 'retained_original': retained,
                    'canonical_destination': canonical, 'operation': 'markdown-artifact-link-update',
                    'original_sha256': row['sha256'],
                    'adapted_sha256': hashlib.sha256(result).hexdigest(), 'updated_links': count})
    preview = migration.preview(WORKSPACE, plan)
    relocations = relocation_aliases(rows, supplier)
    receipt = {'schema': 'supplier-cleanup-proposal-1', 'supplier': supplier, 'preview': preview,
               'held': held, 'changed_since_inventory': changes, 'preserve_edits_requested': preserve,
               'reference_adaptations': adaptations,
               'plan_sha256': migration.plan_hash(plan),
               'limits': ['Not authorization; fresh rows/content and preserve-edits need exact review.',
                          'No pruning, code installation or current-artifact reference edits applied.']}
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in [('file-map.json', plan), ('preview.json', receipt),
                       ('file-relocations.json', relocations)]:
        with zipfile.ZipFile(destination / (name + '.zip'), 'x', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(name, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    for adaptation in adaptations:
        original = (WORKSPACE / adaptation['source']).read_bytes()
        parent = Path(adaptation['canonical_destination']).parent
        names = {Path(row['source']).name: Path(row['destination']).name for row in rows
                 if Path(row['destination']).parent == parent}
        body, count = markdown_references(original, names)
        if hashlib.sha256(body).hexdigest() != adaptation['adapted_sha256'] or count != adaptation['updated_links']:
            raise ValueError('reference adaptation changed during preparation')
        with (destination / 'canonical-report.md').open('xb') as stream:
            stream.write(body)
    return {'selected': len(rows), 'held': len(held), 'changed': len(changes),
            'preserve_edits': preserve, 'blocked': preview['blocked'], 'plan_sha256': migration.plan_hash(plan),
            'reference_adaptations': adaptations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--supplier', required=True)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.supplier, args.destination)))


if __name__ == '__main__':
    main()
