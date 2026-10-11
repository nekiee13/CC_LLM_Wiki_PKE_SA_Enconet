import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

SOURCE=Path(__file__).parents[1]/'runtime_v4/project_layout.py'


@pytest.mark.parametrize('name',['Atlas Engineering','Žuti dobavljač'])
@pytest.mark.parametrize('sibling',[False,True])
def test_local_copy_works_from_foreign_cwd_and_keeps_sibling(tmp_path,name,sibling):
    project=tmp_path/name
    (project/'scripts').mkdir(parents=True)
    shutil.copy2(SOURCE,project/'scripts/project_layout.py')
    (project/'project-layout.json').write_text(json.dumps({'schema_version':1,'layout':'v4'}),encoding='utf-8')
    other=tmp_path/'Other Supplier'
    if sibling:
        other.mkdir()
        (other/'owner.txt').write_text('unchanged',encoding='utf-8')
    before=(other/'owner.txt').read_bytes() if sibling else None
    result=subprocess.run([sys.executable,str(project/'scripts/project_layout.py'),'--describe'],cwd=tmp_path,capture_output=True,text=True,encoding='utf-8')
    assert result.returncode==0,result.stderr
    data=json.loads(result.stdout)
    assert Path(data['manifests'])==project/'work/manifests'
    assert Path(data['handoffs'])==project/'coordination/handoffs'
    assert not (project/'work').exists()
    assert (other/'owner.txt').read_bytes()==before if sibling else not other.exists()


def load(project):
    (project/'scripts').mkdir(parents=True)
    shutil.copy2(SOURCE,project/'scripts/project_layout.py')
    spec=importlib.util.spec_from_file_location('fixture_layout',project/'scripts/project_layout.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_explicit_legacy_mode_and_mixed_layout_refusal(tmp_path):
    m=load(tmp_path/'Supplier')
    with pytest.raises(ValueError,match='configuration'):
        m.describe()
    (m.ROOT/'project-layout.json').write_text(json.dumps({'schema_version':1,'layout':'legacy'}),encoding='utf-8')
    assert m.path('manifests')==m.ROOT/'manifests'
    (m.ROOT/'manifests').mkdir()
    (m.ROOT/'work/manifests').mkdir(parents=True)
    with pytest.raises(ValueError,match='mixed'):
        m.path('manifests')


def test_scope_and_run_guard(tmp_path):
    m=load(tmp_path/'Supplier')
    (m.ROOT/'project-layout.json').write_text(json.dumps({'schema_version':1,'layout':'v4'}),encoding='utf-8')
    assert m.run_output('RUN-20260101-01')==m.ROOT/'outputs/RUN-20260101-01'
    for value in ['../escape','/outside','C:/outside','RUN-x/escape']:
        with pytest.raises(ValueError):
            m.run_output(value)
    with pytest.raises(ValueError):
        m.path('manifests','../escape')
    with pytest.raises(ValueError):
        m.path('unknown')


def test_v4_docs_and_plan_subfolder_are_not_a_mixed_layout(tmp_path):
    m=load(tmp_path/'Supplier')
    (m.ROOT/'project-layout.json').write_text(json.dumps({'schema_version':1,'layout':'v4'}),encoding='utf-8')
    (m.ROOT/'docs/plans').mkdir(parents=True)
    (m.ROOT/'docs/guide.md').write_text('guide',encoding='utf-8')
    assert m.path('plans')==m.ROOT/'docs/plans'
