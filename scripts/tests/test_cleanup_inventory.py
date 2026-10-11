import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess

import pytest

spec = importlib.util.spec_from_file_location('cleanup_inventory', Path(__file__).parents[1] / 'cleanup_inventory.py')
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


def test_mapping_keeps_evidence_and_agent_homes():
    assert inventory.proposed('Atlas/raw/source.md', ['Atlas']) == ('Atlas/raw/source.md', 'retain-evidence-or-runtime')
    assert inventory.proposed('Atlas/.claude/skills/x.md', ['Atlas'])[0] == 'Atlas/.claude/skills/x.md'
    assert inventory.proposed('Atlas/handoffs/CC_old.md', ['Atlas']) == ('Atlas/coordination/handoffs/CC_old.md', 'claude-coordinated-move')
    assert inventory.proposed('Atlas/outputs/mystery.html', ['Atlas'])[0] is None
    assert inventory.proposed('doc/CC_note.md', ['Atlas'])[1] == 'claude-coordinated-move'
    assert inventory.proposed('audit_template/framework/v3/x.py', ['Atlas'])[1] == 'retain-versioned-history'


@pytest.mark.parametrize('name', ['Atlas Engineering', 'Žuti dobavljač'])
def test_capture_is_read_only_and_keeps_sibling(tmp_path, name):
    subprocess.run(['git', 'init', str(tmp_path)], check=True, capture_output=True)
    p = tmp_path / name
    (p / 'raw').mkdir(parents=True)
    (p / 'raw/source.md').write_text('Objective evidence', encoding='utf-8')
    (p / 'db').mkdir()
    db = p / 'db/nqa_audit.sqlite'
    with sqlite3.connect(db) as c:
        c.execute('CREATE TABLE source(id INTEGER PRIMARY KEY, chapter TEXT)')
        c.execute('INSERT INTO source VALUES(1,?)', ('Chapter full text',))
        c.execute("CREATE VIEW active_crumbs AS SELECT 'DOCUMENT' AS document_side FROM source")
    other = tmp_path / 'Other Company'
    other.mkdir()
    (other / 'owner.txt').write_text('unchanged', encoding='utf-8')
    subprocess.run(['git', '-C', str(tmp_path), '-c', 'user.name=Test', '-c', 'user.email=test@example.test', 'commit', '--allow-empty', '-m', 'fixture'], check=True, capture_output=True)
    before = {f: (f.read_bytes(), f.stat().st_mtime_ns) for f in [db, p/'raw/source.md', other/'owner.txt']}
    result = inventory.capture(tmp_path, [name])
    assert result['baselines'][name]['tables']['source']['rows'] == 1
    assert result['baselines'][name]['active_crumbs'] == [('DOCUMENT', 1)]
    assert result['baselines'][name]['sha256_before'] == result['baselines'][name]['sha256_after']
    assert {f: (f.read_bytes(), f.stat().st_mtime_ns) for f in before} == before
    out = tmp_path / 'receipts'
    inventory.write_receipts(tmp_path, out, result)
    assert json.loads((out/'inventory.json').read_text(encoding='utf-8'))['mode'] == 'read-only-proposal'
    with pytest.raises(FileExistsError):
        inventory.write_receipts(tmp_path, out, result)


def test_destination_guard(tmp_path):
    with pytest.raises(ValueError):
        inventory.write_receipts(tmp_path, tmp_path.parent/'escape', {})
    with pytest.raises(ValueError):
        inventory.write_receipts(tmp_path, tmp_path/'raw/receipt', {})
