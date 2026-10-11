import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0,str(Path(__file__).parents[1]))
spec=importlib.util.spec_from_file_location('cleanup_migration',Path(__file__).parents[1]/'cleanup_migration.py')
tool=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def authorize(root,plan):
    # Synthetic authority exists only in disposable tests, never production records.
    return {'schema':'cleanup-authorization-1','root':str(root.resolve()),
            'plan_sha256':tool.plan_hash(plan),'owner_decision':'FIXTURE-OWNER',
            'review_decision':'FIXTURE-REVIEW','allow_apply':True}


def fixture(tmp_path):
    source=tmp_path/'Supplier/manifests/a.csv'
    source.parent.mkdir(parents=True)
    source.write_bytes(b'owner-record\r\n')
    row={'source':'Supplier/manifests/a.csv','destination':'Supplier/work/manifests/a.csv',
         'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'owner':'shared-or-owner',
         'hold':None,'approval':'pending'}
    return source,{'schema':'cleanup-file-map-1','files':[row],'collisions':[]}


def test_preview_is_read_only(tmp_path):
    source,plan=fixture(tmp_path)
    before=(source.read_bytes(),source.stat().st_mtime_ns)
    result=tool.preview(tmp_path,plan)
    assert result['eligible']==1
    assert (source.read_bytes(),source.stat().st_mtime_ns)==before
    assert not (tmp_path/'Supplier/work').exists()


def test_apply_retry_verify_undo(tmp_path):
    source,plan=fixture(tmp_path)
    journal=tmp_path/'journal.jsonl'
    approval=authorize(tmp_path,plan)
    tool.apply(tmp_path,plan,journal,approval)
    target=tmp_path/plan['files'][0]['destination']
    assert not source.exists() and target.read_bytes()==b'owner-record\r\n'
    tool.apply(tmp_path,plan,journal,approval)
    assert tool.verify(tmp_path,plan,journal)['moved']==1
    tool.undo(tmp_path,plan,journal)
    assert source.read_bytes()==b'owner-record\r\n' and not target.exists()


def test_pending_or_unbound_authority_is_refused(tmp_path):
    source,plan=fixture(tmp_path)
    with pytest.raises(ValueError,match='authorization'):
        tool.apply(tmp_path,plan,tmp_path/'journal.jsonl',{})
    approval=authorize(tmp_path,plan)
    plan['files'][0]['destination']='Supplier/work/changed.csv'
    with pytest.raises(ValueError,match='authorization'):
        tool.apply(tmp_path,plan,tmp_path/'journal.jsonl',approval)
    assert source.exists()


@pytest.mark.parametrize('change',['collision','changed-source','claude','held','escape','raw'])
def test_refuse_unsafe_rows_before_writes(tmp_path,change):
    source,plan=fixture(tmp_path)
    row=plan['files'][0]
    if change=='collision':
        target=tmp_path/row['destination']; target.parent.mkdir(parents=True); target.write_bytes(b'owner-file')
    elif change=='changed-source': source.write_bytes(b'changed')
    elif change=='claude': row['owner']='claude-code'
    elif change=='held': row['hold']='dirty'
    elif change=='escape': row['destination']='../escape.csv'
    elif change=='raw': row['source']='Supplier/raw/a.csv'
    result=tool.preview(tmp_path,plan)
    assert result['blocked']>=1
    approval=authorize(tmp_path,plan)
    with pytest.raises(ValueError): tool.apply(tmp_path,plan,tmp_path/'journal.jsonl',approval)
    assert source.exists() and not (tmp_path/'journal.jsonl').exists()


def test_interruption_after_move_can_resume(tmp_path,monkeypatch):
    source,plan=fixture(tmp_path)
    journal=tmp_path/'journal.jsonl'
    approval=authorize(tmp_path,plan)
    real=tool.move_no_replace
    def interrupted(src,dst):
        real(src,dst)
        raise OSError('injected interruption after move')
    monkeypatch.setattr(tool,'move_no_replace',interrupted)
    with pytest.raises(OSError): tool.apply(tmp_path,plan,journal,approval)
    assert not tool.verify(tmp_path,plan,journal)['complete']
    monkeypatch.setattr(tool,'move_no_replace',real)
    tool.apply(tmp_path,plan,journal,approval)
    assert tool.verify(tmp_path,plan,journal)['moved']==1


