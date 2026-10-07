"""Lossless optional v3 metadata, transaction rollback and additive migration."""
import copy
import json
from pathlib import Path
import sqlite3
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import db_util
import import_crumbs
import init_db
import migrate_db
import sieve_run

GOLDEN=ROOT/'benchmarks/sieving_golden/20261007-v3-nuclear-plan/candidate.json'


def setup(tmp_path):
    db=tmp_path/'context.sqlite'
    init_db.initialize(db)
    with db_util.connect(db) as conn:
        db_util.insert(conn,'documents',dict(doc_id='DOC-0001',filename='fixture.md',title='Fixture',
                       supplier='Synthetic company',language='hr',document_side='DOCUMENT',sha256='a'*64))
    sieve_run.create_run(db,run_id='RUN-20261007-01',doc_id='DOC-0001',prompt_version='appb_document_v3_context_anchors',
                         document_side='DOCUMENT',authorities=[])
    return db


def test_twenty_examples_roundtrip(tmp_path):
    db=setup(tmp_path)
    assert import_crumbs.import_file(db,GOLDEN,run_id='RUN-20261007-01',strict=True)==20
    original=json.loads(GOLDEN.read_text(encoding='utf-8'))
    with db_util.connect(db) as conn:
        for item in original['items']:
            row=conn.execute('SELECT x.* FROM crumb_context x JOIN crumbs c ON c.item_id=x.item_id WHERE c.statement=?',
                             (item['statement'],)).fetchone()
            assert row['evidence_type']==item['evidence_type']
            assert row['source_revision']==item['context']['source_revision']
            assert row['project_ref'] is None
        assert conn.execute('SELECT count(*) FROM crumb_context').fetchone()[0]==20
    with pytest.raises(ValueError,match='immutable'):
        import_crumbs.import_file(db,GOLDEN,run_id='RUN-20261007-01',strict=True)


def test_invalid_optional_metadata_rejected_without_writes(tmp_path):
    db=setup(tmp_path)
    payload=json.loads(GOLDEN.read_text(encoding='utf-8'))
    payload['items'][0]['context']['unknown_field']='must not disappear'
    source=tmp_path/'invalid.json'
    source.write_text(json.dumps(payload),encoding='utf-8')
    with pytest.raises(ValueError,match='context'):
        import_crumbs.import_file(db,source,run_id='RUN-20261007-01',strict=True)
    with db_util.connect(db) as conn:
        assert conn.execute('SELECT count(*) FROM crumbs').fetchone()[0]==0


@pytest.mark.parametrize('field,value', [('source_revision',8),('evidence_date','2023-99-12'),('evidence_type','invented-kind')])
def test_invalid_optional_types_and_dates(tmp_path,field,value):
    db=setup(tmp_path)
    payload=json.loads(GOLDEN.read_text(encoding='utf-8'))
    if field=='evidence_type':
        payload['items'][0][field]=value
    else:
        payload['items'][0]['context'][field]=value
    source=tmp_path/'invalid-type.json'
    source.write_text(json.dumps(payload),encoding='utf-8')
    with pytest.raises(ValueError,match='validation failed'):
        import_crumbs.import_file(db,source,run_id='RUN-20261007-01',strict=True)
    with db_util.connect(db) as conn:
        assert conn.execute('SELECT count(*) FROM crumbs').fetchone()[0]==0


def test_context_rolls_back_with_core_failure(tmp_path):
    db=setup(tmp_path)
    payload=json.loads(GOLDEN.read_text(encoding='utf-8'))
    payload['items'][1]['sources'].append(copy.deepcopy(payload['items'][1]['sources'][0]))
    source=tmp_path/'bad-source.json'
    source.write_text(json.dumps(payload),encoding='utf-8')
    with pytest.raises(ValueError):
        import_crumbs.import_file(db,source,run_id='RUN-20261007-01',strict=True)
    with db_util.connect(db) as conn:
        assert conn.execute('SELECT count(*) FROM crumbs').fetchone()[0]==0
        assert conn.execute('SELECT count(*) FROM crumb_context').fetchone()[0]==0
        assert conn.execute('SELECT completed_at FROM sieve_runs').fetchone()[0] is None


def test_missing_optional_anchors_stay_missing(tmp_path):
    db=setup(tmp_path)
    payload=json.loads(GOLDEN.read_text(encoding='utf-8'))
    payload['items']=payload['items'][:1]
    payload['items'][0].pop('context')
    source=tmp_path/'unanchored.json'
    source.write_text(json.dumps(payload),encoding='utf-8')
    assert import_crumbs.import_file(db,source,run_id='RUN-20261007-01',strict=True)==1
    with db_util.connect(db) as conn:
        row=conn.execute('SELECT * FROM crumb_context').fetchone()
        assert row['evidence_type']=='policy_or_procedure' and row['source_revision'] is None


def test_context_migration_preview_backup_idempotence(tmp_path):
    db=setup(tmp_path)
    with sqlite3.connect(db) as conn:
        conn.execute('DROP TABLE IF EXISTS crumb_context')
    before=db.read_bytes()
    assert migrate_db.migrate(db,apply=False)==(['create crumb_context'],None)
    assert db.read_bytes()==before
    actions,backup=migrate_db.migrate(db,apply=True,backup_dir=tmp_path/'backups')
    assert actions==['create crumb_context'] and backup.is_file()
    assert migrate_db.migrate(db,apply=True)==([],None)
    with sqlite3.connect(db) as conn:
        assert conn.execute('SELECT count(*) FROM documents').fetchone()[0]==1
        assert conn.execute('SELECT count(*) FROM crumb_context').fetchone()[0]==0
