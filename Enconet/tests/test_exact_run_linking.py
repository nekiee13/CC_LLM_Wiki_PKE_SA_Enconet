from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import db_util
import init_db
import link_exact_run


def fixture(tmp_path,quote='Exact text.'):
    db=tmp_path/'link.sqlite'
    init_db.initialize(db)
    with db_util.connect(db) as c:
        db_util.insert(c,'documents',dict(doc_id='DOC-0001',filename='fixture.md',title='Fixture',supplier='Synthetic',language='en',document_side='DOCUMENT',sha256='a'*64))
        db_util.insert(c,'sieve_runs',dict(run_id='RUN-20261007-01',doc_id='DOC-0001',prompt_version='fixture',document_side='DOCUMENT'))
        db_util.insert(c,'crumbs',dict(item_id='CRUMB-DOC-0001-APP_B_V-0001',doc_id='DOC-0001',sieve_run_id='RUN-20261007-01',criterion_id='APP_B_V',document_side='DOCUMENT',statement='Fixture'))
        db_util.insert(c,'crumb_quotes',dict(quote_id='QUOTE-DOC-0001-0001-01',item_id='CRUMB-DOC-0001-APP_B_V-0001',quote_original=quote,quote_language='en',source_locator='Chapter2'))
        for n in (1,2):
            db_util.insert(c,'document_chunks',dict(chunk_id=f'CHUNK-DOC-0001-{n:04d}',doc_id='DOC-0001',heading_path=f'Chapter{n}',chunk_text='Exact text.',char_start=(n-1)*20,char_end=(n-1)*20+11,source_sha256='a'*64))
    return db


def test_locator_selects_exact_occurrence_and_repeat_preserves(tmp_path):
    db=fixture(tmp_path)
    assert link_exact_run.link(db,'RUN-20261007-01')['new_links']==1
    assert link_exact_run.link(db,'RUN-20261007-01',True)['new_links']==1
    with db_util.connect(db) as c:
        before=tuple(c.execute('SELECT * FROM crumb_chunk_links').fetchone())
        assert c.execute('SELECT chunk_id FROM crumb_chunk_links').fetchone()[0]=='CHUNK-DOC-0001-0002'
    assert link_exact_run.link(db,'RUN-20261007-01',True)['new_links']==0
    with db_util.connect(db) as c:
        assert tuple(c.execute('SELECT * FROM crumb_chunk_links').fetchone())==before


def test_normalized_only_quote_refused_without_writes(tmp_path):
    db=fixture(tmp_path,'Exact  text.')
    with pytest.raises(ValueError,match='missing or ambiguous'):
        link_exact_run.link(db,'RUN-20261007-01',True)
    with db_util.connect(db) as c:
        assert c.execute('SELECT count(*) FROM crumb_chunk_links').fetchone()[0]==0
