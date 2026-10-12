"""Development candidates only: no real source, decision, or supplier mutation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

SOURCE = Path(__file__).parents[1] / 'prepare_framework_candidate_v4.py'


def builder():
    spec = importlib.util.spec_from_file_location('candidate_builder', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_expression_routing_preserves_literals_and_unrelated_roots():
    source = 'ROOT = Path(__file__).resolve().parents[1]\na = ROOT / "manifests/approvals.csv"\nb = ROOT / "derived" / doc\nc = foreign / "derived"\nquote = "manifests/approvals.csv"\n'
    converted, count = builder().route_python(source)
    assert count == 2
    assert "layout_path('manifests') / 'approvals.csv'" in converted
    assert "layout_path('derived') / doc" in converted
    assert 'foreign / "derived"' in converted
    assert 'quote = "manifests/approvals.csv"' in converted


def test_unicode_offsets_comments_and_shadowed_root():
    source = '"""Žuti evidence."""\nfrom __future__ import annotations\nROOT = Path(__file__).resolve().parents[1]\n# Keep this comment\na = "č"; b = ROOT / "manifests"\ndef foreign(ROOT):\n    return ROOT / "derived"\n'
    converted, count = builder().route_python(source)
    assert count == 1
    assert '# Keep this comment' in converted
    assert 'a = "č"; b = layout_path' in converted
    assert 'return ROOT / "derived"' in converted


def test_verified_local_import_aliases_preserve_foreign_and_shadowed_roots():
    source = ('from source_registry import ENCONET as supplier_root\n'
              'from regression_fixture import ROOT\n'
              'from unrelated import ROOT as other\n'
              'a = supplier_root / "derived"\n'
              'b = ROOT / "out"\n'
              'c = other / "derived"\n'
              'def foreign(supplier_root):\n'
              '    return supplier_root / "derived"\n')
    converted, count = builder().route_python(source)
    assert count == 2
    assert "a = layout_path('derived')" in converted
    assert "b = layout_path('validation')" in converted
    assert 'c = other / "derived"' in converted
    assert 'return supplier_root / "derived"' in converted


def test_candidate_requires_fresh_destination_and_verified_payload(tmp_path):
    m = builder()
    target = tmp_path / 'candidate'
    manifest = m.build(target)
    assert manifest['status'] == 'development-only-not-installable'
    assert (target / 'work/manifests/raw_sources.csv').is_file()
    assert not (target / 'manifests').exists()
    assert not (target / 'db/nqa_audit.sqlite').exists()
    assert m.build(tmp_path / 'second') == manifest
    for row in manifest['files']:
        assert hashlib.sha256((target / row['path']).read_bytes()).hexdigest() == row['sha256']
    with pytest.raises(FileExistsError):
        m.build(target)
    with pytest.raises(ValueError, match='checksum'):
        m.verify_payload({'files': [{'path': 'scripts/init_db.py', 'sha256': 'bad', 'bytes': 0}]}, m.BASELINE)
    assert not (tmp_path / 'Other Supplier').exists()


@pytest.mark.parametrize('name', ['Atlas Engineering', 'Žuti dobavljač'])
@pytest.mark.parametrize('sibling', [False, True])
def test_candidate_intake_extract_chunk_local_paths(tmp_path, name, sibling):
    target = tmp_path / name
    other = tmp_path / 'Other Supplier'
    if sibling:
        other.mkdir()
        (other / 'owner.txt').write_bytes(b'untouched')
    before = (other / 'owner.txt').stat() if sibling else None
    builder().build(target)

    def cli(script, *args, cwd=None):
        result = subprocess.run([sys.executable, '-B', str(target / 'scripts' / script), *args],
                                cwd=cwd or tmp_path, capture_output=True, text=True, encoding='utf-8')
        assert result.returncode == 0, result.stdout + result.stderr
        return result.stdout

    cli('init_db.py')
    for script in ['sieve_run.py', 'import_crumbs.py', 'approve.py', 'reset_audit.py',
                   'generate_report.py', 'build_evaluation_package.py']:
        cli(script, '--help')
    (target / 'incoming').mkdir(exist_ok=True)
    original = '# Test-only manual\n\n## Controls\n\nWork is checked and records are kept.\n'
    (target / 'incoming/manual.md').write_text(original, encoding='utf-8')
    cli('promote_source.py', 'manual.md', '--title', 'Synthetic only', '--supplier', name,
        '--language', 'en', '--side', 'DOCUMENT', '--apply')
    cli('extract_text.py', 'DOC-0001', '--apply', cwd=target)
    cli('chunk_document.py', 'DOC-0001', '--apply')
    cli('validate_chunks.py', '--no-record')
    assert (target / 'work/derived/DOC-0001.txt').is_file()
    assert (target / 'work/derived/chunks/DOC-0001.json').is_file()
    assert (target / 'work/manifests/raw_sources.csv').read_text(encoding='utf-8').count('DOC-0001') == 1
    assert (target / 'incoming/manual.md').read_text(encoding='utf-8') == original
    with sqlite3.connect(target / 'db/nqa_audit.sqlite') as conn:
        assert conn.execute('select count(*) from documents').fetchone()[0] == 1
        assert conn.execute('select count(*) from document_chunks').fetchone()[0] > 0
        assert conn.execute('select count(*) from crumbs').fetchone()[0] == 0
    for old in ['manifests', 'derived', 'benchmarks', 'out', 'handoffs']:
        assert not (target / old).exists()
    if sibling:
        assert (other / 'owner.txt').read_bytes() == b'untouched'
        assert (other / 'owner.txt').stat().st_mtime_ns == before.st_mtime_ns
    else:
        assert not other.exists()
