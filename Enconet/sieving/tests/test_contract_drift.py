import json
from pathlib import Path, PurePosixPath

from src.json_extractor.config import Config
from src.json_extractor.contract import load_contract
from src.json_extractor.pipeline import run_pipeline
from src.json_extractor.query.schema import QuerySchema
from src.json_extractor.templates.app_b import AppBTemplate


ENCONET_ROOT = Path(__file__).resolve().parents[2]
PROMPT = ENCONET_ROOT / "docs" / "context" / "31 Sieving - Crumb generation.md"


def test_owner_matches_runtime_query_and_export_tables(tmp_path):
    owner = load_contract()
    config = Config(data_dir=tmp_path / "data", config_dir=tmp_path / "config")

    assert config.get_canonical_criteria() == owner["criteria"] == AppBTemplate.CRITERIA
    assert [entry["ref_code"] for entry in config.get_canonical_codes()] == AppBTemplate.get_ref_codes()
    assert AppBTemplate.ITEM_TYPE_VALUES == owner["enums"]["item_type"]
    assert QuerySchema.get_field_names() == [entry["name"] for entry in owner["query_fields"]]
    assert QuerySchema.get_field("criterion_id").allowed_values == AppBTemplate.get_criterion_ids()
    assert QuerySchema.get_field("criterion_name").allowed_values == AppBTemplate.get_criterion_names()
    assert QuerySchema.get_field("item_type").allowed_values == AppBTemplate.ITEM_TYPE_VALUES
    assert config.default_columns == owner["columns"]["default"]
    assert config.all_columns == owner["columns"]["all"]


def test_owner_matches_prompt_controlled_vocabulary():
    owner = load_contract()
    prompt = PROMPT.read_text(encoding="utf-8")
    for criterion in owner["criteria"]:
        assert criterion["criterion_id"] in prompt
        assert criterion["criterion_name"] in prompt
    for values in owner["enums"].values():
        for value in values:
            assert value in prompt
    for code in owner["canonical_codes"]:
        assert code["ref_code"] in prompt


def test_existing_data_revalidates_without_migration():
    data_dir = ENCONET_ROOT / "sieving" / "DATA"
    paths = sorted(data_dir.rglob("*.json"))
    result = run_pipeline(file_paths=paths)

    assert len(paths) == 68
    manifest = json.loads((ENCONET_ROOT / "schemas" / "sieving_data_migration_manifest.yml")
                          .read_text(encoding="utf-8"))
    assert result.files_processed == len(paths) == manifest["files_total"]
    assert result.items_loaded == manifest["items_loaded"]
    actual_bad = [
        {"path": PurePosixPath(Path(issue.path).relative_to(data_dir)).as_posix(),
         "error_type": issue.error_type}
        for issue in result.bad_files
    ]
    actual_validation = [
        {"path": PurePosixPath(Path(issue.file_path).relative_to(data_dir)).as_posix(),
         "item_id": issue.item_id, "rule_id": issue.rule_id,
         "severity": issue.severity, "message": issue.message}
        for issue in result.validation_errors
    ]
    assert actual_bad == manifest["bad_files"]
    assert actual_validation == manifest["validation_issues"]
    assert list(result.df.columns) == load_contract()["columns"]["all"]
