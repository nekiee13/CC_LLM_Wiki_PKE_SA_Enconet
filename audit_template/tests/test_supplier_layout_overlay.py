import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

TEMPLATE = Path(__file__).parents[1]
sys.path.insert(0, str(TEMPLATE))
from prepare_supplier_layout_overlay import build, local_literals, review_compatibility


@pytest.mark.parametrize('name', ['Atlas Engineering', 'Žuti dobavljač'])
def test_overlay_preserves_current_audit_logic_and_siblings(tmp_path, name):
    source = tmp_path / name / 'scripts'
    source.mkdir(parents=True)
    current = 'from project_paths import ROOT\nSCORE = 77.8\nPATH = ROOT / "manifests" / "approvals.csv"\n'
    (source / 'evaluation.py').write_text(current, encoding='utf-8')
    sibling = tmp_path / 'Other Supplier'
    sibling.mkdir()
    (sibling / 'owner.md').write_bytes(b'unchanged')
    result = build(name, tmp_path / '.tmp/overlay', workspace=tmp_path)
    assert result['changed_scripts'] == 1
    changed = (tmp_path / '.tmp/overlay/scripts/evaluation.py').read_text(encoding='utf-8')
    assert 'SCORE = 77.8' in changed and "layout_path('manifests')" in changed
    assert (source / 'evaluation.py').read_text(encoding='utf-8') == current
    assert (sibling / 'owner.md').read_bytes() == b'unchanged'
    assert not (tmp_path / '.tmp/overlay/db').exists()
    assert result['status'] == 'development-overlay-not-installable'


def test_path_arguments_route_without_changing_evidence_strings():
    source = '''quote="manifests/approvals.csv"
bind("manifests/approvals.csv")
local(root,"derived/DOC-0001.txt")
parser.add_argument("--output",default=Path("benchmarks/golden.yml"))
'''
    text, count = local_literals(source)
    assert count == 3
    assert 'quote="manifests/approvals.csv"' in text
    assert "'work/manifests/approvals.csv'" in text
    assert "'work/derived/DOC-0001.txt'" in text
    assert "'work/benchmarks/golden.yml'" in text


@pytest.mark.parametrize('root_name', ['PROJECT', 'ANOTHER_LOCAL_ROOT'])
def test_review_default_bridge_is_root_identifier_neutral(root_name):
    source = ('from pathlib import Path\nimport argparse\n'
              f'{root_name} = Path(__file__).resolve().parents[1]\n'
              f'OUTPUT = {root_name} / "outputs" / "candidates" / "evidence_access" / "review_catalog.json"\n')
    converted, policy = review_compatibility(source, 'generate_review_catalog.py')
    assert not policy and "layout_path('reviews', 'review_catalog.json')" in converted
    assert "configuration() == 'v4'" in converted
    assert source in converted or f'{root_name} = Path(__file__).resolve().parents[1]' in converted
    assert review_compatibility(converted, 'generate_review_catalog.py') == (converted, False)


def test_supplier_parent_alias_is_refused(tmp_path):
    with pytest.raises(ValueError):
        build('..', tmp_path / '.tmp/candidate', workspace=tmp_path)


def test_relocated_benchmark_runner_keeps_local_sources(tmp_path):
    supplier = tmp_path / 'Atlas Engineering'
    (supplier / 'scripts').mkdir(parents=True)
    (supplier / 'benchmarks').mkdir()
    original = ('from pathlib import Path\n'
                'ENCONET = Path(__file__).resolve().parents[1]\n'
                'ROOT = Path(__file__).resolve().parent\n')
    source = supplier / 'benchmarks/validate_benchmarks.py'
    source.write_text(original, encoding='utf-8')
    target = tmp_path / '.tmp/overlay'
    build('Atlas Engineering', target, workspace=tmp_path)
    converted = (target / 'scripts/validate_benchmarks.py').read_text(encoding='utf-8')
    assert 'ROOT = layout_path("benchmarks")' in converted
    assert source.read_text(encoding='utf-8') == original
    manifest = json.loads((target / 'candidate-manifest.json').read_text(encoding='utf-8'))
    assert 'scripts/validate_benchmarks.py' in manifest['install_paths']
