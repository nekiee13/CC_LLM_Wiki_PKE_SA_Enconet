from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"


def test_concept_cards_cover_all_18_criteria():
    data = yaml.safe_load((PROMPTS / "appb_concepts.yml").read_text(encoding="utf-8"))
    criteria = data["criteria"]
    assert len(criteria) == 18
    assert set(criteria) == {f"APP_B_{roman}" for roman in (
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
        "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"
    )}
    for card in criteria.values():
        assert card["intent"].strip()
        assert len(card["evidence_signals"]) >= 4


def test_concept_recall_prompt_requires_two_pass_fuzzy_collection():
    prompt = (PROMPTS / "appb_document_v2_concept_recall.md").read_text(encoding="utf-8")
    assert "Pass 1" in prompt
    assert "Pass 2" in prompt
    assert "Do not use a fixed maximum number of crumbs" in prompt
    assert "candidate_lead" in prompt
    assert "exact source quote" in prompt


def test_concept_recall_prompt_requests_source_supported_context_anchors():
    prompt = (PROMPTS / "appb_document_v2_concept_recall.md").read_text(encoding="utf-8")
    assert "Evidence context anchors" in prompt
    assert "evidence_type" in prompt
    assert "project_ref" in prompt
    assert "guess a project" in prompt
    assert "CONTEXT_FIELDS" in prompt


def test_v2_is_the_owner_activated_document_prompt():
    active = yaml.safe_load((PROMPTS / "active.yml").read_text(encoding="utf-8"))
    assert active["active"]["DOCUMENT"] == "appb_document_v2_concept_recall"
