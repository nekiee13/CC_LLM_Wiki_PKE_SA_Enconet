import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('sweep',ROOT/'Enconet/scripts/full_keyword_sweep.py')
sweep=importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep)


def fixture(root):
    for folder in ['incoming','raw','manifests','out']:
        (root/folder).mkdir()
    data=b'# Document control\nProcedures require review and approval.\n'
    (root/'incoming/source.md').write_bytes(data)
    (root/'raw/source.md').write_bytes(data)
    (root/'incoming/desktop.ini').write_bytes(b'not evidence')
    with (root/'manifests/raw_sources.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['filename','doc_id','side_hint','sha256'])
        writer.writeheader()
        writer.writerow(dict(filename='source.md',doc_id='DOC-0001',side_hint='DOCUMENT',sha256=sweep.digest(data)))
    exclusions=root/'exclusions.json'
    exclusions.write_text(json.dumps(dict(files=[dict(filename='desktop.ini',sha256=sweep.digest(b'not evidence'),reason='OS folder metadata')])))
    return exclusions


def test_explicit_exclusion_and_reproducible_bundle(tmp_path):
    exclusions=fixture(tmp_path)
    rules=ROOT/'Enconet/sieving/prompts/full_keyword_sweep_v1.json'
    with pytest.raises(ValueError,match='unregistered incoming'):
        sweep.build(tmp_path,tmp_path/'out/refused',rules)
    assert not (tmp_path/'out/refused').exists()
    manifest=sweep.build(tmp_path,tmp_path/'out/valid',rules,exclusions)
    assert len(manifest['documents'])==1 and len(manifest['incoming_exclusions'])==1
    assert sweep.verify_bundle(tmp_path/'out/valid')['exact_quotes']
    assert (tmp_path/'incoming/desktop.ini').read_bytes()==b'not evidence'


def test_changed_excluded_file_refused(tmp_path):
    exclusions=fixture(tmp_path)
    (tmp_path/'incoming/desktop.ini').write_bytes(b'changed')
    with pytest.raises(ValueError,match='changed'):
        sweep.load_exclusions(exclusions,tmp_path)


def test_registered_source_cannot_be_hidden(tmp_path):
    fixture(tmp_path)
    rules=sweep.load_rules(ROOT/'Enconet/sieving/prompts/full_keyword_sweep_v1.json')
    with pytest.raises(ValueError,match='registered source cannot be excluded'):
        sweep.prepare(tmp_path,rules,{'source.md':{}})
