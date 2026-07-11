"""Appendix B runtime facade over the ADR-0003 canonical contract."""
from typing import Dict, List

from ..contract import canonical_codes, load_contract

_CONTRACT = load_contract()


class AppBTemplate:
    TEMPLATE_ID = _CONTRACT["template"]["id"]
    TEMPLATE_VERSION = _CONTRACT["template"]["version"]
    TAXONOMY_ID = _CONTRACT["template"]["taxonomy_id"]
    CRITERIA = list(_CONTRACT["criteria"])
    CANONICAL_CODES = canonical_codes()
    RECORD_SIDE_VALUES = list(_CONTRACT["enums"]["record_side"])
    RULE_STRENGTH_VALUES = list(_CONTRACT["enums"]["rule_strength"])
    ITEM_TYPE_VALUES = list(_CONTRACT["enums"]["item_type"])

    @classmethod
    def get_criterion_ids(cls) -> List[str]:
        return [entry["criterion_id"] for entry in cls.CRITERIA]

    @classmethod
    def get_criterion_names(cls) -> List[str]:
        return [entry["criterion_name"] for entry in cls.CRITERIA]

    @classmethod
    def get_criterion_map(cls) -> Dict[str, str]:
        return {entry["criterion_id"]: entry["criterion_name"] for entry in cls.CRITERIA}

    @classmethod
    def get_ref_codes(cls) -> List[str]:
        return [entry["ref_code"] for entry in cls.CANONICAL_CODES]

    @classmethod
    def validate_criterion_id(cls, criterion_id: str) -> bool:
        return criterion_id in cls.get_criterion_ids()

    @classmethod
    def validate_criterion_name(cls, criterion_id: str, criterion_name: str) -> bool:
        return cls.get_criterion_map().get(criterion_id) == criterion_name
