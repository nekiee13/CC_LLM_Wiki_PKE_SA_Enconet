"""Exercise approved examples on a new DB copy; never import into live audit."""
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3

import db_util
import import_crumbs
import link_crumbs
from project_paths import ROOT, local_path, configure_standard_streams
import sieve_metrics
import sieve_run


def verify(output):
    output=local_path(output)
    if not output.is_relative_to(ROOT/'out') or output.exists():
        raise ValueError('Use a fresh directory under local out/')
    database=local_path(db_util.DEFAULT_DB)
    before=hashlib.sha256(database.read_bytes()).hexdigest()
    candidate=ROOT/'benchmarks/sieving_golden/20261007-v3-nuclear-plan/candidate.json'
    payload=json.loads(candidate.read_text(encoding='utf-8'))
    output.mkdir(parents=True)
    copy_db=output/'calibration-copy.sqlite'
    with closing(sqlite3.connect(database.as_uri()+'?mode=ro',uri=True)) as source, closing(sqlite3.connect(copy_db)) as target:
        if source.execute('SELECT count(*) FROM crumbs').fetchone()[0]:
            raise ValueError('This fresh-cycle diagnostic expects zero live crumbs')
        source.backup(target)
    run_id='RUN-20261007-01'
    sieve_run.create_run(copy_db,run_id=run_id,doc_id='DOC-0001',prompt_version=payload['prompt_version'],
                         document_side='DOCUMENT',authorities=[])
    count=import_crumbs.import_file(copy_db,candidate,run_id=run_id,strict=True)
    linked,unmatched=link_crumbs.link(copy_db,candidates_path=output/'link-candidates.csv')
    if unmatched:
        raise ValueError('Calibration quote failed chapter linking')
    with closing(db_util.connect(copy_db)) as conn:
        exact=conn.execute("SELECT count(*) FROM crumb_chunk_links WHERE link_method='EXACT'").fetchone()[0]
        for item in payload['items']:
            stored=conn.execute('SELECT x.* FROM crumb_context x JOIN crumbs c ON c.item_id=x.item_id WHERE c.statement=?',
                                (item['statement'],)).fetchone()
            if stored['evidence_type']!=item['evidence_type'] or stored['source_revision']!=item['context']['source_revision']:
                raise ValueError('Context did not round-trip')
    sieve_metrics.generate(copy_db,run_id,output/'run-metrics')
    after=hashlib.sha256(database.read_bytes()).hexdigest()
    if before!=after:
        raise ValueError('Live DB changed during diagnostic')
    result=dict(kind='engineering-calibration-of-approved-manual-examples',
                independent_semantic_prompt_execution=False,examples=count,exact_chapter_links=exact,
                all_links=linked,context_roundtrip=True,live_database_unchanged=True,
                live_before_sha256=before,live_after_sha256=after,
                prompt_activated=False,live_crumbs_imported=False,synthetic_copy=str(copy_db))
    with (output/'report.json').open('x',encoding='utf-8') as stream:
        json.dump(result,stream,indent=2)
    return result


def main():
    configure_standard_streams()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(verify(args.output),indent=2))


if __name__=='__main__':
    main()
