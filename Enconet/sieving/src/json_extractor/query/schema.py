# ------------------------
# src/json_extractor/query/schema.py
# ------------------------
"""
Query schema: defines queryable fields and their types.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class FieldType(Enum):
    """Field data types for query operations."""
    STRING = "string"
    ENUM = "enum"
    NUMBER = "number"


@dataclass
class FieldDef:
    """Definition of a queryable field."""
    name: str
    field_type: FieldType
    description: str
    allowed_values: Optional[List[str]] = None  # For ENUM types
    record_side_filter: Optional[str] = None  # "RULE" or "DOCUMENT" if field is side-specific


class QuerySchema:
    """
    Schema for queryable fields in normalized records.
    
    Supports:
    - Field type definitions
    - Controlled vocabularies for enum fields
    - Record-side specificity (RULE-only, DOCUMENT-only)
    """
    
    FIELDS = [
        # Core discriminators
        FieldDef(
            name="record_side",
            field_type=FieldType.ENUM,
            description="RULE or DOCUMENT discriminator",
            allowed_values=["RULE", "DOCUMENT"],
        ),
        
        # Taxonomy fields
        FieldDef(
            name="criterion_id",
            field_type=FieldType.ENUM,
            description="Appendix B criterion ID (APP_B_I through APP_B_XVIII)",
            allowed_values=[
                "APP_B_I", "APP_B_II", "APP_B_III", "APP_B_IV", "APP_B_V", "APP_B_VI",
                "APP_B_VII", "APP_B_VIII", "APP_B_IX", "APP_B_X", "APP_B_XI", "APP_B_XII",
                "APP_B_XIII", "APP_B_XIV", "APP_B_XV", "APP_B_XVI", "APP_B_XVII", "APP_B_XVIII",
            ],
        ),
        
        FieldDef(
            name="criterion_name",
            field_type=FieldType.ENUM,
            description="Canonical criterion name",
            allowed_values=[
                "Organization",
                "Quality Assurance Program",
                "Design Control",
                "Procurement Document Control",
                "Instructions, Procedures, and Drawings",
                "Document Control",
                "Control of Purchased Material, Equipment, and Services",
                "Identification and Control of Materials, Parts, and Components",
                "Control of Special Processes",
                "Inspection",
                "Test Control",
                "Control of Measuring and Test Equipment",
                "Handling, Storage, and Shipping",
                "Inspection, Test, and Operating Status",
                "Nonconforming Materials, Parts, or Components",
                "Corrective Action",
                "Quality Assurance Records",
                "Audits",
            ],
        ),
        
        FieldDef(
            name="item_type",
            field_type=FieldType.ENUM,
            description="Type of extracted item",
            allowed_values=[
                "requirement", "process_step", "role_responsibility", "definition",
                "control", "record", "reference", "finding", "recommendation",
                "action", "status_statement", "other",
            ],
        ),
        
        # Document metadata
        FieldDef(
            name="doc_id",
            field_type=FieldType.STRING,
            description="Document identifier",
        ),
        
        FieldDef(
            name="filename",
            field_type=FieldType.STRING,
            description="Source filename",
        ),
        
        FieldDef(
            name="title",
            field_type=FieldType.STRING,
            description="Document title",
        ),
        
        FieldDef(
            name="revision",
            field_type=FieldType.STRING,
            description="Document revision",
        ),
        
        # Content
        FieldDef(
            name="statement",
            field_type=FieldType.STRING,
            description="Extracted statement text",
        ),
        
        # RULE-only fields
        FieldDef(
            name="rule_source_rules",
            field_type=FieldType.ENUM,
            description="Canonical rule code (RULE-only)",
            allowed_values=["10CFR50_APPB", "10CFR21"],
            record_side_filter="RULE",
        ),
        
        FieldDef(
            name="rule_locator",
            field_type=FieldType.STRING,
            description="Rule locator within source (RULE-only)",
            record_side_filter="RULE",
        ),
        
        FieldDef(
            name="rule_key",
            field_type=FieldType.STRING,
            description="Composite join key (RULE-only)",
            record_side_filter="RULE",
        ),
        
        FieldDef(
            name="rule_strength",
            field_type=FieldType.ENUM,
            description="Rule obligation level (RULE-only)",
            allowed_values=["MANDATORY", "NON_MANDATORY"],
            record_side_filter="RULE",
        ),
        
        # DOCUMENT-only fields
        FieldDef(
            name="rule_ref_keys",
            field_type=FieldType.STRING,
            description="Semicolon-joined rule reference keys (DOCUMENT-only)",
            record_side_filter="DOCUMENT",
        ),
        
        FieldDef(
            name="rule_ref_codes",
            field_type=FieldType.STRING,
            description="Semicolon-joined ref codes (DOCUMENT-only)",
            record_side_filter="DOCUMENT",
        ),
        
        FieldDef(
            name="rule_ref_locators",
            field_type=FieldType.STRING,
            description="Semicolon-joined ref locators (DOCUMENT-only)",
            record_side_filter="DOCUMENT",
        ),
    ]
    
    @classmethod
    def get_field(cls, name: str) -> Optional[FieldDef]:
        """Get field definition by name."""
        for field in cls.FIELDS:
            if field.name == name:
                return field
        return None
    
    @classmethod
    def get_field_names(cls) -> List[str]:
        """Get list of all queryable field names."""
        return [f.name for f in cls.FIELDS]
    
    @classmethod
    def get_enum_fields(cls) -> List[FieldDef]:
        """Get all enum-type fields."""
        return [f for f in cls.FIELDS if f.field_type == FieldType.ENUM]
    
    @classmethod
    def get_string_fields(cls) -> List[FieldDef]:
        """Get all string-type fields."""
        return [f for f in cls.FIELDS if f.field_type == FieldType.STRING]