def test_undo_refuses_changed_destination(tmp_path):
    source,plan=fixture(tmp_path)
    journal=tmp_path/'journal.jsonl'
    approval=authorize(tmp_path,plan)
    tool.apply(tmp_path,plan,journal,approval)
    target=tmp_path/plan['files'][0]['destination'];target.write_bytes(b'owner changed this')
    with pytest.raises(ValueError): tool.undo(tmp_path,plan,journal)
    assert target.read_bytes()==b'owner changed this'


def test_parent_file_collision_blocks_preview(tmp_path):
    source,plan=fixture(tmp_path)
    (tmp_path/'Supplier/work').write_bytes(b'owner-file')
    assert tool.preview(tmp_path,plan)['blocked']==1


def test_empty_plan_cannot_create_a_fake_success_journal(tmp_path):
    plan={'schema':'cleanup-file-map-1','files':[],'collisions':[]}
    with pytest.raises(ValueError):
        tool.apply(tmp_path,plan,tmp_path/'journal.jsonl',authorize(tmp_path,plan))
    assert not (tmp_path/'journal.jsonl').exists()


def test_file_attributes_and_readonly_bytes_survive_round_trip(tmp_path):
    import stat
    source,plan=fixture(tmp_path)
    original=source.stat().st_mode
    source.chmod(stat.S_IREAD)
    before=tool.identity(source)
    journal=tmp_path/'journal.jsonl'
    try:
        tool.apply(tmp_path,plan,journal,authorize(tmp_path,plan))
        target=tmp_path/plan['files'][0]['destination']
        assert tool.identity(target)==before
        tool.undo(tmp_path,plan,journal)
        assert tool.identity(source)==before
    finally:
        for path in [source,tmp_path/plan['files'][0]['destination']]:
            if path.exists():path.chmod(original)


def test_user_file_added_under_new_directory_is_not_deleted(tmp_path):
    source,plan=fixture(tmp_path)
    journal=tmp_path/'journal.jsonl'
    tool.apply(tmp_path,plan,journal,authorize(tmp_path,plan))
    owner=tmp_path/'Supplier/work/owner.txt';owner.write_bytes(b'owner')
    result=tool.undo(tmp_path,plan,journal)
    assert source.exists() and owner.read_bytes()==b'owner'
    assert 'Supplier/work' in result['retained_directories']


def test_torn_last_journal_write_can_resume_without_rewriting_history(tmp_path):
    source,plan=fixture(tmp_path)
    journal=tmp_path/'journal.jsonl'
    approval=authorize(tmp_path,plan)
    tool.apply(tmp_path,plan,journal,approval)
    with journal.open('ab') as stream: stream.write(b'{"kind":"moved","incomplete":')
    before=journal.read_bytes()
    verification=tool.verify(tmp_path,plan,journal)
    assert verification['journal_tail_incomplete'] and not verification['complete']
    assert journal.read_bytes()==before
    tool.apply(tmp_path,plan,journal,approval)
    assert journal.read_bytes().startswith(before)
    assert tool.verify(tmp_path,plan,journal)['moved']==1


def test_changed_journal_header_is_refused(tmp_path):
    source,plan=fixture(tmp_path)
    journal=tmp_path/'journal.jsonl'
    tool.apply(tmp_path,plan,journal,authorize(tmp_path,plan))
    lines=journal.read_text(encoding='utf-8').splitlines()
    first=json.loads(lines[0]);first['new_directories'].append('owner-empty-dir')
    lines[0]=json.dumps(first)
    journal.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    with pytest.raises(ValueError):tool.undo(tmp_path,plan,journal)


