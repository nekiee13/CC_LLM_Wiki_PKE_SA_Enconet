import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
import pytest

from prepare_supplier_cleanup_batch import markdown_references, relocation_aliases, directory_preflight


def test_current_report_links_change_without_altering_scores_or_quotes():
    original = b'# Report\nScore: 77.8%\nQuoted old.html text stays.\n[CRUMB-1](old.html#crumb:1)\n[Source](raw.md)\n'
    adapted, count = markdown_references(original, {'old.html': 'dashboard_light.html'})
    assert count == 1
    assert adapted == original.replace(b'](old.html#', b'](dashboard_light.html#')
    assert original.startswith(b'# Report\nScore: 77.8%')


def test_relocations_include_routed_history_aliases():
    result = relocation_aliases([{'source': 'Acme/out/old/package.json',
                                 'destination': 'Acme/outputs/RUN-1/evaluation_package.json'}], 'Acme')
    assert result['paths'] == {'out/old/package.json': 'outputs/RUN-1/evaluation_package.json',
                               'work/validation/old/package.json': 'outputs/RUN-1/evaluation_package.json'}


def test_relocations_reject_ambiguous_or_foreign_supplier():
    rows = [{'source': 'Acme/out/file', 'destination': 'Acme/outputs/a'},
            {'source': 'Acme/work/validation/file', 'destination': 'Acme/outputs/b'}]
    with pytest.raises(ValueError, match='ambiguous'):
        relocation_aliases(rows, 'Acme')
    with pytest.raises(ValueError, match='foreign'):
        relocation_aliases(rows[:1], 'Other')


def test_directory_preflight_detects_unmapped_files_and_empty_backup(tmp_path):
    (tmp_path / 'Acme/out/run').mkdir(parents=True)
    (tmp_path / 'Acme/backup').mkdir()
    (tmp_path / 'Acme/out/run/mapped.txt').write_bytes(b'mapped')
    extra = tmp_path / 'Acme/out/run/unmapped.txt'
    extra.write_bytes(b'keep')
    plan = {'files': [{'source': 'Acme/out/run/mapped.txt', 'destination': 'Acme/work/validation/run/mapped.txt'}]}
    result = directory_preflight(tmp_path, 'Acme', plan)
    assert not result['passed']
    assert result['uncovered_files'] == ['Acme/out/run/unmapped.txt']
    assert result['empty_home_moves'][0]['destination'] == 'Acme/work/backup'
    assert result['prune_source_parents'] == ['Acme/out/run', 'Acme/out']
    assert extra.read_bytes() == b'keep'
    assert not (tmp_path / 'Acme/work').exists()


def test_directory_preflight_rejects_foreign_supplier(tmp_path):
    with pytest.raises(ValueError, match='foreign'):
        directory_preflight(tmp_path, 'Acme', {'files': [{'source': 'Other/out/x', 'destination': 'Other/work/x'}]})


def test_unmapped_empty_subfolder_gets_exact_retained_home(tmp_path):
    (tmp_path / 'Acme/out/date/empty').mkdir(parents=True)
    (tmp_path / 'Acme/out/date/mapped').write_bytes(b'mapped')
    result = directory_preflight(tmp_path, 'Acme', {'files': [
        {'source': 'Acme/out/date/mapped', 'destination': 'Acme/work/validation/date/mapped'}]})
    assert result['passed']
    assert result['empty_home_moves'][0]['destination'] == 'Acme/work/validation/date/empty'


def test_directory_walk_access_failure_is_not_silently_passed(tmp_path, monkeypatch):
    import prepare_supplier_cleanup_batch as preparation
    (tmp_path / 'Acme/out').mkdir(parents=True)
    def denied(path, **options):
        options['onerror'](PermissionError('denied'))
        return iter(())
    monkeypatch.setattr(preparation.os, 'walk', denied)
    result = directory_preflight(tmp_path, 'Acme', {'files': []})
    assert not result['passed']
    assert 'denied' in result['blocked_homes'][0]['reason']
