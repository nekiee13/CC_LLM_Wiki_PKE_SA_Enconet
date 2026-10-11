import importlib.util
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).parents[1]))
spec = importlib.util.spec_from_file_location('compile_cleanup_map', Path(__file__).parents[1]/'compile_cleanup_map.py')
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def row(path, destination=None, disposition='retain-or-review-purpose', owner='shared-or-owner', kind='file'):
    return {'path':path, 'new_path':destination or path, 'disposition':disposition,
            'owner':owner, 'type':kind, 'sha256':'fixture', 'dirty':False}


def test_one_file_one_destination_and_no_directory_moves():
    result=tool.compile_rows([row('Atlas/manifests','Atlas/work/manifests',kind='directory'),
                             row('Atlas/manifests/a.csv','Atlas/work/manifests/a.csv')],['Atlas'],{},set())
    assert len(result['files'])==1
    assert result['files'][0]['destination']=='Atlas/work/manifests/a.csv'


def test_do_not_move_vendor_quality_plans_or_agent_homes():
    rows=[row('Atlas/raw/Quality_PLAN.md'),row('Atlas/incoming/Quality_PLAN.md'),
          row('Atlas/.claude/skills/PLAN.md'),row('Atlas/.agents/skills/PLAN.md')]
    assert tool.compile_rows(rows,['Atlas'],{},set())['files']==[]


def test_unknown_output_is_retained_without_invented_run():
    result=tool.compile_rows([row('Atlas/out/2026-01-01/old.html')],['Atlas'],{},set())
    entry=result['files'][0]
    assert entry['destination']=='Atlas/outputs/archive/legacy-out/2026-01-01/old.html'
    assert entry['basis']=='retained history; no proved run identity'
    assert 'RUN-' not in entry['destination']


def test_root_and_nested_plans_get_plan_home():
    result=tool.compile_rows([row('Atlas/MASTER_DEVELOPMENT_PLAN.md'),
                             row('doc/framework-reuse/V3_VENDOR_UPGRADE_PLAN.md')],['Atlas'],{},set())
    assert [r['destination'] for r in result['files']]==[
        'Atlas/docs/plans/MASTER_DEVELOPMENT_PLAN.md',
        'PKE_SA_NQA1_doc/plans/framework-reuse/V3_VENDOR_UPGRADE_PLAN.md']


def test_dirty_claude_and_redirect_holds_are_explicit():
    rows=[row('doc/CC_note.md','PKE_SA_NQA1_doc/CC_note.md',owner='claude-code'),
          row('Atlas/derived/a.md','Atlas/work/derived/a.md',disposition='hold-existing-dirty-content'),
          row('Atlas/out/redirect',disposition='hold-redirect-or-hardlink',kind='redirect')]
    result=tool.compile_rows(rows,['Atlas'],{},set())
    assert result['files'][0]['hold']=='Claude-owned move'
    assert result['files'][1]['hold']=='hold-existing-dirty-content'
    assert result['special_holds'][0]['source']=='Atlas/out/redirect'


def test_casefold_collisions_block_both_entries():
    rows=[row('Atlas/out/a.html'),row('Atlas/out/A.html')]
    result=tool.compile_rows(rows,['Atlas'],{},set())
    assert len(result['collisions'])==1
    assert all(r['hold']=='destination collision' for r in result['files'])


@pytest.mark.parametrize('name',['Atlas Engineering','Žuti dobavljač'])
def test_names_are_data_and_only_proved_runs_are_used(name):
    source=name+'/out/RUN-20260101-01/report.md'
    result=tool.compile_rows([row(source)],[name],{}, {(name,'RUN-20260101-01')})
    assert result['files'][0]['destination']==name+'/outputs/RUN-20260101-01/revisions/legacy-out/report.md'
    unknown=tool.compile_rows([row(source)],[name],{},set())
    assert '/outputs/archive/' in unknown['files'][0]['destination']


def test_preferred_artifact_requires_snapshot_manifest_and_live_hash(tmp_path):
    p=tmp_path/'Atlas'
    p.mkdir()
    source=p/'light.html'
    source.write_text('self contained',encoding='utf-8')
    sha=tool.digest(source)
    manifest=p/'manifest.json'
    manifest.write_text(json.dumps({'run_id':'RUN-20260101-01','artifacts':[
        {'destination':'light.html','sha256':sha}]}),encoding='utf-8')
    config={'Atlas':{'manifest':'Atlas/manifest.json','artifacts':{'Atlas/light.html':'dashboard_light.html'}}}
    before={f:f.read_bytes() for f in [source,manifest]}
    result=tool.load_preferred(tmp_path,config,{('Atlas','RUN-20260101-01')},[{'path':'Atlas/light.html','sha256':sha}])
    assert result['Atlas/light.html']['destination']=='Atlas/outputs/RUN-20260101-01/dashboard_light.html'
    assert all(f.read_bytes()==data for f,data in before.items())
    with pytest.raises(ValueError,match='exact manifest'):
        tool.load_preferred(tmp_path,config,{('Atlas','RUN-20260101-01')},[{'path':'Atlas/light.html','sha256':'wrong'}])


def test_relative_paths_reject_escape_and_windows_drive():
    for path in ['../escape','Atlas/../escape','C:/escape','Atlas\\escape','/escape']:
        with pytest.raises(ValueError):
            tool.relative(path)


def test_two_saved_versions_are_not_collapsed_into_one_destination():
    rows=[row('Atlas/out/2026-01-01/Q01-RUN-20260101-01/metrics.json'),
          row('Atlas/out/2026-01-02/Q02-RUN-20260101-01/metrics.json')]
    result=tool.compile_rows(rows,['Atlas'],{}, {('Atlas','RUN-20260101-01')})
    assert not result['collisions']
    assert len({r['destination'] for r in result['files']})==2


def test_proved_working_receipt_uses_work_not_outputs():
    result=tool.compile_rows([row('Atlas/out/2026-01-01/tests.xml')],['Atlas'],{},set(),
                             {'Atlas/out/2026-01-01/tests.xml':'verified JUnit test receipt'})
    assert result['files'][0]['destination']=='Atlas/work/validation/legacy-out/2026-01-01/tests.xml'


def test_plan_review_is_a_review_not_a_plan():
    result=tool.compile_rows([row('Atlas/docs/reviews/PLAN_CHECKS.md','Atlas/work/reviews/PLAN_CHECKS.md')],['Atlas'],{},set())
    assert result['files'][0]['destination']=='Atlas/work/reviews/PLAN_CHECKS.md'