def test_mid_batch_failure_restores_only_moved_files(tmp_path,monkeypatch):
    source,plan=fixture(tmp_path)
    second=source.parent/'b.csv';second.write_bytes(b'second')
    plan['files'].append({**plan['files'][0],'source':'Supplier/manifests/b.csv',
                         'destination':'Supplier/work/manifests/b.csv','sha256':tool.digest(second)})
    journal=tmp_path/'journal.jsonl'
    real=tool.move_no_replace
    def fail_second(src,dst):
        if src==second:raise PermissionError('injected access failure')
        real(src,dst)
    monkeypatch.setattr(tool,'move_no_replace',fail_second)
    with pytest.raises(PermissionError):tool.apply(tmp_path,plan,journal,authorize(tmp_path,plan))
    monkeypatch.setattr(tool,'move_no_replace',real)
    assert tool.verify(tmp_path,plan,journal)['moved']==1
    tool.undo(tmp_path,plan,journal)
    assert source.read_bytes()==b'owner-record\r\n' and second.read_bytes()==b'second'


def test_hardlinked_source_is_blocked(tmp_path):
    import os
    source,plan=fixture(tmp_path)
    os.link(source,source.parent/'linked.csv')
    assert tool.preview(tmp_path,plan)['blocked']==1


def test_reparse_parent_is_blocked_in_guard(tmp_path,monkeypatch):
    from types import SimpleNamespace
    import stat
    source,plan=fixture(tmp_path)
    real=Path.lstat
    def mocked(path,*args,**kwargs):
        if path==source.parent:
            return SimpleNamespace(st_mode=stat.S_IFDIR,st_file_attributes=0x400,st_nlink=1)
        return real(path,*args,**kwargs)
    monkeypatch.setattr(Path,'lstat',mocked)
    assert tool.preview(tmp_path,plan)['blocked']==1


def test_cli_preview_apply_verify_undo_in_fixture_only(tmp_path):
    source,plan=fixture(tmp_path)
    plan_file=tmp_path/'plan.json';plan_file.write_text(json.dumps(plan),encoding='utf-8')
    auth_file=tmp_path/'authority.json';auth_file.write_text(json.dumps(authorize(tmp_path,plan)),encoding='utf-8')
    journal=tmp_path/'journal.jsonl'
    base=[sys.executable,str(Path(tool.__file__)),'--root',str(tmp_path),'--plan',str(plan_file)]
    for mode in ['preview','apply','verify','apply','undo']:
        command=base+['--mode',mode]
        if mode!='preview':command+=['--journal',str(journal)]
        if mode=='apply':command+=['--authorization',str(auth_file)]
        result=subprocess.run(command,cwd=tmp_path,capture_output=True,text=True)
        assert result.returncode==0,result.stderr
        json.loads(result.stdout)
    assert source.read_bytes()==b'owner-record\r\n'


@pytest.mark.parametrize('alias',['Supplier/RAW/a.csv','Supplier/raw./a.csv','Supplier/.CLAUDE/x.md','Supplier/cc_record.md'])
def test_case_and_windows_aliases_do_not_bypass_protection(tmp_path,alias):
    source,plan=fixture(tmp_path)
    plan['files'][0]['source']=alias
    assert tool.preview(tmp_path,plan)['blocked']==1


def test_foreign_root_authorization_is_refused_before_journal(tmp_path):
    source,plan=fixture(tmp_path)
    approval=authorize(tmp_path,plan)
    approval['root']=str(tmp_path/'Another Root')
    with pytest.raises(ValueError,match='authorization'):
        tool.apply(tmp_path,plan,tmp_path/'journal.jsonl',approval)
    assert source.exists() and not (tmp_path/'journal.jsonl').exists()


def test_missing_source_is_blocked_before_journal(tmp_path):
    source,plan=fixture(tmp_path)
    source.unlink()
    assert tool.preview(tmp_path,plan)['blocked']==1
    with pytest.raises(ValueError):
        tool.apply(tmp_path,plan,tmp_path/'journal.jsonl',authorize(tmp_path,plan))
    assert not (tmp_path/'journal.jsonl').exists()
