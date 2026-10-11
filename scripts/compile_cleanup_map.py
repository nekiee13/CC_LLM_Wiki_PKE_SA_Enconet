"""Compile a review-only file move map. There is deliberately no apply command."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import closing
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sqlite3
import xml.etree.ElementTree as ET
import zipfile

from cleanup_inventory import digest

RUN = re.compile(r'RUN-\d{8}-\d+')
PLAN = re.compile(r'(?i)(?:^|[_-])PLAN(?:[_-]|\.|$)')


def relative(value):
    parts = PurePosixPath(value).parts
    if not parts or PurePosixPath(value).is_absolute() or any(p in {'.','..'} or ':' in p for p in parts) or '\\' in value:
        raise ValueError('unsafe relative path')
    return parts


def compile_rows(entries, suppliers, preferred, known_runs, working_roles=None):
    working_roles=working_roles or {}
    files, special = [], []
    for entry in entries:
        source = entry['path']
        parts = relative(source)
        disposition = entry['disposition']
        if disposition == 'hold-redirect-or-hardlink' or entry['type']=='redirect':
            special.append({'source':source,'hold':disposition,'owner':entry['owner']})
            continue
        if entry['type'] != 'file':
            continue
        if parts[0] in {'audit_template','audit_archives'} or any(p in {'.agents','.claude','.git'} for p in parts):
            continue
        company = parts[0] if parts[0] in suppliers else None
        if company and len(parts)>1 and parts[1] in {'raw','incoming','db','sieving'}:
            continue
        destination = entry.get('new_path') or source
        basis = 'inventory path contract'
        if source in preferred:
            destination = preferred[source]['destination']
            basis = preferred[source].get('basis','explicit current artifact selected from hash-verified run manifest')
        elif source in working_roles:
            destination=PurePosixPath(company,'work','validation','legacy-'+parts[1],*parts[2:]).as_posix()
            basis=working_roles[source]
        elif company and len(parts)>1 and parts[1] in {'out','outputs'}:
            area = parts[1]
            path_runs = set(RUN.findall(source))
            proved = [r for r in path_runs if (company,r) in known_runs]
            if len(path_runs)==1 and len(proved)==1:
                run = proved[0]
                tail = list(parts[2:])
                if tail[:2]==['candidates','evidence_access']:
                    tail=tail[2:]
                if tail and tail[0]==run:
                    tail=tail[1:]
                if not tail:
                    tail=[parts[-1]]
                destination = PurePosixPath(company,'outputs',run,'revisions','legacy-'+area,*tail).as_posix()
                basis = 'existing path run ID verified against this supplier database; retained revision'
            else:
                destination = PurePosixPath(company,'outputs','archive','legacy-'+area,*parts[2:]).as_posix()
                basis = 'retained history; no proved run identity'
        elif company and PLAN.search(parts[-1]) and parts[-1].lower().endswith('.md') and (len(parts)==2 or parts[1]=='docs') and not (len(parts)>2 and parts[2] in {'reviews','context'}):
            if len(parts)>2 and parts[2]=='plans':
                continue
            tail = parts[2:] if len(parts)>2 else parts[1:]
            destination = PurePosixPath(company,'docs','plans',*tail).as_posix()
            basis = 'framework plan, not supplier source; frozen content unchanged'
        elif parts[0]=='doc' and PLAN.search(parts[-1]) and parts[-1].lower().endswith('.md'):
            destination = PurePosixPath('PKE_SA_NQA1_doc','plans',*parts[1:]).as_posix()
            basis = 'workspace framework plan'
        elif parts[0] in {'.pytest_cache','.reset-test-work'}:
            destination = PurePosixPath('.tmp','retained',*parts).as_posix()
            basis = 'retain workspace test scratch'
        if destination==source:
            continue
        relative(destination)
        hold = None
        if entry['owner']=='claude-code':
            hold = 'Claude-owned move'
        if disposition.startswith('hold-') and disposition not in {'hold-assign-result-run-or-validation-history'}:
            hold = disposition
        if entry.get('dirty'):
            hold = 'hold-existing-dirty-content'
        files.append({'source':source,'destination':destination,'owner':entry['owner'],
                      'sha256':entry.get('sha256'),'bytes':entry.get('bytes'),
                      'basis':basis,'hold':hold,'approval':'pending','retention':'keep exact bytes',
                      'requires_live_recheck':True})
    groups = defaultdict(list)
    for entry in files:
        groups[entry['destination'].casefold()].append(entry)
    collisions = []
    for group in groups.values():
        if len(group)>1:
            collisions.append({'destination':group[0]['destination'],'sources':[x['source'] for x in group]})
            for entry in group:
                entry['hold']='destination collision'
    return {'files':files,'special_holds':special,'collisions':collisions}


def load_preferred(root, config, known_runs, entries):
    snapshot = {e['path']:e for e in entries}
    result = {}
    for supplier, choice in config.items():
        manifest_rel = choice['manifest']
        relative(manifest_rel)
        if not manifest_rel.startswith(supplier+'/'):
            raise ValueError('foreign manifest')
        manifest = json.loads((root/manifest_rel).read_text(encoding='utf-8'))
        run = manifest['run_id']
        if (supplier,run) not in known_runs:
            raise ValueError('current manifest run missing from local database')
        pins = {}
        for artifact in manifest.get('artifacts',[]):
            if artifact.get('destination'):
                pins[supplier+'/'+artifact['destination']]=artifact['sha256']
        for artifact in manifest.get('files',[]):
            pins[(PurePosixPath(manifest_rel).parent/artifact['path']).as_posix()]=artifact['sha256']
        for source, filename in choice['artifacts'].items():
            relative(source)
            if len(relative(filename))!=1 or not source.startswith(supplier+'/'):
                raise ValueError('unsafe selected artifact')
            expected = pins.get(source)
            if not expected or snapshot.get(source,{}).get('sha256')!=expected or digest(root/source)!=expected:
                raise ValueError('selected artifact is not exact manifest/snapshot bytes')
            result[source]={'destination':str(PurePosixPath(supplier,'outputs',run,filename)),
                            'manifest':manifest_rel,'run_id':run,'sha256':expected}
        dark = choice.get('dark_artifact')
        if dark:
            source, provenance_rel = dark['path'],dark['provenance']
            relative(source)
            relative(provenance_rel)
            if not source.startswith(supplier+'/') or not provenance_rel.startswith(supplier+'/'):
                raise ValueError('foreign dark artifact')
            if digest(root/provenance_rel)!=snapshot.get(provenance_rel,{}).get('sha256'):
                raise ValueError('dark provenance changed since snapshot')
            provenance=json.loads((root/provenance_rel).read_text(encoding='utf-8'))
            expected=provenance['dark_sha256']
            lights=[s for s,name in choice['artifacts'].items() if name=='dashboard_light.html']
            if len(lights)!=1 or Path(provenance['source']).resolve()!=(root/lights[0]).resolve():
                raise ValueError('dark provenance references a different light artifact')
            if provenance['source_sha256']!=pins[lights[0]] or snapshot.get(source,{}).get('sha256')!=expected or digest(root/source)!=expected:
                raise ValueError('dark artifact hash/source mismatch')
            result[source]={'destination':str(PurePosixPath(supplier,'outputs',run,'dashboard_dark.html')),
                            'manifest':provenance_rel,'run_id':run,'sha256':expected,
                            'basis':'dark artifact/source hashes verified against existing provenance'}
    return result


def validation_roles(root,entries,suppliers):
    """Recognize test receipts by their content, never by a date or run guess."""
    roles={}
    for entry in entries:
        parts=relative(entry['path'])
        if entry['type']!='file' or parts[0] not in suppliers or len(parts)<3 or parts[1] not in {'out','outputs'}:
            continue
        if entry['disposition']=='hold-redirect-or-hardlink':
            continue
        path=root/entry['path']
        suffix=path.suffix.lower()
        if suffix not in {'.json','.xml','.log'} or digest(path)!=entry.get('sha256'):
            continue
        try:
            if suffix=='.log':
                roles[entry['path']]='retained diagnostic log'
            elif suffix=='.xml' and ET.parse(path).getroot().tag in {'testsuite','testsuites'}:
                roles[entry['path']]='verified JUnit test receipt'
            elif suffix=='.json':
                data=json.loads(path.read_text(encoding='utf-8'))
                if isinstance(data,dict) and isinstance(data.get('checks'),list):
                    roles[entry['path']]='validation checks receipt by JSON structure'
                elif isinstance(data,dict) and 'crumb_count' in data and 'field_completeness_percent' in data:
                    roles[entry['path']]='sieving quality metrics by JSON structure'
        except (ValueError,ET.ParseError,UnicodeError):
            continue  # unknown artifacts stay retained history, not guessed logs
    return roles


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace',type=Path,required=True)
    parser.add_argument('--inventory',type=Path,required=True)
    parser.add_argument('--selection',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=args.workspace.resolve()
    out=args.output.absolute()
    out.relative_to(root)
    if out.exists() or out.parent.resolve()!=out.parent.absolute():
        raise ValueError('output must be fresh under a non-redirected parent')
    if any(p in {'raw','incoming','db','.claude','.agents'} for p in out.relative_to(root).parts):
        raise ValueError('protected output destination')
    with zipfile.ZipFile(args.inventory) as archive:
        if archive.testzip() is not None or archive.namelist()!=['inventory.json']:
            raise ValueError('invalid inventory archive')
        record=json.loads(archive.read('inventory.json'))
    if record['access_failures'] or record['changed_protected_inputs']:
        raise ValueError('incomplete inventory; cannot compile')
    known=set()
    for supplier in record['suppliers']:
        path=root/supplier/'db/nqa_audit.sqlite'
        if not path.exists():
            continue
        with closing(sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True)) as conn:
            conn.execute('PRAGMA query_only=ON')
            for table in ('sieve_runs','evaluation_runs'):
                known.update((supplier,r[0]) for r in conn.execute('SELECT run_id FROM '+table))
    selected=load_preferred(root,json.loads(args.selection.read_text(encoding='utf-8')),known,record['entries'])
    roles=validation_roles(root,record['entries'],record['suppliers'])
    result=compile_rows(record['entries'],record['suppliers'],selected,known,roles)
    for entry in result['files']:
        if (root/entry['destination']).exists():
            entry['hold']='existing destination; no overwrite'
    result.update(schema='cleanup-file-map-1',status='proposal-not-approved',
                  capture_head=record['git_head'],input_inventory_sha256=digest(args.inventory),
                  selected_current_artifacts=selected,
                  limits=['No apply command; no directory moves; no deletes.',
                          'History status and immutable bytes unchanged.',
                          'Live SHA/path/permission checks required before migration.',
                          'Run identity does not imply active generation or approval.'])
    result['summary']={'file_rows':len(result['files']),'collisions':len(result['collisions']),
                       'special_holds':len(result['special_holds']),
                       'holds':dict(Counter(x['hold'] or 'pending review' for x in result['files'])),
                       'basis':dict(Counter(x['basis'] for x in result['files']))}
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(result,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
    print(json.dumps(result['summary']))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
