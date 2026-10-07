import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

TEMPLATE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TEMPLATE))
import framework_release
from prepare_vendor import scaffold
from run_source_batches import run


def fixture(tmp_path):
    root=tmp_path/'New Company'
    root.mkdir()
    framework_release.apply(root,'test-install',framework_release.spec())
    for name,data in scaffold('New Company').items():
        (root/name).parent.mkdir(parents=True,exist_ok=True)
        (root/name).write_bytes(data)
    workspace=TEMPLATE.parent
    shutil.copyfile(workspace/'Enconet/scripts/promote_source.py',root/'scripts/promote_source.py')
    shutil.copyfile(TEMPLATE/'runtime_v2/promote_source.py',root/'scripts/copy_incoming_source.py')
    result=subprocess.run([sys.executable,str(root/'scripts/init_db.py')],capture_output=True)
    assert result.returncode==0
    docs=[]
    for name in ['one.md','Priručnik.md']:
        data=('# '+name+'\nQuality control.\n').encode()
        (root/'incoming'/name).write_bytes(data)
        docs.append(dict(filename=name,sha256=hashlib.sha256(data).hexdigest(),title=name,
                         supplier='new-company',doc_date='n-a',language='en',side='DOCUMENT'))
    plan=tmp_path/'plan.json'
    plan.write_text(json.dumps(dict(project=str(root),batches=[dict(batch_id='SRC-20261007-001',size_class='small',documents=docs)])))
    return root,plan,root/'out/receipt.jsonl'


def test_preview_then_two_source_batch(tmp_path):
    root,plan,receipt=fixture(tmp_path)
    assert run(root,plan,receipt)['writes']==0
    assert not receipt.exists() and not (root/'raw/one.md').exists()
    result=run(root,plan,receipt,True)
    assert result['documents']==2
    assert all((root/'incoming'/n).read_bytes()==(root/'raw'/n).read_bytes() for n in ['one.md','Priručnik.md'])
    rows=[json.loads(x) for x in receipt.read_text(encoding='utf-8').splitlines()]
    assert len(rows)==3 and all(r['exit_code']==0 for r in rows)


def test_changed_source_blocks_entire_batch(tmp_path):
    root,plan,receipt=fixture(tmp_path)
    (root/'incoming/Priručnik.md').write_text('changed source')
    with pytest.raises(ValueError,match='Source changed'):
        run(root,plan,receipt,True)
    assert not (root/'raw/one.md').exists() and not receipt.exists()
