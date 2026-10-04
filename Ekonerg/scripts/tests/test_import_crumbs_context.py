import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from import_crumbs import _validate_context_requirements


def test_importer_rejects_evidence_type_without_source_anchor():
    with pytest.raises(ValueError, match="requires at least one source context anchor"):
        _validate_context_requirements([{"evidence_type": "objective_record"}])


def test_importer_accepts_evidence_type_with_one_source_anchor():
    _validate_context_requirements([
        {"evidence_type": "objective_record", "context": {"source_revision": "rev. 2"}}
    ])
