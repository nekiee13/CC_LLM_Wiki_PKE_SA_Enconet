import json
from pathlib import Path
import shutil
import subprocess
import sys

TEMPLATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEMPLATE))
import framework_release


def test_preserving_copy_and_inventory(tmp_path):
    company = tmp_path / 'New Company'
    company.mkdir()
    framework_release.apply(company, 'fixture-install', framework_release.spec())
    shutil.copyfile(TEMPLATE / 'runtime_v2/promote_source.py', company / 'scripts/copy_incoming_source.py')
    shutil.copyfile(TEMPLATE / 'runtime_v2/incoming_inventory.py', company / 'scripts/incoming_inventory.py')
    (company / 'incoming/source.md').write_text('# Quality controls\nDatum objavljivanja: 14.04.2023.\n', encoding='utf-8')
    (company / 'incoming/desktop.ini').write_text('not evidence')
    def run(script, *args):
        return subprocess.run([sys.executable, str(company / 'scripts' / script), *args], cwd=tmp_path,
                              capture_output=True, text=True)
    assert run('init_db.py').returncode == 0
    args = ['source.md','--title','Quality controls','--supplier','New Company','--language','en','--side','DOCUMENT']
    assert run('copy_incoming_source.py', *args).returncode == 0
    assert not (company / 'raw/source.md').exists()
    assert run('copy_incoming_source.py', *args, '--apply').returncode == 0
    assert (company / 'incoming/source.md').read_bytes() == (company / 'raw/source.md').read_bytes()
    assert run('copy_incoming_source.py', *args, '--apply').returncode == 1
    assert run('copy_incoming_source.py', '../Other/source.md', *args[1:], '--apply').returncode == 1
    output = company / 'out/inventory.json'
    assert run('incoming_inventory.py', '--output', str(output)).returncode == 0
    result = json.loads(output.read_text(encoding='utf-8'))
    assert result['counts'] == {'vendor':1,'regulatory':0,'excluded':2}
    vendor = next(r for r in result['files'] if r['role']=='vendor')
    assert vendor['publication_date_observed'] == '2023-04-14'
    assert result['approval_status'] == 'none-implied'
