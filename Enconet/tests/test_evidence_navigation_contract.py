"""EA0.4 tests for deep links, failure states, safety, and accessibility."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml


ENCONET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENCONET / "scripts"))

import evidence_navigation as navigation  # noqa: E402


CASES = (
    ("crumb", "CRUMB-DOC-0021-APP_B_I-0003"),
    ("document", "DOC-0021"),
    ("chunk", "CHUNK-DOC-0021-0105"),
    ("quote", "QUOTE-DOC-0021-0105-01"),
    ("evaluation", "EVAL-APP_B_I"),
    ("gap", "GAP-APP_B_I-01"),
    ("finding", "FIND-0001"),
    ("action", "ACT-0001"),
)


def contract() -> dict:
    return yaml.safe_load(navigation.CONTRACT.read_text(encoding="utf-8"))


@pytest.mark.parametrize("entity_type,entity_id", CASES)
def test_each_entity_has_one_canonical_round_trip_target(entity_type: str, entity_id: str):
    fragment = f"#evidence/{entity_type}/{entity_id}"
    assert navigation.target(entity_type, entity_id) == fragment
    assert navigation.parse(fragment) == (entity_type, entity_id)


def test_target_builder_rejects_unknown_types_and_noncanonical_ids():
    with pytest.raises(ValueError, match="invalid evidence target"):
        navigation.target("document", "../raw/source.md")
    with pytest.raises(ValueError, match="invalid evidence target"):
        navigation.target("unknown", "DOC-0021")


def test_navigation_id_grammar_matches_the_canonical_id_registry():
    registry = yaml.safe_load(
        (ENCONET / "schemas" / "id_patterns.yml").read_text(encoding="utf-8")
    )["patterns"]
    mapping = {
        "crumb": "crumb_id",
        "document": "doc_id",
        "chunk": "chunk_id",
        "quote": "quote_id",
        "evaluation": "evaluation_id",
        "gap": "gap_id",
        "finding": "finding_id",
        "action": "action_id",
    }
    target_specs = contract()["targets"]["entity_types"]
    assert set(target_specs) == set(mapping)
    for entity_type, registry_name in mapping.items():
        assert target_specs[entity_type]["id_regex"] == registry[registry_name]["regex"]


@pytest.mark.parametrize(
    "fragment",
    (
        "",
        "#evidence/crumb",
        "#evidence/crumb/CRUMB-DOC-0021-APP_B_I-0003/extra",
        "#Evidence/crumb/CRUMB-DOC-0021-APP_B_I-0003",
        "#evidence/crumb/CRUMB%2DDOC%2D0021%2DAPP_B_I%2D0003",
        "#evidence/crumb/CRUMB-DOC-0021-APP_B_I-0003?x=1",
        "https://example.test/#evidence/document/DOC-0021",
        "javascript:alert(1)",
        "#evidence/document/../raw/secret.md",
        "#evidence/document/%2e%2e%2fraw%2fsecret.md",
        "#evidence/document/C:%5Craw%5Csecret.md",
        "#evidence/unknown/DOC-0021",
    ),
)
def test_malformed_encoded_external_and_traversal_targets_are_rejected(fragment: str):
    assert navigation.parse(fragment) is None
    state = navigation.resolve(fragment, set())
    assert state["status"] == "unavailable"
    assert state["message"] == "Evidence unavailable"
    assert state["focus_id"] == "evidence-panel-heading"
    assert state["announce"] is True


def test_unknown_well_formed_target_is_visible_failure_not_blank_panel():
    fragment = "#evidence/crumb/CRUMB-DOC-0021-APP_B_I-9999"
    state = navigation.resolve(fragment, {"#evidence/document/DOC-0021"})
    assert state == {
        "status": "unavailable",
        "message": "Evidence unavailable",
        "requested_target": fragment,
        "focus_id": "evidence-panel-heading",
        "announce": True,
    }


@pytest.mark.parametrize(
    "language,expected",
    (
        ("en", "Evidence unavailable"),
        ("sl", "Dokaz ni na voljo"),
        ("hr", "Dokaz nije dostupan"),
        ("unsupported", "Evidence unavailable"),
    ),
)
def test_unavailable_state_is_localized_with_a_deterministic_fallback(
    language: str, expected: str
):
    state = navigation.resolve("#evidence/document/DOC-9999", set(), language=language)
    assert state["message"] == expected


def test_known_target_resolves_and_places_focus_on_panel_heading():
    fragment = "#evidence/document/DOC-0021"
    state = navigation.resolve(fragment, {fragment})
    assert state["status"] == "resolved"
    assert state["entity_type"] == "document"
    assert state["entity_id"] == "DOC-0021"
    assert state["focus_id"] == "evidence-panel-heading"
    assert state["announce"] is False


@pytest.mark.parametrize(
    "cause,expected",
    (("activate", "push"), ("initial_load", "replace"), ("popstate", "none"), ("hashchange", "none")),
)
def test_browser_history_has_deterministic_back_forward_behavior(cause: str, expected: str):
    assert navigation.history_action(cause) == expected


def test_unknown_history_cause_is_rejected():
    with pytest.raises(ValueError, match="unknown navigation cause"):
        navigation.history_action("timer")


def test_keyboard_focus_no_script_and_print_contract_is_explicit():
    rules = contract()
    assert rules["schema_version"] == "1.0"
    assert rules["interaction"]["controls"] == ["a", "button"]
    assert rules["interaction"]["activation_keys"] == ["Enter", "Space"]
    assert rules["interaction"]["native_activation"] == {
        "a": ["Enter"],
        "button": ["Enter", "Space"],
    }
    assert rules["interaction"]["focus_after_navigation"] == "evidence-panel-heading"
    assert rules["interaction"]["error_announcement"] == {"role": "status", "aria_live": "polite"}
    assert rules["no_script"]["required"] is True
    assert "JavaScript" in rules["no_script"]["message"]
    assert rules["print"]["expand_evidence"] is True
    assert rules["print"]["include_source_metadata"] is True
    assert rules["print"]["hide_interactive_controls"] is True


def test_untrusted_evidence_is_literal_text_never_html_or_an_executable_url():
    hostile = '<img src=x onerror=alert(1)><script>location="https://evil.test"</script>'
    payload = navigation.safe_text(hostile)
    assert payload == {
        "text": hostile,
        "insertion_api": "textContent",
        "trusted_html": False,
        "linkify": False,
    }
    rules = contract()["security"]
    assert rules["external_urls"] == "reject"
    assert rules["path_traversal"] == "reject"
    assert rules["source_html"] == "literal_text"
    assert rules["allowed_url_schemes"] == []
