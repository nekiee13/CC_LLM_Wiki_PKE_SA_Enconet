"""EA3.1 tests for the single typed Markdown citation renderer."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import citation_renderer  # noqa: E402
import generate_report  # noqa: E402
from test_epic11_report import package  # noqa: E402


@pytest.mark.parametrize(
    "entity_type,entity_id",
    (
        ("crumb", "CRUMB-DOC-0021-APP_B_I-0003"),
        ("document", "DOC-0021"),
        ("chunk", "CHUNK-DOC-0021-0105"),
        ("quote", "QUOTE-DOC-0021-0105-01"),
        ("evaluation", "EVAL-APP_B_I"),
        ("gap", "GAP-APP_B_I-01"),
        ("finding", "FIND-0001"),
        ("action", "ACT-0001"),
        ("source", "package"),
    ),
)
def test_each_supported_entity_renders_one_typed_visible_link(entity_type, entity_id):
    rendered = citation_renderer.render(entity_type, entity_id)
    assert rendered == f"[{entity_type}:{entity_id}](#evidence/{entity_type}/{entity_id})"


def test_label_is_markdown_escaped_and_relative_viewer_path_is_url_encoded():
    rendered = citation_renderer.render(
        "document", "DOC-0021", label="Source [A] \\",
        viewer_path="pregled dokaza/čitač.html",
    )
    assert rendered == (
        r"[Source \[A\] \\](pregled%20dokaza/%C4%8Dita%C4%8D.html"
        r"#evidence/document/DOC-0021)"
    )


@pytest.mark.parametrize(
    "entity_type,entity_id,viewer_path",
    (
        ("unsupported", "DOC-0021", None),
        ("document", "", None),
        ("document", "DOC-99999", None),
        ("document", "DOC-0021", "../dashboard.html"),
        ("document", "DOC-0021", "C:/dashboard.html"),
        ("document", "DOC-0021", "https://example.test/dashboard.html"),
    ),
)
def test_invalid_type_id_and_nonportable_path_fail_closed(entity_type, entity_id, viewer_path):
    with pytest.raises(ValueError):
        citation_renderer.render(entity_type, entity_id, viewer_path=viewer_path)


def test_action_has_primary_action_link_and_separate_finding_lineage():
    report = generate_report.render(package())
    line = next(line for line in report.splitlines() if line.startswith("- ") and "ACT-0001" in line)
    assert "[action:ACT-0001](#evidence/action/ACT-0001)" in line
    assert "[finding:FIND-0001](#evidence/finding/FIND-0001)" in line
    assert line.index("action:ACT-0001") < line.index("finding:FIND-0001")


def test_gap_primary_link_is_gap_context_not_recursive_affirmative_evidence():
    report = generate_report.render(package())
    line = next(line for line in report.splitlines() if line.startswith("- ") and "GAP-APP_B_I-01" in line)
    assert line.count("[gap:GAP-APP_B_I-01]") == 1
    assert "[crumb:CRUMB-DOC-0001-APP_B_I-0001]" in line
    assert "gap context" in line


def test_all_report_sections_use_typed_links_without_bare_reference_tokens():
    report = generate_report.render(package())
    labels = re.findall(r"\[((?:crumb|document|gap|finding|action|source):[^]]+)\]", report)
    assert labels
    for label in labels:
        assert re.search(rf"\[{re.escape(label)}\]\([^\s)]+\)", report)
    assert "[source:package](#evidence/source/package)" in report
