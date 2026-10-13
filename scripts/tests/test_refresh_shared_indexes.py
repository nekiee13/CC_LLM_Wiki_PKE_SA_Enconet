import copy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
import prepare_shared_index_snapshot as contract
import refresh_shared_indexes as tool


def test_manifest_cannot_expand_corpus_to_owned_files_or_drop_exclusions():
    tracked = ['Enconet/docs/guide.md', 'Enconet/scripts/run.py',
               'Enconet/CLAUDE.md', 'PKE_SA_NQA1_doc/INDEXING.md']
    manifest = dict(profiles=contract.profiles(tracked), excludes=contract.EXCLUDED,
                    code_excludes=contract.CODE_EXCLUDED,
                    controlled_excludes=contract.CONTROLLED_EXCLUDED,
                    global_excludes=contract.GLOBAL_EXCLUDED)
    tool.validate_contract(manifest, tracked)
    changed = copy.deepcopy(manifest)
    changed['profiles']['PKE_SA_NQA1_Enconet_docs'].append('CLAUDE.md')
    with pytest.raises(ValueError, match='neutral committed contract'):
        tool.validate_contract(changed, tracked)
    changed = copy.deepcopy(manifest)
    changed['excludes'] = []
    with pytest.raises(ValueError, match='neutral committed contract'):
        tool.validate_contract(changed, tracked)
