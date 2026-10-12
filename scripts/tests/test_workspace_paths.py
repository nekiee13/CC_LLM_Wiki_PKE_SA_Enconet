import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('workspace_paths', Path(__file__).parents[1] / 'workspace_paths.py')
paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paths)


@pytest.mark.parametrize('home', ['doc', 'PKE_SA_NQA1_doc'])
def test_explicit_documentation_home_in_mixed_tree(tmp_path, home):
    (tmp_path / 'workspace-layout.json').write_text(json.dumps(
        {'schema_version': 1, 'documentation_root': home}), encoding='utf-8')
    for area in ('doc', 'PKE_SA_NQA1_doc'):
        (tmp_path / area).mkdir()
        (tmp_path / area / 'GUIDANCE_PAIRS.json').write_text(area)
    assert paths.documentation('GUIDANCE_PAIRS.json', root=tmp_path).read_text() == home
    with pytest.raises(ValueError):
        paths.documentation('../outside', root=tmp_path)


def test_documentation_does_not_infer_missing_or_bad_configuration(tmp_path):
    with pytest.raises(FileNotFoundError):
        paths.documentation(root=tmp_path)
    (tmp_path / 'workspace-layout.json').write_text(
        '{"schema_version":1,"documentation_root":"../outside"}', encoding='utf-8')
    with pytest.raises(ValueError):
        paths.documentation(root=tmp_path)
    assert not list(tmp_path.glob('doc'))
