"""Queryable fields derived from the ADR-0003 canonical contract."""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ..contract import load_contract


class FieldType(Enum):
    STRING = "string"
    ENUM = "enum"
    NUMBER = "number"


@dataclass
class FieldDef:
    name: str
    field_type: FieldType
    description: str
    allowed_values: Optional[List[str]] = None
    record_side_filter: Optional[str] = None


def _build_fields() -> list[FieldDef]:
    contract = load_contract()
    derived = {
        "criterion_ids": [entry["criterion_id"] for entry in contract["criteria"]],
        "criterion_names": [entry["criterion_name"] for entry in contract["criteria"]],
        "ref_codes": [entry["ref_code"] for entry in contract["canonical_codes"]],
        "regulation_ref_codes": [entry["ref_code"] for entry in contract["canonical_codes"]
                                 if entry.get("ref_type") == "REGULATION"],
    }
    fields = []
    for entry in contract["query_fields"]:
        values = None
        if "enum" in entry:
            values = list(contract["enums"][entry["enum"]])
        elif "values_from" in entry:
            values = derived[entry["values_from"]]
        fields.append(FieldDef(
            entry["name"], FieldType(entry["type"]), entry["description"], values,
            entry.get("record_side"),
        ))
    return fields


class QuerySchema:
    FIELDS = _build_fields()

    @classmethod
    def get_field(cls, name: str) -> Optional[FieldDef]:
        return next((field for field in cls.FIELDS if field.name == name), None)

    @classmethod
    def get_field_names(cls) -> List[str]:
        return [field.name for field in cls.FIELDS]

    @classmethod
    def get_enum_fields(cls) -> List[FieldDef]:
        return [field for field in cls.FIELDS if field.field_type == FieldType.ENUM]

    @classmethod
    def get_string_fields(cls) -> List[FieldDef]:
        return [field for field in cls.FIELDS if field.field_type == FieldType.STRING]
