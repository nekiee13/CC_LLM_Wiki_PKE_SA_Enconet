import json
from pathlib import Path
import subprocess
import sys

import pytest

RUNTIME = Path(__file__).parents[1] / 'runtime_v4'


@pytest.mark.parametrize('mode', ['good', 'foreign-target', 'bad-shape'])
def test_recorded_paths_resolve_local_history_and_refuse_foreign_targets(tmp_path, mode):
    project = tmp_path / 'Company with spaces'
    scripts = project / 'scripts'
    scripts.mkdir(parents=True)
    for name in ('project_layout.py', 'project_records.py'):
        (scripts / name).write_bytes((RUNTIME / name).read_bytes())
    (project / 'project-layout.json').write_text('{"schema_version":1,"layout":"v4"}')
    data = {'schema_version': 1, 'paths': {'out/old.json': 'outputs/archive/old.json'}}
    if mode == 'foreign-target':
        data['paths']['out/old.json'] = '../Other Company/private.json'
    if mode == 'bad-shape':
        data['extra'] = True
    (project / 'project-file-relocations.json').write_text(json.dumps(data))
    probe = scripts / 'probe.py'
    probe.write_text('''
from pathlib import Path
import sys
from project_records import recorded_path, recorded_path_at
from project_layout import ROOT
mode=sys.argv[1]
if mode=='good':
 assert recorded_path('out/old.json')==ROOT/'outputs/archive/old.json'
 assert recorded_path('manifests/approvals.csv')==ROOT/'work/manifests/approvals.csv'
 assert recorded_path(ROOT/'raw/manual.md')==ROOT/'raw/manual.md'
else:
 try: recorded_path('out/old.json')
 except ValueError: pass
 else: raise AssertionError('invalid relocation accepted')
for root,value in ((ROOT.parent/'Other Company','raw/file.md'),(ROOT,'../Other Company/file.md')):
 try: recorded_path_at(root,value)
 except ValueError: pass
 else: raise AssertionError('foreign reference accepted')
''')
    result = subprocess.run([sys.executable, '-B', str(probe), mode], capture_output=True,
                            text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
