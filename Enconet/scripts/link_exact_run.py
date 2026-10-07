"""Preview/apply exact chapter links for one run; preserve existing links."""
import argparse
from contextlib import closing
import json

import db_util
from project_paths import local_path, configure_standard_streams


def link(db,run_id,apply=False):
    with closing(db_util.connect(db)) as conn, conn:
        rows=conn.execute('SELECT q.*,c.doc_id FROM crumb_quotes q JOIN crumbs c ON c.item_id=q.item_id WHERE c.sieve_run_id=?',(run_id,)).fetchall()
        if not rows:
            raise ValueError('Run has no quotes to link')
        planned=[]
        for q in rows:
            matches=conn.execute('SELECT * FROM document_chunks WHERE doc_id=?',(q['doc_id'],)).fetchall()
            exact=[c for c in matches if q['quote_original'] in c['chunk_text']]
            located=[c for c in exact if c['heading_path']==q['source_locator']]
            selected=located or exact
            if len(selected)!=1:
                raise ValueError('Exact quote has missing or ambiguous chapter: '+q['quote_id'])
            target=selected[0]
            existing=conn.execute('SELECT * FROM crumb_chunk_links WHERE quote_id=?',(q['quote_id'],)).fetchall()
            if existing and (len(existing)!=1 or existing[0]['chunk_id']!=target['chunk_id'] or existing[0]['link_method']!='EXACT'):
                raise ValueError('Existing link differs; no in-place repair: '+q['quote_id'])
            if not existing:
                planned.append(dict(item_id=q['item_id'],quote_id=q['quote_id'],chunk_id=target['chunk_id'],link_method='EXACT',confidence=1.0))
        if apply:
            for item in planned:
                db_util.insert(conn,'crumb_chunk_links',item)
        return dict(mode='apply' if apply else 'preview',run_id=run_id,quotes=len(rows),new_links=len(planned),
                    existing_links_preserved=len(rows)-len(planned),all_exact=True)


def main():
    configure_standard_streams()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',default=db_util.DEFAULT_DB)
    parser.add_argument('--run-id',required=True)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    try:
        print(json.dumps(link(local_path(args.db),args.run_id,args.apply)))
    except (ValueError,OSError) as exc:
        parser.exit(1,str(exc)+'\n')


if __name__=='__main__':
    main()
