import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from prepare_supplier_cleanup_batch import markdown_references


def test_current_report_links_change_without_altering_scores_or_quotes():
    original = b'# Report\nScore: 77.8%\nQuoted old.html text stays.\n[CRUMB-1](old.html#crumb:1)\n[Source](raw.md)\n'
    adapted, count = markdown_references(original, {'old.html': 'dashboard_light.html'})
    assert count == 1
    assert adapted == original.replace(b'](old.html#', b'](dashboard_light.html#')
    assert original.startswith(b'# Report\nScore: 77.8%')
