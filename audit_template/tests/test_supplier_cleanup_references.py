import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
import pytest

from prepare_supplier_cleanup_batch import markdown_references, relocation_aliases


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
