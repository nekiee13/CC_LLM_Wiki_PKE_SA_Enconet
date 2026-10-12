"""Prepare a fresh supplier file-map proposal; no migration or authorization."""
import argparse
import hashlib
import json
import os
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


def directory_preflight(root, supplier, plan):
    """Read-only coverage check; never prune or move a directory."""
    root = migration.root_path(root)
    if supplier in {'', '.', '..'} or Path(supplier).name != supplier:
        raise ValueError('one supplier directory required')
    prefix = supplier + '/'
    if any(not row['source'].startswith(prefix) or not row['destination'].startswith(prefix)
           for row in plan['files']):
        raise ValueError('foreign supplier directory plan')
    sources = {row['source'] for row in plan['files']}
    parents = {parent.relative_to(root).as_posix() for name in sources
               for parent in (root / name).parents if parent != root and parent.is_relative_to(root)}
    uncovered, blocked, directories, empty_moves = [], [], set(), []
    homes = {**MOVED, 'docs/reviews': 'work/reviews', '.pytest_cache': '.tmp/pytest-cache'}
    def walk_error(error):
        raise error
    for home, new_home in homes.items():
        name = prefix + home
        try:
            folder = migration.safe(root, name)
            if not folder.exists():
                continue
            if not folder.is_dir():
                raise ValueError('working home is not a directory')
            for current, child_dirs, files in os.walk(folder, followlinks=False, onerror=walk_error):
                current = Path(current)
                migration.safe(root, current.relative_to(root).as_posix())
                directories.add(current.relative_to(root).as_posix())
                for child in child_dirs:
                    migration.safe(root, (current / child).relative_to(root).as_posix())
                for child in files:
                    path = current / child
                    relative = path.relative_to(root).as_posix()
                    migration.safe(root, relative)
                    if relative not in sources:
                        uncovered.append(relative)
            if not any(folder.iterdir()):
                target_name = prefix + new_home
                if migration.safe(root, target_name).exists():
                    raise ValueError('empty-home destination already exists')
                empty_moves.append({'source': name, 'destination': target_name,
                                    'identity': migration.identity(folder),
                                    'operation': 'proposed exact native empty-directory rename; pending review'})
        except (ValueError, OSError) as error:
            blocked.append({'source': name, 'reason': str(error)})
    prune = sorted(directories & parents, key=lambda name: (name.count('/'), name), reverse=True)
    unhandled = []
    for name in sorted(directories - parents - {row['source'] for row in empty_moves}):
        folder = migration.safe(root, name)
        matching = [home for home in homes if name == prefix + home or name.startswith(prefix + home + '/')]
        if any(folder.iterdir()) or len(matching) != 1:
            unhandled.append(name)
            continue
        home = matching[0]
        target_name = prefix + homes[home] + name[len(prefix + home):]
        if migration.safe(root, target_name).exists():
            unhandled.append(name)
            continue
        empty_moves.append({'source': name, 'destination': target_name,
                            'identity': migration.identity(folder),
                            'operation': 'proposed exact native empty-directory rename; pending review'})
    return {'schema': 'supplier-directory-preflight-1', 'supplier': supplier,
            'uncovered_files': sorted(uncovered), 'blocked_homes': blocked,
            'prune_source_parents': prune, 'empty_home_moves': empty_moves,
            'other_empty_directories': unhandled,
            'passed': not uncovered and not blocked and not unhandled,
            'scope': 'Coverage/proposal only; directory identity and native ACLs must be rechecked before any move or pruning.'}


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
    # Frozen portable packages must retain their relative member paths as a unit.
    # Active dashboards remain standalone in outputs/RUN-*; this is history only.
    package_prefix = supplier + '/outputs/candidates/evidence_access/portable_package/'
    for row in rows:
        if row['source'].startswith(package_prefix):
            row['destination'] = (supplier + '/outputs/archive/legacy-outputs/candidates/evidence_access/'
                                  'portable_package/' + row['source'][len(package_prefix):])
    preview = migration.preview(WORKSPACE, plan)
    relocations = relocation_aliases(rows, supplier)
    directory_check = directory_preflight(WORKSPACE, supplier, plan)
    receipt = {'schema': 'supplier-cleanup-proposal-1', 'supplier': supplier, 'preview': preview,
               'held': held, 'changed_since_inventory': changes, 'preserve_edits_requested': preserve,
               'reference_adaptations': adaptations,
               'directory_preflight': directory_check,
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
            'directories_ready': directory_check['passed'],
            'reference_adaptations': adaptations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--supplier', required=True)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.supplier, args.destination)))


if __name__ == '__main__':
    main()
