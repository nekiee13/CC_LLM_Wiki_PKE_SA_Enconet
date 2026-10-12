import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

TEMPLATE = Path(__file__).parents[1]
sys.path.insert(0, str(TEMPLATE))
from prepare_supplier_layout_overlay import build


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
