"""Two independent synthetic benchmark classes; never vendor audit evidence."""
from pathlib import Path
import argparse
import copy
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import evaluation_engine
import build_dashboard_data
import generate_dashboard
import validate_dashboard

RATINGS = ['fully','substantially','partially','minimally','unmet','undetermined','na']+['fully']*11


def scoring():
    expected = {'fully':100.,'substantially':75.,'partially':50.,'minimally':25.,
                'unmet':0.,'undetermined':0.,'na':None}
    assert {r:evaluation_engine.score_rating(r) for r in expected} == expected
    result = evaluation_engine.metrics([{'rating':r} for r in RATINGS])
    assert result['consolidated_score']==79.4 and result['applicable_count']==17
    assert result['classification']=='substantially'
    return result


def dashboard():
    taxonomy = yaml.safe_load((ROOT/'schemas/app_b_taxonomy.yml').read_text(encoding='utf-8'))['criteria']
    run = 'RUN-20000101-01'
    package = {'schema_version':'1.0','run':{'run_id':run,'supplier':'Synthetic benchmark',
                'deliverable_language':'en','scoring_model_version':evaluation_engine.model()['model_version']},
               'applicability':[],'evaluations':[],'gaps':[],'findings':[],'actions':[],
               'metrics':scoring(),'approvals':[{'object_id':f'G{gate}-{run}','decision':'approved',
                'date':'2000-01-01','reviewer':'synthetic-fixture','notes':'Unit fixture only'} for gate in (2,3,4)]}
    for taxon, rating in zip(taxonomy,RATINGS):
        cid = taxon['criterion_id']
        package['applicability'].append({'criterion_id':cid,'applicable':int(rating!='na'),
            'justification':'Synthetic benchmark exclusion' if rating=='na' else 'Synthetic benchmark scope',
            'scope_source_doc_id':'DOC-0001'})
        package['evaluations'].append({'evaluation_id':f'EVAL-{cid}','criterion_id':cid,
            'criterion_name':taxon['criterion_name'],'classification':rating,
            'score':evaluation_engine.score_rating(rating),'affirmative_summary':'Synthetic rendering case </script>',
            'contrary_summary':'Not a real audit','judge_ruling':'Synthetic test','rationale':'Synthetic test',
            'evidence_ids':[]})
    before = copy.deepcopy(package)
    data = build_dashboard_data.build(package,generated_date='2000-01-01',dash_id='DASH-20000101-0001')
    html = generate_dashboard.render(data)
    assert not validate_dashboard.validate(package,data,html)
    assert package == before and data['weighted_score']==79.4
    assert '\\u003c/script>' in html and 'http://' not in html and 'https://' not in html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scoring',action='store_true')
    parser.add_argument('--dashboard',action='store_true')
    args = parser.parse_args()
    try:
        if args.scoring or not args.dashboard:
            scoring()
            print('benchmark_scoring: PASS - synthetic 1350/17 = 79.4; not audit approval')
        if args.dashboard or not args.scoring:
            dashboard()
            print('benchmark_dashboard: PASS - independent synthetic rendering; not audit approval')
    except Exception as exc:
        print(f'benchmark: FAIL - {exc}',file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
